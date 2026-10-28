from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sales_data.csv"
DB_PATH = BASE_DIR / "sales.db"

REQUIRED_COLUMNS = [
    "Transaction_Id", "Order_date", "Product", "Category", "Region",
    "Sales_channel", "Quantity", "Unit_price", "Discount_amount", "Status"
]

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database(csv_path=DATA_PATH):
    """Create the table and import the supplied CSV. Safe to rerun: replaces imported rows."""
    df = pd.read_csv(csv_path)
    missing_columns = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_columns:
        raise ValueError(f"CSV is missing required columns: {missing_columns}")

    df = df[REQUIRED_COLUMNS].copy()
    df["Order_date"] = pd.to_datetime(df["Order_date"], format="%d-%m-%Y", errors="coerce")
    for col in ["Quantity", "Unit_price", "Discount_amount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove records missing key identifiers/dimensions or with invalid dates.
    df = df.dropna(subset=["Transaction_Id", "Order_date", "Product", "Region", "Status"])
    # Preserve rows with missing numeric values for audit, but those rows won't count toward revenue.
    df["Order_date"] = df["Order_date"].dt.strftime("%Y-%m-%d")
    df["Transaction_Id"] = df["Transaction_Id"].astype(str).str.strip()
    df["Product"] = df["Product"].astype(str).str.strip()
    df["Region"] = df["Region"].astype(str).str.strip()
    df["Status"] = df["Status"].astype(str).str.strip().str.title()

    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                transaction_id TEXT PRIMARY KEY,
                order_date TEXT NOT NULL,
                product TEXT NOT NULL,
                category TEXT,
                region TEXT NOT NULL,
                sales_channel TEXT,
                quantity REAL,
                unit_price REAL,
                discount_amount REAL,
                status TEXT NOT NULL
            )
        """)
        conn.execute("DELETE FROM sales")
        conn.executemany("""
            INSERT OR REPLACE INTO sales
            (transaction_id, order_date, product, category, region, sales_channel,
             quantity, unit_price, discount_amount, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            (
                row.Transaction_Id, row.Order_date, row.Product, row.Category,
                row.Region, row.Sales_channel, _number(row.Quantity),
                _number(row.Unit_price), _number(row.Discount_amount), row.Status
            )
            for row in df.itertuples(index=False)
        ])
    return {"loaded_rows": len(df), "source_rows": int(pd.read_csv(csv_path).shape[0])}

def _number(value):
    return None if pd.isna(value) else float(value)
