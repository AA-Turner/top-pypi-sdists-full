"""Durable-file primitives: atomic replace, directory fsync, cross-process lock, retry, UTC stamp.

Stdlib-only: importing it must never pull in ``httpx``. Why: DESIGN.md (durable.py).
"""

from __future__ import annotations

import ctypes
import json
import os
import random
import shutil
import stat
import sys
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterator

from ..os_backend import os_backend as oscompat


#: First delay and ceiling (s) for every durable retry loop, doubling between. The 5 min ceiling
#: keeps an overnight import retrying unattended without hammering a wedged dependency.
RETRY_BACKOFF = (2.0, 300.0)


def backoff_delays(
    attempts: int | None, backoff: tuple[float, float] = RETRY_BACKOFF
) -> Iterator[float]:
    """The wait before each retry: start, doubling, clamped at the ceiling.

    ``attempts`` is total tries, so this yields one fewer delay ("3 attempts" sleeps twice).
    ``attempts=None`` never runs out: for loops stopped by a clock or an empty queue (the
    outbox worker, the in-process exporter, `Run.finish()`'s deadline loop; plan 0.6), so
    poll rate is one policy. These are the exact steps: a loop that retries a server shared with
    a fleet waits `pick_jittered_wait(step)` and keeps the step for its "at the ceiling" checks.
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


#: The jitter's own generator: `random`'s shared one would shift a training script's seeded
#: stream. OS-seeded, and re-seeded in every forked child so forked ranks do not retry in step.
_JITTER = random.Random()
if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_JITTER.seed)

#: A `Retry-After` is waited out plus up to this fraction of it again: 10k clients told "30 s" in
#: one second come back over 15 s, not in one (infra-capacity I14).
RETRY_AFTER_SPREAD = 0.5


def pick_jittered_wait(step: float) -> float:
    """A wait drawn evenly from ``[0, step]`` ("full jitter"), for a loop that retries one server
    with many others: clients that failed in the same second spread over the whole step instead
    of retrying in it together (infra-capacity I14; the ladder is `backoff_delays`)."""
    return _JITTER.uniform(0.0, max(0.0, float(step)))


def honor_retry_after(delay: float, retry_after: float | None, *, ceiling: float) -> float:
    """The wait before the next try: the backoff ``delay``, or the server's longer
    ``Retry-After`` plus up to `RETRY_AFTER_SPREAD` of it, never past ``ceiling``. Only
    LENGTHENS: "retry in 0 s" cannot make a loop hot, and "retry in a day" cannot park a queue
    past the ceiling.
    """
    wait = max(0.0, float(delay))
    if retry_after is not None and float(retry_after) > wait:
        asked = float(retry_after)
        wait = asked + _JITTER.uniform(0.0, asked * RETRY_AFTER_SPREAD)
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

    The mechanism only: each caller keeps its own budget (memory, ledger, journal), or one
    network blip spends three budgets. ``accept`` judges results that fail without raising
    (an agent turn's ``(None, detail)``, a drain report). ``retry_on`` is empty by default,
    so a programming error raises at once instead of retrying and reading as a timeout.
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


#: `write_text_atomic`'s durability levels: all atomic and safe against a PROCESS crash; they
#: differ only in what survives a MACHINE crash (power loss, panic) inside the commit window.
SYNC_FULL = "full"  #: fsync the file and the directory: the rename itself is durable
SYNC_FILE = "file"  #: fsync the file only: if the rename survives, so do its bytes
SYNC_NONE = "none"  #: no fsync: bookkeeping a later pass rebuilds or tolerates
_SYNC_LEVELS = (SYNC_FULL, SYNC_FILE, SYNC_NONE)


def write_text_atomic(
    path: str | Path,
    text: str,
    *,
    mode: int | None = None,
    sync: str = SYNC_FULL,
    keep_mode: bool = False,
) -> None:
    """Atomically replace ``path`` with ``text``: temp sibling, fsync, ``os.replace``, fsync
    the parent. A crash leaves the old file or the new, never a torn one. The parent must
    exist; ``mode`` (e.g. ``0o600``) or the umask sets the new file's bits.

    ``sync`` trades machine-crash durability for latency (plan 1.3; an fsync is 0.3-0.6 ms
    locally, `Run.log()` used to pay eight): ``"full"`` (default) as above; ``"file"`` skips
    the directory fsync (a power loss may lose the rename, never tear the file); ``"none"``
    skips both, only for bookkeeping a later pass rebuilds or recovers.

    ``keep_mode``: for a user-owned file, keep the replaced file's bits (never
    setuid/setgid/sticky), so umask cannot turn 0600 into 0644. ``mode`` applies when there
    is no file or ``path`` is a symlink. An unstat-able path (a link loop) raises. Best effort
    (a filesystem refusing chmod still gets the write); POSIX only (on Windows the read-only
    bit must not reach the temp).
    """
    if sync not in _SYNC_LEVELS:
        raise ValueError(f"sync must be one of {_SYNC_LEVELS}, not {sync!r}")
    path = Path(path)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    open_mode = 0o666 if mode is None else mode
    kept = None
    if keep_mode and os.name != "nt":
        try:
            existing = os.stat(path)
        except FileNotFoundError:  # no file yet (or a dangling link): `mode` applies
            existing = None
        if existing is not None and not path.is_symlink():
            kept = stat.S_IMODE(existing.st_mode) & 0o777
            open_mode = kept  # never readable more widely than the old file, even briefly
    try:
        descriptor = os.open(
            temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | oscompat.O_BINARY, open_mode
        )
        if kept is not None:
            # On the open descriptor, not the path: a path chmod would follow a
            # link swapped in for the temp. Exact bits, which the umask trimmed.
            try:
                os.fchmod(descriptor, kept)
            except OSError:
                pass
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


def through_symlink(path: str | Path) -> Path:
    """``path``, or the file it links to when ``path`` is a symlink: use before replacing a
    user-owned file, or a dotfiles link (``~/.codex/AGENTS.md`` into a repo) becomes a plain
    file and quietly detaches the machine from that repo.

    A dangling link gives the path it names; a link loop gives ``path``. A target folder
    that cannot take the temp file (a read-only Nix store) gives ``path``: the link is
    replaced rather than nothing written.
    """
    path = Path(path)
    try:
        if not path.is_symlink():
            return path
        target = Path(os.path.realpath(path))
    except OSError:
        return path
    return target if os.access(target.parent, os.W_OK) else path


@contextmanager
def file_lock(path: str | Path) -> Iterator[None]:
    """Serialize a narrow cross-process critical section via an advisory ``flock``.

    A sidecar file; a missing parent is created at the umask, NOT 0o700 (make a private
    one first). NEVER hold it across network I/O: a hung holder blocks every writer.
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
    """Immutable point-in-time snapshot of ``src`` at ``dst``: a copy-on-write clone where the
    filesystem has one, else a byte copy. ``dst`` appears atomically, and later changes to
    ``src`` never alter it.
    """
    src = Path(src)
    dst = Path(dst)
    temporary = dst.with_name(f".{dst.name}.{uuid.uuid4().hex}.tmp")
    try:
        if not try_clone(str(src), str(temporary)):
            shutil.copyfile(src, temporary)
        os.chmod(temporary, mode)
        # fsync so the rename lands on a durable file; Windows flushes only through a WRITABLE
        # descriptor (a read-only one is EBADF).
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
    "RETRY_AFTER_SPREAD",
    "RETRY_BACKOFF",
    "backoff_delays",
    "honor_retry_after",
    "pick_jittered_wait",
    "retry",
    "now_iso",
    "fsync_directory",
    "write_text_atomic",
    "file_lock",
    "read_json",
    "snapshot_file",
    "try_clone",
]
