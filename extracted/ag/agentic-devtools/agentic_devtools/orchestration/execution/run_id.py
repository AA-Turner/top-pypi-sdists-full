"""Validation helpers for orchestration run identifiers."""

from __future__ import annotations

from pathlib import PurePath


def validate_run_id(run_id: str) -> str:
    """Normalize and validate a run identifier used in persistence paths."""
    normalized = str(run_id).strip()
    if not normalized:
        raise ValueError("run_id must be a non-empty run identifier.")
    if "/" in normalized or "\\" in normalized or ":" in normalized:
        raise ValueError("run_id must be a run identifier, not a file path.")
    path = PurePath(normalized)
    if path.is_absolute() or any(part == ".." for part in path.parts):
        raise ValueError("run_id must be a run identifier, not a file path.")
    return normalized
