"""
Pydantic models for request/response
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Auth Models
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Employee Models
class EmployeeBase(BaseModel):
    employee_id: str
    name: str
    email: Optional[EmailStr] = None
    role: str = "employee"

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class EmployeeResponse(EmployeeBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Photo Models
class PhotoUploadResponse(BaseModel):
    message: str
    employee_id: int
    photos_uploaded: int

# Recognition Models
class RecognitionRequest(BaseModel):
    image_base64: Optional[str] = None
    image_path: Optional[str] = None

class RecognitionResponse(BaseModel):
    recognized: bool
    employee_id: Optional[int] = None
    employee_name: Optional[str] = None
    confidence_score: Optional[float] = None
    decision: str  # "granted" or "denied"
    message: str

# Log Models
class AccessLogResponse(BaseModel):
    id: int
    employee_id: Optional[int]
    employee_name: Optional[str]
    recognition_score: Optional[float]
    decision: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

class LogsFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    employee_id: Optional[int] = None
    decision: Optional[str] = None
    limit: int = 100

