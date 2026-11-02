"""
outside.py - what a robot's acts spend outside its worker, which each act tells the worker.

In one sentence: each act its worker answered - its own time (act/policy.py total_ms) less the worker's handler_ms:
the upload, the download, the encoding and decoding here - goes into its connection's window (the latest WINDOW) → each
act on that connection says the window's p90, in whole ms and at most MOST_MS, as the X-Seq-Outside-Ms header → the
worker holds an act for other robots only within what is left of the robot's buffer after that and what its batch takes
in the worker. Before FIRST acts were measured, the most of them and the connection's /ping round trip (ping_ms, its
opening taken out).

WHY the robot says it: its worker cannot see its trip, and the 100 ms the worker took for every robot was a third short
of what robots' acts spent outside it - 41% of their answers came late.

"""
from __future__ import annotations

import math
import threading
from collections import deque
from typing import Optional

HEADER = "X-Seq-Outside-Ms"




LEFT_HEADER = "X-Seq-Chunk-Left-Ms"


WINDOW = 20
FIRST = 3
MOST_MS = 5000


class Window:
    """One connection's acts' time outside its worker, and its /ping's round trip (ping_ms)."""

    def __init__(self) -> None:
        self._ms: deque = deque(maxlen=WINDOW)
        self._lock = threading.Lock()
        self.ping_ms: Optional[float] = None

    def add(self, ms: float) -> None:
        """An act that spent `ms` outside its worker; a number that is no time (negative, NaN) is left out."""
        if isinstance(ms, (int, float)) and not isinstance(ms, bool) and math.isfinite(ms) and ms >= 0:
            with self._lock:
                self._ms.append(float(ms))

    def said(self) -> Optional[int]:
        """What an act tells its worker: the nearest-rank p90 of the window, rounded up - before FIRST acts, the most of
        them and ping_ms - at most MOST_MS; None when nothing is known."""
        with self._lock:
            ms = sorted(self._ms)
        if len(ms) >= FIRST:
            value = ms[min(len(ms) - 1, max(0, math.ceil(0.9 * len(ms)) - 1))]
        else:
            known = ms + ([self.ping_ms] if self.ping_ms is not None else [])
            if not known:
                return None
            value = max(known)
        return min(MOST_MS, int(math.ceil(value)))
