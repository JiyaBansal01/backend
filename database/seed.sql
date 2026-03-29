-- ============================================================
-- Flipkart Clone - Sample Seed Data
-- Run this AFTER schema.sql to populate the database
-- ============================================================

USE flipkart_clone;

-- -------------------------------------------------------
-- CATEGORIES
-- -------------------------------------------------------
INSERT INTO categories (name, slug, emoji) VALUES
('Electronics',       'electronics',       '📱'),
('Fashion',           'fashion',           '👗'),
('Home & Kitchen',    'home-kitchen',      '🏠'),
('Books',             'books',             '📚'),
('Sports & Fitness',  'sports-fitness',    '⚽'),
('Toys & Games',      'toys-games',        '🎮'),
('Beauty & Personal Care', 'beauty',       '💄'),
('Grocery',           'grocery',           '🛒');

-- -------------------------------------------------------
-- DEFAULT USER (no login needed initially)
-- Password: "password123" (bcrypt hash shown below)
-- -------------------------------------------------------
INSERT INTO users (name, email, password_hash, phone) VALUES
('Rahul Sharma', 'rahul@example.com', '$2b$12$examplehash', '9876543210');

-- -------------------------------------------------------
-- PRODUCTS - Electronics
-- -------------------------------------------------------
INSERT INTO products (category_id, name, slug, brand, description, specifications, price, discounted_price, discount_percent, stock_quantity, rating, review_count) VALUES
(1, 'Samsung Galaxy S24 Ultra 5G (256GB)', 'samsung-galaxy-s24-ultra', 'Samsung',
 'The Samsung Galaxy S24 Ultra is a premium flagship smartphone featuring a stunning 6.8-inch Dynamic AMOLED display, advanced AI photography, and the built-in S Pen. Experience next-gen performance with the Snapdragon 8 Gen 3 chipset.',
 '{"Display": "6.8-inch Dynamic AMOLED 2X, 120Hz", "Processor": "Snapdragon 8 Gen 3", "RAM": "12GB", "Storage": "256GB", "Battery": "5000mAh", "Camera": "200MP + 12MP + 10MP + 10MP", "OS": "Android 14", "5G": "Yes"}',
 124999.00, 89999.00, 28, 50, 4.60, 2341),

(1, 'Apple iPhone 15 Pro (128GB, Natural Titanium)', 'apple-iphone-15-pro', 'Apple',
 'iPhone 15 Pro features a Grade 5 titanium design — the same alloy used in aerospace. Get the latest iPhone with A17 Pro chip, ProMotion technology, and the versatile 48MP Main camera with next-generation portraits.',
 '{"Display": "6.1-inch Super Retina XDR, 120Hz", "Processor": "A17 Pro Chip", "RAM": "8GB", "Storage": "128GB", "Battery": "3274mAh", "Camera": "48MP + 12MP + 12MP", "OS": "iOS 17", "5G": "Yes"}',
 134900.00, 119900.00, 11, 30, 4.70, 5821),

(1, 'OnePlus Nord CE3 Lite 5G (128GB, Pastel Lime)', 'oneplus-nord-ce3-lite', 'OnePlus',
 'The OnePlus Nord CE3 Lite 5G brings flagship-inspired features to a budget-friendly price. Featuring a large 5000mAh battery with SUPERVOOC fast charging and a vibrant 120Hz display.',
 '{"Display": "6.72-inch LCD, 120Hz", "Processor": "Snapdragon 695", "RAM": "8GB", "Storage": "128GB", "Battery": "5000mAh", "Camera": "108MP + 2MP + 2MP", "OS": "OxygenOS 13.1", "5G": "Yes"}',
 19999.00, 16999.00, 15, 200, 4.20, 8764),

(1, 'boAt Airdopes 141 Bluetooth Truly Wireless Earbuds', 'boat-airdopes-141', 'boAt',
 'boAt Airdopes 141 features 42H total playback, Beast Mode low latency gaming, ASAP Charge, and IWS. Designed for superior sound quality with 6mm drivers and environmental noise cancellation.',
 '{"Driver Size": "6mm", "Battery Life": "42 Hours total", "Connectivity": "Bluetooth 5.1", "Water Resistance": "IPX4", "Charging": "USB-C", "Latency": "80ms (Beast Mode)"}',
 3999.00, 1299.00, 68, 500, 4.10, 98234),

