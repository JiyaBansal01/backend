"""
routers/cart.py - Shopping Cart API Endpoints
================================================
Handles all cart operations for the default user (user_id=1).

ENDPOINTS:
    GET    /api/cart/              - Get cart contents
    POST   /api/cart/add           - Add item to cart
    PUT    /api/cart/{item_id}     - Update item quantity
    DELETE /api/cart/{item_id}     - Remove item from cart
    DELETE /api/cart/clear         - Clear entire cart
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from decimal import Decimal
from typing import Optional

from database.connection import get_db
from models.models import CartItem, Product, ProductImage
from schemas.schemas import AddToCartRequest, UpdateCartRequest, CartResponse, CartItemResponse, SuccessResponse

router = APIRouter()

# For this demo, we use a default user (no login required)
DEFAULT_USER_ID = 1


def build_cart_response(cart_items, db: Session) -> CartResponse:
    """Helper: Convert cart items from DB into CartResponse format"""
    items = []
    subtotal = Decimal("0.00")
    savings = Decimal("0.00")

    for item in cart_items:
        product = item.product
        if not product or not product.is_active:
            continue

        # Use discounted price if available, else original price
        unit_price = product.discounted_price or product.price
        total_price = unit_price * item.quantity
        subtotal += total_price

        # Calculate savings (original - discounted) * quantity
        if product.discounted_price and product.price > product.discounted_price:
            savings += (product.price - product.discounted_price) * item.quantity

        # Get primary image
        primary_image = None
        for img in product.images:
            if img.is_primary:
                primary_image = img.image_url
                break
        if not primary_image and product.images:
            primary_image = product.images[0].image_url

        items.append(CartItemResponse(
            id=item.id,
            product_id=product.id,
            quantity=item.quantity,
            product_name=product.name,
            product_image=primary_image,
            unit_price=unit_price,
            total_price=total_price,
            stock_quantity=product.stock_quantity,
            brand=product.brand
        ))

    return CartResponse(
        items=items,
        subtotal=subtotal,
        total_items=len(items),
        savings=savings
    )


@router.get("/", response_model=CartResponse)
def get_cart(user_id: int = DEFAULT_USER_ID, db: Session = Depends(get_db)):
    """Get all items in the cart for the current user"""
    cart_items = db.query(CartItem).options(
        joinedload(CartItem.product).joinedload(Product.images)
    ).filter(CartItem.user_id == user_id).all()

    return build_cart_response(cart_items, db)


@router.post("/add", response_model=CartResponse)
def add_to_cart(request: AddToCartRequest, db: Session = Depends(get_db)):
    """
    Add a product to cart.
    If product already in cart, increases quantity.
    """
    user_id = DEFAULT_USER_ID

    # Check product exists and is available
    product = db.query(Product).filter(
        Product.id == request.product_id,
        Product.is_active == True
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock_quantity < request.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Only {product.stock_quantity} items available in stock"
        )

    # Check if already in cart
    existing_item = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == request.product_id
    ).first()

    if existing_item:
        # Update quantity instead of adding duplicate
        new_qty = existing_item.quantity + request.quantity
        if new_qty > product.stock_quantity:
            raise HTTPException(status_code=400, detail="Cannot add more than available stock")
        existing_item.quantity = new_qty
    else:
        # Add new cart item
        new_item = CartItem(
            user_id=user_id,
            product_id=request.product_id,
            quantity=request.quantity
        )
        db.add(new_item)

    db.commit()

    # Return updated cart
    return get_cart(user_id, db)


@router.put("/{item_id}", response_model=CartResponse)
def update_cart_item(
    item_id: int,
    request: UpdateCartRequest,
    user_id: int = DEFAULT_USER_ID,
    db: Session = Depends(get_db)
):
    """Update the quantity of a cart item"""
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == user_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if request.quantity <= 0:
        # If quantity is 0, remove the item
        db.delete(cart_item)
        db.commit()
    else:
        # Check stock availability
        product = cart_item.product
        if request.quantity > product.stock_quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Only {product.stock_quantity} items available"
            )
        cart_item.quantity = request.quantity
        db.commit()

    return get_cart(user_id, db)


@router.delete("/clear", response_model=SuccessResponse)
def clear_cart(user_id: int = DEFAULT_USER_ID, db: Session = Depends(get_db)):
    """Remove all items from cart"""
    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    db.commit()
    return SuccessResponse(message="Cart cleared successfully")


@router.delete("/{item_id}", response_model=CartResponse)
def remove_cart_item(
    item_id: int,
    user_id: int = DEFAULT_USER_ID,
    db: Session = Depends(get_db)
):
    """Remove a single item from cart"""
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == user_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()

    return get_cart(user_id, db)
