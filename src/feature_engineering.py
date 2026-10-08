"""
Feature Engineering & Preprocessing Pipeline
Defines feature transformations, scaling, one-hot encoding, and train-test splitting.
"""

from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "customer_churn_cleaned.csv"

# Feature definitions
NUMERICAL_FEATURES = [
    "age",
    "total_orders",
    "total_spend",
    "average_order_value",
    "days_since_last_purchase",
    "purchase_frequency",
    "support_tickets",
    "satisfaction_score",
    "membership_duration_months"
]

CATEGORICAL_FEATURES = [
    "gender",
    "city",
    "membership_type"
]

TARGET_COLUMN = "churn"


def get_preprocessor():
    """
    Constructs a ColumnTransformer that scales numerical variables
    and encodes categorical variables.
    """
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERICAL_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ],
        remainder="drop"
    )
    return preprocessor


def load_and_prepare_features(data_file=None, test_size=0.2, random_state=42):
    """
    Loads processed churn data and splits into train and test sets.
    Returns:
        X_train, X_test, y_train, y_test, preprocessor, feature_cols
    """
    file_to_load = Path(data_file) if data_file else DATA_PATH
    if not file_to_load.exists():
        raise FileNotFoundError(f"Cleaned dataset not found at {file_to_load}. Run data cleaning first.")

    df = pd.read_csv(file_to_load)

    # Validate columns
    required_cols = NUMERICAL_FEATURES + CATEGORICAL_FEATURES + [TARGET_COLUMN]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' is missing from dataset.")

    X = df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET_COLUMN].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    preprocessor = get_preprocessor()

    return X_train, X_test, y_train, y_test, preprocessor


if __name__ == "__main__":
    print("[*] Feature engineering configuration:")
    print(f"    Numerical Features ({len(NUMERICAL_FEATURES)}): {NUMERICAL_FEATURES}")
    print(f"    Categorical Features ({len(CATEGORICAL_FEATURES)}): {CATEGORICAL_FEATURES}")
    print(f"    Target Column: {TARGET_COLUMN}")
