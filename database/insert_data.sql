-- =====================================================================
-- Sample Data Insertion Script for Customer Churn Analytics System
-- Provides initial seed records for testing and standalone SQL workflows
-- =====================================================================

USE customer_churn_db;

-- 1. Insert Sample Customers
INSERT INTO customers (customer_code, first_name, last_name, email, age, gender, city, signup_date, membership_type) VALUES
('CUST-1001', 'Aarav', 'Sharma', 'aarav.sharma@example.com', 29, 'Male', 'Mumbai', '2023-01-15', 'Gold'),
('CUST-1002', 'Priya', 'Patel', 'priya.patel@example.com', 34, 'Female', 'Bengaluru', '2023-02-10', 'Platinum'),
('CUST-1003', 'Rahul', 'Verma', 'rahul.verma@example.com', 24, 'Male', 'Delhi', '2023-03-05', 'Silver'),
('CUST-1004', 'Ananya', 'Iyer', 'ananya.iyer@example.com', 41, 'Female', 'Chennai', '2022-11-20', 'Bronze'),
('CUST-1005', 'Vikram', 'Singh', 'vikram.singh@example.com', 48, 'Male', 'Hyderabad', '2022-09-12', 'Gold'),
('CUST-1006', 'Sneha', 'Nair', 'sneha.nair@example.com', 31, 'Female', 'Kochi', '2023-04-18', 'Silver'),
('CUST-1007', 'Rohan', 'Gupta', 'rohan.gupta@example.com', 27, 'Male', 'Pune', '2023-05-22', 'Platinum'),
('CUST-1008', 'Kavita', 'Reddy', 'kavita.reddy@example.com', 39, 'Female', 'Hyderabad', '2022-12-01', 'Bronze'),
('CUST-1009', 'Aditya', 'Joshi', 'aditya.joshi@example.com', 22, 'Male', 'Ahmedabad', '2023-06-11', 'Bronze'),
('CUST-1010', 'Pooja', 'Mehta', 'pooja.mehta@example.com', 36, 'Female', 'Mumbai', '2022-08-30', 'Gold');

-- 2. Insert Sample Products
INSERT INTO products (product_code, product_name, category, unit_price, cost_price, stock_quantity) VALUES
('PROD-E101', 'Noise Cancelling Wireless Headphones', 'Electronics', 149.99, 85.00, 150),
('PROD-E102', 'Ultra HD 4K Smart Monitor 27-inch', 'Electronics', 329.99, 210.00, 80),
('PROD-F201', 'Slim-Fit Organic Cotton Denim Jacket', 'Fashion & Apparel', 79.99, 32.00, 200),
('PROD-F202', 'Breathable Performance Running Shoes', 'Fashion & Apparel', 99.50, 44.00, 180),
('PROD-H301', 'Programmable Smart Air Fryer 5.8L', 'Home & Kitchen', 119.00, 62.00, 95),
('PROD-H302', 'Stainless Steel Thermal Coffee Carafe', 'Home & Kitchen', 34.99, 14.50, 250),
('PROD-B401', 'Anti-Aging Vitamin C Facial Serum', 'Beauty & Health', 29.95, 9.50, 300),
('PROD-B402', 'Sonic Electric Rechargeable Toothbrush', 'Beauty & Health', 49.99, 19.00, 220),
('PROD-S501', 'High-Density Non-Slip Yoga Mat', 'Sports & Fitness', 39.99, 15.00, 175),
('PROD-S502', 'Adjustable Quick-Select Dumbbell Pair', 'Sports & Fitness', 199.99, 110.00, 60);

