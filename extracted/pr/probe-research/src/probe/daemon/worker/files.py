"""the worker's files: one worker per session by lock, its inbox and markers, sweeping stale sessions."""

from __future__ import annotations
import time
from pathlib import Path
from typing import Callable
from probe.daemon.host import lease
from probe.shared import mailbox
from probe.daemon.trace import trace as trace_mod
from probe.daemon.store.store import (
    state_dir,
    store_path)
#: Stores, inboxes and logs no worker holds, untouched this long, are deleted at start.
STALE_AFTER_S = trace_mod.KEEP_S
LOCK_POLL_S = 1.0
#: How long a new worker waits for the session lock before it leaves with
#: EXIT_RESPAWN_LATER. The holder hands over only once it is stopping (after a
#: model round), so one that never stops would keep a waiter forever, and a
#: supervisor that lost track of its child would add one per respawn (the
#: Windows harness: ~100). A supervisor never starts a worker while the lock
#: is held (it asks the holder to hand over itself), so this bounds only a
#: race or an older supervisor's waiter.
LOCK_WAIT_S = 5 * 60.0


# ---------------------------------------------------------------------------
# Files beside the store.
# ---------------------------------------------------------------------------


def _state_base() -> Path:
    return state_dir().parent


def inbox_path(session_id: str) -> Path:
    return state_dir() / f"{session_id}.inbox.jsonl"


def lock_path(session_id: str) -> Path:
    return store_path(session_id).with_suffix(".lock")


def _mark(path: Path) -> None:
    """Best effort: an empty marker file beside the store."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
    except OSError as exc:
        log.warning("marker %s not written: %s", path.name, exc)


def session_lock(session_id: str, *, should_stop: Callable[[], bool] = lambda: False,
                 poll_s: float = LOCK_POLL_S, max_wait_s: float = LOCK_WAIT_S):
    """Take `<state>/probe/daemon/<sid>.lock` for the worker's life: one worker per
    session. Held by another -- the previous worker of a resumed session finishing
    its queue -- wait for it, at most `max_wait_s`. Returns the open lock file
    (keep it open), or an exit code: EXIT_RESPAWN_LATER if the switch leaves
    `daemon` (or cannot be read) while waiting or the holder did not let go in
    time, 0 when told to stop."""
    from probe._shared import oscompat as fcntl  # fcntl.flock, or msvcrt on Windows

    path = lock_path(session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    handover = mailbox.handover_path(session_id)
    handle = path.open("a")
    waiting = False
    deadline = time.monotonic() + max_wait_s
    try:
        while True:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                pass
            else:
                # Any ask to hand over was the previous holder's (one dated ahead
                # by a restarting service included): left, it would make this
                # worker hand over when its own session ends, not finish its queue.
                # Held now either way: a delete that fails (Windows, while a next
                # worker touches the ask) never sends this worker back to take a
                # lock it holds, which msvcrt's byte lock refuses even to itself.
                _discard(handover)
                return handle
            if not waiting:
                # The holder is the previous worker of a resumed session: it hands
                # over at its next model round (`Worker.handing_over`).
                log.info("another worker holds %s: asking it to hand over", path)
                waiting = True
            _mark(handover)  # every poll: the holder trusts only a fresh one
            if not lease.worker_wanted(session_id):
                handle.close()
                return inline_exit_code(session_id) if lease.inline(session_id) else EXIT_RESPAWN_LATER
            if should_stop():
                handle.close()
                return 0
            if time.monotonic() >= deadline:
                # The ask stays (it goes stale in HANDOVER_FRESH_S): the
                # supervisor, or the waiter it starts next, asks again before then.
                log.info("%s still held after %.0fs: leaving; the supervisor starts a worker again later",
                         path, max_wait_s)
                waiting = False
                handle.close()
                return EXIT_RESPAWN_LATER
            time.sleep(poll_s)
    finally:
        if waiting:
            _discard(handover)


def _discard(path: Path) -> None:
    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass


def sweep_stale(keep: str, *, now: float | None = None, max_age: float = STALE_AFTER_S) -> int:
    """Delete the stores, inboxes, logs and session folders (`trace.py`) of
    sessions untouched for `max_age` that no worker holds (their lock is free).
    One directory listing, at start. Lock files stay: deleting one another worker
    has open would split the lock."""
    from probe._shared import oscompat as fcntl  # fcntl.flock, or msvcrt on Windows
    import shutil

    base = state_dir()
    cutoff = (time.time() if now is None else now) - max_age
    try:
        entries = list(base.iterdir())
    except OSError:
        return 0
    by_session: dict[str, list[Path]] = {}
    for path in entries:
        for suffix in (".sqlite", ".sqlite-wal", ".sqlite-shm", ".inbox.jsonl", ".log"):
            if path.name.endswith(suffix):
                by_session.setdefault(path.name[: -len(suffix)], []).append(path)
                break
    try:
        folders_ = [p for p in trace_mod.sessions_dir().iterdir() if p.is_dir()]
    except OSError:
        folders_ = []
    for folder in folders_:
        by_session.setdefault(folder.name, []).append(folder)
    removed = 0
    for sid, paths in by_session.items():
        if sid == store_path(keep).stem:
            continue
        try:
            if max(_last_touched(p) for p in paths) > cutoff:
                continue
            with (base / f"{sid}.lock").open("a") as handle:
                try:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                except OSError:
                    continue  # a live worker holds it
                for p in paths:
                    if p.is_dir():
                        shutil.rmtree(p, ignore_errors=True)
                    else:
                        p.unlink(missing_ok=True)
                    removed += 1
        except OSError:
            continue
    return removed


def _last_touched(path: Path) -> float:
    """A file's modification time; a folder's is its newest file's (appending
    to a file leaves the folder's own time alone)."""
    if not path.is_dir():
        return path.stat().st_mtime
    return max([path.stat().st_mtime] + [p.stat().st_mtime for p in path.iterdir() if p.is_file()])
from probe.daemon.worker.loop.reading import log  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.supervisor import EXIT_RESPAWN_LATER, inline_exit_code  # noqa: E402 -- pieces need each other; the front door loads this one first
