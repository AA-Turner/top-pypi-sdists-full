"""
Lightweight entry point for auto-emit subprocess.

This module is the dedicated entry point for auto-emit, designed to be
imported with minimal overhead (~6ms). It avoids importing heavy dependencies
like httpx, click, and django that the main CLI loads.

Usage: python -m kolo._emit_auto

Called by _spawn_auto_emit() in core.py after each trace is saved.
"""

from __future__ import annotations

import logging
import os
import shutil
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

logger = logging.getLogger("kolo")

# PID-reuse / Windows backstop for the single-flight lock (1 hour). A live
# holder is never reclaimed (see _lock_holder_alive), so this only kicks in to
# break a lock whose recorded PID we can't trust: it has been recycled to an
# unrelated process, or we're on a platform without a cheap liveness check.
LOCK_TIMEOUT_SECONDS = 3600

# Marker file dropped into a trace directory when it is emitted outside of
# auto-emit (e.g. via `kolo trace emit`). The file contents are a decimal
# Unix timestamp. Directories whose marker is within MANUAL_EMIT_GRACE_SECONDS
# are preserved by auto-emit cleanup even if the trace is no longer in the
# latest-N window.
MANUAL_EMIT_MARKER_NAME = ".manual_emit"
MANUAL_EMIT_GRACE_SECONDS = 24 * 3600


def write_manual_emit_marker(trace_dir: Path, now: float | None = None) -> None:
    """Mark ``trace_dir`` as manually emitted so auto-emit cleanup preserves it.

    Writes a current Unix timestamp to ``{trace_dir}/.manual_emit``. Silent on
    I/O errors - marking is best-effort.
    """
    if now is None:
        now = time.time()
    try:
        (trace_dir / MANUAL_EMIT_MARKER_NAME).write_text(f"{now:.6f}")
    except OSError:  # pragma: no cover
        pass


def has_fresh_manual_emit_marker(
    trace_dir: Path,
    grace_seconds: float = MANUAL_EMIT_GRACE_SECONDS,
    now: float | None = None,
) -> bool:
    """Return True if ``trace_dir`` has a manual-emit marker within the grace window.

    A missing or unreadable marker returns False. A marker file whose contents
    are not a valid timestamp is treated as stale (returns False) so that a
    corrupt marker doesn't pin a directory forever.
    """
    marker = trace_dir / MANUAL_EMIT_MARKER_NAME
    try:
        raw = marker.read_text().strip()
    except OSError:
        return False
    try:
        marked_at = float(raw)
    except ValueError:
        return False
    if now is None:
        now = time.time()
    return (now - marked_at) < grace_seconds


def _lock_holder_alive(lock_path: Path) -> bool:
    """Return True iff ``lock_path`` exists and its recorded PID is a live process.

    This is the staleness predicate for the single-flight lock: a live holder
    must never be reclaimed (otherwise a slow-but-alive run -- e.g. a multi-minute
    migration on a large store -- loses its lock and a second emit piles on),
    while a dead/crashed holder is reclaimable immediately.

    Liveness uses POSIX ``os.kill(pid, 0)`` (ProcessLookupError => dead;
    PermissionError => alive, owned by another user). Windows has no cheap
    portable equivalent, so there we fall back to an age check: a lock younger
    than ``LOCK_TIMEOUT_SECONDS`` is assumed alive. ``LOCK_TIMEOUT_SECONDS`` is
    also a backstop everywhere against PID reuse -- a lock older than it is
    always reclaimable regardless of whether that PID now belongs to some
    unrelated process. A missing file or an unreadable/corrupt PID counts as not
    held (reclaimable).
    """
    try:
        mtime = lock_path.stat().st_mtime
    except OSError:
        return False  # No lock file => nothing held.

    if (time.time() - mtime) >= LOCK_TIMEOUT_SECONDS:
        return False  # Past the backstop: PID is no longer trustworthy.

    if sys.platform == "win32":  # pragma: no cover
        # No cheap portable os.kill(pid, 0); a recent lock is assumed alive.
        return True

    try:
        pid = int(lock_path.read_text().strip())
    except (OSError, ValueError):
        return False  # Corrupt/unreadable PID => can't prove a live holder.
    if pid <= 0:
        return False

    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False  # No such process => holder is dead.
    except PermissionError:
        return True  # Process exists (owned by another user) => alive.
    except OSError:  # pragma: no cover
        return False
    return True


@contextmanager
def _migration_lock(lock_path: Path) -> Iterator[bool]:
    """
    Context manager for acquiring a non-blocking file-based single-flight lock.

    Yields True if lock was acquired, False otherwise.
    Uses O_CREAT | O_EXCL for atomic lock creation to avoid TOCTOU races.
    Automatically releases the lock when the context exits. A lock whose holder
    is no longer alive (see ``_lock_holder_alive``) is reclaimed; a lock held by
    a live process is left alone (we yield False).
    """
    acquired = False

    # If a live holder already holds the lock, don't pile on.
    if _lock_holder_alive(lock_path):
        yield False
        return

    # No live holder: reclaim any leftover lock file (crashed holder, corrupt
    # PID, or past the backstop) before atomically re-creating it below.
    try:
        lock_path.unlink(missing_ok=True)
    except OSError:  # pragma: no cover
        pass  # Race condition, let the next step handle it

    # Atomically create lock file - O_EXCL fails if file exists
    fd = None
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        try:
            os.write(fd, str(os.getpid()).encode())
        finally:
            # Ensure we close the FD even if write fails (fixes FD leak)
            os.close(fd)
        acquired = True
        yield True
    except (FileExistsError, OSError):  # pragma: no cover
        yield False
    finally:
        # Release lock if we acquired it
        if acquired:
            try:
                lock_path.unlink(missing_ok=True)
            except OSError:  # pragma: no cover
                pass


