"""AgentJobManager — spawn, supervise, persist, and re-adopt jobs.

Correctness properties (the exit-255 fix):

* The child runs in its own session/process group (``start_new_session=True``),
  so signals hit the whole tree and a daemon crash never SIGHUPs the job.
* stdout/stderr are file descriptors onto spool files — the daemon holds no
  pipes, so the job's output path is independent of any connection and a daemon
  restart doesn't break it.
* Every job has a state dir with ``meta.json`` (start) and ``exit.json`` (reap).
  A reconnecting world reads the persisted outcome no matter how long it was
  gone.
* On daemon boot, jobs with meta but no exit.json are re-adopted if their pid is
  alive, else recorded ``lost`` — explicit "unknown outcome", not a guess.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import os
import shutil
import signal
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from plato.agents.daemon.spawn_env import login_env
from plato.rpc.models.job import AgentJobStatus

logger = logging.getLogger(__name__)


class AgentJobConflictError(Exception):
    """A start for an existing agent_job_id whose argv/shell differs."""


class AgentJobNotFoundError(Exception):
    pass


def _now() -> datetime:
    return datetime.now(UTC)


def _as_int(value: object) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, str)):
        try:
            return int(value)
        except ValueError:
            return None
    return None


def _proc_identity(pid: int) -> str | None:
    """Stable identity of a live process: its start time.

    A pid alone is not an identity — after wraparound the same pid can name a
    foreign process, and adopting one means wait tracks a stranger and killpg
    signals it. Start time is immutable for a process's lifetime, so
    pid+starttime is the same identity check every supervisor uses. Linux:
    /proc/<pid>/stat field 22 (jiffies since boot). Fallback (macOS tests):
    ``ps -o lstart=``. None = could not establish identity.
    """
    try:
        stat = Path(f"/proc/{pid}/stat").read_text()
        # comm (field 2) may contain spaces/parens; fields resume after the
        # LAST ")". starttime is field 22 -> index 19 of the remainder.
        return "stat:" + stat.rsplit(")", 1)[1].split()[19]
    except (OSError, IndexError):
        pass
    try:
        out = subprocess.run(
            ["ps", "-p", str(pid), "-o", "lstart="], capture_output=True, text=True, timeout=5, check=False
        )
        text = out.stdout.strip()
        return ("ps:" + text) if text else None
    except (OSError, subprocess.SubprocessError):
        return None


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


class _Job:
    def __init__(self, agent_job_id: str, job_dir: Path, meta: dict[str, object]) -> None:
        self.agent_job_id = agent_job_id
        self.job_dir = job_dir
        self.meta = meta
        self.proc: asyncio.subprocess.Process | None = None
        # Event set once the exit record is persisted (by supervisor or reaper).
        self.done = asyncio.Event()

    @property
    def stdout_path(self) -> Path:
        return self.job_dir / "stdout.log"

    @property
    def stderr_path(self) -> Path:
        return self.job_dir / "stderr.log"

    @property
    def exit_path(self) -> Path:
        return self.job_dir / "exit.json"

    def _spec_key(self) -> tuple[object, object]:
        return (self.meta.get("argv"), self.meta.get("shell"))

    def status(self) -> AgentJobStatus:
        exit_rec = self._read_exit()
        started_at = datetime.fromisoformat(str(self.meta["started_at"]))
        stdout_bytes = self.stdout_path.stat().st_size if self.stdout_path.exists() else 0
        stderr_bytes = self.stderr_path.stat().st_size if self.stderr_path.exists() else 0
        pid = _as_int(self.meta.get("pid"))
        pgid = _as_int(self.meta.get("pgid"))

        if exit_rec is not None:
            return AgentJobStatus(
                agent_job_id=self.agent_job_id,
                state=exit_rec["state"],
                pid=pid,
                pgid=pgid,
                rc=exit_rec.get("rc"),
                term_signal=exit_rec.get("term_signal"),
                started_at=started_at,
                finished_at=datetime.fromisoformat(exit_rec["finished_at"]),
                stdout_bytes=stdout_bytes,
                stderr_bytes=stderr_bytes,
            )
        # No exit record yet. If we own the process handle, trust it — this
        # closes the race where a just-signaled process dies before the
        # supervisor persists exit.json (which otherwise reads as "lost").
        if self.proc is not None:
            rc = self.proc.returncode
            if rc is None:
                return AgentJobStatus(
                    agent_job_id=self.agent_job_id,
                    state="running",
                    pid=pid,
                    pgid=pgid,
                    started_at=started_at,
                    stdout_bytes=stdout_bytes,
                    stderr_bytes=stderr_bytes,
                )
            term_signal = -rc if rc < 0 else None
            return AgentJobStatus(
                agent_job_id=self.agent_job_id,
                state="signaled" if term_signal else "exited",
                pid=pid,
                pgid=pgid,
                rc=None if term_signal else rc,
                term_signal=term_signal,
                started_at=started_at,
                finished_at=_now(),
                stdout_bytes=stdout_bytes,
                stderr_bytes=stderr_bytes,
            )
        # No handle (recovered job): alive pid ⇒ running, else genuinely lost.
        state = "running" if (pid is not None and _pid_alive(pid)) else "lost"
        return AgentJobStatus(
            agent_job_id=self.agent_job_id,
            state=state,
            pid=pid,
            pgid=pgid,
            started_at=started_at,
            stdout_bytes=stdout_bytes,
            stderr_bytes=stderr_bytes,
        )

    def _read_exit(self) -> dict | None:
        if not self.exit_path.exists():
            return None
        try:
            return json.loads(self.exit_path.read_text())
        except (OSError, json.JSONDecodeError):
            return None

    def write_exit(self, *, rc: int | None, term_signal: int | None) -> None:
        state = "signaled" if term_signal else "exited"
        record = {
            "state": state,
            "rc": rc,
            "term_signal": term_signal,
            "finished_at": _now().isoformat(),
        }
        tmp = self.exit_path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(record))
        tmp.replace(self.exit_path)
        self.done.set()

    def mark_lost(self) -> None:
        record = {"state": "lost", "rc": None, "term_signal": None, "finished_at": _now().isoformat()}
        self.exit_path.write_text(json.dumps(record))
        self.done.set()


class AgentJobManager:
    def __init__(self, jobs_dir: Path) -> None:
        self._jobs_dir = jobs_dir
        self._jobs: dict[str, _Job] = {}
        # Serializes check→spawn→register in start().
        self._start_lock = asyncio.Lock()
        self._jobs_dir.mkdir(parents=True, exist_ok=True)

    async def start(
        self,
        agent_job_id: str,
        *,
        argv: list[str] | None,
        shell: str | None,
        cwd: str | None,
        env: dict[str, str],
        inherit_env: bool,
        payload_path: str | None,
    ) -> AgentJobStatus:
        # The check below and the registration further down straddle an await,
        # so without this lock two concurrent starts for the same id both see no
        # existing job and both spawn — the second registration orphaning the
        # first live runner. The client resends start with agent_job_id as the
        # idempotency key after a timeout/disconnect, so this is a real path.
        async with self._start_lock:
            existing = self._jobs.get(agent_job_id)
            if existing is not None:
                if existing._spec_key() != (argv, shell):
                    raise AgentJobConflictError(agent_job_id)
                return existing.status()  # idempotent restart
            return await self._spawn(
                agent_job_id,
                argv=argv,
                shell=shell,
                cwd=cwd,
                env=env,
                inherit_env=inherit_env,
                payload_path=payload_path,
            )

    async def _spawn(
        self,
        agent_job_id: str,
        *,
        argv: list[str] | None,
        shell: str | None,
        cwd: str | None,
        env: dict[str, str],
        inherit_env: bool,
        payload_path: str | None,
    ) -> AgentJobStatus:
        """Spawn and register a job. Caller MUST hold ``self._start_lock``."""
        job_dir = self._jobs_dir / agent_job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        meta: dict[str, object] = {
            "agent_job_id": agent_job_id,
            "argv": argv,
            "shell": shell,
            "cwd": cwd,
            "payload_path": payload_path,
            "started_at": _now().isoformat(),
        }
        job = _Job(agent_job_id, job_dir, meta)

        # login_env, not os.environ: a fresh SSH session re-read
        # /etc/environment via PAM and prepended VM_PATH_EXPORT; the daemon's
        # own environ is frozen at bootstrap time and may predate env setup.
        run_env = {**login_env(), **env} if inherit_env else dict(env)

        stdout_fd = os.open(job.stdout_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        stderr_fd = os.open(job.stderr_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        try:
            if argv:
                proc = await asyncio.create_subprocess_exec(
                    *argv,
                    cwd=cwd,
                    env=run_env,
                    stdin=asyncio.subprocess.DEVNULL,
                    stdout=stdout_fd,
                    stderr=stderr_fd,
                    start_new_session=True,
                )
            else:
                assert shell is not None
                proc = await asyncio.create_subprocess_shell(
                    shell,
                    cwd=cwd,
                    env=run_env,
                    stdin=asyncio.subprocess.DEVNULL,
                    stdout=stdout_fd,
                    stderr=stderr_fd,
                    start_new_session=True,
                )
        finally:
            os.close(stdout_fd)
            os.close(stderr_fd)

        job.proc = proc
        meta["pid"] = proc.pid
        meta["pgid"] = proc.pid  # start_new_session ⇒ pgid == pid
        # Recorded so recovery can verify the pid still names THIS process.
        meta["proc_identity"] = _proc_identity(proc.pid)
        (job_dir / "meta.json").write_text(json.dumps(meta))
        self._jobs[agent_job_id] = job

        asyncio.create_task(self._supervise(job))
        return job.status()

    async def _supervise(self, job: _Job) -> None:
        assert job.proc is not None
        rc = await job.proc.wait()
        if rc < 0:
            job.write_exit(rc=None, term_signal=-rc)
        else:
            job.write_exit(rc=rc, term_signal=None)

    def status(self, agent_job_id: str) -> AgentJobStatus:
        job = self._jobs.get(agent_job_id)
        if job is None:
            raise AgentJobNotFoundError(agent_job_id)
        return job.status()

    def prune_finished(self) -> int:
        """Remove state (dirs + registry entries) for every non-running job.

        Called by the pool reset between warm-pool tenants so job dirs and
        spools don't accumulate across a pooled VM's lifetime (the SSH path
        never persisted output; without pruning this would be a new disk-fill
        failure mode). Running jobs are left untouched.
        """
        pruned = 0
        for agent_job_id in list(self._jobs):
            job = self._jobs[agent_job_id]
            if job.status().state == "running":
                continue
            shutil.rmtree(job.job_dir, ignore_errors=True)
            del self._jobs[agent_job_id]
            pruned += 1
        return pruned

    async def wait(self, agent_job_id: str, timeout_s: float) -> AgentJobStatus:
        job = self._jobs.get(agent_job_id)
        if job is None:
            raise AgentJobNotFoundError(agent_job_id)
        if job.status().state != "running":
            return job.status()
        with contextlib.suppress(TimeoutError):
            await asyncio.wait_for(job.done.wait(), timeout=timeout_s)
        return job.status()

    def signal(self, agent_job_id: str, sig: int) -> AgentJobStatus:
        job = self._jobs.get(agent_job_id)
        if job is None:
            raise AgentJobNotFoundError(agent_job_id)
        pgid = _as_int(job.meta.get("pgid"))
        if pgid is not None:
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.killpg(pgid, sig)
        return job.status()

    def recover(self) -> None:
        """On daemon boot: re-adopt live jobs, mark dead-without-exit as lost."""
        if not self._jobs_dir.is_dir():
            return
        for job_dir in self._jobs_dir.iterdir():
            if not job_dir.is_dir():
                continue
            meta_path = job_dir / "meta.json"
            if not meta_path.exists():
                continue
            try:
                meta = json.loads(meta_path.read_text())
            except (OSError, json.JSONDecodeError):
                continue
            job = _Job(meta["agent_job_id"], job_dir, meta)
            self._jobs[job.agent_job_id] = job
            if job.exit_path.exists():
                job.done.set()
                continue
            pid = _as_int(meta.get("pid"))
            if pid is not None and _pid_alive(pid):
                stored = meta.get("proc_identity")
                current = _proc_identity(pid)
                if stored is not None and current == stored:
                    # Re-adopt: poll for exit (we are no longer its parent, so
                    # wait() is unavailable — poll the pid).
                    asyncio.create_task(self._poll_readopted(job, pid))
                    continue
                # Alive pid that is NOT our process (wraparound reuse), or a
                # pre-identity meta record we cannot verify: adopting would
                # make wait track — and signal/killpg target — a foreign
                # process. Honest "lost" instead, loudly: this path is nearly
                # impossible to exercise outside an incident.
                logger.warning(
                    "Job %s: pid %d alive but identity mismatch (stored=%s current=%s) — "
                    "refusing adoption of a foreign process; marking lost",
                    job.agent_job_id,
                    pid,
                    stored,
                    current,
                )
                job.mark_lost()
            else:
                job.mark_lost()

    async def _poll_readopted(self, job: _Job, pid: int) -> None:
        while _pid_alive(pid):
            await asyncio.sleep(1.0)
        # Reparented process: we can't read its exit code. Record signaled/exit
        # unknown as a clean exit record with rc=None but state exited is wrong;
        # use lost only if we truly can't tell. A vanished reparented pid that
        # left no exit.json is indistinguishable → mark lost (honest).
        if not job.exit_path.exists():
            job.mark_lost()


_TERM_TO_KILL_GRACE_S = 5.0


async def signal_term_then_kill(
    manager: AgentJobManager, agent_job_id: str, *, grace_s: float = _TERM_TO_KILL_GRACE_S
) -> None:
    """Best-effort graceful stop: SIGTERM, then SIGKILL after a grace period.

    Runs daemon-side (spawned by the signal endpoint's ``escalate_kill_after_s``)
    so a cancelling world never blocks on the grace window.
    """
    with contextlib.suppress(AgentJobNotFoundError):
        manager.signal(agent_job_id, signal.SIGTERM)
        await asyncio.sleep(grace_s)
        if manager.status(agent_job_id).state == "running":
            manager.signal(agent_job_id, signal.SIGKILL)
