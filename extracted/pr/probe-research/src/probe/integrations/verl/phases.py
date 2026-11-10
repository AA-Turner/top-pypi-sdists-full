"""verl's own step timers as phase spans: every block `marked_timer` / `simple_timer` times (the source of its
`timing_s/*` metrics, `utils/profiler/performance.py:140-174`) keeps its real start and end, and goes out with the step
its metrics row is logged at. Line refs are `verl-project/verl@b17218ba58a6`. Why: DESIGN.md "Phases"."""

from __future__ import annotations

import functools
import sys
import time
from collections.abc import Callable
from typing import Any

from .._phases import PhaseClock as TimerClock

#: Where verl's timers keep their one timing function: every timer variant calls it by this module's global.
TIMER_MODULE = "verl.utils.profiler.performance"
TIMER_NAME = "_timer"
#: Marks the timer Probe already wrapped (once per process).
WRAPPED_MARK = "__probe_verl_phases__"
#: verl reports each step timer as `timing_s/<name>` (`trainer/ppo/metric_utils.py:644-646`).
TIMING_PREFIX = "timing_s/"
#: Each phase's `attributes.source`.
SOURCE = "verl.marked_timer"


class PhaseClock(TimerClock):
    """verl's timed blocks since the last metrics row, reported as `timing_s/<name>`."""

    def __init__(self) -> None:
        super().__init__(prefix=TIMING_PREFIX, source=SOURCE)


def install_phase_timer(get_clock: Callable[[], PhaseClock | None]) -> bool:
    """Wrap verl's timing function in this process, once: each block it times is told to ``get_clock()``'s clock
    (none: nothing kept). Never imports verl; False when its timer module is not loaded or is already wrapped."""
    module = sys.modules.get(TIMER_MODULE)
    original = getattr(module, TIMER_NAME, None)
    if not callable(original) or getattr(original, WRAPPED_MARK, False):
        return False

    @functools.wraps(original)
    def record_block(name: str, timing_raw: dict[str, float]) -> Any:
        started = time.time()
        yield from original(name, timing_raw)
        try:
            clock = get_clock()
            if clock is not None:
                clock.record(name, started, time.time())
        except Exception:  # noqa: BLE001 -- a phase is never worth a training step
            pass

    setattr(record_block, WRAPPED_MARK, True)
    setattr(module, TIMER_NAME, record_block)
    return True