def auto_emit(keep_count: int = 5, db_path: Path | None = None) -> None:
    """
    Auto-emit the latest traces and cleanup old directories.

    This is called after saving a trace.
    It reconciles the emitted directories so the latest `keep_count`
    traces exist on disk and older directories are removed.

    Also runs migration from database to file-based storage if needed,
    protected by a lock to prevent concurrent migrations.

    Single-flight: at most one auto-emit runs per store at a time. The
    reconcile is idempotent and convergent, so if another emit already holds
    the lock this spawn's work is already covered and we exit immediately
    rather than pile on. This bounds concurrency at 1 regardless of how many
    processes spawn us, which matters under KOLO=1 fan-out where every
    short-lived subprocess spawns its own detached emit (the incident that
    drove 265 concurrent emits and load avg 220). Staleness keys off holder
    liveness (see ``_lock_holder_alive``): a crashed holder is reclaimed
    immediately via its PID, while a slow-but-alive run (e.g. a long migration)
    is never evicted.
    """
    from .db import setup_db

    if db_path is None:
        db_path = setup_db()

    emit_lock = db_path.parent / "emit.lock"
    with _migration_lock(emit_lock) as acquired:
        if not acquired:
            logger.debug("Skipping auto-emit: another emit is already in flight")
            return
        _auto_emit_locked(keep_count, db_path)


def _auto_emit_locked(keep_count: int, db_path: Path) -> None:
    """Run the auto-emit reconcile body while holding the single-flight lock."""
    # Lazy imports to minimize startup time
    from .db import (
        TraceNotFoundError,
        list_traces_from_db,
        load_trace_from_db,
    )
    from .emit import emit_trace
    from .trace_container import load_trace
    from .trace import Trace

    # db_path is .kolo/.internal/db.sqlite3, traces are in .kolo/traces
    kolo_dir = db_path.parent.parent
    traces_dir = kolo_dir / "traces"

    # Get the latest N trace IDs from the database
    traces = list_traces_from_db(db_path, count=keep_count)
    if not traces:
        return

    traces_dir.mkdir(exist_ok=True)
    latest_trace_ids = {row[0] for row in traces}

    # Find existing emitted directories by looking for trace ID files inside them
    # Each emitted directory contains a {trace_id}.txt file
    existing_dirs: dict[str, Path] = {}
    for entry in traces_dir.iterdir():
        if entry.is_dir():
            # Look for a trc_*.txt file to identify the trace
            for file in entry.iterdir():
                if file.name.startswith("trc_") and file.name.endswith(".txt"):
                    trace_id = file.stem  # Remove .txt extension
                    existing_dirs[trace_id] = entry
                    break

    # Delete directories for traces not in latest N, but preserve any that
    # carry a fresh manual-emit marker so users/agents inspecting specific
    # traces aren't surprised by them disappearing under them.
    now = time.time()
    for trace_id, dir_path in existing_dirs.items():
        if trace_id in latest_trace_ids:
            continue
        if has_fresh_manual_emit_marker(dir_path, now=now):
            continue
        try:
            shutil.rmtree(dir_path)
        except OSError:  # pragma: no cover
            pass  # Silent failure - this runs in background

    # Fill in any missing emitted directories within the desired latest-N set.
    # Iterate oldest->newest so newly created directory mtimes preserve recency.
    for row in reversed(traces):
        trace_id = row[0]
        if trace_id in existing_dirs:
            continue
        try:
            msgpack_data, _ = load_trace_from_db(db_path, trace_id)
            data = load_trace(msgpack_data)
            trace = Trace(unprocessed_data=data, size=len(msgpack_data))
            emit_trace(trace, traces_dir)
        except TraceNotFoundError:
            logger.debug("Skipping disappeared trace during auto-emit: %s", trace_id)
        except (OSError, KeyError, ValueError):  # pragma: no cover
            pass  # Silent failure - this runs in background

    # Update the kolo.txt file
    try:
        from ._kolotxt import update_kolotxt

        update_kolotxt(db_path)
    except Exception:
        logger.debug("Failed to update kolo.txt", exc_info=True)

    # Run migration if needed, protected by lock
    _run_migration_if_needed(db_path)


def _run_migration_if_needed(db_path: Path) -> None:
    """
    Run migration from database to file-based storage if needed.

    Uses a lock file to prevent concurrent migrations from racing on the
    same database. Since this runs in the same subprocess as auto_emit,
    we avoid the overhead of spawning another Python process.

    Note: We don't vacuum automatically because VACUUM blocks writes and can
    take a long time for large databases. Users can run `kolo delete --vacuum`
    manually to reclaim disk space.
    """
    from .db import migrate_traces_to_files, migration_pending

    # Quick check before acquiring lock. migration_pending() is SQLite-only and
    # never enumerates the raw/ directory, so this stays cheap even when the
    # store holds millions of files (the old get_migration_status() globbed
    # raw/ on every call, which is what melted the host under KOLO=1 fan-out).
    try:
        if not migration_pending(db_path):
            return
    except Exception:  # pragma: no cover
        return

    lock_path = db_path.parent / "migrate.lock"

    with _migration_lock(lock_path) as acquired:
        if not acquired:
            logger.debug("Skipping migration: another migration is already running")
            return

        try:
            # Re-check inside lock in case another process just finished
            if migration_pending(db_path):
                migrate_traces_to_files(db_path)
        except Exception as e:  # pragma: no cover
            logger.debug(f"Auto-migration failed: {e}")


if __name__ == "__main__":  # pragma: no cover
    auto_emit()
