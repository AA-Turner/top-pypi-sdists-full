"""Durable local jobs for already-approved imports.

Workers detach from the terminal and reuse the import lanes' existing journals.
No credentials are saved here. Each lane must verify the approved destination
against its runtime credentials and replay only the approved files/sessions.
A folder-scoped automatic approval may prepare its plan in the worker; that
lane persists the exact resulting delivery snapshot before sending any files.
A machine restart stops workers; opening job status can recover their journals.
There is no boot service. Connection failures wait and retry; other failed jobs
need an explicit resume after their cause has been addressed.
"""

from __future__ import annotations
import json
import shutil
from contextlib import contextmanager
from pathlib import Path

from ....foundation.durable.durable import file_lock, now_iso


@contextmanager
def _lifecycle(directory: Path | None):
    root = _root(directory)
    # Outside the removable journal tree so all sessions keep the same lock.
    with file_lock(root.parent / (root.name + ".lock")):
        yield


def get_job(job_id: str, *, directory: Path | None = None, _launch_owned: bool = False) -> dict:
    """Read status, marking an unowned former worker interrupted.

    The lifetime lock, not a saved PID, proves running ownership: operating
    systems reuse PIDs. Queued children get their startup interval while alive.
    """
    folder = _directory(job_id, directory)
    if not (folder / "job.json").is_file():
        raise JobError("Import job not found.")
    with _job_lock(folder, "state.lock"):
        job = _read(folder)
        if job.get("cancel_requested") or job["state"] not in (State.QUEUED, State.RUNNING):
            return job
        with _try_lock(folder / "worker.lock") as unowned:
            with _try_lock(folder / "launch.lock") as not_launching:
                if unowned and (not_launching or _launch_owned) and (
                    job["state"] == State.RUNNING
                    or not _alive(job.get("pid"), job.get("pid_identity"))
                ):
                    job.update(
                        state=State.INTERRUPTED, pid=None, updated_at=now_iso(),
                        progress=_progress_message(job["progress"], "Worker stopped; the saved import can resume."),
                    )
                    _save(folder, job)
                    # The worker that would have reported this is the one that
                    # died, so the observation has to ride whichever process
                    # next reads the record. Emitted on the TRANSITION only --
                    # an interrupted job is re-read on every status refresh,
                    # and a level reported per read is a level reported
                    # hundreds of times.
                    _emit_stalled(job, "worker_vanished")
        return job


def enqueue(kind: str, payload: dict, label: str, *, directory: Path | None = None) -> dict:
    with _lifecycle(directory):
        return _enqueue(kind, payload, label, directory=directory)


def _enqueue(kind: str, payload: dict, label: str, *, directory: Path | None = None) -> dict:
    """Persist the exact approval, then start it once. Repeats share its ID.

    A changed approval must have changed payload (including scope and reviewed
    fingerprints). Re-enqueuing an identical success never imports it again.
    """
    kind = Kind(kind)
    if not isinstance(payload, dict):
        raise JobError("An import job needs an approved request object.")
    _check_payload(payload)
    canonical = json.dumps({"kind": kind, "payload": payload}, sort_keys=True, allow_nan=False)
    job_id = _identity(kind, payload)
    folder = _directory(job_id, directory)
    folder.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    folder.mkdir(exist_ok=True, mode=0o700)
    is_resumed = False
    with _job_lock(folder, "launch.lock"):
        if (folder / "job.json").exists():
            job = get_job(job_id, directory=folder.parent, _launch_owned=True)
            if not job.get("cancel_requested") and job["state"] not in (State.INTERRUPTED, State.CANCELED):
                return job
            is_resumed = True
        else:
            now = now_iso()
            _save(folder, {
                "version": 1, "id": job_id, "kind": kind, "label": _clean(label, 200),
                "payload": json.loads(canonical)["payload"], "state": State.QUEUED,
                "created_at": now, "updated_at": now, "started_at": None,
                "finished_at": None, "attempt": 0, "pid": None, "pid_identity": None,
                "progress": {"message": "Queued."}, "error": None, "report": [], "children": [],
                "log_path": str(folder / "output.log"),
                # OUTSIDE `payload` deliberately: the payload's hash IS the job
                # id, so a session id in there would give the same approval a
                # different identity every run and defeat deduplication.
                "origin": _origin_stamp(),
            })
        started = _launch(folder)
    _emit_enqueued(started, resumed=is_resumed)
    return started


def resume(job_id: str, *, directory: Path | None = None) -> dict:
    with _lifecycle(directory):
        return _resume(job_id, directory=directory)


def _resume(job_id: str, *, directory: Path | None = None, recovering: bool = False) -> dict:
    """Explicitly retry failed/interrupted/canceled work with its approval."""
    folder = _directory(job_id, directory)
    with _job_lock(folder, "launch.lock"):
        job = get_job(job_id, directory=folder.parent, _launch_owned=True)
        if job.get("cancel_requested"):
            job = _cancel_locked(folder)
        if recovering and job["state"] != State.INTERRUPTED:
            return job
        if not job.get("cancel_requested") and job["state"] in (State.QUEUED, State.RUNNING, State.SUCCEEDED):
            return job
        started = _launch(folder)
    _emit_enqueued(started, resumed=True)
    return started


def cancel(job_id: str, *, directory: Path | None = None) -> dict:
    """Stop one importer, preserving its approval, progress, and delivery receipts.

    Cancellation is durable and never automatically recovered. Explicit resume
    or enqueue of the same approval can continue from its saved receipts. This
    stops the selected importer, not uploads already submitted to a shared spool.
    Completed jobs remain completed; this operation never undoes remote writes.
    """
    folder = _directory(job_id, directory)
    with _lifecycle(directory):
        if not (folder / "job.json").is_file():
            raise JobError("Import job not found.")
        with _job_lock(folder, "launch.lock"):
            return _cancel_locked(folder)


