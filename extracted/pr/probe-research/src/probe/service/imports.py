"""`import.start`: an approved import's worker, started and watched by the service (plan Q4).

An approved import (`probe wizard`'s Import research / transcripts, the desktop
app's) is journaled by the CLI under `<state>/probe/import-jobs/<job id>/`
(`probe.cli.import_jobs`), which used to start its worker as a detached
process of its own. Where a service answers, the CLI asks it to start that
worker instead:

    the worker       `<the CLI's python> -I -u -m probe.cli.import_jobs <job id>
                     --directory <jobs folder>`, in the job's folder, its
                     output appended to the job's `output.log`, in a session
                     of its own, with the CLI's environment as the CLI handed
                     it over (the worker replays the approval with the
                     credentials and agents that environment reaches): never
                     stored, never logged
    watched          its exit is seen at once; one that ends non-zero before
                     it claimed its job is reported failed, exactly as the
                     CLI's own launcher reports it (`import_jobs.py
                     --launch-failed`, run with the same environment)
    supervised       a running worker keeps the service up and counts as a
                     run in flight for the updater (an in-place CLI update
                     waits for it); `service.status` lists it
    not mid-update   while an in-place update replaces the CLI's files
                     (`held`), no worker starts here (`updating`: the CLI
                     starts its own, as before) and a launch-failure report
                     waits for it to end
    survives         the CLI that asked exiting (the service is its parent),
                     and the service stopping too: `imports.json` (0600,
                     beside the registry) has the next service watch it
    one per attempt  a job is its jobs folder (real path) and its id: one
                     approval in two state folders has one id and two jobs. A
                     job whose worker this service runs for that attempt is not
                     started again (`running`); a newer attempt (the old worker
                     still exiting) gets its own, and every worker stays
                     listed, held and saved until its own process exits

The job's own journal stays the authority on its state (the wizard's Imports
screen, `probe wizard --action imports`): the service knows only that a
process runs.

Stdlib only (the start path; plan S1).
"""

from __future__ import annotations

import json
import os
import stat
import tempfile
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from . import children, procid

IMPORTS_NAME = "imports.json"
IMPORTS_VERSION = 1
#: Workers watched at once (a person approves a handful); past it a start is refused.
MAX_WORKERS = 64
#: `probe.cli.import_jobs._ID`.
JOB_ID_CHARS = frozenset("0123456789abcdef")
JOB_ID_LEN = 32
WORKER_MODULE = "probe.cli.import_jobs"
#: The launch-failure report child past this is killed.
REAP_TIMEOUT_S = 30.0


def valid_job_id(value: object) -> bool:
    return isinstance(value, str) and len(value) == JOB_ID_LEN and set(value) <= JOB_ID_CHARS


@dataclass
class Worker:
    job_id: str
    directory: str
    pid: int
    start_time: str
    attempt: int
    since: float
    #: The environment it was started with: only for a worker this service
    #: started (its launch-failure report runs with it), never saved.
    env: dict | None = None

    @property
    def ident(self) -> tuple:
        """This worker among the service's: its jobs folder, job and process.
        One approval in two state folders has one job id (its payload's hash),
        and a newer attempt's worker may start while the last one exits: each
        is its own entry, kept until its own process exits."""
        return (self.directory, self.job_id, self.pid)

    @property
    def key(self) -> tuple:
        """The pid watcher's key: never a session's or a run hold's."""
        return ("import", *self.ident)

    def public(self) -> dict:
        return {"job_id": self.job_id, "pid": self.pid, "since": self.since}

    def stored(self) -> dict:
        return {
            "job_id": self.job_id, "directory": self.directory, "pid": self.pid,
            "start_time": self.start_time, "attempt": self.attempt, "since": self.since,
        }