-- 3. Insert Sample Orders
INSERT INTO orders (order_code, customer_id, order_date, order_status, gross_amount, discount_amount, net_amount) VALUES
('ORD-2024-001', 1, '2024-01-10', 'Delivered', 229.98, 20.00, 209.98),
('ORD-2024-002', 2, '2024-01-14', 'Delivered', 429.49, 40.00, 389.49),
('ORD-2024-003', 3, '2024-01-20', 'Delivered', 79.99, 0.00, 79.99),
('ORD-2024-004', 4, '2024-02-02', 'Delivered', 34.99, 0.00, 34.99),
('ORD-2024-005', 5, '2024-02-15', 'Delivered', 319.98, 25.00, 294.98),
('ORD-2024-006', 1, '2024-02-28', 'Delivered', 99.50, 10.00, 89.50),
('ORD-2024-007', 7, '2024-03-04', 'Delivered', 329.99, 30.00, 299.99),
('ORD-2024-008', 2, '2024-03-12', 'Delivered', 119.00, 10.00, 109.00),
('ORD-2024-009', 8, '2024-03-18', 'Delivered', 29.95, 0.00, 29.95),
('ORD-2024-010', 10, '2024-03-25', 'Delivered', 239.98, 20.00, 219.98);

-- 4. Insert Sample Order Items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount_rate, item_total) VALUES
(1, 1, 1, 149.99, 0.10, 134.99),
(1, 3, 1, 79.99, 0.00, 74.99),
(2, 2, 1, 329.99, 0.10, 296.99),
(2, 4, 1, 99.50, 0.05, 92.50),
(3, 3, 1, 79.99, 0.00, 79.99),
(4, 6, 1, 34.99, 0.00, 34.99),
(5, 5, 1, 119.00, 0.05, 114.00),
(5, 10, 1, 199.99, 0.10, 180.98),
(6, 4, 1, 99.50, 0.10, 89.50),
(7, 2, 1, 329.99, 0.10, 299.99),
(8, 5, 1, 119.00, 0.08, 109.00),
(9, 7, 1, 29.95, 0.00, 29.95),
(10, 1, 1, 149.99, 0.05, 142.49),
(10, 9, 2, 39.99, 0.10, 77.49);

-- 5. Insert Sample Payments
INSERT INTO payments (order_id, payment_date, payment_method, payment_status, amount) VALUES
(1, '2024-01-10', 'UPI', 'Completed', 209.98),
(2, '2024-01-14', 'Credit Card', 'Completed', 389.49),
(3, '2024-01-20', 'Debit Card', 'Completed', 79.99),
(4, '2024-02-02', 'Cash on Delivery', 'Completed', 34.99),
(5, '2024-02-15', 'Credit Card', 'Completed', 294.98),
(6, '2024-02-28', 'UPI', 'Completed', 89.50),
(7, '2024-03-04', 'Net Banking', 'Completed', 299.99),
(8, '2024-03-12', 'Credit Card', 'Completed', 109.00),
(9, '2024-03-18', 'UPI', 'Completed', 29.95),
(10, '2024-03-25', 'Credit Card', 'Completed', 219.98);

-- 6. Insert Sample Customer Churn Analytics Snapshot
INSERT INTO customer_churn (customer_id, total_orders, total_spend, average_order_value, days_since_last_purchase, purchase_frequency, support_tickets, satisfaction_score, membership_duration_months, churn) VALUES
(1, 2, 299.48, 149.74, 22, 0.850, 0, 4.8, 14, 0),
(2, 2, 498.49, 249.25, 18, 0.750, 1, 4.6, 13, 0),
(3, 1, 79.99, 79.99, 65, 0.250, 3, 2.8, 12, 1),
(4, 1, 34.99, 34.99, 82, 0.180, 4, 2.1, 16, 1),
(5, 1, 294.98, 294.98, 45, 0.400, 1, 4.0, 18, 0),
(6, 0, 0.00, 0.00, 120, 0.000, 5, 1.9, 11, 1),
(7, 1, 299.99, 299.99, 28, 0.600, 0, 4.9, 10, 0),
(8, 1, 29.95, 29.95, 94, 0.120, 3, 2.4, 15, 1),
(9, 0, 0.00, 0.00, 150, 0.000, 2, 2.7, 9, 1),
(10, 1, 219.98, 219.98, 12, 0.900, 0, 4.7, 19, 0);
