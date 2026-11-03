"""ItemLocks: the Protocol for item locks that survive their file's deletion, plus try-lock and blocking lock built on it."""

from __future__ import annotations
import os
from contextlib import contextmanager
from pathlib import Path

from ....foundation.os_backend import os_backend as oscompat


def _same_file(handle, path: Path) -> bool:
    """The locked handle is still the file at `path`. Item locks are unlinked when an item is
    done; one opened just before that unlink and locked just after is a lock on nothing, while
    the next opener creates a new file. Always true on Windows: a file another handle has open
    cannot be deleted there (see `_retire_lock`), so a held lock is the file at its path."""
    if os.name == "nt":
        return True
    try:
        return os.fstat(handle.fileno()).st_ino == os.stat(path).st_ino
    except FileNotFoundError:
        return False


#: Windows: item locks `_retire_lock` was asked to delete while this process held them,
#: deleted as `_try_lock`/`_item_lock` let go.
_RETIRED_WHILE_HELD: set[str] = set()


def _retire_lock(path: Path) -> None:
    """Delete an item lock this process holds (safe on POSIX: see `_same_file`). Windows
    refuses to delete an open file, so there the delete waits for the release
    (`_release_retired`) and may still fail because another process opened the file to wait
    for it: the safe outcome (that waiter locks the live file, finds the item done, and the
    orphan sweep retires the lock later)."""
    if os.name != "nt":
        path.unlink(missing_ok=True)
        return
    _RETIRED_WHILE_HELD.add(str(path))


def _release_retired(path: Path) -> None:
    """After a lock's handle is closed: the delete `_retire_lock` deferred."""
    if not _RETIRED_WHILE_HELD or str(path) not in _RETIRED_WHILE_HELD:
        return
    _RETIRED_WHILE_HELD.discard(str(path))
    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass  # open elsewhere: the orphan sweep retires it


@contextmanager
def _try_lock(path: Path):
    """Non-blocking flock: yields whether this process now holds it. The kernel drops it if
    the holder dies, so a crashed promoter never wedges an item."""
    handle = open(path, "a+")
    try:
        try:
            oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        except BlockingIOError:
            yield False
            return
        try:
            yield _same_file(handle, path)
        finally:
            oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
    finally:
        handle.close()
        _release_retired(path)


@contextmanager
def _item_lock(path: Path):
    """Blocking flock on an item lock, re-opened until it holds the file actually at `path`
    (see `_same_file`)."""
    while True:
        handle = open(path, "a+")
        oscompat.flock(handle.fileno(), oscompat.LOCK_EX)
        if _same_file(handle, path):
            break
        handle.close()
    try:
        yield
    finally:
        oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
        handle.close()
        _release_retired(path)


def _write_private(path: Path, data: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_BINARY", 0), 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
