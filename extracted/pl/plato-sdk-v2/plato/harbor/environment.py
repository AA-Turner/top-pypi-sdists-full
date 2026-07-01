"""A Harbor ``BaseEnvironment`` backed by a Plato VM running Docker.

Expose it to Harbor with::

    harbor run ... \\
        --environment-import-path plato.harbor.environment:PlatoEnvironment

How it works
------------
A Plato ``ubuntu-vm`` artifact ships a working Docker daemon, so this provider
treats the Plato VM as a **remote Docker host** and runs the task's container(s)
with Docker Compose inside it — exactly like the EC2 provider, but provisioning
a Plato Firecracker VM instead of an EC2 instance and talking to it over the
Plato ``execute`` channel instead of SSH. The thing Harbor ``exec``/copies into
is therefore the *task container*, giving full Dockerfile fidelity (``RUN``
layers, ``CMD``/``ENTRYPOINT``, ``HEALTHCHECK``, multi-service Compose).

The build + run happen entirely on the VM; no local Docker daemon, no ECR push,
and no AWS credentials are required on the machine running ``harbor run`` — only
``PLATO_API_KEY``.

Configuration is passed through the task's ``[environment].kwargs`` table, which
Harbor forwards to this constructor:

* ``artifact_id``    — Plato artifact to boot (default: a Docker-enabled
  ``ubuntu-vm`` artifact). The artifact MUST have Docker installed.
* ``simulator``      — simulator name to associate with the env (default
  ``ubuntu-vm``); only needed so the desktop SDK can be resolved.
* ``session_timeout``— Plato VM session timeout in seconds (default 3600).

Scope / caveats
---------------
* Linux only; Windows containers are rejected by Harbor's capability gate.
* GPU/TPU not supported (the default ``ubuntu-vm`` artifact has neither).
* The default artifact is modestly sized (≈1 vCPU / 2 GiB); heavy builds may
  need a larger Docker-enabled artifact passed via ``artifact_id``.
* Snapshot-restored VMs boot with a frozen clock, so ``start()`` calls
  ``set_date`` before any Docker pull/build — otherwise registry TLS fails.
"""

from __future__ import annotations

import asyncio
import base64
import io
import logging
import os
import shlex
import tarfile
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, override
from uuid import uuid4

from harbor.constants import MAIN_SERVICE_NAME
from harbor.environments.base import BaseEnvironment, ExecResult
from harbor.environments.capabilities import (
    EnvironmentCapabilities,
    EnvironmentResourceCapabilities,
)
from harbor.environments.compose_service_ops import (
    ComposeServiceOpsMixin,
    ComposeServiceTransport,
)
from harbor.environments.definition import (
    require_agent_environment_definition,
    should_use_prebuilt_docker_image,
)
from harbor.environments.dind_compose import DinDComposeOps
from harbor.environments.docker import (
    COMPOSE_BUILD_PATH,
    COMPOSE_NO_NETWORK_PATH,
    COMPOSE_PREBUILT_PATH,
    RESOURCES_COMPOSE_NAME,
    self_bind_mount,
    write_mounts_compose_file,
    write_resources_compose_file,
)
from harbor.environments.docker.compose_env import (
    ComposeInfraEnvVars,
    legacy_log_mount_env_vars,
    merge_compose_env,
)
from harbor.environments.docker.docker import (
    _sanitize_docker_compose_project_name,
    _sanitize_docker_image_name,
)
from harbor.models.task.config import EnvironmentConfig
from harbor.models.trial.config import ResourceMode, ServiceVolumeConfig
from harbor.models.trial.paths import TrialPaths

from plato.harbor._shell import (
    build_download_dir_script,
    build_download_file_script,
    build_host_command,
    build_upload_dir_script,
    build_upload_file_script,
)
from plato.v2 import AsyncPlato, Env

