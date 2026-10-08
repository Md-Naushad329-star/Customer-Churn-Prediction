"""
Data Generation Module
Generates a realistic synthetic enterprise dataset for:
- Customers (5,000 records)
- Products (25 catalog items)
- Orders (12,500 transactions)
- Order Items (25,000 line items)
- Payments (12,500 payments)
- Customer Churn Analytics Snapshot (5,000 enriched records)
"""

import os
import random
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Define Directories
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Set random seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)


def generate_synthetic_data(num_customers=5000):
    """
    Generates all relational tables and churn feature tables with realistic distributions.
    """
    print(f"[*] Generating synthetic dataset for {num_customers} customers...")

    first_names_male = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Reyansh", "Muhammad", "Sai", "Ayaan", "Krishna",
                        "Ishaan", "Shaurya", "Atharv", "Dhruv", "Kabir", "Rohan", "Vikram", "Rahul", "Kunal", "Amit"]
    first_names_female = ["Saanvi", "Aanya", "Aadhya", "Aarohi", "Ananya", "Pari", "Anika", "Navya", "Angel", "Diya",
                          "Myra", "Sara", "Ira", "Kavya", "Sneha", "Pooja", "Priya", "Neha", "Rhea", "Tanvi"]
    last_names = ["Sharma", "Verma", "Patel", "Mehta", "Singh", "Nair", "Reddy", "Iyer", "Gupta", "Joshi",
                  "Chopra", "Malhotra", "Bhat", "Rao", "Kulkarni", "Das", "Mukherjee", "Chatterjee", "Menon", "Kapoor"]

    cities = ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Kochi"]
    membership_tiers = ["Bronze", "Silver", "Gold", "Platinum"]
    membership_weights = [0.45, 0.30, 0.18, 0.07]

    # -------------------------------------------------------------
    # 1. Customers Table
    # -------------------------------------------------------------
    customer_records = []
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 12, 31)
    date_range_days = (end_date - start_date).days

    for i in range(1, num_customers + 1):
        gender = np.random.choice(["Male", "Female", "Other"], p=[0.50, 0.48, 0.02])
        if gender == "Male":
            first_name = random.choice(first_names_male)
        elif gender == "Female":
            first_name = random.choice(first_names_female)
        else:
            first_name = random.choice(first_names_male + first_names_female)

        last_name = random.choice(last_names)
        age = int(np.random.normal(36, 11))
        age = max(18, min(75, age))

        city = random.choice(cities)
        membership = np.random.choice(membership_tiers, p=membership_weights)
        signup_dt = start_date + timedelta(days=random.randint(0, date_range_days))
        email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"

        customer_records.append({
            "customer_id": i,
            "customer_code": f"CUST-{1000 + i}",
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "age": age,
            "gender": gender,
            "city": city,
            "signup_date": signup_dt.strftime("%Y-%m-%d"),
            "membership_type": membership
        })

    df_customers = pd.DataFrame(customer_records)
    print(f"[+] Created customers table: {len(df_customers)} records")

    # -------------------------------------------------------------
    # 2. Products Table
    # -------------------------------------------------------------
    products_catalog = [
        # Electronics
        ("Noise Cancelling Wireless Headphones", "Electronics", 149.99, 85.00),
        ("Ultra HD 4K Smart Monitor 27-inch", "Electronics", 329.99, 210.00),
        ("Wireless Mechanical Gaming Keyboard", "Electronics", 89.99, 45.00),
        ("Precision Optical Ergonomic Mouse", "Electronics", 49.99, 22.00),
        ("Fast Wireless Charging Pad 15W", "Electronics", 29.99, 12.00),
        # Fashion & Apparel
        ("Slim-Fit Organic Cotton Denim Jacket", "Fashion & Apparel", 79.99, 34.00),
        ("Breathable Performance Running Shoes", "Fashion & Apparel", 99.50, 46.00),
        ("Classic Premium Merino Wool Sweater", "Fashion & Apparel", 69.99, 28.00),
        ("Water-Resistant All-Weather Windbreaker", "Fashion & Apparel", 84.99, 36.00),
        ("Vintage Leather Everyday Messenger Bag", "Fashion & Apparel", 119.00, 52.00),
        # Home & Kitchen
        ("Programmable Smart Air Fryer 5.8L", "Home & Kitchen", 119.00, 62.00),
        ("Stainless Steel Thermal Coffee Carafe", "Home & Kitchen", 34.99, 14.50),
        ("Cast Iron Pre-Seasoned Dutch Oven 6-Qt", "Home & Kitchen", 74.99, 31.00),
        ("High-Speed Blender & Smoothie Maker", "Home & Kitchen", 89.99, 41.00),
        ("Aroma Essential Oil Ultrasonic Diffuser", "Home & Kitchen", 29.99, 11.50),
        # Beauty & Health
        ("Anti-Aging Vitamin C Facial Serum", "Beauty & Health", 29.95, 9.50),
        ("Sonic Electric Rechargeable Toothbrush", "Beauty & Health", 49.99, 19.00),
        ("Deep Hydration Hyaluronic Moisturizer", "Beauty & Health", 24.99, 8.00),
        ("Organic Herbal Revitalizing Hair Oil", "Beauty & Health", 19.99, 6.50),
        ("Natural Clay Purifying Face Mask 100g", "Beauty & Health", 18.50, 5.50),
        # Sports & Fitness
        ("High-Density Non-Slip Yoga Mat", "Sports & Fitness", 39.99, 15.00),
        ("Adjustable Quick-Select Dumbbell Pair", "Sports & Fitness", 199.99, 110.00),
        ("Smart Fitness Tracker with Heart Monitor", "Sports & Fitness", 69.99, 32.00),
        ("Insulated Stainless Sports Water Bottle", "Sports & Fitness", 24.99, 8.50),
        ("Heavy Duty Resistance Exercise Loop Bands", "Sports & Fitness", 19.99, 6.00),
    ]

    product_records = []
    for idx, (p_name, category, u_price, c_price) in enumerate(products_catalog, start=1):
        product_records.append({
            "product_id": idx,
            "product_code": f"PROD-{idx:04d}",
            "product_name": p_name,
            "category": category,
            "unit_price": u_price,
            "cost_price": c_price,
            "stock_quantity": random.randint(50, 400)
        })

    df_products = pd.DataFrame(product_records)
    print(f"[+] Created products catalog: {len(df_products)} records")

    # -------------------------------------------------------------
    # 3. Orders and Order Items Tables
    # -------------------------------------------------------------
    order_records = []
    order_item_records = []
    payment_records = []

    order_counter = 1
    item_counter = 1
    payment_counter = 1

    sim_start = datetime(2023, 1, 1)
    sim_end = datetime(2024, 6, 30)
    sim_span_days = (sim_end - sim_start).days

    payment_methods = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash on Delivery"]
    payment_weights = [0.42, 0.28, 0.15, 0.08, 0.07]

    # Pre-determine customer order counts based on membership tier
    customer_order_counts = {}
    for _, c_row in df_customers.iterrows():
        cid = c_row["customer_id"]
        tier = c_row["membership_type"]
        if tier == "Platinum":
            n_orders = np.random.choice([2, 3, 4, 5, 6, 7, 8], p=[0.05, 0.15, 0.25, 0.25, 0.15, 0.10, 0.05])
        elif tier == "Gold":
            n_orders = np.random.choice([1, 2, 3, 4, 5, 6], p=[0.10, 0.25, 0.30, 0.20, 0.10, 0.05])
        elif tier == "Silver":
            n_orders = np.random.choice([1, 2, 3, 4], p=[0.30, 0.40, 0.20, 0.10])
        else: # Bronze
            n_orders = np.random.choice([0, 1, 2, 3], p=[0.20, 0.50, 0.20, 0.10])
        customer_order_counts[cid] = n_orders

    for cid, n_orders in customer_order_counts.items():
        if n_orders == 0:
            continue

        c_signup = datetime.strptime(df_customers.loc[df_customers["customer_id"] == cid, "signup_date"].values[0], "%Y-%m-%d")

        for _ in range(n_orders):
            # Order date between signup and end date
            if c_signup >= sim_end:
                order_dt = sim_end
            else:
                max_days = max(1, (sim_end - c_signup).days)
                order_dt = c_signup + timedelta(days=random.randint(0, max_days))

            num_items = np.random.choice([1, 2, 3, 4], p=[0.55, 0.30, 0.10, 0.05])
            order_gross = 0.0
            order_discount = 0.0

            order_id = order_counter
            order_counter += 1

            for _ in range(num_items):
                p_item = random.choice(product_records)
                p_id = p_item["product_id"]
                p_price = p_item["unit_price"]
                qty = np.random.choice([1, 2, 3], p=[0.80, 0.15, 0.05])
                disc_rate = np.random.choice([0.0, 0.05, 0.10, 0.15], p=[0.50, 0.25, 0.15, 0.10])

                line_gross = p_price * qty
                line_disc = line_gross * disc_rate
                line_total = line_gross - line_disc

                order_gross += line_gross
                order_discount += line_disc

                order_item_records.append({
                    "order_item_id": item_counter,
                    "order_id": order_id,
                    "product_id": p_id,
                    "quantity": int(qty),
                    "unit_price": round(float(p_price), 2),
                    "discount_rate": round(float(disc_rate), 2),
                    "item_total": round(float(line_total), 2)
                })
                item_counter += 1

            net_amt = round(order_gross - order_discount, 2)
            order_status = np.random.choice(
                ["Delivered", "Shipped", "Processing", "Cancelled"],
                p=[0.88, 0.06, 0.04, 0.02]
            )

            order_records.append({
                "order_id": order_id,
                "order_code": f"ORD-{20240000 + order_id}",
                "customer_id": cid,
                "order_date": order_dt.strftime("%Y-%m-%d"),
                "order_status": order_status,
                "gross_amount": round(order_gross, 2),
                "discount_amount": round(order_discount, 2),
                "net_amount": net_amt
            })

            # Payment record
            pmt_method = np.random.choice(payment_methods, p=payment_weights)
            pmt_status = "Completed" if order_status in ["Delivered", "Shipped", "Processing"] else "Refunded"

            payment_records.append({
                "payment_id": payment_counter,
                "order_id": order_id,
                "payment_date": order_dt.strftime("%Y-%m-%d"),
                "payment_method": pmt_method,
                "payment_status": pmt_status,
                "amount": net_amt
            })
            payment_counter += 1

    df_orders = pd.DataFrame(order_records)
    df_order_items = pd.DataFrame(order_item_records)
    df_payments = pd.DataFrame(payment_records)

    print(f"[+] Created orders table: {len(df_orders)} records")
    print(f"[+] Created order items: {len(df_order_items)} records")
    print(f"[+] Created payments table: {len(df_payments)} records")

    # -------------------------------------------------------------
    # 4. Customer Churn Analytical Snapshot (Customer Behavior)
    # -------------------------------------------------------------
    today = sim_end
    churn_records = []

    # Map aggregate spending from orders
    if len(df_orders) > 0:
        valid_orders = df_orders[df_orders["order_status"].isin(["Delivered", "Shipped"])]
        spend_map = valid_orders.groupby("customer_id")["net_amount"].sum().to_dict()
        order_count_map = valid_orders.groupby("customer_id")["order_id"].count().to_dict()
        latest_order_map = valid_orders.groupby("customer_id")["order_date"].max().to_dict()
    else:
        spend_map = {}
        order_count_map = {}
        latest_order_map = {}

    for _, c_row in df_customers.iterrows():
        cid = c_row["customer_id"]
        tier = c_row["membership_type"]
        age = c_row["age"]
        signup_dt = datetime.strptime(c_row["signup_date"], "%Y-%m-%d")
        membership_duration_months = max(1, int((today - signup_dt).days / 30.4))

        tot_orders = order_count_map.get(cid, 0)
        tot_spend = spend_map.get(cid, 0.0)
        aov = round(tot_spend / tot_orders, 2) if tot_orders > 0 else 0.0

        if cid in latest_order_map:
            last_date = datetime.strptime(latest_order_map[cid], "%Y-%m-%d")
            days_since_last_purchase = max(0, (today - last_date).days)
        else:
            days_since_last_purchase = min(365, (today - signup_dt).days)

        purchase_freq = round(tot_orders / (membership_duration_months / 12.0), 3) if membership_duration_months > 0 else 0.0

        # Behavioral drivers based on experience & tier
        if tier in ["Platinum", "Gold"]:
            support_tickets = np.random.choice([0, 1, 2, 3], p=[0.60, 0.28, 0.09, 0.03])
            satisfaction_score = round(float(np.random.normal(4.2, 0.5)), 1)
        else:
            support_tickets = np.random.choice([0, 1, 2, 3, 4, 5], p=[0.35, 0.30, 0.18, 0.10, 0.05, 0.02])
            satisfaction_score = round(float(np.random.normal(3.4, 0.8)), 1)

        satisfaction_score = max(1.0, min(5.0, satisfaction_score))

        # Realistic Churn Logit Function
        # Factors increasing churn: high days since purchase, low satisfaction, high support tickets, low orders
        logit = (
            -0.8
            + 0.028 * days_since_last_purchase
            + 0.72 * support_tickets
            - 1.15 * satisfaction_score
            - 0.18 * tot_orders
            - 0.0015 * tot_spend
            + (0.4 if tier == "Bronze" else -0.5 if tier == "Platinum" else 0.0)
            + np.random.normal(0, 0.45)
        )

        churn_prob = 1.0 / (1.0 + np.exp(-logit))
        churn_flag = 1 if churn_prob >= 0.50 else 0

        churn_records.append({
            "churn_id": cid,
            "customer_id": cid,
            "total_orders": tot_orders,
            "total_spend": round(tot_spend, 2),
            "average_order_value": aov,
            "days_since_last_purchase": days_since_last_purchase,
            "purchase_frequency": purchase_freq,
            "support_tickets": int(support_tickets),
            "satisfaction_score": satisfaction_score,
            "membership_duration_months": membership_duration_months,
            "churn": churn_flag
        })

    df_churn = pd.DataFrame(churn_records)
    print(f"[+] Created customer churn analytics snapshot: {len(df_churn)} records")
    print(f"    Churn rate: {df_churn['churn'].mean() * 100:.2f}%")

    # -------------------------------------------------------------
    # 5. Save Raw CSVs
    # -------------------------------------------------------------
    df_customers.to_csv(RAW_DATA_DIR / "customers_raw.csv", index=False)
    df_products.to_csv(RAW_DATA_DIR / "products_raw.csv", index=False)
    df_orders.to_csv(RAW_DATA_DIR / "orders_raw.csv", index=False)
    df_order_items.to_csv(RAW_DATA_DIR / "order_items_raw.csv", index=False)
    df_payments.to_csv(RAW_DATA_DIR / "payments_raw.csv", index=False)
    df_churn.to_csv(RAW_DATA_DIR / "customer_churn_raw.csv", index=False)

    print(f"[SUCCESS] All raw CSV files exported to {RAW_DATA_DIR}")

    return {
        "customers": df_customers,
        "products": df_products,
        "orders": df_orders,
        "order_items": df_order_items,
        "payments": df_payments,
        "customer_churn": df_churn
    }


