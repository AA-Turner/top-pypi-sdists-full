"""worker processes: launch one for a job, record it, signal or reclaim it and the agent process groups it spawned."""

from __future__ import annotations
import os
import signal
import subprocess
import sys
import threading
import time
from contextlib import contextmanager
from pathlib import Path

from ....foundation.durable.durable import now_iso


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
    folder = _runner._active_job
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
    folder = _runner._active_job
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
    if _runner._active_job is None:
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


def _source_root() -> Path:
    return Path(__file__).resolve().parents[4]  # agent/src


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
    worker_env = dict(os.environ)
    # Replay the approval's structured origin, not a blanket inherited
    # human marker that would also reach the worker's coding agents.
    worker_env.pop("PROBE_DESKTOP_HUMAN", None)
    # The Probe service starts and watches the worker where one answers: it
    # survives this process, a failed start is reported as below, and
    # `probe status` lists it (`probe.service.jobs.imports`). Else it is ours.
    from ...lifecycle import service_calls

    hosted = service_calls.start_import(folder.name, str(folder.parent), pending["attempt"], worker_env)
    if hosted is not None:
        return _record_launch(folder, hosted["pid"])
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
                cwd=folder, start_new_session=True, close_fds=True, env=worker_env,
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
    job = _record_launch(folder, child.pid)

    # Reap direct children even if this wizard stays open for hours. All worker
    # descriptors are detached; this thread owns no part of the worker's life.
    def reap():
        code = child.wait()
        if code:
            _launch_failed(folder, child.pid, pending["attempt"], code)

    threading.Thread(target=reap, daemon=True).start()
    return job


def _record_launch(folder: Path, pid: int) -> dict:
    """The worker `pid` was started for this job (here or by the service)."""
    # The worker may already have claimed the job. Never overwrite its newer
    # state (or a fast completion) with the parent's queued snapshot.
    with _job_lock(folder, "state.lock"):
        job = _read(folder)
        # Keep launch ownership even if the worker claimed or finished before
        # Popen returned. Terminal worker writes clear pid before interpreter
        # shutdown, which can still need to be stopped by Cancel or sign-out.
        identity = _process_identity(pid)
        job.update(launch_pid=pid, launch_identity=identity, updated_at=now_iso())
        if job["state"] == State.QUEUED:
            job.update(pid=pid, pid_identity=identity)
        _save(folder, job)
    return job


def _launch_failed(folder: Path, pid: int, attempt: int, code: int) -> None:
    """The worker `pid`, launched for `attempt`, exited `code` (non-zero): the
    job reads failed if it never claimed it (still queued or interrupted at
    that attempt), so recovery does not start it again and again. Run by the
    launching CLI's reaper, or by the Probe service's report of a worker it
    started (`--launch-failed`)."""
    try:
        with _lifecycle(folder.parent), _job_lock(folder, "state.lock"):
            current = _read(folder)
            if (current["state"] in (State.QUEUED, State.INTERRUPTED)
                    and not current.get("cancel_requested")
                    and current.get("launch_pid") == pid
                    and current["attempt"] == attempt):
                current.update(
                    state=State.FAILED, pid=None, finished_at=now_iso(), updated_at=now_iso(),
                    error=f"The import worker could not start (exit code {code}).",
                )
                _save(folder, current)
    except (OSError, JobError):
        pass  # The next status read reports an unreadable job record.


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
from probe.cli.imports.jobs.errors import JobError, _Interrupted  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.jobs.failure_report import _report_failure  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.jobs.jobs import _cancel_locked, _lifecycle  # noqa: E402 -- pieces need each other; the front door loads this one first
# runner rebinds it (`global`) as a job runs: read it there, never a copy taken at import.
from probe.cli.imports.jobs import runner as _runner  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.jobs.store import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    State,
    _clean,
    _job_lock,
    _progress_message,
    _read,
    _save,
    _try_lock,
    _update,
)
from probe.cli.imports.jobs.telemetry import _context, _emit_finished  # noqa: E402 -- pieces need each other; the front door loads this one first
