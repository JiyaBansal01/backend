"""
routers/categories.py - Category API Endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database.connection import get_db
from models.models import Category
from schemas.schemas import CategoryResponse

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    """Get all product categories"""
    return db.query(Category).all()
