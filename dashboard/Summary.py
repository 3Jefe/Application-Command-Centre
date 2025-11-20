"""
Simple console "dashboard" for the Application Command Centre.

Summarises:
- totals (applications, interviews, offers, rejections)
- average requirements score
- average progression probability
- top applications in a compact table
"""

from __future__ import annotations

import math
from typing import Iterable

import pandas as pd


def _rate_outcome(outcome: str) -> str:
    outcome = outcome.lower()
    if "offer" in outcome:
        return "offer"
    if "reject" in outcome:
        return "rejected"
    if "interview" in outcome:
        return "interview"
    return "other"


def print_summary(df: pd.DataFrame, top_n: int = 5) -> None:
    total = len(df)
    outcome_labels = [_rate_outcome(o) for o in df["outcome"]]

    offers = outcome_labels.count("offer")
    rejections = outcome_labels.count("rejected")
    interviews = outcome_labels.count("interview")

    avg_req = df["requirements_score"].mean()
    avg_prob = df["progress_probability"].mean()

    print("=" * 70)
    print("APPLICATION COMMAND CENTRE – SUMMARY")
    print("=" * 70)
    print(f"Total applications : {total}")
    print(f"Interviews         : {interviews}")
    print(f"Offers             : {offers}")
    print(f"Rejections         : {rejections}")
    print(f"Avg req. score     : {avg_req:5.1f} / 100")
    print(f"Avg prog. prob.    : {avg_prob:5.1f} %")
    print("-" * 70)

    # Show top N applications by probability
    print(f"Top {min(top_n, total)} applications by progression probability:\n")

    cols = [
        "company",
        "role",
        "route",
        "location",
        "requirements_score",
        "progress_probability",
        "stage",
        "outcome",
    ]

    display_df = df[cols].head(top_n).copy()
    display_df["requirements_score"] = display_df["requirements_score"].round(1)
    display_df["progress_probability"] = display_df["progress_probability"].round(1)

    # Nicely formatted table
    print(
        display_df.to_string(
            index=False,
            formatters={
                "requirements_score": "{:5.1f}".format,
                "progress_probability": "{:5.1f}".format,
            },
        )
    )
    print("\nTip: focus first on the applications at the top of this list.")
