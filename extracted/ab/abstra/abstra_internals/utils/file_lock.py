"""Cross-process file locks that work on the editor's shared EFS.

Uses ``fcntl.lockf()`` (POSIX byte-range locks) on POSIX rather than
``flock()``: only POSIX locks are honored by NFSv4/EFS, so this gives reliable
mutual exclusion across the pods (and the linter sidecar child) that share the
web-editor filesystem. On Windows we fall back to the ``filelock`` package.

POSIX locks are owned by the PROCESS, not the fd/thread — two threads in the
same process both "acquire" successfully — so callers that also need
intra-process exclusion must pair this with a ``threading.Lock`` (see
SqlStorage._locked).
"""

import errno
import os
import sys
import time
from contextlib import contextmanager
from typing import Iterator, Optional

from abstra_internals.logger import AbstraLogger

LOCK_TIMEOUT = 30


if sys.platform == "win32":
    from filelock import FileLock
    from filelock import Timeout as _FileLockTimeout

    class _FileLockWrapper:
        def __init__(self, lock_path: str, timeout: float = LOCK_TIMEOUT):
            self._lock = FileLock(lock_path, timeout=timeout)

        def acquire(self) -> None:
            self._lock.acquire()

        def try_acquire(self) -> bool:
            try:
                self._lock.acquire(timeout=0)
                return True
            except _FileLockTimeout:
                return False

        def release(self) -> None:
            self._lock.release()

    def create_file_lock(
        lock_path: str, timeout: float = LOCK_TIMEOUT
    ) -> "_FileLockWrapper":
        return _FileLockWrapper(lock_path, timeout)

else:
    import fcntl

    class _PosixFileLock:
        """Cross-process lock using fcntl.lockf() (POSIX byte-range locks).

        Unlike flock(), POSIX locks are properly supported by NFSv4 and EFS,
        providing reliable mutual exclusion across pods sharing a filesystem.
        """

        def __init__(self, lock_path: str, timeout: float = LOCK_TIMEOUT):
            self._lock_path = lock_path
            self._timeout = timeout
            self._fd: Optional[int] = None

        def _open(self) -> int:
            if self._fd is None:
                self._fd = os.open(self._lock_path, os.O_CREAT | os.O_RDWR)
            return self._fd

        def _close(self) -> None:
            if self._fd is not None:
                os.close(self._fd)
                self._fd = None

        def acquire(self) -> None:
            fd = self._open()
            deadline = time.monotonic() + self._timeout
            while True:
                try:
                    fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    return
                except OSError as e:
                    if e.errno not in (errno.EACCES, errno.EAGAIN):
                        self._close()
                        raise
                    if time.monotonic() >= deadline:
                        self._close()
                        raise TimeoutError(
                            f"Could not acquire lock {self._lock_path} "
                            f"within {self._timeout}s"
                        )
                    time.sleep(0.05)

        def try_acquire(self) -> bool:
            """Attempt to acquire without blocking. Returns False (releasing the
            fd) when another process holds the lock."""
            fd = self._open()
            try:
                fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return True
            except OSError as e:
                if e.errno not in (errno.EACCES, errno.EAGAIN):
                    self._close()
                    raise
                self._close()
                return False

        def release(self) -> None:
            fd = self._fd
            if fd is not None:
                try:
                    fcntl.lockf(fd, fcntl.LOCK_UN)
                finally:
                    self._close()

    def create_file_lock(
        lock_path: str, timeout: float = LOCK_TIMEOUT
    ) -> "_PosixFileLock":
        return _PosixFileLock(lock_path, timeout)


@contextmanager
def try_file_lock(lock_path: str) -> Iterator[bool]:
    """Non-blocking cross-process lock as a context manager.

    Yields True when the lock was acquired (and releases it on exit), or False
    when another process already holds it (nothing to release). The lock is
    also released if the holding process dies, since the OS drops POSIX locks
    on fd close / process exit — so a crashed (or os._exit'd) holder never
    leaves a stale lock behind.
    """
    lock = create_file_lock(lock_path)
    acquired = lock.try_acquire()
    try:
        yield acquired
    finally:
        if acquired:
            try:
                lock.release()
            except OSError as release_error:
                AbstraLogger.capture_exception(release_error)
