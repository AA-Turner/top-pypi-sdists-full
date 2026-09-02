"""Cross-process exclusion for AI Watch scans."""

from __future__ import annotations

import errno
import os
import stat
import sys
from pathlib import Path
from typing import NoReturn

import structlog

from runlayer_cli.paths import get_runlayer_dir

if sys.platform == "win32":
    import msvcrt
else:
    import fcntl

logger = structlog.get_logger(__name__)

_LOCK_FILENAME = "aiwatch-scan.lock"
_BUSY_ERRNOS = {errno.EACCES, errno.EAGAIN}
if hasattr(errno, "EDEADLK"):
    _BUSY_ERRNOS.add(errno.EDEADLK)


class ScanRunLockError(RuntimeError):
    """Lock infrastructure failed; callers may log and continue unlocked."""


class ScanRunLock:
    """Owned kernel lock released by :meth:`close`."""

    def __init__(self, fd: int) -> None:
        self._fd = fd
        self._closed = False

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            if sys.platform == "win32":
                os.lseek(self._fd, 0, os.SEEK_SET)
                msvcrt.locking(self._fd, msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(self._fd, fcntl.LOCK_UN)
        except OSError:
            logger.warning("failed to unlock AI Watch scan lock", exc_info=True)
        finally:
            os.close(self._fd)

    def __enter__(self) -> ScanRunLock:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


def _is_busy_error(exc: OSError) -> bool:
    return exc.errno in _BUSY_ERRNOS or getattr(exc, "winerror", None) == 33


def _raise_lock_error(path: Path, operation: str, exc: BaseException) -> NoReturn:
    logger.warning(
        "AI Watch scan lock infrastructure failed",
        operation=operation,
        path=str(path),
        exc_info=True,
    )
    raise ScanRunLockError(f"scan lock {operation} failed for {path}") from exc


def acquire_scan_run_lock(path: Path | None = None) -> ScanRunLock | None:
    """Acquire the per-user scan lock, or return ``None`` when already held.

    The lock file remains on disk permanently: unlinking it while a process owns
    the inode would let a second process lock a replacement inode. Unexpected
    setup/open/lock failures raise :class:`ScanRunLockError`, allowing the scan
    command to distinguish contention from a best-effort fail-open condition.
    """

    lock_path = path if path is not None else get_runlayer_dir() / _LOCK_FILENAME
    try:
        lock_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    except OSError as exc:
        _raise_lock_error(lock_path, "parent setup", exc)

    flags = os.O_CREAT | os.O_RDWR | getattr(os, "O_CLOEXEC", 0)
    if os.name == "posix":
        flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(lock_path, flags, 0o600)
    except OSError as exc:
        _raise_lock_error(lock_path, "open", exc)

    try:
        file_stat = os.fstat(fd)
        if not stat.S_ISREG(file_stat.st_mode):
            raise PermissionError(f"scan lock is not a regular file: {lock_path}")
        if os.name == "posix":
            os.fchmod(fd, 0o600)

        if sys.platform == "win32":
            if file_stat.st_size == 0:
                os.write(fd, b"\0")
            os.lseek(fd, 0, os.SEEK_SET)
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        else:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as exc:
        os.close(fd)
        if _is_busy_error(exc):
            return None
        _raise_lock_error(lock_path, "acquire", exc)
    except BaseException:
        os.close(fd)
        raise

    return ScanRunLock(fd)
