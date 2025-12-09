# Guide d'Installation

## Prérequis

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Docker et Docker Compose (optionnel)

## Installation Manuelle

### 1. Cloner le projet

```bash
git clone <repo-url>
cd FaceRecognitionSystem
```

### 2. Configuration de la base de données

#### Installer PostgreSQL

**Windows:**
- Télécharger depuis https://www.postgresql.org/download/windows/
- Installer avec les paramètres par défaut

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

**macOS:**
```bash
brew install postgresql
```

#### Créer la base de données

```bash
# Se connecter à PostgreSQL
psql -U postgres

# Créer la base de données
CREATE DATABASE face_recognition_db;

# Créer un utilisateur (optionnel)
CREATE USER face_user WITH PASSWORD 'face_password';
GRANT ALL PRIVILEGES ON DATABASE face_recognition_db TO face_user;

# Quitter
\q
```

#### Exécuter le schéma SQL

```bash
psql -U postgres -d face_recognition_db -f database/schema.sql
```

### 3. Configuration du Backend

```bash
cd backend

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Créer le fichier .env
cp .env.example .env

# Éditer .env et configurer:
# - DATABASE_URL avec vos identifiants PostgreSQL
# - SECRET_KEY (générer une clé aléatoire)
# - ADMIN_EMAIL et ADMIN_PASSWORD
```

**Générer une SECRET_KEY:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

### 4. Configuration du Frontend

```bash
cd frontend

# Installer les dépendances
npm install

# Le fichier .env est optionnel pour le frontend
# L'URL de l'API est configurée dans src/services/api.js
```

### 5. Créer les dossiers nécessaires

```bash
# Depuis la racine du projet
mkdir -p backend/uploads
mkdir -p backend/models
mkdir -p backend/uploads/temp
```

## Installation avec Docker

### 1. Cloner le projet

```bash
git clone <repo-url>
cd FaceRecognitionSystem
```

### 2. Créer le fichier .env pour le backend

```bash
cd backend
cp .env.example .env
# Éditer .env avec les valeurs appropriées
```

### 3. Démarrer avec Docker Compose

```bash
# Depuis la racine du projet
docker-compose up -d
```

Les services seront disponibles sur:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 4. Arrêter les services

```bash
docker-compose down
```

## Vérification de l'installation

### Backend

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import cv2; print('OpenCV:', cv2.__version__)"
```

### Frontend

```bash
cd frontend
npm list react
```

## Dépannage

### Erreur de connexion à la base de données

- Vérifier que PostgreSQL est démarré
- Vérifier les identifiants dans `.env`
- Vérifier que la base de données existe

### Erreur d'importation de modules Python

- Vérifier que l'environnement virtuel est activé
- Réinstaller les dépendances: `pip install -r requirements.txt`

### Erreur de port déjà utilisé

- Changer les ports dans `docker-compose.yml` ou dans les commandes de démarrage
- Vérifier qu'aucun autre service n'utilise les ports 3000, 8000, 5432

### Erreur de modèle ML

- Les modèles seront téléchargés automatiquement au premier usage
- Vérifier la connexion internet pour le téléchargement initial
- Vérifier l'espace disque disponible

