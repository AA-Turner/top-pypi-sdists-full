"""held/: writes set aside once their run stalled (R9, R12), let out hourly and by `probe outbox
retry`. A metric, step or upload is moved aside whole, bytes included; anything else (a run PATCH,
a span, an ingest) holds its whole run's lane in place, so nothing of that run passes it."""

from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path

from probe.foundation.compat.compat import StrEnum
from probe.foundation.durable.durable import file_lock, fsync_directory, write_text_atomic

#: The quarantine folder beside a queue's ``ops/`` (and ``multipart/held/`` beside ``multipart/ops/``).
HELD_DIR = "held"
#: Lane holds: one marker per held run lane, under the queue's ``held/``.
LANES_DIR = "lanes"
#: How long a held write waits before it is tried again (T1: hourly).
HELD_RETRY_SECONDS = 3600.0
#: A best-effort write set aside at its first failure is tried again after this, doubling with each
#: hold, up to `HELD_RETRY_SECONDS`: a blip delays it a minute, not an hour.
BEST_EFFORT_RETRY_SECONDS = 60.0

#: Op fields the quarantine writes.
HELD_AT = "held_at"  # epoch seconds it was set aside
HELD_UNTIL = "held_until"  # epoch seconds it is let out again
HELD_CAUSE = "held_cause"  # a `HeldCause`
HELD_ERROR = "held_error"  # the failure that set it aside
HELD_COUNT = "held_count"  # times set aside: one let out that fails again goes straight back


class HeldCause(StrEnum):
    """Why a write was set aside."""

    #: Its run made no progress for `STALL_LIMIT_SECONDS` while this write kept failing.
    STALLED = "stalled"


def is_set_aside_alone(op: dict) -> bool:
    """Whether ``op`` may leave its run's line on its own: metric points, step records and
    uploads, which nothing later depends on. A PATCH replaces whole values (a stale one landing
    after a newer one undoes it) and a span's child needs its parent, so those hold their lane."""
    from probe.sdk import routes

    kind = op.get("kind")
    if kind in ("upload", "multipart_upload"):
        return True
    if kind != "http":
        return False
    write = routes.classify(str(op.get("method") or ""), str(op.get("path") or "")).op
    return op.get("method") == "POST" and write in (routes.WriteOp.METRICS, routes.WriteOp.STEPS)


def held_folders(queue_dir: Path) -> list[Path]:
    """The held folders of one queue: its own and its multipart queue's."""
    return [Path(queue_dir) / HELD_DIR, Path(queue_dir) / "multipart" / HELD_DIR]


def _queue_of(path: Path) -> Path:
    """The queue a file in ``ops/``, ``held/`` or ``multipart/<x>/`` belongs to."""
    folder = path.parent.parent
    return folder.parent if folder.name == "multipart" else folder


def _append_lock(queue_dir: Path) -> Path:
    return Path(queue_dir) / ".append.lock"


def is_best_effort(op: dict) -> bool:
    """A write that never holds its run's result (``blocking: false``: lineage, captured outputs,
    diagnostics, the exit span); a multipart upload is the user's file, so it is not."""
    return op.get("blocking", True) is False and op.get("kind") != "multipart_upload"


def best_effort_retry(op: dict) -> float:
    """When a best-effort write held again is next tried: a minute, doubling, up to the hour."""
    try:
        times = int(op.get(HELD_COUNT) or 0)
    except (TypeError, ValueError):
        times = 0
    return min(BEST_EFFORT_RETRY_SECONDS * (2 ** min(times, 10)), HELD_RETRY_SECONDS)


def _stamp(op: dict, cause: HeldCause, now: float, retry_seconds: float | None = None) -> None:
    op[HELD_AT] = now
    op[HELD_UNTIL] = now + (HELD_RETRY_SECONDS if retry_seconds is None else retry_seconds)
    op[HELD_CAUSE] = str(cause)
    op[HELD_ERROR] = op.get("last_error")
    op[HELD_COUNT] = int(op.get(HELD_COUNT) or 0) + 1


def hold_op(
    path: Path, op: dict | None = None, *, cause: HeldCause, now: float | None = None,
    retry_seconds: float | None = None,
) -> Path | None:
    """Move one queued write (``ops/`` or ``multipart/ops/``) to the ``held/`` beside it, whole: a
    multipart upload keeps its staged copy and server upload (never `on_dead_letter`). Under the
    queue's append lock, as the blob and staging gcs scan, so no gc sees it in neither folder.
    Returns the new path, or None when the write is gone (delivered meanwhile)."""
    now = time.time() if now is None else now
    queue = _queue_of(path)
    target_dir = path.parent.parent / HELD_DIR
    with file_lock(_append_lock(queue)):
        if op is None:
            try:
                op = json.loads(path.read_text())
            except (OSError, ValueError):
                return None
        if not isinstance(op, dict) or not path.exists():
            return None
        _stamp(op, cause, now, retry_seconds)
        target_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        try:
            # Update in place, then MOVE: a crash leaves the write in one folder, never two.
            write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
            os.replace(path, target_dir / path.name)
        except FileNotFoundError:
            return None
    fsync_directory(target_dir)
    fsync_directory(path.parent)
    return target_dir / path.name


