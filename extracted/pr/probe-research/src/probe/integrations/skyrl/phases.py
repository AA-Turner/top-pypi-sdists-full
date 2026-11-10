"""SkyRL's own step timers as phase spans: every block its `Timer` adds to a step's timings (reported as `timing/<name>`,
`trainer.py:578`, `fully_async_trainer.py:671`) keeps its real start and end, and goes out with the step its metrics row
is logged at. Pure: the caller hands in SkyRL's `Timer`. Line refs are `NovaSky-AI/SkyRL@d87004689e3a`. Why: DESIGN.md."""

from __future__ import annotations

import functools
import time
from collections.abc import Callable
from typing import Any

from .._phases import PhaseClock as TimerClock

#: SkyRL logs each step timer as `timing/<name>`.
TIMING_PREFIX = "timing/"
#: Each phase's `attributes.source`.
SOURCE = "skyrl.Timer"
#: Marks the `Timer` class Probe already wrapped (once per process).
WRAPPED_MARK = "__probe_skyrl_phases__"

_CLOCK: PhaseClock | None = None


class PhaseClock(TimerClock):
    """SkyRL's timed blocks since the last metrics row, reported as `timing/<name>`."""

    def __init__(self) -> None:
        super().__init__(prefix=TIMING_PREFIX, source=SOURCE)


def set_active_clock(clock: PhaseClock | None) -> None:
    """The clock this process's timers report to (None: nothing kept)."""
    global _CLOCK
    _CLOCK = clock


def get_active_clock() -> PhaseClock | None:
    return _CLOCK


def install_phase_timer(timer_class: Any, get_clock: Callable[[], PhaseClock | None] = get_active_clock) -> bool:
    """Wrap ``timer_class``'s exits (`utils/utils.py:53-86`) in this process, once: a block timed into a step's
    timings (its `update_dict`) is told to ``get_clock()``'s clock. The class, not an instance: Python looks a `with`
    block's methods up on the class. False when it is already wrapped."""
    if getattr(timer_class, WRAPPED_MARK, False):
        return False
    original = getattr(timer_class, "__exit__", None)
    if callable(original):

        @functools.wraps(original)
        def record_exit(timer: Any, *exc_info: Any) -> Any:
            result = original(timer, *exc_info)
            _record_block(timer, get_clock)
            return result

        setattr(timer_class, "__exit__", record_exit)
    original_async = getattr(timer_class, "__aexit__", None)
    if callable(original_async):

        @functools.wraps(original_async)
        async def record_async_exit(timer: Any, *exc_info: Any) -> Any:
            result = await original_async(timer, *exc_info)
            _record_block(timer, get_clock)
            return result

        setattr(timer_class, "__aexit__", record_async_exit)
    setattr(timer_class, WRAPPED_MARK, True)
    return True


def _record_block(timer: Any, get_clock: Callable[[], PhaseClock | None]) -> None:
    try:
        clock = get_clock()
        started = getattr(timer, "start_time", None)
        if clock is None or getattr(timer, "update_dict", None) is None or not isinstance(started, (int, float)):
            return
        clock.record(getattr(timer, "message", "timer"), float(started), time.time())
    except Exception:  # noqa: BLE001 -- a phase is never worth a training step
        pass
