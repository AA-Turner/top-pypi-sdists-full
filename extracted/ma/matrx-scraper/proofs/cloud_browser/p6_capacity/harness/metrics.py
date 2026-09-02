"""Percentile / series helpers. Phase-0 proof harness (NOT shipped code).

Deliberately stdlib-only: this file has to run unattended on a bare EC2 host and on a
Hostinger VPS with nothing installed but python3.
"""

from __future__ import annotations

import math
from typing import Iterable, Sequence


def percentile(values: Sequence[float], q: float) -> float | None:
    """Nearest-rank percentile. q in 0..100. None for an empty series."""
    if not values:
        return None
    ordered = sorted(values)
    if q <= 0:
        return ordered[0]
    if q >= 100:
        return ordered[-1]
    rank = math.ceil(q / 100.0 * len(ordered))
    return ordered[max(0, rank - 1)]


def stats(values: Iterable[float]) -> dict[str, float | int | None]:
    vals = [float(v) for v in values]
    return {
        "n": len(vals),
        "min": min(vals) if vals else None,
        "p50": percentile(vals, 50),
        "p95": percentile(vals, 95),
        "p99": percentile(vals, 99),
        "max": max(vals) if vals else None,
        "mean": (sum(vals) / len(vals)) if vals else None,
    }


def rate(delta_value: float, delta_seconds: float) -> float:
    if delta_seconds <= 0:
        return 0.0
    return delta_value / delta_seconds
