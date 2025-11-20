"""
Scoring logic for the Application Command Centre.

This module contains:
- requirements_score: how well you match the role (0–100)
- progression_probability: chance of progressing to the next stage (0–100)

The formulas are deliberately simple and transparent – this is NOT real
machine learning. It's a clean, realistic early-career scoring model.
"""

from __future__ import annotations

from typing import Dict


def requirements_score(row: Dict[str, object]) -> float:
    """
    Convert requirements_match (0–1) into a 0–100 score.
    """
    raw = float(row["requirements_match"])
    return round(raw * 100, 1)


def progression_probability(row: Dict[str, object]) -> float:
    """
    Estimate probability (0–100) of progressing to the next stage.

    Uses:
    - requirements_match       (0–1, higher is better)
    - competition_level        (1–5, higher is more competitive)
    - prep_hours               (0–10+, more prep helps slightly)

    The output is clamped between 5% and 95% so nothing looks guaranteed.
    """
    req = float(row["requirements_match"])           # 0–1
    competition = float(row["competition_level"])    # 1–5
    prep = float(row["prep_hours"])                  # hours

    # Base from requirements match (centre around 50%)
    base = 0.35 + 0.45 * (req - 0.5) * 2

    # Competition: each step above 3 reduces a bit, below 3 helps a bit
    competition_adjust = -(competition - 3) * 0.04
    base += competition_adjust

    # Preparation: mild positive effect, capped
    prep_boost = min(prep, 8) * 0.015
    base += prep_boost

    # Clamp to [0.05, 0.95]
    prob = max(0.05, min(0.95, base))

    return round(prob * 100, 1)