def seed_mysql_database(data_dict):
    """
    Attempts to seed MySQL database if server is reachable.
    """
    try:
        from database import test_connection, execute_sql_file, insert_dataframe
        success, msg = test_connection()
        if not success:
            print(f"[INFO] Skipping MySQL direct seeding (MySQL offline or not configured: {msg}).")
            print("[INFO] Data is saved locally in data/raw/ and ready for analysis or manual import.")
            return False

        print("[*] MySQL connection confirmed! Initializing database schema...")
        schema_path = BASE_DIR / "database" / "schema.sql"
        execute_sql_file(schema_path)

        print("[*] Inserting generated data into MySQL tables...")
        insert_dataframe(data_dict["customers"], "customers", if_exists="append")
        insert_dataframe(data_dict["products"], "products", if_exists="append")
        insert_dataframe(data_dict["orders"], "orders", if_exists="append")
        insert_dataframe(data_dict["order_items"], "order_items", if_exists="append")
        insert_dataframe(data_dict["payments"], "payments", if_exists="append")
        insert_dataframe(data_dict["customer_churn"], "customer_churn", if_exists="append")

        print("[SUCCESS] MySQL database seeded successfully!")
        return True
    except Exception as e:
        print(f"[WARNING] MySQL database seeding encountered an issue: {e}")
        return False


if __name__ == "__main__":
    datasets = generate_synthetic_data(num_customers=5000)
    seed_mysql_database(datasets)
