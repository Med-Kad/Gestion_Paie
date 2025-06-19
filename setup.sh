#!/bin/bash

echo "🚀 Initialisation de l'environnement de développement Django + MongoDB + Tailwind..."

# Créer et activer un environnement virtuel
python -m venv venv
source venv/bin/activate

# Installer les dépendances Python
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

# Installer les dépendances JavaScript
echo "🎨 Installation des dépendances npm (Tailwind)..."
npm install

# Compiler Tailwind en mode dev
echo "💅 Compilation de Tailwind CSS..."
npx tailwindcss -i ./GestionApp/static/styles/static.css -o ./GestionApp/static/styles/output.css --watch &
TAILWIND_PID=$!

# Lancer le serveur Django
echo "🚀 Lancement du serveur Django..."
python manage.py runserver

# Kill Tailwind watcher après interruption
trap "kill $TAILWIND_PID" EXIT
