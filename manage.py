#!/usr/bin/env python
"""Django-nun komandline idarəetmə vasitəsi."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sirin_anlar.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django tapılmadı. Virtual mühiti aktivləşdirdiyinizə və "
            "'pip install -r requirements.txt' etdiyinizə əmin olun."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
