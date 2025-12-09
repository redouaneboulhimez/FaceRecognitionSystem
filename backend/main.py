"""
Main FastAPI Application
Système de contrôle d'accès intelligent par reconnaissance faciale
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn

from app.database import engine, Base
from app.routers import auth, employees, recognition, logs
from app.config import settings

# Créer les tables au démarrage
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Face Recognition Access Control System",
    description="Système de contrôle d'accès intelligent par reconnaissance faciale",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(employees.router, prefix="/api/employees", tags=["Employees"])
app.include_router(recognition.router, prefix="/api/recognition", tags=["Recognition"])
app.include_router(logs.router, prefix="/api/logs", tags=["Logs"])

@app.get("/")
async def root():
    return {
        "message": "Face Recognition Access Control System API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

