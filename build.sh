#!/bin/bash

# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. Statik dosyaları topla (WhiteNoise için)
python manage.py collectstatic --noinput

# 3. Veritabanı miqrasiyalarını icra et (Opsiyonel - Canlı DB bağlıysa)
python manage.py migrate --noinput