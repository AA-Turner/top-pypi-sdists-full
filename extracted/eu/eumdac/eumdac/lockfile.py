"""Lockfile implementation mindful of OS specifics."""

import sys

from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from threading import Lock
from time import sleep
from typing import Generator, IO, Optional

if sys.platform == "win32":
    import msvcrt
else:
    import fcntl


@contextmanager
def open_locked(
    lockfile_path: Path,
    timeout: Optional[timedelta] = None,
    delete: Optional[bool] = False,
) -> Generator[Optional[IO[str]], None, None]:
    """Open a file, locking it."""
    with open_locked.lock:  # type: ignore
        try:
            open_locked.locks  # type: ignore
        except AttributeError:
            open_locked.locks = {}  # type: ignore

        # create one lock object per file
        if lockfile_path not in open_locked.locks:  # type: ignore
            open_locked.locks[lockfile_path] = Lock()  # type: ignore
        lock = open_locked.locks[lockfile_path]  # type: ignore

    start = datetime.now()

    lockfile_path.parent.mkdir(exist_ok=True, parents=True)
    if timeout:
        r = lock.acquire(timeout=timeout.total_seconds())
    else:
        r = lock.acquire()
    if not r:
        yield None
    else:
        while True:
            if timeout and datetime.now() - start >= timeout:
                lockfile = None
                break

            lockfile = open(lockfile_path, "w")

            if sys.platform == "win32":
                try:
                    msvcrt.locking(lockfile.fileno(), msvcrt.LK_NBLCK, 1)
                    break
                except OSError:
                    sleep(0.1)
                    continue
            else:
                try:
                    fcntl.flock(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except IOError:
                    sleep(0.1)
                    continue

        yield lockfile

        if lockfile:
            if sys.platform == "win32":
                msvcrt.locking(lockfile.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(lockfile, fcntl.LOCK_UN)
            lockfile.close()

            if delete:
                if sys.version_info >= (3, 8):
                    lockfile_path.unlink(missing_ok=False)
                else:
                    lockfile_path.unlink()
        lock.release()


setattr(open_locked, "lock", Lock())
