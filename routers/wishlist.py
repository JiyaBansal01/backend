"""
routers/wishlist.py - Wishlist API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from database.connection import get_db
from models.models import WishlistItem, Product
from schemas.schemas import SuccessResponse

router = APIRouter()

DEFAULT_USER_ID = 1

@router.get("/")
def get_wishlist(user_id: int = DEFAULT_USER_ID, db: Session = Depends(get_db)):
    items = db.query(WishlistItem).options(
        joinedload(WishlistItem.product).joinedload(Product.images)
    ).filter(WishlistItem.user_id == user_id).all()

    result = []
    for item in items:
        p = item.product
        if not p or not p.is_active:
            continue
        primary_image = None
        for img in p.images:
            if img.is_primary:
                primary_image = img.image_url
                break
        result.append({
            "id": item.id,
            "product_id": p.id,
            "product_name": p.name,
            "product_image": primary_image,
            "price": float(p.price),
            "discounted_price": float(p.discounted_price) if p.discounted_price else None,
            "rating": float(p.rating) if p.rating else None,
            "slug": p.slug
        })
    return result

@router.post("/toggle/{product_id}")
def toggle_wishlist(product_id: int, user_id: int = DEFAULT_USER_ID, db: Session = Depends(get_db)):
    """Add to wishlist if not present, remove if already present"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing = db.query(WishlistItem).filter(
        WishlistItem.user_id == user_id,
        WishlistItem.product_id == product_id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return {"action": "removed", "message": "Removed from wishlist"}
    else:
        new_item = WishlistItem(user_id=user_id, product_id=product_id)
        db.add(new_item)
        db.commit()
        return {"action": "added", "message": "Added to wishlist"}

@router.get("/check/{product_id}")
def check_wishlist(product_id: int, user_id: int = DEFAULT_USER_ID, db: Session = Depends(get_db)):
    """Check if a product is in wishlist"""
    exists = db.query(WishlistItem).filter(
        WishlistItem.user_id == user_id,
        WishlistItem.product_id == product_id
    ).first()
    return {"in_wishlist": bool(exists)}
