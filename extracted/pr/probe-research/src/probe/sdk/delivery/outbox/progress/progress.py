"""progress.json: what a queue's worker last saw of each run (R1), the one thing a waiting
`finish()` reads. Written by the worker only; a torn or missing file reads as None."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path
from typing import Any

from probe.foundation.compat.compat import StrEnum
from probe.foundation.durable.durable import SYNC_NONE, write_text_atomic

#: Beside the queue's status.json; never written by an append, so no other process erases it.
PROGRESS_FILE = "progress.json"
SCHEMA = 1


class DeliveryErrorKind(StrEnum):
    """What last stopped one run's writes, as the worker saw it."""

    #: The server answered an error that may pass (5xx, 429, a timeout); the worker retries.
    TRANSIENT = "transient"
    #: Nothing answered at all (connect failure, or answers lost twice in one pass).
    UNREACHABLE = "unreachable"
    #: The server refused a write for good (4xx): it is in failed/.
    REFUSED = "refused"
    #: The server refused the credential (401/403): waits for a new sign-in.
    LOGIN_REFUSED = "login_refused"
    #: Held for a credential this worker lacks, or behind another queue: its holder sends it.
    HELD_ELSEWHERE = "held_elsewhere"
    #: The run stalled and its stuck write was set aside to held/ (R12).
    STALLED = "stalled"


@dataclass
class RunProgress:
    """One run in the record. Times are epoch seconds (another process reads them)."""

    #: Writes of the run still queued: ops, multipart uploads, uploads waiting for their scan.
    pending: int = 0
    pending_bytes: int = 0
    #: Writes of the run this queue's workers delivered, carried from worker to worker.
    delivered_total: int = 0
    #: When a write of the run last moved (delivered, refused, superseded, a slice of an upload).
    last_progress_at: float | None = None
    #: The server's Retry-After for the run ends then; timing only, never the stall rule (R11).
    retry_after_until: float | None = None
    unreachable_since: float | None = None
    last_error_kind: str | None = None
    last_error: str | None = None
    #: Writes set aside in held/, refused into failed/ (blocking ones), superseded into discarded/.
    held: int = 0
    failed: int = 0
    discarded: int = 0
    #: Best-effort writes (lineage, captured outputs, the exit span) still in line: waited for,
    #: never a reason to raise (one that fails is set aside and no longer counted).
    best_effort: int = 0
    #: Since when its head write keeps failing with no progress (the stall clock, R12).
    failing_since: float | None = None
    #: Stall causes already reported to the server for this run (sent once each).
    reported: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: Any) -> "RunProgress":
        if not isinstance(raw, dict):
            return cls()
        known = {f.name for f in fields(cls)}
        out = cls(**{k: v for k, v in raw.items() if k in known})
        if not isinstance(out.reported, list):
            out.reported = []
        return out


@dataclass
class ProgressRecord:
    """A queue's progress record: who wrote it, when, and each run it tracks."""

    pid: int | None = None
    version: str = ""
    updated_at: float = 0.0
    #: The whole queue could not reach the server since then (None: it could).
    unreachable_since: float | None = None
    paused: bool = False
    #: Runs a `finish()` waits on, served first (R2).
    priority: list[str] = field(default_factory=list)
    runs: dict[str, RunProgress] = field(default_factory=dict)
    #: Writes of the queue still to send, every run included ("N writes ahead of yours").
    queue_pending: int = 0
    #: The worker wrote this record on its way out (a clean exit); False while it runs. A
    #: free lease with a record still saying False is a worker that died (the waiter counts it).
    exited: bool = False

    def run(self, run_ref: str) -> RunProgress | None:
        return self.runs.get(run_ref)

    def to_dict(self) -> dict:
        out = asdict(self)
        out["schema"] = SCHEMA
        out["runs"] = {ref: progress.to_dict() for ref, progress in self.runs.items()}
        return out

    @classmethod
    def from_dict(cls, raw: Any) -> "ProgressRecord | None":
        if not isinstance(raw, dict) or raw.get("schema") != SCHEMA:
            return None
        runs = raw.get("runs") if isinstance(raw.get("runs"), dict) else {}
        try:
            return cls(
                pid=raw.get("pid") if isinstance(raw.get("pid"), int) else None,
                version=str(raw.get("version") or ""),
                updated_at=float(raw.get("updated_at") or 0.0),
                unreachable_since=_number(raw.get("unreachable_since")),
                paused=bool(raw.get("paused")),
                priority=[str(r) for r in raw.get("priority") or () if isinstance(r, str)],
                runs={str(ref): RunProgress.from_dict(value) for ref, value in runs.items()},
                queue_pending=int(raw.get("queue_pending") or 0),
                exited=bool(raw.get("exited")),
            )
        except (TypeError, ValueError):
            return None


def progress_path(queue_dir: str | Path) -> Path:
    return Path(queue_dir) / PROGRESS_FILE


def load_progress(queue_dir: str | Path) -> ProgressRecord | None:
    """The queue's record, or None (no worker of this release wrote one, or it is torn)."""
    try:
        raw = json.loads(progress_path(queue_dir).read_text())
    except (OSError, ValueError):
        return None
    return ProgressRecord.from_dict(raw)


def save_progress(queue_dir: str | Path, record: ProgressRecord) -> None:
    """Replace the record atomically. No fsync: a crash loses one pass of bookkeeping, which the
    next worker rebuilds; the waiter checks the queue itself before it says "delivered"."""
    try:
        write_text_atomic(
            progress_path(queue_dir),
            json.dumps(record.to_dict(), separators=(",", ":")) + "\n",
            mode=0o600,
            sync=SYNC_NONE,
        )
    except OSError:
        pass


def worker_version() -> str:
    try:
        import probe

        return str(getattr(probe, "__version__", "") or "")
    except Exception:  # noqa: BLE001 -- a version is a label, never a condition
        return ""


def current_pid() -> int:
    return os.getpid()


def _number(value: Any) -> float | None:
    try:
        return None if value is None else float(value)
    except (TypeError, ValueError):
        return None
