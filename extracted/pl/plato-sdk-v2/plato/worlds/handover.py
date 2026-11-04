"""Hand a running world over to a newer version of itself, in place.

A world's Chronos session outlives any one world process if the process lets it: the agent VMs run their agents as
agent-daemon jobs (``vm_setup.execute_agent``), the workspaces are a plato-fuse mount exported by the kernel NFS
server, and the session ends only on ``/complete`` or a missed heartbeat. ``BaseWorld.hand_over`` uses that:

1. The old process writes a handoff (``Handoff``, root-only, on the world VM): its session, each running agent's VM and
   daemon job id, each workspace's live mount, and whatever state the world adds.
2. It installs the new version with Chronos's own install commands (``next_process``; a failed install hands nothing
   over) and starts Chronos's runner with ``HANDOFF_ENV`` pointing at the handoff. Once the new process is ready it
   stops its Plato heartbeat and exits with ``os._exit``: no ``close()``, no agent shutdown, nothing unmounted, no
   ``/complete``.
3. The new process (``BaseWorld.run`` with ``HANDOFF_ENV`` set) loads the session, checks the handoff (``verify``:
   its own session, readable with its org's key, and only agent VMs that are jobs of that session) and says it's ready.
   Only then does the old process exit; if the new one dies or isn't ready in time, the old one stops it, puts its own
   version back and carries on. Once the old process is gone, the new one adopts the live mounts instead of mounting
   again, and hands the world its agents (``BaseWorld.handoff``) to re-attach with ``vm_setup.attach_agent``.

Adopting is the only safe path for the workspaces: setting them up again unmounts the live mount under the agents
(``Workspace._cleanup_stale_mount``), and a write in flight is lost without an error.
"""

from __future__ import annotations

import logging
import os
import re
import shlex
import signal
import subprocess
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field, JsonValue

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from plato.v2.async_.session import Session

logger = logging.getLogger(__name__)

HANDOFF_ENV = "PLATO_WORLD_HANDOFF"
"""Set in the new process's environment: the path of the handoff it adopts."""
HANDOFF_DIR = Path("/var/lib/plato-world/handoff")
START_SCRIPT = Path("/tmp/run_world.sh")  # noqa: S108 - Chronos's start script on the world VM
"""What Chronos ran to start this world (services/vm_commands.py ``start_world``): install, then plato-world-runner."""
WORLD_LOG = Path("/tmp/world.log")  # noqa: S108 - where Chronos reads the world's log
OLD_PROCESS_WAIT_S = 120.0
READY_WAIT_S = 300.0
"""How long the old process waits for the new one to say it can take over (installed, imported, handoff verified)."""


class HandoffRefused(RuntimeError):
    """A handoff this process won't adopt (another session, a VM outside it, the old process still running), or a
    hand-over this world can't do (an agent not re-attachable, a workspace transport other than NFS)."""


class HandoffAgent(BaseModel):
    name: str = Field(description="The world's name for the agent")
    agent_job_id: str | None = Field(
        description="Its daemon job on its VM (AgentTask.agent_job_id); None: it was between turns"
    )
    runtime: dict[str, JsonValue] = Field(description="Its VM's RuntimeInfo, without the env handle")


class HandoffWorkspace(BaseModel):
    name: str
    mountpoint: str = Field(description="What the NFS server exports: the live plato-fuse mount, or a plain directory")
    cache_dir: str | None = Field(default=None, description="The plato-fuse mount's cache dir; None: not mounted")
    worker_pid: int | None = Field(default=None, description="The plato-fuse process serving it")


class Handoff(BaseModel):
    generation: int = Field(description="1 for the first hand-over in a session, +1 each time")
    old_pid: int
    handed_at: float
    package_spec: str = Field(description="What the new process was started on, e.g. plato-world-x==1.2.3")
    chronos_session_id: str
    plato_session_id: str | None = None
    agents: list[HandoffAgent] = Field(default_factory=list)
    workspaces: list[HandoffWorkspace] = Field(default_factory=list)
    state: dict[str, JsonValue] = Field(default_factory=dict, description="The world's own, from hand_over(state=)")


