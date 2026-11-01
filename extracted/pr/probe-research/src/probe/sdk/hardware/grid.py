"""Epoch step grid and window aggregation for the hardware rail.

``step_index = floor(unix_seconds / HW_STEP_SECONDS)`` is a protocol CONSTANT: every writer
(collector, restart, backfill weeks later) derives the same step for the same instant with no
shared state, so the store's first-write-wins identity dedups redelivery and backfill.
Changing HW_STEP_SECONDS is a breaking protocol change, not a knob; finer capture uses the
labeled per-sample rail.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

HW_STEP_SECONDS = 60


def step_for(ts: float) -> int:
    """Epoch grid: the hardware step for a unix timestamp."""
    return int(ts // HW_STEP_SECONDS)


@dataclass
class HwPoint:
    key: str
    coords: dict
    step: int
    value: float
    agg: str = "mean"  # declared reduce, rides onto the wire (0062)


@dataclass
class _Series:
    agg: str
    companions: tuple
    values: list = field(default_factory=list)  # in arrival (ts) order


# The server's declared-agg vocabulary usable as a window reduce. No 'last': not in the server enum.
_REDUCERS = {
    "mean": lambda vs: sum(vs) / len(vs),
    "max": max,
    "min": min,
    "sum": sum,
    "count": len,
}


class WindowAggregator:
    """Accumulates samples, emitting one reduced point per series per completed window. The current
    window is emitted only by `flush_all` at the collector's end: a partial value earlier would be
    frozen forever by first-write-wins."""

    def __init__(self) -> None:
        # step -> (key, coords-items) -> _Series
        self._windows: dict[int, dict[tuple, _Series]] = {}
        self._coords: dict[tuple, dict] = {}

    def add(
        self,
        key: str,
        coords: dict,
        value: float,
        ts: float,
        *,
        agg: str,
        companions: tuple = (),
    ) -> None:
        if not math.isfinite(value):
            return  # non-finite values poison the server-side catalog fold
        ckey = tuple(sorted(coords.items()))
        self._coords[ckey] = coords
        series = self._windows.setdefault(step_for(ts), {}).setdefault(
            (key, ckey), _Series(agg=agg, companions=companions)
        )
        series.values.append(value)

    def flush_completed(self, now: float) -> list[HwPoint]:
        """Emit every window strictly before the one containing ``now``."""
        current = step_for(now)
        return self._flush(lambda step: step < current)

    def flush_all(self) -> list[HwPoint]:
        """Emit every window, the open one included: the collector's LAST pass, at run close. Without it
        a run under a minute recorded no hardware and every run lost its last partial minute
        (environment suite, lane E3)."""
        return self._flush(lambda step: True)

    def _flush(self, due) -> list[HwPoint]:
        points: list[HwPoint] = []
        for step in sorted(s for s in self._windows if due(s)):
            for (key, ckey), series in self._windows.pop(step).items():
                coords = self._coords[ckey]
                points.append(
                    HwPoint(
                        key, coords, step, _REDUCERS[series.agg](series.values), series.agg
                    )
                )
                for comp in series.companions:
                    points.append(
                        HwPoint(
                            f"{key}_{comp}", coords, step, _REDUCERS[comp](series.values), comp
                        )
                    )
        return points
