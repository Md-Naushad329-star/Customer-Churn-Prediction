"""
Prediction Service Module
Loads the serialized champion machine learning model and provides:
1. Single customer real-time inference with probability and risk factors
2. Batch scoring on customer datasets
3. Standalone CLI testing
"""

from pathlib import Path
import json
import joblib
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "best_model.pkl"
PREDICTIONS_DIR = BASE_DIR / "outputs" / "predictions"
PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)

# Default baseline fallback values
DEFAULT_CUSTOMER = {
    "age": 35,
    "gender": "Female",
    "city": "Mumbai",
    "membership_type": "Silver",
    "total_orders": 3,
    "total_spend": 280.0,
    "average_order_value": 93.33,
    "days_since_last_purchase": 45,
    "purchase_frequency": 0.5,
    "support_tickets": 1,
    "satisfaction_score": 3.8,
    "membership_duration_months": 12
}


def load_champion_model(model_path=None):
    """Loads the persisted scikit-learn pipeline."""
    target_path = Path(model_path) if model_path else MODEL_PATH
    if not target_path.exists():
        raise FileNotFoundError(
            f"Trained model not found at {target_path}. Please execute `python src/train_model.py` first."
        )
    return joblib.load(target_path)


def predict_churn(customer_data: dict, model=None) -> dict:
    """
    Predicts customer churn status and probability for a single customer profile.
    
    Parameters:
        customer_data (dict): Dictionary with customer attributes
        model: Optional pre-loaded model pipeline
        
    Returns:
        dict: Prediction summary containing:
              - churn_prediction ('Yes' / 'No')
              - churn_flag (1 / 0)
              - churn_probability_pct (float)
              - risk_category ('Low', 'Moderate', 'High')
              - risk_factors (list of actionable insights)
    """
    if model is None:
        model = load_champion_model()

    # Fill any missing keys with sensible defaults
    full_data = {**DEFAULT_CUSTOMER, **customer_data}
    
    # Auto-calculate derived fields if not passed
    if "average_order_value" not in customer_data or customer_data["average_order_value"] is None:
        orders = full_data.get("total_orders", 1)
        spend = full_data.get("total_spend", 0.0)
        full_data["average_order_value"] = round(spend / orders, 2) if orders > 0 else 0.0

    df_input = pd.DataFrame([full_data])

    pred = model.predict(df_input)[0]
    
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(df_input)[0][1]
    else:
        prob = float(pred)

    prob_pct = round(float(prob) * 100, 2)

    # Risk category
    if prob >= 0.70:
        risk_level = "High Risk"
    elif prob >= 0.40:
        risk_level = "Moderate Risk"
    else:
        risk_level = "Low Risk"

    # Actionable risk driver insights
    risk_factors = []
    if full_data.get("satisfaction_score", 5.0) < 3.0:
        risk_factors.append("Low satisfaction score (< 3.0)")
    if full_data.get("days_since_last_purchase", 0) > 60:
        risk_factors.append(f"High inactivity ({full_data['days_since_last_purchase']} days without purchase)")
    if full_data.get("support_tickets", 0) >= 3:
        risk_factors.append(f"Elevated support tickets ({full_data['support_tickets']} logged)")
    if full_data.get("membership_type") == "Bronze":
        risk_factors.append("Bronze membership tier (historically lowest retention)")
    if full_data.get("total_orders", 0) <= 1:
        risk_factors.append("Low order frequency (1 or fewer lifetime orders)")

    if not risk_factors and prob < 0.40:
        risk_factors.append("Healthy engagement telemetry across all indicators")

    return {
        "churn_prediction": "Yes" if pred == 1 else "No",
        "churn_flag": int(pred),
        "churn_probability": f"{prob_pct}%",
        "churn_probability_raw": prob,
        "risk_category": risk_level,
        "risk_factors": risk_factors
    }


def predict_batch(df: pd.DataFrame, output_filename="batch_scored_customers.csv", model=None):
    """Scores an entire DataFrame of customers and exports the predictions."""
    if model is None:
        model = load_champion_model()

    df_out = df.copy()
    preds = model.predict(df_out)
    probs = model.predict_proba(df_out)[:, 1] if hasattr(model, "predict_proba") else preds

    df_out["predicted_churn"] = preds
    df_out["churn_probability"] = np.round(probs * 100, 2)
    df_out["churn_risk_level"] = np.where(
        probs >= 0.70, "High Risk",
        np.where(probs >= 0.40, "Moderate Risk", "Low Risk")
    )

    save_path = PREDICTIONS_DIR / output_filename
    df_out.to_csv(save_path, index=False)
    print(f"[+] Batch predictions saved to {save_path} ({len(df_out)} records)")
    return df_out


if __name__ == "__main__":
    print("================== SINGLE PREDICTION TEST ==================")
    sample_happy_customer = {
        "age": 32,
        "gender": "Female",
        "city": "Bengaluru",
        "membership_type": "Platinum",
        "total_orders": 6,
        "total_spend": 680.0,
        "days_since_last_purchase": 14,
        "purchase_frequency": 1.2,
        "support_tickets": 0,
        "satisfaction_score": 4.8,
        "membership_duration_months": 15
    }

    sample_at_risk_customer = {
        "age": 45,
        "gender": "Male",
        "city": "Delhi",
        "membership_type": "Bronze",
        "total_orders": 1,
        "total_spend": 45.0,
        "days_since_last_purchase": 85,
        "purchase_frequency": 0.15,
        "support_tickets": 4,
        "satisfaction_score": 2.1,
        "membership_duration_months": 8
    }

    print("\n[Test 1] Retained VIP Profile:")
    res1 = predict_churn(sample_happy_customer)
    print(json.dumps(res1, indent=2))

    print("\n[Test 2] At-Risk Customer Profile:")
    res2 = predict_churn(sample_at_risk_customer)
    print(json.dumps(res2, indent=2))