def write(handoff: Handoff, directory: Path = HANDOFF_DIR) -> Path:
    """Write the handoff where only root can read it (it names the VMs and the SSH key that reaches them). A retry
    of a failed hand-over reuses the generation's path: an earlier attempt's markers are cleared first."""

    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    path = directory / f"handoff-{handoff.generation}.json"
    ready_path(path).unlink(missing_ok=True)
    taken_path(path).unlink(missing_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(handoff.model_dump_json())
    return path


def read(path: Path) -> Handoff:
    return Handoff.model_validate_json(path.read_text())


class NextProcess(BaseModel):
    """How to start the next world process: Chronos's install commands with the package pinned, and its runner."""

    install: list[str]
    runner: list[str]


def next_process(script: str, package: str, version: str) -> NextProcess:
    """Read Chronos's start script (``START_SCRIPT``): its ``uv pip install`` commands, with ``package`` pinned to
    ``version``, and its ``plato-world-runner`` command line.

    The script itself isn't run again: it first downloads the world config from a presigned URL that expires an hour
    after launch, and a failed step there completes the session as failed, ending every agent with it. The config it
    downloaded is still at ``/tmp/config.json``, and this process's environment already has its exports.
    """

    joined = re.sub(r"\\\n\s*", " ", script)
    install = [line.strip() for line in joined.splitlines() if line.strip().startswith("uv pip install ")]
    runner = [line.strip() for line in joined.splitlines() if "plato-world-runner run" in line]
    if not install or len(runner) != 1:
        raise HandoffRefused("Chronos's start script isn't in the expected form: can't start the new version in place")
    name = re.escape(package)
    pinned: list[str] = []
    found = 0
    for command in install:
        command, count = re.subn(
            rf"(?<![\w.-]){name}(==[A-Za-z0-9.+!_-]+)?(?![\w.=-])", f"{package}=={version}", command
        )
        found += count
        pinned.append(command)
    if not found:
        raise HandoffRefused(f"the start script doesn't install {package}: can't start the new version in place")
    return NextProcess(install=pinned, runner=shlex.split(runner[0]))


INSTALL_ATTEMPTS = 3
INSTALL_RETRY_S = 30.0
"""A release can take a minute to reach the index after it's published: a failed install is tried again before the
hand-over is refused."""


def install(
    commands: list[str],
    timeout_s: float = 600,
    *,
    attempts: int = INSTALL_ATTEMPTS,
    retry_s: float = INSTALL_RETRY_S,
) -> None:
    """Install the next version beside the running one. Fails (``HandoffRefused``) before anything is handed over,
    so a broken release leaves the old process running. Output isn't logged: the index URL can carry a credential."""

    for command in commands:
        for attempt in range(1, attempts + 1):
            try:
                done = subprocess.run(  # noqa: S603 - Chronos's own install command
                    ["/bin/bash", "-c", command], capture_output=True, text=True, timeout=timeout_s, check=False
                )
            except subprocess.TimeoutExpired as timed_out:
                # Not chained: TimeoutExpired carries the command, and the index URL in it can carry a credential.
                stderr = timed_out.stderr
                said = stderr.decode(errors="replace") if isinstance(stderr, bytes) else (stderr or "")
                raise HandoffRefused(
                    f"installing the next version timed out after {timeout_s:.0f} s: {_redacted(said)}"
                ) from None
            if done.returncode == 0:
                break
            if attempt == attempts:
                raise HandoffRefused(
                    f"installing the next version failed (exit {done.returncode}, {attempts} attempts): "
                    f"{_redacted(done.stderr)}"
                )
            logger.warning("Installing the next version failed (exit %d); again in %.0f s", done.returncode, retry_s)
            time.sleep(retry_s)


def _redacted(output: str) -> str:
    """An install's error output with URLs cut to their host (an index URL can carry a credential)."""
    return re.sub(r"(\w+://)([^\s/@'\"]*@)?([^\s/'\"]*)[^\s'\"]*", r"\1\3/…", output.strip())


def start_next(runner: list[str], handoff_path: Path, log_path: Path = WORLD_LOG) -> int:
    """Start the next world process, detached from this one (its own session), logging where Chronos reads the world's
    log. It gets this process's environment, which has the start script's exports. Returns its pid."""

    env = {**os.environ, HANDOFF_ENV: str(handoff_path)}
    with log_path.open("ab") as log:
        proc = subprocess.Popen(  # noqa: S603 - Chronos's own runner command
            runner,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            env=env,
            start_new_session=True,
            close_fds=True,
        )
    return proc.pid


def ready_path(handoff_path: Path) -> Path:
    """Written by the new process once it can take over: installed, imported, handoff verified."""
    return handoff_path.with_suffix(".ready")


def taken_path(handoff_path: Path) -> Path:
    """Written by the new process once the old one has exited and the world is its own."""
    return handoff_path.with_suffix(".taken")


def taking_over() -> bool:
    """This process was started to take a world over and hasn't yet: while that's so, the old process is still in
    charge, so a crash here must not complete the session (plato-world-runner's crash report checks this)."""
    path = os.environ.get(HANDOFF_ENV)
    return bool(path) and not taken_path(Path(path)).exists()


def wait_ready(handoff_path: Path, pid: int, timeout_s: float = READY_WAIT_S) -> bool:
    """The old process's side: True once the new one is ready, False if it exited first or took too long."""
    ready = ready_path(handoff_path)
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        if ready.exists():
            return True
        try:
            waited, _ = os.waitpid(pid, os.WNOHANG)
        except ChildProcessError:
            waited = pid
        if waited == pid:
            return ready.exists()
        time.sleep(0.2)
    return False


def abort(pid: int) -> None:
    """Stop a new process that didn't get ready (it leads its own process group, start_new_session)."""
    try:
        os.killpg(pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass


def wait_for_exit(pid: int, timeout_s: float = OLD_PROCESS_WAIT_S) -> None:
    """Wait until the old process is gone: one world process at a time, so /work and the session keep one owner."""

    deadline = time.monotonic() + timeout_s
    while True:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return
        except PermissionError:
            pass
        if time.monotonic() > deadline:
            raise HandoffRefused(f"the previous world process {pid} is still running after {timeout_s:.0f} s")
        time.sleep(0.2)


async def verify(
    handoff: Handoff,
    *,
    session_id: str,
    plato_session: Session | None,
    get_session: Callable[[str], Awaitable[Any]],
) -> None:
    """Adopt only what belongs to this process's own session, in this org.

    - The handoff names this process's Chronos session.
    - That session is readable with this org's key (Chronos answers 404 for another org's session), and its Plato
      session is the one this process loaded.
    - Every agent VM is a job of that Plato session, by the backend's list (``Session.envs`` is this process's own
      cache: it doesn't have VMs another process added).
    """

    if handoff.chronos_session_id != session_id:
        raise HandoffRefused(
            f"the handoff is for session {handoff.chronos_session_id}, this world runs in {session_id}"
        )
    try:
        session = await get_session(session_id)
    except Exception as e:
        raise HandoffRefused(f"session {session_id} isn't readable with this org's key: {type(e).__name__}") from e
    loaded = plato_session.session_id if plato_session is not None else None
    chronos_plato = getattr(session, "plato_session_id", None)
    if loaded is None or (chronos_plato and chronos_plato != loaded):
        raise HandoffRefused(f"Chronos session {session_id} runs on Plato session {chronos_plato}, not {loaded}")
    if handoff.plato_session_id and handoff.plato_session_id != loaded:
        raise HandoffRefused(f"the handoff's Plato session {handoff.plato_session_id} isn't {loaded}")
    if handoff.agents:
        assert plato_session is not None
        jobs = {job.job_id for job in await plato_session.list_jobs()}
        for agent in handoff.agents:
            metadata = agent.runtime.get("metadata")
            vm_job = metadata.get("job_id") if isinstance(metadata, dict) else None
            if vm_job not in jobs:
                raise HandoffRefused(f"agent {agent.name}'s VM {vm_job} isn't a job of Plato session {loaded}")


class AdoptedFuseConfig(BaseModel):
    """The live mount's own config, as ``mount_lazy`` wrote it for plato-fuse (other keys are plato-fuse's)."""

    manifest: dict[str, JsonValue]
    s3_config: dict[str, JsonValue]


def adopted_fuse_config(cache_dir: Path) -> AdoptedFuseConfig:
    """The live mount's own config (what ``mount_lazy`` wrote for plato-fuse): manifest and S3 access."""

    return AdoptedFuseConfig.model_validate_json((cache_dir / "config.json").read_text())
