"""Shared sample shape emitted by every hardware source."""

from __future__ import annotations

from dataclasses import dataclass

# The server's closed declared-agg enum (MetricPointIn.agg). One illegal value 422s the WHOLE batch,
# so every source declaration comes from this set (no 'last': constants reduce exactly under mean;
# headroom wants min). Probed live against prod 2026-08-06.
SERVER_AGGS = frozenset({"mean", "sum", "min", "max", "count"})


@dataclass
class HwSample:
    key: str
    value: float
    coords: dict
    agg: str
    companions: tuple = ()
