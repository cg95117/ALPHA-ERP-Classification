# ==============================================================================
# classify_all.py
# Classifies the test texts and writes the results to results/result.xlsx.
# ==============================================================================
from pathlib import Path

import pandas as pd

from src.classify import classify
from src.load_data import load_test_data

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# The original script used .head(1) as a one-row test run.
# Remove .head(1) to process the complete test worksheet.
test_data = load_test_data()

categories = []
reasons = []

for _, row in test_data.iterrows():
    response, _ = classify(row["Coding_Unit"])
    category = ""
    reason = ""

    for response_line in response.splitlines():
        if response_line.startswith("Category:"):
            category = response_line.replace("Category:", "").strip()
        if response_line.startswith("Reason:"):
            reason = response_line.replace("Reason:", "").strip()

    categories.append(category)
    reasons.append(reason)
    print(row["Nr"], category, row["Coding_Unit"][:60])

test_data["Category_LLM"] = categories
test_data["Reason_LLM"] = reasons

output_file = RESULTS_DIR / "result.xlsx"
test_data.to_excel(output_file, index=False)
print(f"Done: {output_file}")
