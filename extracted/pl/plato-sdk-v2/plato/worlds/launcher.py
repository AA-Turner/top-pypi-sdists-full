"""Helpers for launching worlds inside managed runtimes."""

from __future__ import annotations

import asyncio
import base64
import json
import logging
import shlex
import tempfile
import uuid
from collections.abc import Awaitable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Literal, cast

from pydantic import BaseModel

import plato
from plato.runtimes import create_runtime
from plato.runtimes.base import Runtime, RuntimeInfo, VMMetadata
from plato.runtimes.config import RuntimeConfig, VMRuntimeConfig
from plato.runtimes.settings import get_settings
from plato.runtimes.vm import VMRuntime
from plato.utils.ssh import generate_ssh_key
from plato.utils.subprocess import SSH_OPTS, VM_VENV_PYTHON
from plato.v2 import AsyncPlato
from plato.worlds.config import ChronosConfig, DevConfig
from plato.worlds.testing import WorldTestRunResult, WorldTestSpec, dump_world_test_spec

if TYPE_CHECKING:
    from plato.v2.async_.session import Session

WorldLaunchMode = Literal["dev", "image", "test"]

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class WorldLaunchResult:
    """Result of executing ``plato-world-runner`` inside a runtime."""

    exit_code: int
    stdout: str
    stderr: str
    result: WorldTestRunResult | None = None