(1, 'LG 80 cm (32 inches) HD Ready Smart LED TV', 'lg-32-hd-smart-tv', 'LG',
 'Experience the world of entertainment with the LG HD Ready Smart LED TV. Enjoy content from apps like Netflix, Prime Video, Disney+ Hotstar with ThinQ AI and webOS platform.',
 '{"Screen Size": "32 inches", "Resolution": "HD Ready (1366x768)", "Smart": "Yes (webOS)", "HDR": "No", "Connectivity": "3 HDMI, 2 USB", "Refresh Rate": "60Hz"}',
 29990.00, 19990.00, 33, 75, 4.30, 12453);

-- -------------------------------------------------------
-- PRODUCTS - Fashion
-- -------------------------------------------------------
INSERT INTO products (category_id, name, slug, brand, description, specifications, price, discounted_price, discount_percent, stock_quantity, rating, review_count) VALUES
(2, 'Allen Solly Men Slim Fit Formal Shirt', 'allen-solly-slim-fit-shirt', 'Allen Solly',
 'This Allen Solly shirt features premium cotton fabric with a slim-fit cut, perfect for office and formal occasions. Easy-care fabric resists wrinkles throughout the day.',
 '{"Fabric": "100% Cotton", "Fit": "Slim Fit", "Sleeve": "Full Sleeve", "Occasion": "Formal, Office", "Wash Care": "Machine Wash"}',
 1999.00, 999.00, 50, 300, 4.10, 3421),

(2, 'Levi`s Women Skinny Fit Jeans', 'levis-women-skinny-jeans', 'Levi\'s',
 'The iconic Levi\'s 311 Shaping Skinny jeans are designed to flatter your curves while providing all-day comfort. Made with a blend of cotton and stretch fabric for the perfect fit.',
 '{"Fabric": "76% Cotton, 23% Polyester, 1% Elastane", "Fit": "Skinny", "Rise": "Mid Rise", "Closure": "Zip fly with button", "Wash": "Dark Wash"}',
 3999.00, 2499.00, 38, 150, 4.30, 1876),

(2, 'Nike Air Max 270 Running Shoes', 'nike-air-max-270', 'Nike',
 'The Nike Air Max 270 features the biggest heel Air unit yet, providing all-day comfort. The design draws inspiration from Air Max icons, giving you heritage details with modern comfort.',
 '{"Upper": "Mesh and synthetic", "Sole": "Rubber", "Closure": "Lace-up", "Technology": "Air Max 270 unit", "Occasion": "Running, Casual", "Available Sizes": "UK 6-11"}',
 12995.00, 9995.00, 23, 80, 4.40, 5643);

-- -------------------------------------------------------
-- PRODUCTS - Home & Kitchen
-- -------------------------------------------------------
INSERT INTO products (category_id, name, slug, brand, description, specifications, price, discounted_price, discount_percent, stock_quantity, rating, review_count) VALUES
(3, 'Instant Pot Duo 7-in-1 Electric Pressure Cooker', 'instant-pot-duo-7in1', 'Instant Pot',
 'The Instant Pot Duo is 7 appliances in 1: pressure cooker, slow cooker, rice cooker, steamer, sauté pan, yogurt maker and warmer. Cook up to 70% faster than traditional methods.',
 '{"Capacity": "5.7 Litre", "Functions": "7 in 1", "Material": "Stainless Steel", "Wattage": "1000W", "Safety": "10 safety mechanisms", "Preset Programs": "13"}',
 14995.00, 8999.00, 40, 120, 4.50, 23456),

(3, 'Philips HL7756/00 750W Mixer Grinder', 'philips-mixer-grinder', 'Philips',
 'Philips HL7756/00 Mixer Grinder comes with 750W motor and 3 multipurpose jars that help you do all kitchen tasks from making juices, chutneys to grinding dry spices effortlessly.',
 '{"Power": "750W", "Jars": "3 (1.5L, 1L, 0.4L)", "Speed Settings": "3 + Pulse", "Material": "Stainless Steel Jars", "Warranty": "2 Years"}',
 4295.00, 2899.00, 33, 200, 4.20, 8901);

-- -------------------------------------------------------
-- PRODUCTS - Books
-- -------------------------------------------------------
INSERT INTO products (category_id, name, slug, brand, description, specifications, price, discounted_price, discount_percent, stock_quantity, rating, review_count) VALUES
(4, 'Atomic Habits by James Clear', 'atomic-habits-james-clear', 'Penguin Random House',
 'Atomic Habits is a revolutionary guide to making good habits, breaking bad ones, and getting 1% better every day. Discover a proven framework for improving every day based on the author\'s research.',
 '{"Author": "James Clear", "Pages": "320", "Language": "English", "Format": "Paperback", "Genre": "Self-Help, Productivity", "ISBN": "9781847941831"}',
 999.00, 399.00, 60, 500, 4.80, 45621),

