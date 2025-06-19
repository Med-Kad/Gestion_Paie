# Gestion Paie

Application de gestion de la paie développée avec Django, MongoDB et Tailwind CSS.

---

## ⚙️ Prérequis

- Python 3.9+
- Node.js & npm (pour Tailwind CSS)
- MongoDB (local ou en ligne, ex : MongoDB Atlas)
- pip ou pipenv
- Docker (facultatif mais disponible)

---

## 🚀 Installation (en local sans Docker)

### 1. Cloner le projet

```bash
git clone https://github.com/Med-Kad/Gestion_Paie.git
cd Gestion_Paie
```

### 2. Créer et activer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
```

### 3. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

> Assure-toi que `djongo` ou `mongoengine` est bien listé selon ton choix d'ORM.

### 4. Installer les dépendances JavaScript (pour Tailwind CSS)

```bash
npm install
```

### 5. Compiler Tailwind CSS (en mode dev)

```bash
npx tailwindcss -i ./GestionApp/static/styles/static.css -o ./GestionApp/static/styles/output.css --watch
```

> Tu peux ajuster les chemins si besoin selon ta structure.

---

## 🔐 Configuration de l’environnement

Crée un fichier `.env` à la racine du projet et configure les variables suivantes :

```env
SECRET_KEY=your-secret-key
DEBUG=True
MONGODB_URI=mongodb://localhost:27017/
MONGO_DB_NAME=gestion_paie
```

---

## 🧪 Initialiser la base de données

 
Si tu utilises `djongo`, tu peux effectuer :

```bash
python manage.py makemigrations
python manage.py migrate
```

Créer un super utilisateur :

```bash
python manage.py createsuperuser
```

---

## ▶️ Lancer le serveur

```bash
python manage.py runserver
```

---

## 🐳 Utilisation avec Docker (optionnel)

```bash
docker-compose up --build
```

> Assure-toi que la variable d'environnement `MONGODB_URI` est correctement passée si tu utilises Docker.

---

## 🧰 Générer les fichiers statiques (pour production)

```bash
python manage.py collectstatic
```

---

## 📁 Structure simplifiée

```
Gestion_Paie/
├── GestionApp/                  # Application Django
│   ├── static/                  # JS, CSS (non compilés)
│   ├── templates/               # Templates HTML
│   └── migrations/
├── Gestion_Paie/               # Réglages du projet Django
├── manage.py
├── package.json, tailwind.config.js
├── Dockerfile, docker-compose.yml
└── .env (à créer)
```

---

## 👤 Auteur

Med-Kad

---

## 📌 Notes

- Les fichiers CSS générés sont ignorés par Git.

