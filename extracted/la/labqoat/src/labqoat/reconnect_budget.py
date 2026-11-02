"""A bound on consecutive failed stream connections that a healthy long wait never exhausts."""

import time


class ReconnectBudget:
    """Count connections that ended early and empty; one that lasted or delivered restores the whole budget."""

    def __init__(self, limit: int, healthy_seconds: float = 30.0) -> None:
        """Allow ``limit`` reconnects in a row after connections that neither lasted nor delivered anything."""
        self.limit = limit
        self.healthy_seconds = healthy_seconds
        self.failures = 0
        self._opened = time.monotonic()

    def opened(self) -> None:
        """Mark the start of a connection attempt."""
        self._opened = time.monotonic()

    def exhausted(self, progressed: bool = False) -> bool:
        """Account for one ended connection and say whether no reconnect remains."""
        if progressed or time.monotonic() - self._opened >= self.healthy_seconds:
            self.failures = 0
            return False
        self.failures += 1
        return self.failures > self.limit

    def delay(self) -> float:
        """Back off exponentially while failures repeat, starting again from the shortest pause after a reset."""
        return float(min(0.1 * 2 ** min(max(self.failures - 1, 0), 6), 5.0))
