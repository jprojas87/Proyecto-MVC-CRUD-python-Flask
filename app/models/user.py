from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    bio: Optional[str] = None
    location: Optional[str] = Field(None, max_length=100)

class UserCreate(UserBase):
    """Modelo para crear un nuevo usuario"""
    pass

class UserUpdate(BaseModel):
    """Modelo para actualizar información del usuario"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    bio: Optional[str] = None
    location: Optional[str] = Field(None, max_length=100)

class UserResponse(UserBase):
    """Modelo de respuesta con información completa del usuario"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserProfileResponse(BaseModel):
    """Modelo simplificado para visualización de perfil"""
    id: int
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class DeleteAccountResponse(BaseModel):
    """Modelo de respuesta al eliminar cuenta"""
    message: str
    deleted_user_id: int
    deleted_email: str