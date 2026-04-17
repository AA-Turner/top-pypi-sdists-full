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
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

logger = logging.getLogger("kolo")

# Lock file timeout in seconds (1 hour) - if lock is older than this, consider it stale
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


@contextmanager
def _migration_lock(lock_path: Path) -> Iterator[bool]:
    """
    Context manager for acquiring a file-based migration lock.

    Yields True if lock was acquired, False otherwise.
    Uses O_CREAT | O_EXCL for atomic lock creation to avoid TOCTOU races.
    Automatically releases the lock when the context exits.
    """
    acquired = False

    # First, check for and clean up stale locks
    try:
        if lock_path.exists():
            lock_age = time.time() - lock_path.stat().st_mtime
            if lock_age < LOCK_TIMEOUT_SECONDS:
                # Lock is fresh, another migration may be running
                yield False
                return
            # Lock is stale, remove it
            try:
                lock_path.unlink(missing_ok=True)
            except OSError:  # pragma: no cover
                pass  # Race condition, let the next step handle it
    except OSError:  # pragma: no cover
        pass

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
    """
    # Lazy imports to minimize startup time
    from .db import (
        TraceNotFoundError,
        list_traces_from_db,
        load_trace_from_db,
        setup_db,
    )
    from .emit import emit_trace
    from .serialize import load_msgpack
    from .trace import Trace

    if db_path is None:
        db_path = setup_db()
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
            data = load_msgpack(msgpack_data)
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
    from .db import get_migration_status, migrate_traces_to_files

    # Quick check before acquiring lock
    try:
        if get_migration_status(db_path)["needs_migration"] == 0:
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
            if get_migration_status(db_path)["needs_migration"] > 0:
                migrate_traces_to_files(db_path)
        except Exception as e:  # pragma: no cover
            logger.debug(f"Auto-migration failed: {e}")


if __name__ == "__main__":  # pragma: no cover
    auto_emit()
