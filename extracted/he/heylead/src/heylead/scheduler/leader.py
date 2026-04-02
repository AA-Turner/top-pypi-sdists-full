"""File-based leader election for scheduler singleton.

Ensures only one MCP server process runs the SchedulerEngine.
Other instances serve MCP tools normally but skip the scheduler.

Uses fcntl.flock() (Unix) or msvcrt.locking() (Windows) for a
non-blocking exclusive lock on ~/.heylead/data/scheduler.lock.
The OS automatically releases the lock when the process exits
(even on SIGKILL), so there are no stale lock problems.
"""

from __future__ import annotations

import logging
import os
import sys
from typing import Optional

from .. import config

logger = logging.getLogger(__name__)

_LOCK_FILE = "scheduler.lock"
_lock_fd: Optional[int] = None


def try_acquire_leader() -> bool:
    """Try to become the scheduler leader.

    Returns True if this process acquired the lock (is the leader).
    Returns False if another process holds the lock (follower mode).

    The lock is held until the process exits or release_leader() is called.
    If the leader process crashes, the OS releases the flock automatically.
    """
    global _lock_fd

    lock_path = config._heylead_home() / "data" / _LOCK_FILE
    config.ensure_dirs()

    try:
        fd = os.open(str(lock_path), os.O_RDWR | os.O_CREAT, 0o644)

        if sys.platform == "win32":
            import msvcrt

            try:
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            except OSError:
                os.close(fd)
                logger.info("Another instance is scheduler leader, running as follower")
                return False
        else:
            import fcntl

            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                os.close(fd)
                logger.info("Another instance is scheduler leader, running as follower")
                return False

        # Lock acquired — write PID for debugging
        _lock_fd = fd
        os.ftruncate(fd, 0)
        os.lseek(fd, 0, os.SEEK_SET)
        os.write(fd, f"{os.getpid()}\n".encode())
        os.fsync(fd)
        logger.info("Acquired scheduler leader lock (pid=%d)", os.getpid())
        return True

    except Exception as e:
        logger.warning("Leader election failed, running as follower: %s", e)
        return False


def release_leader() -> None:
    """Release the scheduler leader lock."""
    global _lock_fd

    if _lock_fd is not None:
        try:
            os.close(_lock_fd)  # Closing the fd releases flock automatically
        except OSError:
            pass
        _lock_fd = None
        logger.info("Released scheduler leader lock")
