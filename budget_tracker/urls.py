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

def test_error(request):
    try:
        from django.conf import settings
        db_url = os.environ.get('DATABASE_URL', 'NOT SET')
        return HttpResponse(f"DEBUG={settings.DEBUG}<br>DATABASE_URL={db_url[:50]}...")
    except Exception as e:
        import traceback
        return HttpResponse(f"Error: {str(e)}<br>{traceback.format_exc()}", status=500)

urlpatterns = [
    path('test-error/', test_error, name='test_error'),
    path('', include('budget.urls')),
    path('admin/', admin.site.urls),
]
