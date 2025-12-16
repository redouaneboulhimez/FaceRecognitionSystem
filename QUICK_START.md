# 🚀 Guide de Démarrage Rapide

## Installation Express (5 minutes)

### 1. Base de données PostgreSQL

```bash
# Créer la base de données
createdb face_recognition_db

# Exécuter le schéma
psql -d face_recognition_db -f database/schema.sql
```

### 2. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

pip install -r requirements.txt

# Créer .env (copier depuis .env.example et modifier)
# DATABASE_URL=postgresql://postgres:password@localhost:5432/face_recognition_db
# SECRET_KEY=<générer avec: python -c "import secrets; print(secrets.token_urlsafe(32))">

mkdir uploads models uploads\temp

# Démarrer
uvicorn main:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm start
```

### 4. Accéder à l'application

- **Frontend:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs
- **Login:** admin@company.com / admin123

---

## Première utilisation

1. **Se connecter** avec admin@company.com / admin123
2. **Ajouter un employé** dans la section "Employés"
3. **Uploader 3-5 photos** du visage de l'employé
4. **Tester la reconnaissance** via l'API `/api/recognition/recognize`
5. **Vérifier les logs** dans la section "Logs d'accès"

---

## Structure du projet

```
FaceRecognitionSystem/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── routers/     # Endpoints API
│   │   ├── ml_module/   # Module ML
│   │   └── ...
│   ├── main.py
│   └── requirements.txt
├── frontend/            # Interface React
│   ├── src/
│   │   ├── components/  # Composants React
│   │   └── ...
│   └── package.json
├── database/            # Scripts SQL
│   └── schema.sql
├── docs/                # Documentation
│   ├── GUIDE_ETAPES.md  # Guide détaillé
│   ├── INSTALLATION.md  # Installation complète
│   ├── SRS.md          # Software Requirements
│   └── PRD.md          # Product Requirements
└── docker-compose.yml   # Docker (optionnel)
```

---

## Commandes utiles

### Backend
```bash
# Démarrer le serveur
uvicorn main:app --reload --port 8000

# Tester l'API
curl http://localhost:8000/health
```

### Frontend
```bash
# Démarrer le serveur de développement
npm start

# Build pour production
npm run build
```

### Base de données
```bash
# Se connecter à PostgreSQL
psql -d face_recognition_db

# Voir les tables
\dt

# Voir les employés
SELECT * FROM employees;
```

---

## Dépannage rapide

**Erreur de connexion DB:**
- Vérifier que PostgreSQL est démarré
- Vérifier DATABASE_URL dans .env

**Module Python manquant:**
- Activer l'environnement virtuel
- pip install -r requirements.txt

**Port déjà utilisé:**
- Changer le port dans la commande de démarrage

**Reconnaissance ne fonctionne pas:**
- Vérifier que des photos ont été uploadées
- Vérifier la qualité des images
- Consulter les logs du backend

cd C:\Users\hp\FaceRecognitionSystem; psql -U postgres -d face_recognition_db -c "\dt"

---

## Documentation complète

Pour plus de détails, consultez:
- `docs/GUIDE_ETAPES.md` - Guide étape par étape complet
- `docs/INSTALLATION.md` - Installation détaillée
- `docs/SRS.md` - Spécifications techniques
- `docs/PRD.md` - Exigences produit

---

**Bon développement ! 🎉**

