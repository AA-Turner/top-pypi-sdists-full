"""Process-safe shared leases and exclusive cache publication locks."""

import fcntl
import os
from pathlib import Path


class CacheLock:
    """Coordinate processes through a persistent, non-symlink lock file."""

    def __init__(self, path: Path) -> None:
        """Store the lock location without acquiring filesystem resources."""
        self.path = path
        self._descriptor: int | None = None

    def acquire(self, *, shared: bool = False, blocking: bool = True) -> bool:
        """Acquire or change a lease, returning false for a busy nonblocking lock."""
        if self._descriptor is None:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self._descriptor = os.open(self.path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
        operation = fcntl.LOCK_SH if shared else fcntl.LOCK_EX
        if not blocking:
            operation |= fcntl.LOCK_NB
        try:
            fcntl.flock(self._descriptor, operation)
        except BlockingIOError:
            return False
        return True

    def close(self) -> None:
        """Release the lock without unlinking its shared synchronization identity."""
        if self._descriptor is not None:
            os.close(self._descriptor)
            self._descriptor = None
