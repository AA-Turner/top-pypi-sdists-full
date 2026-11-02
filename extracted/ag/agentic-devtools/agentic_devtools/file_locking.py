"""
Cross-platform file locking utilities.

Provides file locking to prevent race conditions when multiple processes
access the state file concurrently. Uses fcntl on Unix and msvcrt on Windows.
"""

import contextlib
import os
import sys
import time
from collections.abc import Iterator
from os import PathLike
from pathlib import Path
from typing import IO, cast


class FileLockError(Exception):
    """Raised when a file lock cannot be acquired."""

    pass


_RPLUS_REOPEN_MAX_ATTEMPTS = 10


def _lock_file_unix(file_handle: IO, exclusive: bool = True, timeout: float = 5.0) -> None:
    """
    Lock a file on Unix systems using fcntl.

    Args:
        file_handle: Open file handle to lock
        exclusive: If True, acquire exclusive lock; otherwise shared lock
        timeout: Maximum time to wait for lock in seconds

    Raises:
        FileLockError: If lock cannot be acquired within timeout
    """
    import fcntl

    lock_type = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
    start_time = time.time()

    while True:
        try:
            fcntl.flock(file_handle.fileno(), lock_type | fcntl.LOCK_NB)
            return
        except OSError as e:
            if time.time() - start_time > timeout:
                raise FileLockError(f"Could not acquire lock within {timeout}s: {e}") from e
            time.sleep(0.01)  # 10ms retry interval


def _unlock_file_unix(file_handle: IO) -> None:
    """Unlock a file on Unix systems."""
    import fcntl

    fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)


def _lock_file_windows(file_handle: IO, exclusive: bool = True, timeout: float = 5.0) -> None:
    """
    Lock a file on Windows systems using msvcrt.

    Args:
        file_handle: Open file handle to lock
        exclusive: If True, acquire exclusive lock; otherwise shared lock
        timeout: Maximum time to wait for lock in seconds

    Raises:
        FileLockError: If lock cannot be acquired within timeout
    """
    import msvcrt

    start_time = time.time()

    while True:
        try:
            # On Windows, we lock the first byte of the file
            # LK_NBLCK for exclusive, LK_NBRLCK for shared (read-only)
            lock_mode = msvcrt.LK_NBLCK if exclusive else msvcrt.LK_NBRLCK  # type: ignore[attr-defined]
            msvcrt.locking(file_handle.fileno(), lock_mode, 1)  # type: ignore[attr-defined]
            return
        except OSError as e:
            if time.time() - start_time > timeout:
                raise FileLockError(f"Could not acquire lock within {timeout}s: {e}") from e
            time.sleep(0.01)  # 10ms retry interval


def _unlock_file_windows(file_handle: IO) -> None:
    """Unlock a file on Windows systems."""
    import msvcrt

    try:
        msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)  # type: ignore[attr-defined]
    except OSError:
        # Ignore unlock errors - file may already be unlocked
        pass


def lock_file(file_handle: IO, exclusive: bool = True, timeout: float = 5.0) -> None:
    """
    Lock a file handle (cross-platform).

    Args:
        file_handle: Open file handle to lock
        exclusive: If True, acquire exclusive lock; otherwise shared lock
        timeout: Maximum time to wait for lock in seconds

    Raises:
        FileLockError: If lock cannot be acquired within timeout
    """
    if sys.platform == "win32":
        _lock_file_windows(file_handle, exclusive, timeout)
    else:
        _lock_file_unix(file_handle, exclusive, timeout)


def unlock_file(file_handle: IO) -> None:
    """
    Unlock a file handle (cross-platform).

    Args:
        file_handle: Open file handle to unlock
    """
    if sys.platform == "win32":
        _unlock_file_windows(file_handle)
    else:
        _unlock_file_unix(file_handle)


def _open_rplus_fd(path: str | PathLike[str], open_flags: int) -> tuple[int, bool]:
    for _ in range(_RPLUS_REOPEN_MAX_ATTEMPTS):
        try:
            return os.open(path, open_flags | os.O_CREAT | os.O_EXCL, 0o666), True
        except FileExistsError:
            try:
                return os.open(path, open_flags), False
            except FileNotFoundError:
                continue
    raise RuntimeError("could not reopen file after repeated create/delete races")


