"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, AdminUser
from app.models import LoginRequest, Token
from app.auth import verify_password, get_password_hash, create_access_token
from app.config import settings
from datetime import timedelta

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authentification de l'administrateur
    """
    # Vérifier si l'utilisateur existe
    user = db.query(AdminUser).filter(AdminUser.email == login_data.email).first()
    
    # Si pas d'utilisateur, créer l'admin par défaut au premier login
    if not user:
        if login_data.email == settings.ADMIN_EMAIL:
            # Créer l'admin par défaut
            hashed_password = get_password_hash(login_data.password)
            user = AdminUser(
                email=settings.ADMIN_EMAIL,
                hashed_password=hashed_password
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
    
    # Vérifier le mot de passe
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Créer le token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

