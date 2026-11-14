# ==============================================================================
# load_data.py
# Opens data/data.xlsx and prepares the worksheets for the other scripts.
# ==============================================================================
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "data.xlsx"


def load_categories():
    """Load the 20-category system from the Excel workbook."""
    df = pd.read_excel(DATA_FILE, sheet_name="category_system ", header=3)
    df = df.iloc[:, 3:7]
    df.columns = ["Category", "Technology", "Description", "Keywords"]
    df = df.dropna(subset=["Category"])
    df["Category"] = df["Category"].str.strip()
    return df.fillna("")


def load_training_data():
    """Load the human-labelled training examples."""
    df = pd.read_excel(DATA_FILE, sheet_name="training_data")
    df.columns = ["Category", "Reason", "Text", "Source"]
    df = df.dropna(subset=["Text"])
    df["Category"] = df["Category"].str.replace(" ", "", regex=False)
    return df.fillna("")


def load_test_data():
    """Load the unclassified coding units."""
    df = pd.read_excel(DATA_FILE, sheet_name="test_1")
    df.columns = ["Nr", "Coding_Unit"]
    df = df.dropna(subset=["Coding_Unit"])
    return df.fillna("")