def _creation_guard_path(path: Path) -> Path:
    return path.with_name(f"{path.name}.create.lock")


@contextlib.contextmanager
def locked_file(
    path: Path,
    mode: str = "r+",
    exclusive: bool = True,
    timeout: float = 5.0,
    encoding: str | None = "utf-8",
    *,
    include_created: bool = False,
) -> Iterator[IO | tuple[IO, bool]]:
    """
    Context manager for accessing a file with locking.

    Usage:
        with locked_file(path, "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(new_data)
            f.truncate()

    Args:
        path: Path to the file
        mode: File open mode (default "r+")
        exclusive: If True, acquire exclusive lock; otherwise shared lock
        timeout: Maximum time to wait for lock in seconds
        encoding: File encoding (None for binary mode)
        include_created: When True, yield a ``(handle, created)`` tuple where
            ``created`` reports whether the underlying ``r+`` open atomically
            created the file. For non-``r+`` modes the flag is always ``False``.

    Yields:
        Locked file handle, or ``(handle, created)`` when ``include_created=True``.

    Raises:
        FileLockError: If lock cannot be acquired within timeout
    """
    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    deadline = time.monotonic() + timeout
    creation_guard: IO | None = None
    if "r" in mode and "+" in mode:
        # Atomically create-if-missing using a single OS call (O_CREAT | O_RDWR),
        # which eliminates the TOCTOU race of the old exists()->write_text() pattern:
        # another process can no longer clobber a just-written file between the
        # existence check and the pre-lock bootstrap write.
        if "b" in mode and encoding is not None:
            raise ValueError("cannot specify encoding when using binary mode")
        try:
            if include_created:
                creation_guard = open(_creation_guard_path(path), "a+", encoding="utf-8")
                lock_file(creation_guard, exclusive=True, timeout=timeout)
            open_flags = os.O_RDWR
            if sys.platform == "win32":
                open_flags |= getattr(os, "O_BINARY", 0)
            raw_fd, created = _open_rplus_fd(str(path), open_flags)
            try:
                if encoding is not None:
                    file_handle = os.fdopen(raw_fd, mode, encoding=encoding)
                else:
                    file_handle = os.fdopen(raw_fd, mode)
            except Exception:
                os.close(raw_fd)
                raise
        except Exception:
            if creation_guard is not None:
                try:
                    unlock_file(creation_guard)
                finally:
                    creation_guard.close()
            raise
    else:
        if encoding is not None:
            file_handle = open(path, mode, encoding=encoding)
        else:
            file_handle = open(path, mode)
        created = False

    remaining = max(0.0, deadline - time.monotonic())
    target_locked = False
    try:
        lock_file(file_handle, exclusive=exclusive, timeout=remaining)
        target_locked = True
    except Exception:
        file_handle.close()
        raise
    finally:
        if creation_guard is not None:
            creation_guard_release_error: Exception | None = None
            try:
                unlock_file(creation_guard)
            except Exception as exc:
                creation_guard_release_error = exc
            try:
                creation_guard.close()
            except Exception as exc:
                if creation_guard_release_error is None:
                    creation_guard_release_error = exc
            if creation_guard_release_error is not None:
                if target_locked:
                    try:
                        unlock_file(file_handle)
                    finally:
                        file_handle.close()
                raise creation_guard_release_error

    try:
        if include_created:
            yield file_handle, created
        else:
            yield file_handle
    finally:
        try:
            unlock_file(file_handle)
        finally:
            file_handle.close()


@contextlib.contextmanager
def locked_state_file(
    path: Path,
    timeout: float = 5.0,
) -> Iterator[IO]:
    """
    Context manager specifically for state file access with exclusive locking.

    Creates the file with empty JSON object if it doesn't exist.

    Args:
        path: Path to the state file
        timeout: Maximum time to wait for lock in seconds

    Yields:
        Locked file handle

    Raises:
        FileLockError: If lock cannot be acquired within timeout
    """
    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Create file if it doesn't exist
    if not path.exists():
        path.write_text("{}", encoding="utf-8")

    with locked_file(path, mode="r+", exclusive=True, timeout=timeout, encoding="utf-8") as f:
        yield cast(IO, f)
