"""
Optional safety tools for a policy's own code — the platform enforces no limits of its own.

The worker hands a policy's outputs back untouched (north star 5), so keeping actions inside a robot's limits is the
policy's job, or its client's. These are two such checks, as plain functions to call where the author wants them.

"""
from __future__ import annotations

from typing import Sequence

__all__ = ["clip", "limit_step"]


def clip(values: Sequence[float], bounds: Sequence[tuple[float, float]]) -> list[float]:
    """Each value clipped into its dimension's [low, high]."""
    if len(values) != len(bounds):
        raise ValueError(f"{len(values)} values for {len(bounds)} bounds")
    return [min(max(float(v), lo), hi) for v, (lo, hi) in zip(values, bounds)]


def limit_step(previous: Sequence[float], target: Sequence[float], max_delta: float | Sequence[float]) -> list[float]:
    """`target` moved toward from `previous` by at most `max_delta` per dimension (one number for all, or one each)."""
    if len(previous) != len(target):
        raise ValueError(f"{len(previous)} previous values for {len(target)} targets")
    deltas = [float(max_delta)] * len(target) if isinstance(max_delta, (int, float)) else [float(d) for d in max_delta]
    if len(deltas) != len(target):
        raise ValueError(f"{len(deltas)} max_delta values for {len(target)} dimensions")
    return [p + min(max(float(t) - p, -d), d) for p, t, d in zip(map(float, previous), target, deltas)]
