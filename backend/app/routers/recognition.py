"""
Face recognition routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime
import os
import shutil
from pathlib import Path

from app.database import get_db, Employee, AccessLog
from app.models import RecognitionResponse
from app.config import settings
from app.ml_module.face_recognition import FaceRecognitionService

router = APIRouter()

@router.post("/recognize", response_model=RecognitionResponse)
async def recognize_face(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Reconnaître un visage à partir d'une image
    """
    # Sauvegarder temporairement l'image
    temp_dir = Path(settings.UPLOAD_DIR) / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    temp_path = temp_dir / f"recognition_{datetime.now().timestamp()}.jpg"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Initialiser le service de reconnaissance
        face_service = FaceRecognitionService()
        
        # Obtenir l'embedding
        embedding = face_service.get_embedding(str(temp_path))
        
        if embedding is None:
            # Pas de visage détecté
            log = AccessLog(
                employee_id=None,
                employee_name=None,
                recognition_score=None,
                decision="denied",
                image_path=str(temp_path)
            )
            db.add(log)
            db.commit()
            
            return RecognitionResponse(
                recognized=False,
                decision="denied",
                message="No face detected in the image"
            )
        
        # Rechercher dans l'index FAISS
        result = face_service.search_in_index(embedding)
        
        if result and result['distance'] < settings.SIMILARITY_THRESHOLD:
            # Visage reconnu
            employee = db.query(Employee).filter(Employee.id == result['employee_id']).first()
            
            log = AccessLog(
                employee_id=employee.id if employee else None,
                employee_name=employee.name if employee else None,
                recognition_score=float(1 - result['distance']),  # Convertir distance en score
                decision="granted",
                image_path=str(temp_path)
            )
            db.add(log)
            db.commit()
            
            return RecognitionResponse(
                recognized=True,
                employee_id=employee.id if employee else None,
                employee_name=employee.name if employee else None,
                confidence_score=float(1 - result['distance']),
                decision="granted",
                message=f"Access granted for {employee.name if employee else 'Unknown'}"
            )
        else:
            # Visage non reconnu
            log = AccessLog(
                employee_id=None,
                employee_name=None,
                recognition_score=float(1 - result['distance']) if result else None,
                decision="denied",
                image_path=str(temp_path)
            )
            db.add(log)
            db.commit()
            
            return RecognitionResponse(
                recognized=False,
                decision="denied",
                message="Face not recognized. Access denied."
            )
    
    except Exception as e:
        # En cas d'erreur
        log = AccessLog(
            employee_id=None,
            employee_name=None,
            recognition_score=None,
            decision="denied",
            image_path=str(temp_path)
        )
        db.add(log)
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Recognition error: {str(e)}"
        )
    
    finally:
        # Nettoyer le fichier temporaire après un délai (optionnel)
        # Pour l'instant, on garde les images pour debug
        pass