def prepare(job_id: str, directory: str) -> tuple[int | None, str, str | None]:
    """`(the job's output.log opened for appending, the jobs folder's real
    path, None)` when `<directory>/<job_id>` is a job folder of this user's (a
    real folder, not a link, holding a regular `job.json`), else `(None,
    directory, why not)`. Reads the disk: never on the loop."""
    if os.name != "posix":
        return None, directory, "POSIX only"
    directory = os.path.realpath(directory)
    folder = Path(directory) / job_id
    try:
        st = folder.lstat()
        if stat.S_ISLNK(st.st_mode) or not stat.S_ISDIR(st.st_mode) or st.st_uid != os.getuid():
            return None, directory, "not a job folder of this user's"
        record = (folder / "job.json").lstat()
        if not stat.S_ISREG(record.st_mode) or record.st_uid != os.getuid():
            return None, directory, "no job record"
    except OSError:
        return None, directory, "no such job"
    try:
        fd = os.open(
            folder / "output.log",
            os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0),
            0o600,
        )
    except OSError as exc:
        return None, directory, f"its log cannot be opened ({exc.strerror or exc})"
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            os.close(fd)
            return None, directory, "its log is not a regular file"
    except OSError:
        os.close(fd)
        return None, directory, "its log cannot be read"
    return fd, directory, None


