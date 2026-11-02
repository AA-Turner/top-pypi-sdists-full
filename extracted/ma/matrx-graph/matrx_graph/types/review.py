"""Author review marks — ``data.review`` on a step or a connection (review flags, 0117).

An author marks a step or a connection "review if this runs": the run carries on and
succeeds, but every time the marked step starts an attempt (or the marked connection is
TAKEN — payload delivered, never pruned) the engine raises one review flag through the
one ``workflow.run_log`` writer. Shape: ``{"reason": str, "category": <CATEGORIES>,
"label": optional stable key}``.

Parsing is lenient (validation offers, never blocks): a mark with a non-empty reason is
honored; an unknown category reads as ``other`` and ``validate_definition`` reports it.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from matrx_graph.run_log import CATEGORIES


class ReviewMark(BaseModel):
    """A parsed ``data.review`` author mark."""

    model_config = ConfigDict(frozen=True)

    reason: str
    category: str = "other"
    label: str | None = None


def parse_review_mark(raw: Any) -> ReviewMark | None:
    """``data.review`` → :class:`ReviewMark`, or None when absent / not usable (no reason)."""
    if not isinstance(raw, dict):
        return None
    reason = raw.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        return None
    category = raw.get("category")
    label = raw.get("label")
    return ReviewMark(
        reason=reason.strip(),
        category=category if isinstance(category, str) and category in CATEGORIES else "other",
        label=label.strip() if isinstance(label, str) and label.strip() else None,
    )


__all__ = ["ReviewMark", "parse_review_mark"]
