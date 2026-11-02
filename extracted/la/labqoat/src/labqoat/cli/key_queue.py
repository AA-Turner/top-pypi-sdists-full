"""Keys read on a helper thread, so a screen can keep moving while it waits for one."""

from __future__ import annotations

import queue
import threading
from collections.abc import Callable

import click


class KeyQueue:
    """Hand over each key as it arrives, or nothing when none came in time."""

    LEAVING = ("q", "Q", "\x1b", "\x03", "\x04", "")

    def __init__(self, getchar: Callable[[], str] = click.getchar) -> None:
        """Hold the blocking reader and the keys it has produced."""
        self.getchar = getchar
        self.keys: queue.Queue[str] = queue.Queue()

    def start(self) -> None:
        """Begin reading; the thread ends by itself on a leaving key, which also restores the terminal."""
        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self) -> None:
        """Queue keys until one of them means leave, so no read is left holding the terminal."""
        while True:
            pressed = self.read()
            self.keys.put(pressed)
            if pressed in self.LEAVING:
                return

    def read(self) -> str:
        """One key; an interrupted or closed keyboard counts as leaving."""
        try:
            return self.getchar()
        except (KeyboardInterrupt, EOFError, click.Abort):
            return "q"

    def next(self, timeout: float) -> str | None:
        """The next key, or nothing when none arrives within the timeout."""
        try:
            return self.keys.get(timeout=timeout)
        except queue.Empty:
            return None
