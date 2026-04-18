release: python manage.py migrate --noinput
web: gunicorn budget_tracker.wsgi:application --bind 0.0.0.0:${PORT:-10000}
