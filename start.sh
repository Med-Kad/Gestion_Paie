#!/bin/sh

python manage.py makemigrations
python manage.py migrate

# Variables d'environnement pour le super utilisateur
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=admin@example.com
export DJANGO_SUPERUSER_PASSWORD=admin

# Création du super utilisateur
python manage.py createsuperuser --noinput || echo "Super utilisateur déjà existant"


python manage.py collectstatic --noinput

gunicorn --bind 0.0.0.0:8000 Gestion_Paie.wsgi:application