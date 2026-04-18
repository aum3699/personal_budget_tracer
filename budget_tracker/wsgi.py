"""
WSGI config for budget_tracker project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""
import os

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_tracker.settings')

# Run migrations automatically on startup (handles Render's no-shell limitation)
try:
    call_command('migrate', '--noinput')
except Exception as e:
    print(f"Warning: Automatic migration failed: {e}")

application = get_wsgi_application()
