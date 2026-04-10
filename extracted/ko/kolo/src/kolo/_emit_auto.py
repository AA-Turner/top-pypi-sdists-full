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


def auto_emit(keep_count: int = 5) -> None:
    """
    Auto-emit the latest traces and cleanup old directories.

    This is called via subprocess from the middleware after saving a trace.
    It keeps only `keep_count` emitted trace directories.

    Also runs migration from database to file-based storage if needed,
    protected by a lock to prevent concurrent migrations.
    """
    # Lazy imports to minimize startup time
    from .db import list_traces_from_db, load_trace_from_db, setup_db
    from .emit import emit_trace
    from .serialize import load_msgpack
    from .trace import Trace

    db_path = setup_db()
    # db_path is .kolo/.internal/db.sqlite3, traces are in .kolo/traces
    kolo_dir = db_path.parent.parent
    traces_dir = kolo_dir / "traces"
    if not traces_dir.exists():
        return

    # Get the latest N trace IDs from the database
    traces = list_traces_from_db(db_path, count=keep_count)
    if not traces:
        return

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

    # Delete directories for traces not in latest N
    for trace_id, dir_path in existing_dirs.items():
        if trace_id not in latest_trace_ids:
            try:
                shutil.rmtree(dir_path)
            except OSError:  # pragma: no cover
                pass  # Silent failure - this runs in background

    # Emit the latest trace if not already emitted
    latest_trace_id = traces[0][0]
    if latest_trace_id not in existing_dirs:
        try:
            msgpack_data, _ = load_trace_from_db(db_path, latest_trace_id)
            data = load_msgpack(msgpack_data)
            trace = Trace(unprocessed_data=data, size=len(msgpack_data))
            emit_trace(trace, traces_dir)
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
