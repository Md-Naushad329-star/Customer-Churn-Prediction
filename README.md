# 📊 Customer Sales, Revenue & Churn Prediction Analytics System

> **A Complete, End-to-End Enterprise Data Science, Machine Learning & Business Intelligence Project**  
> *Developed for local execution on Windows / VS Code / Jupyter / Google Colab / Streamlit & Power BI.*

---

## 1. Project Overview

Customer attrition (churn) directly reduces customer lifetime value and recurring business revenue. Acquiring new customers typically costs **5x to 7x more** than retaining existing ones. 

This project provides an end-to-end data analytics and predictive intelligence solution that:
1. Simulates an enterprise e-commerce / retail transactional ecosystem with **5,000+ customers** and **10,000+ order records**.
2. Organizes transactional telemetry into a normalized relational database schema (**MySQL 8.0**).
3. Executes analytical SQL queries to extract KPIs: Customer Lifetime Value (CLV), Average Order Value (AOV), Repeat Purchase Rate, and cohort churn rates.
4. Performs rigorous data cleaning and **Exploratory Data Analysis (EDA)** using **Pandas, Matplotlib, and Seaborn**.
5. Trains, evaluates, and compares multiple supervised classification models (**Logistic Regression, Decision Tree, Random Forest**) using **Scikit-learn**, auto-selecting the best model.
6. Deploys an interactive **Streamlit web application** for real-time customer churn prediction, risk analysis, and exploratory BI.
7. Prepares star-schema dimensional datasets and DAX measures for an interactive **Power BI Executive Dashboard**.

---

## 2. Key Features

- **Relational MySQL Database Architecture**: 6 fully normalized tables with primary/foreign keys, indexing, and cascade rules.
- **Advanced SQL Analytical Query Suite**: CTEs, Window functions (`LAG`), aggregation, and RFM-style segmentation queries.
- **Enterprise Synthetic Data Generator**: Realistic distributions capturing non-linear churn triggers (inactivity, low satisfaction, support backlogs).
- **Automated Data Quality & Preprocessing**: Type casting, handling missing values, standard scaling, and one-hot encoding pipelines.
- **Publication-Ready EDA Visualizations**: 12 custom Matplotlib & Seaborn figures saved in high-res format.
- **Multi-Model Machine Learning Benchmark**: Logistic Regression, Decision Tree, and Random Forest evaluated on Accuracy, Precision, Recall, F1, and ROC-AUC.
- **Champion Model Serialization**: Automated model champion selection and Joblib persistence.
- **Interactive Streamlit Web Dashboard**: 7 comprehensive pages with custom CSS metric cards and real-time prediction inputs.
- **Power BI Dimensional Export**: Ready-to-import CSVs (`dim_*`, `fact_*`) and a complete DAX measures reference.

---

## 3. Technologies Used

| Technology | Domain | Purpose |
| :--- | :--- | :--- |
| **Python 3.10+ / 3.13** | Core Programming | Data pipeline, statistical modeling, application logic |
| **SQL / MySQL 8.0** | Relational Database | Data storage, transactional consistency, analytical queries |
| **Pandas & NumPy** | Data Processing | Dataframes manipulation, vectorization, cleaning |
| **Scikit-Learn** | Machine Learning | Preprocessing pipelines, model training, metric evaluation |
| **Matplotlib & Seaborn** | Data Visualization | Publication-grade statistical plots and correlation charts |
| **Streamlit** | Web Application | Interactive analytical dashboards and live ML scoring tool |
| **Power BI Desktop** | Business Intelligence | Interactive multi-dimensional executive dashboard |
| **Joblib** | ML Serialization | Saving and loading trained machine learning pipelines |
| **SQLAlchemy** | ORM / DB Engine | Robust, safe Python-to-MySQL database connectivity |
| **Python-Dotenv** | Configuration | Environment variable and database credential management |

---

