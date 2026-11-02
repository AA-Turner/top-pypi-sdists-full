"""How long a blocking dict or queue call may still wait."""

import time


class WaitDeadline:
    """A caller's timeout, or none, measured on the monotonic clock from when the call began."""

    def __init__(self, timeout: float | None) -> None:
        """Start counting now; ``None`` waits for as long as it takes."""
        if timeout is not None and timeout < 0:
            raise ValueError("A timeout is a number of seconds, zero or more")
        self._end = None if timeout is None else time.monotonic() + timeout

    def remaining(self, limit: float) -> float:
        """Seconds left, at most ``limit``."""
        if self._end is None:
            return limit
        return max(0.0, min(limit, self._end - time.monotonic()))

    def expired(self) -> bool:
        """Whether the caller's timeout has run out."""
        return self._end is not None and time.monotonic() >= self._end
