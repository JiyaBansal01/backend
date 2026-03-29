"""
routers/products.py - Product API Endpoints
=============================================
All API routes related to products.

ENDPOINTS:
    GET  /api/products/           - List all products (with search & filter)
    GET  /api/products/{id}       - Get single product details
    GET  /api/products/slug/{slug} - Get product by URL slug
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from typing import Optional, List
import math

from database.connection import get_db
from models.models import Product, ProductImage, Category
from schemas.schemas import ProductListItem, ProductDetail, ProductsResponse

# Create a router (like a mini-app for products)
router = APIRouter()


def get_primary_image(product: Product) -> Optional[str]:
    """Helper: Get the primary (main) image URL for a product"""
    for img in product.images:
        if img.is_primary:
            return img.image_url
    # Fallback: return first image if no primary set
    if product.images:
        return product.images[0].image_url
    return None


@router.get("/", response_model=ProductsResponse)
def get_products(
    # Query parameters for filtering - all optional
    search:      Optional[str] = Query(None,  description="Search by product name"),
    category_id: Optional[int] = Query(None,  description="Filter by category ID"),
    category_slug: Optional[str] = Query(None, description="Filter by category slug"),
    min_price:   Optional[float] = Query(None, description="Minimum price filter"),
    max_price:   Optional[float] = Query(None, description="Maximum price filter"),
    sort_by:     Optional[str] = Query("created_at", description="Sort field: price, rating, name"),
    sort_order:  Optional[str] = Query("desc",  description="asc or desc"),
    page:        int = Query(1,   ge=1,   description="Page number"),
    per_page:    int = Query(20,  ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get all products with optional filtering, searching, and pagination.
    
    This is the main product listing endpoint used by:
    - Home page
    - Category pages
    - Search results
    """
    # Start with base query - join images and category for efficiency
    query = db.query(Product).options(
        joinedload(Product.images),
        joinedload(Product.category)
    ).filter(Product.is_active == True)

    # Apply search filter (case-insensitive name search)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Product.name.ilike(search_term),
                Product.brand.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )

    # Apply category filter by ID
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    # Apply category filter by slug (more SEO friendly)
    if category_slug:
        category = db.query(Category).filter(Category.slug == category_slug).first()
        if category:
            query = query.filter(Product.category_id == category.id)

    # Price range filters
    if min_price is not None:
        query = query.filter(Product.discounted_price >= min_price)
    if max_price is not None:
        query = query.filter(Product.discounted_price <= max_price)

    # Count total before pagination (for frontend to show "Page 1 of 5")
    total = query.count()

    # Apply sorting
    if sort_by == "price":
        sort_col = Product.discounted_price
    elif sort_by == "rating":
        sort_col = Product.rating
    elif sort_by == "name":
        sort_col = Product.name
    else:
        sort_col = Product.id

    if sort_order == "asc":
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())

    # Apply pagination (skip to correct page, take per_page items)
    offset = (page - 1) * per_page
    products = query.offset(offset).limit(per_page).all()

    # Convert to response format
    product_list = []
    for p in products:
        product_list.append(ProductListItem(
            id=p.id,
            name=p.name,
            slug=p.slug,
            brand=p.brand,
            price=p.price,
            discounted_price=p.discounted_price or p.price,
            discount_percent=p.discount_percent or 0,
            rating=p.rating,
            review_count=p.review_count,
            stock_quantity=p.stock_quantity,
            primary_image=get_primary_image(p),
            category_id=p.category_id,
            category_name=p.category.name if p.category else None
        ))

    return ProductsResponse(
        products=product_list,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=math.ceil(total / per_page)
    )


@router.get("/slug/{slug}", response_model=ProductDetail)
def get_product_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get a single product by its URL slug"""
    product = db.query(Product).options(
        joinedload(Product.images),
        joinedload(Product.category)
    ).filter(
        Product.slug == slug,
        Product.is_active == True
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail=f"Product with slug '{slug}' not found")

    return product


@router.get("/{product_id}", response_model=ProductDetail)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """Get a single product by its ID"""
    product = db.query(Product).options(
        joinedload(Product.images),
        joinedload(Product.category)
    ).filter(
        Product.id == product_id,
        Product.is_active == True
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")

    return product
