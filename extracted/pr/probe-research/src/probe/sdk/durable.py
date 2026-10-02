"""Durable-file primitives shared by the SDK spool and the stack connectors.

Every "capture bytes locally, upload out-of-band" path in this SDK needs the same
four low-level moves: an atomic file replacement that survives a crash, a directory
fsync, an advisory cross-process lock, and one UTC timestamp spelling. They were
copy-pasted into spool, capture, harbor, harbor_export, and miles. This is the one
home.

Deliberately stdlib-only and dependency-free: importing it must never pull in
``httpx`` (see the lazy package init in ``probe/__init__.py``), so a distributed
Miles actor can write metric batches to disk without importing the network stack.

The atomic writer is TEXT-based on purpose. Callers serialize their own way -- a
pretty ``indent=2`` ledger, a compact metric record, a JSONL spool page -- and hand
the finished text here. That keeps the serialization divergence in the callers where
it belongs and leaves this primitive with exactly one meaningful knob: the file
``mode`` (e.g. ``0o600`` for a queue on a shared PVC that carries scrubbed config).
"""

from __future__ import annotations

import ctypes
import json
import os
import shutil
import sys
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterator

from .._shared import oscompat


#: First delay and hard ceiling for every durable retry loop here. Doubling in
#: between. The ceiling is the load-bearing half: five minutes keeps an
#: overnight import retrying without a human awake for it, and keeps a wedged
#: dependency from being hammered while it is down.
RETRY_BACKOFF = (2.0, 300.0)


def backoff_delays(
    attempts: int | None, backoff: tuple[float, float] = RETRY_BACKOFF
) -> Iterator[float]:
    """The wait before each retry: start, doubling, clamped at the ceiling.

    ``attempts`` is total tries, so this yields one fewer delay -- nothing waits
    after the last attempt, which is the off-by-one that makes a "3 attempts"
    loop sleep twice rather than three times.

    ``attempts=None`` never runs out: for a loop whose stop condition is a
    clock or an empty queue rather than a count -- the detached outbox worker,
    the in-process exporter, `Run.finish()`'s deadline loop (plan 0.6). Every
    one of them takes its waits from here, so how often a loop polls is one
    policy, not four.
    """
    start, cap = backoff
    delay = max(0.0, float(start))
    ceiling = max(0.0, float(cap))
    remaining = None if attempts is None else max(0, int(attempts) - 1)
    while remaining is None or remaining > 0:
        yield min(delay, ceiling)
        delay = min(delay * 2, ceiling) if ceiling else delay * 2
        if remaining is not None:
            remaining -= 1


def honor_retry_after(delay: float, retry_after: float | None, *, ceiling: float) -> float:
    """The wait before the next try: the backoff ``delay``, or longer when the
    server's ``Retry-After`` asked for longer -- never past ``ceiling``.

    Only ever LENGTHENS a wait. A server that says "retry in 0 s" does not get
    to turn a backing-off loop into a hot one, and one that says "retry in a
    day" does not get to park a queue past the loop's own ceiling.
    """
    wait = max(0.0, float(delay))
    if retry_after is not None:
        wait = max(wait, float(retry_after))
    return min(wait, max(0.0, float(ceiling)))


def retry(
    fn: Callable[[], Any],
    *,
    attempts: int,
    backoff: tuple[float, float] = RETRY_BACKOFF,
    accept: Callable[[Any], bool] | None = None,
    retry_on: type[BaseException] | tuple[type[BaseException], ...] = (),
    on_retry: Callable[[int, Any], None] | None = None,
    sleep: Callable[[float], None] | None = None,
) -> Any:
    """Call ``fn`` until it succeeds or ``attempts`` is spent. Returns the last result.

    THE MECHANISM ONLY. Every caller keeps its own budget and its own
    persistence: an agent turn counts in memory, a backfill unit counts in its
    ledger, an outbox operation counts in its journal. "How many tries has this
    had" is a fact about the work, not about the loop, and sharing a counter
    between layers is how a single flaky network blip spends three different
    budgets at once.

    ``accept`` exists because not every failure raises -- an agent turn returns
    ``(None, detail)`` and a drain pass returns a report. Without it this could
    only retry exceptions, which is the smaller half of the problem.

    ``retry_on`` is empty by default: a raising ``fn`` propagates on the first
    attempt unless the caller says which exceptions are worth another try. That
    keeps a programming error from being retried three times and reported as a
    timeout.
    """
    total = max(1, int(attempts))
    delays = list(backoff_delays(total, backoff))
    pause = sleep if sleep is not None else time.sleep
    result: Any = None
    for index in range(total):
        failure: BaseException | None = None
        try:
            result = fn()
            if accept is None or accept(result):
                return result
        except retry_on as exc:  # type: ignore[misc]
            failure, result = exc, None
        last = index + 1 >= total
        if on_retry is not None:
            on_retry(index + 1, failure if failure is not None else result)
        if last:
            if failure is not None:
                raise failure
            return result
        if delays[index]:
            pause(delays[index])
    return result


def now_iso() -> str:
    """The single UTC, ISO 8601 timestamp spelling used across durable records."""
    return datetime.now(timezone.utc).isoformat()


