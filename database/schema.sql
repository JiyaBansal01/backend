-- ============================================================
-- Flipkart Clone - MySQL Database Schema
-- ============================================================
-- This file creates all tables needed for the e-commerce app.
-- Run this file once to set up your database.

CREATE DATABASE IF NOT EXISTS flipkart_clone;
USE flipkart_clone;

-- -------------------------------------------------------
-- CATEGORIES table: Groups products into categories
-- Example: Electronics, Fashion, Home & Kitchen
-- -------------------------------------------------------
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,                  -- e.g. "Electronics"
    slug VARCHAR(100) NOT NULL UNIQUE,           -- URL-friendly name e.g. "electronics"
    icon VARCHAR(255),                           -- emoji or icon URL
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -------------------------------------------------------
-- USERS table: Stores customer accounts
-- -------------------------------------------------------
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,         -- bcrypt hashed password
    phone VARCHAR(20),
    avatar_url VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- -------------------------------------------------------
-- PRODUCTS table: All products listed on the platform
-- -------------------------------------------------------
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,                  -- Full product name
    slug VARCHAR(255) NOT NULL UNIQUE,           -- URL slug
    brand VARCHAR(100),
    description TEXT,                            -- Long product description
    specifications JSON,                         -- Key-value specs as JSON
    price DECIMAL(10, 2) NOT NULL,               -- Original MRP price
    discounted_price DECIMAL(10, 2),             -- Sale price (if any)
    discount_percent INT DEFAULT 0,              -- Calculated discount %
    stock_quantity INT DEFAULT 0,                -- How many units available
    rating DECIMAL(3, 2) DEFAULT 0.00,           -- Average rating (0-5)
    review_count INT DEFAULT 0,                  -- Number of reviews
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- -------------------------------------------------------
-- PRODUCT_IMAGES table: Multiple images per product
-- First image is the thumbnail shown in listings
-- -------------------------------------------------------
CREATE TABLE product_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,            -- TRUE = shown in product card
    display_order INT DEFAULT 0,                 -- Carousel order
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- -------------------------------------------------------
-- ADDRESSES table: Shipping addresses for users
-- -------------------------------------------------------
CREATE TABLE addresses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address_line1 VARCHAR(255) NOT NULL,
    address_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    address_type ENUM('HOME', 'WORK', 'OTHER') DEFAULT 'HOME',
    is_default BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- -------------------------------------------------------
-- CART_ITEMS table: Products added to cart (per session or user)
-- session_id is used when user is not logged in
-- -------------------------------------------------------
CREATE TABLE cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,                                 -- NULL if guest user
    session_id VARCHAR(100),                     -- For guest checkout
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    -- Prevent duplicate cart entries for same product
    UNIQUE KEY unique_cart_item (user_id, product_id),
    UNIQUE KEY unique_session_cart_item (session_id, product_id)
);

-- -------------------------------------------------------
-- ORDERS table: Placed orders
-- -------------------------------------------------------
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL UNIQUE,    -- e.g. "FK-2024-ABC123"
    user_id INT,
    session_id VARCHAR(100),
    shipping_address_id INT,
    -- Snapshot of address at time of order (in case address is later changed)
    shipping_address_snapshot JSON NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    shipping_fee DECIMAL(10, 2) DEFAULT 0.00,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED') DEFAULT 'PENDING',
    payment_method ENUM('COD', 'UPI', 'CARD', 'NETBANKING') DEFAULT 'COD',
    payment_status ENUM('PENDING', 'PAID', 'FAILED', 'REFUNDED') DEFAULT 'PENDING',
    notes TEXT,
    placed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- -------------------------------------------------------
-- ORDER_ITEMS table: Individual products in each order
-- We store price snapshot so historical orders stay accurate
-- -------------------------------------------------------
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id    INT,
    product_name  VARCHAR(255) NOT NULL,          -- Snapshot of name
    product_image VARCHAR(500),                  -- Snapshot of image
    quantity      INT NOT NULL,
    unit_price    DECIMAL(10, 2) NOT NULL,          -- Price at time of purchase
    total_price   DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
);

-- -------------------------------------------------------
-- WISHLIST table: Products saved for later
-- -------------------------------------------------------
CREATE TABLE wishlist_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_wishlist (user_id, product_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- -------------------------------------------------------
-- REVIEWS table: Product ratings and text reviews
-- -------------------------------------------------------
CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    title VARCHAR(200),
    body TEXT,
    is_verified_purchase BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY one_review_per_user (product_id, user_id),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================
-- INDEXES for performance optimization
-- These speed up common queries like search and filtering
-- ============================================================
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_price ON products(discounted_price);
CREATE INDEX idx_cart_user ON cart_items(user_id);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
