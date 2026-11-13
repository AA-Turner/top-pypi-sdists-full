"""A file a rollout attached, uploaded in a worker thread (never on the caller's event loop) and read back as the
sample's `TrialFile` once it landed."""

from __future__ import annotations

import mimetypes
import os
import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import PurePosixPath
from typing import Any

#: Seconds an export waits for one file's upload, counted from the upload's start (A1).
UPLOAD_TIMEOUT_S = 30.0
#: Seconds an export waits for an upload still queued behind others to start, from its attach; then it is canceled.
#: A stalled store costs the files behind it, never the rollout (`PROBE_SAMPLE_UPLOAD_QUEUE_TIMEOUT_S`).
UPLOAD_QUEUE_TIMEOUT_S = 60.0
UPLOAD_QUEUE_TIMEOUT_ENV = "PROBE_SAMPLE_UPLOAD_QUEUE_TIMEOUT_S"
#: Upload threads one process shares across its rollouts (`PROBE_SAMPLE_UPLOAD_THREADS`).
UPLOAD_WORKERS = 4
UPLOAD_THREADS_ENV = "PROBE_SAMPLE_UPLOAD_THREADS"
#: What a file's bytes are, from its suffix, where mimetypes says nothing useful (Harbor's `get_file_kind` rules).
_KINDS = {".json": "json", ".jsonl": "json", ".ndjson": "json", ".html": "html", ".htm": "html", ".diff": "text",
          ".patch": "text", ".log": "text", ".txt": "text", ".out": "text", ".err": "text", ".md": "text", "": "text",
          ".tar": "archive", ".gz": "archive", ".tgz": "archive", ".zip": "archive", ".zst": "archive"}  # fmt: skip
_MEDIA = frozenset({"image", "audio", "video", "text"})

_POOL: ThreadPoolExecutor | None = None
_POOL_LOCK = threading.Lock()


def get_upload_pool() -> ThreadPoolExecutor:
    """The process's upload threads, made on first use (a process that never attaches starts none)."""
    global _POOL
    with _POOL_LOCK:
        if _POOL is None:
            _POOL = ThreadPoolExecutor(max_workers=get_upload_threads(), thread_name_prefix="probe-rollout-upload")
        return _POOL


def get_upload_threads() -> int:
    """`PROBE_SAMPLE_UPLOAD_THREADS` (at least 1), else 4."""
    try:
        return max(1, int(os.environ.get(UPLOAD_THREADS_ENV) or UPLOAD_WORKERS))
    except ValueError:
        return UPLOAD_WORKERS


def get_upload_queue_timeout() -> float:
    """`PROBE_SAMPLE_UPLOAD_QUEUE_TIMEOUT_S` (seconds, at least 0), else 60."""
    try:
        value = float(os.environ.get(UPLOAD_QUEUE_TIMEOUT_ENV) or UPLOAD_QUEUE_TIMEOUT_S)
    except ValueError:
        return UPLOAD_QUEUE_TIMEOUT_S
    return value if value >= 0 and value != float("inf") else UPLOAD_QUEUE_TIMEOUT_S


def _reset_pool_in_child() -> None:
    """A forked child (a Ray or multiprocessing worker) inherits the pool without its threads: it makes its own."""
    global _POOL, _POOL_LOCK
    _POOL = None
    _POOL_LOCK = threading.Lock()


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_pool_in_child)


def get_file_kind(path: str) -> str:
    """text, json, html, image, audio, video, archive or other, from the file's name."""
    suffix = PurePosixPath(path).suffix.lower()
    if suffix in _KINDS:
        return _KINDS[suffix]
    major = (mimetypes.guess_type(path, strict=False)[0] or "").partition("/")[0]
    return major if major in _MEDIA else "other"


@dataclass
class Attachment:
    """One attached file: its name in the rollout, its role, whether the sample reads it as a log or an output, and
    its upload. `wait` gives the `TrialFile` once the bytes landed, or None (failed, refused, or past its time)."""

    name: str
    role: str
    is_log: bool
    attached_at: float = field(default_factory=time.monotonic)
    #: When a worker thread began the upload (None while it waits for one).
    started_at: float | None = None
    future: Future | None = None
    #: A temp file holding attached text, deleted once its upload ends.
    temp_path: str | None = None
    _started: threading.Event = field(default_factory=threading.Event, repr=False)

    def mark_started(self) -> None:
        """Called by the worker thread as the upload begins: the wait's clock starts here."""
        self.started_at = time.monotonic()
        self._started.set()

    def wait(self, timeout: float = UPLOAD_TIMEOUT_S, queue_timeout: float | None = None) -> dict | None:
        """The `TrialFile` (plus `is_log`), waiting at most ``timeout`` seconds after the upload STARTED (a busy pool
        never fails a file that is only queued), and at most ``queue_timeout`` (default `get_upload_queue_timeout`)
        after the attach for it to start. A file past either is canceled where it has not started; one already
        running finishes later, stored under its rollout's name and span, and still counts as failed here (DESIGN.md
        "Rollout capture")."""
        future = self.future
        if future is None:
            return None
        if queue_timeout is None:
            queue_timeout = get_upload_queue_timeout()
        if not self._started.wait(max(0.0, self.attached_at + queue_timeout - time.monotonic())) and not future.done():
            self._cancel()
            return None
        started = self.started_at if self.started_at is not None else time.monotonic()
        try:
            row = future.result(timeout=max(0.0, started + timeout - time.monotonic()))
        except Exception:  # noqa: BLE001 -- a failed or late upload leaves the file out (fail open)
            self._cancel()
            return None
        return self.to_file(row)

    def _cancel(self) -> None:
        """Cancel an upload that has not started (its temp file goes too; a running one cleans up after itself)."""
        if self.future is not None and self.future.cancel():
            self.delete_temp()

    def to_file(self, row: Any) -> dict | None:
        """The stored artifact row as a `TrialFile`; None when no bytes were stored (no row, or a reference row the
        credential gate left in place of the bytes)."""
        if not isinstance(row, dict) or not row.get("id") or row.get("is_reference"):
            return None
        found = {"artifact_id": str(row["id"]), "path": self.name, "role": self.role,
                 "size_bytes": row.get("size_bytes"), "sha256": row.get("content_hash"),
                 "kind": get_file_kind(self.name), "is_log": self.is_log}  # fmt: skip
        return {key: value for key, value in found.items() if value is not None}

    def delete_temp(self) -> None:
        if self.temp_path:
            try:
                os.unlink(self.temp_path)
            except OSError:
                pass
