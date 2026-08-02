# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Shared utilities for collecting and reporting stress test metrics."""

from __future__ import annotations

import json
import logging
import os
import statistics
from dataclasses import asdict, dataclass, field
from typing import Any

import pytest

_LOG = logging.getLogger(__name__)

# Cap the maximum scale point for resource-constrained CI environments.
STRESS_MAX_SCALE = int(os.environ.get("STRESS_MAX_SCALE", "2000"))

# Default scale sweep used across stress tests.
DEFAULT_SCALE_SWEEP = [100, 200, 400, 800, 1200, 1600, 2000]


def scale_sweep(sweep: list[int] | None = None) -> list[int]:
    """Return the scale sweep capped by ``STRESS_MAX_SCALE``."""
    return [s for s in (sweep or DEFAULT_SCALE_SWEEP) if s <= STRESS_MAX_SCALE]


# Default threshold: scale points at or above this are exploratory.
_EXPLORE_THRESHOLD = int(os.environ.get("STRESS_EXPLORE_THRESHOLD", "800"))

_explore_marks = [
    pytest.mark.stress_explore,
    pytest.mark.xfail(strict=False, reason="explore: probing for scale limits"),
]


def scale_params(
    sweep: list[int] | None = None,
    *,
    id_prefix: str = "scale",
    explore_threshold: int | None = None,
) -> list[Any]:
    """Build ``pytest.param`` list with ``stress_explore`` on high scales.

    Scale points below *explore_threshold* are regression tests (expected
    to pass).  Points at or above are marked ``stress_explore`` so they
    run in a separate CI job with longer timeouts and soft assertions.
    """
    threshold = (
        explore_threshold if explore_threshold is not None else _EXPLORE_THRESHOLD
    )
    params: list[Any] = []
    # When an explicit sweep is provided, use it as-is (caller controls
    # the values).  Only apply the STRESS_MAX_SCALE cap for the default sweep.
    points = sweep if sweep is not None else scale_sweep()
    for s in points:
        p = pytest.param(s, id=f"{id_prefix}-{s}")
        if s >= threshold:
            p = pytest.param(s, id=f"{id_prefix}-{s}", marks=_explore_marks)
        params.append(p)
    return params


@dataclass(slots=True)
class StressResult:
    """Standard result container for a single stress-test scale point."""

    scale: int
    throughput: float  # ops/sec
    p50_latency_s: float
    p90_latency_s: float
    p99_latency_s: float
    max_latency_s: float
    error_count: int
    error_rate: float
    elapsed_s: float
    metadata: dict[str, Any] = field(default_factory=dict)


def percentile(values: list[float], pct: float) -> float:
    """Nearest-rank percentile consistent with existing stress tests."""
    if not values:
        return 0.0
    k = max(0, min(len(values) - 1, int(round((pct / 100.0) * (len(values) - 1)))))
    return sorted(values)[k]


def latency_stats(latencies: list[float]) -> dict[str, float]:
    """Compute p50/p90/p99/max from a list of latency samples."""
    return {
        "p50": statistics.median(latencies) if latencies else 0.0,
        "p90": percentile(latencies, 90.0),
        "p99": percentile(latencies, 99.0),
        "max": max(latencies) if latencies else 0.0,
    }


def make_result(
    *,
    scale: int,
    latencies: list[float],
    error_count: int,
    elapsed_s: float,
    metadata: dict[str, Any] | None = None,
) -> StressResult:
    """Build a ``StressResult`` from raw latency samples."""
    total = len(latencies) + error_count
    stats = latency_stats(latencies)
    return StressResult(
        scale=scale,
        throughput=len(latencies) / elapsed_s if elapsed_s > 0 else 0.0,
        p50_latency_s=stats["p50"],
        p90_latency_s=stats["p90"],
        p99_latency_s=stats["p99"],
        max_latency_s=stats["max"],
        error_count=error_count,
        error_rate=error_count / total if total > 0 else 0.0,
        elapsed_s=elapsed_s,
        metadata=metadata or {},
    )


def log_result(result: StressResult) -> None:
    """Log a stress result at INFO level."""
    _LOG.info(
        "StressResult scale=%d throughput=%.1f ops/s p50=%.3fs p90=%.3fs "
        "p99=%.3fs max=%.3fs errors=%d (%.2f%%) elapsed=%.1fs",
        result.scale,
        result.throughput,
        result.p50_latency_s,
        result.p90_latency_s,
        result.p99_latency_s,
        result.max_latency_s,
        result.error_count,
        result.error_rate * 100,
        result.elapsed_s,
    )


def save_result(result: StressResult, path: str) -> None:
    """Write a stress result to a JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(result), f, indent=2)
    _LOG.info("Saved stress result to %s", path)
