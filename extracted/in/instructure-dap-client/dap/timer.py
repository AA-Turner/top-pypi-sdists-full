import logging
import time
from types import TracebackType
from typing import Optional, Type

logger = logging.getLogger("dap")


class TimerError(Exception):
    """An exception used to report errors in use of the `Timer` class."""


class Timer:
    _name: str
    _start_time: Optional[float]

    def __init__(self, name: str) -> None:
        self._name = name
        self._start_time = None

    async def start(self) -> None:
        """Starts a new timer."""

        if self._start_time is not None:
            raise TimerError(f"timer is running; use `stop()` to stop it")

        logger.debug(f"start {self._name}")
        self._start_time = time.perf_counter()

    async def stop(self) -> None:
        """Stops the timer, and reports the elapsed time."""

        if self._start_time is None:
            raise TimerError(f"timer is not running; use `start()` to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        logger.debug(f"{self._name} took {elapsed_time:0.3f}s")

    async def __aenter__(self) -> "Timer":
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.stop()
