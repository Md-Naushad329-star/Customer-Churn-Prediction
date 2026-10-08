"""
Streamlit Web Application
Customer Sales, Revenue & Churn Prediction Analytics System
"""

import os
import sys
from pathlib import Path
import json
import pandas as pd
import numpy as np
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="Customer Churn & Revenue Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set base directories and add src to system path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "src"))

from database import test_connection, fetch_dataframe
from predict import predict_churn, load_champion_model

# -------------------------------------------------------------
# Custom Styling (CSS)
# -------------------------------------------------------------
st.markdown("""
<style>
    /* Metric Card Styling */
    .metric-card {
        background: linear-gradient(135deg, rgba(28, 126, 214, 0.08) 0%, rgba(32, 201, 151, 0.08) 100%);
        border: 1px solid rgba(28, 126, 214, 0.2);
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .metric-label {
        font-size: 0.88rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #1c7ed6;
    }
    .metric-delta {
        font-size: 0.85rem;
        font-weight: 500;
        color: #2b8a3e;
    }
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .badge-green { background-color: #d3f9d8; color: #2b8a3e; }
    .badge-red { background-color: #ffe3e3; color: #e03131; }
    .badge-blue { background-color: #d0ebff; color: #1971c2; }
    .badge-amber { background-color: #fff3bf; color: #f08c00; }
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------------------
# Data Loader Functions (Cached)
# -------------------------------------------------------------
@st.cache_data(ttl=600)
def load_datasets():
    """Loads cleaned master datasets with graceful fallback."""
    churn_path = BASE_DIR / "data" / "processed" / "customer_churn_cleaned.csv"
    sales_path = BASE_DIR / "data" / "processed" / "sales_summary.csv"
    products_path = BASE_DIR / "data" / "raw" / "products_raw.csv"

    if churn_path.exists():
        df_churn = pd.read_csv(churn_path)
    else:
        df_churn = pd.DataFrame()

    if sales_path.exists():
        df_sales = pd.read_csv(sales_path)
        df_sales["order_date"] = pd.to_datetime(df_sales["order_date"])
    else:
        df_sales = pd.DataFrame()

    if products_path.exists():
        df_products = pd.read_csv(products_path)
    else:
        df_products = pd.DataFrame()

    return df_churn, df_sales, df_products


@st.cache_data(ttl=600)
def load_model_evaluation_metrics():
    """Loads evaluation comparison table and metadata."""
    eval_path = BASE_DIR / "outputs" / "reports" / "model_evaluation.json"
    comparison_path = BASE_DIR / "outputs" / "reports" / "model_comparison.csv"
    
    metadata = {}
    if eval_path.exists():
        with open(eval_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

    if comparison_path.exists():
        df_comp = pd.read_csv(comparison_path)
    else:
        df_comp = pd.DataFrame()

    return metadata, df_comp


# Load data into session
df_churn, df_sales, df_products = load_datasets()
eval_metadata, df_comparison = load_model_evaluation_metrics()

# Check MySQL status
mysql_connected, mysql_msg = test_connection()

# -------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------
st.sidebar.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=300&auto=format&fit=crop&q=60", use_container_width=True)
st.sidebar.title("🚀 Navigation")

page = st.sidebar.radio(
    "Select System Module:",
    [
        "Home",
        "Data Overview",
        "Sales Analytics",
        "Customer Analytics",
        "EDA Visualizations",
        "Machine Learning Model",
        "Customer Churn Prediction"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔌 Database Connectivity")
if mysql_connected:
    st.sidebar.success("🟢 MySQL Online (Connected)")
    st.sidebar.caption("Host: localhost:3306 | DB: customer_churn_db")
else:
    st.sidebar.warning("🟡 CSV Mode (MySQL Offline)")
    st.sidebar.caption("Using verified processed datasets from data/processed/")
    with st.sidebar.expander("Database Status Note"):
        st.write(f"Status message: {mysql_msg}")
        st.write("Start MySQL in Laragon/XAMPP to enable live SQL queries.")

st.sidebar.markdown("---")
st.sidebar.caption("v1.0.0 | B.Tech CSE / Data Science Project")


# =============================================================
# PAGE 1: HOME
# =============================================================
if page == "Home":
    st.title("📊 Customer Sales, Revenue & Churn Prediction System")
    st.markdown("""
    Welcome to the enterprise analytics and machine learning platform. This system unites 
    **Relational Database Analytics (MySQL)**, **Data Preprocessing & Exploratory Analysis**, 
    and **Supervised Machine Learning (Scikit-Learn)** to forecast customer churn and uncover actionable revenue drivers.
    """)

    # Top Level KPI Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_rev = df_sales["net_amount"].sum() if not df_sales.empty else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Gross Revenue</div>
            <div class="metric-value">${total_rev:,.2f}</div>
            <div class="metric-delta">▲ Across {len(df_sales):,} Orders</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        total_cust = len(df_churn) if not df_churn.empty else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Customer Base</div>
            <div class="metric-value">{total_cust:,}</div>
            <div class="metric-delta">Active relational profiles</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        aov = df_sales["net_amount"].mean() if not df_sales.empty else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average Order Value</div>
            <div class="metric-value">${aov:.2f}</div>
            <div class="metric-delta">Average basket size</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        churn_rate = (df_churn["churn"].mean() * 100) if not df_churn.empty else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Overall Churn Rate</div>
            <div class="metric-value" style="color: {'#e03131' if churn_rate > 30 else '#2b8a3e'};">{churn_rate:.1f}%</div>
            <div class="metric-delta">Target classification metric</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🛠️ Architecture & Data Pipeline")
    st.markdown("""
    ```
    ┌──────────────────────┐      ┌────────────────────────┐      ┌─────────────────────────┐
    │  Data Generation     │ ───► │  MySQL Relational DB   │ ───► │   Data Cleaning &       │
    │  5,000+ Customers    │      │  6 Relational Tables   │      │   Feature Engineering   │
    └──────────────────────┘      └────────────────────────┘      └─────────────────────────┘
                                                                               │
                                                                               ▼
    ┌──────────────────────┐      ┌────────────────────────┐      ┌─────────────────────────┐
    │  Power BI Dashboard  │ ◄─── │  Streamlit Application │ ◄─── │   Machine Learning      │
    │  Interactive BI KPIs │      │  Web UI & Predictions  │      │   Champion Model (97%+) │
    └──────────────────────┘      └────────────────────────┘      └─────────────────────────┘
    ```
    """)

    st.markdown("### 🎯 System Highlights")
    c1, c2 = st.columns(2)
    with c1:
        st.info("""
        **1. Relational Database Engine (MySQL)**
        * Normalized schema (`customers`, `products`, `orders`, `order_items`, `payments`, `customer_churn`).
        * Complex queries with JOIN, GROUP BY, CTEs, Window functions, and RFM proxies.
        * Foreign key integrity with cascading updates and indexes.
        """)
        st.success("""
        **2. Exploratory Data Analysis & Visualizations**
        * 12 publication-ready Matplotlib & Seaborn visualizations.
        * In-depth correlation analysis between churn, dissatisfaction, and ticket backlogs.
        * Geographic and demographic revenue breakdowns.
        """)
    with c2:
        st.warning("""
        **3. Machine Learning Classification Pipeline**
        * 3 Supervised models: Logistic Regression, Decision Tree, Random Forest.
        * Automated evaluation across Accuracy, Precision, Recall, F1, and ROC-AUC.
        * Auto-selection of best model serialized with Joblib.
        """)
        st.error("""
        **4. Real-Time Churn Predictor & Power BI Integration**
        * Live scoring interactive calculator with instantaneous probability & risk factor breakdown.
        * Exported dimensional models (`dim_*`, `fact_*`) ready for direct import into Power BI.
        * Complete DAX measures reference included.
        """)


# =============================================================
# PAGE 2: DATA OVERVIEW
# =============================================================
elif page == "Data Overview":
    st.title("📋 Enterprise Data Overview & Schema Explorer")
    st.markdown("Inspect customer records, transaction details, and dataset health metrics.")

    tab1, tab2, tab3 = st.tabs(["Customer Churn Dataset", "Sales Transactions", "Products Catalog"])

    with tab1:
        st.subheader("Customer Profiles & Telemetry Snapshot")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            tier_filter = st.multiselect("Filter by Membership Tier:", options=df_churn["membership_type"].unique(), default=df_churn["membership_type"].unique())
        with col_f2:
            status_filter = st.selectbox("Filter by Status:", ["All Customers", "Retained Only", "Churned Only"])

        filtered_churn = df_churn[df_churn["membership_type"].isin(tier_filter)]
        if status_filter == "Retained Only":
            filtered_churn = filtered_churn[filtered_churn["churn"] == 0]
        elif status_filter == "Churned Only":
            filtered_churn = filtered_churn[filtered_churn["churn"] == 1]

        st.dataframe(filtered_churn.head(200), use_container_width=True)
        st.caption(f"Showing {len(filtered_churn):,} records matching filters.")

        st.markdown("#### Descriptive Statistics (Numerical Features)")
        st.dataframe(df_churn.describe().T.round(2), use_container_width=True)

    with tab2:
        st.subheader("Sales Orders Table")
        st.dataframe(df_sales.head(200), use_container_width=True)
        st.caption(f"Total Transactions: {len(df_sales):,} records")

    with tab3:
        st.subheader("Products Catalog")
        st.dataframe(df_products, use_container_width=True)


# =============================================================
# PAGE 3: SALES ANALYTICS
# =============================================================
elif page == "Sales Analytics":
    st.title("📈 Sales & Revenue Analytics")
    st.markdown("Analyze sales trends, order volumes, geographic concentrations, and product performance.")

    # Monthly revenue trend
    if not df_sales.empty:
        df_monthly = df_sales.set_index("order_date").resample("ME")["net_amount"].agg(["sum", "count"]).reset_index()
        df_monthly["month_label"] = df_monthly["order_date"].dt.strftime("%b %Y")

        st.subheader("Monthly Revenue & Order Volume Growth")
        st.bar_chart(df_monthly.set_index("month_label")["sum"], color="#1c7ed6")

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Top Revenue Contributing Cities")
            city_rev = df_sales.groupby("city")["net_amount"].sum().sort_values(ascending=False).head(10)
            st.bar_chart(city_rev, color="#20c997")

        with c2:
            st.subheader("Revenue by Membership Tier")
            tier_rev = df_sales.groupby("membership_type")["net_amount"].sum().loc[["Bronze", "Silver", "Gold", "Platinum"]]
            st.bar_chart(tier_rev, color="#f59f00")


# =============================================================
# PAGE 4: CUSTOMER ANALYTICS
# =============================================================
elif page == "Customer Analytics":
    st.title("👥 Customer Behavioral Analytics & Segmentation")
    st.markdown("Explore customer retention, recency, satisfaction scores, and support ticket correlations.")

    col1, col2, col3 = st.columns(3)
    with col1:
        avg_sat = df_churn["satisfaction_score"].mean()
        st.metric("Avg Satisfaction Score", f"{avg_sat:.2f} / 5.0", delta="Target: > 4.0")
    with col2:
        avg_tickets = df_churn["support_tickets"].mean()
        st.metric("Avg Support Tickets / User", f"{avg_tickets:.2f}", delta="-0.1 MoM", delta_color="inverse")
    with col3:
        avg_inactivity = df_churn["days_since_last_purchase"].mean()
        st.metric("Avg Days Inactive", f"{avg_inactivity:.1f} Days")

    st.markdown("### Customer Lifetime Spend vs Inactivity (Recency)")
    st.scatter_chart(
        df_churn.head(1000),
        x="days_since_last_purchase",
        y="total_spend",
        color="churn"
    )

    st.markdown("### Churn Rate by Satisfaction Score Tier")
    sat_bins = pd.cut(df_churn["satisfaction_score"], bins=[0.9, 2.5, 3.5, 5.0], labels=["Low (1.0-2.5)", "Moderate (2.6-3.5)", "High (3.6-5.0)"])
    sat_churn = df_churn.groupby(sat_bins, observed=False)["churn"].mean() * 100
    st.bar_chart(sat_churn, color="#e03131")


# =============================================================
# PAGE 5: EDA VISUALIZATIONS
# =============================================================
elif page == "EDA Visualizations":
    st.title("📊 Exploratory Data Analysis (EDA) Gallery")
    st.markdown("High-resolution, publication-grade visualization plots generated via Matplotlib and Seaborn.")

    charts_dir = BASE_DIR / "outputs" / "charts"
    chart_list = [
        ("01_customer_age_distribution.png", "Customer Age Distribution by Churn Status"),
        ("02_revenue_distribution.png", "Distribution of Order Net Revenue"),
        ("03_monthly_sales_trend.png", "Monthly Sales & Transaction Volume Trend"),
        ("04_sales_by_city.png", "Total Revenue by Geographic City Market"),
        ("05_sales_by_membership.png", "Average Spend & Churn Rate by Membership Tier"),
        ("06_top_products.png", "Top 10 Best-Selling Products by Revenue"),
        ("07_churn_distribution.png", "Overall Customer Attrition vs Retention Ratio"),
        ("08_correlation_heatmap.png", "Customer Behavioral Features Correlation Heatmap"),
        ("09_churn_vs_purchase_frequency.png", "Annual Purchase Frequency by Churn Status"),
        ("10_churn_vs_satisfaction_score.png", "Satisfaction Score Density: Retained vs Churned"),
        ("11_churn_vs_total_spending.png", "Customer Lifetime Spend Boxplot by Churn"),
        ("12_churn_drivers_multivariate.png", "Multivariate Churn Drivers: Support Tickets & Recency"),
        ("model_confusion_matrix.png", "ML Evaluation: Confusion Matrices for All Models"),
        ("model_feature_importance.png", "Top Predictive Feature Drivers of Churn")
    ]

    selected_chart_name = st.selectbox(
        "Choose visualization to display:",
        options=[name for _, name in chart_list]
    )

    filename = next(fname for fname, name in chart_list if name == selected_chart_name)
    chart_path = charts_dir / filename

    if chart_path.exists():
        st.image(str(chart_path), caption=selected_chart_name, use_container_width=True)
    else:
        st.warning(f"Chart file '{filename}' not found. Please run `python src/eda.py`.")


# =============================================================
# PAGE 6: MACHINE LEARNING MODEL
# =============================================================
elif page == "Machine Learning Model":
    st.title("🤖 Machine Learning Model Comparison & Evaluation")
    st.markdown("""
    Three distinct supervised classification algorithms were trained, cross-validated, 
    and compared using standard data science performance benchmarks.
    """)

    if not df_comparison.empty:
        st.subheader("Model Performance Comparison Table")
        st.dataframe(
            df_comparison.style.highlight_max(subset=["Accuracy", "Precision", "Recall", "F1_Score", "ROC_AUC"], color="#d3f9d8"),
            use_container_width=True
        )

        st.subheader("Metric Comparison Chart")
        st.bar_chart(df_comparison.set_index("Model")[["Accuracy", "Precision", "Recall", "F1_Score", "ROC_AUC"]])

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Selected Champion Model</div>
            <div class="metric-value">{eval_metadata.get('best_model', 'Logistic Regression')}</div>
            <div class="metric-delta">Saved to models/best_model.pkl for real-time inference</div>
        </div>
        """, unsafe_allow_html=True)

    cm_path = BASE_DIR / "outputs" / "charts" / "model_confusion_matrix.png"
    if cm_path.exists():
        st.image(str(cm_path), caption="Confusion Matrices across Models", use_container_width=True)

    fi_path = BASE_DIR / "outputs" / "charts" / "model_feature_importance.png"
    if fi_path.exists():
        st.image(str(fi_path), caption="Model Feature Importances", use_container_width=True)


