"""Views for Personal Budget Tracker - Optimized with timezone support"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime
from calendar import monthrange
import csv
from django.contrib.auth.models import User

from .models import Transaction, UserProfile
from .forms import TransactionForm, MonthFilterForm, LoginForm, RegistrationForm

CURRENCY = '₹'

def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect(request.GET.get('next', 'index'))
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html', {'form': LoginForm()})

def user_logout(request):
    logout(request)
    messages.info(request, 'Logged out.')
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email exists')
            else:
                user = form.save()
                UserProfile.objects.create(user=user, is_admin=False)
                messages.success(request, 'Registered! Login now.')
                return redirect('login')
    return render(request, 'register.html', {'form': RegistrationForm()})

@login_required
def index(request):
    form = TransactionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        txn = form.save(commit=False)
        txn.user = request.user
        txn.save()
        messages.success(request, 'Added!')
        return redirect('index')
    
    month = request.GET.get('month', datetime.now().strftime('%m'))
    year = request.GET.get('year', str(datetime.now().year))
    start = timezone.make_aware(datetime(int(year), int(month), 1))
    end = timezone.make_aware(datetime(int(year), int(month), monthrange(int(year), int(month))[1], 23, 59, 59))
    
    txns = Transaction.objects.filter(user=request.user, date__range=(start, end)).order_by('-date')
    income = sum(t.amount for t in txns if t.type == 'Income')
    expense = sum(t.amount for t in txns if t.type == 'Expense')
    
    return render(request, 'index.html', {
        'form': TransactionForm(), 
        'filter_form': MonthFilterForm(initial={'month': month, 'year': year}),
        'transactions': txns, 
        'income': income, 
        'expense': expense, 
        'balance': income - expense,
        'current_month': month, 
        'current_year': year, 
        'currency_symbol': CURRENCY
    })

@login_required
def edit_transaction(request, transaction_id):
    txn = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=txn)
        if form.is_valid(): 
            form.save()
            messages.success(request, 'Updated!')
            return redirect('index')
    return render(request, 'edit_transaction.html', {'form': TransactionForm(instance=txn), 'transaction_id': transaction_id})

@login_required
def delete_transaction(request, transaction_id):
    get_object_or_404(Transaction, id=transaction_id, user=request.user).delete()
    messages.success(request, 'Deleted!')
    return redirect('index')

@login_required
def export_csv(request):
    month = request.GET.get('month', datetime.now().strftime('%m'))
    year = request.GET.get('year', str(datetime.now().year))
    start = timezone.make_aware(datetime(int(year), int(month), 1))
    end = timezone.make_aware(datetime(int(year), int(month), monthrange(int(year), int(month))[1], 23, 59, 59))
    txns = Transaction.objects.filter(user=request.user, date__range=(start, end)).order_by('-date')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=budget_{year}_{month}.csv'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Type', 'Category', 'Amount', 'Note'])
    for t in txns:
        writer.writerow([t.date.strftime('%Y-%m-%d'), t.type, t.category, t.amount, t.note])
    return response

def check_admin(request):
    return hasattr(request.user, 'profile') and request.user.profile.is_admin

@login_required
def admin_dashboard(request):
    if not check_admin(request):
        messages.error(request, 'Admin only!')
        return redirect('index')
    from django.db.models import Sum
    users = User.objects.all()
    stats = []
    for u in users:
        inc = u.transactions.filter(type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
        exp = u.transactions.filter(type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
        stats.append({'user': u, 'transaction_count': u.transactions.count(), 'total_income': inc, 'total_expense': exp, 'balance': inc - exp})
    return render(request, 'admin/dashboard.html', {
        'total_users': users.count(), 
        'total_transactions': Transaction.objects.count(),
        'total_income': Transaction.objects.filter(type='Income').aggregate(Sum('amount'))['amount__sum'] or 0,
        'total_expense': Transaction.objects.filter(type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0,
        'recent_transactions': Transaction.objects.all().order_by('-date')[:10],
        'user_stats': stats,
        'currency_symbol': CURRENCY
    })

@login_required
def admin_users(request):
    if not check_admin(request):
        messages.error(request, 'Admin only!')
        return redirect('index')
    return render(request, 'admin/users.html', {'users': User.objects.all()})

@login_required
def admin_transactions(request):
    if not check_admin(request):
        messages.error(request, 'Admin only!')
        return redirect('index')
    from django.core.paginator import Paginator
    page = request.GET.get('page', 1)
    paginator = Paginator(Transaction.objects.all().order_by('-date'), 50)
    all_txns = Transaction.objects.all()
    total_income = sum(t.amount for t in all_txns if t.type == 'Income')
    total_expense = sum(t.amount for t in all_txns if t.type == 'Expense')
    return render(request, 'admin/transactions.html', {
        'page_obj': paginator.get_page(page),
        'total_income': total_income,
        'total_expense': total_expense,
        'currency_symbol': CURRENCY
    })

@login_required
def admin_user_detail(request, user_id):
    if not check_admin(request):
        messages.error(request, 'Admin only!')
        return redirect('index')
    user = get_object_or_404(User, id=user_id)
    txns = user.transactions.all()
    income = sum(t.amount for t in txns if t.type == 'Income')
    expense = sum(t.amount for t in txns if t.type == 'Expense')
    return render(request, 'admin/user_detail.html', {
        'user': user, 
        'transactions': txns.order_by('-date'),
        'total_income': income,
        'total_expense': expense,
        'balance': income - expense,
        'currency_symbol': CURRENCY
    })

@login_required
def make_admin(request, user_id):
    if not check_admin(request):
        messages.error(request, 'Admin only!')
        return redirect('index')
    profile = get_object_or_404(UserProfile, user_id=user_id)
    profile.is_admin = True
    profile.save()
    messages.success(request, 'Made admin!')
    return redirect('admin_users')

@login_required
def remove_admin(request, user_id):
    if not check_admin(request):
        messages.error(request, 'Admin only!')
        return redirect('index')
    if user_id == request.user.id:
        messages.error(request, 'Cannot remove yourself!')
        return redirect('admin_users')
    profile = get_object_or_404(UserProfile, user_id=user_id)
    profile.is_admin = False
    profile.save()
    messages.success(request, 'Removed admin!')
    return redirect('admin_users')

@login_required
def delete_user(request, user_id):
    if not check_admin(request):
        messages.error(request, 'Admin only!')
        return redirect('index')
    if user_id == request.user.id:
        messages.error(request, 'Cannot delete yourself!')
        return redirect('admin_users')
    user = get_object_or_404(User, id=user_id)
    Transaction.objects.filter(user=user).delete()
    try:
        user.profile.delete()
    except:
        pass
    user.delete()
    messages.success(request, 'Deleted!')
    return redirect('admin_users')