def hold_lane(
    queue_dir: Path, lane: str, head: Path, *, run_ref: str | None, error: str | None,
    cause: HeldCause = HeldCause.STALLED, now: float | None = None,
) -> bool:
    """Hold a whole run lane in place: its writes stay in ``ops/``, in order, and no drain sends
    any until the hold is let out. The head is stamped (`was_held`) so a fresh failure after the
    release holds the lane again at once. False when the head is gone."""
    now = time.time() if now is None else now
    try:
        op = json.loads(head.read_text())
    except (OSError, ValueError):
        return False
    if isinstance(op, dict):
        _stamp(op, cause, now)
        try:
            write_text_atomic(head, json.dumps(op, indent=2) + "\n", mode=0o600)
        except FileNotFoundError:
            return False
    marker = {
        "lane": lane, "run_ref": run_ref, "head": head.name, HELD_AT: now,
        HELD_UNTIL: now + HELD_RETRY_SECONDS, HELD_CAUSE: str(cause), HELD_ERROR: error,
    }
    folder = Path(queue_dir) / HELD_DIR / LANES_DIR
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    write_text_atomic(folder / _lane_file(lane), json.dumps(marker) + "\n", mode=0o600)
    return True


def lane_holds(queue_dir: Path) -> list[tuple[Path, dict]]:
    """Every lane hold of one queue (marker path, marker)."""
    folder = Path(queue_dir) / HELD_DIR / LANES_DIR
    try:
        names = sorted(n for n in os.listdir(folder) if n.endswith(".json"))
    except OSError:
        return []
    out = []
    for name in names:
        try:
            marker = json.loads((folder / name).read_text())
        except (OSError, ValueError):
            continue
        if isinstance(marker, dict) and isinstance(marker.get("lane"), str):
            out.append((folder / name, marker))
    return out


def held_lanes(queue_dir: Path, now: float | None = None) -> set:
    """The run lanes held right now (a hold that is due is let out by the worker)."""
    now = time.time() if now is None else now
    return {marker["lane"] for _path, marker in lane_holds(queue_dir) if not _is_due(marker, now)}


def held_ops(queue_dir: Path) -> list[tuple[Path, dict]]:
    """Every write moved to a held folder of one queue, oldest first."""
    out: list[tuple[Path, dict]] = []
    for folder in held_folders(queue_dir):
        try:
            names = sorted(n for n in os.listdir(folder) if n.endswith(".json"))
        except OSError:
            continue
        for name in names:
            try:
                op = json.loads((folder / name).read_text())
            except (OSError, ValueError):
                continue
            if isinstance(op, dict):
                out.append((folder / name, op))
    return out


def has_held(queue_dir: Path) -> bool:
    """Whether anything of this queue is held (moved aside or a lane hold). Listings only."""
    for folder in [*held_folders(queue_dir), Path(queue_dir) / HELD_DIR / LANES_DIR]:
        try:
            if any(n.endswith(".json") for n in os.listdir(folder)):
                return True
        except OSError:
            continue
    return False


def next_release_in(queue_dir: Path, now: float | None = None) -> float | None:
    """Seconds until the soonest held write or lane is let out (0: one is due), or None."""
    now = time.time() if now is None else now
    until = [_until(op) for _path, op in held_ops(queue_dir)]
    until += [_until(marker) for _path, marker in lane_holds(queue_dir)]
    return max(0.0, min(until) - now) if until else None


def has_due_held(queue_dir: Path, now: float | None = None) -> bool:
    """Whether a held write or lane of this queue may be tried again now."""
    if not has_held(queue_dir):
        return False
    left = next_release_in(queue_dir, now)
    return left is not None and left <= 0


def release_held(
    queue_dir: Path, *, due_only: bool = True, now: float | None = None, run_ref: str | None = None
) -> int:
    """Let held writes back into line under their own names (their old place), and drop lane
    holds: the due ones, or (``due_only=False``, `probe outbox retry`) all; ``run_ref``: that run's
    only. Under the append lock
    (see `hold_op`). Returns how many writes and lanes were let out."""
    now = time.time() if now is None else now
    if not has_held(queue_dir) or (due_only and not has_due_held(queue_dir, now)):
        return 0
    released = 0
    with file_lock(_append_lock(queue_dir)):
        for path, op in held_ops(queue_dir):
            if (due_only and not _is_due(op, now)) or (run_ref is not None and op.get("run_ref") != run_ref):
                continue
            op.pop(HELD_UNTIL, None)
            target_dir = path.parent.parent / "ops"
            target_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
            try:
                write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
                os.replace(path, target_dir / path.name)
            except FileNotFoundError:
                continue
            fsync_directory(target_dir)
            released += 1
        for path, marker in lane_holds(queue_dir):
            if (due_only and not _is_due(marker, now)) or (
                run_ref is not None and marker.get("run_ref") != run_ref
            ):
                continue
            path.unlink(missing_ok=True)
            released += 1
    return released


def was_held(op: dict) -> bool:
    """Whether ``op`` was set aside before: a transient failure sends it straight back."""
    try:
        return int(op.get(HELD_COUNT) or 0) > 0
    except (TypeError, ValueError):
        return False


def _lane_file(lane: str) -> str:
    return hashlib.sha256(lane.encode("utf-8", "surrogatepass")).hexdigest()[:24] + ".json"


def _until(record: dict) -> float:
    try:
        return float(record.get(HELD_UNTIL) or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _is_due(record: dict, now: float) -> bool:
    return _until(record) <= now
