# PRD — Product Requirements Document

## Système de contrôle d'accès intelligent par reconnaissance faciale

**Cadre :** Entreprise (High-Tech / Industrie)  
**Auteur :** [Votre Nom]  
**Année :** 2025

---

## 1. Résumé exécutif

Ce projet vise à développer un système intelligent de contrôle d'accès basé sur la reconnaissance faciale pour sécuriser les entrées d'un bâtiment d'entreprise.

L'objectif principal est de remplacer les badges d'accès classiques par une méthode biométrique plus rapide, plus sécurisée et impossible à perdre ou échanger.

Le système repose sur :
- une caméra pour capturer le visage des employés,
- un module Machine Learning / Deep Learning pour reconnaître les visages,
- un backend qui gère les employés, droits d'accès et logs,
- un contrôleur de porte pour autoriser ou refuser l'ouverture.

Ce projet est réalisé 100% gratuitement grâce à des modèles open-source et un déploiement local.

---

## 2. Objectifs du produit

### 🎯 Objectif principal

Permettre l'authentification automatique des employés lors de l'entrée dans un bâtiment, sans badge, uniquement via leur visage.

### 🎯 Objectifs secondaires

- Réduire les risques de fraude (perte, vol, emprunt de badge).
- Accélérer le passage des employés.
- Fournir à l'entreprise un historique complet des accès.
- Démontrer une application réelle de ML/DL dans un cadre industriel.
- Proposer un système réutilisable pour d'autres entreprises.

---

## 3. Scope du projet

### ✔️ Inclus dans le périmètre

- Capture d'image via webcam.
- Détection et reconnaissance faciale.
- Enregistrement (enrollment) des visages des employés.
- Matching visage ↔ base d'employés.
- Décision d'accès (autorisé/refusé).
- Interface admin simple pour gérer :
  - employés
  - images
  - logs
- Base de données locale.
- Dashboard / logs accès.
- Sécurité minimale (JWT + hashing + seuils ML).

### ❌ Hors périmètre (non nécessaires pour un PFA)

- Contrôleur physique réel de porte industrielle.
- Système cloud ou IoT complet.
- Caméras professionnelles.
- Liveness avancé IR.
- Scalabilité multi-sites.

---

## 4. Personas

### 👨‍💼 1. Administrateur Sécurité

**Rôle :** gérer les employés et superviser les accès.  
**Besoin :** système fiable, rapide, logs clairs.

### 👨‍🔧 2. Employé

**Rôle :** entrer dans le bâtiment.  
**Besoin :** accès rapide, sans badge.

### 👨‍💻 3. Développeur / Data Engineer

**Rôle :** configurer modèles ML et pipeline.  
**Besoin :** système modulaire, open-source, facilement modifiable.

---

## 5. User Stories

### 🔐 Contrôle d'accès

- **En tant qu'employé**, je veux être authentifié automatiquement, afin d'entrer sans badge.
- **En tant que système**, je veux comparer le visage capturé aux embeddings, afin de déterminer l'identité.

### 👨‍💼 Administration

- **En tant qu'administrateur**, je veux enregistrer le visage d'un employé (enrollment), afin qu'il puisse accéder au site.
- **En tant qu'administrateur**, je veux consulter les logs d'accès, afin de savoir qui est entré et quand.

### 🧠 Machine Learning

- **En tant que modèle ML**, je dois générer des embeddings faciaux fiables, pour permettre un match précis.

---

## 6. Functional Requirements (Fonctionnels)

### 6.1. Capture & Détection

- Le système doit capturer des images via webcam.
- Le système doit détecter un visage dans l'image.
- Le système doit rejeter les images floues.

### 6.2. Reconnaissance faciale

- Le système doit extraire un embedding facial (128–512 dims).
- Le système doit comparer cet embedding à ceux en base.
- Le système doit décider :
  - MATCH (si distance < seuil)
  - NO MATCH sinon

### 6.3. Workflow d'accès

1. Le visage est capturé.
2. Le visage est détecté et aligné.
3. Embedding généré.
4. Matching contre DB.
5. Logs créés :
   - employé identifié
   - decision (granted/denied)
   - score de similarité
   - timestamp

### 6.4. Interface d'administration

- Ajouter un employé 🧑‍💼
- Uploader image(s) d'entraînement
- Liste des employés
- Logs d'accès en temps réel
- Supprimer un employé

---

## 7. Non-Functional Requirements (NFR)

### Performance

- Latence totale < 1 seconde.
- Reconnaissance ≥ 95% de précision.

### Sécurité

- JWT pour l'interface admin.
- Hashing des mots de passe.
- Chiffrement local (facultatif).

### Fiabilité

- Le système doit fonctionner sans internet.
- Base de données doit stocker 1000 utilisateurs sans problème.

### Extensibilité

- Architecture modulaire (ML, API, UI indépendants).
- Modèle ML interchangeable.

---

## 8. Architecture Technique

### Stack recommandée (gratuite)

- **Caméra** : Webcam PC
- **ML** : Python + PyTorch + FaceNet/ArcFace
- **Backend** : FastAPI
- **DB** : PostgreSQL
- **Vector Index** : Faiss
- **Interface Admin** : React + Tailwind
- **Logs** : PostgreSQL table access_logs
- **Déploiement** : Docker local

### Architecture (texte)

1. Webcam → Frame → Module ML
2. Détection visage
3. Embedding
4. Envoi au backend → matching FAISS
5. Backend → décision → logs
6. UI admin → gestion employés & logs

---

## 9. Success Metrics

- **TAR (True Accept Rate)** ≥ 95%
- **FAR (False Accept Rate)** ≤ 2%
- **Temps d'accès** ≤ 1 seconde
- **100% des accès loggés** en BDD

---

## 10. Risques

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Mauvaise luminosité | Rejet visage | Filtre qualité + augmentation dataset |
| Faux positif | accès frauduleux | seuil élevé + plusieurs images |
| Webcam mauvaise qualité | détection faible | réglage résolution |
| Dataset trop petit | mauvaise précision | 10 images/personne |

---

## 11. Plan de réalisation (Roadmap)

### Phase 1 — Setup technique
- Installation FastAPI, DB, models
- Setup webcam capture

### Phase 2 — ML
- Détection (MTCNN/RetinaFace)
- Embedding (FaceNet/ArcFace)
- Matching Faiss

### Phase 3 — Backend
- API recognition
- API enrollment
- API logs

### Phase 4 — UI
- dashboard accès
- gestion employés
- upload images

### Phase 5 — Tests
- dataset interne
- test lumière
- test précision
- mesures TAR/FAR

### Phase 6 — Finalisation / Rapport
- Architecture
- Résultats ML
- Démo vidéo

---

## 12. Livrables

- Code du système complet
- Modèle ML
- Base de données
- Dashboard Admin
- Vidéo démonstration
- Rapport PFA + présentation PPT

