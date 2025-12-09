"""
Employee management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from pathlib import Path

from app.database import get_db, Employee, EmployeePhoto
from app.models import EmployeeCreate, EmployeeUpdate, EmployeeResponse, PhotoUploadResponse
from app.auth import get_current_user
from app.config import settings
from app.ml_module.face_recognition import FaceRecognitionService

router = APIRouter()

# Créer le dossier uploads s'il n'existe pas
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Créer un nouvel employé
    """
    # Vérifier si l'employee_id existe déjà
    existing = db.query(Employee).filter(Employee.employee_id == employee.employee_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID already exists"
        )
    
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    
    return db_employee

@router.get("/", response_model=List[EmployeeResponse])
async def get_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Récupérer la liste des employés
    """
    employees = db.query(Employee).offset(skip).limit(limit).all()
    return employees

@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Récupérer un employé par ID
    """
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return employee

@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Mettre à jour un employé
    """
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    update_data = employee_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employee, field, value)
    
    db.commit()
    db.refresh(employee)
    return employee

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Supprimer un employé et ses photos
    """
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Supprimer les photos associées
    photos = db.query(EmployeePhoto).filter(EmployeePhoto.employee_id == employee_id).all()
    for photo in photos:
        if os.path.exists(photo.photo_path):
            os.remove(photo.photo_path)
        db.delete(photo)
    
    # Supprimer l'employé
    db.delete(employee)
    db.commit()
    
    # Mettre à jour l'index FAISS
    face_service = FaceRecognitionService()
    face_service.rebuild_index(db)
    
    return None

@router.post("/{employee_id}/photos", response_model=PhotoUploadResponse)
async def upload_photos(
    employee_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Uploader des photos pour un employé et générer les embeddings
    """
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    if len(files) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 10 photos per employee"
        )
    
    # Créer le dossier pour l'employé
    employee_dir = Path(settings.UPLOAD_DIR) / f"employee_{employee_id}"
    employee_dir.mkdir(parents=True, exist_ok=True)
    
    face_service = FaceRecognitionService()
    photos_uploaded = 0
    
    for file in files:
        # Sauvegarder le fichier
        file_path = employee_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Générer l'embedding
        try:
            embedding = face_service.get_embedding(str(file_path))
            if embedding is not None:
                # Sauvegarder dans la base de données
                db_photo = EmployeePhoto(
                    employee_id=employee_id,
                    photo_path=str(file_path),
                    embedding_path=None  # Stocké dans FAISS
                )
                db.add(db_photo)
                
                # Ajouter à l'index FAISS
                face_service.add_to_index(employee_id, embedding)
                photos_uploaded += 1
            else:
                # Supprimer le fichier si pas de visage détecté
                os.remove(file_path)
        except Exception as e:
            # Supprimer le fichier en cas d'erreur
            if os.path.exists(file_path):
                os.remove(file_path)
            continue
    
    db.commit()
    
    return PhotoUploadResponse(
        message=f"Successfully uploaded {photos_uploaded} photos",
        employee_id=employee_id,
        photos_uploaded=photos_uploaded
    )

