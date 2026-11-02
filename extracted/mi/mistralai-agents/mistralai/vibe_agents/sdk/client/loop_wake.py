"""Wake the event loop on a timer while the program awaits a long wait, so that a stop lands at once.

A notebook's stop (ipykernel's SIGINT handler) queues the cancel with ``call_soon``, which does not
wake the selector: after the signal, the loop goes back to its wait until a timer or I/O wakes it.
A wait on a quiet turn (a model call with no token yet, an open approval) has neither, so the stop
would never land. Each wake runs what was queued.
"""

from __future__ import annotations

import asyncio
import contextlib
from collections.abc import Iterator

__all__ = ["waking"]

# The most a queued stop waits for the loop to run it.
_WAKE_SECONDS = 0.25


@contextlib.contextmanager
def waking(interval: float = _WAKE_SECONDS) -> Iterator[None]:
    """Wake the running event loop every ``interval`` seconds until the block exits."""
    loop = asyncio.get_running_loop()
    timer: asyncio.TimerHandle

    def wake() -> None:
        nonlocal timer
        timer = loop.call_later(interval, wake)

    wake()
    try:
        yield
    finally:
        timer.cancel()
