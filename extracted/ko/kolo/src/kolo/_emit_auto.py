"""
Lightweight entry point for auto-emit subprocess.

This module is the dedicated entry point for auto-emit, designed to be
imported with minimal overhead (~6ms). It avoids importing heavy dependencies
like httpx, click, and django that the main CLI loads.

Usage: python -m kolo._emit_auto

Called by _spawn_auto_emit() in core.py after each trace is saved. Runs under
a CPU-time cap (see AUTO_EMIT_CPU_LIMIT_SECONDS).
"""

from __future__ import annotations

import logging
import os
import shutil
import signal
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

logger = logging.getLogger("kolo")

# Backstop for PID reuse / Windows: a live holder is never reclaimed, this only breaks
# a lock whose recorded PID can't be trusted.
LOCK_TIMEOUT_SECONDS = 3600

# Preserve manually emitted directories during the marker's grace period, even outside latest-N.
MANUAL_EMIT_MARKER_NAME = ".manual_emit"
MANUAL_EMIT_GRACE_SECONDS = 24 * 3600

# Worst legitimate emit measured ~35s CPU. The kernel sends SIGXCPU at this limit and SIGKILL
# after the grace period, giving the handler time to release the locks.
AUTO_EMIT_CPU_LIMIT_SECONDS = 120
CPU_LIMIT_KILL_GRACE_SECONDS = 15

# Auto-emit builds each trace directory under traces/STAGING_DIR_NAME and moves
# it into place only once complete, so a killed emit never leaves a partial
# directory that the reconcile would mistake for a finished one.
STAGING_DIR_NAME = ".emit-staging"

GAVE_UP_FILE_NAME = "emit_gave_up.txt"


class CPULimitExceeded(BaseException):
    """Raised by the SIGXCPU handler.

    A BaseException so the reconcile's and migration's broad ``except
    Exception`` blocks don't swallow it.
    """


def _on_cpu_limit(signum: int, frame: object) -> None:
    # Linux re-sends SIGXCPU every second until the hard limit; raise only once
    # so a second signal can't interrupt the finally blocks releasing locks.
    signal.signal(signal.SIGXCPU, signal.SIG_IGN)
    raise CPULimitExceeded


def _apply_cpu_limit(seconds: int) -> None:
    """Cap this process's CPU time via RLIMIT_CPU. No-op where unsupported."""
    try:
        import resource
    except ImportError:  # pragma: no cover - Windows
        return

    _, current_hard = resource.getrlimit(resource.RLIMIT_CPU)
    hard = seconds + CPU_LIMIT_KILL_GRACE_SECONDS
    if current_hard != resource.RLIM_INFINITY:
        hard = min(hard, current_hard)  # An unprivileged process can't raise it.
    signal.signal(signal.SIGXCPU, _on_cpu_limit)
    resource.setrlimit(resource.RLIMIT_CPU, (min(seconds, hard), hard))


def _read_gave_up(path: Path) -> set[str]:
    try:
        return set(path.read_text().split())
    except OSError:
        return set()


def _record_gave_up(path: Path, trace_id: str) -> None:
    try:
        with open(path, "a") as f:
            f.write(f"{trace_id}\n")
    except OSError:  # pragma: no cover
        pass


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
        return False

    if (time.time() - mtime) >= LOCK_TIMEOUT_SECONDS:
        return False  # Past the backstop: PID is no longer trustworthy.

    if sys.platform == "win32":  # pragma: no cover
        # No cheap portable os.kill(pid, 0); a recent lock is assumed alive.
        return True

    try:
        pid = int(lock_path.read_text().strip())
    except (OSError, ValueError):
        return False
    if pid <= 0:
        return False

    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
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

    if _lock_holder_alive(lock_path):
        yield False
        return

    try:
        lock_path.unlink(missing_ok=True)
    except OSError:  # pragma: no cover
        pass

    fd = None
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        try:
            os.write(fd, str(os.getpid()).encode())
        finally:
            os.close(fd)
        acquired = True
        yield True
    except (FileExistsError, OSError):  # pragma: no cover
        yield False
    finally:
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
    from .db import (
        TraceNotFoundError,
        list_traces_from_db,
        load_trace_from_db,
    )
    from .emit import emit_trace
    from .trace_container import load_trace
    from .trace import Trace

    kolo_dir = db_path.parent.parent
    traces_dir = kolo_dir / "traces"

    traces = list_traces_from_db(db_path, count=keep_count)
    if not traces:
        return

    traces_dir.mkdir(exist_ok=True)
    latest_trace_ids = {row[0] for row in traces}

    # Anything left in staging is from an emit that was killed mid-way. We hold
    # the single-flight lock, so no live emit is writing there.
    staging_dir = traces_dir / STAGING_DIR_NAME
    shutil.rmtree(staging_dir, ignore_errors=True)

    existing_dirs: dict[str, Path] = {}
    for entry in traces_dir.iterdir():
        if entry.is_dir() and entry != staging_dir:
            for file in entry.iterdir():
                if file.name.startswith("trc_") and file.name.endswith(".txt"):
                    trace_id = file.stem
                    existing_dirs[trace_id] = entry
                    break

    now = time.time()
    for trace_id, dir_path in existing_dirs.items():
        if trace_id in latest_trace_ids:
            continue
        if has_fresh_manual_emit_marker(dir_path, now=now):
            continue
        try:
            shutil.rmtree(dir_path)
        except OSError:  # pragma: no cover
            pass

    # Iterate oldest->newest so newly created directory mtimes preserve recency.
    gave_up_path = db_path.parent / GAVE_UP_FILE_NAME
    gave_up = _read_gave_up(gave_up_path)
    for row in reversed(traces):
        trace_id = row[0]
        if trace_id in existing_dirs or trace_id in gave_up:
            continue
        try:
            msgpack_data, _ = load_trace_from_db(db_path, trace_id)
            data = load_trace(msgpack_data)
            trace = Trace(unprocessed_data=data, size=len(msgpack_data))
            emit_trace(trace, traces_dir, staging_dir=staging_dir)
        except CPULimitExceeded:
            # Mark an over-budget emit so subsequent saves can reach newer traces.
            _record_gave_up(gave_up_path, trace_id)
            raise
        except TraceNotFoundError:
            logger.debug("Skipping disappeared trace during auto-emit: %s", trace_id)
        except Exception:
            logger.debug("Could not emit trace %s", trace_id, exc_info=True)
    shutil.rmtree(staging_dir, ignore_errors=True)

    try:
        from ._kolotxt import update_kolotxt

        update_kolotxt(db_path)
    except Exception:
        logger.debug("Failed to update kolo.txt", exc_info=True)

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

    # migration_pending() is SQLite-only and never lists raw/, so it stays cheap with millions of files.
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
            if migration_pending(db_path):
                migrate_traces_to_files(db_path)
        except Exception as e:  # pragma: no cover
            logger.debug(f"Auto-migration failed: {e}")


def main(cpu_limit_seconds: int = AUTO_EMIT_CPU_LIMIT_SECONDS) -> int:
    """Entry point for the detached subprocess: auto_emit under a CPU cap.

    The cap lives here rather than in auto_emit() because auto_emit() can also
    run in-process (see _spawn_auto_emit), where an RLIMIT would apply to the
    host program.
    """
    _apply_cpu_limit(cpu_limit_seconds)
    try:
        auto_emit()
    except CPULimitExceeded:
        logger.debug("auto-emit hit its %ss CPU limit", cpu_limit_seconds)
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
