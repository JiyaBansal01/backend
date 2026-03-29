"""
database/connection.py - Database Connection Setup
====================================================
This file handles connecting to MySQL database.
We use SQLAlchemy ORM (Object Relational Mapper) which lets us
write Python code instead of raw SQL queries.

WHAT IS AN ORM?
    Instead of: SELECT * FROM products WHERE id = 1
    We write:   db.query(Product).filter(Product.id == 1).first()

    The ORM converts Python code to SQL automatically.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This keeps sensitive info like passwords out of code
load_dotenv()

# -------------------------------------------------------
# Database URL Format:
# dialect+driver://username:password@host:port/database_name
# -------------------------------------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@localhost:3306/flipkart_clone"
)

# Create the database engine (connection pool)
# echo=True prints SQL queries to console (helpful for debugging)
engine = create_engine(
    DATABASE_URL,
    echo=False,              # Set to True for SQL debugging
    pool_size=5,             # Keep 5 connections ready
    max_overflow=10,         # Allow up to 10 extra connections
    pool_pre_ping=True       # Verify connections before using them
)

# SessionLocal is a factory for creating database sessions
# Each request gets its own session (like its own workspace)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all our database models
# All model classes will inherit from this
Base = declarative_base()


def get_db():
    """
    Dependency function that provides a database session.
    
    This is used with FastAPI's Dependency Injection system.
    It creates a new session for each request and closes it after.
    
    Usage in route:
        @router.get("/")
        def get_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items
    """
    db = SessionLocal()
    try:
        yield db          # Give the session to the route handler
    finally:
        db.close()        # Always close the session, even if an error occurs
