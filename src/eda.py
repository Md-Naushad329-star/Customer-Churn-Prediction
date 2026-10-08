"""
Exploratory Data Analysis (EDA) Module
Generates statistical summaries and high-resolution visualization charts
saved to outputs/charts/ and outputs/reports/.
"""

import os
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Styling configuration
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["font.size"] = 11
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.labelsize"] = 12
plt.rcParams["figure.titlesize"] = 16

BASE_DIR = Path(__file__).resolve().parent.parent
CHARTS_DIR = BASE_DIR / "outputs" / "charts"
REPORTS_DIR = BASE_DIR / "outputs" / "reports"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RAW_DIR = BASE_DIR / "data" / "raw"

CHARTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

STATUS_PALETTE = {"Retained": "#2b8a3e", "Churned": "#e03131"}


def run_exploratory_analysis():
    """Executes full EDA pipeline and writes charts & summary report."""
    print("[*] Starting comprehensive Exploratory Data Analysis...")

    df_churn = pd.read_csv(PROCESSED_DIR / "customer_churn_cleaned.csv")
    df_sales = pd.read_csv(PROCESSED_DIR / "sales_summary.csv")
    df_items = pd.read_csv(RAW_DIR / "order_items_raw.csv")
    df_products = pd.read_csv(RAW_DIR / "products_raw.csv")

    df_sales["order_date"] = pd.to_datetime(df_sales["order_date"])
    df_churn["churn_label"] = df_churn["churn"].map({0: "Retained", 1: "Churned"})

    # -------------------------------------------------------------
    # 1. Dataset Overview & Statistical Summary
    # -------------------------------------------------------------
    summary_stats = {
        "total_customers": int(len(df_churn)),
        "total_orders": int(len(df_sales)),
        "total_revenue": float(round(df_sales["net_amount"].sum(), 2)),
        "average_order_value": float(round(df_sales["net_amount"].mean(), 2)),
        "overall_churn_rate_pct": float(round(df_churn["churn"].mean() * 100, 2)),
        "churned_customers": int(df_churn["churn"].sum()),
        "retained_customers": int((df_churn["churn"] == 0).sum()),
        "avg_customer_age": float(round(df_churn["age"].mean(), 1)),
        "avg_satisfaction_score": float(round(df_churn["satisfaction_score"].mean(), 2)),
        "avg_support_tickets": float(round(df_churn["support_tickets"].mean(), 2)),
        "missing_values_count": int(df_churn.isnull().sum().sum()),
        "duplicate_rows_count": int(df_churn.duplicated().sum())
    }

    report_path = REPORTS_DIR / "eda_summary.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(summary_stats, f, indent=4)
    print(f"[+] Summary report saved to {report_path}")

    # -------------------------------------------------------------
    # Chart 1: Customer Age Distribution
    # -------------------------------------------------------------
    plt.figure(figsize=(9, 5))
    sns.histplot(
        data=df_churn,
        x="age",
        hue="churn_label",
        palette=STATUS_PALETTE,
        kde=True,
        bins=25,
        alpha=0.6,
        element="step"
    )
    plt.title("Distribution of Customer Age by Churn Status")
    plt.xlabel("Customer Age (Years)")
    plt.ylabel("Customer Count")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "01_customer_age_distribution.png", dpi=200)
    plt.close()

    # -------------------------------------------------------------
    # Chart 2: Revenue Distribution (Order Values)
    # -------------------------------------------------------------
    plt.figure(figsize=(9, 5))
    sns.histplot(df_sales["net_amount"], kde=True, color="#1c7ed6", bins=30, alpha=0.6)
    plt.axvline(df_sales["net_amount"].mean(), color="#e03131", linestyle="--", label=f"Mean: ${df_sales['net_amount'].mean():.2f}")
    plt.axvline(df_sales["net_amount"].median(), color="#2b8a3e", linestyle=":", label=f"Median: ${df_sales['net_amount'].median():.2f}")
    plt.title("Distribution of Net Order Revenue")
    plt.xlabel("Order Net Value ($)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "02_revenue_distribution.png", dpi=200)
    plt.close()

    # -------------------------------------------------------------
    # Chart 3: Monthly Sales & Revenue Trend
    # -------------------------------------------------------------
    monthly_sales = df_sales.set_index("order_date").resample("ME")["net_amount"].agg(["sum", "count"]).reset_index()
    monthly_sales["month_str"] = monthly_sales["order_date"].dt.strftime("%b %Y")

    fig, ax1 = plt.subplots(figsize=(11, 5))
    ax2 = ax1.twinx()

    x_indices = np.arange(len(monthly_sales))
    ax1.bar(x_indices, monthly_sales["sum"] / 1000.0, color="#74c0fc", alpha=0.7, label="Monthly Revenue ($K)")
    ax2.plot(x_indices, monthly_sales["count"], color="#1864ab", marker="o", linewidth=2.5, label="Order Count")

    ax1.set_xlabel("Month")
    ax1.set_ylabel("Revenue ($ in Thousands)", color="#1864ab")
    ax2.set_ylabel("Number of Orders", color="#1c7ed6")
    ax1.set_title("Monthly Revenue and Transaction Volume Trend")
    ax1.set_xticks(x_indices)
    ax1.set_xticklabels(monthly_sales["month_str"], rotation=45, ha="right")
    ax1.grid(axis="y", linestyle="--", alpha=0.5)
    ax2.grid(False)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "03_monthly_sales_trend.png", dpi=200)
    plt.close()

    # -------------------------------------------------------------
    # Chart 4: Sales Revenue by City
    # -------------------------------------------------------------
    city_rev = df_sales.groupby("city")["net_amount"].sum().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(10, 5))
    sns.barplot(data=city_rev, x="city", y="net_amount", hue="city", palette="crest", legend=False)
    plt.title("Total Revenue by Geographic Market (City)")
    plt.xlabel("City")
    plt.ylabel("Total Revenue ($)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "04_sales_by_city.png", dpi=200)
    plt.close()

    # -------------------------------------------------------------
    # Chart 5: Revenue and Churn by Membership Tier
    # -------------------------------------------------------------
    tier_stats = df_churn.groupby("membership_type").agg(
        total_customers=("customer_id", "count"),
        churn_rate=("churn", lambda x: x.mean() * 100),
        avg_spend=("total_spend", "mean")
    ).loc[["Bronze", "Silver", "Gold", "Platinum"]].reset_index()

    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    sns.barplot(data=tier_stats, x="membership_type", y="avg_spend", hue="membership_type", palette="viridis", legend=False, ax=ax[0])
    ax[0].set_title("Average Customer Spend by Membership Tier")
    ax[0].set_ylabel("Average Spend ($)")
    ax[0].set_xlabel("Membership Tier")

    sns.barplot(data=tier_stats, x="membership_type", y="churn_rate", hue="membership_type", palette="rocket", legend=False, ax=ax[1])
    ax[1].set_title("Customer Churn Rate (%) by Membership Tier")
    ax[1].set_ylabel("Churn Rate (%)")
    ax[1].set_xlabel("Membership Tier")
    for p in ax[1].patches:
        ax[1].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height() / 2.),
                       ha='center', va='center', color='white', fontweight='bold')
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "05_sales_by_membership.png", dpi=200)
    plt.close()

    # -------------------------------------------------------------
    # Chart 6: Top 10 Best-Selling Products by Revenue
    # -------------------------------------------------------------
    items_prod = pd.merge(df_items, df_products[["product_id", "product_name", "category"]], on="product_id")
    top_prod = items_prod.groupby("product_name")["item_total"].sum().sort_values(ascending=False).head(10).reset_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_prod, y="product_name", x="item_total", hue="product_name", palette="Blues_r", legend=False)
    plt.title("Top 10 Best-Selling Products by Revenue")
    plt.xlabel("Total Gross Revenue ($)")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "06_top_products.png", dpi=200)
    plt.close()

    # -------------------------------------------------------------
    # Chart 7: Overall Churn Distribution
    # -------------------------------------------------------------
    churn_counts = df_churn["churn_label"].value_counts()
    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        churn_counts,
        labels=churn_counts.index,
        autopct="%1.1f%%",
        colors=["#2b8a3e", "#e03131"],
        startangle=140,
        explode=(0, 0.08),
        textprops=dict(color="black", fontweight="bold", fontsize=12)
    )
    plt.title("Customer Attrition vs Retention Ratio", pad=20)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "07_churn_distribution.png", dpi=200)
    plt.close()

    # -------------------------------------------------------------
    # Chart 8: Feature Correlation Heatmap
    # -------------------------------------------------------------
    corr_cols = [
        "age", "total_orders", "total_spend", "average_order_value",
        "days_since_last_purchase", "purchase_frequency", "support_tickets",
        "satisfaction_score", "membership_duration_months", "churn"
    ]
    corr_matrix = df_churn[corr_cols].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8}
    )
    plt.title("Customer Behavioral Features Correlation Heatmap")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "08_correlation_heatmap.png", dpi=200)
    plt.close()

    # -------------------------------------------------------------
    # Chart 9: Churn vs Purchase Frequency
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df_churn, x="churn_label", y="purchase_frequency", hue="churn_label", palette=STATUS_PALETTE, legend=False)
    plt.title("Annual Purchase Frequency by Churn Status")
    plt.xlabel("Status")
    plt.ylabel("Purchases Per Year")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "09_churn_vs_purchase_frequency.png", dpi=200)
    plt.close()

    # -------------------------------------------------------------
    # Chart 10: Churn vs Customer Satisfaction Score
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 5))
    sns.kdeplot(data=df_churn, x="satisfaction_score", hue="churn_label", common_norm=False, fill=True, palette=STATUS_PALETTE, alpha=0.5)
    plt.title("Satisfaction Score Density: Retained vs Churned")
    plt.xlabel("Satisfaction Score (1.0 to 5.0)")
    plt.ylabel("Density")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "10_churn_vs_satisfaction_score.png", dpi=200)
    plt.close()

    # -------------------------------------------------------------
    # Chart 11: Churn vs Total Spending
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df_churn, x="churn_label", y="total_spend", hue="churn_label", palette=STATUS_PALETTE, legend=False)
    plt.title("Customer Lifetime Spend by Churn Status")
    plt.xlabel("Status")
    plt.ylabel("Total Spend ($)")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "11_churn_vs_total_spending.png", dpi=200)
    plt.close()

    # -------------------------------------------------------------
    # Chart 12: Churn Drivers (Support Tickets & Days Inactive)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    sns.barplot(data=df_churn, x="support_tickets", y="churn", color="#e03131", errorbar=None, ax=ax[0])
    ax[0].set_title("Churn Rate by Unresolved Support Tickets")
    ax[0].set_xlabel("Number of Support Tickets")
    ax[0].set_ylabel("Churn Probability")
    ax[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y*100:.0f}%"))

    sns.boxplot(data=df_churn, x="churn_label", y="days_since_last_purchase", hue="churn_label", palette=STATUS_PALETTE, legend=False, ax=ax[1])
    ax[1].set_title("Days Since Last Purchase by Churn Status")
    ax[1].set_xlabel("Status")
    ax[1].set_ylabel("Inactivity (Days)")

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "12_churn_drivers_multivariate.png", dpi=200)
    plt.close()

    print(f"[SUCCESS] All 12 EDA charts generated and saved into {CHARTS_DIR}")
    return summary_stats


if __name__ == "__main__":
    run_exploratory_analysis()
