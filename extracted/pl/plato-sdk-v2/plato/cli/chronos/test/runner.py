"""One-shot VM runner for `plato chronos test`."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import shlex
import sys
from datetime import UTC, datetime
from pathlib import Path

import httpx
from rich.console import Console

from plato.chronos.api.sessions import complete_session, create_session
from plato.chronos.models import CompleteSessionRequest, CreateSessionRequest, CreateSessionResponse, Status1
from plato.cli.chronos.dev.paths import get_sdk_root
from plato.cli.chronos.dev.runner import resolve_agent_images
from plato.cli.chronos.dev.ssh import SSHKeyPair, build_ssh_command, build_ssh_command_string
from plato.cli.chronos.dev.sync import SyncManager
from plato.cli.chronos.env import resolve_config_env_vars
from plato.cli.chronos.provision import SyncTarget, provision_vm
from plato.cli.chronos.registry import get_world_schema, parse_package_string
from plato.cli.chronos.settings import get_settings
from plato.cli.chronos.test.config import TestConfig, TestPhaseConfig
from plato.otel import get_tracer, init_tracing, shutdown_tracing
from plato.runtime import VMRuntimeConfig
from plato.utils.pypi_index import plato_token_simple_index, redact_pypi_token_credential
from plato.v2 import AsyncPlato, Env
from plato.v2.types import SimConfigCompute

settings = get_settings()
logger = logging.getLogger(__name__)
console = Console()


def _slug(value: str) -> str:
    out = []
    for char in value.lower():
        if char.isalnum() or char in {"-", "_"}:
            out.append(char)
        elif char.isspace():
            out.append("-")
    return "".join(out).strip("-") or "phase"


def select_test_phases(phases: list[TestPhaseConfig], phase_filter: str) -> list[TestPhaseConfig]:
    """Return configured phases filtered by `unit|integration|all`."""
    requested = phase_filter.strip().lower()
    if requested == "all":
        return phases

    selected = [p for p in phases if p.name.strip().lower() == requested]
    if not selected:
        available = ", ".join(p.name for p in phases)
        raise ValueError(f"No phase named '{phase_filter}'. Available phases: {available}")
    return selected


class TestRunner:
    """Provision a VM, sync code, run test phases, and clean up."""

    def __init__(
        self,
        *,
        config: TestConfig,
        config_path: Path,
        api_key: str,
        phase_filter: str,
        pytest_args: str | None,
        artifacts_dir: Path | None,
        keep_vm_on_fail: bool,
        verbose: bool,
    ):
        self.config = config
        self.config_path = config_path
        self.api_key = api_key
        self.phase_filter = phase_filter
        self.pytest_args = (pytest_args or "").strip()
        self.keep_vm_on_fail = keep_vm_on_fail
        self.verbose = verbose

        self.plato: AsyncPlato | None = None
        self.session = None
        self.world_env = None
        self.ssh_key: SSHKeyPair | None = None
        self.sync_manager: SyncManager | None = None

        run_stamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
        base = artifacts_dir or Path.cwd() / ".chronos-test-artifacts" / run_stamp
        self.artifacts_dir = base.resolve()
        self.logs_dir = self.artifacts_dir / "logs"
        self.junit_dir = self.artifacts_dir / "junit"
        self.summary_path = self.artifacts_dir / "summary.json"

        self.session_id: str = ""
        self._phase_results: list[dict] = []
        self._tracing_initialized = False

    def _print(self, msg: str) -> None:
        """Write to stdout with immediate flush — reliable in agent subprocess contexts."""
        sys.stdout.write(msg + "\n")
        sys.stdout.flush()

    async def run(self) -> int:
        """Run setup + selected test phases. Returns process exit code."""
        exit_code = 1
        error_message: str | None = None

        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.junit_dir.mkdir(parents=True, exist_ok=True)

        try:
            await self._setup_vm()
            selected_phases = select_test_phases(self.config.test.phases, self.phase_filter)
            exit_code = await self._run_phases(selected_phases)
        except KeyboardInterrupt:
            error_message = "Interrupted by user"
            self._print("ERROR: Interrupted by user")
            exit_code = 130
        except Exception as exc:  # noqa: BLE001
            error_message = str(exc)
            self._print(f"ERROR: {error_message}")
            logger.exception("chronos test failed")
            exit_code = 1
        finally:
            status = "completed" if exit_code == 0 else "failed"
            if self.session_id:
                await self._complete_chronos_session(status, exit_code, error_message)

            self._write_summary(exit_code=exit_code, status=status, error_message=error_message)

            keep_vm = self.keep_vm_on_fail and exit_code != 0
            await self._cleanup(keep_vm=keep_vm)

            self._print(f"TEST_STATUS={status}")
            self._print(f"TEST_EXIT_CODE={exit_code}")
            if self.session_id:
                self._print(f"CHRONOS_SESSION_ID={self.session_id}")
                self._print(f"CHRONOS_URL={settings.chronos_url}/sessions/{self.session_id}")

            if keep_vm and self.world_env:
                self._print(f"VM kept alive for debugging: {self.world_env.job_id}")

            console.print(f"\n[dim]Artifacts:[/dim] {self.artifacts_dir}")

        return exit_code

    def _resolve_path(self, value: Path | None) -> Path | None:
        if value is None:
            return None
        if value.is_absolute():
            return value
        return (self.config_path.parent / value).resolve()

    async def _setup_vm(self) -> None:
        world_package, world_version = parse_package_string(self.config.world.package)
        world_image = self.config.world.image
        if not world_image:
            world_schema = await get_world_schema(world_package, world_version, self.config.world.world_name)
            world_image = world_schema.get("image", "")
            if not world_image:
                raise RuntimeError(f"No world image found in schema for {self.config.world.package}")
            # Use the registered world name from the schema if not explicitly set
            if not self.config.world.world_name:
                self.config = self.config.model_copy(
                    update={"world": self.config.world.model_copy(update={"world_name": world_schema.get("name")})}
                )

        chronos = await self._create_chronos_session()
        self.session_id = chronos.public_id
        self._print(f"CHRONOS_SESSION_ID={self.session_id}")
        self._print(f"CHRONOS_URL={settings.chronos_url}/sessions/{self.session_id}")
        otel_url = chronos.otel_url or f"{settings.chronos_url}/api/otel"
        self.config = self.config.model_copy(
            update={
                "session": self.config.session.model_copy(
                    update={
                        "session_id": chronos.public_id,
                        "otel_url": otel_url,
                        "chronos_url": settings.chronos_url,
                    }
                )
            }
        )

        # Initialize OTel tracing now that we have a session
        try:
            init_tracing(
                service_name=f"chronos-test.{world_package}",
                session_id=self.session_id,
                otlp_endpoint=otel_url,
            )
            self._tracing_initialized = True
        except Exception:  # noqa: BLE001
            logger.warning("Failed to initialize OTel tracing", exc_info=True)

        world_runtime = self.config.world.runtime
        if world_runtime.type != "vm" or not isinstance(world_runtime, VMRuntimeConfig):
            raise ValueError("World runtime must be VM for `plato chronos test`")

        self._print("[setup] Provisioning VM...")
        self.plato = AsyncPlato()
        self.session = await self.plato.sessions.create(
            envs=[
                Env.resource(
                    simulator=f"test-{world_package}",
                    sim_config=SimConfigCompute(
                        cpus=world_runtime.vm.cpus,
                        memory=world_runtime.vm.memory,
                        disk=world_runtime.vm.disk,
                    ),
                    alias="runtime",
                    docker_image_url=world_image,
                    upload_rootfs=False,
                    rootfs_storage_backend="snapshot-store",
                )
            ],
            timeout=world_runtime.vm.timeout or 7200,
        )
        await self.session.start_heartbeat()

        # Build sync targets from config
        sync_targets = self._build_sync_targets()

        self._print("[setup] VM provisioned")
        result = await provision_vm(
            session=self.session,
            copy_ssh_key_to_vm=True,
            sync_targets=sync_targets,
            verbose=self.verbose,
        )
        self.world_env = result.env
        self.ssh_key = result.ssh_key
        self.sync_manager = result.sync_manager
        self._print("[setup] SSH connected")

        await self._install_editable_packages()
        self._print("[setup] Code synced and packages installed")
        # Resolve ${VAR} placeholders from Chronos analyzer-env settings
        # (same as the Chronos backend launch flow)
        world_config = self.config.world.config or {}
        await resolve_config_env_vars(world_config, self.api_key)
        # Resolve agent package → image URIs (same as dev runner / Chronos backend)
        await resolve_agent_images(world_config, self.api_key)
        await self._write_runtime_files()

        self._print("[setup] VM ready for tests")

    def _build_sync_targets(self) -> list[SyncTarget]:
        """Build the list of sync targets from config."""
        targets: list[SyncTarget] = []

        world_path = self._resolve_path(self.config.dev.world)
        if world_path:
            targets.append(SyncTarget(local_path=world_path, remote_path="/world"))

        for name, agent_path in self.config.dev.agents.items():
            resolved = self._resolve_path(agent_path)
            if resolved:
                targets.append(SyncTarget(local_path=resolved, remote_path=f"/agents/{name}"))

        for name, extra_path in self.config.dev.extra_sync.items():
            resolved = self._resolve_path(extra_path)
            if resolved:
                targets.append(SyncTarget(local_path=resolved, remote_path=f"/extra/{name}"))

        if self.config.dev.sync_sdk:
            sdk_root = get_sdk_root()
            if sdk_root and (sdk_root / "pyproject.toml").exists():
                targets.append(SyncTarget(local_path=sdk_root, remote_path="/sdk"))

        if not targets:
            raise RuntimeError("No sync targets configured. Provide `dev.world` and/or `dev.agents`.")

        return targets

    async def _install_editable_packages(self) -> None:
        if not self.world_env:
            raise RuntimeError("world_env must be initialized")

        from time import perf_counter

        self._print("[setup] Installing packages...")
        logger.info("Installing editable packages on VM...")

        t0 = perf_counter()
        await self.world_env.execute(
            "dpkg -s fuse3 > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq fuse3) > /dev/null 2>&1",
            timeout=60,
        )
        logger.info("fuse3 check: %.1fs", perf_counter() - t0)

        # Clean build artifacts so editable install uses fresh source
        if self.config.dev.world:
            await self.world_env.execute(
                "rm -rf /world/dist /world/*.egg-info /world/src/*.egg-info /world/build",
                timeout=20,
            )

        # Uninstall published packages, then reinstall as editable.
        # Use base SDK (no [worlds] extra) — DVC/dvc-s3 are already in the
        # VM image and don't need re-resolving, which saves ~90s.
        uninstall_pkgs: list[str] = []
        editables: list[str] = []

        if self.config.dev.sync_sdk:
            uninstall_pkgs.append("plato-sdk-v2")
            editables.append("-e /sdk")

        if self.config.dev.world:
            t0 = perf_counter()
            world_pkgs = await self.world_env.execute(
                'python3 -c "import importlib.metadata; '
                "eps = importlib.metadata.entry_points(group='plato.worlds'); "
                "print(' '.join(set(ep.dist.name for ep in eps)))\" 2>/dev/null || true",
                timeout=30,
            )
            installed_world_pkgs = (world_pkgs.stdout or "").strip()
            if installed_world_pkgs:
                uninstall_pkgs.extend(installed_world_pkgs.split())
            editables.append("-e /world")

        for name in self.config.dev.agents:
            editables.append(f"-e /agents/{name}")

        if not editables:
            return

        if uninstall_pkgs:
            t0 = perf_counter()
            await self.world_env.execute(
                f"uv pip uninstall --system {' '.join(uninstall_pkgs)}",
                timeout=90,
            )
            logger.info("Uninstalled %s: %.1fs", " ".join(uninstall_pkgs), perf_counter() - t0)

        store_idx = plato_token_simple_index("pypi-store", api_key=self.api_key)
        install_cmd = (
            f"UV_HTTP_TIMEOUT=90 uv pip install --system --default-index {shlex.quote(store_idx)} {' '.join(editables)}"
        )
        logger.info("Installing: %s", redact_pypi_token_credential(install_cmd))
        t0 = perf_counter()
        result = await self.world_env.execute(install_cmd, timeout=300)
        if result.exit_code != 0:
            raise RuntimeError(f"Editable install failed: {result.stderr}")
        logger.info("Editable install complete: %.1fs", perf_counter() - t0)

    async def _run_phases(self, phases: list[TestPhaseConfig]) -> int:
        if not phases:
            raise RuntimeError("No test phases selected")

        for index, phase in enumerate(phases, start=1):
            slug = _slug(phase.name)
            log_path = self.logs_dir / f"{index:02d}-{slug}.log"
            remote_junit = phase.junit_path

            cmd = phase.command
            if remote_junit and "pytest" in cmd and "--junitxml" not in cmd:
                cmd = f"{cmd} --junitxml={shlex.quote(remote_junit)}"
            if self.pytest_args:
                cmd = f"{cmd} {self.pytest_args}"

            self._print(f"[test] Phase {index}/{len(phases)}: {phase.name}")

            tracer = get_tracer("chronos-test")
            with tracer.start_as_current_span(f"test.phase.{slug}") as span:
                rc = await self._run_phase_command(cmd=cmd, phase_name=phase.name, log_path=log_path)
                if rc != 0:
                    span.set_attribute("error", True)
                span.set_attribute("exit_code", rc)

            junit_local = None
            if remote_junit:
                junit_local = self.junit_dir / f"{index:02d}-{slug}.xml"
                fetched = await self._fetch_remote_file(remote_junit, junit_local)
                if not fetched:
                    junit_local = None

            result = {
                "name": phase.name,
                "command": cmd,
                "exit_code": rc,
                "log": str(log_path),
                "junit": str(junit_local) if junit_local else None,
            }
            self._phase_results.append(result)

            if rc != 0:
                self._print(f"[test] FAILED (exit {rc}): {phase.name}")
                return rc

            self._print(f"[test] PASSED: {phase.name}")

        return 0

    async def _run_phase_command(self, *, cmd: str, phase_name: str, log_path: Path) -> int:
        if not self.world_env or not self.ssh_key:
            raise RuntimeError("VM and SSH key must be initialized")

        env_map = {"PLATO_API_KEY": self.api_key, **self.config.test.env}

        for env_name in self.config.test.pass_env:
            value = os.environ.get(env_name)
            if value:
                env_map[env_name] = value

        export_parts = [f"export {key}={shlex.quote(value)};" for key, value in sorted(env_map.items())]
        script = (
            "set -euo pipefail; "
            f"cd {shlex.quote(self.config.test.workdir)}; "
            + " ".join(export_parts)
            + f" echo {shlex.quote(f'>>> Running phase: {phase_name}')}; "
            + cmd
        )
        remote_cmd = f"bash -lc {shlex.quote(script)}"

        ssh_cmd = build_ssh_command(self.world_env.job_id, self.ssh_key.private_key_path)
        ssh_cmd.append(remote_cmd)

        proc = await asyncio.create_subprocess_exec(
            *ssh_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        stdout_data, _ = await proc.communicate()
        output = stdout_data.decode(errors="replace") if stdout_data else ""
        log_path.write_text(output, encoding="utf-8")

        return proc.returncode or 0

    async def _fetch_remote_file(self, remote_path: str, local_path: Path) -> bool:
        if not self.world_env or not self.ssh_key:
            raise RuntimeError("VM and SSH key must be initialized")

        exists = await self.world_env.execute(
            f"test -f {shlex.quote(remote_path)}",
            timeout=10,
        )
        if exists.exit_code != 0:
            return False

        local_path.parent.mkdir(parents=True, exist_ok=True)

        ssh_str = build_ssh_command_string(self.world_env.job_id, self.ssh_key.private_key_path)
        host = f"root@{self.world_env.job_id}.plato"
        proc = await asyncio.create_subprocess_exec(
            "rsync",
            "-az",
            "-e",
            ssh_str,
            f"{host}:{remote_path}",
            str(local_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()
        if proc.returncode != 0:
            logger.warning("Failed to fetch %s: %s", remote_path, stderr.decode(errors="replace"))
            return False
        return True

    async def _write_file_to_vm(self, remote_path: str, content: str, *, mkdir: bool = False) -> None:
        """Write content to a file on the VM using base64 to avoid shell escaping issues."""
        if not self.world_env:
            raise RuntimeError("world_env must be initialized")
        import base64

        b64 = base64.b64encode(content.encode()).decode()
        prefix = f"mkdir -p $(dirname {remote_path}) && " if mkdir else ""
        result = await self.world_env.execute(
            f"{prefix}echo '{b64}' | base64 -d > {remote_path}",
            timeout=30,
        )
        if result.exit_code != 0:
            raise RuntimeError(f"Failed to write {remote_path}: {result.stderr}")

    async def _write_runtime_files(self) -> None:
        if not self.world_env or not self.session:
            raise RuntimeError("world_env and session must be initialized")

        self.config = self.config.model_copy(
            update={
                "dev": self.config.dev.model_copy(update={"ssh_key_path": Path("/root/.ssh/agent_key")}),
                "session": self.config.session.model_copy(update={"plato_session": self.session.dump()}),
            }
        )

        config_json = json.dumps(self.config.model_dump(mode="json"))
        await self._write_file_to_vm("/tmp/config.json", config_json)

        if self.config.session.plato_session:
            session_json = json.dumps(self.config.session.plato_session.model_dump(mode="json"))
            await self._write_file_to_vm("/etc/plato/session.json", session_json, mkdir=True)

    async def _create_chronos_session(self) -> CreateSessionResponse:
        world_config = self.config.world.config or {}
        tags = list({*self.config.tags, "test", "ci.test"})
        # world_name is resolved from the schema in _setup_vm, or set
        # explicitly in the config. Fall back to package name as last resort.
        world_name = self.config.world.world_name
        if not world_name:
            pkg, _ = parse_package_string(self.config.world.package)
            world_name = pkg.removeprefix("plato-world-")
            logger.warning("world_name not set, falling back to '%s'", world_name)
        body = CreateSessionRequest(
            world_name=world_name,
            world_config=world_config,
            tags=tags,
        )
        async with httpx.AsyncClient(
            base_url=settings.chronos_url.rstrip("/"),
            timeout=30.0,
        ) as client:
            return await create_session.asyncio(client, body=body, x_api_key=self.api_key)

    async def _complete_chronos_session(
        self,
        status: str,
        exit_code: int,
        error_message: str | None,
    ) -> None:
        if not self.session_id:
            return

        body = CompleteSessionRequest(
            status=Status1(status),
            exit_code=exit_code,
            error_message=error_message[:500] if error_message else None,
        )
        try:
            async with httpx.AsyncClient(
                base_url=settings.chronos_url.rstrip("/"),
                timeout=30.0,
            ) as client:
                await complete_session.asyncio(
                    client,
                    public_id=self.session_id,
                    body=body,
                    x_api_key=self.api_key,
                )
        except Exception:  # noqa: BLE001
            logger.warning("Failed to complete Chronos session", exc_info=True)

    def _write_summary(self, *, exit_code: int, status: str, error_message: str | None) -> None:
        summary = {
            "generated_at": datetime.now(UTC).isoformat(),
            "session_id": self.session_id,
            "world_job_id": self.world_env.job_id if self.world_env else None,
            "status": status,
            "exit_code": exit_code,
            "error": error_message,
            "phase_filter": self.phase_filter,
            "phases": self._phase_results,
        }
        self.summary_path.write_text(json.dumps(summary, indent=2) + "\n")

    async def _cleanup(self, *, keep_vm: bool) -> None:
        if self._tracing_initialized:
            shutdown_tracing()

        if self.sync_manager:
            self.sync_manager.stop()

        if keep_vm:
            return

        logger.info("Cleaning up session and VM...")
        if self.session:
            await self.session.close()
            logger.info("Session closed: %s", self.session_id)
        if self.plato:
            await self.plato.close()
        logger.info("Cleanup complete.")


TestRunner.__test__ = False

__all__ = ["TestRunner", "select_test_phases"]
