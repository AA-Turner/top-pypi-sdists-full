from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ExtractedSpan(BaseModel):
    """One extracted span. ``label`` is the GLiNER schema label that matched;
    ``start``/``end`` are character offsets into the input text (``-1`` when the
    API did not return offsets); ``score`` is the confidence in [0, 1] or None."""

    label: str
    text: str
    start: int
    end: int
    score: float | None = None


class SpanExtractionResult(BaseModel):
    """Result of one information-extraction call: the flat span list plus the
    raw provider payload (kept for the eval harness — calibration, debugging)."""

    model: str
    spans: list[ExtractedSpan]
    raw: dict[str, Any] | None = None
