import os
import signal
import sys
from collections import defaultdict
from collections.abc import Callable
from typing import Any, DefaultDict, List, Set, Tuple
from pprint import pformat

from eumdac.logging import logger

__all__ = ["signal_registry"]


class _SignalHandlerRegistry:
    handled_signals: Set[Tuple[int, int]] = set()

    def __init__(self) -> None:
        logger.trace("[SIGNAL] Initializing new registry")
        self._handlers: DefaultDict[int, List[Tuple[int, Callable[[], None]]]] = defaultdict(list)

    def register(self, signum: int, func: Callable) -> None:  # type: ignore
        try:
            signal.signal(signum, self.handler)
        except ValueError:
            pass
        logger.trace(f"[SIGNAL] registering handler for {sig_num_to_name(signum)}: {func}")
        self._handlers[signum].append((os.getpid(), func))

    def unregister(self, signum: int, func: Callable) -> None:  # type: ignore
        try:
            self._handlers[signum].remove((os.getpid(), func))
        except ValueError:
            logger.trace(f"[SIGNAL] failed to remove ({os.getpid()}, {func})")

    def handler(self, signum: int, frame: Any) -> None:
        # Avoid handling multiple times the same signal for the same PID
        if (os.getpid(), signum) in self.handled_signals:
            logger.trace(
                f"[{os.getpid()}][SIGNAL] Not handling signal {sig_num_to_name(signum)} {signum}, already handled"
            )
            return

        self.handled_signals.add((os.getpid(), signum))

        logger.trace(
            f"[{os.getpid()}][SIGNAL] signal handler {self} called because of {sig_num_to_name(signum)} {signum}"
        )
        logger.trace(pformat(self._handlers))
        my_handlers = [h for pid, h in self._handlers[signum] if pid == os.getpid()]
        logger.trace(
            f"[{os.getpid()}][SIGNAL] registry handler {self} because of {sig_num_to_name(signum)} "
        )
        for h in my_handlers:
            logger.trace(f"[{os.getpid()}][SIGNAL] executing {h}")
            h()
            logger.trace(f"[{os.getpid()}][SIGNAL] finished executing {h}")
        logger.trace(f"[{os.getpid()}][SIGNAL] All handlers finished")
        sys.exit(1)


def sig_num_to_name(sig_num: int) -> str:
    """Return the signal name for a given signal number"""
    for name, num in signal.__dict__.items():
        if name.startswith("SIG") and not name.startswith("SIG_"):
            if num == sig_num:
                return name
    return "UNKNOWN (num: {signum})"


signal_registry: _SignalHandlerRegistry = _SignalHandlerRegistry()