## 4. Project Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA PIPELINE ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────────────────────┘

 [1. Data Generation]
   python src/data_generation.py
          │
          ├──► Raw Data Exports (data/raw/*.csv)
          │
          └──► MySQL Database (customer_churn_db) ──► Analytical SQL Queries
                         │
                         ▼
 [2. Data Cleaning & Dimensional Modeling]
   python src/data_cleaning.py
          │
          ├──► Cleaned Master Dataset (data/processed/customer_churn_cleaned.csv)
          └──► Power BI Star Schema Tables (data/powerbi_export/*.csv)
                         │
                         ▼
 [3. Exploratory Data Analysis (EDA)]
   python src/eda.py ──► 12 High-Res Plots (outputs/charts/*.png)
                         │
                         ▼
 [4. Machine Learning Pipeline]
   python src/train_model.py
          ├── Feature Engineering (ColumnTransformer: StandardScaler + OneHotEncoder)
          ├── Model Training (Logistic Regression, Decision Tree, Random Forest)
          ├── Evaluation & Comparison (Accuracy, Precision, Recall, F1, ROC-AUC)
          └── Best Model Serialized (models/best_model.pkl)
                         │
                         ▼
 [5. Production Deployment & Consumption]
          ├── Streamlit Web App (app/app.py) ──► Live Real-time Churn Predictor
          └── Power BI Dashboard (powerbi/README.md) ──► Executive Business Intelligence
```

---

## 5. Folder Structure

```
customer-sales-churn-project/
│
├── data/
│   ├── raw/                      # Raw simulated CSV files (customers, orders, products, etc.)
│   ├── processed/                # Cleaned master dataset & sales summary
│   └── powerbi_export/           # Star-schema dimension and fact tables for Power BI
│
├── database/
│   ├── schema.sql                # MySQL DDL table creation and foreign key constraints
│   ├── insert_data.sql           # SQL seed script with initial records
│   └── analysis_queries.sql      # 10 comprehensive business intelligence SQL queries
│
├── notebooks/
│   ├── 01_data_generation.ipynb  # Step-by-step data synthesis walkthrough
│   ├── 02_data_cleaning.ipynb    # Data quality auditing and feature creation
│   ├── 03_eda.ipynb              # Visual analysis and statistical breakdown
│   └── 04_machine_learning.ipynb # ML pipeline training, evaluation & tuning
│
├── src/
│   ├── __init__.py               # Package marker
│   ├── database.py               # MySQL connection pooling & query executor
│   ├── data_generation.py        # Synthetic dataset generator
│   ├── data_cleaning.py          # Data validation & cleaning script
│   ├── eda.py                    # Visual exploratory data analysis script
│   ├── feature_engineering.py    # Sklearn ColumnTransformer & preprocessor
│   ├── train_model.py            # Model training & champion auto-selector
│   └── predict.py                # Single & batch prediction inference service
│
├── models/
│   └── best_model.pkl            # Trained scikit-learn champion pipeline
│
├── outputs/
│   ├── charts/                   # 12 high-resolution generated PNG charts
│   ├── reports/                  # JSON & CSV model evaluations & EDA summary
│   └── predictions/              # Batch inference prediction output CSVs
│
├── app/
│   └── app.py                    # 7-page Streamlit web analytics platform
│
├── powerbi/
│   ├── README.md                 # Power BI connection & setup tutorial
│   └── dax_measures.dax          # Ready-to-use DAX measures reference
│
├── requirements.txt              # Complete Python dependency list
├── .env.example                  # Environment configuration template
├── .gitignore                    # Git tracking rules
└── README.md                     # Comprehensive project documentation
```

---

## 6. Dataset Description

The generated dataset mirrors realistic business logic across 6 relational entities:

### 1. `customers` (5,000 records)
* `customer_id`: Unique surrogate integer primary key.
* `customer_code`: Business code (e.g. `CUST-1001`).
* `first_name`, `last_name`, `email`: Contact details.
* `age`: Normal distribution centered at 36 years (range 18–75).
* `gender`: `Male` (50%), `Female` (48%), `Other` (2%).
* `city`: 10 major metropolitan hubs (Mumbai, Bengaluru, Delhi, etc.).
* `signup_date`: Dates spanning 2022 to 2023.
* `membership_type`: `Bronze`, `Silver`, `Gold`, `Platinum`.

### 2. `products` (25 records)
* `product_id`, `product_code`, `product_name`.
* `category`: `Electronics`, `Fashion & Apparel`, `Home & Kitchen`, `Beauty & Health`, `Sports & Fitness`.
* `unit_price`, `cost_price`: Margins and unit costs.
* `stock_quantity`: Catalog stock levels.

### 3. `orders` (10,510 records)
* `order_id`, `order_code`, `customer_id`, `order_date`.
* `order_status`: `Delivered`, `Shipped`, `Processing`, `Cancelled`.
* `gross_amount`, `discount_amount`, `net_amount`.

### 4. `order_items` (17,411 records)
* `order_item_id`, `order_id`, `product_id`, `quantity`, `unit_price`, `discount_rate`, `item_total`.

### 5. `payments` (10,510 records)
* `payment_id`, `order_id`, `payment_date`, `payment_method` (UPI, Credit Card, Debit Card, etc.), `payment_status`, `amount`.

### 6. `customer_churn` (5,000 records)
* `total_orders`, `total_spend`, `average_order_value`.
* `days_since_last_purchase`: Customer recency in days.
* `purchase_frequency`: Annualized purchase rate.
* `support_tickets`: Unresolved tickets (0 to 5+).
* `satisfaction_score`: Rating on 1.0 to 5.0 scale.
* `membership_duration_months`: Account tenure.
* `churn`: Target binary indicator (**1 = Churned, 0 = Retained**).

---

## 7. MySQL Setup

If you have MySQL installed (via **Laragon**, **XAMPP**, or **MySQL Workbench**):

1. Ensure the MySQL service is running on `localhost:3306`.
2. Configure credentials in your `.env` file:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=
   DB_NAME=customer_churn_db
   ```
3. Initialize the schema and seed sample data:
   * **Via MySQL CLI**:
     ```bash
     mysql -u root -p < database/schema.sql
     mysql -u root -p < database/insert_data.sql
     ```
   * **Or via Python automated seeder**:
     ```bash
     python src/data_generation.py
     ```
> **Note**: If MySQL is not running on your machine, the entire system **gracefully switches to local processed CSV mode**, ensuring all EDA, ML modeling, and Streamlit dashboards function without error.

---

## 8. Python Environment Setup

### Prerequisites
* Python 3.10, 3.11, 3.12, or 3.13 installed.
* PowerShell or Command Prompt on Windows.

### Virtual Environment Creation
```powershell
# Navigate to the project root directory
cd customer-sales-churn-project

# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment on Windows
venv\Scripts\activate
```

---

## 9. Installation Commands

Install all required dependencies using `pip`:
```powershell
pip install -r requirements.txt
```

Verify that key packages are available:
```powershell
python -c "import pandas, sklearn, streamlit, matplotlib, seaborn; print('All core libraries verified!')"
```

---

## 10. How to Generate Dataset

Run the automated data generator script:
```powershell
python src/data_generation.py
```
This script creates:
* 5,000 Customers, 25 Products, ~10,500 Orders, ~17,400 Line Items, and Churn profiles.
* Saves all files to `data/raw/*.csv`.

Next, clean and enrich the data:
```powershell
python src/data_cleaning.py
```
This generates:
* `data/processed/customer_churn_cleaned.csv`
* `data/processed/sales_summary.csv`
* `data/powerbi_export/*.csv`

---

## 11. How to Run EDA

Generate all 12 statistical charts and the JSON summary report:
```powershell
python src/eda.py
```
Outputs created:
* `outputs/charts/01_customer_age_distribution.png`
* `outputs/charts/02_revenue_distribution.png`
* `outputs/charts/03_monthly_sales_trend.png`
* `outputs/charts/04_sales_by_city.png`
* `outputs/charts/05_sales_by_membership.png`
* `outputs/charts/06_top_products.png`
* `outputs/charts/07_churn_distribution.png`
* `outputs/charts/08_correlation_heatmap.png`
* `outputs/charts/09_churn_vs_purchase_frequency.png`
* `outputs/charts/10_churn_vs_satisfaction_score.png`
* `outputs/charts/11_churn_vs_total_spending.png`
* `outputs/charts/12_churn_drivers_multivariate.png`
* `outputs/reports/eda_summary.json`

---

## 12. How to Train the ML Models

Train Logistic Regression, Decision Tree, and Random Forest:
```powershell
python src/train_model.py
```
The script evaluates all models on the stratified test set, creates a comparison table, automatically selects the best-performing model, and saves:
* Champion model: `models/best_model.pkl`
* Confusion matrix plot: `outputs/charts/model_confusion_matrix.png`
* Feature importance plot: `outputs/charts/model_feature_importance.png`
* Evaluation report: `outputs/reports/model_evaluation.json`

Test a prediction from the command line:
```powershell
python src/predict.py
```

---

## 13. How to Run the Streamlit Web Application

Launch the Streamlit interactive dashboard:
```powershell
streamlit run app/app.py
```
Open your browser at `http://localhost:8501`.

### App Pages Included:
1. **Home**: Executive high-level KPIs, pipeline architecture diagram, and project overview.
2. **Data Overview**: Filterable data tables, customer tiers, and statistical summaries.
3. **Sales Analytics**: Monthly revenue trends, city rankings, and membership spending.
4. **Customer Analytics**: Behavioral telemetry, satisfaction ratings, and inactivity scatter charts.
5. **EDA Visualizations**: Interactive gallery viewer for all 12 generated Seaborn/Matplotlib charts.
6. **Machine Learning Model**: Model comparison metrics table, confusion matrices, and feature importance.
7. **Customer Churn Prediction**: Real-time interactive calculator with probability bar, risk category badge, and retention tips.

---

## 14. How to Connect Power BI

Refer to the dedicated guide at [`powerbi/README.md`](powerbi/README.md).

### Quick Steps:
1. Open **Power BI Desktop**.
2. Select **Get Data** ➔ **Text/CSV**.
3. Import the 6 CSV files from `data/powerbi_export/`:
   - `dim_customers.csv`
   - `dim_products.csv`
   - `fact_orders.csv`
   - `fact_order_items.csv`
   - `fact_payments.csv`
   - `fact_customer_churn.csv`
4. Confirm relationships in **Model view** (1-to-many from dimension to fact tables).
5. Add the DAX measures provided in [`powerbi/dax_measures.dax`](powerbi/dax_measures.dax).
6. Build your KPI cards and charts as demonstrated in the layout guide.

---

## 15. Example SQL Queries

Key queries from [`database/analysis_queries.sql`](database/analysis_queries.sql):

### Monthly Revenue & MoM Growth using Window Function (`LAG`):
```sql
WITH MonthlySales AS (
    SELECT 
        DATE_FORMAT(o.order_date, '%Y-%m') AS sales_month,
        COUNT(o.order_id) AS orders_count,
        ROUND(SUM(o.net_amount), 2) AS monthly_revenue
    FROM orders o
    WHERE o.order_status IN ('Delivered', 'Shipped')
    GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
)
SELECT 
    sales_month,
    orders_count,
    monthly_revenue,
    LAG(monthly_revenue, 1) OVER (ORDER BY sales_month) AS prev_revenue,
    ROUND(((monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY sales_month)) / 
          LAG(monthly_revenue, 1) OVER (ORDER BY sales_month)) * 100, 2) AS mom_growth_pct
FROM MonthlySales;
```

### Customer RFM Segmentation via `CASE WHEN`:
```sql
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.membership_type,
    cc.total_spend,
    cc.days_since_last_purchase,
    CASE 
        WHEN cc.total_spend >= 500 AND cc.days_since_last_purchase <= 45 THEN 'VIP Champion'
        WHEN cc.total_spend >= 300 AND cc.days_since_last_purchase <= 90 THEN 'High Value Active'
        WHEN cc.total_spend >= 300 AND cc.days_since_last_purchase > 90 THEN 'High Value At Risk'
        ELSE 'Low Engagement / Churn Candidate'
    END AS customer_segment
FROM customers c
INNER JOIN customer_churn cc ON c.customer_id = cc.customer_id
ORDER BY cc.total_spend DESC;
```

---

## 16. Machine Learning Model Results

Evaluating the models on a **stratified hold-out test set** (1,000 customers) yielded the following benchmarks:

| Model Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | **97.40%** | **96.66%** | **98.20%** | **0.9743** | **0.9975** | 🏆 **Champion Selected** |
| **Decision Tree** | 95.60% | 96.54% | 94.61% | 0.9556 | 0.9869 | Candidate |
| **Random Forest** | 95.00% | 95.37% | 94.61% | 0.9499 | 0.9922 | Candidate |

### Top Predictive Features for Churn:
1. `days_since_last_purchase` (Recency / Inactivity)
2. `satisfaction_score` (Customer rating)
3. `support_tickets` (Unresolved issues)
4. `total_spend` & `total_orders` (Lifetime engagement)
5. `membership_type_Bronze` (Lower commitment tier)

---

## 17. Screenshots & Visual Demonstrations

### Streamlit Application Preview:
* **Interactive Prediction Engine**: Live sliders, calculated AOV, and instant probability gauge.
* **Model Benchmark Gallery**: Metric tables and confusion matrix heatmaps.
* **EDA Visual Explorer**: 12 custom charts with data science takeaways.

*(Place your exported screenshots here: `outputs/reports/app_home.png`, `outputs/reports/app_prediction.png`)*

---

## 18. Viva & Placement Interview Preparation (B.Tech CSE / Data Science)

### Q1: Why did you use Logistic Regression over complex ensembles if Random Forest is usually stronger?
> **Answer**: In our feature space, the churn boundary is driven by strong continuous signals (recency, satisfaction rating, support tickets). Logistic Regression with scaled features produced an F1-score of 97.43% and ROC-AUC of 0.9975 without overfitting, while offering high interpretability through log-odds coefficients and fast real-time inference.

### Q2: How did you handle data leakage during preprocessing?
> **Answer**: We split the dataset into training (80%) and testing (20%) sets using `stratify=y` *before* fitting the `StandardScaler` and `OneHotEncoder`. The preprocessor was bundled into a Scikit-Learn `Pipeline`, ensuring transformation parameters were learned strictly on training folds and only applied to the test fold.

### Q3: Why is F1-Score prioritized over Accuracy for Churn Prediction?
> **Answer**: Customer churn datasets are often class-imbalanced. A naive model predicting "Retained" for all customers can achieve high accuracy while failing to identify churners. F1-score balances Precision (minimizing false alarms) and Recall (catching all true churners), which directly aligns with business retention costs.

### Q4: How is Power BI connected and structured?
> **Answer**: Power BI connects to the relational model via a Star Schema. Fact tables (`fact_orders`, `fact_order_items`, `fact_customer_churn`) contain measurable business events, linked to Dimension tables (`dim_customers`, `dim_products`) via 1-to-many relationships. DAX measures compute dynamic aggregates like MoM growth and Churn Rate.

---

## 19. Future Improvements

* **Hyperparameter Tuning**: Integrate `GridSearchCV` or `Optuna` for automated tree depth and regularization tuning.
* **Explainable AI (XAI)**: Incorporate SHAP (SHapley Additive exPlanations) values in the Streamlit UI to display individual feature contribution force plots for each customer.
* **Real-time Webhook Integration**: Trigger automatic email incentives via SendGrid/Twilio API when a customer is flagged as "High Risk".
* **Docker Containerization**: Add a `Dockerfile` and `docker-compose.yml` to package Python, MySQL, and Streamlit into single-command deployments.

---

## 20. Author & License

* **Project**: Customer Sales, Revenue & Churn Prediction Analytics System
* **Domain**: Data Science / Machine Learning / Business Intelligence
* **License**: MIT Open Source
