"""
URL configuration for budget_tracker project.

The `urlpatterns` list routes URLs to views.
"""
from django.urls import path, include

urlpatterns = [
    path('', include('budget.urls')),
]