# A Plato ``ubuntu-vm`` artifact that ships a working Docker daemon + compose +
# buildx. Override per-task via ``[environment.kwargs].artifact_id`` to use a
# larger / customised Docker-enabled artifact.
_DEFAULT_ARTIFACT_ID = "971d3c5e-5682-4df7-a8ca-bc38e7fc1e08"
_DEFAULT_SIMULATOR = "ubuntu-vm"
_DEFAULT_SESSION_TIMEOUT_SEC = 3600

# Layout on the VM (mirrors the EC2 provider).
_HARBOR_ROOT_VM = "/harbor"
_COMPOSE_DIR_NAME = "compose"
_ENVIRONMENT_DIR_NAME = "environment"
_MOUNTS_COMPOSE_NAME = "docker-compose-mounts.json"

_DOCKER_READY_TIMEOUT_SEC = 120
_COMPOSE_UP_TIMEOUT_SEC = 300
_HOST_EXEC_DEFAULT_TIMEOUT_SEC = 120
_TRANSFER_TIMEOUT_SEC = 300


class _PlatoComposeOps(DinDComposeOps):
    """Remote Docker Compose operations over a Plato VM host.

    Mirrors ``_EC2ComposeOps``: ``DinDComposeOps`` supplies upload/download and
    per-service operations on top of the four primitives we override here
    (``_compose_exec``, ``_host_exec``, and the host file-staging helpers), plus
    a detached ``exec`` for the main service so long-running agent commands are
    not bounded by a single ``execute`` round-trip timeout.
    """

    _SELF_BIND_LOG_DIRS = True
    _CP_FILE_TIMEOUT_SEC = 120
    _CP_DIR_TIMEOUT_SEC = 300
    _POLL_INTERVAL_SEC = 1
    _STATUS_POLL_FAILURE_LIMIT = 5

    def __init__(self, env: PlatoEnvironment) -> None:
        self._env = env

    @override
    async def _compose_exec(
        self,
        subcommand: list[str],
        timeout_sec: int | None = None,
    ) -> ExecResult:
        return await self._env._compose_exec(subcommand, timeout_sec=timeout_sec)

    @override
    async def _host_exec(
        self,
        command: str,
        timeout_sec: int | None = None,
    ) -> ExecResult:
        return await self._env._host_exec(command, cwd="/", timeout_sec=timeout_sec)

    @override
    async def exec(
        self,
        command: str,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
        timeout_sec: int | None = None,
        user: str | int | None = None,
        *,
        service: str | None = None,
    ) -> ExecResult:
        service = service or MAIN_SERVICE_NAME
        if service != MAIN_SERVICE_NAME:
            return await super().exec(
                command,
                cwd=cwd,
                env=env,
                timeout_sec=timeout_sec,
                user=user,
                service=service,
            )
        return await self._exec_main_detached(
            command,
            cwd=cwd,
            env=env,
            timeout_sec=timeout_sec,
            user=user,
        )

    async def _exec_main_detached(
        self,
        command: str,
        cwd: str | None,
        env: dict[str, str] | None,
        timeout_sec: int | None,
        user: str | int | None,
    ) -> ExecResult:
        token = uuid4().hex
        base_path = f"/tmp/harbor_exec_{token}"
        stdout_path = f"{base_path}.stdout"
        stderr_path = f"{base_path}.stderr"
        status_path = f"{base_path}.status"
        pid_path = f"{base_path}.pid"
        paths = " ".join(shlex.quote(path) for path in (stdout_path, stderr_path, status_path, pid_path))
        wrapper = (
            f"rm -f {paths}; "
            f"(bash -lc {shlex.quote(command)} > {shlex.quote(stdout_path)} "
            f"2> {shlex.quote(stderr_path)}; "
            f"code=$?; printf '%s' \"$code\" > {shlex.quote(status_path)}) "
            f"& echo $! > {shlex.quote(pid_path)}"
        )

        parts: list[str] = ["exec", "-T", "-d"]
        if cwd:
            parts.extend(["-w", cwd])
        if env:
            for key, value in env.items():
                parts.extend(["-e", f"{key}={value}"])
        if user is not None:
            parts.extend(["-u", str(user)])
        parts.extend([MAIN_SERVICE_NAME, "bash", "-lc", wrapper])

        start_result = await self._compose_exec(parts, timeout_sec=30)
        if start_result.return_code != 0:
            return start_result

        timed_out = False
        status_poll_failed = False
        status_poll_error: str | None = None
        consecutive_status_poll_failures = 0
        return_code: int | None = None
        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout_sec if timeout_sec is not None else None
        while True:
            status_result = await self._compose_exec(
                [
                    "exec",
                    "-T",
                    MAIN_SERVICE_NAME,
                    "sh",
                    "-c",
                    f"cat {shlex.quote(status_path)} 2>/dev/null || true",
                ],
                timeout_sec=10,
            )
            status_text = (status_result.stdout or "").strip()
            if status_text:
                consecutive_status_poll_failures = 0
                try:
                    return_code = int(status_text.splitlines()[-1])
                except ValueError:
                    return_code = 1
                break
            if status_result.return_code != 0:
                consecutive_status_poll_failures += 1
                status_poll_error = status_result.stderr or status_result.stdout
                if consecutive_status_poll_failures >= self._STATUS_POLL_FAILURE_LIMIT:
                    status_poll_failed = True
                    return_code = status_result.return_code
                    break
            else:
                consecutive_status_poll_failures = 0
            if deadline is not None and loop.time() >= deadline:
                timed_out = True
                await self._compose_exec(
                    [
                        "exec",
                        "-T",
                        MAIN_SERVICE_NAME,
                        "sh",
                        "-c",
                        (
                            f"if [ -s {shlex.quote(pid_path)} ]; then "
                            f"kill -TERM $(cat {shlex.quote(pid_path)}) "
                            "2>/dev/null || true; fi"
                        ),
                    ],
                    timeout_sec=10,
                )
                return_code = 124
                break
            await asyncio.sleep(self._POLL_INTERVAL_SEC)

        stdout_text = await self._read_exec_output_file(stdout_path)
        stderr_text = await self._read_exec_output_file(stderr_path)
        await self._compose_exec(
            ["exec", "-T", MAIN_SERVICE_NAME, "sh", "-c", f"rm -f {paths}"],
            timeout_sec=10,
        )

        if timed_out:
            timeout_message = f"Command timed out after {timeout_sec} seconds"
            stderr_text = f"{stderr_text}\n{timeout_message}" if stderr_text else timeout_message
        if status_poll_failed:
            failure_message = "Main container appears to have stopped while waiting for detached exec status."
            if status_poll_error:
                failure_message = f"{failure_message} Last status poll error: {status_poll_error}"
            stderr_text = f"{stderr_text}\n{failure_message}" if stderr_text else failure_message

        callback = self._env._output_callback()
        if callback is not None:
            if stdout_text:
                await callback(stdout_text, "stdout")
            if stderr_text:
                await callback(stderr_text, "stderr")
        return ExecResult(
            stdout=stdout_text or None,
            stderr=stderr_text or None,
            return_code=return_code if return_code is not None else 1,
        )

    async def _read_exec_output_file(self, path: str) -> str:
        result = await self._compose_exec(
            [
                "exec",
                "-T",
                MAIN_SERVICE_NAME,
                "sh",
                "-c",
                f"cat {shlex.quote(path)} 2>/dev/null || true",
            ],
            timeout_sec=30,
        )
        return result.stdout or ""

    @override
    async def _stage_file_to_host(self, source_path: Path | str, host_path: str):
        await self._env._upload_file_to_host(source_path, host_path)

    @override
    async def _stage_dir_to_host(self, source_dir: Path | str, host_dir: str):
        await self._env._upload_dir_to_host(source_dir, host_dir)

    @override
    async def _fetch_file_from_host(self, host_path: str, target_path: Path | str):
        await self._env._download_file_from_host(host_path, target_path)

    @override
    async def _fetch_dir_from_host(self, host_dir: str, target_dir: Path | str):
        await self._env._download_dir_from_host(host_dir, target_dir)