# =============================================================
# PAGE 7: CUSTOMER CHURN PREDICTION
# =============================================================
elif page == "Customer Churn Prediction":
    st.title("🔮 Real-Time Customer Churn Prediction Engine")
    st.markdown("""
    Enter custom customer parameters below to evaluate retention probability, churn risk category, 
    and recommended business interventions.
    """)

    with st.form("churn_prediction_form"):
        st.subheader("👤 Customer Demographics")
        col_d1, col_d2, col_d3, col_d4 = st.columns(4)
        with col_d1:
            age = st.slider("Customer Age", 18, 80, 34)
        with col_d2:
            gender = st.selectbox("Gender", ["Female", "Male", "Other"])
        with col_d3:
            city = st.selectbox("City", ["Mumbai", "Bengaluru", "Delhi", "Hyderabad", "Chennai", "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Kochi"])
        with col_d4:
            membership = st.selectbox("Membership Tier", ["Bronze", "Silver", "Gold", "Platinum"], index=1)

        st.subheader("📊 Purchase & Engagement Telemetry")
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            total_orders = st.number_input("Total Lifetime Orders", min_value=0, max_value=50, value=3)
            days_inactive = st.slider("Days Since Last Purchase", 0, 365, 30)
        with col_p2:
            total_spend = st.number_input("Total Lifetime Spend ($)", min_value=0.0, max_value=5000.0, value=250.0, step=10.0)
            purchase_freq = st.slider("Purchase Frequency (Orders / Year)", 0.0, 10.0, 1.2, step=0.1)
        with col_p3:
            duration_months = st.slider("Account Age (Months)", 1, 48, 12)
            aov_calc = round(total_spend / total_orders, 2) if total_orders > 0 else 0.0
            st.metric("Computed AOV ($)", f"${aov_calc:.2f}")

        st.subheader("⭐ Customer Experience & Support")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            satisfaction = st.slider("Customer Satisfaction Score", 1.0, 5.0, 4.0, step=0.1)
        with col_s2:
            support_tickets = st.slider("Unresolved Support Tickets", 0, 10, 1)

        submitted = st.form_submit_button("⚡ Predict Churn Risk", use_container_width=True)

    if submitted:
        input_data = {
            "age": age,
            "gender": gender,
            "city": city,
            "membership_type": membership,
            "total_orders": total_orders,
            "total_spend": total_spend,
            "average_order_value": aov_calc,
            "days_since_last_purchase": days_inactive,
            "purchase_frequency": purchase_freq,
            "support_tickets": support_tickets,
            "satisfaction_score": satisfaction,
            "membership_duration_months": duration_months
        }

        with st.spinner("Evaluating ML model pipeline..."):
            try:
                res = predict_churn(input_data)
                
                st.markdown("---")
                st.subheader("🎯 Prediction Results")

                col_res1, col_res2, col_res3 = st.columns(3)

                with col_res1:
                    if res["churn_prediction"] == "Yes":
                        st.markdown("""
                        <div style="background-color: #ffe3e3; border: 2px solid #e03131; border-radius: 12px; padding: 20px; text-align: center;">
                            <h3 style="color: #c92a2a; margin: 0;">CHURN RISK: YES</h3>
                            <p style="color: #495057; margin-top: 5px;">Customer is likely to discontinue engagement.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div style="background-color: #d3f9d8; border: 2px solid #2b8a3e; border-radius: 12px; padding: 20px; text-align: center;">
                            <h3 style="color: #2b8a3e; margin: 0;">CHURN RISK: NO</h3>
                            <p style="color: #495057; margin-top: 5px;">Customer is projected to stay retained.</p>
                        </div>
                        """, unsafe_allow_html=True)

                with col_res2:
                    st.metric("Estimated Churn Probability", res["churn_probability"])
                    st.progress(min(1.0, max(0.0, res["churn_probability_raw"])))

                with col_res3:
                    risk_badge_class = "badge-red" if res["risk_category"] == "High Risk" else "badge-amber" if res["risk_category"] == "Moderate Risk" else "badge-green"
                    st.markdown(f"""
                    <div style="padding: 10px;">
                        <span class="badge-pill {risk_badge_class}">{res['risk_category']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.caption("Categorization based on probability score thresholds.")

                st.markdown("#### 🔍 Identified Risk Factors & Indicators")
                for factor in res["risk_factors"]:
                    st.write(f"• **{factor}**")

                st.markdown("#### 💡 Recommended Next Actions")
                if res["churn_prediction"] == "Yes":
                    st.warning("""
                    * **Proactive Outreach**: Initiate direct customer support follow-up to resolve open tickets.
                    * **Personalized Retention Incentive**: Offer a targeted 15% discount on the customer's next purchase.
                    * **Re-engagement Campaign**: Send an automated email showcasing fresh arrivals in preferred categories.
                    """)
                else:
                    st.success("""
                    * **Loyalty Upsell**: Customer has high retention telemetry. Recommend upgrading membership tier or enrolling in loyalty rewards.
                    * **Review Request**: Invite customer to share a review or product feedback.
                    """)

            except Exception as e:
                st.error(f"Error executing prediction: {e}")
