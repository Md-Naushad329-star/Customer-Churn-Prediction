-- =====================================================================
-- Customer Sales, Revenue & Churn Prediction Analytics System
-- Relational Database Schema (MySQL 8.0+)
-- =====================================================================

DROP DATABASE IF EXISTS customer_churn_db;
CREATE DATABASE customer_churn_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

USE customer_churn_db;

-- ---------------------------------------------------------------------
-- Table: customers
-- Stores demographic and account profile details for each customer
-- ---------------------------------------------------------------------
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_code VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    age INT NOT NULL CHECK (age >= 18 AND age <= 100),
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    city VARCHAR(60) NOT NULL,
    signup_date DATE NOT NULL,
    membership_type ENUM('Bronze', 'Silver', 'Gold', 'Platinum') NOT NULL DEFAULT 'Bronze',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_customer_city (city),
    INDEX idx_customer_membership (membership_type),
    INDEX idx_customer_signup (signup_date)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Table: products
-- Stores catalog items, retail pricing, categories and unit costs
-- ---------------------------------------------------------------------
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_code VARCHAR(20) NOT NULL UNIQUE,
    product_name VARCHAR(120) NOT NULL,
    category ENUM('Electronics', 'Fashion & Apparel', 'Home & Kitchen', 'Beauty & Health', 'Sports & Fitness') NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price > 0),
    cost_price DECIMAL(10, 2) NOT NULL CHECK (cost_price > 0),
    stock_quantity INT NOT NULL DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_product_category (category)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Table: orders
-- Stores header-level transaction data placed by customers
-- ---------------------------------------------------------------------
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    order_code VARCHAR(25) NOT NULL UNIQUE,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    order_status ENUM('Delivered', 'Shipped', 'Processing', 'Cancelled', 'Returned') NOT NULL DEFAULT 'Delivered',
    gross_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    discount_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    net_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) 
        REFERENCES customers(customer_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    INDEX idx_orders_customer (customer_id),
    INDEX idx_orders_date (order_date),
    INDEX idx_orders_status (order_status)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Table: order_items
-- Stores line-item details for individual products within an order
-- ---------------------------------------------------------------------
CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    discount_rate DECIMAL(5, 2) NOT NULL DEFAULT 0.00 CHECK (discount_rate >= 0 AND discount_rate <= 1.00),
    item_total DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_items_order FOREIGN KEY (order_id) 
        REFERENCES orders(order_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT fk_items_product FOREIGN KEY (product_id) 
        REFERENCES products(product_id) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
    INDEX idx_items_order (order_id),
    INDEX idx_items_product (product_id)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Table: payments
-- Records settlement and payment processing methods for orders
-- ---------------------------------------------------------------------
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    payment_date DATE NOT NULL,
    payment_method ENUM('Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Cash on Delivery') NOT NULL,
    payment_status ENUM('Completed', 'Pending', 'Failed', 'Refunded') NOT NULL DEFAULT 'Completed',
    amount DECIMAL(10, 2) NOT NULL CHECK (amount >= 0),
    CONSTRAINT fk_payments_order FOREIGN KEY (order_id) 
        REFERENCES orders(order_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    INDEX idx_payments_order (order_id),
    INDEX idx_payments_method (payment_method)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Table: customer_churn
-- Analytical snapshot table capturing behavioural telemetry & churn
-- ---------------------------------------------------------------------
CREATE TABLE customer_churn (
    churn_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL UNIQUE,
    total_orders INT NOT NULL DEFAULT 0,
    total_spend DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    average_order_value DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    days_since_last_purchase INT NOT NULL DEFAULT 0,
    purchase_frequency DECIMAL(8, 3) NOT NULL DEFAULT 0.00,
    support_tickets INT NOT NULL DEFAULT 0,
    satisfaction_score DECIMAL(3, 1) NOT NULL CHECK (satisfaction_score >= 1.0 AND satisfaction_score <= 5.0),
    membership_duration_months INT NOT NULL DEFAULT 0,
    churn TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0 = Retained, 1 = Churned',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_churn_customer FOREIGN KEY (customer_id) 
        REFERENCES customers(customer_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    INDEX idx_churn_flag (churn),
    INDEX idx_churn_spend (total_spend),
    INDEX idx_churn_recency (days_since_last_purchase)
) ENGINE=InnoDB;
