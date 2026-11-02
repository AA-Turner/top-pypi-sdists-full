"""Shared result type for concurrent checks."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class _CheckResult:
    """Outcome of a single parallel check."""

    label: str
    passed: bool
    output: str
    duration: float = 0.0