class PlatoEnvironment(ComposeServiceOpsMixin, BaseEnvironment):
    """Run a Harbor trial inside a Plato VM using remote Docker Compose."""

    def __init__(
        self,
        environment_dir: Path,
        environment_name: str,
        session_id: str,
        trial_paths: TrialPaths,
        task_env_config: EnvironmentConfig,
        logger: logging.Logger | None = None,
        *,
        artifact_id: str | None = None,
        simulator: str | None = None,
        session_timeout: int | None = None,
        docker_ready_timeout_sec: int = _DOCKER_READY_TIMEOUT_SEC,
        compose_up_timeout_sec: int = _COMPOSE_UP_TIMEOUT_SEC,
        **kwargs: Any,
    ) -> None:
        # Pull Plato-specific options out of [environment].kwargs before handing
        # the rest of the standard Harbor constructor args to the base class.
        self._artifact_id = artifact_id or _DEFAULT_ARTIFACT_ID
        self._simulator = simulator or _DEFAULT_SIMULATOR
        self._session_timeout = session_timeout or _DEFAULT_SESSION_TIMEOUT_SEC
        self._docker_ready_timeout_sec = docker_ready_timeout_sec
        self.compose_up_timeout_sec = compose_up_timeout_sec

        super().__init__(
            environment_dir=environment_dir,
            environment_name=environment_name,
            session_id=session_id,
            trial_paths=trial_paths,
            task_env_config=task_env_config,
            logger=logger,
            **kwargs,
        )

        self._plato: AsyncPlato | None = None
        self._session: Any = None
        self._vm: Any = None
        # The Plato ubuntu-vm runs everything as root, so plain `docker`/`docker
        # compose` work without sudo.
        self._docker_cmd = "docker"
        self._use_prebuilt = False
        self._compose_ops = _PlatoComposeOps(self)

    # -- capabilities / metadata ---------------------------------------------

    @staticmethod
    @override
    def type() -> str:
        return "plato"

    @property
    @override
    def _uses_compose(self) -> bool:
        return True

    @classmethod
    @override
    def resource_capabilities(cls) -> EnvironmentResourceCapabilities:
        return EnvironmentResourceCapabilities(cpu_limit=True, memory_limit=True)

    @property
    @override
    def capabilities(self) -> EnvironmentCapabilities:
        # We run real containers via Compose inside the VM, so we can honour
        # Dockerfile/Compose task definitions and `no-network` (compose
        # network_mode: none). GPU/TPU/Windows/allowlist stay unsupported and
        # are rejected up front by Harbor's validators.
        return EnvironmentCapabilities(
            disable_internet=True,
            docker_compose=True,
        )

    @classmethod
    @override
    def preflight(cls) -> None:
        if not os.environ.get("PLATO_API_KEY"):
            raise SystemExit("The Plato environment requires PLATO_API_KEY to be set. Please export it and try again.")

    @property
    def _environment_docker_compose_path(self) -> Path:
        return self.environment_dir / "docker-compose.yaml"

    @override
    def _validate_definition(self) -> None:
        require_agent_environment_definition(
            self.environment_dir,
            docker_image=self.task_env_config.docker_image,
            extra_docker_compose_paths=self.extra_docker_compose_paths,
        )

    # -- internals -----------------------------------------------------------

    def _require_vm(self):
        if self._vm is None:
            raise RuntimeError("Plato environment not started. Call start() first.")
        return self._vm

    def _docker_parts(self) -> list[str]:
        return [self._docker_cmd]

    # -- host channel (over the Plato `execute` API) -------------------------

    async def _host_exec(
        self,
        command: str,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
        timeout_sec: int | None = None,
    ) -> ExecResult:
        script = build_host_command(command, cwd=cwd, env=env)
        try:
            result = await self._require_vm().execute(
                script,
                timeout=timeout_sec or _HOST_EXEC_DEFAULT_TIMEOUT_SEC,
            )
        except Exception as exc:  # noqa: BLE001 - surface as a failed exec
            self.logger.debug("Plato execute call failed: %s", exc)
            return ExecResult(stdout=None, stderr=str(exc), return_code=1)

        stdout = result.stdout or None
        stderr = result.stderr or None
        return_code = result.exit_code if result.exit_code is not None else (0 if result.success else 1)
        if getattr(result, "timed_out", False):
            return_code = 124
            timeout_msg = f"Command timed out after {timeout_sec} seconds"
            stderr = f"{stderr}\n{timeout_msg}" if stderr else timeout_msg
        return ExecResult(stdout=stdout, stderr=stderr, return_code=return_code)

    async def _upload_file_to_host(self, source_path: Path | str, host_path: str) -> None:
        data = Path(source_path).read_bytes()
        b64 = base64.b64encode(data).decode("ascii")
        result = await self._host_exec(
            build_upload_file_script(host_path, b64),
            timeout_sec=_TRANSFER_TIMEOUT_SEC,
        )
        if result.return_code != 0:
            raise RuntimeError(
                f"Failed to upload {source_path!r} to {host_path!r} "
                f"(rc={result.return_code}): {result.stderr or result.stdout}"
            )

    async def _upload_dir_to_host(self, source_dir: Path | str, host_dir: str) -> None:
        source = Path(source_dir)
        if not source.is_dir():
            self.logger.warning("No files to upload from %s", source)
            return
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
            tar.add(str(source), arcname=".")
        b64 = base64.b64encode(buffer.getvalue()).decode("ascii")
        result = await self._host_exec(
            build_upload_dir_script(host_dir, b64),
            timeout_sec=_TRANSFER_TIMEOUT_SEC,
        )
        if result.return_code != 0:
            raise RuntimeError(
                f"Failed to upload directory {source!r} to {host_dir!r} "
                f"(rc={result.return_code}): {result.stderr or result.stdout}"
            )

    async def _download_file_from_host(self, host_path: str, target_path: Path | str) -> None:
        result = await self._host_exec(
            build_download_file_script(host_path),
            timeout_sec=_TRANSFER_TIMEOUT_SEC,
        )
        if result.return_code != 0:
            raise RuntimeError(
                f"Failed to download {host_path!r} (rc={result.return_code}): {result.stderr or result.stdout}"
            )
        data = base64.b64decode((result.stdout or "").strip())
        target = Path(target_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    async def _download_dir_from_host(self, host_dir: str, target_dir: Path | str) -> None:
        result = await self._host_exec(
            build_download_dir_script(host_dir),
            timeout_sec=_TRANSFER_TIMEOUT_SEC,
        )
        if result.return_code != 0:
            raise RuntimeError(
                f"Failed to download directory {host_dir!r} (rc={result.return_code}): {result.stderr or result.stdout}"
            )
        data = base64.b64decode((result.stdout or "").strip())
        target = Path(target_dir)
        target.mkdir(parents=True, exist_ok=True)
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
            tar.extractall(path=target, filter="data")

    # -- docker / compose on the VM ------------------------------------------

    async def _ensure_docker_ready(self) -> None:
        attempts = max(1, self._docker_ready_timeout_sec // 3)
        last_output = ""
        for _ in range(attempts):
            result = await self._host_exec("docker info", timeout_sec=15)
            if result.return_code == 0:
                return
            last_output = (result.stdout or "") + (result.stderr or "")
            await asyncio.sleep(3)
        raise RuntimeError(f"Docker did not become ready on the Plato VM. Last output: {last_output}")

    def _resolve_volumes(self) -> list[ServiceVolumeConfig]:
        return [self_bind_mount(mount) if mount.get("type") == "bind" else mount for mount in self._mounts]

    def _compose_infra_env_vars(self) -> dict[str, str]:
        volumes = self._resolve_volumes()
        env_vars = ComposeInfraEnvVars(
            main_image_name=_sanitize_docker_image_name(f"hb__{self.environment_name}"),
            context_dir=self._environment_dir_vm,
            prebuilt_image_name=(self.task_env_config.docker_image if self._use_prebuilt else None),
            cpus=self._effective_cpus,
            memory=(f"{memory_mb}M" if (memory_mb := self._effective_memory_mb) else None),
        ).to_env_dict()
        env_vars.update(legacy_log_mount_env_vars(volumes, host_value="target"))
        return env_vars

    def _compose_env_vars(self) -> dict[str, str]:
        user_env: dict[str, str] = {}
        if self.task_env_config.env:
            user_env.update(self.task_env_config.env)
        if self._persistent_env:
            user_env.update(self._persistent_env)
        return merge_compose_env(
            user_env=user_env,
            infra_env=self._compose_infra_env_vars(),
            logger=self.logger,
        )

    def _extra_compose_target_paths(self) -> list[str]:
        return [
            f"{self._compose_dir_vm}/docker-compose-extra-{index}.yaml"
            for index, _ in enumerate(self.extra_docker_compose_paths)
        ]

    def _compose_file_flags(self) -> list[str]:
        build_or_prebuilt = "docker-compose-prebuilt.yaml" if self._use_prebuilt else "docker-compose-build.yaml"
        files = [
            f"{self._compose_dir_vm}/{RESOURCES_COMPOSE_NAME}",
            f"{self._compose_dir_vm}/{build_or_prebuilt}",
        ]
        if self._environment_docker_compose_path.exists():
            files.append(f"{self._environment_dir_vm}/docker-compose.yaml")
        files.extend(self._extra_compose_target_paths())
        files.append(f"{self._compose_dir_vm}/{_MOUNTS_COMPOSE_NAME}")
        if self._network_disabled:
            files.append(f"{self._compose_dir_vm}/docker-compose-no-network.yaml")

        flags: list[str] = []
        for path in files:
            flags.extend(["-f", path])
        return flags

    @property
    def _compose_project_name(self) -> str:
        return _sanitize_docker_compose_project_name(self.session_id)

    @property
    def _session_dir_vm(self) -> str:
        return f"{_HARBOR_ROOT_VM}/{self._compose_project_name}"

    @property
    def _compose_dir_vm(self) -> str:
        return f"{self._session_dir_vm}/{_COMPOSE_DIR_NAME}"

    @property
    def _environment_dir_vm(self) -> str:
        return f"{self._session_dir_vm}/{_ENVIRONMENT_DIR_NAME}"

    def _compose_cmd(self, subcommand: list[str]) -> str:
        parts = [
            *self._docker_parts(),
            "compose",
            "-p",
            self._compose_project_name,
            "--project-directory",
            self._environment_dir_vm,
            *self._compose_file_flags(),
            *subcommand,
        ]
        return shlex.join(parts)

    async def _compose_exec(
        self,
        subcommand: list[str],
        timeout_sec: int | None = None,
    ) -> ExecResult:
        return await self._host_exec(
            self._compose_cmd(subcommand),
            cwd="/",
            env=self._compose_env_vars(),
            timeout_sec=timeout_sec,
        )

    # -- staging -------------------------------------------------------------

    async def _stage_resources_compose_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            local_path = Path(temp_dir) / RESOURCES_COMPOSE_NAME
            write_resources_compose_file(
                local_path,
                cpu_request=self._resource_request_value("cpu", auto_mode=ResourceMode.LIMIT),
                cpu_limit=self._resource_limit_value("cpu", auto_mode=ResourceMode.LIMIT),
                memory_request_mb=self._resource_request_value("memory", auto_mode=ResourceMode.LIMIT),
                memory_limit_mb=self._resource_limit_value("memory", auto_mode=ResourceMode.LIMIT),
            )
            await self._upload_file_to_host(local_path, f"{self._compose_dir_vm}/{RESOURCES_COMPOSE_NAME}")

    async def _stage_mounts_compose_file(self, volumes: list[ServiceVolumeConfig]) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            local_path = Path(temp_dir) / _MOUNTS_COMPOSE_NAME
            write_mounts_compose_file(local_path, volumes)
            await self._upload_file_to_host(local_path, f"{self._compose_dir_vm}/{_MOUNTS_COMPOSE_NAME}")

    async def _stage_extra_compose_files(self) -> None:
        for source, target in zip(
            self.extra_docker_compose_paths,
            self._extra_compose_target_paths(),
            strict=True,
        ):
            await self._upload_file_to_host(source, target)

    async def _start_compose(self, force_build: bool) -> None:
        await self._ensure_docker_ready()
        session_dir = self._session_dir_vm
        stage_result = await self._host_exec(
            f"mkdir -p {shlex.quote(_HARBOR_ROOT_VM)} "
            f"&& rm -rf {shlex.quote(session_dir)} "
            f"&& mkdir -p {shlex.quote(self._compose_dir_vm)} "
            f"{shlex.quote(self._environment_dir_vm)}",
            cwd="/",
            timeout_sec=30,
        )
        if stage_result.return_code != 0:
            raise RuntimeError(
                f"Failed to prepare Plato staging directories: {stage_result.stdout} {stage_result.stderr}"
            )
        for path in (
            COMPOSE_BUILD_PATH,
            COMPOSE_PREBUILT_PATH,
            COMPOSE_NO_NETWORK_PATH,
        ):
            await self._upload_file_to_host(path, f"{self._compose_dir_vm}/{path.name}")

        self._use_prebuilt = should_use_prebuilt_docker_image(
            self.environment_dir,
            docker_image=self.task_env_config.docker_image,
            force_build=force_build,
        )

        await self._stage_resources_compose_file()
        await self._upload_dir_to_host(self.environment_dir, self._environment_dir_vm)
        await self._stage_extra_compose_files()

        volumes = self._resolve_volumes()
        await self._stage_mounts_compose_file(volumes)

        bind_sources = [volume["source"] for volume in volumes if volume["type"] == "bind"]
        if bind_sources:
            quoted = " ".join(shlex.quote(source) for source in bind_sources)
            result = await self._host_exec(
                f"mkdir -p {quoted} && chmod 777 {quoted}",
                cwd="/",
                timeout_sec=30,
            )
            if result.return_code != 0:
                raise RuntimeError(f"Failed to prepare Plato bind mount directories: {result.stdout} {result.stderr}")

        if not self._use_prebuilt:
            build_result = await self._compose_exec(
                ["build"],
                timeout_sec=round(self.task_env_config.build_timeout_sec),
            )
            if build_result.return_code != 0:
                raise RuntimeError(
                    f"docker compose build failed on Plato VM: {build_result.stdout} {build_result.stderr}"
                )

        up_result = await self._compose_exec(
            ["up", "-d"],
            timeout_sec=self.compose_up_timeout_sec,
        )
        if up_result.return_code != 0:
            raise RuntimeError(f"docker compose up failed on Plato VM: {up_result.stdout} {up_result.stderr}")

        await self._wait_for_main_container()
        await self._upload_environment_dir_after_start()

    async def _wait_for_main_container(self, timeout_sec: int = 120) -> None:
        self.logger.debug("Waiting for Plato Docker Compose main service...")
        for _ in range(max(1, timeout_sec // 2)):
            result = await self._compose_exec(
                ["exec", "-T", MAIN_SERVICE_NAME, "true"],
                timeout_sec=10,
            )
            if result.return_code == 0:
                return
            await asyncio.sleep(2)
        raise RuntimeError(f"Main compose service was not ready on the Plato VM after {timeout_sec}s.")

    # -- lifecycle -----------------------------------------------------------

    @override
    async def start(self, force_build: bool) -> None:
        self._plato = AsyncPlato()
        self._session = await self._plato.sessions.create(
            envs=[Env.artifact(self._artifact_id, alias=self._simulator)],
            timeout=self._session_timeout,
            wait=True,
        )
        vm = self._session.desktop_env
        if vm is None:
            envs = self._session.envs
            vm = envs[0] if envs else None
        if vm is None:
            raise RuntimeError("Plato session created but exposed no environment.")
        # Env.artifact() yields an env without a simulator; set one so the SDK
        # can resolve the desktop client if needed.
        if not vm.simulator:
            vm.simulator = self._simulator
        self._vm = vm

        # Snapshot-restored VMs boot with a frozen clock; fix it before any
        # Docker pull/build so registry TLS validation succeeds.
        try:
            await vm.set_date(datetime.now(UTC))
        except Exception as exc:  # noqa: BLE001 - non-fatal; pulls may still work
            self.logger.warning("Failed to set Plato VM date: %s", exc)

        await self._start_compose(force_build)

    @override
    async def stop(self, delete: bool) -> None:
        if self._vm is not None:
            try:
                down_result = await self._compose_exec(["down", "--remove-orphans"], timeout_sec=60)
                if down_result.return_code != 0:
                    self.logger.warning(
                        "docker compose down failed on Plato VM: %s %s",
                        down_result.stdout,
                        down_result.stderr,
                    )
            except Exception as exc:  # noqa: BLE001 - cleanup must not raise
                self.logger.warning("Failed to stop Plato Compose project: %s", exc)
            try:
                await self._host_exec(
                    f"rm -rf {shlex.quote(self._session_dir_vm)}",
                    cwd="/",
                    timeout_sec=30,
                )
            except Exception as exc:  # noqa: BLE001 - cleanup must not raise
                self.logger.warning("Failed to clean Plato staging directory: %s", exc)

        if self._session is not None:
            try:
                await self._session.close()
            except Exception as exc:  # noqa: BLE001 - cleanup must not raise
                self.logger.warning("Error closing Plato session: %s", exc)
            finally:
                self._session = None
                self._vm = None

        if self._plato is not None:
            try:
                await self._plato.close()
            except Exception as exc:  # noqa: BLE001 - cleanup must not raise
                self.logger.warning("Error closing Plato client: %s", exc)
            finally:
                self._plato = None

    # -- Harbor exec / transfer surface (delegates to the container) ---------

    @override
    async def exec(
        self,
        command: str,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
        timeout_sec: int | None = None,
        user: str | int | None = None,
    ) -> ExecResult:
        return await self._compose_ops.exec(
            command,
            cwd=cwd or self.task_env_config.workdir,
            env=self._merge_env(env),
            timeout_sec=timeout_sec,
            user=self._resolve_user(user),
        )

    @override
    async def upload_file(self, source_path: Path | str, target_path: str) -> None:
        await self._compose_ops.upload_file(source_path, target_path)

    @override
    async def upload_dir(self, source_dir: Path | str, target_dir: str) -> None:
        await self._compose_ops.upload_dir(source_dir, target_dir)

    @override
    async def download_file(self, source_path: str, target_path: Path | str) -> None:
        await self._compose_ops.download_file(source_path, target_path)

    @override
    async def download_dir(self, source_dir: str, target_dir: Path | str) -> None:
        await self._compose_ops.download_dir(source_dir, target_dir)

    @override
    def _compose_service_transport(self, service: str | None) -> ComposeServiceTransport:
        return self._compose_ops
