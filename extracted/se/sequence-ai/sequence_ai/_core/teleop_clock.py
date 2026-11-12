"""
A console's and its robot's clocks, and how late each command and each step reached the other side
. Every time on the wire is
an integer of microseconds since the epoch, each side's own clock (the team's interface, worker 3 to workers 1, 7 and 2,
11-10).

In one sentence: the console asks the robot its time (a tick, carrying when it was sent) → the robot answers at once
with when it got the tick and when it answered (a tock) → of the last ROUNDS rounds the console keeps the one with the
shortest trip, and the robot's clock is the console's plus that round's offset, within half its trip → a command's one
way is when the robot got it, less the offset, less when the console sent it; a step's glass to glass is when the
console handed it on, less when the robot's observe() made it, the offset between.

WHY the shortest trip: a round whose trip was short spent little time queued either way, so the offset it gives is off
by little - NTP's clock filter keeps the same one.


WHY over the path the commands take: through the worker the ticks go the way the commands go, straight to the robot
they go the direct way - the same asymmetry each command meets, so the two paths are measured alike.
"""
from __future__ import annotations

import threading
from collections import deque
from typing import Any, Optional

from .latency_stats import now_us


ROUNDS = 16


TICK_S = 0.5
FIRST_TICKS = 5
FIRST_TICK_S = 0.05


def tock(tick: dict, got_us: int) -> dict:
    """The robot's answer to a console's tick, sent at once: when the tick was sent (`a_us`, the console's clock), when
    the robot got it (`b_us`) and when it answered (`c_us`), both the robot's clock."""
    return {"t": "tock", "a_us": tick.get("a_us"), "b_us": got_us, "c_us": now_us()}


def _micros(value: Any) -> Optional[int]:
    """A time a message carried, in microseconds - None for one that is no integer."""
    return int(value) if isinstance(value, int) and not isinstance(value, bool) else None


class Clock:
    """The robot's clock as a console reads it (module docstring): offset_us (robot's time less the console's) and
    error_us (how far off that may be: half the chosen round's trip) - None until a round came back."""

    def __init__(self) -> None:
        self._lock = threading.Lock()

        self._rounds: deque = deque(maxlen=ROUNDS)
        self.ticks = 0
        self.last_trip_us: Optional[int] = None

    def tick(self) -> dict:
        """A tick to send now: when it was sent, by this console's clock."""
        with self._lock:
            self.ticks += 1
        return {"t": "tick", "a_us": now_us()}

    def due(self) -> float:
        """Seconds until the next tick: FIRST_TICK_S for the first few, TICK_S after."""
        with self._lock:
            return FIRST_TICK_S if self.ticks < FIRST_TICKS else TICK_S

    def tock(self, message: dict, at_us: Optional[int] = None) -> Optional[int]:
        """The robot's tock to one of this console's ticks, come at `at_us`: one round, kept (NTP's offset and delay of
        its four times) - its trip, in microseconds. One whose times do not read is dropped (None)."""
        at_us = now_us() if at_us is None else at_us
        a, b, c = (_micros(message.get(k)) for k in ("a_us", "b_us", "c_us"))
        if a is None or b is None or c is None:
            return None

        trip = (at_us - a) - (c - b)
        if trip < 0:
            return None

        offset = ((b - a) + (c - at_us)) // 2
        with self._lock:
            self._rounds.append((trip, offset))
            self.last_trip_us = trip
        return trip

    @property
    def offset_us(self) -> Optional[int]:
        """The robot's clock less this console's, in microseconds, from the round with the shortest trip; None before
        any."""
        with self._lock:
            return min(self._rounds)[1] if self._rounds else None

    @property
    def error_us(self) -> Optional[int]:
        """How far `offset_us` may be off: half the shortest trip; None before any round."""
        with self._lock:
            return min(self._rounds)[0] // 2 if self._rounds else None
