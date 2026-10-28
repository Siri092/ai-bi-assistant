
import sys
from pathlib import Path

# Add the project root to Python's import path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
import database
from database import initialize_database
from analytics import run_analytics
from interpreter import interpret_question


@pytest.fixture(autouse=True)
def fresh_db(tmp_path, monkeypatch):
    # Use the actual supplied CSV, but isolate the SQLite DB per test.
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    initialize_database(database.DATA_PATH)

def test_total_revenue_returns_numeric_answer():
    result = run_analytics("total_revenue")
    assert result["data"][0]["total_revenue"] > 0
    assert result["data"][0]["transaction_count"] > 0

def test_top_product_returns_product():
    result = run_analytics("top_product")
    assert result["data"]
    assert result["data"][0]["product"]

def test_monthly_trend_is_ordered():
    result = run_analytics("monthly_trend")
    months = [row["month"] for row in result["data"]]
    assert months == sorted(months)
    assert len(months) >= 2

def test_top_region_returns_region():
    result = run_analytics("top_region")
    assert result["data"][0]["region"] in {"North", "South", "East", "West"}

def test_compare_months_calculates_change():
    result = run_analytics("compare_months", {"month1": "2026-01", "month2": "2026-02"})
    row = result["data"][0]
    assert row["absolute_change"] == round(row["revenue2"] - row["revenue1"], 2)

def test_invalid_month_is_handled():
    result = run_analytics("compare_months", {"month1": "January", "month2": "2026-02"})
    assert "Please provide two months" in result["answer"]

def test_unknown_question_gets_help():
    result = interpret_question("Tell me a joke about a cat")
    assert result["intent"] == "help"
