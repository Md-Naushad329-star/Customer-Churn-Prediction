"""
Data Cleaning & Preparation Module
Performs data verification, duplicate removal, missing value handling,
type normalization, and table joining for downstream ML and Power BI analytics.
"""

from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
POWERBI_DIR = BASE_DIR / "data" / "powerbi_export"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
POWERBI_DIR.mkdir(parents=True, exist_ok=True)


def clean_and_prepare_data():
    """
    Cleans raw CSV data and outputs analytical datasets.
    """
    print("[*] Starting data cleaning and preprocessing pipeline...")

    # Load raw files
    df_customers = pd.read_csv(RAW_DIR / "customers_raw.csv")
    df_products = pd.read_csv(RAW_DIR / "products_raw.csv")
    df_orders = pd.read_csv(RAW_DIR / "orders_raw.csv")
    df_order_items = pd.read_csv(RAW_DIR / "order_items_raw.csv")
    df_payments = pd.read_csv(RAW_DIR / "payments_raw.csv")
    df_churn = pd.read_csv(RAW_DIR / "customer_churn_raw.csv")

    print(f"[+] Loaded raw datasets: {len(df_customers)} customers, {len(df_orders)} orders.")

    # 1. Deduplication Check
    for name, df, pk in [
        ("Customers", df_customers, "customer_id"),
        ("Products", df_products, "product_id"),
        ("Orders", df_orders, "order_id"),
        ("Order Items", df_order_items, "order_item_id"),
        ("Payments", df_payments, "payment_id"),
        ("Churn", df_churn, "customer_id"),
    ]:
        init_len = len(df)
        df.drop_duplicates(subset=[pk], inplace=True)
        if len(df) < init_len:
            print(f"[-] Removed {init_len - len(df)} duplicates from {name}.")

    # 2. Date Formatting & Parsing
    df_customers["signup_date"] = pd.to_datetime(df_customers["signup_date"])
    df_orders["order_date"] = pd.to_datetime(df_orders["order_date"])
    df_payments["payment_date"] = pd.to_datetime(df_payments["payment_date"])

    # 3. Numeric Types and Outlier Truncation
    df_churn["satisfaction_score"] = df_churn["satisfaction_score"].clip(1.0, 5.0)
    df_churn["support_tickets"] = df_churn["support_tickets"].clip(lower=0)
    df_churn["days_since_last_purchase"] = df_churn["days_since_last_purchase"].clip(lower=0)

    # 4. Merge Customer Demographic Data with Behavioral Telemetry
    # This forms the single master dataset for ML Churn Modelling & EDA
    df_master = pd.merge(
        df_customers,
        df_churn[[
            "customer_id", "total_orders", "total_spend", "average_order_value",
            "days_since_last_purchase", "purchase_frequency", "support_tickets",
            "satisfaction_score", "membership_duration_months", "churn"
        ]],
        on="customer_id",
        how="inner"
    )

    # Derived Segmentations for Analytics
    df_master["age_group"] = pd.cut(
        df_master["age"],
        bins=[17, 25, 35, 50, 100],
        labels=["18-25", "26-35", "36-50", "51+"]
    )

    df_master["spending_bracket"] = pd.cut(
        df_master["total_spend"],
        bins=[-1, 100, 300, 600, 10000],
        labels=["Low (<$100)", "Medium ($100-$300)", "High ($300-$600)", "VIP ($600+)"]
    )

    # 5. Order Enriched Dataset (Joining Customer, Order, Order Items, Product)
    df_items_prod = pd.merge(
        df_order_items,
        df_products[["product_id", "product_name", "category", "cost_price"]],
        on="product_id",
        how="left"
    )
    df_items_prod["cost_total"] = df_items_prod["cost_price"] * df_items_prod["quantity"]
    df_items_prod["gross_profit"] = df_items_prod["item_total"] - df_items_prod["cost_total"]

    df_sales_enriched = pd.merge(
        df_orders,
        df_customers[["customer_id", "city", "gender", "membership_type"]],
        on="customer_id",
        how="left"
    )

    # 6. Save Processed Datasets
    master_path = PROCESSED_DIR / "customer_churn_cleaned.csv"
    df_master.to_csv(master_path, index=False)
    print(f"[+] Master Churn dataset saved to {master_path} ({len(df_master)} rows)")

    sales_enriched_path = PROCESSED_DIR / "sales_summary.csv"
    df_sales_enriched.to_csv(sales_enriched_path, index=False)
    print(f"[+] Sales summary saved to {sales_enriched_path} ({len(df_sales_enriched)} rows)")

    # 7. Export Power BI-ready CSV files
    df_customers.to_csv(POWERBI_DIR / "dim_customers.csv", index=False)
    df_products.to_csv(POWERBI_DIR / "dim_products.csv", index=False)
    df_orders.to_csv(POWERBI_DIR / "fact_orders.csv", index=False)
    df_items_prod.to_csv(POWERBI_DIR / "fact_order_items.csv", index=False)
    df_payments.to_csv(POWERBI_DIR / "fact_payments.csv", index=False)
    df_master.to_csv(POWERBI_DIR / "fact_customer_churn.csv", index=False)
    print(f"[SUCCESS] All Power BI dimension and fact tables exported to {POWERBI_DIR}")

    return df_master, df_sales_enriched


if __name__ == "__main__":
    clean_and_prepare_data()
