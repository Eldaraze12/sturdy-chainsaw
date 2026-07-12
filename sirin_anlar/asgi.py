"""ASGI konfiqurasiyası - asinxron serverlər üçün."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sirin_anlar.settings")

application = get_asgi_application()
