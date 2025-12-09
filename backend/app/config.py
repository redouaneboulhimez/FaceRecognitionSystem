"""
Configuration settings
"""
from pydantic_settings import BaseSettings
from typing import Optional

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
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

