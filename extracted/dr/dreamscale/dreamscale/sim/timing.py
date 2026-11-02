"""Timing contract for MolmoAct2-LIBERO simulation."""

from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from dreamscale.constants import CHUNK_SIZE

LEGACY_LIBERO_CONTROL_HZ = 20
LIBERO_ACTION_HZ = 10
LIBERO_ACTION_DT_S = 1.0 / LIBERO_ACTION_HZ
LIBERO_CHUNK_DURATION_S = CHUNK_SIZE / LIBERO_ACTION_HZ
LIBERO_REPLAN_REMAINING = max(1, CHUNK_SIZE // 2)
REALTIME_DEADLINE_TOLERANCE_MS = 1.0
DEFAULT_SIM_MAX_STEPS = 600


def action_steps_for_legacy_steps(steps: int) -> int:
    """Preserve old 20 Hz episode duration after moving action ticks to 10 Hz."""
    return max(1, round(int(steps) * LIBERO_ACTION_HZ / LEGACY_LIBERO_CONTROL_HZ))


@dataclass(frozen=True)
class RealtimeTick:
    tick: int
    target_ns: int
    actual_ns: int
    slept_s: float
    lateness_ms: float


class RealtimePacer:
    def __init__(
        self,
        *,
        action_hz: int = LIBERO_ACTION_HZ,
        clock: Callable[[], int] = time.monotonic_ns,
    ) -> None:
        if action_hz <= 0:
            raise ValueError("action_hz must be positive")
        self.action_hz = int(action_hz)
        self.dt_ns = int(round(1_000_000_000 / self.action_hz))
        self._clock = clock
        self._start_ns: int | None = None

    @property
    def start_ns(self) -> int | None:
        return self._start_ns

    def start(self, now_ns: int | None = None) -> int:
        self._start_ns = self._clock() if now_ns is None else int(now_ns)
        return self._start_ns

    def target_ns(self, tick: int) -> int:
        if self._start_ns is None:
            raise RuntimeError("real-time pacer has not been started")
        return self._start_ns + int(tick) * self.dt_ns

    async def wait_async(
        self,
        tick: int,
        *,
        sleep: Callable[[float], Awaitable[object]] = asyncio.sleep,
    ) -> RealtimeTick:
        target_ns = self.target_ns(tick)
        now_ns = self._clock()
        slept_s = 0.0
        if now_ns < target_ns:
            slept_s = (target_ns - now_ns) / 1_000_000_000.0
            await sleep(slept_s)
            now_ns = self._clock()
        return self._tick(tick=tick, target_ns=target_ns, actual_ns=now_ns, slept_s=slept_s)

    def wait(
        self,
        tick: int,
        *,
        sleep: Callable[[float], object] = time.sleep,
    ) -> RealtimeTick:
        target_ns = self.target_ns(tick)
        now_ns = self._clock()
        slept_s = 0.0
        if now_ns < target_ns:
            slept_s = (target_ns - now_ns) / 1_000_000_000.0
            sleep(slept_s)
            now_ns = self._clock()
        return self._tick(tick=tick, target_ns=target_ns, actual_ns=now_ns, slept_s=slept_s)

    @staticmethod
    def _tick(*, tick: int, target_ns: int, actual_ns: int, slept_s: float) -> RealtimeTick:
        return RealtimeTick(
            tick=int(tick),
            target_ns=int(target_ns),
            actual_ns=int(actual_ns),
            slept_s=max(0.0, float(slept_s)),
            lateness_ms=max(0.0, (actual_ns - target_ns) / 1_000_000.0),
        )
