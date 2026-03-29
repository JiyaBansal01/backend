"""
models/models.py - Database Table Models
==========================================
These Python classes represent database tables.
Each class = one table, each attribute = one column.

SQLAlchemy reads these classes and:
1. Creates the actual database tables
2. Handles INSERT, SELECT, UPDATE, DELETE automatically
"""

from sqlalchemy import (
    Column, Integer, String, Text, DECIMAL, Boolean,
    ForeignKey, JSON, Enum, TIMESTAMP, func
)
from sqlalchemy.orm import relationship
from database.connection import Base
import enum


# -------------------------------------------------------
# Enum Types (restricted value lists)
# -------------------------------------------------------
class OrderStatus(str, enum.Enum):
    PENDING   = "PENDING"
    CONFIRMED = "CONFIRMED"
    SHIPPED   = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class PaymentMethod(str, enum.Enum):
    COD        = "COD"
    UPI        = "UPI"
    CARD       = "CARD"
    NETBANKING = "NETBANKING"

class AddressType(str, enum.Enum):
    HOME  = "HOME"
    WORK  = "WORK"
    OTHER = "OTHER"


# -------------------------------------------------------
# CATEGORY Model
# -------------------------------------------------------
class Category(Base):
    __tablename__ = "categories"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(100), nullable=False)
    slug       = Column(String(100), nullable=False, unique=True)
    icon       = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())

    # One category can have MANY products
    products = relationship("Product", back_populates="category")


# -------------------------------------------------------
# USER Model
# -------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String(100), nullable=False)
    email         = Column(String(150), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    phone         = Column(String(20))
    avatar_url    = Column(String(255))
    is_active     = Column(Boolean, default=True)
    created_at    = Column(TIMESTAMP, server_default=func.now())
    updated_at    = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    cart_items     = relationship("CartItem", back_populates="user")
    orders         = relationship("Order", back_populates="user")
    addresses      = relationship("Address", back_populates="user")
    wishlist_items = relationship("WishlistItem", back_populates="user")


# -------------------------------------------------------
# PRODUCT Model
# -------------------------------------------------------
class Product(Base):
    __tablename__ = "products"

    id               = Column(Integer, primary_key=True, index=True)
    category_id      = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name             = Column(String(255), nullable=False, index=True)
    slug             = Column(String(255), nullable=False, unique=True)
    brand            = Column(String(100))
    description      = Column(Text)
    specifications   = Column(JSON)                       # Stored as JSON object
    price            = Column(DECIMAL(10, 2), nullable=False)
    discounted_price = Column(DECIMAL(10, 2))
    discount_percent = Column(Integer, default=0)
    stock_quantity   = Column(Integer, default=0)
    rating           = Column(DECIMAL(3, 2), default=0.00)
    review_count     = Column(Integer, default=0)
    is_active        = Column(Boolean, default=True)
    created_at       = Column(TIMESTAMP, server_default=func.now())
    updated_at       = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    category       = relationship("Category", back_populates="products")
    images         = relationship("ProductImage", back_populates="product", order_by="ProductImage.display_order")
    cart_items     = relationship("CartItem", back_populates="product")
    order_items    = relationship("OrderItem", back_populates="product")
    wishlist_items = relationship("WishlistItem", back_populates="product")


# -------------------------------------------------------
# PRODUCT IMAGE Model
# -------------------------------------------------------
class ProductImage(Base):
    __tablename__ = "product_images"

    id            = Column(Integer, primary_key=True, index=True)
    product_id    = Column(Integer, ForeignKey("products.id"), nullable=False)
    image_url     = Column(String(500), nullable=False)
    is_primary    = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)

    product = relationship("Product", back_populates="images")


# -------------------------------------------------------
# ADDRESS Model
# -------------------------------------------------------
class Address(Base):
    __tablename__ = "addresses"

    id            = Column(Integer, primary_key=True, index=True)
    user_id       = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name     = Column(String(100), nullable=False)
    phone         = Column(String(20), nullable=False)
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255))
    city          = Column(String(100), nullable=False)
    state         = Column(String(100), nullable=False)
    pincode       = Column(String(10), nullable=False)
    address_type  = Column(Enum(AddressType), default=AddressType.HOME)
    is_default    = Column(Boolean, default=False)

    user = relationship("User", back_populates="addresses")


# -------------------------------------------------------
# CART ITEM Model
# -------------------------------------------------------
class CartItem(Base):
    __tablename__ = "cart_items"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String(100))              # For guest users
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity   = Column(Integer, nullable=False, default=1)
    added_at   = Column(TIMESTAMP, server_default=func.now())

    user    = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")


# -------------------------------------------------------
# ORDER Model
# -------------------------------------------------------
class Order(Base):
    __tablename__ = "orders"

    id                       = Column(Integer, primary_key=True, index=True)
    order_number             = Column(String(50), nullable=False, unique=True)
    user_id                  = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id               = Column(String(100))
    shipping_address_id      = Column(Integer, ForeignKey("addresses.id"), nullable=True)
    shipping_address_snapshot = Column(JSON, nullable=False)  # Address at time of order
    subtotal                 = Column(DECIMAL(10, 2), nullable=False)
    shipping_fee             = Column(DECIMAL(10, 2), default=0.00)
    total_amount             = Column(DECIMAL(10, 2), nullable=False)
    status                   = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    payment_method           = Column(Enum(PaymentMethod), default=PaymentMethod.COD)
    payment_status           = Column(String(20), default="PENDING")
    notes                    = Column(Text)
    placed_at                = Column(TIMESTAMP, server_default=func.now())
    updated_at               = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user        = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")


# -------------------------------------------------------
# ORDER ITEM Model
# -------------------------------------------------------
class OrderItem(Base):
    __tablename__ = "order_items"

    id            = Column(Integer, primary_key=True, index=True)
    order_id      = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id    = Column(Integer, ForeignKey("products.id"), nullable=True)
    product_name  = Column(String(255), nullable=False)     # Snapshot
    product_image = Column(String(500))                     # Snapshot
    quantity      = Column(Integer, nullable=False)
    unit_price    = Column(DECIMAL(10, 2), nullable=False)  # Price at time of purchase
    total_price   = Column(DECIMAL(10, 2), nullable=False)

    order   = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")


# -------------------------------------------------------
# WISHLIST ITEM Model
# -------------------------------------------------------
class WishlistItem(Base):
    __tablename__ = "wishlist_items"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    added_at   = Column(TIMESTAMP, server_default=func.now())

    user    = relationship("User", back_populates="wishlist_items")
    product = relationship("Product", back_populates="wishlist_items")
