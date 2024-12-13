# # Étape 1 : Construire l'application Django
# FROM python:3.11-slim AS django

# # Définir le répertoire de travail dans le conteneur
# WORKDIR /app

# # Copier les fichiers du projet dans l'image
# COPY . /app

# # Installer les dépendances du projet
# RUN pip install --no-cache-dir -r requirements.txt

# # Collecter les fichiers statiques
# RUN python manage.py collectstatic --noinput

# # Étape 2 : Construire les fichiers Tailwind et JavaScript avec Node.js
# FROM node:18-alpine AS node

# # Définir le répertoire de travail
# WORKDIR /app

# # Copier uniquement les fichiers nécessaires pour Node.js
# COPY package.json package-lock.json /app/

# # Installer les dépendances Node.js
# RUN npm install

# # Copier tout le projet pour accéder aux fichiers source
# COPY . /app

# # Construire les fichiers CSS et JavaScript
# RUN npm run build-css


# # Étape 3 : Configurer Nginx pour servir l'application
# FROM nginx:latest AS production

# # Copier les fichiers statiques générés par Django et Node.js dans l'image Nginx
# COPY --from=django /app/staticfiles /usr/share/nginx/html/static
# COPY --from=node /app/staticfiles/styles /usr/share/nginx/html/static

# # Copier la configuration personnalisée de Nginx
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# # Exposer le port utilisé par Nginx
# EXPOSE 80

# # Commande par défaut pour démarrer Nginx
# CMD ["nginx", "-g", "daemon off;"]



# Étape 1 : Construire l'application Django
FROM python:3.11-slim AS django

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers du projet dans l'image
COPY . /app

# Installer les dépendances du projet
RUN pip install --no-cache-dir -r requirements.txt

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port 8000
EXPOSE 8000

# Définir la commande de démarrage
CMD ["./start.sh"]

