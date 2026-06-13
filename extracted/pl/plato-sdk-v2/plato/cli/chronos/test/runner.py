"""One-shot VM runner for `plato chronos test`."""

from __future__ import annotations

import asyncio
import base64
import json
import logging
import os
import shlex
import signal
import sys
import tempfile
import uuid
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter

import httpx
from pydantic import BaseModel
from rich.console import Console

from plato.agents.install import (
    CLEAN_WORLD_BUILD_ARTIFACTS_COMMAND,
    DISCOVER_WORLD_PACKAGES_COMMAND,
    ENSURE_FUSE3_COMMAND,
    build_editable_install_commands,
    build_world_deps_sync_command,
)
from plato.chronos.api.registry import (
    get_world_schema_api_registry_worlds__package_name__schema_get as get_world_schema_api,
)
from plato.chronos.api.sessions import (
    complete_session,
    create_session,
    link_plato_session,
    update_session_status,
)
from plato.chronos.models import (
    CompleteSessionRequest,
    CreateSessionRequest,
    CreateSessionResponse,
    LinkPlatoSessionRequest,
    Status1,
    UpdateStatusRequest,
)
from plato.cli.chronos.dev.runner import resolve_agent_images
from plato.cli.chronos.dev.ssh import SSHKeyPair, build_ssh_command, build_ssh_command_string
from plato.cli.chronos.dev.sync import SyncManager
from plato.cli.chronos.env import resolve_config_env_vars, substitute_env_vars
from plato.cli.chronos.provision import (
    SyncTarget,
    build_sync_targets,
    build_world_process_env,
    provision_vm,
)
from plato.cli.chronos.registry import parse_package_string
from plato.cli.chronos.settings import get_settings
from plato.cli.chronos.test.config import TestConfig, TestPhaseConfig
from plato.otel import get_tracer, init_tracing, shutdown_tracing
from plato.runtimes.config import VMRuntimeConfig
from plato.utils.pypi_index import redact_pypi_token_credential
from plato.utils.subprocess import VM_PATH_EXPORT
from plato.v2 import AsyncPlato, Env
from plato.v2.async_.session import SerializedSession, Session
from plato.v2.types import SimConfigCompute

settings = get_settings()
logger = logging.getLogger(__name__)
console = Console()


class ReusableVM(BaseModel):
    """Persisted VM state for reuse across test runs."""

    job_id: str
    session: SerializedSession
    ssh_private_key: str
    ssh_public_key: str

    def save(self, path: Path) -> None:
        path.write_text(self.model_dump_json(indent=2) + "\n")
        path.chmod(0o600)

    @classmethod
    def load(cls, path: Path) -> ReusableVM:
        return cls.model_validate_json(path.read_text())


