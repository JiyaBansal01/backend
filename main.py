"""
main.py - FastAPI Application Entry Point
==========================================
This is the starting point of our backend server.
FastAPI is a modern Python web framework that:
- Automatically generates API documentation at /docs
- Validates request/response data automatically
- Is very fast due to async support

HOW TO RUN:
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Import all our route handlers (like chapters in a book)
from routers import products, categories, cart, orders, users, wishlist

# Create the FastAPI application instance
app = FastAPI(
    title="Flipkart Clone API",
    description="Backend API for Flipkart-inspired e-commerce application",
    version="1.0.0",
    # These URLs show the auto-generated API documentation
    docs_url="/docs",
    redoc_url="/redoc"
)

# -------------------------------------------------------
# CORS (Cross-Origin Resource Sharing) Configuration
# This allows our React frontend (running on port 3000)
# to communicate with this backend (running on port 8000)
# Without CORS, browsers block these requests for security
# -------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # React dev server
        "http://localhost:5173",   # Vite dev server
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],           # Allow GET, POST, PUT, DELETE etc.
    allow_headers=["*"],           # Allow all headers
)

# -------------------------------------------------------
# Register Route Handlers
# Each router handles a specific feature area.
# The prefix is added to all routes in that router.
# Example: products router has /api/products/...
# -------------------------------------------------------
app.include_router(products.router,    prefix="/api/products",    tags=["Products"])
app.include_router(categories.router,  prefix="/api/categories",  tags=["Categories"])
app.include_router(cart.router,        prefix="/api/cart",        tags=["Cart"])
app.include_router(orders.router,      prefix="/api/orders",      tags=["Orders"])
app.include_router(users.router,       prefix="/api/users",       tags=["Users"])
app.include_router(wishlist.router,    prefix="/api/wishlist",    tags=["Wishlist"])


# -------------------------------------------------------
# Health Check Endpoint
# Useful to verify the server is running
# Visit: http://localhost:8000/health
# -------------------------------------------------------
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "Flipkart Clone API is running!"}


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Flipkart Clone API",
        "docs": "/docs",
        "health": "/health"
    }
