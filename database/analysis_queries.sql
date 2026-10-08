-- =====================================================================
-- Customer Sales, Revenue & Churn Prediction Analytics System
-- Business Intelligence & Analytical SQL Queries (MySQL 8.0+)
-- =====================================================================

USE customer_churn_db;

-- =====================================================================
-- 1. OVERALL REVENUE & SALES KPIS
-- Aggregate calculations for total transactions, revenue, and gross sales
-- =====================================================================
SELECT 
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS paying_customers,
    ROUND(SUM(o.gross_amount), 2) AS total_gross_sales,
    ROUND(SUM(o.discount_amount), 2) AS total_discounts_given,
    ROUND(SUM(o.net_amount), 2) AS total_net_revenue,
    ROUND(AVG(o.net_amount), 2) AS average_order_value
FROM orders o
WHERE o.order_status IN ('Delivered', 'Shipped');


-- =====================================================================
-- 2. MONTHLY REVENUE & SALES GROWTH TRENDS
-- Demonstrating DATE_FORMAT, GROUP BY, ORDER BY, and Window Functions (LAG)
-- =====================================================================
WITH MonthlySales AS (
    SELECT 
        DATE_FORMAT(o.order_date, '%Y-%m') AS sales_month,
        COUNT(o.order_id) AS orders_count,
        ROUND(SUM(o.net_amount), 2) AS monthly_revenue,
        ROUND(AVG(o.net_amount), 2) AS monthly_aov
    FROM orders o
    WHERE o.order_status IN ('Delivered', 'Shipped')
    GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
)
SELECT 
    sales_month,
    orders_count,
    monthly_revenue,
    monthly_aov,
    LAG(monthly_revenue, 1) OVER (ORDER BY sales_month) AS previous_month_revenue,
    ROUND(
        ((monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY sales_month)) / 
        LAG(monthly_revenue, 1) OVER (ORDER BY sales_month)) * 100, 
        2
    ) AS mom_growth_percentage
FROM MonthlySales
ORDER BY sales_month;


-- =====================================================================
-- 3. TOP-SELLING PRODUCTS BY REVENUE & VOLUME
-- Using INNER JOIN across orders, order_items, and products
-- =====================================================================
SELECT 
    p.product_id,
    p.product_code,
    p.product_name,
    p.category,
    SUM(oi.quantity) AS total_units_sold,
    ROUND(SUM(oi.item_total), 2) AS gross_revenue_generated,
    ROUND(SUM(oi.quantity * p.cost_price), 2) AS total_cost_of_goods,
    ROUND(SUM(oi.item_total) - SUM(oi.quantity * p.cost_price), 2) AS gross_profit,
    ROUND(
        ((SUM(oi.item_total) - SUM(oi.quantity * p.cost_price)) / SUM(oi.item_total)) * 100, 
        2
    ) AS profit_margin_percentage
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id
INNER JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Delivered'
GROUP BY p.product_id, p.product_code, p.product_name, p.category
ORDER BY gross_revenue_generated DESC
LIMIT 10;


-- =====================================================================
-- 4. REVENUE BY PRODUCT CATEGORY & CITY
-- Multidimensional slice using JOIN and GROUP BY
-- =====================================================================
SELECT 
    c.city,
    p.category,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.item_total), 2) AS category_revenue
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE o.order_status = 'Delivered'
GROUP BY c.city, p.category
ORDER BY c.city ASC, category_revenue DESC;


-- =====================================================================
-- 5. CUSTOMER PURCHASE FREQUENCY & REPEAT PURCHASE RATE
-- Subquery and CASE statement to analyze one-time vs repeat buyers
-- =====================================================================
SELECT 
    customer_order_bracket,
    COUNT(customer_id) AS customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM customers), 2) AS percentage_of_customer_base,
    ROUND(SUM(total_spent), 2) AS group_total_spend,
    ROUND(AVG(total_spent), 2) AS group_avg_spend
FROM (
    SELECT 
        c.customer_id,
        COUNT(o.order_id) AS order_count,
        COALESCE(SUM(o.net_amount), 0) AS total_spent,
        CASE 
            WHEN COUNT(o.order_id) = 0 THEN '0 Orders (Inactive)'
            WHEN COUNT(o.order_id) = 1 THEN '1 Order (One-Time Buyer)'
            WHEN COUNT(o.order_id) BETWEEN 2 AND 4 THEN '2-4 Orders (Repeat Buyer)'
            ELSE '5+ Orders (Loyal Buyer)'
        END AS customer_order_bracket
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.order_status = 'Delivered'
    GROUP BY c.customer_id
) sub
GROUP BY customer_order_bracket
ORDER BY customer_count DESC;


