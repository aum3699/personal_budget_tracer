release: python manage.py migrate && python manage.py migrate auth
web: gunicorn budget_tracker.wsgi:application --bind 0.0.0.0:${PORT:-10000}
