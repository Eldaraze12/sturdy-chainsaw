#!/bin/bash

# Bağımlılıkları yükle
pip install -r requirements.txt

# Statik dosyaları 'staticfiles' klasörüne topla
python manage.py collectstatic --noinput