-- =====================================================================
-- 6. CUSTOMER LIFETIME VALUE (CLV) & SEGMENTATION (RFM PROXIES)
-- Evaluates Recency, Frequency, and Monetary (RFM) value
-- =====================================================================
SELECT 
    c.customer_id,
    c.customer_code,
    CONCAT(c.first_name, ' ', c.last_name) AS full_name,
    c.membership_type,
    c.city,
    cc.total_orders,
    cc.total_spend AS lifetime_revenue,
    cc.average_order_value,
    cc.days_since_last_purchase,
    CASE 
        WHEN cc.total_spend >= 500 AND cc.days_since_last_purchase <= 45 THEN 'VIP Champion'
        WHEN cc.total_spend >= 300 AND cc.days_since_last_purchase <= 90 THEN 'High Value Active'
        WHEN cc.total_spend >= 300 AND cc.days_since_last_purchase > 90 THEN 'High Value At Risk'
        WHEN cc.total_spend < 300 AND cc.days_since_last_purchase <= 60 THEN 'Promising Occasional'
        ELSE 'Low Engagement / Churn Candidate'
    END AS customer_segment
FROM customers c
INNER JOIN customer_churn cc ON c.customer_id = cc.customer_id
ORDER BY cc.total_spend DESC
LIMIT 20;


-- =====================================================================
-- 7. CHURN RATE ANALYSIS BY MEMBERSHIP TIER
-- Aggregate metrics comparing retention and attrition across tiers
-- =====================================================================
SELECT 
    c.membership_type,
    COUNT(c.customer_id) AS total_members,
    SUM(CASE WHEN cc.churn = 1 THEN 1 ELSE 0 END) AS churned_count,
    SUM(CASE WHEN cc.churn = 0 THEN 1 ELSE 0 END) AS retained_count,
    ROUND(AVG(cc.churn) * 100, 2) AS churn_rate_percentage,
    ROUND(AVG(cc.satisfaction_score), 2) AS avg_satisfaction_score,
    ROUND(AVG(cc.support_tickets), 2) AS avg_support_tickets_raised,
    ROUND(AVG(cc.total_spend), 2) AS avg_total_spend
FROM customers c
INNER JOIN customer_churn cc ON c.customer_id = cc.customer_id
GROUP BY c.membership_type
ORDER BY churn_rate_percentage DESC;


-- =====================================================================
-- 8. ROOT-CAUSE CHURN ANALYSIS: SUPPORT TICKETS & SATISFACTION
-- Grouping by satisfaction rating and support volume
-- =====================================================================
SELECT 
    CASE 
        WHEN cc.satisfaction_score >= 4.0 THEN 'High Satisfaction (4.0 - 5.0)'
        WHEN cc.satisfaction_score >= 3.0 THEN 'Moderate Satisfaction (3.0 - 3.9)'
        ELSE 'Low Satisfaction (< 3.0)'
    END AS satisfaction_group,
    COUNT(cc.customer_id) AS customers_count,
    ROUND(AVG(cc.support_tickets), 2) AS avg_support_tickets,
    ROUND(AVG(cc.days_since_last_purchase), 1) AS avg_days_since_last_order,
    SUM(CASE WHEN cc.churn = 1 THEN 1 ELSE 0 END) AS churned_count,
    ROUND(AVG(cc.churn) * 100, 2) AS churn_rate_percentage
FROM customer_churn cc
GROUP BY satisfaction_group
ORDER BY churn_rate_percentage DESC;


-- =====================================================================
-- 9. PAYMENT METHOD DISTRIBUTION & REVENUE CONTRIBUTION
-- Breakdown of preferred customer checkout channels
-- =====================================================================
SELECT 
    p.payment_method,
    COUNT(p.payment_id) AS total_transactions,
    ROUND(SUM(p.amount), 2) AS total_collected_amount,
    ROUND(AVG(p.amount), 2) AS avg_transaction_value,
    ROUND(SUM(p.amount) * 100.0 / (SELECT SUM(amount) FROM payments WHERE payment_status = 'Completed'), 2) AS revenue_share_percentage
FROM payments p
WHERE p.payment_status = 'Completed'
GROUP BY p.payment_method
ORDER BY total_collected_amount DESC;


-- =====================================================================
-- 10. AT-RISK HIGH VALUE CUSTOMERS (ACTIONABLE ALERT LIST)
-- Filters customers with above-average lifetime value but high inactivity
-- =====================================================================
SELECT 
    c.customer_id,
    c.customer_code,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    c.city,
    cc.total_spend,
    cc.days_since_last_purchase,
    cc.satisfaction_score,
    cc.support_tickets
FROM customers c
INNER JOIN customer_churn cc ON c.customer_id = cc.customer_id
WHERE cc.churn = 1 
  AND cc.total_spend > (SELECT AVG(total_spend) FROM customer_churn)
ORDER BY cc.total_spend DESC
LIMIT 15;