def _cancel_locked(folder: Path) -> dict:
    """Caller owns lifecycle + launch locks; workers never take either lock."""
    with _job_lock(folder, "state.lock"):
        job = _read(folder)
        if job["state"] in (State.SUCCEEDED, State.CANCELED):
            return job
        # Persist intent before signaling. Recovery after a UI crash must finish
        # cancellation instead of restarting a worker killed by that request.
        job.update(cancel_requested=True, updated_at=now_iso(),
                   progress=_progress_message(job["progress"], "Canceling import…"))
        _save(folder, job)
    owned = _signal_worker(folder)
    with _stopped_worker(folder, owned):
        canceled = _update(
            folder, state=State.CANCELED, cancel_requested=False, pid=None,
            pid_identity=None, launch_pid=None, launch_identity=None, finished_at=now_iso(), error=None,
            progress=_progress_message(_read(folder)["progress"],
                "Import canceled. Already imported work is kept; uploads already submitted may finish."),
        )
    # Reported HERE, not by the worker: a cancel reaches a running worker as a
    # signal, which its own terminal path can only read as an interruption. The
    # worker stays silent when `cancel_requested` is set (see `run_worker`), so
    # one stopped import produces exactly one terminal event, and it is the one
    # that says a person decided this.
    _emit_finished(canceled, "canceled")
    return canceled


def clear_all(*, directory: Path | None = None) -> int:
    """Stop owned workers and clear their local jobs, logs, and progress.

    Never visit payload paths: source files, delivery receipts, import journals,
    and previously uploaded research remain intact. Those receipts make the next
    explicitly requested import safe to repeat.
    """
    root = _root(directory)
    if not root.exists():
        return 0
    with _lifecycle(root):
        folders = [folder for folder in root.iterdir()
                   if not folder.is_symlink() and folder.is_dir() and _ID.fullmatch(folder.name)]
        owned = {}
        # Snapshot before the records are removed: what is being thrown away is
        # the whole point of the event, and after the rmtree below nothing can
        # say how much of it was still unfinished.
        discarded = {"jobs": len(folders), "unfinished": 0, "kinds": set()}
        for folder in folders:
            with _job_lock(folder, "launch.lock"):
                job = _read(folder)
                if job["state"] != State.SUCCEEDED:
                    discarded["unfinished"] += 1
                discarded["kinds"].add(str(job.get("kind") or ""))
                owned[folder] = _signal_worker(folder)

        for folder in folders:
            with _stopped_worker(folder, owned[folder]):
                with _job_lock(folder, "state.lock"):
                    shutil.rmtree(folder)
        if folders:
            try:
                _context().emit(
                    _telemetry().EVENT_IMPORT_JOB_CLEARED,
                    jobs=discarded["jobs"],
                    unfinished=discarded["unfinished"],
                    kinds=sorted(kind for kind in discarded["kinds"] if kind),
                )
            except Exception:
                pass
        return len(folders)


def list_jobs(*, recover: bool = False, directory: Path | None = None) -> list[dict]:
    """List local jobs; optionally restart orphan active work on reconnect."""
    root = _root(directory)
    if not root.exists():
        return []
    jobs = []
    for folder in root.iterdir():
        if folder.is_dir() and _ID.fullmatch(folder.name) and (folder / "job.json").exists():
            try:
                job = get_job(folder.name, directory=root)
            except (JobError, OSError):
                # Preserve evidence and keep every other import reachable.
                # This is a display-only row: it is never saved or restarted.
                jobs.append({
                    "id": folder.name, "kind": None, "label": "Unreadable saved import",
                    "state": State.FAILED, "readable": False, "retryable": False,
                    "payload": None, "created_at": "", "updated_at": "",
                    "started_at": None, "finished_at": None, "attempt": 0, "pid": None,
                    "progress": {"message": "The saved import record needs attention."},
                    "error": "This import record could not be read. Its saved files were left unchanged.",
                    "report": [], "log_path": str(folder / "output.log"),
                })
                continue
            if recover and (job.get("cancel_requested") or job["state"] == State.INTERRUPTED):
                # Recheck after taking the lifecycle lock: a cancellation may
                # have completed since the status read, and recovery is never
                # consent to restart that now-canceled job.
                with _lifecycle(root):
                    job = _resume(job["id"], directory=root, recovering=True)
            jobs.append(job)
    return sorted(jobs, key=lambda job: job["created_at"], reverse=True)


def recover_jobs(*, directory: Path | None = None) -> list[dict]:
    """Restart interrupted jobs once; permanent failures await explicit retry."""
    return list_jobs(recover=True, directory=directory)
from probe.cli.imports.jobs.errors import JobError  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.jobs.kind import Kind  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.jobs.store import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    State,
    _ID,
    _check_payload,
    _clean,
    _directory,
    _identity,
    _job_lock,
    _progress_message,
    _read,
    _root,
    _save,
    _try_lock,
    _update,
)
from probe.cli.imports.jobs.telemetry import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _context,
    _emit_enqueued,
    _emit_finished,
    _emit_stalled,
    _origin_stamp,
    _telemetry,
)
from probe.cli.imports.jobs.workers import _alive, _launch, _signal_worker, _stopped_worker  # noqa: E402 -- pieces need each other; the front door loads this one first
