# 📊 Power BI Dashboard Implementation Guide

## Customer Sales, Revenue & Churn Prediction Analytics System

This guide explains how to connect **Power BI Desktop** to either the **MySQL Database** or the **Exported CSV Files**, set up the relational star schema data model, create DAX measures, and arrange the visualizations into a dashboard.

---

## 1. Connecting Data to Power BI

You can use either of the following methods:

### Method A: Connect Directly via MySQL Database (Recommended if MySQL is running)

1. Open **Power BI Desktop**.
2. Click **Get Data** ➔ **More...** ➔ Select **MySQL database** ➔ Click **Connect**.
3. In the MySQL Server dialog:
   * **Server**: `localhost:3306`
   * **Database**: `customer_churn_db`
   * **Data Connectivity Mode**: `Import`
4. Click **OK**.
5. When prompted for credentials:
   * Select **Database** tab.
   * **User name**: `root` (or your configured username)
   * **Password**: Leave blank (if default) or enter your password.
6. In the **Navigator** window, select all 6 tables:
   * `customers`
   * `products`
   * `orders`
   * `order_items`
   * `payments`
   * `customer_churn`
7. Click **Load**.

---

### Method B: Connect via Exported Cleaned CSV Files (Instant & Offline)

All dimensional and fact tables are automatically exported by `python src/data_cleaning.py` to `data/powerbi_export/`:

1. Open **Power BI Desktop**.
2. Click **Get Data** ➔ **Text/CSV**.
3. Navigate to the project's `data/powerbi_export/` folder and import each file:
   * `dim_customers.csv`
   * `dim_products.csv`
   * `fact_orders.csv`
   * `fact_order_items.csv`
   * `fact_payments.csv`
   * `fact_customer_churn.csv`
4. Click **Load**.

---

## 2. Setting Up the Star Schema Data Model

In Power BI Desktop, click the **Model view** tab (left sidebar) and verify or create the following relationships:

```
                  ┌──────────────────────┐
                  │    dim_customers     │
                  │  (PK: customer_id)   │
                  └──────────┬───────────┘
                             │ 1
                             │
                             │ *
                  ┌──────────▼───────────┐         1 ┌──────────────────────┐
                  │     fact_orders      │───────────│    fact_payments     │
                  │   (PK: order_id)     │           │  (FK: order_id)      │
                  └──────────┬───────────┘           └──────────────────────┘
                             │ 1
                             │
                             │ *
┌──────────────────────┐  *  │
│     dim_products     │─────┼───────────────────┐
│  (PK: product_id)    │     │                   │
└──────────────────────┘     │                   ▼
                             │        ┌──────────────────────┐
                             └───────►│   fact_order_items   │
                                      │   (FK: order_id)     │
                                      │   (FK: product_id)   │
                                      └──────────────────────┘
                                                 │
                                                 │ 1
                                                 ▼
                                      ┌──────────────────────┐
                                      │ fact_customer_churn  │
                                      │  (PK: customer_id)   │
                                      └──────────────────────┘
```

### Table Relationships:
1. `dim_customers[customer_id]` (1) ➔ `fact_orders[customer_id]` (*) [Single direction]
2. `dim_customers[customer_id]` (1) ➔ `fact_customer_churn[customer_id]` (1) [Both directions]
3. `dim_products[product_id]` (1) ➔ `fact_order_items[product_id]` (*) [Single direction]
4. `fact_orders[order_id]` (1) ➔ `fact_order_items[order_id]` (*) [Single direction]
5. `fact_orders[order_id]` (1) ➔ `fact_payments[order_id]` (*) [Single direction]

---

## 3. Creating DAX Measures

1. In the Fields pane, right-click on `fact_orders` or create a new dedicated measures table.
2. Click **New Measure** and copy formulas from [`powerbi/dax_measures.dax`](./dax_measures.dax).

Key measures summary:
* **Total Revenue**: `SUM('fact_orders'[net_amount])`
* **Total Orders**: `DISTINCTCOUNT('fact_orders'[order_id])`
* **Total Customers**: `DISTINCTCOUNT('dim_customers'[customer_id])`
* **Average Order Value (AOV)**: `DIVIDE([Total Revenue], [Total Orders], 0)`
* **Churn Rate %**: `DIVIDE([Churned Customers], [Total Customers], 0) * 100`

---

## 4. Visual Dashboard Layout Wireframe

Design the canvas with a 16:9 aspect ratio and dark or modern slate grey theme:

```
+-----------------------------------------------------------------------------------------------+
|  CUSTOMER SALES, REVENUE & CHURN PREDICTION EXECUTIVE DASHBOARD                               |
+-----------------------------------------------------------------------------------------------+
|  [ Slicers: Date Range  |  City Filter  |  Gender  |  Membership Tier  |  Payment Method ]    |
+---------------+---------------+---------------+-------------------------------+---------------+
|  KPI 1        |  KPI 2        |  KPI 3        |  KPI 4                        |  KPI 5        |
|  Total Rev    |  Total Orders |  Customers    |  Avg Order Value              |  Churn Rate % |
|  $1.42M       |  10,510       |  5,000        |  $135.20                      |  27.4%        |
+---------------+---------------+---------------+-------------------------------+---------------+
|  CHART 1: Monthly Revenue Trend               |  CHART 2: Revenue by Geographic City          |
|  (Line & Clustered Column Chart)              |  (Horizontal Bar Chart)                       |
|  X: Month | Y1: Net Amount | Y2: Orders Count |  Y: City | X: Net Revenue                     |
+-----------------------------------------------+-----------------------------------------------+
|  CHART 3: Revenue by Membership Tier          |  CHART 4: Top 10 Best-Selling Products        |
|  (Donut Chart: Bronze, Silver, Gold, Plat)    |  (Bar Chart: Units Sold & Gross Revenue)      |
+-----------------------------------------------+-----------------------------------------------+
|  CHART 5: Churn by Satisfaction Score         |  CHART 6: Customer Spending vs Inactivity     |
|  (Column Chart: Rating 1.0 to 5.0)            |  (Scatter Plot: Spend vs Days Since Purchase) |
+-----------------------------------------------------------------------------------------------+
```

---

## 5. Adding Interactive Slicers

Place these slicers in the top control header:
1. **Date Range**: `fact_orders[order_date]` (Between slider)
2. **City**: `dim_customers[city]` (Dropdown)
3. **Gender**: `dim_customers[gender]` (Tile / Pill buttons)
4. **Membership Tier**: `dim_customers[membership_type]` (Dropdown)
5. **Payment Method**: `fact_payments[payment_method]` (Dropdown)
