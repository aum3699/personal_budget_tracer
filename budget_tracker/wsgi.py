"""
WSGI config for budget_tracker project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""
import os

from django.core.wsgi import get_wsgi_application
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_tracker.settings')

# Create superuser if none exists (fallback if releaseCommand didn't run)
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
    print(f"⚠️  Superuser creation skipped: {e}")

application = get_wsgi_application()
