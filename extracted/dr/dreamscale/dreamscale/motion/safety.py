"""Safety primitives (spec §8, DoD 3): per-tick step clamp and the e-stop."""

from __future__ import annotations

import math
import threading

from dreamscale.constants import MAX_STEP_DEG


def clamp_step(current: list[float], target: list[float],
               max_step: float = MAX_STEP_DEG) -> list[float]:
    """Clamp (target − current) per joint to ±max_step degrees for ONE tick.

    Hard-fails on non-finite inputs: ``nan < max_step`` is False, so without
    this gate a NaN target silently becomes a sustained +max_step runaway and
    a NaN current propagates NaN straight to the bus. This clamp is the last
    line of defense before hardware — refuse rather than guess.
    """
    if not (math.isfinite(max_step) and max_step > 0):
        raise ValueError(f"max_step must be finite and > 0, got {max_step}")
    if len(current) != len(target):
        raise ValueError(f"joint dim mismatch: {len(current)} vs {len(target)}")
    for name, values in (("current", current), ("target", target)):
        for i, value in enumerate(values):
            if not math.isfinite(value):
                raise ValueError(
                    f"non-finite {name} position at joint {i}: {value}"
                )
    clamped: list[float] = []
    for cur, tgt in zip(current, target, strict=True):  # lengths validated above
        delta = max(-max_step, min(max_step, tgt - cur))
        clamped.append(cur + delta)
    return clamped


class EStop:
    """Latched emergency stop. Thread-safe: triggered from signal handlers or a
    keyboard thread, read by the asyncio control loop every tick."""

    def __init__(self) -> None:
        self._event = threading.Event()
        self._lock = threading.Lock()
        self.reason: str | None = None

    def trigger(self, reason: str) -> None:
        with self._lock:
            if self.reason is None:
                self.reason = reason
        self._event.set()

    def is_set(self) -> bool:
        return self._event.is_set()
