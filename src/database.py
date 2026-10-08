"""
Database Management Module
Handles MySQL connectivity, connection pooling, graceful fallback, and query execution.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError

# Load environment variables from .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "customer_churn_db")


def get_db_url(include_db=True):
    """Constructs MySQL SQLAlchemy connection URL."""
    password_part = f":{DB_PASSWORD}" if DB_PASSWORD else ""
    db_part = f"/{DB_NAME}" if include_db else ""
    return f"mysql+mysqlconnector://{DB_USER}{password_part}@{DB_HOST}:{DB_PORT}{db_part}?charset=utf8mb4"


def get_engine(include_db=True):
    """Creates and returns a SQLAlchemy Engine."""
    db_url = get_db_url(include_db=include_db)
    return create_engine(
        db_url,
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args={"connect_timeout": 5}
    )


def test_connection():
    """
    Tests MySQL connection.
    Returns:
        tuple: (bool success, str message)
    """
    try:
        engine = get_engine(include_db=False)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1;"))
        return True, "Successfully connected to MySQL server."
    except OperationalError as e:
        return False, f"MySQL connection failed: {e.orig if hasattr(e, 'orig') else str(e)}"
    except Exception as e:
        return False, f"Unexpected database error: {str(e)}"


def execute_sql_file(file_path):
    """
    Executes a multi-statement SQL script file.
    """
    resolved_path = Path(file_path)
    if not resolved_path.is_absolute():
        resolved_path = BASE_DIR / resolved_path

    if not resolved_path.exists():
        raise FileNotFoundError(f"SQL file not found at: {resolved_path}")

    with open(resolved_path, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # Split commands by semicolon while respecting comments
    statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]

    engine = get_engine(include_db=False)
    with engine.connect() as conn:
        for stmt in statements:
            if stmt:
                conn.execute(text(stmt))
        conn.commit()
    return True


def fetch_dataframe(query, params=None):
    """
    Executes a SELECT query and returns a pandas DataFrame.
    Gracefully falls back if database is not available.
    """
    try:
        engine = get_engine(include_db=True)
        with engine.connect() as conn:
            df = pd.read_sql_query(text(query), conn, params=params)
        return df, True, "Query executed successfully."
    except Exception as e:
        return pd.DataFrame(), False, f"Database query failed: {str(e)}"


def insert_dataframe(df, table_name, if_exists="append"):
    """
    Inserts a pandas DataFrame into a MySQL table.
    """
    try:
        engine = get_engine(include_db=True)
        df.to_sql(table_name, con=engine, if_exists=if_exists, index=False, chunksize=1000)
        return True, f"Successfully inserted {len(df)} records into table '{table_name}'."
    except Exception as e:
        return False, f"Failed to insert DataFrame into table '{table_name}': {str(e)}"


if __name__ == "__main__":
    print("Testing MySQL connection settings...")
    success, msg = test_connection()
    print(f"Status: {'CONNECTED' if success else 'NOT CONNECTED'}")
    print(f"Details: {msg}")
