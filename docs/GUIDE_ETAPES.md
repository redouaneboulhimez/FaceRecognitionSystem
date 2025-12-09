# Guide Étape par Étape - Laboratoire

## 🎯 Vue d'ensemble

Ce guide vous accompagne étape par étape pour mettre en place et utiliser le système de reconnaissance faciale.

---

## 📋 ÉTAPE 1 : Préparation de l'environnement

### 1.1 Vérifier les prérequis

```bash
# Vérifier Python
python --version  # Doit être 3.11+

# Vérifier Node.js
node --version  # Doit être 18+

# Vérifier PostgreSQL
psql --version  # Doit être 14+
```

### 1.2 Créer la structure du projet

La structure est déjà créée. Vérifiez que vous avez :

```
FaceRecognitionSystem/
├── backend/
├── frontend/
├── database/
├── docs/
└── docker-compose.yml
```

---

## 📋 ÉTAPE 2 : Configuration de la base de données

### 2.1 Installer PostgreSQL

**Windows:**
- Télécharger: https://www.postgresql.org/download/windows/
- Installer avec les paramètres par défaut
- Notez le mot de passe du superutilisateur `postgres`

**Linux:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

### 2.2 Créer la base de données

```bash
# Se connecter à PostgreSQL
psql -U postgres

# Dans le shell PostgreSQL:
CREATE DATABASE face_recognition_db;
\q
```

### 2.3 Exécuter le schéma SQL

```bash
psql -U postgres -d face_recognition_db -f database/schema.sql
```

✅ **Vérification:** Les tables `employees`, `employee_photos`, `access_logs`, `admin_users` sont créées.

---

## 📋 ÉTAPE 3 : Configuration du Backend

### 3.1 Créer l'environnement virtuel

```bash
cd backend
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3.2 Installer les dépendances

```bash
pip install -r requirements.txt
```

⏱️ **Temps estimé:** 5-10 minutes (téléchargement des modèles ML)

### 3.3 Configurer les variables d'environnement

Créez un fichier `.env` dans le dossier `backend/`:

```env
DATABASE_URL=postgresql://postgres:votre_mot_de_passe@localhost:5432/face_recognition_db
SECRET_KEY=votre_cle_secrete_aleatoire_ici
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ADMIN_EMAIL=admin@company.com
ADMIN_PASSWORD=admin123
FACE_DETECTION_MODEL=mtcnn
FACE_RECOGNITION_MODEL=facenet
SIMILARITY_THRESHOLD=0.6
EMBEDDING_SIZE=512
UPLOAD_DIR=./uploads
MODELS_DIR=./models
```

**Générer SECRET_KEY:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

### 3.4 Créer les dossiers nécessaires

```bash
mkdir uploads
mkdir models
mkdir uploads\temp  # Windows
# ou
mkdir -p uploads/temp  # Linux/macOS
```

### 3.5 Tester le backend

```bash
# Démarrer le serveur
uvicorn main:app --reload --port 8000
```

✅ **Vérification:** Ouvrir http://localhost:8000/docs - Vous devriez voir la documentation Swagger.

---

## 📋 ÉTAPE 4 : Configuration du Frontend

### 4.1 Installer les dépendances

```bash
cd frontend
npm install
```

⏱️ **Temps estimé:** 2-5 minutes

### 4.2 Vérifier la configuration API

Le fichier `src/services/api.js` pointe vers `http://localhost:8000/api`. 
Si votre backend tourne sur un autre port, modifiez cette URL.

### 4.3 Démarrer le frontend

```bash
npm start
```

✅ **Vérification:** Ouvrir http://localhost:3000 - Vous devriez voir la page de connexion.

---

## 📋 ÉTAPE 5 : Premier démarrage et test

### 5.1 Se connecter à l'interface admin

1. Ouvrir http://localhost:3000
2. Email: `admin@company.com`
3. Mot de passe: `admin123`
4. Cliquer sur "Se connecter"

✅ **Résultat attendu:** Redirection vers le Dashboard

### 5.2 Ajouter un premier employé

1. Cliquer sur "Employés" dans le menu
2. Cliquer sur "+ Ajouter un employé"
3. Remplir le formulaire:
   - ID Employé: `EMP001`
   - Nom: `Jean Dupont`
   - Email: `jean.dupont@company.com`
   - Rôle: `employee`
4. Cliquer sur "Créer"

✅ **Résultat attendu:** L'employé apparaît dans la liste

### 5.3 Uploader des photos pour l'employé

