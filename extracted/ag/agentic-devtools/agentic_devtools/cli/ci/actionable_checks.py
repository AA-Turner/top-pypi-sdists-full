"""Shared actionable check names for CI evaluation."""

from __future__ import annotations

import os

DEFAULT_ACTIONABLE_CHECK_NAMES = frozenset(
    {
        "Run Targeted Checks",
        "Run Smart Module Tests",
        "Workflow Tests",
        "Analyze (python)",
        "Analyze (actions)",
        "CodeQL",
        "Code scanning results / CodeQL",
        "CodeQL / Analyze (actions) (dynamic)",
        "CodeQL / Analyze (python) (dynamic)",
    }
)


def get_actionable_check_names() -> frozenset[str]:
    """Return actionable check names, honoring an optional environment override."""
    configured_names = os.environ.get("AI_PR_LOOP_ACTIONABLE_CHECKS", "")
    if configured_names:
        return frozenset(name.strip() for name in configured_names.split(",") if name.strip())
    return DEFAULT_ACTIONABLE_CHECK_NAMES