class WorldLauncher:
    """Launch worlds inside a managed runtime.

    The launcher owns runtime construction and lifecycle. For VM runtimes it can
    create a session automatically from ``PLATO_API_KEY`` when one is not
    supplied explicitly.
    """

    def __init__(
        self,
        runtime_config: RuntimeConfig,
        *,
        api_key: str | None = None,
        session: Session | None = None,
        ssh_key_path: Path | None = None,
    ) -> None:
        self._runtime_config = runtime_config
        self._api_key = api_key
        self._provided_session = session
        self._ssh_key_path = ssh_key_path

        self._runtime: Runtime | None = None
        self._runtime_info: RuntimeInfo | None = None
        self._world_runtime_info: RuntimeInfo | None = None
        self._session: Session | None = session
        self._plato_client: AsyncPlato | None = None

        self._owns_session = session is None
        self._owns_plato_client = False
        self._owns_ssh_key = ssh_key_path is None
        self._sdk_synced = False
        self._runtime_key_synced = False

    @property
    def runtime(self) -> Runtime:
        if self._runtime is None:
            raise RuntimeError("WorldLauncher runtime not started")
        return self._runtime

    @property
    def runtime_info(self) -> RuntimeInfo:
        if self._runtime_info is None:
            raise RuntimeError("WorldLauncher runtime not started")
        return self._runtime_info

    async def start(self, *, timeout: int = 300, alias: str | None = None) -> RuntimeInfo:
        """Start the runtime if needed and return its ``RuntimeInfo``."""
        if self._runtime_info is not None:
            return self._runtime_info

        if isinstance(self._runtime_config, VMRuntimeConfig) and alias is None:
            alias = "runtime"

        logger.debug("Starting world runtime: type=%s alias=%s", self._runtime_config.type, alias)
        ssh_key_path = self._ssh_key_path or generate_ssh_key()
        self._ssh_key_path = ssh_key_path

        runtime: Runtime
        runtime_info: RuntimeInfo
        if isinstance(self._runtime_config, VMRuntimeConfig):
            if self._session is None:
                api_key = self._launcher_api_key()
                if not api_key:
                    raise RuntimeError("PLATO_API_KEY is required to launch a VM world runtime")
                self._plato_client = AsyncPlato(api_key=api_key)
                self._owns_plato_client = True
                self._session = await self._plato_client.sessions.create(envs=[], connect_network=True, wait=False)

            runtime = create_runtime(
                self._runtime_config,
                session=self._session,
                ssh_key_path=ssh_key_path,
            )
        else:
            runtime = create_runtime(
                self._runtime_config,
                ssh_key_path=ssh_key_path,
            )

        runtime_info = await runtime.start(timeout=timeout, alias=alias)
        if self._session is not None:
            runtime_info = runtime_info.model_copy(update={"serialized_session": self._session.dump()})

        self._runtime = runtime
        self._runtime_info = runtime_info
        self._world_runtime_info = runtime_info
        logger.debug(
            "World runtime started: type=%s runtime_id=%s hostname=%s",
            self._runtime_config.type,
            runtime_info.runtime_id,
            runtime_info.hostname,
        )
        return runtime_info

    async def close(self) -> None:
        """Stop the runtime and release owned resources."""
        runtime = self._runtime
        runtime_info = self._runtime_info
        if runtime is not None and runtime_info is not None:
            logger.debug("Stopping world runtime: runtime_id=%s", runtime_info.runtime_id)
            await runtime.stop(runtime_info.runtime_id)

        if self._session is not None and self._owns_session:
            try:
                await self._session.close()
            except Exception:
                pass

        if self._plato_client is not None and self._owns_plato_client:
            try:
                await self._plato_client.close()
            except Exception:
                pass

        self._runtime = None
        self._runtime_info = None
        self._world_runtime_info = None
        self._session = self._provided_session
        self._plato_client = None
        self._owns_plato_client = False
        self._sdk_synced = False
        self._runtime_key_synced = False

        if self._owns_ssh_key:
            self._ssh_key_path = None

    async def __aenter__(self) -> WorldLauncher:
        await self.start()
        return self

    async def __aexit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        del exc_type, exc_value, traceback
        await self.close()

    async def prepare(
        self,
        *,
        mode: WorldLaunchMode,
        sdk_root: Path | None = None,
        extra_sync: dict[str, Path] | None = None,
    ) -> None:
        """Prepare the runtime for world execution."""
        await self.start()
        logger.debug("Preparing world runtime: mode=%s", mode)

        needs_sdk = mode in {"dev", "test"} and not self._sdk_synced
        sync_tasks: list[Awaitable[None]] = []
        if needs_sdk:
            sync_tasks.append(self._sync_sdk(sdk_root or _find_sdk_root()))
        if mode in {"dev", "test"} and extra_sync:
            sync_tasks.extend(self._sync_extra_path(name, path) for name, path in extra_sync.items())
        if not self._runtime_key_synced:
            sync_tasks.append(self._sync_runtime_ssh_key())
        if sync_tasks:
            await asyncio.gather(*sync_tasks)

        if needs_sdk:
            await self._install_sdk()
            self._sdk_synced = True
        if not self._runtime_key_synced:
            self._runtime_key_synced = True

    async def launch(
        self,
        *,
        mode: WorldLaunchMode,
        timeout: int = 60,
        sdk_root: Path | None = None,
        chronos: Mapping[str, object] | ChronosConfig | None = None,
        dev: Mapping[str, object] | DevConfig | None = None,
        world: str | None = None,
        config: Mapping[str, object] | BaseModel | None = None,
        test_spec: WorldTestSpec | None = None,
        config_overrides: dict[str, object] | None = None,
    ) -> WorldLaunchResult:
        """Launch a world or test harness based on ``mode``."""
        extra_sync = _extract_extra_sync_paths(dev)
        await self.prepare(mode=mode, sdk_root=sdk_root, extra_sync=extra_sync)
        logger.debug("Launching world: mode=%s world=%s", mode, world or "plato-world-test-harness")
        chronos_dict = _model_to_dict(chronos)
        if "api_key" not in chronos_dict:
            chronos_dict["api_key"] = self._launcher_api_key()

        if mode == "test":
            if test_spec is None:
                raise ValueError("test_spec is required when mode='test'")
            return await self._launch_test_impl(
                test_spec=test_spec,
                timeout=timeout,
                sdk_root=sdk_root,
                chronos=chronos_dict,
                dev=_model_to_dict(dev),
                config_overrides=config_overrides,
            )

        if world is None:
            raise ValueError("world is required when mode is not 'test'")
        if config is None:
            raise ValueError("config is required when mode is not 'test'")

        return await self._launch_prod_impl(
            world=world,
            config=_model_to_dict(config),
            timeout=timeout,
            chronos=chronos_dict,
            dev=_model_to_dict(dev),
        )

    async def write_file(self, remote_path: str, content: str) -> None:
        """Write a file into the runtime via ``runtime.exec``.

        Uses chunked base64 encoding to avoid hitting ARG_MAX limits on
        large payloads (e.g. structured-execution configs with inline step
        instructions can exceed 128 KB).
        """
        await self.start()

        encoded = base64.b64encode(content.encode()).decode()
        q_dir = shlex.quote(str(Path(remote_path).parent))
        q_path = shlex.quote(remote_path)

        if not encoded:
            code, _, stderr = await self.runtime.exec(
                self.runtime_info.runtime_id,
                f"mkdir -p {q_dir} && : > {q_path}",
                timeout=30,
            )
            if code != 0:
                raise RuntimeError(f"Failed to write {remote_path}: {stderr}")
            return

        q_tmp = shlex.quote(f"{remote_path}.b64tmp")
        chunk_size = 65536
        chunks = [encoded[i : i + chunk_size] for i in range(0, len(encoded), chunk_size)]

        # First chunk: create directory and write (truncate)
        code, _, stderr = await self.runtime.exec(
            self.runtime_info.runtime_id,
            f"mkdir -p {q_dir} && printf '%s' '{chunks[0]}' > {q_tmp}",
            timeout=30,
        )
        if code != 0:
            raise RuntimeError(f"Failed to write {remote_path}: {stderr}")

        # Remaining chunks: append
        for chunk in chunks[1:]:
            code, _, stderr = await self.runtime.exec(
                self.runtime_info.runtime_id,
                f"printf '%s' '{chunk}' >> {q_tmp}",
                timeout=30,
            )
            if code != 0:
                raise RuntimeError(f"Failed to write {remote_path}: {stderr}")

        # Decode and clean up
        code, _, stderr = await self.runtime.exec(
            self.runtime_info.runtime_id,
            f"base64 -d < {q_tmp} > {q_path} && rm -f {q_tmp}",
            timeout=30,
        )
        if code != 0:
            raise RuntimeError(f"Failed to write {remote_path}: {stderr}")

    async def write_config(self, config: Mapping[str, object], *, remote_path: str = "/tmp/config.json") -> None:
        """Write a JSON config file into the runtime."""
        await self.write_file(remote_path, json.dumps(config))

    async def sync_dir(self, local_path: Path, remote_path: str, *, delete: bool = True) -> None:
        """Sync a local directory into the runtime via rsync over SSH."""
        await self.start()

        user = self._ssh_user()
        host = self._ssh_host()
        ssh_cmd = self._rsync_ssh_command()
        args = [
            "rsync",
            "-az",
            "--exclude=.venv",
            "--exclude=__pycache__",
            "--exclude=.git",
            "--exclude=*.pyc",
            "--exclude=.pytest_cache",
            "-e",
            ssh_cmd,
        ]
        if delete:
            args.append("--delete")

        mkdir_proc = await asyncio.create_subprocess_exec(
            *self._ssh_command(),
            f"mkdir -p {remote_path.rstrip('/')}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, mkdir_err = await asyncio.wait_for(mkdir_proc.communicate(), timeout=30)
        if mkdir_proc.returncode != 0:
            raise RuntimeError(f"Failed to create remote directory {remote_path}: {mkdir_err.decode()}")

        proc = await asyncio.create_subprocess_exec(
            *args,
            f"{local_path}/",
            f"{user}@{host}:{remote_path.rstrip('/')}/",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, err = await asyncio.wait_for(proc.communicate(), timeout=60)
        if proc.returncode != 0:
            raise RuntimeError(f"Failed to sync {local_path} to {remote_path}: {err.decode()}")

    async def run_script(
        self,
        script: str,
        *,
        remote_path: str = "/tmp/world_launcher_script.py",
        timeout: int = 60,
    ) -> WorldLaunchResult:
        """Write a Python script into the runtime and execute it."""
        await self.write_file(remote_path, script)
        exit_code, stdout, stderr = await self.runtime.exec(
            self.runtime_info.runtime_id,
            f"python3 {remote_path}",
            timeout=timeout,
        )
        return WorldLaunchResult(exit_code=exit_code, stdout=stdout, stderr=stderr)

    async def _launch_prod_impl(
        self,
        *,
        world: str,
        config: dict[str, object],
        timeout: int,
        chronos: dict[str, object],
        dev: dict[str, object],
    ) -> WorldLaunchResult:
        logger.debug("Running world via plato-world-runner: world=%s", world)
        remote_bundle_dir = f"/tmp/plato-world-launch-{uuid.uuid4().hex}"
        remote_config_path = f"{remote_bundle_dir}/config.json"
        remote_log_path = f"{remote_bundle_dir}/runner.log"
        await self.write_config(
            self._build_runner_config(
                config=config,
                chronos=chronos,
                dev=dev,
            )
        )

        runner_cmd = (
            f"{self._runner_env_prefix()}"
            f"cp /tmp/config.json {remote_config_path} && "
            f"bash -lc {shlex.quote(f'set -o pipefail; plato-world-runner run --world {world} --config {remote_config_path} 2>&1 | tee {remote_log_path}')}"
        )
        exit_code, _, stderr = await self.runtime.exec(
            self.runtime_info.runtime_id,
            f"mkdir -p {remote_bundle_dir} && {runner_cmd}",
            timeout=timeout,
            stream=True,
        )
        stdout = await self._read_remote_file(remote_log_path)
        return WorldLaunchResult(exit_code=exit_code, stdout=stdout, stderr=stderr)

    async def _launch_test_impl(
        self,
        *,
        test_spec: WorldTestSpec,
        timeout: int,
        sdk_root: Path | None,
        chronos: dict[str, object],
        dev: dict[str, object],
        config_overrides: dict[str, object] | None,
    ) -> WorldLaunchResult:
        del sdk_root

        logger.debug("Preparing test world bundle: spec=%s", test_spec.name)
        remote_bundle_dir = f"/tmp/plato-world-test-{uuid.uuid4().hex}"
        remote_result_path = f"{remote_bundle_dir}/result.json"
        remote_log_path = f"{remote_bundle_dir}/runner.log"

        world_config: dict[str, object] = {
            "state": {"enabled": False},
            "test_spec_path": f"{remote_bundle_dir}/spec.json",
            "result_path": remote_result_path,
        }
        if config_overrides:
            _deep_merge(world_config, config_overrides)

        with tempfile.TemporaryDirectory(prefix="plato-world-test-") as tmp_dir:
            bundle_dir = Path(tmp_dir)
            dump_world_test_spec(test_spec, bundle_dir)
            logger.debug("Syncing test world bundle to runtime: remote_dir=%s", remote_bundle_dir)
            await asyncio.gather(
                self.write_config(
                    self._build_runner_config(
                        config=world_config,
                        chronos=chronos,
                        dev=dev,
                    )
                ),
                self.sync_dir(bundle_dir, remote_bundle_dir),
            )

        remote_config_path = f"{remote_bundle_dir}/config.json"
        logger.debug("Running harness world via plato-world-runner: config=%s", remote_config_path)
        runner_cmd = (
            f"{self._runner_env_prefix()}"
            f"cp /tmp/config.json {remote_config_path} && "
            f"bash -lc {shlex.quote(f'set -o pipefail; plato-world-runner run --world plato-world-test-harness --config {remote_config_path} 2>&1 | tee {remote_log_path}')}"
        )
        exit_code, _, stderr = await self.runtime.exec(
            self.runtime_info.runtime_id,
            runner_cmd,
            timeout=timeout,
            stream=True,
        )
        stdout = await self._read_remote_file(remote_log_path)
        result = await self._read_world_test_result(remote_result_path)
        return WorldLaunchResult(exit_code=exit_code, stdout=stdout, stderr=stderr, result=result)

    async def _read_remote_file(self, remote_path: str) -> str:
        quoted_path = shlex.quote(remote_path)
        code, stdout, _ = await self.runtime.exec(
            self.runtime_info.runtime_id,
            f"test -f {quoted_path} && cat {quoted_path}",
            timeout=30,
        )
        if code != 0:
            return ""
        return stdout

    async def _sync_sdk(self, sdk_root: Path) -> None:
        logger.debug("Syncing SDK to runtime: source=%s", sdk_root)
        user = self._ssh_user()
        host = self._ssh_host()
        ssh_cmd = self._rsync_ssh_command()

        proc = await asyncio.create_subprocess_exec(
            "rsync",
            "-az",
            "--delete",
            "--exclude=.venv",
            "--exclude=__pycache__",
            "--exclude=.git",
            "--exclude=*.pyc",
            "--exclude=dist",
            "--exclude=.mypy_cache",
            "--exclude=.pytest_cache",
            "-e",
            ssh_cmd,
            f"{sdk_root}/",
            f"{user}@{host}:/sdk/",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, err = await asyncio.wait_for(proc.communicate(), timeout=60)
        if proc.returncode != 0:
            raise RuntimeError(f"rsync SDK failed: {err.decode()}")

    async def _sync_extra_path(self, name: str, local_path: Path) -> None:
        remote_path = f"/extra/{name}"
        logger.debug("Syncing extra path to runtime: %s -> %s", local_path, remote_path)
        await self.sync_dir(local_path, remote_path)

    async def _install_sdk(self) -> None:
        logger.debug("Installing SDK in runtime with --no-deps fast path")
        code, _, stderr = await self.runtime.exec(
            self.runtime_info.runtime_id,
            f"uv pip install --python {VM_VENV_PYTHON} --no-deps -q /sdk",
            timeout=60,
        )
        if code != 0:
            raise RuntimeError(f"pip install SDK failed: {stderr}")
        logger.debug("SDK install complete")

    async def _sync_runtime_ssh_key(self) -> None:
        ssh_key_path = self.runtime_info.ssh_key_path
        if ssh_key_path is None:
            return

        logger.debug("Syncing runtime SSH key for nested world/agent launches")
        user = self._ssh_user()
        host = self._ssh_host()
        ssh_cmd = self._rsync_ssh_command()
        remote_key_path = "/tmp/plato-runtime-key"
        remote_pub_path = "/tmp/plato-runtime-key.pub"

        for source, target in (
            (ssh_key_path, remote_key_path),
            (Path(str(ssh_key_path) + ".pub"), remote_pub_path),
        ):
            proc = await asyncio.create_subprocess_exec(
                "rsync",
                "-az",
                "-e",
                ssh_cmd,
                str(source),
                f"{user}@{host}:{target}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            _, err = await asyncio.wait_for(proc.communicate(), timeout=30)
            if proc.returncode != 0:
                raise RuntimeError(f"Failed to sync runtime SSH key {source}: {err.decode()}")

        proc = await asyncio.create_subprocess_exec(
            *self._ssh_command(),
            f"chmod 600 {remote_key_path} && chmod 644 {remote_pub_path}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, err = await asyncio.wait_for(proc.communicate(), timeout=10)
        if proc.returncode != 0:
            raise RuntimeError(f"Failed to install runtime SSH key: {err.decode()}")

        self._world_runtime_info = self.runtime_info.model_copy(update={"ssh_key_path": Path(remote_key_path)})
        logger.debug("Runtime SSH key installed at %s", remote_key_path)

    async def _read_world_test_result(self, remote_result_path: str) -> WorldTestRunResult | None:
        exit_code, stdout, _ = await self.runtime.exec(
            self.runtime_info.runtime_id,
            f"test -f {remote_result_path} && cat {remote_result_path}",
            timeout=10,
        )
        if exit_code != 0 or not stdout.strip():
            return None
        return WorldTestRunResult.model_validate_json(stdout)

    def _build_runner_config(
        self,
        *,
        config: dict[str, object],
        chronos: dict[str, object],
        dev: dict[str, object],
    ) -> dict[str, object]:
        if self._world_runtime_info is None:
            raise RuntimeError("WorldLauncher runtime not started")
        runtime_payload = self._world_runtime_info.to_runner_payload()
        if isinstance(self._world_runtime_info.metadata, VMMetadata) and self._world_runtime_info.metadata.hostname:
            runtime_payload["hostname"] = self._world_runtime_info.metadata.hostname

        return {
            "session": chronos,
            "dev": dev,
            "world": {
                "config": config,
                "runtime_info": runtime_payload,
            },
        }

    def _launcher_api_key(self) -> str:
        if self._api_key is not None:
            return self._api_key
        return get_settings().api_key

    def _runner_env_prefix(self) -> str:
        exports: list[str] = []
        api_key = self._launcher_api_key()
        if api_key:
            exports.append(f"export PLATO_API_KEY={shlex.quote(api_key)};")
        if isinstance(self.runtime_info.metadata, VMMetadata) and self.runtime_info.metadata.job_id:
            exports.append(f"export JOB_ID={shlex.quote(self.runtime_info.metadata.job_id)};")
        return " ".join(exports) + (" " if exports else "")

    def _ssh_target(self) -> tuple[str, list[tuple[str, str]]]:
        if isinstance(self.runtime, VMRuntime):
            env = self.runtime.get_env(self.runtime_info.runtime_id)
            return self.runtime._ssh_target(env)
        return self.runtime_info.hostname, []

    def _ssh_host(self) -> str:
        ssh_key = self.runtime_info.ssh_key_path
        host, _ = self._ssh_target()
        if ssh_key is None or not host:
            raise RuntimeError("SSH key and host required for SSH access")
        return host

    def _ssh_user(self) -> str:
        return self.runtime_info.ssh_user or "root"

    def _ssh_base_command(self) -> list[str]:
        ssh_key = self.runtime_info.ssh_key_path
        host, extra_opts = self._ssh_target()
        if ssh_key is None or not host:
            raise RuntimeError("SSH key and host required for SSH access")
        command = ["ssh", "-i", str(ssh_key)]
        for key, value in [*SSH_OPTS, *extra_opts]:
            command.extend(["-o", f"{key}={value}"])
        return command

    def _ssh_command(self) -> list[str]:
        return [*self._ssh_base_command(), f"{self._ssh_user()}@{self._ssh_host()}"]

    def _rsync_ssh_command(self) -> str:
        return shlex.join(self._ssh_base_command())


def _find_sdk_root() -> Path:
    module_file = plato.__file__
    if module_file is None:
        raise RuntimeError("Could not resolve plato package path")
    module_path = Path(module_file).resolve()
    for parent in (module_path.parent, *module_path.parents):
        if (parent / "pyproject.toml").exists() and (parent / "plato").is_dir():
            return parent
    raise RuntimeError(f"Could not resolve plato-sdk-v2 root from {module_path}")


def _model_to_dict(value: Mapping[str, object] | BaseModel | None) -> dict[str, object]:
    if value is None:
        return {}
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json", exclude_none=True)
    return dict(value)


def _extract_extra_sync_paths(value: Mapping[str, object] | BaseModel | None) -> dict[str, Path]:
    if value is None:
        return {}

    raw_extra_sync: object
    if isinstance(value, DevConfig):
        raw_extra_sync = value.extra_sync
    elif isinstance(value, BaseModel):
        raw_extra_sync = getattr(value, "extra_sync", {})
    else:
        raw_extra_sync = value.get("extra_sync", {})

    if not isinstance(raw_extra_sync, Mapping):
        return {}

    normalized: dict[str, Path] = {}
    for name, path_value in raw_extra_sync.items():
        if not isinstance(name, str):
            continue
        if isinstance(path_value, Path):
            normalized[name] = path_value
        elif isinstance(path_value, str):
            normalized[name] = Path(path_value)
    return normalized


def _deep_merge(target: dict[str, object], overrides: dict[str, object]) -> None:
    for key, value in overrides.items():
        existing = target.get(key)
        if isinstance(existing, dict) and isinstance(value, dict):
            _deep_merge(cast(dict[str, object], existing), cast(dict[str, object], value))
        else:
            target[key] = value
