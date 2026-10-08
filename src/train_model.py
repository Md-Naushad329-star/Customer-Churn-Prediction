"""
Model Training & Evaluation Module
Trains, tunes, and evaluates:
1. Logistic Regression
2. Decision Tree Classifier
3. Random Forest Classifier
Compares metrics (Accuracy, Precision, Recall, F1, ROC-AUC),
automatically selects the champion model, and serializes it to models/best_model.pkl.
"""

from pathlib import Path
import json
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

from feature_engineering import (
    load_and_prepare_features, NUMERICAL_FEATURES, CATEGORICAL_FEATURES, get_preprocessor
)

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "outputs" / "reports"
CHARTS_DIR = BASE_DIR / "outputs" / "charts"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
CHARTS_DIR.mkdir(parents=True, exist_ok=True)


def train_and_evaluate_models():
    """
    Executes ML training workflow, evaluates models, saves artifacts,
    and returns evaluation results dictionary.
    """
    print("[*] Loading and splitting customer churn dataset...")
    X_train, X_test, y_train, y_test, preprocessor = load_and_prepare_features()
    print(f"[+] Train set: {X_train.shape[0]} samples | Test set: {X_test.shape[0]} samples")

    # Define model candidates
    models_dict = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=6, min_samples_split=20, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=150, max_depth=10, min_samples_split=10, random_state=42)
    }

    results = []
    trained_pipelines = {}
    confusion_matrices = {}

    print("\n[*] Training and evaluating models...")
    for model_name, classifier in models_dict.items():
        print(f"--> Training {model_name}...")
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier)
        ])

        pipeline.fit(X_train, y_train)
        trained_pipelines[model_name] = pipeline

        # Predictions
        y_pred = pipeline.predict(X_test)
        y_prob = pipeline.predict_proba(X_test)[:, 1] if hasattr(pipeline, "predict_proba") else y_pred

        # Metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc = roc_auc_score(y_test, y_prob)
        cm = confusion_matrix(y_test, y_pred)
        confusion_matrices[model_name] = cm

        results.append({
            "Model": model_name,
            "Accuracy": round(float(acc), 4),
            "Precision": round(float(prec), 4),
            "Recall": round(float(rec), 4),
            "F1_Score": round(float(f1), 4),
            "ROC_AUC": round(float(roc), 4)
        })

    df_results = pd.DataFrame(results).sort_values(by="F1_Score", ascending=False)
    print("\n================= MODEL COMPARISON TABLE =================")
    print(df_results.to_string(index=False))
    print("==========================================================\n")

    # Save comparison table
    df_results.to_csv(REPORTS_DIR / "model_comparison.csv", index=False)

    # Automatically select best model
    best_model_name = df_results.iloc[0]["Model"]
    best_pipeline = trained_pipelines[best_model_name]
    best_f1 = df_results.iloc[0]["F1_Score"]
    print(f"[BEST MODEL SELECTED]: {best_model_name} with F1-Score: {best_f1:.4f}")

    # Serialize champion model
    model_save_path = MODELS_DIR / "best_model.pkl"
    joblib.dump(best_pipeline, model_save_path)
    print(f"[+] Champion model pipeline persisted to {model_save_path}")

    # Save metadata report
    evaluation_metadata = {
        "best_model": best_model_name,
        "metrics_summary": results,
        "features": {
            "numerical": NUMERICAL_FEATURES,
            "categorical": CATEGORICAL_FEATURES
        },
        "test_set_size": len(y_test)
    }
    with open(REPORTS_DIR / "model_evaluation.json", "w", encoding="utf-8") as f:
        json.dump(evaluation_metadata, f, indent=4)

    # -------------------------------------------------------------
    # Visualization: Confusion Matrices for All 3 Models
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    for idx, (m_name, cm) in enumerate(confusion_matrices.items()):
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            cbar=False,
            ax=axes[idx],
            xticklabels=["Retained (0)", "Churned (1)"],
            yticklabels=["Retained (0)", "Churned (1)"]
        )
        axes[idx].set_title(f"{m_name}\nConfusion Matrix", fontsize=12, fontweight="bold")
        axes[idx].set_xlabel("Predicted Label")
        axes[idx].set_ylabel("Actual Label")

    plt.suptitle("Model Evaluation: Confusion Matrices", fontsize=14, fontweight="bold", y=1.03)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "model_confusion_matrix.png", dpi=200, bbox_inches="tight")
    plt.close()

    # -------------------------------------------------------------
    # Visualization: Feature Importance (from Champion or Tree)
    # -------------------------------------------------------------
    try:
        rf_pipeline = trained_pipelines.get("Random Forest", best_pipeline)
        rf_clf = rf_pipeline.named_steps["classifier"]
        fitted_preprocessor = rf_pipeline.named_steps["preprocessor"]

        # Extract encoded feature names
        cat_encoder = fitted_preprocessor.named_transformers_["cat"]
        encoded_cat_names = list(cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES))
        all_feature_names = NUMERICAL_FEATURES + encoded_cat_names

        importances = rf_clf.feature_importances_
        feat_df = pd.DataFrame({
            "Feature": all_feature_names,
            "Importance": importances
        }).sort_values(by="Importance", ascending=False).head(12)

        plt.figure(figsize=(9, 6))
        sns.barplot(data=feat_df, y="Feature", x="Importance", palette="viridis")
        plt.title("Top Predictive Drivers of Customer Churn (Random Forest)")
        plt.xlabel("Feature Importance Score")
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "model_feature_importance.png", dpi=200)
        plt.close()
        print(f"[+] Feature importance plot saved to {CHARTS_DIR / 'model_feature_importance.png'}")
    except Exception as e:
        print(f"[WARNING] Feature importance plot skipped: {e}")

    return df_results, best_model_name


if __name__ == "__main__":
    train_and_evaluate_models()
