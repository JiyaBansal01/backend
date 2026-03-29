"""
routers/orders.py - Order Management API Endpoints
=====================================================
ENDPOINTS:
    POST /api/orders/place     - Place a new order
    GET  /api/orders/          - Get order history
    GET  /api/orders/{id}      - Get single order details
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
import uuid
import random
import string
from datetime import datetime

from database.connection import get_db
from models.models import Order, OrderItem, CartItem, Product
from schemas.schemas import PlaceOrderRequest, OrderResponse, SuccessResponse

router = APIRouter()

DEFAULT_USER_ID = 1


def generate_order_number() -> str:
    """Generate a unique order number like FK-2024-ABC12345"""
    year = datetime.now().year
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"FK-{year}-{suffix}"


@router.post("/place", response_model=OrderResponse)
def place_order(request: PlaceOrderRequest, db: Session = Depends(get_db)):
    """
    Place a new order from the current cart.
    
    Steps:
    1. Get all cart items for the user
    2. Calculate totals
    3. Create order record
    4. Create order item records (snapshots of products)
    5. Clear the cart
    6. Return order confirmation
    """
    user_id = request.user_id or DEFAULT_USER_ID

    # Step 1: Get cart items
    cart_items = db.query(CartItem).options(
        joinedload(CartItem.product).joinedload(Product.images)
    ).filter(CartItem.user_id == user_id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty. Add items before placing order.")

    # Step 2: Calculate totals
    subtotal = 0
    order_items_data = []

    for item in cart_items:
        product = item.product
        if not product or not product.is_active:
            raise HTTPException(
                status_code=400,
                detail=f"Product '{item.product_id}' is no longer available"
            )

        # Check stock
        if item.quantity > product.stock_quantity:
            raise HTTPException(
                status_code=400,
                detail=f"'{product.name}' has only {product.stock_quantity} items in stock"
            )

        unit_price = float(product.discounted_price or product.price)
        total_price = unit_price * item.quantity
        subtotal += total_price

        # Get primary image URL
        primary_image = None
        for img in product.images:
            if img.is_primary:
                primary_image = img.image_url
                break

        order_items_data.append({
            "product_id": product.id,
            "product_name": product.name,
            "product_image": primary_image,
            "quantity": item.quantity,
            "unit_price": unit_price,
            "total_price": total_price
        })

    # Free shipping above Rs 499
    shipping_fee = 0 if subtotal >= 499 else 40
    total_amount = subtotal + shipping_fee

    # Step 3: Create the address snapshot
    # We save address as JSON so it doesn't change if user updates their address later
    address_snapshot = {
        "full_name":     request.shipping_address.full_name,
        "phone":         request.shipping_address.phone,
        "address_line1": request.shipping_address.address_line1,
        "address_line2": request.shipping_address.address_line2 or "",
        "city":          request.shipping_address.city,
        "state":         request.shipping_address.state,
        "pincode":       request.shipping_address.pincode,
        "address_type":  request.shipping_address.address_type or "HOME"
    }

    # Step 4: Create the order
    new_order = Order(
        order_number=generate_order_number(),
        user_id=user_id,
        shipping_address_snapshot=address_snapshot,
        subtotal=subtotal,
        shipping_fee=shipping_fee,
        total_amount=total_amount,
        payment_method=request.payment_method or "COD",
        payment_status="PENDING",
        status="CONFIRMED",     # Auto-confirm for this demo
        notes=request.notes
    )
    db.add(new_order)
    db.flush()  # Get the new order's ID without committing

    # Step 5: Create order items
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=new_order.id,
            **item_data
        )
        db.add(order_item)

        # Reduce stock quantity
        product = db.query(Product).get(item_data["product_id"])
        if product:
            product.stock_quantity -= item_data["quantity"]

    # Step 6: Clear the cart
    db.query(CartItem).filter(CartItem.user_id == user_id).delete()

    db.commit()
    db.refresh(new_order)

    # Load order items for response
    order = db.query(Order).options(
        joinedload(Order.order_items)
    ).filter(Order.id == new_order.id).first()

    return order


@router.get("/", response_model=List[OrderResponse])
def get_order_history(user_id: int = DEFAULT_USER_ID, db: Session = Depends(get_db)):
    """Get all orders for the current user"""
    orders = db.query(Order).options(
        joinedload(Order.order_items)
    ).filter(
        Order.user_id == user_id
    ).order_by(Order.placed_at.desc()).all()

    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_details(order_id: int, db: Session = Depends(get_db)):
    """Get details of a specific order"""
    order = db.query(Order).options(
        joinedload(Order.order_items)
    ).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order
