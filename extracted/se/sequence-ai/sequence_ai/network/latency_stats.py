# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
One connection's metrics, read as one snapshot: counters, gauges, and latencies in microseconds, with each latency's
p50, p95 and p99 over its latest 256 samples.

    from sequence_ai.network.latency_stats import LatencyStats, now_us

    stats = LatencyStats(counters=["sent"], latencies=["round_trip_us"])
    sent = now_us(); ...; stats.since("round_trip_us", sent); stats.count("sent")
    stats.snapshot()

In one sentence: a transport counts what it sent, received and dropped (count), sets current values (gauge), and records
each latency it can measure (sample, or since a timestamp) into that latency's window of the latest 256 → snapshot()
reads them all at once: each counter, each gauge, and per latency its window's n, total, last, mean, max and
nearest-rank p50 / p95 / p99, where a percentile is None until the window holds enough samples for it → reset() clears
the counters and the windows and leaves the gauges.

WHY microseconds, a window of 256 and a snapshot: the design follows LiveKit Portal's metrics (Apache-2.0).
WHY nearest-rank: the result is a value that was measured, never an interpolation between two, and two percentiles are
comparable only if both were computed the same way.
WHY no percentile below its minimum sample count: with fewer than 1/(1-q) samples a q-percentile equals the window's max
(the p99 of 20 samples is the largest of the 20), so p50 needs 2 samples, p95 20 and p99 100; until then it is None, not
a number that looks like a percentile.
Cost: count, gauge and sample each take the lock and do O(1) work (a ring buffer written in place, with its sum
maintained incrementally); only snapshot() sorts, at most 256 numbers per latency.
"""
from __future__ import annotations

import math
import threading
import time
from typing import Dict, Iterable, List, Optional

# How many of the latest samples a latency's percentiles are computed over.
WINDOW = 256
# Each percentile reported, with the samples its window must hold first: ceil(1 / (1 - q)). Below that it is the max.
PERCENTILES = ((50, 2), (95, 20), (99, 100))


def now_us() -> int:
    """The wall clock in whole microseconds: the unit of a timestamp sent to another process or machine, and the clock
    since() measures against."""
    return time.time_ns() // 1000


def nearest_rank(ordered: List[int], q: int) -> Optional[int]:
    """The q-th percentile (q an integer, 0 < q <= 100) of `ordered`, whose values are sorted ascending, by nearest
    rank: the ceil(q/100 * n)-th smallest, computed in integers so that float rounding cannot shift it; None for no
    values. The caller enforces a percentile's minimum sample count (PERCENTILES)."""
    if not ordered:
        return None
    return ordered[max(0, -(-q * len(ordered) // 100) - 1)]


def _microseconds(us) -> int:
    """`us` as whole microseconds. A value that is not a finite number raises: a bad timestamp is a bug in the caller
    that should surface, not a sample to drop silently."""
    # bool is a subclass of int in Python, and never a latency
    if isinstance(us, bool) or not isinstance(us, (int, float)):
        raise TypeError(f"a latency must be a number of microseconds, not {type(us).__name__}")
    # NaN and the infinities would corrupt the window's sum and every later percentile
    if isinstance(us, float) and not math.isfinite(us):
        raise ValueError(f"a latency must be a finite number of microseconds, not {us}")
    return int(round(us))


class _Window:
    """One latency's latest WINDOW samples, each written in place over the oldest, with their sum maintained
    incrementally: adding one is O(1). Guarded by its LatencyStats's lock."""

    __slots__ = ("values", "n", "at", "sum", "last", "total")

    def __init__(self) -> None:
        self.values: List[int] = [0] * WINDOW   # allocated once: a sample overwrites a slot and never appends
        self.clear()

    def clear(self) -> None:
        """Empty the window, as reset() does: the slots remain allocated and their contents no longer count."""
        self.n = 0              # how many of the slots hold a sample (WINDOW once full)
        self.at = 0             # the slot the next sample is written to: the oldest, once full
        self.sum = 0            # the sum of the samples in the window
        self.last: Optional[int] = None
        self.total = 0          # samples since the start or the last reset, including those the window has dropped

    def add(self, us: int) -> None:
        # once full, the oldest sample is subtracted from the sum as the new one takes its slot
        if self.n == WINDOW:
            self.sum -= self.values[self.at]
        else:
            self.n += 1
        self.values[self.at] = us
        self.sum += us
        self.at = self.at + 1 if self.at + 1 < WINDOW else 0
        self.last = us
        self.total += 1

    def read(self) -> dict:
        """The window as snapshot() reports it: n, total, last, mean, max and the percentiles, each None where the
        window holds too few samples. Called under the lock; this is the only place that sorts, at most WINDOW
        numbers."""
        # before the window fills, its samples are the first n slots; once full, all of them
        ordered = sorted(self.values[:self.n])
        out = {"n": self.n, "total": self.total, "last": self.last,
               "mean": round(self.sum / self.n) if self.n else None, "max": ordered[-1] if ordered else None}
        for q, floor in PERCENTILES:
            # below its minimum sample count a percentile would be the window's max: None
            out[f"p{q}"] = nearest_rank(ordered, q) if self.n >= floor else None
        return out


class LatencyStats:
    """
    One connection's metrics (the module's docstring): counters (count), gauges (gauge) and latencies in microseconds
    (sample, since), read together by snapshot() and cleared by reset(). Thread-safe: a transport's loop can write while
    the caller reads. Every call is O(1) except snapshot().

    counters, gauges, latencies   names present from the start: a counter at 0, a gauge and each percentile at None;
                                  any other name is added when it is first used.
    """

    def __init__(self, counters: Iterable[str] = (), gauges: Iterable[str] = (), latencies: Iterable[str] = ()) -> None:
        # one lock for all three: a snapshot never pairs a counter from one instant with a window from the next
        self._lock = threading.Lock()
        self._counters: Dict[str, int] = {name: 0 for name in counters}
        self._gauges: Dict[str, Optional[int]] = {name: None for name in gauges}
        self._windows: Dict[str, _Window] = {name: _Window() for name in latencies}

    def count(self, name: str, n: int = 1) -> None:
        """Add n to the counter `name`: what was sent, received, dropped or expired since the start or reset()."""
        with self._lock:
            self._counters[name] = self._counters.get(name, 0) + n

    def gauge(self, name: str, value: float) -> None:
        """Set the gauge `name` to its current value (a clock offset, a queue depth); None means unknown."""
        with self._lock:
            self._gauges[name] = value

    def sample(self, name: str, us: float) -> None:
        """Record one latency of `name`, in microseconds, in its window of the latest WINDOW samples: O(1). A value that
        is not a finite number raises TypeError or ValueError, and nothing is recorded."""
        value = _microseconds(us)              # checked before the lock: a bad sample changes nothing
        with self._lock:
            self._window(name).add(value)

    def _window(self, name: str) -> _Window:
        """The window of `name`, created on first use. Called under the lock."""
        window = self._windows.get(name)
        if window is None:
            window = self._windows[name] = _Window()
        return window

    def since(self, name: str, stamp_us: float) -> None:
        """Record the latency of `name` from `stamp_us`, a wall-clock timestamp in microseconds (now_us(), or the
        robot's clock with its offset applied), to now."""
        self.sample(name, now_us() - _microseconds(stamp_us))

    def snapshot(self) -> dict:
        """All metrics at one instant, as plain JSON-compatible data that later events do not change: {"counters":
        {name: int}, "gauges": {name: value}, "latency_us": {name: {"n", "total", "last", "mean", "max", "p50", "p95",
        "p99"}}}. "n" is the number of samples in the window and "total" the number since the start or reset(); a
        percentile is None until "n" reaches 2 for p50, 20 for p95 and 100 for p99."""
        with self._lock:
            return {"counters": dict(self._counters), "gauges": dict(self._gauges),
                    "latency_us": {name: window.read() for name, window in self._windows.items()}}

    def reset(self) -> None:
        """Clear the counts: every counter is set to 0 and every window emptied, with their names kept. The gauges are
        left as they are: each is a current value, not a count since a start, and a clock offset set to zero would read
        as a clock that lost its synchronization. LiveKit Portal's reset_metrics() does the same, for the same reason:
        it zeroes its counts and leaves its offset and its synced flag unchanged, as that project's documentation of
        its metrics says (THIRD_PARTY_NOTICES.md names it)."""
        with self._lock:
            for name in self._counters:
                self._counters[name] = 0
            for window in self._windows.values():
                window.clear()
