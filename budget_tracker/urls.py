"""
URL configuration for budget_tracker project.

The `urlpatterns` list routes URLs to views.
"""
from django.urls import path, include
from django.contrib import admin
from django.http import HttpResponse

def test_db(request):
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return HttpResponse("Database OK!")
    except Exception as e:
        return HttpResponse(f"Database Error: {str(e)}", status=500)

urlpatterns = [
    path('test-db/', test_db, name='test_db'),
    path('', include('budget.urls')),
    path('admin/', admin.site.urls),
]
