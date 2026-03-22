"""
URL configuration for budget_tracker project.

The `urlpatterns` list routes URLs to views.
"""
import os
import logging
from django.urls import path, include
from django.contrib import admin
from django.http import HttpResponse

logger = logging.getLogger(__name__)

def simple_test(request):
    return HttpResponse("App is working!")

def db_test(request):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    return HttpResponse("Database OK!")

urlpatterns = [
    path('test/', simple_test, name='simple_test'),
    path('db-test/', db_test, name='db_test'),
    path('', include('budget.urls')),
    path('admin/', admin.site.urls),
]
