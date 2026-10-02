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

import argparse
import errno
import fcntl
import hashlib
import json
import math
import os
import re
import signal
import shutil
import socket
import subprocess
import sys
import threading
import time
from contextlib import ExitStack, contextmanager, redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from probe._compat import StrEnum
from pathlib import Path
from urllib.error import HTTPError, URLError

from ..sdk.durable import file_lock, now_iso, write_text_atomic


#: How often a worker that is still waiting for a connection re-reports the
#: stall. Ten minutes keeps an overnight disconnection to a readable handful of
#: events while still bounding how long a new stall stays invisible.
STALL_REPORT_INTERVAL_S = 600.0


class Kind(StrEnum):
    TRANSCRIPTS = "transcripts"
    FOLDER = "folder"


class State(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    INTERRUPTED = "interrupted"
    CANCELED = "canceled"


class JobError(RuntimeError):
    """A safe, user-facing failure reason; never include credentials in it."""


class RetryableJobError(JobError):
    """A known temporary connection failure while replaying approved work."""


def is_retryable_error(exc: BaseException) -> bool:
    """Recognize transport failures without guessing from exception messages.

    Authored JobError refusals are final even if they wrap a network error.
    Unknown wrappers may preserve a typed transport error as their cause.
    """
    import httpx
    from ..sdk.errors import AuthError, RosError, ScopeError, TransportError

    seen = set()
    while exc is not None and id(exc) not in seen:
        seen.add(id(exc))
        if isinstance(exc, RetryableJobError):
            return True
        if isinstance(exc, (JobError, AuthError, ScopeError)):
            return False
        if isinstance(exc, RosError) and exc.status is not None:
            return exc.status in (408, 429) or 500 <= exc.status <= 599
        if isinstance(exc, HTTPError):
            return exc.code in (408, 429) or 500 <= exc.code <= 599
        if isinstance(exc, httpx.HTTPStatusError):
            status = exc.response.status_code
            return status in (408, 429) or 500 <= status <= 599
        if isinstance(exc, (
            TransportError, ConnectionError, TimeoutError, socket.gaierror,
            httpx.NetworkError, httpx.TimeoutException, httpx.RemoteProtocolError,
        )):
            return True
        if isinstance(exc, OSError) and exc.errno in {
            errno.ECONNABORTED, errno.ECONNREFUSED, errno.ECONNRESET,
            errno.EHOSTUNREACH, errno.ENETDOWN, errno.ENETUNREACH, errno.ETIMEDOUT,
        }:
            return True
        # URLError also wraps invalid URLs and local file failures; only its
        # typed connection cause qualifies. Never retry arbitrary OSError.
        exc = exc.reason if isinstance(exc, URLError) and isinstance(exc.reason, BaseException) else exc.__cause__
    return False


class _Interrupted(BaseException):
    pass


_ID = re.compile(r"[0-9a-f]{32}\Z")
_SECRET_KEYS = {
    "token", "access_token", "refresh_token", "api_key", "password", "secret",
    "authorization", "credential", "credentials", "env", "environment",
}
_active_job: Path | None = None  # One worker per process; launch threads share it.


def prepared_approval_digest() -> str | None:
    """The automatic folder worker's durable transition into exact delivery."""
    return _read(_active_job).get("prepared_approval") if _active_job is not None else None


def remember_prepared_approval(digest: str) -> None:
    """A missing plan after this marker is an error, never permission to replan."""
    if _active_job is not None:
        _update(_active_job, prepared_approval=digest)


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


# -- funnel ------------------------------------------------------------------
# The wizard's own `backfill.summary` fires when it HANDS WORK OFF to one of
# these workers, and reports `partial` with 0% coverage for everything still
# queued -- which is every onboarding import, every time. So "did the import
# this person approved actually finish?" is answerable only from here.
#
# Metadata only, same contract as the rest of client telemetry: counts,
# booleans, durations and enum outcomes. Never a label (it carries a folder
# name), never `error` (lane prose can embed a path), never a payload field.


def _telemetry():
    """The telemetry module, or None when this process cannot reach it.

    A worker runs from a PINNED source tree -- the copy of `probe/` that was on
    disk when its approval was made, so an upgrade mid-import cannot change the
    code replaying it -- and that tree carries only the modules the lanes need.
    An unconditional import here turned every detached worker into an immediate
    ImportError: the import did not merely go unreported, it stopped happening.
    Telemetry is allowed to be absent; it is never allowed to be load-bearing.
    """
    try:
        from . import telemetry
    except Exception:
        return None
    return telemetry


def _context(job: dict | None = None):
    """This process's funnel handle, or None. Never raises.

    With a job, the APPROVING session replayed off its record; without one,
    whatever context this process already started.
    """
    telemetry = _telemetry()
    if telemetry is None:
        return None
    try:
        return telemetry.current() if job is None else telemetry.job_context(job.get("origin"))
    except Exception:
        return None


def _origin_stamp():
    telemetry = _telemetry()
    if telemetry is None:
        return None
    try:
        return telemetry.origin_stamp()
    except Exception:
        return None


def _job_props(job: dict) -> dict:
    """The shape every import_job event shares. Never raises."""
    from .import_progress import counts

    props = {"kind": str(job.get("kind") or ""), "job_id": job.get("id"),
             "attempt": job.get("attempt")}
    try:
        done, total = counts(job)
        props["units_done"] = done
        props["units_total"] = total
        if total:
            props["coverage_pct"] = round(100.0 * min(done or 0, total) / total, 1)
    except Exception:
        pass
    return props


def _elapsed_seconds(job: dict) -> float | None:
    for field in ("started_at", "created_at"):
        try:
            started = datetime.fromisoformat(job[field].replace("Z", "+00:00"))
            if started.tzinfo is None:
                started = started.replace(tzinfo=timezone.utc)
            return round(max(0.0, time.time() - started.timestamp()), 1)
        except Exception:
            continue
    return None


def _emit_finished(job: dict, outcome, *, tel=None, **extra) -> None:
    try:
        tel = tel or _context(job)
        tel.emit(
            _telemetry().EVENT_IMPORT_JOB_FINISHED,
            outcome=str(outcome),
            duration_seconds=_elapsed_seconds(job),
            **_job_props(job),
            **extra,
        )
    except Exception:
        pass  # observability must never become observable


# -- telling the person -------------------------------------------------------
# The funnel above reaches US. Nothing in it reaches the researcher, and a
# detached worker has no terminal to print to: an overnight import that stops at
# 03:00 is invisible until somebody thinks to reopen the import screen. So a
# terminal FAILURE also asks the server to email the account that approved it.
#
# Everything here is best-effort in exactly the sense the funnel is: it runs
# after the job record is already durable, it never raises, and a job that could
# not be reported is still a job whose own record says what happened.


#: How long the worker will wait on the report before giving up and exiting.
#: A failed import is already finished; nobody is served by a worker that lingers
#: on a slow network to send a courtesy email.
_REPORT_TIMEOUT_S = 10.0


def _job_context_name(job: dict) -> str | None:
    """The saved CLI context this job's lane authenticates with.

    The two lanes spell it differently because they pin different things: the
    transcript lane pins a whole account identity it re-verifies before
    uploading, the folder lane pins a destination scope. Neither shape is worth
    changing for a notification, so this reads both.
    """
    payload = job.get("payload")
    if not isinstance(payload, dict):
        return None
    account = payload.get("account")
    if isinstance(account, dict) and isinstance(account.get("context"), str):
        return account["context"]
    return payload.get("context") if isinstance(payload.get("context"), str) else None


def _report_digest(job: dict) -> str:
    """What makes one failure DIFFERENT from the one already reported.

    The attempt number alone is not enough: a job relaunched by recovery can
    fail before `run_worker` ever increments it, and mailing on every one of
    those turns a crash loop into an inbox. The error text alone is not enough
    either: a person who fixed the cause, resumed, and hit the same wall must
    hear about it again.
    """
    canonical = json.dumps(
        [job.get("attempt"), str(job.get("state") or ""), str(job.get("error") or "")],
        sort_keys=True,
    )
    return hashlib.sha256(canonical.encode()).hexdigest()[:32]


def _post_failure_report(context: str, job_id: str, body: dict) -> None:
    """One authenticated POST. Its own function so tests can replace it.

    A TRANSPORT rather than a `Client`: this needs one request, and a client
    would also stand up an outbox and a journal for a process that is on its way
    out. Imported inside the call for the reason `_telemetry` documents -- a
    worker replays from a PINNED source tree, and a module that is missing there
    must cost a notification, never the import.
    """
    from ..sdk.config import resolve
    from ..sdk.transport import Transport

    transport = Transport(
        resolve(context=context), timeout=_REPORT_TIMEOUT_S, surface="cli", attribution="backfill"
    )
    try:
        transport.post(f"/v1/import-jobs/{job_id}/failure", body, idempotent=True)
    finally:
        transport.close()


def _report_failure(folder: Path, job: dict, *, failure_kind: str | None = None) -> bool:
    """Ask the server to email this job's owner. Never raises.

    Returns whether a report was SENT -- False covers "already reported",
    "no saved context to authenticate with", and every transport failure.

    THE DEDUPE LIVES HERE, not on the server, because this is the only side that
    holds a durable per-job record and can therefore tell a new failure from the
    same failure being observed twice. The server keeps a short in-process window
    as a backstop; it cannot survive a restart and is not the authority.
    """
    try:
        reason = str(job.get("error") or "").strip()
        if not reason:
            return False
        digest = _report_digest(job)
        if job.get("notified") == digest:
            return False
        context = _job_context_name(job)
        if context is None:
            return False
        done, total = None, None
        try:
            from .import_progress import counts

            done, total = counts(job)
        except Exception:
            pass
        _post_failure_report(context, job["id"], {
            "kind": str(job.get("kind") or ""),
            "outcome": "launch_failed" if failure_kind in ("reclaim", "launch") else "failed",
            "reason": _clean(reason),
            "failure_kind": failure_kind,
            "attempt": job.get("attempt"),
            "units_done": done,
            "units_total": total,
            "duration_seconds": _elapsed_seconds(job),
            # The researcher's own machine name, so an email that arrives on a
            # phone says WHICH laptop to go back to. Bounded and re-validated
            # server-side; a host that cannot name itself simply omits it.
            "machine": _machine_label(),
        })
    except Exception:
        return False  # a notification must never become the failure
    # Stamped only after the POST returns: a report that never left must be
    # retried by the next observation, not suppressed by this one.
    try:
        _update(folder, notified=digest)
    except Exception:
        pass
    return True


def _machine_label() -> str | None:
    try:
        name = socket.gethostname().split(".")[0].strip()
    except Exception:
        return None
    return name[:64] if name else None


def _emit_enqueued(job: dict, *, resumed: bool) -> None:
    """The approval becoming durable work -- the funnel's join to the lane
    events, emitted in the APPROVING process so it carries that session."""
    try:
        _context().emit(
            _telemetry().EVENT_IMPORT_JOB_ENQUEUED,
            resumed=resumed,
            state=str(job.get("state") or ""),
            **_job_props(job),
        )
    except Exception:
        pass


def _emit_stalled(job: dict, reason, *, tel=None, **extra) -> None:
    try:
        tel = tel or _context(job)
        tel.emit(
            _telemetry().EVENT_IMPORT_JOB_STALLED,
            reason=str(reason),
            age_seconds=_elapsed_seconds(job),
            **_job_props(job),
            **extra,
        )
    except Exception:
        pass


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


class _ProgressEstimate:
    """Estimate delivery time from observed work, never queue or scan duration."""

    def __init__(self, *, start_on_advance: bool = False):
        self.baseline = None
        self.latest = None
        self.start_on_advance = start_on_advance
        self.ready = not start_on_advance

    def update(self, previous: dict, fields: dict) -> dict:
        phase = fields.get("phase", previous.get("phase"))
        changed_phase = "phase" in fields and phase != previous.get("phase")
        result = {} if changed_phase else {
            key: previous[key] for key in (
                "completed", "total", "phase", "stage", "stage_completed", "stage_total",
                "completion_completed", "completion_total", "completion_ids",
                "eta_seconds", "eta_updated_at",
            ) if key in previous
        }
        result.update(fields)
        counter_keys = ("completion_completed", "completion_total") if any(
            key in result for key in ("completion_completed", "completion_total")
        ) else ("completed", "total")
        completed_key, total_key = counter_keys
        measured = all(
            isinstance(result.get(key), (int, float))
            and not isinstance(result[key], bool) and math.isfinite(result[key])
            for key in counter_keys
        ) and 0 <= result[completed_key] <= result[total_key] and result[total_key] > 0
        if changed_phase or phase == "scanning" or fields.get("waiting_for_connection") or not measured:
            self.baseline = self.latest = None
            result.pop("eta_seconds", None)
            result.pop("eta_updated_at", None)
            if phase == "scanning" or fields.get("waiting_for_connection") or not measured:
                return result
        # A message-only update retains the previous observation, but does not
        # manufacture another sample or count elapsed connection retry time.
        if any(key not in fields for key in counter_keys):
            return result
        now = time.monotonic()
        completed, total = result[completed_key], result[total_key]
        if self.baseline is None or self.latest is None or (
            self.latest[1:] != (total, counter_keys) or completed < self.latest[0]
        ):
            self.baseline = (now, completed)
            self.latest = (completed, total, counter_keys)
            self.ready = not self.start_on_advance
            result.pop("eta_seconds", None)
            result.pop("eta_updated_at", None)
            return result
        if completed > self.latest[0]:
            if not self.ready:
                # Folder work can prepare for minutes before its first new
                # receipt. Start timing at that receipt, including on resume
                # when the initial count already includes earlier deliveries.
                self.baseline = (now, completed)
                self.latest = (completed, total, counter_keys)
                self.ready = True
                result.pop("eta_seconds", None)
                result.pop("eta_updated_at", None)
                return result
            elapsed, advanced = now - self.baseline[0], completed - self.baseline[1]
            if elapsed >= 1 and advanced > 0:
                result["eta_seconds"] = (total - completed) * elapsed / advanced
                result["eta_updated_at"] = now_iso()
        self.latest = (completed, total, counter_keys)
        return result


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


@contextmanager
def _lifecycle(directory: Path | None):
    root = _root(directory)
    # Outside the removable journal tree so all sessions keep the same lock.
    with file_lock(root.parent / (root.name + ".lock")):
        yield


def _process_identity(pid: int) -> str | None:
    """Distinguish PID reuse, including a restart of the whole machine."""
    try:
        stat = Path(f"/proc/{pid}/stat").read_text().rpartition(")")[2].split()
        if stat[0] == "Z":
            return None
        boot = Path("/proc/sys/kernel/random/boot_id").read_text().strip()
        return f"{boot}:{stat[19]}"
    except (OSError, IndexError):
        try:
            result = subprocess.run(
                ["ps", "-p", str(pid), "-o", "lstart="],
                capture_output=True, text=True, timeout=1, check=False,
            )
            return result.stdout.strip() or None
        except (OSError, subprocess.SubprocessError):
            return None


def _alive(pid, identity=None) -> bool:
    if not isinstance(pid, int) or pid < 1:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return identity is not None and identity == _process_identity(pid)


def register_child(pid: int) -> None:
    """Persist a worker-owned coding-agent process group before it can run."""
    folder = _active_job
    if folder is None:
        return
    identity = _process_identity(pid)
    try:
        group = os.getpgid(pid)
    except OSError as exc:
        raise JobError("The coding-agent process exited before it could be registered.") from exc
    if identity is None or group != pid:
        raise JobError("Could not establish ownership of the coding-agent process group.")
    with _job_lock(folder, "state.lock"):
        job = _read(folder)
        if job.get("cancel_requested") or job["state"] == State.CANCELED:
            raise _Interrupted
        children = [child for child in job.get("children", []) if child["pid"] != pid]
        children.append({"pid": pid, "pgid": group, "identity": identity})
        job.update(children=children, updated_at=now_iso())
        _save(folder, job)


def unregister_child(pid: int) -> None:
    """Forget a coding agent only after its process has stopped/reaped."""
    folder = _active_job
    if folder is None:
        return
    with _job_lock(folder, "state.lock"):
        job = _read(folder)
        children = [child for child in job.get("children", []) if child["pid"] != pid]
        job.update(children=children, updated_at=now_iso())
        _save(folder, job)


def spawn_child(argv, **kwargs):
    """Popen with a durable launch gate inside import workers.

    The gate uses a separate inherited descriptor, preserving the agent's stdin.
    If the worker dies before the registry write, pipe EOF exits the bootstrap
    without starting the agent. Once released, its PID/group already has a
    durable owner. Exec preserves that PID and its process-start identity.
    """
    if _active_job is None:
        return subprocess.Popen(argv, **kwargs)
    read_fd, write_fd = os.pipe()
    child = None
    gate = (
        "import os,sys; fd=int(sys.argv[1]); ready=os.read(fd,1); os.close(fd); "
        "os._exit(1) if ready != b'1' else None; os.execvp(sys.argv[2],sys.argv[2:])"
    )
    try:
        kwargs = {**kwargs, "start_new_session": True, "close_fds": True,
                  "pass_fds": (*kwargs.get("pass_fds", ()), read_fd)}
        child = subprocess.Popen([sys.executable, "-c", gate, str(read_fd), *argv], **kwargs)
        register_child(child.pid)
        os.write(write_fd, b"1")
        return child
    except BaseException:
        if child is not None:
            child.kill()
            child.wait()
            unregister_child(child.pid)
        raise
    finally:
        os.close(read_fd)
        os.close(write_fd)


def _reclaim_children(folder: Path) -> None:
    """Stop prior owned agent groups before another attempt can launch."""
    children = _read(folder).get("children", [])
    for child in children:
        pid, identity = child["pid"], child["identity"]
        if not _alive(pid, identity):
            continue  # Gone, or its PID was reused; neither is ours to signal.
        try:
            if child["pgid"] != pid or os.getpgid(pid) != pid:
                raise JobError("A previous coding agent still runs without its saved process group.")
            for number, grace in ((signal.SIGTERM, 3.0), (signal.SIGKILL, 1.0)):
                if not _alive(pid, identity):
                    break
                os.killpg(pid, number)
                deadline = time.monotonic() + grace
                while _alive(pid, identity) and time.monotonic() < deadline:
                    time.sleep(0.05)
            if _alive(pid, identity):
                raise JobError("The previous coding agent could not be stopped; the import was not restarted.")
        except ProcessLookupError:
            pass
        except PermissionError as exc:
            raise JobError("The previous coding agent could not be stopped with this account.") from exc
    if children:
        _update(folder, children=[])


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


def _source_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _launch(folder: Path) -> dict:
    """Called under launch.lock; a second worker still needs worker.lock."""
    if _read(folder).get("cancel_requested"):
        _cancel_locked(folder)
    with _try_lock(folder / "worker.lock") as acquired:
        if not acquired:
            return _read(folder)
        try:
            _reclaim_children(folder)
        except JobError as exc:
            failed = _update(folder, state=State.FAILED, error=_clean(exc), finished_at=now_iso())
            _emit_finished(failed, "launch_failed", tel=_context(), failure_kind="reclaim")
            _report_failure(folder, failed, failure_kind="reclaim")
            return failed
    pending = _update(
        folder, state=State.QUEUED, pid=None, pid_identity=None, launch_pid=None, launch_identity=None,
        error=None, finished_at=None, cancel_requested=False,
        progress=_progress_message(_read(folder)["progress"], "Queued to resume the approved import."),
    )
    try:
        descriptor = os.open(folder / "output.log", os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        with os.fdopen(descriptor, "ab", buffering=0) as output:
            child = subprocess.Popen(
                [sys.executable, "-u", "-c",
                 "import sys; sys.path.insert(0, sys.argv.pop(1)); "
                 "from probe.cli.import_jobs import main; main()",
                 str(_source_root()), folder.name,
                 "--directory", str(folder.parent)],
                stdin=subprocess.DEVNULL, stdout=output, stderr=output,
                cwd=folder, start_new_session=True, close_fds=True,
            )
    except OSError as exc:
        failed = _update(
            folder, state=State.FAILED, finished_at=now_iso(),
            error=f"Could not start the import worker ({type(exc).__name__}).",
        )
        _emit_finished(
            failed, "launch_failed", tel=_context(), failure_kind=type(exc).__name__,
        )
        _report_failure(folder, failed, failure_kind="launch")
        return failed
    # The worker may already have claimed the job. Never overwrite its newer
    # state (or a fast completion) with the parent's queued snapshot.
    with _job_lock(folder, "state.lock"):
        job = _read(folder)
        # Keep launch ownership even if the worker claimed or finished before
        # Popen returned. Terminal worker writes clear pid before interpreter
        # shutdown, which can still need to be stopped by Cancel or sign-out.
        identity = _process_identity(child.pid)
        job.update(launch_pid=child.pid, launch_identity=identity, updated_at=now_iso())
        if job["state"] == State.QUEUED:
            job.update(pid=child.pid, pid_identity=identity)
        _save(folder, job)
    # Reap direct children even if this wizard stays open for hours. All worker
    # descriptors are detached; this thread owns no part of the worker's life.
    def reap():
        code = child.wait()
        if not code:
            return
        try:
            with _lifecycle(folder.parent), _job_lock(folder, "state.lock"):
                current = _read(folder)
                if (current["state"] in (State.QUEUED, State.INTERRUPTED)
                        and not current.get("cancel_requested")
                        and current.get("launch_pid") == child.pid
                        and current["attempt"] == pending["attempt"]):
                    current.update(
                        state=State.FAILED, pid=None, finished_at=now_iso(), updated_at=now_iso(),
                        error=f"The import worker could not start (exit code {code}).",
                    )
                    _save(folder, current)
        except (OSError, JobError):
            pass  # The next status read reports an unreadable job record.

    threading.Thread(target=reap, daemon=True).start()
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
    resumed = False
    with _job_lock(folder, "launch.lock"):
        if (folder / "job.json").exists():
            job = get_job(job_id, directory=folder.parent, _launch_owned=True)
            if not job.get("cancel_requested") and job["state"] not in (State.INTERRUPTED, State.CANCELED):
                return job
            resumed = True
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
    _emit_enqueued(started, resumed=resumed)
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


def _signal_worker(folder: Path) -> tuple[int, str] | None:
    """Signal only a saved, verified worker; caller holds the lifecycle lock."""
    job = _read(folder)
    pid = job.get("pid")
    identity = job.get("pid_identity")
    if not _alive(pid, identity):
        pid = job.get("launch_pid")
        # Older journals used one identity for both fields.
        identity = job.get("launch_identity", job.get("pid_identity"))
        if not _alive(pid, identity):
            return None
    if pid == os.getpid():
        raise JobError("An import is running in this process; it could not be stopped.")
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    except PermissionError as exc:
        raise JobError("An import worker could not be stopped with this account.") from exc
    return pid, identity


@contextmanager
def _stopped_worker(folder: Path, owned: tuple[int, str] | None):
    """Reclaim the worker and agents, retaining worker.lock during finalization."""
    # A free lifetime lock alone is insufficient: interpreter shutdown may run
    # after it is released. Wait for both the lock and the verified process.
    for grace, force in ((5.0, False), (2.0, True)):
        if force and owned and _alive(*owned):
            try:
                os.kill(owned[0], signal.SIGKILL)
            except ProcessLookupError:
                pass
            except PermissionError as exc:
                raise JobError("An import worker could not be stopped with this account.") from exc
        deadline = time.monotonic() + grace
        while True:
            with _try_lock(folder / "worker.lock") as unowned:
                if unowned and (not owned or not _alive(*owned)):
                    _reclaim_children(folder)
                    yield
                    return
            if time.monotonic() >= deadline:
                break
            time.sleep(0.05)
    raise JobError("An import worker is still stopping. Its local history was kept; try again.")


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


def _dispatch(kind: str, payload: dict, progress):
    if kind == Kind.TRANSCRIPTS:
        from .backfill_transcripts import run_background_job
        return run_background_job(payload, progress=progress)
    from .backfill_coverage import CoverageError
    from .backfill_import import run_background_job

    try:
        return run_background_job(payload, progress=progress)
    except CoverageError as exc:
        raise JobError(str(exc)) from exc


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


def run_worker(job_id: str, *, directory: Path | None = None) -> int:
    """Run one approved request under a process-lifetime ownership lock."""
    global _active_job

    folder = _directory(job_id, directory)
    with ExitStack() as ownership:
        # Status reads hold state.lock while briefly probing worker.lock. Wait
        # for that probe before claiming ownership, or a newborn worker can
        # mistake the reader for another worker and exit without an attempt.
        # The lifetime lock stays nonblocking: an existing worker can need
        # state.lock for progress, so waiting on its lock here would deadlock.
        with _job_lock(folder, "state.lock"):
            if not ownership.enter_context(_try_lock(folder / "worker.lock")):
                return 0
        job = _read(folder)
        if job.get("cancel_requested") or job["state"] in (State.SUCCEEDED, State.CANCELED):
            return 0
        # A new process cannot inherit the approving wizard's context object,
        # so it replays that session off the record. Without this the
        # completion lands in its own session and no funnel can join it to the
        # approval that asked for it.
        tel = _context(job)
        try:
            _reclaim_children(folder)
        except JobError as exc:
            failed = _update(folder, state=State.FAILED, error=_clean(exc), finished_at=now_iso())
            _emit_finished(failed, "launch_failed", tel=tel, failure_kind="reclaim")
            _report_failure(folder, failed, failure_kind="reclaim")
            return 1
        job = _update(
            folder, state=State.RUNNING, pid=os.getpid(),
            pid_identity=_process_identity(os.getpid()), attempt=job["attempt"] + 1,
            started_at=now_iso(), finished_at=None, error=None,
            progress=_progress_message(job["progress"], "Starting the approved import."),
        )
        if job.get("cancel_requested"):
            return 130

        estimate = _ProgressEstimate(start_on_advance=job["kind"] == Kind.FOLDER)
        progress_lock = threading.Lock()

        def progress(message: str, **fields):
            if _read(folder).get("cancel_requested"):
                raise _Interrupted
            _check_payload(fields)
            # Folder callbacks can arrive from several worker threads. Keep
            # their observation and persisted state in the same order.
            with progress_lock:
                previous_progress = _read(folder)["progress"]
                if (job["kind"] == Kind.TRANSCRIPTS and "completion_ids" in fields
                        and fields.get("phase", previous_progress.get("phase")) != "scanning"
                        and previous_progress.get("phase") != "scanning"):
                    # A retry checks the same immutable approved sessions from
                    # the beginning. Already-finalized receipts remain valid;
                    # their identity must not disappear during that replay.
                    identities = [*previous_progress.get("completion_ids", []), *fields["completion_ids"]]
                    if all(isinstance(item, (list, tuple)) and len(item) == 2
                           and all(isinstance(part, str) for part in item) for item in identities):
                        fields["completion_ids"] = [list(item) for item in sorted({tuple(item) for item in identities})]
                        fields["completion_completed"] = len(fields["completion_ids"])
                update = estimate.update(previous_progress, fields)
                update["message"] = _clean(message)
                _update(folder, progress=update)
            print(f"{now_iso()} {_clean(message)}", flush=True)

        def interrupt(_signal, _frame):
            raise _Interrupted

        previous_job, _active_job = _active_job, folder
        previous = {}
        if threading.current_thread() is threading.main_thread():
            for number in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
                previous[number] = signal.getsignal(number)
                signal.signal(number, signal.SIG_IGN if number == signal.SIGHUP else interrupt)
        try:
            descriptor = os.open(folder / "output.log", os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
            with os.fdopen(descriptor, "a", encoding="utf-8", buffering=1) as output:
                with redirect_stdout(output), redirect_stderr(output):
                    print(f"{now_iso()} Starting attempt {job['attempt']}.", flush=True)
                    try:
                        with _serial_lane(job, folder):
                            retry_delay = 2
                            retries = 0
                            waited = 0.0
                            # A disconnected laptop retries forever, so the
                            # stall is a LEVEL and not an edge. Report the
                            # entry into it, then at most once per
                            # STALL_REPORT_INTERVAL_S of continued waiting:
                            # an event per retry would turn one bad afternoon
                            # into hundreds.
                            reported = 0.0
                            while True:
                                if _read(folder).get("cancel_requested"):
                                    raise _Interrupted
                                try:
                                    result = _dispatch(job["kind"], job["payload"], progress)
                                    break
                                except RetryableJobError as exc:
                                    # No coding-agent process may survive into
                                    # the next replay of this same approval.
                                    from . import backfill

                                    backfill.stop_all()
                                    _reclaim_children(folder)
                                    retries += 1
                                    progress(
                                        f"Waiting for connection. Retrying in {retry_delay}s. {_clean(exc)}",
                                        waiting_for_connection=True,
                                        retry_in=retry_delay, network_retries=retries,
                                    )
                                    if retries == 1 or waited - reported >= STALL_REPORT_INTERVAL_S:
                                        reported = waited
                                        _emit_stalled(
                                            _read(folder), "waiting_for_connection", tel=tel,
                                            network_retries=retries,
                                            waiting_seconds=round(waited, 1),
                                        )
                                    waited += retry_delay
                                    # Keep the lifetime locks, but no state lock,
                                    # while waiting. Signals still interrupt it.
                                    time.sleep(retry_delay)
                                    retry_delay = min(retry_delay * 2, 60)
                                    progress("Connection retry: resuming saved import progress.")
                        lines = result.splitlines() if isinstance(result, str) else list(result or [])
                        for line in lines:
                            print(_clean(line), flush=True)
                        done = _update(
                            folder, state=State.SUCCEEDED, pid=None, finished_at=now_iso(),
                            report=[_clean(line) for line in lines[-20:]],
                            progress=_progress_message(_read(folder)["progress"], "Import finished."),
                        )
                        _emit_finished(
                            done, "succeeded", tel=tel, network_retries=retries or None,
                        )
                        return 0
                    except (_Interrupted, KeyboardInterrupt):
                        stopped = _update(
                            folder, state=State.INTERRUPTED, pid=None, finished_at=now_iso(),
                            progress=_progress_message(_read(folder)["progress"], "Worker interrupted; saved work can resume."),
                        )
                        if not stopped.get("cancel_requested"):
                            # A cancel arrives as a signal and lands here too;
                            # `_cancel_locked` owns that event and knows it was
                            # deliberate. Two terminal events for one job would
                            # be one import counted twice, as both.
                            _emit_finished(stopped, "interrupted", tel=tel)
                        return 130
                    except Exception as exc:
                        # HTTP exception strings can carry signed URLs or auth
                        # headers. Only lane-authored JobError prose is displayable.
                        reason = _clean(exc) if isinstance(exc, JobError) else f"Import failed ({type(exc).__name__})."
                        print(reason, flush=True)
                        broken = _update(
                            folder, state=State.FAILED, pid=None, finished_at=now_iso(), error=reason,
                            progress=_progress_message(_read(folder)["progress"], "Import needs attention before retrying."),
                        )
                        # The TYPE, never `reason`: lane-authored prose is safe
                        # to show a person but can name a folder, and a
                        # formatted httpx error can carry a signed URL.
                        _emit_finished(
                            broken, "failed", tel=tel,
                            failure_kind="refused" if isinstance(exc, JobError) else type(exc).__name__,
                            network_retries=retries or None,
                        )
                        _report_failure(
                            folder, broken,
                            failure_kind="refused" if isinstance(exc, JobError) else type(exc).__name__,
                        )
                        return 1
        finally:
            try:
                from . import backfill

                backfill.stop_all()
                _reclaim_children(folder)
            except JobError as exc:
                broken = _update(
                    folder, state=State.FAILED, pid=None, error=_clean(exc), finished_at=now_iso(),
                )
                _emit_finished(broken, "failed", tel=tel, failure_kind="cleanup")
                _report_failure(folder, broken, failure_kind="cleanup")
                raise
            finally:
                _active_job = previous_job
                for number, handler in previous.items():
                    signal.signal(number, handler)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_id")
    parser.add_argument("--directory", type=Path)
    args = parser.parse_args()
    raise SystemExit(run_worker(args.job_id, directory=args.directory))


if __name__ == "__main__":
    # Hooks import the canonical module. `-m` must share their worker context.
    sys.modules["probe.cli.import_jobs"] = sys.modules[__name__]
    main()