def fsync_directory(path: str | Path) -> None:
    """fsync a directory entry so a create/rename survives a crash.

    OSError is swallowed: some network filesystems reject a directory fsync, and a
    file fsync plus an atomic replace is still the strongest guarantee they expose.
    """
    try:
        directory_fd = os.open(path, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except OSError:
        pass


#: `write_text_atomic`'s durability levels. Every level is atomic (a reader
#: sees the old file or the new one) and survives a crash of the PROCESS: the
#: rename is done before the call returns and the kernel keeps the bytes. They
#: differ only in what survives a crash of the MACHINE (power loss, kernel
#: panic) inside the filesystem's commit window.
SYNC_FULL = "full"  #: fsync the file and the directory: the rename itself is durable
SYNC_FILE = "file"  #: fsync the file only: if the rename survives, so do its bytes
SYNC_NONE = "none"  #: no fsync: bookkeeping a later pass rebuilds or tolerates
_SYNC_LEVELS = (SYNC_FULL, SYNC_FILE, SYNC_NONE)


def write_text_atomic(
    path: str | Path, text: str, *, mode: int | None = None, sync: str = SYNC_FULL
) -> None:
    """Atomically replace ``path`` with ``text``.

    Write a temp sibling, fsync it, ``os.replace`` it onto ``path`` (atomic on POSIX),
    then fsync the parent directory. A crash leaves either the old file or the new one,
    never a torn write. ``mode`` (e.g. ``0o600``) is applied to the new file when given;
    ``None`` leaves it to the umask, matching a plain ``open("x")``. The parent
    directory must already exist.

    ``sync`` trades machine-crash durability for latency (plan 1.3): each fsync
    is 0.3-0.6 ms on a local disk, and `Run.log()` used to pay eight.
    ``"full"`` (the default) is the above. ``"file"`` skips the directory
    fsync: a power loss may lose the rename, never leave a torn file.
    ``"none"`` skips both: only for bookkeeping a later pass rebuilds (a status
    count) or recovers (the queue sequence, from the op filenames).
    """
    if sync not in _SYNC_LEVELS:
        raise ValueError(f"sync must be one of {_SYNC_LEVELS}, not {sync!r}")
    path = Path(path)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    open_mode = 0o666 if mode is None else mode
    try:
        descriptor = os.open(
            temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | oscompat.O_BINARY, open_mode
        )
        # newline="": the text's own "\n", on every OS (Windows would write "\r\n").
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
            if sync != SYNC_NONE:
                handle.flush()
                os.fsync(handle.fileno())
        oscompat.replace(temporary, path)
        if sync == SYNC_FULL:
            fsync_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


@contextmanager
def file_lock(path: str | Path) -> Iterator[None]:
    """Serialize a narrow cross-process critical section via an advisory ``flock``.

    The lock is a sidecar file; its parent is created if missing (at the umask
    default, NOT 0o700 -- a caller that needs a private directory must create it
    itself first). NEVER hold it across network I/O -- ``flock`` is released only when
    the holder exits, so a hung holder blocks every other writer indefinitely.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+", encoding="utf-8") as handle:
        oscompat.flock(handle.fileno(), oscompat.LOCK_EX)
        try:
            yield
        finally:
            oscompat.flock(handle.fileno(), oscompat.LOCK_UN)


def read_json(path: str | Path, *, error: type[Exception] = ValueError) -> dict[str, Any]:
    """Read and parse a JSON object from ``path``.

    Raises ``error`` -- the caller's own exception type, e.g. ``HarborExportError`` --
    on missing/unreadable/invalid/non-object content, so folding several readers into
    one never silently changes a caller's ``except`` surface.
    """
    path = Path(path)
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise error(f"invalid JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise error(f"{path} must contain a JSON object")
    return value


def try_clone(src: str, dst: str) -> bool:
    """Filesystem-level clone of ``src`` at ``dst``. True when the platform and
    filesystem support one (APFS clonefile, Linux FICLONE reflink); False means
    the caller must fall back to a byte copy. ``dst`` must not exist."""
    if sys.platform == "darwin":
        try:
            libc = ctypes.CDLL(None, use_errno=True)
            if libc.clonefile(os.fsencode(src), os.fsencode(dst), 0) == 0:
                return True
        except (OSError, AttributeError):
            pass
        return False
    if sys.platform.startswith("linux"):
        import fcntl

        _FICLONE = 0x40049409
        try:
            with open(src, "rb") as source, open(dst, "wb") as target:
                fcntl.ioctl(target.fileno(), _FICLONE, source.fileno())
            return True
        except OSError:
            Path(dst).unlink(missing_ok=True)
            return False
    return False


def snapshot_file(src: str | Path, dst: str | Path, *, mode: int = 0o600) -> None:
    """Immutable point-in-time snapshot of ``src`` at ``dst``.

    The mechanism is an internal detail: a copy-on-write filesystem clone where
    the filesystem offers one (instant, no extra space until the original
    changes), else a streamed byte copy. Either way ``dst`` appears atomically
    (temp sibling + ``os.replace``) and never shares mutable state with ``src``
    through the original path -- overwriting or deleting the original later
    cannot alter the snapshot. Named for what it is FOR, not how it works.
    """
    src = Path(src)
    dst = Path(dst)
    temporary = dst.with_name(f".{dst.name}.{uuid.uuid4().hex}.tmp")
    try:
        if not try_clone(str(src), str(temporary)):
            shutil.copyfile(src, temporary)
        os.chmod(temporary, mode)
        # A clone is a metadata operation and a copy already streamed the bytes;
        # fsync the result so the rename below lands on a durable file. Windows
        # flushes only through a WRITABLE descriptor (a read-only one is EBADF).
        descriptor = os.open(temporary, (os.O_RDWR if os.name == "nt" else os.O_RDONLY) | oscompat.O_BINARY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        oscompat.replace(temporary, dst)
        fsync_directory(dst.parent)
    finally:
        temporary.unlink(missing_ok=True)


__all__ = [
    "RETRY_BACKOFF",
    "backoff_delays",
    "honor_retry_after",
    "retry",
    "now_iso",
    "fsync_directory",
    "write_text_atomic",
    "file_lock",
    "read_json",
    "snapshot_file",
    "try_clone",
]
