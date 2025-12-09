# SRS — Software Requirements Specification

## Système de contrôle d'accès intelligent par reconnaissance faciale

**Cadre :** Entreprise (bâtiment high-tech)  
**Auteur :** [Votre Nom] — 2025

---

## 1. Introduction

### 1.1. Objectif du document

L'objectif de ce SRS est de définir l'ensemble des exigences fonctionnelles, non fonctionnelles, techniques et opérationnelles du système de contrôle d'accès intelligent basé sur la reconnaissance faciale, destiné à sécuriser l'entrée d'un bâtiment d'entreprise.

Ce document servira de référence pour :
- les développeurs
- les data engineers
- les administrateurs système
- les encadrants académiques

### 1.2. Portée (Scope)

Le système permet :
- d'identifier les employés à partir de leur visage,
- d'autoriser ou refuser l'accès au bâtiment,
- d'enregistrer les logs des accès,
- de gérer les employés et leurs images via une interface admin.

Ce système vise à remplacer les badges physiques par une solution biométrique plus fiable, rapide et sécurisée.

### 1.3. Définitions

- **Reconnaissance faciale** : Processus ML d'identification d'une personne à partir d'une image.
- **Embedding** : Représentation vectorielle d'un visage.
- **Enrollment** : Enregistrement initial du visage d'un employé.
- **FAISS** : Bibliothèque de recherche vectorielle haute performance.
- **Liveness Detection** (optionnel) : Détection pour éviter photos ou deepfakes.

---

## 2. Description générale

### 2.1. Perspective produit

Le système est composé de quatre modules principaux :

1. **Module Vision / ML**
   - capture d'image
   - détection du visage
   - extraction d'embeddings
   - comparaison

2. **Backend API**
   - endpoints pour recognition
   - endpoints pour enrollment
   - gestion employés
   - gestion logs

3. **Base de données**
   - table employés
   - table embeddings
   - table logs d'accès

4. **Interface Administrateur**
   - ajout/suppression employés
   - upload d'images
   - consultation des logs

### 2.2. Utilisateurs du système (Personas)

- **Administrateur Sécurité** : Gère les employés et les droits d'accès.
- **Employé** : Souhaite entrer dans le bâtiment sans badge.
- **Système Automatisé** : Caméra + ML en charge de l'authentification.

### 2.3. Contraintes

- Utilisation de modèles open-source (gratuit).
- Fonctionnement local sans internet.
- Matériel limité (webcam + PC standard).

---

## 3. Exigences Fonctionnelles (Functional Requirements)

### 3.1. FR1 — Capture & Prétraitement

- **FR1.1** : Le système doit capturer une image via une webcam à l'approche d'un individu.
- **FR1.2** : Le système doit détecter la présence d'un visage dans l'image.
- **FR1.3** : Le système doit effectuer l'alignement facial (rotation, zoom).

### 3.2. FR2 — Reconnaissance faciale

- **FR2.1** : Extraire un embedding pour chaque visage détecté.
- **FR2.2** : Comparer cet embedding aux embeddings stockés.
- **FR2.3** : Déterminer l'identité si distance < seuil.
- **FR2.4** : Retourner "Authorisé" ou "Refusé".

### 3.3. FR3 — Enrollment (Enregistrement des employés)

- **FR3.1** : Ajouter un nouvel employé avec nom, ID, rôle.
- **FR3.2** : Uploader entre 1 et 10 images par employé.
- **FR3.3** : Générer automatiquement les embeddings.
- **FR3.4** : Stocker les embeddings dans la base FAISS.
- **FR3.5** : Mettre à jour ou supprimer un employé.

### 3.4. FR4 — Gestion des accès

- **FR4.1** : Enregistrer chaque tentative d'accès avec :
  - ID employé (si trouvé)
  - timestamp
  - score de similarité
  - décision (grant/deny)
- **FR4.2** : Permettre à l'administrateur de consulter ces logs.

### 3.5. FR5 — Interface administrateur

- **FR5.1** : Interface login admin (email + mot de passe).
- **FR5.2** : Table de gestion employés (CRUD).
- **FR5.3** : Page des logs.
- **FR5.4** : Page d'upload images.

---

## 4. Exigences Non Fonctionnelles (NFR)

### 4.1. Performance

- **NFR1** : Temps de reconnaissance < 1 seconde.
- **NFR2** : Précision ≥ 95%.
- **NFR3** : Support de 500 à 1000 employés sans latence.

### 4.2. Sécurité

- **NFR4** : Mot de passe admin hashé (bcrypt).
- **NFR5** : Authentification JWT pour l'accès au Dashboard.
- **NFR6** : Images stockées localement, non exposées.
- **NFR7** : API recognition non accessible sans token.

### 4.3. Disponibilité

- **NFR8** : Fonctionnement hors-ligne.
- **NFR9** : Recovery automatique si la caméra se déconnecte.

### 4.4. Maintenabilité

- **NFR10** : Architecture modulaire (ML, API, UI séparés).
- **NFR11** : Code documenté.
- **NFR12** : Modèles ML facilement remplaçables.

---

## 5. Exigences Techniques

### 5.1. Technologies utilisées

- Python 3.11
- FastAPI
- PyTorch
- ArcFace / FaceNet
- MTCNN / RetinaFace
- PostgreSQL
- FAISS (vector search)
- React + Tailwind
- Docker (optionnel)

### 5.2. Architecture Logicielle

**Pipeline reconnaissance :**
1. Webcam capture
2. Détection du visage
3. Alignement
4. Embedding
5. Matching FAISS
6. Retour décision + log

**Architecture API :**
- `/auth/login`
- `/employee/add`
- `/employee/delete`
- `/employee/photos/upload`
- `/recognize`
- `/logs`

---

## 6. Interface utilisateur (UI/UX)

### 6.1. Dashboard Admin

Contient :
- Menu latéral
- Liste employés
- Page ajout employé
- Upload photos
- Logs d'accès (table filtrable)

### 6.2. Page Reconnaissance

Non visible à l'utilisateur → affichage en plein écran pour la caméra.

---

## 7. Critères d'acceptation

1. Le système doit identifier un employé enregistré en < 1 seconde.
2. Le système doit refuser un visage inconnu.
3. L'administrateur doit pouvoir enregistrer un employé en moins de 2 minutes.
4. Un log doit être créé à chaque tentative d'accès.
5. Le taux d'erreur doit être < 5%.

---

## 8. Scénarios Tests

1. **Test 1** : Reconnaissance employé connu
   - Input : visage employé enregistré
   - Output : accès autorisé + log

2. **Test 2** : Visage inconnu
   - Résultat : accès refusé + log

3. **Test 3** : Mauvaise luminosité
   - Le système doit rejeter l'image comme "faible qualité".

4. **Test 4** : Ajout employé + images
   - Doit créer les embeddings automatiquement.

5. **Test 5** : Sécurité admin
   - Sans token JWT → accès interdit au dashboard.

---

## 9. Livrables

- Code source (ML + API + UI)
- Base de données
- Modèle ML
- Documentation technique
- SRS (ce document)
- PRD
- Présentation PowerPoint
- Vidéo de démonstration

---

## 10. Annexes

- Matériel utilisé
- Versions des packages
- Dataset d'entraînement (images des employés)
- Hyperparamètres
- Métriques ML

