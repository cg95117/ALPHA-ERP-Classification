# ==============================================================================
# alpha_cal.py
# Compares two raters using exact agreement, Jaccard distance and
# Krippendorff's alpha for each of the 20 predefined categories.
# Input: data/ALPHA.xlsx | Output: results/ALPHA_Result_Kripp.xlsx
# ==============================================================================
from pathlib import Path

import krippendorff
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "data" / "ALPHA.xlsx"
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

all_categories = [
    "A", "E", "R", "S", "T", "D", "F", "G", "L", "P",
    "C", "K", "O", "Q", "B", "H", "M", "J", "N", "X",
]


def normalize_categories(value):
    if pd.isna(value):
        return set()
    return set(str(value).replace(" ", "").split(";"))


def jaccard_distance(set1, set2):
    if not set1 and not set2:
        return 0.0
    union = len(set1.union(set2))
    return 1 - (len(set1.intersection(set2)) / union)


def main():
    df = pd.read_excel(INPUT_FILE)
    df["Rater1_set"] = df["Rater1"].apply(normalize_categories)
    df["Rater2_set"] = df["Rater2"].apply(normalize_categories)

    df["is_identical"] = df.apply(
        lambda row: row["Rater1_set"] == row["Rater2_set"], axis=1
    )
    identical_count = int(df["is_identical"].sum())
    different_count = len(df) - identical_count

    df["jaccard_dist"] = df.apply(
        lambda row: jaccard_distance(row["Rater1_set"], row["Rater2_set"]),
        axis=1,
    )
    avg_jaccard_dist = df["jaccard_dist"].mean()

    alpha_results = {}
    for category in all_categories:
        r1_binary = df["Rater1_set"].apply(
            lambda values: 1 if category in values else 0
        ).values
        r2_binary = df["Rater2_set"].apply(
            lambda values: 1 if category in values else 0
        ).values
        reliability_data = np.array([r1_binary, r2_binary])
        try:
            alpha_results[category] = krippendorff.alpha(
                reliability_data=reliability_data,
                level_of_measurement="nominal",
            )
        except Exception:
            alpha_results[category] = 0.0

    print("--- Summary ---")
    print(f"Identical: {identical_count}")
    print(f"Different: {different_count}")
    print(f"Average Jaccard distance: {avg_jaccard_dist:.4f}\\n")
    print("--- Krippendorff's Alpha ---")
    for category, alpha in alpha_results.items():
        print(f"Category {category}: {alpha:.4f}")

    output_file = RESULTS_DIR / "ALPHA_Result_Kripp.xlsx"
    df[["Rater2", "Rater1", "is_identical", "jaccard_dist"]].to_excel(
        output_file, index=False
    )
    print(f"\\nSaved: {output_file}")


if __name__ == "__main__":
    main()
