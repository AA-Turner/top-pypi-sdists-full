"""Harbor trials inside Labqoat sandboxes."""

import asyncio
import contextlib
import re
import uuid
from pathlib import Path
from typing import ClassVar

from harbor.environments.base import BaseEnvironment, ExecResult
from harbor.environments.capabilities import EnvironmentCapabilities
from harbor.environments.definition import COMPOSE_FILE_NAME
from harbor.models.task.config import NetworkMode, NetworkPolicy

from labqoat.harbor.sandbox_users import SandboxUsers
from labqoat.sandbox.sandbox import Sandbox
from labqoat.sandbox.sandbox_client import SandboxClient
from labqoat.sandbox.sandbox_error import SandboxError
from labqoat.sandbox.sandbox_not_found_error import SandboxNotFoundError
from labqoat.sandbox.sandbox_platform import SandboxPlatform
from labqoat.sandbox.sandbox_reach import SandboxReach
from labqoat.sandbox.sandbox_timeout_error import SandboxTimeoutError
from labqoat.sandbox.stream_type import StreamType


class LabqoatEnvironment(BaseEnvironment):
    """Run each trial in one sandbox: ``harbor run -e labqoat.harbor:LabqoatEnvironment``.

    From a laptop, or from a run without a sandbox host of its own, the platform places each trial's sandbox in
    the project the CLI would use. Inside a function that declares ``sandboxes=[...]``, or pointed at a served
    host by ``LABQOAT_SANDBOX_URL``, trials use that host. A sandbox starts from a prebuilt image and runs as
    root, with the public
    network, with none, or with exactly the hosts the task allows, as its ``network_mode`` says. A task
    therefore names its image in ``[environment].docker_image``; tasks that need a Dockerfile build, Docker
    Compose, wildcard hosts or address ranges in an allowlist, a different network for one phase or a GPU are
    rejected when the trial is set up, before anything runs.

    A command's exit code is the task's outcome. A failing sandbox host raises instead, so Harbor records an
    environment error and no reward.
    """

    DEFAULT_CPUS: ClassVar[int] = 1
    DEFAULT_MEMORY_MB: ClassVar[int] = 2048
    LIFETIME_SECONDS: ClassVar[float] = 86_400.0

    _sandbox: Sandbox | None = None
    _users: SandboxUsers | None = None

    @staticmethod
    def type() -> str:
        """Name this environment in Harbor's messages and results."""
        return "labqoat"

    @property
    def capabilities(self) -> EnvironmentCapabilities:
        """Offer the public network, none, or exact hosts and IPv4 addresses; no GPUs, Compose, mounts or Windows."""
        return EnvironmentCapabilities(
            disable_internet=True,
            network_allowlist=True,
            network_allowlist_hostnames=True,
            network_allowlist_ipv4_addresses=True,
        )

    @classmethod
    def preflight(cls) -> None:
        """Stop a job before any trial is queued when this process cannot reach sandboxes."""
        try:
            cls._reached(SandboxReach.nearest())
        except SandboxError as error:
            raise SystemExit(f"Labqoat sandboxes are not available: {error}") from error

    @staticmethod
    def _reached(client: SandboxClient | SandboxPlatform) -> None:
        """Ask a host for its capacity, or the platform about a sandbox that does not exist."""
        if isinstance(client, SandboxClient):
            client.capacity()
            return
        with contextlib.suppress(SandboxNotFoundError):
            client.from_id("labqoat-preflight").poll()

    def validate_network_policy_support(self, network_policy: NetworkPolicy | None = None) -> None:
        """Accept the public network, none or listed hosts, and only what the sandbox starts with for every phase."""
        super().validate_network_policy_support(network_policy)
        started, asked = self._network_policy, network_policy or self._network_policy
        if (asked.network_mode, sorted(asked.allowed_hosts)) != (started.network_mode, sorted(started.allowed_hosts)):
            raise ValueError(
                f"A Labqoat sandbox keeps the network it starts with (network_mode='{started.network_mode.value}'), "
                f"but a phase asks for network_mode='{asked.network_mode.value}' or other hosts. Give [environment], "
                "[agent] and [verifier] in task.toml the same network_mode and allowed_hosts."
            )

    def _network(self) -> bool | list[str]:
        """Translate the task's policy: the public network, none, or exactly the hosts it lists."""
        if self._network_policy.network_mode == NetworkMode.ALLOWLIST:
            return list(self._network_policy.allowed_hosts)
        return self._network_policy.network_mode == NetworkMode.PUBLIC

    def _validate_definition(self) -> None:
        """Require a prebuilt image and refuse definitions that need more than one container."""
        compose = self.environment_dir / COMPOSE_FILE_NAME
        if compose.exists():
            raise ValueError(f"Labqoat sandboxes run a single image and cannot run Docker Compose ({compose}).")
        self._image()

    def _image(self) -> str:
        """Return the task's prebuilt image; a Dockerfile alone cannot be used."""
        image = self.task_env_config.docker_image
        if not image:
            raise ValueError(
                "Labqoat sandboxes start from prebuilt images and cannot build environment/Dockerfile. "
                "Set [environment].docker_image in task.toml to an image the sandbox host was launched with."
            )
        return image

    async def start(self, force_build: bool) -> None:
        """Start the sandbox from the task's image and prepare the directories Harbor expects in it.

        ``force_build`` has nothing to rebuild. More trials than the host's memory fits wait for room, for as
        long as the task allows its environment to build. A start that fails or is cancelled terminates its
        sandbox, even when the host created it without the answer arriving, so the host's budget is not held by
        a trial that never ran. The trial ends the sandbox; the host's longest lifetime only bounds a trial
        whose process went away.
        """
        client = SandboxReach.nearest()
        sandbox = client.from_id(self._sandbox_id())
        cpus, memory_mb = self._effective_cpus, self._effective_memory_mb
        try:
            await client.create_async(
                image=self._image(),
                cpu=self.DEFAULT_CPUS if cpus is None else cpus,
                memory=self.DEFAULT_MEMORY_MB if memory_mb is None else memory_mb,
                env=self._startup_env(),
                sandbox_id=sandbox.id,
                timeout=self.LIFETIME_SECONDS,
                network=self._network(),
                wait=self.task_env_config.build_timeout_sec,
            )
            self._sandbox, self._users = sandbox, SandboxUsers(sandbox)
            self.logger.debug(f"Started sandbox {sandbox.id} for {self.session_id}")
            await self._prepare(sandbox)
        except BaseException:
            self._sandbox = self._users = None
            with contextlib.suppress(SandboxError):
                await sandbox.terminate_async()
            raise

    async def stop(self, delete: bool) -> None:
        """Terminate the sandbox, or leave it on the host for inspection when asked to keep it."""
        sandbox, self._sandbox, self._users = self._sandbox, None, None
        if sandbox is None:
            return
        if not delete:
            self.logger.debug(f"Keeping sandbox {sandbox.id}; it holds host budget until its lifetime ends")
            return
        try:
            await sandbox.terminate_async()
        except SandboxError as error:
            self.logger.error(f"Could not terminate sandbox {sandbox.id}: {error}")

    async def exec(
        self,
        command: str,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
        timeout_sec: int | None = None,
        user: str | int | None = None,
    ) -> ExecResult:
        """Run a shell command with bash, without input, and return its merged output as stdout.

        Without ``timeout_sec`` the command may run as long as the sandbox. A command the host kills for
        exceeding its timeout raises as Harbor's Docker environment does. A command whose caller stops waiting,
        as Harbor's own time limits do, is killed in the sandbox. Any other sandbox failure propagates unchanged.
        """
        sandbox, users = self._running()
        process = await sandbox.exec_async(
            "bash",
            "-c",
            command,
            workdir=cwd or self.task_env_config.workdir,
            env=self._merge_env(env),
            user=await users.resolve(self._resolve_user(user)),
            timeout=timeout_sec,
            stdin=StreamType.DEVNULL,
            stderr=StreamType.STDOUT,
        )
        try:
            output = await process.stdout.read_async()
            return ExecResult(stdout=output, stderr=None, return_code=await process.wait_async())
        except SandboxTimeoutError as error:
            raise RuntimeError(f"Command timed out after {timeout_sec} seconds") from error
        except asyncio.CancelledError:
            with contextlib.suppress(SandboxError):
                await asyncio.shield(process.kill_async())
            raise

    async def upload_file(self, source_path: Path | str, target_path: str) -> None:
        """Copy a local file to an absolute sandbox path."""
        sandbox, _users = self._running()
        await sandbox.write_file_async(target_path, Path(source_path))

    async def upload_dir(self, source_dir: Path | str, target_dir: str) -> None:
        """Copy a local directory's contents into a sandbox directory."""
        sandbox, _users = self._running()
        await sandbox.upload_dir_async(source_dir, target_dir)

    async def download_file(self, source_path: str, target_path: Path | str) -> None:
        """Copy a sandbox file to a local path, creating its parent directories."""
        sandbox, _users = self._running()
        content = await sandbox.read_file_async(source_path)
        target = Path(target_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)

    async def download_dir(self, source_dir: str, target_dir: Path | str) -> None:
        """Copy a sandbox directory's contents into a local directory, overwriting files already there."""
        sandbox, _users = self._running()
        await sandbox.download_dir_async(source_dir, target_dir)

    def _running(self) -> tuple[Sandbox, SandboxUsers]:
        """Return the started sandbox with its user table."""
        if self._sandbox is None or self._users is None:
            raise RuntimeError("The Labqoat sandbox is not running; call start() before using the environment.")
        return self._sandbox, self._users

    def _sandbox_id(self) -> str:
        """Name the sandbox after the trial so the host's listing is readable, within its identifier rules."""
        trial = re.sub(r"[^a-z0-9]+", "-", self.session_id.lower()).strip("-")[:40]
        return f"{trial or 'harbor'}-{uuid.uuid4().hex[:12]}"

    async def _prepare(self, sandbox: Sandbox) -> None:
        """Create the working directory and log directories, then upload loose environment files."""
        if workdir := self.task_env_config.workdir:
            await sandbox.mkdir_async(workdir, parents=True)
        await self.ensure_dirs(self._mount_targets(writable_only=True))
        await self._upload_environment_dir_after_start()
