"""the session import job: run its background job, one transcript lane at a time across snapshots."""

from __future__ import annotations
import fcntl
import os
from contextlib import contextmanager
from pathlib import Path

from .....foundation.durable.durable import now_iso


@contextmanager
def _serial_lane(job: dict, folder: Path):
    """Session journals need one upload/digest owner across snapshots.

    Their transactions are locked individually, but two different approved
    snapshots can contain the same session. Serialize the whole transcript
    lane so the second job sees the first job's completed digest/receipts.
    Folder imports already have the scope-specific Coverage.writer lock.
    """
    if job["kind"] != Kind.TRANSCRIPTS:
        yield
        return
    descriptor = os.open(folder.parent / "transcripts.lock", os.O_CREAT | os.O_RDWR, 0o600)
    with os.fdopen(descriptor, "a+") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            _update(
                folder, state=State.QUEUED,
                started_at=None,
                progress=_progress_message(_read(folder)["progress"], "Waiting for the previous session import."),
            )
            fcntl.flock(handle, fcntl.LOCK_EX)
            _update(folder, state=State.RUNNING, started_at=now_iso(),
                    progress=_progress_message(_read(folder)["progress"], "Resuming the approved import."))
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)
from probe.cli.imports.jobs.kind import Kind  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.jobs.store import State, _progress_message, _read, _update  # noqa: E402 -- pieces need each other; the front door loads this one first
