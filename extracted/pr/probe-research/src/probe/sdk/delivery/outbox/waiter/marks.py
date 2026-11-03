"""Want markers (R2): a waiting `finish()` names its run in the outbox root; every worker of that
outbox sends those runs' writes first. Not the `.drain.want` flock: holding that makes each pass
give its drain lock away between ops, to a waiter that never takes it."""

from __future__ import annotations

import hashlib
import json
import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from probe.foundation.durable.durable import SYNC_NONE, write_text_atomic

WAITING_DIR = ".waiting-runs"
#: A marker its waiter has not touched this long is dropped (a waiter in another pid namespace,
#: or one killed without cleanup). A waiter touches its marker every poll.
MARK_STALE_SECONDS = 120.0


def _marks_dir(outbox_root: str | Path) -> Path:
    return Path(outbox_root) / WAITING_DIR


def _mark_path(outbox_root: str | Path, run_ref: str, pid: int) -> Path:
    digest = hashlib.sha256(run_ref.encode("utf-8", "surrogatepass")).hexdigest()[:16]
    return _marks_dir(outbox_root) / f"{digest}-{pid}.json"


def touch_mark(outbox_root: str | Path, run_ref: str) -> None:
    """Say (again) that this process waits on ``run_ref``. Best-effort."""
    path = _mark_path(outbox_root, run_ref, os.getpid())
    try:
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        if path.exists():
            os.utime(path)
            return
        body = {"run_ref": run_ref, "pid": os.getpid(), "since": time.time()}
        write_text_atomic(path, json.dumps(body) + "\n", mode=0o600, sync=SYNC_NONE)
    except OSError:
        pass


def clear_mark(outbox_root: str | Path, run_ref: str) -> None:
    try:
        _mark_path(outbox_root, run_ref, os.getpid()).unlink(missing_ok=True)
    except OSError:
        pass


@contextmanager
def mark_waiting(outbox_root: str | Path, run_ref: str) -> Iterator[None]:
    """While the body runs, ``run_ref`` is waited on (the body calls `touch_mark` as it polls)."""
    touch_mark(outbox_root, run_ref)
    try:
        yield
    finally:
        clear_mark(outbox_root, run_ref)


def waited_runs(outbox_root: str | Path, *, now: float | None = None) -> list[str]:
    """The runs a live `finish()` waits on, longest-waiting first. Stale markers are removed."""
    now = time.time() if now is None else now
    folder = _marks_dir(outbox_root)
    try:
        names = [n for n in os.listdir(folder) if n.endswith(".json")]
    except OSError:
        return []
    found: list[tuple[float, str]] = []
    for name in names:
        path = folder / name
        try:
            fresh = now - path.stat().st_mtime < MARK_STALE_SECONDS
            body = json.loads(path.read_text()) if fresh else None
            if not isinstance(body, dict) or not isinstance(body.get("run_ref"), str):
                path.unlink(missing_ok=True)  # stale or not a marker
                continue
            found.append((float(body.get("since") or 0.0), body["run_ref"]))
        except (OSError, ValueError, TypeError, OverflowError):
            continue
    out: list[str] = []
    for _since, ref in sorted(found):
        if ref not in out:
            out.append(ref)
    return out
