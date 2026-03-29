"""
schemas/schemas.py - Data Validation Schemas (Pydantic)
========================================================
Pydantic schemas define the shape of data going IN and OUT of our API.

WHY SCHEMAS?
    - They validate incoming data (e.g., price must be a number)
    - They control what data is returned (e.g., don't send password to frontend)
    - They generate automatic API documentation

NAMING CONVENTION:
    - Base: Common fields
    - Create: Fields needed to create a new record
    - Update: Optional fields for updating
    - Response: What we return to frontend (may exclude sensitive fields)
"""

from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal


# ================================================================
# CATEGORY SCHEMAS
# ================================================================
class CategoryBase(BaseModel):
    name: str
    slug: str
    icon: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True   # Allows reading from SQLAlchemy model objects


# ================================================================
# PRODUCT IMAGE SCHEMAS
# ================================================================
class ProductImageResponse(BaseModel):
    id: int
    image_url: str
    is_primary: bool
    display_order: int

    class Config:
        from_attributes = True


# ================================================================
# PRODUCT SCHEMAS
# ================================================================
class ProductBase(BaseModel):
    name: str
    brand: Optional[str] = None
    description: Optional[str] = None
    price: Decimal
    discounted_price: Optional[Decimal] = None
    discount_percent: Optional[int] = 0
    stock_quantity: Optional[int] = 0

class ProductListItem(BaseModel):
    """Compact product info for listing pages (cards)"""
    id: int
    name: str
    slug: str
    brand: Optional[str]
    price: Decimal
    discounted_price: Optional[Decimal]
    discount_percent: Optional[int]
    rating: Optional[Decimal]
    review_count: Optional[int]
    stock_quantity: int
    # Include only primary image for listing cards
    primary_image: Optional[str] = None
    category_id: int
    category_name: Optional[str] = None

    class Config:
        from_attributes = True

class ProductDetail(BaseModel):
    """Full product info for detail page"""
    id: int
    name: str
    slug: str
    brand: Optional[str]
    description: Optional[str]
    specifications: Optional[Dict[str, Any]]
    price: Decimal
    discounted_price: Optional[Decimal]
    discount_percent: Optional[int]
    rating: Optional[Decimal]
    review_count: Optional[int]
    stock_quantity: int
    images: List[ProductImageResponse] = []
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True

class ProductsResponse(BaseModel):
    """Paginated product list response"""
    products: List[ProductListItem]
    total: int
    page: int
    per_page: int
    total_pages: int


# ================================================================
# USER SCHEMAS
# ================================================================
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None

    @validator("password")
    def password_must_be_strong(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    avatar_url: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None


# ================================================================
# ADDRESS SCHEMAS
# ================================================================
class AddressCreate(BaseModel):
    full_name: str
    phone: str
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    pincode: str
    address_type: Optional[str] = "HOME"
    is_default: Optional[bool] = False

class AddressResponse(AddressCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# ================================================================
# CART SCHEMAS
# ================================================================
class AddToCartRequest(BaseModel):
    product_id: int
    quantity: int = 1
    session_id: Optional[str] = None

class UpdateCartRequest(BaseModel):
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product_name: str
    product_image: Optional[str]
    unit_price: Decimal
    total_price: Decimal
    stock_quantity: int
    brand: Optional[str]

class CartResponse(BaseModel):
    items: List[CartItemResponse]
    subtotal: Decimal
    total_items: int
    savings: Decimal              # How much they saved with discounts


# ================================================================
# ORDER SCHEMAS
# ================================================================
class PlaceOrderRequest(BaseModel):
    session_id: Optional[str] = None
    user_id: Optional[int] = 1       # Default user for demo
    shipping_address: AddressCreate
    payment_method: Optional[str] = "COD"
    notes: Optional[str] = None

class OrderItemResponse(BaseModel):
    id: int
    product_id: Optional[int]
    product_name: str
    product_image: Optional[str]
    quantity: int
    unit_price: Decimal
    total_price: Decimal

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    order_number: str
    status: str
    payment_method: str
    payment_status: str
    subtotal: Decimal
    shipping_fee: Decimal
    total_amount: Decimal
    placed_at: datetime
    shipping_address_snapshot: Dict[str, Any]
    order_items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


# ================================================================
# WISHLIST SCHEMAS
# ================================================================
class WishlistItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_image: Optional[str]
    price: Decimal
    discounted_price: Optional[Decimal]
    rating: Optional[Decimal]

    class Config:
        from_attributes = True


# ================================================================
# GENERAL RESPONSE SCHEMAS
# ================================================================
class SuccessResponse(BaseModel):
    success: bool = True
    message: str

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None
