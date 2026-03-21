"""
URL configuration for budget app
"""
from django.urls import path
from . import views

urlpatterns = [
    # Auth URLs
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    
    # Main URLs
    path('', views.index, name='index'),
    path('edit/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    path('delete/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('export/csv/', views.export_csv, name='export_csv'),
    
    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/transactions/', views.admin_transactions, name='admin_transactions'),
    path('admin/user/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path('admin/make_admin/<int:user_id>/', views.make_admin, name='make_admin'),
    path('admin/remove_admin/<int:user_id>/', views.remove_admin, name='remove_admin'),
    path('admin/delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
]
