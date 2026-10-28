import sqlite3
from database import get_connection

# Revenue rule: (quantity * unit price) - discount.
# Count only Completed records; exclude Returned and rows with missing/invalid numeric values.
VALID_REVENUE = """
    status = 'Completed'
    AND quantity IS NOT NULL AND quantity > 0
    AND unit_price IS NOT NULL AND unit_price >= 0
    AND discount_amount IS NOT NULL AND discount_amount >= 0
"""

def _rows(conn, sql, params=()):
    return [dict(row) for row in conn.execute(sql, params).fetchall()]

def run_analytics(intent: str, params: dict | None = None):
    params = params or {}
    with get_connection() as conn:
        if intent == "total_revenue":
            rows = _rows(conn, f"""
                SELECT ROUND(SUM(quantity * unit_price - discount_amount), 2) AS total_revenue,
                       COUNT(*) AS transaction_count
                FROM sales WHERE {VALID_REVENUE}
            """)
            return {"intent": intent, "answer": f"Total revenue is {rows[0]['total_revenue']:.2f}.",
                    "data": rows, "revenue_rule": "(quantity × unit price) − discount; completed valid rows only"}

        if intent == "top_product":
            rows = _rows(conn, f"""
                SELECT product,
                       ROUND(SUM(quantity * unit_price - discount_amount), 2) AS revenue,
                       SUM(quantity) AS units_sold
                FROM sales WHERE {VALID_REVENUE}
                GROUP BY product ORDER BY revenue DESC, product ASC LIMIT 1
            """)
            if not rows:
                return {"intent": intent, "answer": "No eligible sales records were found.", "data": []}
            return {"intent": intent, "answer": f"{rows[0]['product']} generated the highest revenue: {rows[0]['revenue']:.2f}.",
                    "data": rows}

        if intent == "monthly_trend":
            rows = _rows(conn, f"""
                SELECT substr(order_date, 1, 7) AS month,
                       ROUND(SUM(quantity * unit_price - discount_amount), 2) AS revenue,
                       COUNT(*) AS transaction_count
                FROM sales WHERE {VALID_REVENUE}
                GROUP BY substr(order_date, 1, 7) ORDER BY month
            """)
            return {"intent": intent, "answer": "Monthly revenue trend (YYYY-MM).", "data": rows}

        if intent == "top_region":
            rows = _rows(conn, f"""
                SELECT region,
                       ROUND(SUM(quantity * unit_price - discount_amount), 2) AS revenue,
                       SUM(quantity) AS units_sold
                FROM sales WHERE {VALID_REVENUE}
                GROUP BY region ORDER BY revenue DESC, region ASC LIMIT 1
            """)
            if not rows:
                return {"intent": intent, "answer": "No eligible sales records were found.", "data": []}
            return {"intent": intent, "answer": f"{rows[0]['region']} generated the highest sales revenue: {rows[0]['revenue']:.2f}.",
                    "data": rows}

        if intent == "compare_months":
            month1 = _normalize_month(params.get("month1"))
            month2 = _normalize_month(params.get("month2"))
            if not month1 or not month2:
                return {"intent": intent, "answer": "Please provide two months in YYYY-MM format, for example: compare revenue between 2026-01 and 2026-02.", "data": []}
            rows = _rows(conn, f"""
                SELECT substr(order_date, 1, 7) AS month,
                       ROUND(SUM(quantity * unit_price - discount_amount), 2) AS revenue
                FROM sales WHERE {VALID_REVENUE}
                  AND substr(order_date, 1, 7) IN (?, ?)
                GROUP BY substr(order_date, 1, 7) ORDER BY month
            """, (month1, month2))
            revenue = {r["month"]: r["revenue"] or 0 for r in rows}
            a, b = revenue.get(month1, 0), revenue.get(month2, 0)
            change = round(b - a, 2)
            pct = round((change / a) * 100, 2) if a else None
            result = {"month1": month1, "revenue1": a, "month2": month2, "revenue2": b,
                      "absolute_change": change, "percentage_change": pct}
            if change > 0:
                summary = f"Revenue increased by {change:.2f} from {month1} to {month2}."
            elif change < 0:
                summary = f"Revenue decreased by {abs(change):.2f} from {month1} to {month2}."
            else:
                summary = f"Revenue was unchanged between {month1} and {month2}."
            return {"intent": intent, "answer": summary, "data": [result]}

        if intent == "help":
            return {"intent": intent, "answer": "Try asking about total revenue, top product, monthly trend, top region, or compare revenue between YYYY-MM and YYYY-MM.", "data": []}

        raise ValueError("Unsupported analytics intent")

def _normalize_month(value):
    if not isinstance(value, str):
        return None
    value = value.strip()
    if len(value) == 7 and value[4] == "-" and value[:4].isdigit() and value[5:].isdigit():
        month_num = int(value[5:])
        if 1 <= month_num <= 12:
            return value
    return None
