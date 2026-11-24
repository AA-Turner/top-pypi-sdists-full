"""This provider call's thinking time, from its reasoning-start frame to its stop (or to now).

A model that HIDES its reasoning streams a 'started' signal and then nothing: the time is the only
evidence of how much it thought. matrx-ai's stopped-call estimator reads it (``get_turn_thinking_ms``)
to bill a call stopped mid-thought. Reset with the turn text before each model call, so time before the
provider began is never counted.
"""

from __future__ import annotations

import time


class TurnThinkingClock:
    __slots__ = ("_open_at", "_ms")

    def __init__(self) -> None:
        self._open_at: float | None = None
        self._ms = 0.0

    def reset(self) -> None:
        self._open_at = None
        self._ms = 0.0

    def signal(self, state: str) -> None:
        now = time.monotonic()
        if state == "started":
            if self._open_at is None:
                self._open_at = now
        elif self._open_at is not None:
            self._ms += (now - self._open_at) * 1000
            self._open_at = None

    def elapsed_ms(self) -> int:
        total = self._ms
        if self._open_at is not None:
            total += (time.monotonic() - self._open_at) * 1000
        return round(total)


def turn_thinking_clock(emitter: object) -> TurnThinkingClock:
    """The emitter's clock, made on first use (emitters built without ``__init__`` still get one)."""
    clock = getattr(emitter, "_turn_thinking_clock", None)
    if clock is None:
        clock = TurnThinkingClock()
        setattr(emitter, "_turn_thinking_clock", clock)
    return clock
