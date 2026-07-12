#!/bin/bash

# 1. Python paket yükleyicisini güncelle ve bağımlılıkları yükle
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# 2. Statik dosyaları topla
python3 manage.py collectstatic --noinput
