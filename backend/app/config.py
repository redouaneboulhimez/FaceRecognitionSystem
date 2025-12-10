"""
Configuration settings
"""
from pydantic_settings import BaseSettings
from pydantic import Field, model_validator
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/face_recognition_db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Admin
    ADMIN_EMAIL: str = "admin@company.com"
    ADMIN_PASSWORD: str = "admin123"
    
    # ML Settings
    FACE_DETECTION_MODEL: str = "mtcnn"
    FACE_RECOGNITION_MODEL: str = "facenet"
    SIMILARITY_THRESHOLD: float = 0.6
    EMBEDDING_SIZE: int = 512
    
    # Paths
    UPLOAD_DIR: str = "./uploads"
    MODELS_DIR: str = "./models"
    
    @model_validator(mode='after')
    def read_from_env_file_if_empty(self):
        """If DATABASE_URL or SECRET_KEY are empty, read from .env file"""
        env_file = Path(".env")
        if env_file.exists():
            import re
            content = env_file.read_text(encoding="utf-8")
            
            # If DATABASE_URL is empty or default, try to read from .env
            if not self.DATABASE_URL or self.DATABASE_URL == "postgresql://user:password@localhost:5432/face_recognition_db":
                db_match = re.search(r'^DATABASE_URL\s*=\s*(.+)$', content, re.MULTILINE)
                if db_match:
                    self.DATABASE_URL = db_match.group(1).strip()
            
            # If SECRET_KEY is empty or default, try to read from .env
            if not self.SECRET_KEY or self.SECRET_KEY == "your-secret-key-change-in-production":
                secret_match = re.search(r'^SECRET_KEY\s*=\s*(.+)$', content, re.MULTILINE)
                if secret_match:
                    self.SECRET_KEY = secret_match.group(1).strip()
        
        return self
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()

