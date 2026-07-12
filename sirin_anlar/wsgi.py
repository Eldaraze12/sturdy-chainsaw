"""WSGI konfiqurasiyası - istehsalat serverləri (gunicorn, uWSGI) üçün."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sirin_anlar.settings")

application = get_wsgi_application()
