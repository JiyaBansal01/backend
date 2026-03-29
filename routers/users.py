"""
routers/users.py - User API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.models import User
from schemas.schemas import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_current_user(user_id: int = 1, db: Session = Depends(get_db)):
    """Get the currently logged-in user (default user for demo)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
