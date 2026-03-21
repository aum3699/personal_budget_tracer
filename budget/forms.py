"""
Forms for Personal Budget Tracker
Converted from Flask-WTF to Django forms
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Transaction
from datetime import datetime


class TransactionForm(forms.ModelForm):
    """Form for adding/editing transactions"""
    type = forms.ChoiceField(choices=Transaction.TYPE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    category = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Category'
    }))
    amount = forms.FloatField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Amount',
        'step': '0.01'
    }))
    note = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Note (optional)'
    }))
    
    class Meta:
        model = Transaction
        fields = ['type', 'category', 'amount', 'note']


class MonthFilterForm(forms.Form):
    """Form for filtering transactions by month/year"""
    MONTH_CHOICES = [
        ('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
        ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'),
        ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ]
    
    month = forms.ChoiceField(choices=MONTH_CHOICES, initial=datetime.now().strftime('%m'), 
                              widget=forms.Select(attrs={'class': 'form-control'}))
    year = forms.ChoiceField(choices=[(str(y), str(y)) for y in range(datetime.now().year - 5, datetime.now().year + 1)],
                             initial=str(datetime.now().year),
                             widget=forms.Select(attrs={'class': 'form-control'}))


class LoginForm(forms.Form):
    """Form for user login"""
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class RegistrationForm(UserCreationForm):
    """Form for user registration"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
