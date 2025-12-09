# Système de Contrôle d'Accès Intelligent par Reconnaissance Faciale

## 📋 Description

Système de contrôle d'accès intelligent basé sur la reconnaissance faciale pour sécuriser l'entrée d'un bâtiment d'entreprise. Ce système remplace les badges physiques par une solution biométrique fiable, rapide et sécurisée.

## 🏗️ Architecture

```
FaceRecognitionSystem/
├── backend/          # API FastAPI
├── frontend/         # Interface React
├── ml_module/        # Module ML (détection + embedding)
├── database/         # Scripts de base de données
├── docker/           # Configuration Docker
└── docs/             # Documentation
```

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Docker (optionnel)

### Installation

1. **Cloner le projet**
```bash
git clone <repo-url>
cd FaceRecognitionSystem
```

2. **Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Frontend**
```bash
cd frontend
npm install
```

4. **Base de données**
```bash
# Créer la base de données PostgreSQL
createdb face_recognition_db

# Exécuter les migrations
cd database
psql -d face_recognition_db -f schema.sql
```

### Démarrage

1. **Démarrer le backend**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

2. **Démarrer le frontend**
```bash
cd frontend
npm start
```

3. **Accéder à l'application**
- Frontend: http://localhost:3000
- API: http://localhost:8000
- Docs API: http://localhost:8000/docs

## 📚 Documentation

Voir le dossier `docs/` pour:
- SRS (Software Requirements Specification)
- PRD (Product Requirements Document)
- Guide d'installation détaillé
- Guide d'utilisation

## 🔧 Technologies

- **Backend**: FastAPI, PostgreSQL, FAISS
- **ML**: PyTorch, FaceNet/ArcFace, MTCNN/RetinaFace
- **Frontend**: React, Tailwind CSS
- **Docker**: Containerisation

## 📝 License

Ce projet est développé dans le cadre d'un PFA (Projet de Fin d'Année).

