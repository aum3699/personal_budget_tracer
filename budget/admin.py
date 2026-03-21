"""
Django admin configuration for budget app
"""
from django.contrib import admin
from .models import Transaction, UserProfile


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'type', 'category', 'amount', 'date']
    list_filter = ['type', 'category', 'date']
    search_fields = ['user__username', 'category', 'note']
    date_hierarchy = 'date'
    ordering = ['-date']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_admin']
    list_filter = ['is_admin']
    search_fields = ['user__username', 'user__email']
