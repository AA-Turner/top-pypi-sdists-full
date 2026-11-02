"""a job's folder on disk: its states, read/save/update its record under its lock, payloads checked for secrets."""

from __future__ import annotations
import fcntl
import hashlib
import json
import os
import re
from contextlib import contextmanager
from probe.foundation.compat.compat import StrEnum
from pathlib import Path

from ....foundation.durable.durable import now_iso, write_text_atomic
ACTIVITY_LINES = 200
ACTIVITY_LINE_CHARS = 2000


class State(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    INTERRUPTED = "interrupted"
    CANCELED = "canceled"


_ID = re.compile(r"[0-9a-f]{32}\Z")
_SECRET_KEYS = {
    "token", "access_token", "refresh_token", "api_key", "password", "secret",
    "authorization", "credential", "credentials", "env", "environment",
}


def default_dir() -> Path:
    base = os.environ.get("XDG_STATE_HOME")
    return (Path(base).expanduser() if base else Path.home() / ".local" / "state") / "probe" / "import-jobs"


def _root(directory: Path | None) -> Path:
    return (directory or default_dir()).expanduser().resolve()


def _directory(job_id: str, directory: Path | None = None) -> Path:
    if not _ID.fullmatch(job_id):
        raise JobError("Invalid import job ID.")
    return _root(directory) / job_id


def _check_payload(value) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str) or key.lower().replace("-", "_") in _SECRET_KEYS:
                raise JobError("Import jobs cannot store credentials or environment variables.")
            _check_payload(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _check_payload(item)


def _clean(text, limit=1500) -> str:
    return "".join(c for c in str(text) if c.isprintable() or c == "\t")[:limit]


def _identity(kind: str, payload: dict) -> str:
    canonical = json.dumps({"kind": kind, "payload": payload}, sort_keys=True, allow_nan=False)
    return hashlib.sha256(canonical.encode()).hexdigest()[:32]


def _read(folder: Path) -> dict:
    try:
        value = json.loads((folder / "job.json").read_text(encoding="utf-8"))
        if not isinstance(value, dict) or value.get("id") != folder.name:
            raise ValueError
        State(value["state"])
        Kind(value["kind"])
        for field in ("created_at", "updated_at", "label", "log_path"):
            if not isinstance(value.get(field), str):
                raise ValueError
        if not isinstance(value.get("progress"), dict):
            raise ValueError
        if not isinstance(value.get("report"), list):
            raise ValueError
        if not isinstance(value.get("attempt"), int) or value["attempt"] < 0:
            raise ValueError
        if not isinstance(value["payload"], dict):
            raise ValueError
        _check_payload(value["payload"])
        if _identity(value["kind"], value["payload"]) != folder.name:
            raise ValueError
        return value
    except (OSError, ValueError, KeyError) as exc:
        raise JobError("The saved import job could not be read.") from exc


def _save(folder: Path, job: dict) -> None:
    # Only worker-authored public progress joins this stream. output.log also
    # contains arbitrary agent stdout/stderr and must never cross desktop IPC.
    previous = job.get("activity")
    previous = previous if isinstance(previous, list) else []
    events = previous[-ACTIVITY_LINES:]
    message = (job.get("progress") or {}).get("message")
    is_clipped = False
    if isinstance(message, str) and message:
        is_clipped = len(message) > ACTIVITY_LINE_CHARS
        # Keep the worker's dependency set unchanged: the desktop boundary
        # applies credential redaction when rendering these private records.
        message = _clean(message, ACTIVITY_LINE_CHARS)
        latest = events[-1] if events and isinstance(events[-1], dict) else {}
        if message != latest.get("message") or job["state"] != latest.get("state"):
            events = [*events, {"at": job["updated_at"], "state": job["state"], "message": message}]
    job["activity_truncated"] = (bool(job.get("activity_truncated")) or is_clipped
                                 or len(previous) > ACTIVITY_LINES or len(events) > ACTIVITY_LINES)
    job["activity"] = events[-ACTIVITY_LINES:]
    write_text_atomic(folder / "job.json", json.dumps(job, sort_keys=True, allow_nan=False), mode=0o600)


def _update(folder: Path, **changes) -> dict:
    with _job_lock(folder, "state.lock"):
        job = _read(folder)
        if job.get("cancel_requested") and changes.get("cancel_requested") is not False:
            # The canceling process owns the terminal transition. A worker may
            # still finish a journal write or handle SIGTERM before it exits;
            # neither can turn cancellation into a success or restartable stop.
            for key in ("state", "finished_at", "pid", "pid_identity", "launch_pid", "launch_identity", "error"):
                changes.pop(key, None)
            if "progress" in changes:
                changes["progress"] = _progress_message(changes["progress"], "Canceling import…")
        job.update(changes, updated_at=now_iso())
        _save(folder, job)
        return job


def _progress_message(previous: dict, message: str) -> dict:
    """Keep measured work when only the worker's lifecycle state changes."""
    return {
        **{key: previous[key] for key in (
            "completed", "total", "phase", "stage", "stage_completed", "stage_total",
            "completion_completed", "completion_total", "completion_ids",
        ) if key in previous},
        "message": message,
    }


@contextmanager
def _try_lock(path: Path):
    descriptor = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
    with os.fdopen(descriptor, "a+") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            yield False
            return
        try:
            yield True
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


@contextmanager
def _job_lock(folder: Path, name: str):
    """Lock an existing job without recreating a folder cleared by the user."""
    descriptor = os.open(folder / name, os.O_CREAT | os.O_RDWR, 0o600)
    with os.fdopen(descriptor, "a+") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)
from probe.cli.imports.jobs.errors import JobError  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.jobs.kind import Kind  # noqa: E402 -- pieces need each other; the front door loads this one first
