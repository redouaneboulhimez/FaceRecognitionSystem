"""
Access logs routes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime

from app.database import get_db, AccessLog
from app.models import AccessLogResponse
from app.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[AccessLogResponse])
async def get_logs(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    employee_id: Optional[int] = Query(None),
    decision: Optional[str] = Query(None),
    limit: int = Query(100, le=1000),
    skip: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Récupérer les logs d'accès avec filtres
    """
    query = db.query(AccessLog)
    
    if start_date:
        query = query.filter(AccessLog.timestamp >= start_date)
    if end_date:
        query = query.filter(AccessLog.timestamp <= end_date)
    if employee_id:
        query = query.filter(AccessLog.employee_id == employee_id)
    if decision:
        query = query.filter(AccessLog.decision == decision)
    
    logs = query.order_by(desc(AccessLog.timestamp)).offset(skip).limit(limit).all()
    return logs

@router.get("/stats")
async def get_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Obtenir des statistiques sur les accès
    """
    total_logs = db.query(AccessLog).count()
    granted_logs = db.query(AccessLog).filter(AccessLog.decision == "granted").count()
    denied_logs = db.query(AccessLog).filter(AccessLog.decision == "denied").count()
    
    return {
        "total_access_attempts": total_logs,
        "granted": granted_logs,
        "denied": denied_logs,
        "grant_rate": round(granted_logs / total_logs * 100, 2) if total_logs > 0 else 0
    }