def _reuse_file_path(config_path: Path) -> Path:
    """Return the reuse file path derived from the config file name."""
    stem = config_path.stem
    return config_path.parent / f".chronos-test-vm-{stem}.json"


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
        keep_vm: bool = False,
        reuse_vm: bool = False,
        clean: bool = False,
        verbose: bool,
    ):
        self.config = config
        self.config_path = config_path
        self.api_key = api_key
        self.phase_filter = phase_filter
        self.pytest_args = (pytest_args or "").strip()
        self.keep_vm = keep_vm
        self.reuse_vm = reuse_vm
        self.clean = clean
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
        self._phase_process: asyncio.subprocess.Process | None = None

    def _print(self, msg: str) -> None:
        """Write to stdout with immediate flush — reliable in agent subprocess contexts."""
        sys.stdout.write(msg + "\n")
        sys.stdout.flush()

    def _should_keep_vm(self) -> bool:
        """Return whether this run should preserve the VM for reuse."""
        return self.world_env is not None and (self.keep_vm or self.reuse_vm)

    @staticmethod
    def _build_phase_remote_command(
        *,
        workdir: str,
        env_map: dict[str, str],
        phase_name: str,
        cmd: str,
    ) -> tuple[str, str]:
        """Wrap a phase command in its own remote process group and PID file."""
        pid_file = f"/tmp/plato-chronos-test-phase-{uuid.uuid4().hex}.pid"
        export_parts = [
            f"{VM_PATH_EXPORT};",
            *[f"export {key}={shlex.quote(value)};" for key, value in sorted(env_map.items())],
        ]
        phase_script = (
            f"echo $$ > {shlex.quote(pid_file)}; "
            f"trap 'rm -f {shlex.quote(pid_file)}' EXIT; "
            f"exec bash -lc {shlex.quote(cmd)}"
        )
        script = (
            "set -euo pipefail; "
            f"cd {shlex.quote(workdir)}; "
            + " ".join(export_parts)
            + f" echo {shlex.quote(f'>>> Running phase: {phase_name}')}; "
            + f"exec setsid bash -lc {shlex.quote(phase_script)}"
        )
        return f"bash -lc {shlex.quote(script)}", pid_file

    def _terminate_remote_phase(self, pid_file: str) -> None:
        """Terminate the currently running remote phase process group, if any.

        This method is intentionally synchronous so it can be called safely
        from a signal handler without needing asyncio.create_task (which
        only holds a weak reference and may be garbage-collected).
        """
        import subprocess

        if not self.world_env or not self.ssh_key:
            return

        stop_script = (
            f"if [ -f {shlex.quote(pid_file)} ]; then "
            f"kill -TERM -- -$(cat {shlex.quote(pid_file)}) 2>/dev/null || true; "
            "fi"
        )
        try:
            subprocess.run(
                build_ssh_command(self.world_env.job_id, self.ssh_key.private_key_path)
                + [f"bash -lc {shlex.quote(stop_script)}"],
                timeout=5,
                capture_output=True,
            )
        except Exception:
            logger.warning("Failed to terminate remote phase process", exc_info=True)

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
            if exit_code == 0:
                status = "completed"
            elif exit_code == 130:
                status = "cancelled"
            else:
                status = "failed"
            keep_vm = self._should_keep_vm()
            if self.session_id and status == "cancelled":
                await self._cancel_chronos_session(error_message or "Interrupted by user")
            elif self.session_id and not keep_vm:
                await self._complete_chronos_session(status, exit_code, error_message)
            elif self.session_id and keep_vm:
                logger.info("Skipping Chronos session completion because VM is being kept for reuse")

            self._write_summary(exit_code=exit_code, status=status, error_message=error_message)

            await self._cleanup(keep_vm=keep_vm)

            self._print(f"TEST_STATUS={status}")
            self._print(f"TEST_EXIT_CODE={exit_code}")
            if self.session_id:
                self._print(f"CHRONOS_SESSION_ID={self.session_id}")
                self._print(f"CHRONOS_URL={settings.chronos_url}/sessions/{self.session_id}")

            if keep_vm and self.world_env:
                self._print(f"VM kept alive for reuse: {self.world_env.job_id}")

            console.print(f"\n[dim]Artifacts:[/dim] {self.artifacts_dir}")

        return exit_code

    async def _setup_vm(self) -> None:
        if self.reuse_vm:
            await self._setup_vm_reuse()
            return

        world_package, world_version = parse_package_string(self.config.world.package)
        world_image = self.config.world.image
        if not world_image:
            async with httpx.AsyncClient(
                base_url=settings.chronos_url.rstrip("/"),
                timeout=30.0,
            ) as client:
                world_schema = await get_world_schema_api.asyncio(
                    client,
                    package_name=world_package,
                    version=world_version,
                    world_name=self.config.world.world_name,
                )
            world_image = world_schema.image or ""
            if not world_image:
                raise RuntimeError(f"No world image found in schema for {self.config.world.package}")
            self._print(f"[setup] Resolved world: {world_package}:{world_schema.version} (image={world_image})")
            # Use the registered world name from the schema if not explicitly set
            if not self.config.world.world_name:
                self.config = self.config.model_copy(
                    update={
                        "world": self.config.world.model_copy(
                            update={"world_name": world_schema.name or world_schema.resolved_world_name}
                        )
                    }
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
                        "api_key": self.api_key,
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
            timeout=world_runtime.vm.timeout,
        )
        await self.session.start_heartbeat()

        # Link the Plato session to the Chronos session so the environments
        # tab is populated in the UI.
        await self._link_plato_session(self.session.session_id)

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

        await self._resolve_and_write_config()
        self._print("[setup] VM ready for tests")

    async def _setup_vm_reuse(self) -> None:
        """Reuse an existing VM: restore session, rsync code, skip editable install."""
        reuse_path = _reuse_file_path(self.config_path)
        if not reuse_path.exists():
            raise RuntimeError(f"No reuse file found at {reuse_path}. Run with --keep-vm first to create one.")

        self._print(f"[reuse] Loading VM state from {reuse_path}")
        vm_state = ReusableVM.load(reuse_path)

        world_package, _ = parse_package_string(self.config.world.package)

        # Resolve world_name from schema if needed
        if not self.config.world.world_name:
            _, world_version = parse_package_string(self.config.world.package)
            async with httpx.AsyncClient(
                base_url=settings.chronos_url.rstrip("/"),
                timeout=30.0,
            ) as client:
                world_schema = await get_world_schema_api.asyncio(
                    client,
                    package_name=world_package,
                    version=world_version,
                )
            self.config = self.config.model_copy(
                update={
                    "world": self.config.world.model_copy(
                        update={"world_name": world_schema.name or world_schema.resolved_world_name}
                    )
                }
            )

        # Create a fresh Chronos session for telemetry
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
                        "api_key": self.api_key,
                    }
                )
            }
        )

        try:
            init_tracing(
                service_name=f"chronos-test.{world_package}",
                session_id=self.session_id,
                otlp_endpoint=otel_url,
            )
            self._tracing_initialized = True
        except Exception:  # noqa: BLE001
            logger.warning("Failed to initialize OTel tracing", exc_info=True)

        # Restore the Plato session from serialized state, using the current API key
        # in case credentials have rotated since the reuse file was saved.
        self._print(f"[reuse] Reconnecting to VM {vm_state.job_id}...")
        self.plato = AsyncPlato()
        session_data = vm_state.session.model_copy(update={"api_key": self.api_key})
        self.session = await Session.load(session_data, start_heartbeat=True)

        # Restore SSH key from saved content
        key_dir = Path(tempfile.mkdtemp(prefix="plato_ssh_reuse_"))
        private_key_path = key_dir / "id_ed25519"
        public_key_path = key_dir / "id_ed25519.pub"
        private_key_path.write_text(vm_state.ssh_private_key)
        private_key_path.chmod(0o600)
        public_key_path.write_text(vm_state.ssh_public_key)
        public_key_path.chmod(0o644)
        self.ssh_key = SSHKeyPair(private_key_path=private_key_path, public_key=vm_state.ssh_public_key)

        # Verify SSH connectivity before committing to this VM
        from plato.cli.chronos.dev.ssh import wait_for_ssh_reachable

        reachable = await wait_for_ssh_reachable(vm_state.job_id, private_key_path, retries=3, delay=2.0)
        if not reachable:
            reuse_path.unlink(missing_ok=True)
            raise RuntimeError(
                f"VM {vm_state.job_id} is no longer reachable. "
                f"Removed stale reuse file. Run without --reuse-vm to provision a new VM."
            )

        # VM confirmed reachable — safe to assign world_env (controls reuse file saving)
        self.world_env = self.session.envs[0]
        await self._link_plato_session(self.session.session_id)
        self._print("[reuse] SSH connected")

        if self.clean:
            await self._clean_vm_state()

        # Rsync code to the existing VM (skip editable install)
        sync_targets = self._build_sync_targets()
        self.sync_manager = SyncManager(self.ssh_key.private_key_path, verbose=self.verbose)
        for target in sync_targets:
            self.sync_manager.add_target(
                local_path=target.local_path,
                remote_path=target.remote_path,
                job_id=vm_state.job_id,
            )

        synced = await self.sync_manager.initial_sync()
        if synced != len(self.sync_manager.targets):
            failed = len(self.sync_manager.targets) - synced
            raise RuntimeError(f"Sync failed for {failed} target(s)")
        self._print("[reuse] Code synced (skipped editable install)")

        await self._sync_world_deps()
        await self._resolve_and_write_config()
        self._print("[reuse] VM ready for tests")

    async def _clean_vm_state(self) -> None:
        """Fast-clean workspace and cache dirs on the VM using mv + background rm."""
        if not self.world_env:
            raise RuntimeError("world_env must be initialized")

        # mv is instant (inode rename), rm runs in background
        clean_script = (
            "set -e; "
            "for d in /state /tmp/plato-*; do "
            '  [ -e "$d" ] && mv "$d" "${d}.cleanup.$$" && mkdir -p "$d"; '
            "done; "
            "rm -rf /state.cleanup.* /tmp/plato-*.cleanup.* &"
        )
        result = await self.world_env.execute(clean_script, timeout=30)
        if result.exit_code != 0:
            raise RuntimeError(f"VM clean failed (exit {result.exit_code}): {result.stderr}")
        self._print("[reuse] Cleaned workspace state")

    async def _resolve_and_write_config(self) -> None:
        """Resolve ${VAR} placeholders in world config and write runtime files to the VM."""
        world_config = self.config.world.config or {}
        await resolve_config_env_vars(world_config, self.api_key)
        pass_env_values = {name: val for name in self.config.test.pass_env if (val := os.environ.get(name))}
        if pass_env_values:
            substituted = substitute_env_vars(world_config, pass_env_values)
            if isinstance(substituted, dict):
                world_config.clear()
                world_config.update(substituted)
        await resolve_agent_images(world_config, self.api_key)
        await self._write_runtime_files()

    def _build_sync_targets(self) -> list[SyncTarget]:
        """Build the list of sync targets from config."""
        targets = build_sync_targets(self.config.dev, self.config_path.parent)
        if not targets:
            raise RuntimeError("No sync targets configured. Provide `dev.world` and/or `dev.agents`.")
        return targets

    async def _install_editable_packages(self) -> None:
        if not self.world_env:
            raise RuntimeError("world_env must be initialized")

        self._print("[setup] Installing packages...")
        logger.info("Installing editable packages on VM...")

        t0 = perf_counter()
        await self.world_env.execute(ENSURE_FUSE3_COMMAND, timeout=60)
        logger.info("fuse3 check: %.1fs", perf_counter() - t0)

        # Clean build artifacts so editable install uses fresh source
        if self.config.dev.world:
            await self.world_env.execute(CLEAN_WORLD_BUILD_ARTIFACTS_COMMAND, timeout=20)

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
            world_pkgs = await self.world_env.execute(DISCOVER_WORLD_PACKAGES_COMMAND, timeout=30)
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
                f"uv pip uninstall --python /opt/plato-venv/bin/python {' '.join(uninstall_pkgs)}",
                timeout=90,
            )
            logger.info("Uninstalled %s: %.1fs", " ".join(uninstall_pkgs), perf_counter() - t0)

        # Strip "-e " prefix to get bare paths for build_editable_install_commands
        paths = [e.removeprefix("-e ") for e in editables]
        install_cmds = build_editable_install_commands(paths)
        t0 = perf_counter()
        for cmd in install_cmds:
            logger.info("Installing: %s", redact_pypi_token_credential(cmd))
            result = await self.world_env.execute(cmd, timeout=120)
            if result.exit_code != 0:
                raise RuntimeError(f"Editable install failed: {result.stderr}")
        logger.info("Editable install complete: %.1fs", perf_counter() - t0)

        await self._sync_world_deps()

    async def _sync_world_deps(self) -> None:
        """Install world deps missing from the pre-baked venv.

        Editable installs are --no-deps, so a dep added to the synced world's
        pyproject.toml after its image was baked must be installed here
        (no-op when already satisfied).
        """
        if not self.config.dev.world:
            return
        if not self.world_env:
            raise RuntimeError("world_env must be initialized")
        t0 = perf_counter()
        result = await self.world_env.execute(build_world_deps_sync_command(), timeout=300)
        if result.exit_code != 0:
            raise RuntimeError(f"World dependency sync failed: {result.stderr}")
        logger.info("World deps sync: %.1fs", perf_counter() - t0)

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

        # Core env (PLATO_API_KEY, JOB_ID) is applied after merging test.env so
        # it cannot be accidentally overridden — JOB_ID in particular controls
        # mesh-IP SSH to agent VMs (see build_world_process_env).
        env_map = {
            **self.config.test.env,
            **build_world_process_env(self.api_key, self.world_env.job_id),
        }
        # Tell the world runner not to call /complete — the test runner
        # handles session completion after collecting artifacts.  The
        # Chronos /complete endpoint closes the Plato session (killing
        # the VM), so calling it from within the VM is fatal.
        env_map["PLATO_WORLD_TEST_MODE"] = "1"

        for env_name in self.config.test.pass_env:
            value = os.environ.get(env_name)
            if value:
                env_map[env_name] = value

        remote_cmd, pid_file = self._build_phase_remote_command(
            workdir=self.config.test.workdir,
            env_map=env_map,
            phase_name=phase_name,
            cmd=cmd,
        )
        ssh_cmd = build_ssh_command(self.world_env.job_id, self.ssh_key.private_key_path)
        ssh_cmd.append(remote_cmd)

        self._phase_process = await asyncio.create_subprocess_exec(
            *ssh_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        proc = self._phase_process

        original_handler = signal.getsignal(signal.SIGINT)
        sigint_count = 0

        def sigint_handler(signum: int, frame: object) -> None:
            nonlocal sigint_count
            sigint_count += 1
            if sigint_count == 1:
                console.print("\n[yellow]Stopping phase (graceful)...[/yellow] [dim](Ctrl+C again to force)[/dim]")
                self._terminate_remote_phase(pid_file)
            else:
                console.print("\n[red]Force killing local SSH...[/red]")
                if proc:
                    proc.kill()

        signal.signal(signal.SIGINT, sigint_handler)

        output_lines: list[str] = []
        interrupted = False
        try:
            stdout = proc.stdout
            if stdout:
                while True:
                    line = await stdout.readline()
                    if not line:
                        break
                    decoded = line.decode(errors="replace")
                    output_lines.append(decoded)
                    sys.stdout.write(decoded)
                    sys.stdout.flush()

            await proc.wait()
            interrupted = sigint_count > 0
        finally:
            signal.signal(signal.SIGINT, original_handler)
            self._phase_process = None
            log_path.write_text("".join(output_lines), encoding="utf-8")

        if interrupted:
            return 130
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
        """Write content to a file on the VM using chunked base64 to avoid ARG_MAX limits."""
        if not self.world_env:
            raise RuntimeError("world_env must be initialized")
        b64 = base64.b64encode(content.encode()).decode()
        q_path = shlex.quote(remote_path)
        prefix = f"mkdir -p $(dirname {q_path}) && " if mkdir else ""

        if not b64:
            result = await self.world_env.execute(f"{prefix}: > {q_path}", timeout=30)
            if result.exit_code != 0:
                raise RuntimeError(f"Failed to write {remote_path}: {result.stderr}")
            return

        q_tmp = shlex.quote(f"{remote_path}.b64tmp")
        chunk_size = 65536
        chunks = [b64[i : i + chunk_size] for i in range(0, len(b64), chunk_size)]

        result = await self.world_env.execute(
            f"{prefix}printf '%s' '{chunks[0]}' > {q_tmp}",
            timeout=30,
        )
        if result.exit_code != 0:
            raise RuntimeError(f"Failed to write {remote_path}: {result.stderr}")

        for chunk in chunks[1:]:
            result = await self.world_env.execute(
                f"printf '%s' '{chunk}' >> {q_tmp}",
                timeout=30,
            )
            if result.exit_code != 0:
                raise RuntimeError(f"Failed to write {remote_path}: {result.stderr}")

        result = await self.world_env.execute(
            f"base64 -d < {q_tmp} > {q_path} && rm -f {q_tmp}",
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
            }
        )
        serialized_session = self.session.dump()
        runtime_hostname = self.world_env.mesh_ip or await self.world_env.get_mesh_ip() or self.world_env.job_id
        if runtime_hostname == self.world_env.job_id:
            logger.warning(
                "Falling back to world job_id for runtime hostname because no mesh_ip was available: %s",
                self.world_env.job_id,
            )

        config_dict = self.config.model_dump(mode="json")
        # Inject serialized Plato session into runtime_info for the world runner
        if serialized_session:
            config_dict.setdefault("world", {})["runtime_info"] = {
                "runtime_id": self.world_env.job_id,
                "hostname": runtime_hostname,
                "ssh_key_path": "/root/.ssh/agent_key",
                "serialized_session": serialized_session.model_dump(mode="json")
                if hasattr(serialized_session, "model_dump")
                else serialized_session,
                "metadata": {
                    "kind": "vm",
                    "job_id": self.world_env.job_id,
                    "hostname": runtime_hostname,
                },
            }
        config_json = json.dumps(config_dict)
        await self._write_file_to_vm("/tmp/config.json", config_json)

        if serialized_session:
            session_json = json.dumps(
                serialized_session.model_dump(mode="json")
                if hasattr(serialized_session, "model_dump")
                else serialized_session
            )
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

    async def _link_plato_session(self, plato_session_id: str) -> None:
        """Link the Plato session to the Chronos session so envs tab is populated."""
        if not self.session_id:
            return

        body = LinkPlatoSessionRequest(plato_session_id=plato_session_id)
        try:
            async with httpx.AsyncClient(
                base_url=settings.chronos_url.rstrip("/"),
                timeout=30.0,
            ) as client:
                await link_plato_session.asyncio(
                    client,
                    public_id=self.session_id,
                    body=body,
                    x_api_key=self.api_key,
                )
        except Exception:  # noqa: BLE001
            logger.warning("Failed to link Plato session to Chronos", exc_info=True)

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

    async def _cancel_chronos_session(self, reason: str) -> None:
        """Mark the Chronos session as cancelled without closing the Plato VM session."""
        if not self.session_id:
            return

        body = UpdateStatusRequest(status="cancelled", status_reason=reason[:500])
        try:
            async with httpx.AsyncClient(
                base_url=settings.chronos_url.rstrip("/"),
                timeout=30.0,
            ) as client:
                await update_session_status.asyncio(
                    client,
                    public_id=self.session_id,
                    body=body,
                    x_api_key=self.api_key,
                )
        except Exception:  # noqa: BLE001
            logger.warning("Failed to cancel Chronos session", exc_info=True)

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

    def _save_reuse_file(self) -> None:
        """Save VM state to a reuse file for subsequent --reuse-vm runs."""
        if not self.session or not self.ssh_key or not self.world_env:
            logger.warning("Cannot save reuse file: session/SSH key/env not initialized")
            return

        try:
            reuse_path = _reuse_file_path(self.config_path)
            vm_state = ReusableVM(
                job_id=self.world_env.job_id,
                session=self.session.dump(),
                ssh_private_key=self.ssh_key.private_key_path.read_text(),
                ssh_public_key=self.ssh_key.public_key,
            )
            vm_state.save(reuse_path)
            self._print(f"[reuse] VM state saved to {reuse_path}")
            self._print(f"[reuse] Reuse with: plato chronos test {self.config_path} --reuse-vm")
        except Exception:  # noqa: BLE001
            logger.warning("Failed to save reuse file", exc_info=True)

    async def _cleanup(self, *, keep_vm: bool) -> None:
        if self._tracing_initialized:
            shutdown_tracing()

        if self.sync_manager:
            self.sync_manager.stop()

        if keep_vm:
            self._save_reuse_file()
            return

        logger.info("Cleaning up session and VM...")
        if self.session and not self.reuse_vm:
            # Don't close the underlying Plato session when reusing — we didn't create it
            await self.session.close()
            logger.info("Session closed: %s", self.session_id)
        if self.plato:
            await self.plato.close()
        logger.info("Cleanup complete.")


TestRunner.__test__ = False

__all__ = ["TestRunner", "select_test_phases"]