class ImportWorkers:
    def __init__(
        self,
        path: Path,
        *,
        log: Callable[[str], None],
        changed: Callable[[], None] = lambda: None,
        owner_alive: Callable[[int, str], bool | None] = procid.alive,
        held: Callable[[], bool] = lambda: False,
    ) -> None:
        self.path = path
        self.log = log
        self._changed = changed
        self.owner_alive = owner_alive
        #: True while no CLI process may start (an in-place update replaces its files).
        self.held = held
        #: `Worker.ident` -> worker: every one this service runs or watches.
        self.workers: dict[tuple, Worker] = {}
        #: Launch-failure reports waiting or running (a short child each).
        self._reports = 0
        #: Their tasks (asyncio keeps only a weak reference to a task).
        self._tasks: set = set()
        self._closed = False

    # -- queries -------------------------------------------------------------

    def live(self) -> bool:
        return bool(self.workers) or self._reports > 0

    def public(self) -> list[dict]:
        return [w.public() for w in sorted(self.workers.values(), key=lambda w: w.since)]

    # -- starting (the loop) ---------------------------------------------------

    def refuse(self, directory: str, job_id: str, attempt: int) -> dict | None:
        """The answer when the worker of `directory`'s (a real path) job
        `job_id` for `attempt` cannot be started now, else None."""
        if self._closed:
            return {"started": False, "reason": "stopping"}
        for current in self.workers.values():
            if (current.directory, current.job_id, current.attempt) == (directory, job_id, attempt):
                return {"started": False, "reason": "running", "pid": current.pid, "start_time": current.start_time}
        if self.held():
            return {"started": False, "reason": "updating"}
        if len(self.workers) >= MAX_WORKERS:
            return {"started": False, "reason": "too_many"}
        return None

    def start(self, job_id: str, directory: str, attempt: int, env: dict, log_fd: int) -> Worker | dict:
        """Start `job_id`'s worker, its output on `log_fd` (taken over: always
        closed here): the `Worker` (its `start_time` still to be read:
        `started`), or the answer `{started: false, reason[, pid, start_time]}`
        (`running`: this service runs its worker for that attempt already;
        `updating`, `too_many`, `stopping`, `could_not_start: ...`). The
        caller checked the job folder and opened its log (`prepare`, off the loop)."""
        refused = self.refuse(directory, job_id, attempt)
        if refused is not None:
            os.close(log_fd)
            return refused
        folder = Path(directory) / job_id
        argv = [children.core_python(), "-I", "-u", "-m", WORKER_MODULE, job_id, "--directory", directory]
        holder: dict = {}
        try:
            child = children.spawn_watched(
                argv, env=dict(env), cwd=str(folder), log_fd=log_fd,
                on_exit=lambda code: self._exited(holder.get("worker"), code),
            )
        except OSError as exc:
            return {"started": False, "reason": f"could_not_start: {exc.strerror or exc}"}
        worker = Worker(job_id, directory, child.pid, "", attempt, time.time(), env=dict(env))
        holder["worker"] = worker
        self.workers[worker.ident] = worker
        self.log(f"import {job_id}: worker {child.pid} started (attempt {attempt + 1})")
        self._changed()
        return worker

    def started(self, worker: Worker, start_time: str) -> dict:
        """`worker`'s start time, read off the loop (`ps` on macOS): saved
        with it (the next service watches it by pid AND start time), and
        `import.start`'s answer."""
        worker.start_time = start_time
        if self.workers.get(worker.ident) is worker:
            self.save()
        return {"started": True, "pid": worker.pid, "start_time": start_time}

    def _exited(self, worker: Worker | None, code: int) -> None:
        """A worker this service started exited with `code`."""
        if worker is None or self.workers.get(worker.ident) is not worker:
            return
        del self.workers[worker.ident]
        self.save()
        self.log(f"import {worker.job_id}: worker {worker.pid} exited ({code})")
        if code != 0 and not self._closed and worker.env is not None:
            self._report_launch_failure(worker, code)
        self._changed()

    def _report_launch_failure(self, worker: Worker, code: int) -> None:
        """`import_jobs.py --launch-failed`: the job reads failed only when the
        worker never claimed it (that code decides; the service knows no job
        format), so a resume does not start it again and again."""
        import asyncio

        status = 128 - code if code < 0 else code
        argv = [
            children.core_python(), "-I", "-m", WORKER_MODULE, worker.job_id, "--directory", worker.directory,
            "--launch-failed", str(worker.pid), "--attempt", str(worker.attempt), "--exit-code", str(status),
        ]

        async def report() -> None:
            try:
                while self.held() and not self._closed:
                    # Not on files an in-place update is replacing.
                    await asyncio.sleep(1.0)
                await children.run_command(
                    argv, env=dict(worker.env or {}), cwd=str(Path(worker.directory) / worker.job_id),
                    timeout=REAP_TIMEOUT_S,
                )
            except Exception as exc:  # noqa: BLE001 -- the next status read still says it stopped
                self.log(f"import {worker.job_id}: the launch-failure report failed: {exc!r}")
            finally:
                self._reports -= 1
                self._changed()

        self._reports += 1
        task = asyncio.ensure_future(report())
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    def _watched_exit(self, worker: Worker) -> None:
        """A worker of an earlier service exited (no status: it is not ours to wait for)."""
        if self.workers.get(worker.ident) is not worker:
            return
        del self.workers[worker.ident]
        self.save()
        self.log(f"import {worker.job_id}: worker {worker.pid} exited")
        self._changed()

    # -- disk --------------------------------------------------------------------

    def save(self) -> None:
        payload = {"v": IMPORTS_VERSION, "workers": [w.stored() for w in self.workers.values()]}
        try:
            fd, tmp = tempfile.mkstemp(prefix=self.path.name + ".", suffix=".tmp", dir=str(self.path.parent))
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as handle:
                    json.dump(payload, handle, separators=(",", ":"))
                os.replace(tmp, self.path)
            except BaseException:
                try:
                    os.unlink(tmp)
                except OSError:
                    pass
                raise
        except OSError:
            pass  # the job's own journal still says what runs

    def load(self, watch: Callable) -> list[Worker]:
        """The workers an earlier service started that still run, each watched
        (`watch(key, pid, start, callback)`) until it exits."""
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return []
        if not isinstance(data, dict) or data.get("v") != IMPORTS_VERSION:
            return []
        kept: list[Worker] = []
        for raw in data.get("workers") or []:
            try:
                worker = Worker(
                    str(raw["job_id"]), str(raw["directory"]), int(raw["pid"]), str(raw["start_time"]),
                    int(raw["attempt"]), float(raw["since"]),
                )
            except (KeyError, TypeError, ValueError):
                continue
            if not valid_job_id(worker.job_id) or worker.pid <= 1 or not worker.start_time:
                continue
            if self.owner_alive(worker.pid, worker.start_time) is False:
                continue
            self.workers[worker.ident] = worker
            kept.append(worker)
            watch(worker.key, worker.pid, worker.start_time, lambda w=worker: self._watched_exit(w))
        self.save()
        return kept

    def close(self) -> None:
        """The service stops: its workers go on (their own sessions), and the
        next service watches them from `imports.json`."""
        self._closed = True
        for worker in self.workers.values():
            worker.env = None
