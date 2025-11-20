"""
Demo script for the Application Command Centre.

Loads the sample applications dataset, applies the scoring logic,
sorts by progression probability, and prints a simple summary table.
"""

import pandas as pd

from engine.scoring import requirements_score, progression_probability
from dashboard.summary import print_summary


def main() -> None:
    df = pd.read_csv("data/applications_sample.csv")

    # Add scores
    df["requirements_score"] = df.apply(requirements_score, axis=1)
    df["progress_probability"] = df.apply(progression_probability, axis=1)

    # Sort strongest applications first
    df_sorted = df.sort_values("progress_probability", ascending=False)

    print_summary(df_sorted)


if __name__ == "__main__":
    main()
