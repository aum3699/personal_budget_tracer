"""
WSGI config for budget_tracker project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""
import os

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_tracker.settings')

# Run migrations automatically on startup (handles Render's no-shell limitation)
try:
    call_command('migrate', '--noinput')
except Exception as e:
    print(f"Warning: Automatic migration failed: {e}")

# Create superuser if none exists (for Render admin access)
try:
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("✅ Superuser created: admin / admin123")
except Exception as e:
    print(f"Warning: Superuser creation failed: {e}")

application = get_wsgi_application()