(4, 'Rich Dad Poor Dad by Robert T. Kiyosaki', 'rich-dad-poor-dad', 'Plata Publishing',
 'Rich Dad Poor Dad is Robert\'s story of growing up with two dads — his real father and the father of his best friend — and the ways in which both men shaped his thoughts about money and investing.',
 '{"Author": "Robert T. Kiyosaki", "Pages": "336", "Language": "English", "Format": "Paperback", "Genre": "Finance, Personal Development"}',
 499.00, 249.00, 50, 400, 4.70, 32109);

-- -------------------------------------------------------
-- PRODUCTS - Sports
-- -------------------------------------------------------
INSERT INTO products (category_id, name, slug, brand, description, specifications, price, discounted_price, discount_percent, stock_quantity, rating, review_count) VALUES
(5, 'Strauss ST-1001 Yoga Mat Anti-Skid', 'strauss-yoga-mat', 'Strauss',
 'Strauss Yoga Mat is made with eco-friendly TPE material. Anti-skid surface ensures grip during complex poses. 6mm thick cushioning protects joints during workout sessions.',
 '{"Material": "TPE (Eco-friendly)", "Thickness": "6mm", "Dimensions": "183 x 61 cm", "Weight": "1kg", "Includes": "Carry bag"}',
 1999.00, 899.00, 55, 350, 4.30, 15432),

(5, 'Cosco Authentic Football Size 5', 'cosco-football-size-5', 'Cosco',
 'Cosco Authentic football is designed for professional-level play. The 32-panel construction with premium synthetic leather ensures consistent flight and durability on any surface.',
 '{"Size": "5 (Standard)", "Material": "Synthetic Leather", "Panels": "32", "Bladder": "Butyl", "Suitable for": "Grass, Artificial Turf", "Circumference": "68-70 cm"}',
 799.00, 599.00, 25, 200, 4.10, 6789);

-- -------------------------------------------------------
-- PRODUCT IMAGES
-- Using Unsplash-style placeholder images
-- -------------------------------------------------------
INSERT INTO product_images (product_id, image_url, is_primary, display_order) VALUES
-- Samsung Galaxy S24 Ultra (product_id=1)
(1, 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=500', TRUE, 1),
(1, 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=500', FALSE, 2),
(1, 'https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?w=500', FALSE, 3),

-- iPhone 15 Pro (product_id=2)
(2, 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=500', TRUE, 1),
(2, 'https://images.unsplash.com/photo-1678685888221-cda773a3dcdb?w=500', FALSE, 2),
(2, 'https://images.unsplash.com/photo-1684503369431-d5386a8b6a5a?w=500', FALSE, 3),

-- OnePlus Nord (product_id=3)
(3, 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500', TRUE, 1),
(3, 'https://images.unsplash.com/photo-1567581935884-3349723552ca?w=500', FALSE, 2),

-- boAt Earbuds (product_id=4)
(4, 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500', TRUE, 1),
(4, 'https://images.unsplash.com/photo-1560393464-5c69a73c5770?w=500', FALSE, 2),

-- LG TV (product_id=5)
(5, 'https://images.unsplash.com/photo-1593305841991-05c297ba4575?w=500', TRUE, 1),
(5, 'https://images.unsplash.com/photo-1461151304267-38535e780c79?w=500', FALSE, 2),

-- Allen Solly Shirt (product_id=6)
(6, 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500', TRUE, 1),
(6, 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500', FALSE, 2),

-- Levi's Jeans (product_id=7)
(7, 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=500', TRUE, 1),
(7, 'https://images.unsplash.com/photo-1475178626620-a4d074967452?w=500', FALSE, 2),

-- Nike Air Max (product_id=8)
(8, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500', TRUE, 1),
(8, 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500', FALSE, 2),

-- Instant Pot (product_id=9)
(9, 'https://images.unsplash.com/photo-1585515320310-259814833e62?w=500', TRUE, 1),
(9, 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500', FALSE, 2),

-- Philips Mixer (product_id=10)
(10, 'https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=500', TRUE, 1),

-- Atomic Habits (product_id=11)
(11, 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500', TRUE, 1),
(11, 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500', FALSE, 2),

-- Rich Dad Poor Dad (product_id=12)
(12, 'https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=500', TRUE, 1),

-- Strauss Yoga Mat (product_id=13)
(13, 'https://images.unsplash.com/photo-1592432678016-e910b452f9a2?w=500', TRUE, 1),
(13, 'https://images.unsplash.com/photo-1601925228110-24c7ecddc7c7?w=500', FALSE, 2),

-- Cosco Football (product_id=14)
(14, 'https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=500', TRUE, 1),
(14, 'https://images.unsplash.com/photo-1551958219-acbc595d887f?w=500', FALSE, 2);