1. Cliquer sur "Upload Photos" pour l'employé créé
2. Sélectionner 3-5 photos du visage de l'employé
   - **Important:** Photos claires, visage bien visible
   - Format: JPG, PNG
   - Taille recommandée: 200x200 à 1000x1000 pixels
3. Cliquer sur "Uploader"

✅ **Résultat attendu:** Message de succès avec le nombre de photos uploadées

⏱️ **Temps estimé:** 10-30 secondes par photo (génération des embeddings)

---

## 📋 ÉTAPE 6 : Test de reconnaissance faciale

### 6.1 Préparer une image de test

Prendre une photo du même employé (peut être différente des photos d'enrollment).

### 6.2 Tester via l'API

**Option A: Via Swagger UI**

1. Aller sur http://localhost:8000/docs
2. Trouver l'endpoint `POST /api/recognition/recognize`
3. Cliquer sur "Try it out"
4. Uploader l'image de test
5. Cliquer sur "Execute"

**Option B: Via curl**

```bash
curl -X POST "http://localhost:8000/api/recognition/recognize" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@chemin/vers/image.jpg"
```

**Option C: Via Python**

```python
import requests

url = "http://localhost:8000/api/recognition/recognize"
files = {'file': open('chemin/vers/image.jpg', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

### 6.3 Vérifier les résultats

✅ **Résultat attendu:**
```json
{
  "recognized": true,
  "employee_id": 1,
  "employee_name": "Jean Dupont",
  "confidence_score": 0.85,
  "decision": "granted",
  "message": "Access granted for Jean Dupont"
}
```

### 6.4 Vérifier les logs

1. Aller sur http://localhost:3000/logs
2. Vérifier que la tentative d'accès apparaît dans les logs

---

## 📋 ÉTAPE 7 : Tests avancés

### 7.1 Test avec visage inconnu

Uploader une photo d'une personne non enregistrée.

✅ **Résultat attendu:** `"decision": "denied"`

### 7.2 Test avec plusieurs employés

1. Ajouter 2-3 autres employés
2. Uploader leurs photos
3. Tester la reconnaissance pour chacun

### 7.3 Test de performance

Mesurer le temps de réponse:
- Temps de reconnaissance < 1 seconde ✅

### 7.4 Test de précision

Tester avec:
- Différentes conditions d'éclairage
- Différents angles
- Avec/sans lunettes
- Avec/sans masque (si supporté)

---

## 📋 ÉTAPE 8 : Utilisation en production

### 8.1 Configuration de sécurité

1. Changer le mot de passe admin par défaut
2. Générer une nouvelle SECRET_KEY forte
3. Configurer HTTPS
4. Restreindre l'accès au réseau

### 8.2 Optimisation

1. Ajuster `SIMILARITY_THRESHOLD` selon vos besoins
2. Configurer la sauvegarde automatique de la base de données
3. Configurer les logs système

### 8.3 Monitoring

1. Surveiller les logs d'accès
2. Surveiller les performances
3. Surveiller l'espace disque (uploads, modèles)

---

## 🔧 Dépannage

### Problème: Erreur de connexion à la base de données

**Solution:**
```bash
# Vérifier que PostgreSQL est démarré
# Windows: Services > PostgreSQL
# Linux: sudo systemctl status postgresql
# macOS: brew services list

# Vérifier les identifiants dans .env
```

### Problème: Module Python non trouvé

**Solution:**
```bash
# Vérifier que l'environnement virtuel est activé
# Réinstaller les dépendances
pip install -r requirements.txt
```

### Problème: Port déjà utilisé

**Solution:**
```bash
# Changer le port dans la commande de démarrage
uvicorn main:app --reload --port 8001  # Backend
# ou modifier package.json pour le frontend
```

### Problème: Reconnaissance ne fonctionne pas

**Vérifications:**
1. Vérifier que des photos ont été uploadées
2. Vérifier que les embeddings ont été générés (dossier models/)
3. Vérifier la qualité de l'image de test
4. Vérifier les logs du backend

---

## 📊 Métriques de succès

- ✅ Temps de reconnaissance < 1 seconde
- ✅ Précision ≥ 95%
- ✅ Tous les accès sont loggés
- ✅ Interface admin fonctionnelle
- ✅ Gestion CRUD des employés opérationnelle

---

## 🎓 Prochaines étapes

1. Ajouter plus d'employés
2. Tester avec différentes conditions
3. Analyser les statistiques dans le Dashboard
4. Personnaliser l'interface selon vos besoins
5. Intégrer avec un système de contrôle d'accès physique (optionnel)

---

**Félicitations ! Votre système de reconnaissance faciale est opérationnel ! 🎉**

