"""Dev mode runner - orchestrates VM creation, sync, and execution."""

from __future__ import annotations

import asyncio
import base64
import contextlib
import json
import logging
import os
import shlex
import signal
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

import httpx
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from plato.agents.install import (
    CLEAN_WORLD_BUILD_ARTIFACTS_COMMAND,
    DISCOVER_WORLD_PACKAGES_COMMAND,
    ENSURE_FUSE3_COMMAND,
    build_editable_install_commands,
    build_world_deps_sync_command,
)
from plato.chronos.api.registry import (
    get_agent_schema_api_registry_agents__agent_name__schema_get as get_agent_schema_api,
)
from plato.chronos.api.registry import (
    get_world_schema_api_registry_worlds__package_name__schema_get as get_world_schema_api,
)
from plato.chronos.api.sessions import complete_session, create_session, link_plato_session
from plato.chronos.models import (
    CompleteSessionRequest,
    CreateSessionRequest,
    CreateSessionResponse,
    LinkPlatoSessionRequest,
    RegistryAgentSchemaResponse,
    Status1,
)
from plato.cli.chronos.config import Config
from plato.cli.chronos.dev.ecr import ensure_image_exists
from plato.cli.chronos.dev.profiling import StartupProfiler
from plato.cli.chronos.dev.ssh import SSHKeyPair, build_ssh_command
from plato.cli.chronos.dev.sync import SyncManager
from plato.cli.chronos.env import resolve_config_env_vars
from plato.cli.chronos.provision import build_sync_targets, build_world_process_env, provision_vm
from plato.cli.chronos.registry import parse_package_string
from plato.cli.chronos.settings import get_settings

if TYPE_CHECKING:
    from plato.v2 import AsyncPlato
    from plato.v2.environment import Environment
    from plato.v2.session import SerializedSession, Session

settings = get_settings()
logger = logging.getLogger(__name__)
console = Console()

# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------


def _step(msg: str) -> None:
    """Print a completed step with a checkmark."""
    console.print(f"  [green]✓[/green] {msg}")


def _info(msg: str) -> None:
    """Print an info line."""
    console.print(f"  [dim]→[/dim] {msg}")


def _warn(msg: str) -> None:
    """Print a warning."""
    console.print(f"  [yellow]![/yellow] {msg}")


def _error(msg: str) -> None:
    """Print an error."""
    console.print(f"  [red]✗[/red] {msg}")


def _link(label: str, url: str) -> None:
    """Print a labeled link."""
    console.print(f"  [dim]{label}:[/dim] [blue]{url}[/blue]", soft_wrap=True)


# ---------------------------------------------------------------------------
# Registry helper
# ---------------------------------------------------------------------------


def find_agent_configs(config: dict, prefix: str = "") -> dict[str, dict]:
    """Recursively find agent-like dicts (with 'package' or 'image' key) in config."""
    agents: dict[str, dict] = {}
    for key, value in config.items():
        if not isinstance(value, dict):
            continue
        path = f"{prefix}.{key}" if prefix else key
        if "package" in value or "image" in value:
            agents[path] = value
        else:
            agents.update(find_agent_configs(value, path))
    return agents


async def resolve_agent_images(config: dict, api_key: str | None = None) -> None:
    """Resolve package → image for all agent configs in a world config dict.

    Mutates agent dicts in-place, setting ``image`` from the registry and
    normalizing ``package`` to ``name:resolved_version`` for downstream VM setup.
    """
    agents = find_agent_configs(config)
    for name, agent in agents.items():
        package_ref = agent.get("package")
        if not package_ref:
            continue

        package_name, package_version = parse_package_string(package_ref)
        # The ``version`` field in the agent config overrides the version
        # embedded in the package string.  Normalise it the same way
        # ``parse_package_string`` does (empty / "latest" → None).
        explicit_version = agent.get("version")
        if explicit_version is not None:
            _, explicit_version = parse_package_string(f"_:{explicit_version}")
        version = explicit_version or package_version
        image = agent.get("image")

        if not image or version is None:
            schema = await _fetch_agent_schema_from_registry(package_name, version, api_key)
            if not schema or not schema.image:
                raise ValueError(
                    f"Could not resolve image for agent '{name}' (package={package_name}, version={version or 'latest'})"
                )
            image = schema.image
            version = schema.version
            agent["image"] = image

        if version is None:
            raise ValueError(
                f"Could not resolve version for agent '{name}' (package={package_name}, image={image or 'unknown'})"
            )

        agent["package"] = f"{package_name}:{version}"
        if "version" in agent:
            agent["version"] = version
        logger.info("Resolved agent '%s': %s -> %s", name, agent["package"], image)


async def _fetch_agent_schema_from_registry(
    package: str, version: str | None = None, api_key: str | None = None
) -> RegistryAgentSchemaResponse | None:
    """Fetch agent schema from the Chronos registry API."""
    try:
        async with httpx.AsyncClient(
            base_url=settings.chronos_url.rstrip("/"),
            timeout=30.0,
            headers={"X-API-Key": api_key} if api_key else {},
        ) as client:
            return await get_agent_schema_api.asyncio(client, agent_name=package, version=version)
    except Exception as e:
        logger.warning(f"Could not fetch agent schema from registry: {e}")
    return None


class DevRunner:
    """Orchestrates dev mode execution."""

    def __init__(
        self,
        config: Config,
        config_path: Path,
        api_key: str | None = None,
        verbose: bool = False,
        memray: bool = False,
        startup_profile_out: Path | None = None,
    ):
        self.config = config
        self.config_path = config_path
        self.api_key: str = api_key or os.environ.get("PLATO_API_KEY") or ""
        self.verbose = verbose
        self.memray = memray
        self.startup_profile_out = startup_profile_out

        if not self.api_key:
            raise ValueError("PLATO_API_KEY environment variable is required")

        self.plato: AsyncPlato | None = None
        self.session: Session | None = None
        self.sync_manager: SyncManager | None = None
        self.ssh_key: SSHKeyPair | None = None
        self.world_env: Environment | None = None
        self.world_image: str = ""  # Fetched from registry
        self._world_process: asyncio.subprocess.Process | None = None
        self._sigint_count = 0
        self._graceful_requested = False
        self._force_killed = False
        self._shutdown_requested = False
        self._force_fresh_next_run = False
        self._serialized_session: SerializedSession | None = None
        self._startup_profiler = StartupProfiler(metadata={"config_path": str(config_path)})

    def _forwarded_debug_env_assignments(self) -> str:
        parts: list[str] = []
        for key in ("PLATO_FUSE_DEBUG", "PLATO_SMART_COMMIT_DEBUG", "RUST_LOG"):
            value = os.environ.get(key)
            if value:
                parts.append(f"{key}={shlex.quote(value)}")
        return " ".join(parts)

    async def run(self) -> None:
        """Run the dev workflow."""
        from plato.runtimes.config import VMRuntimeConfig
        from plato.v2 import AsyncPlato, Env
        from plato.v2.types import SimConfigCompute

        if not self.config.world.package:
            raise ValueError("world.package is required")

        # Parse package:version format
        world_package, world_version = parse_package_string(self.config.world.package)

        total_start = time.time()

        console.print()
        console.print(f"  [bold]plato chronos dev[/bold] [dim]—[/dim] {world_package}")
        console.print()

        self.plato = AsyncPlato()

        try:
            with self._startup_profiler.time("setup.total"):
                # 1 + 2. Fetch world schema and create Chronos session in parallel
                with self._startup_profiler.time("setup.images_and_session"):
                    with console.status("  Fetching world schema & creating session...", spinner="dots") as status:

                        async def _fetch_schema():
                            with self._startup_profiler.time("setup.images.fetch_world_schema"):
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
                            self.world_image = world_schema.image or ""
                            if not self.world_image:
                                raise ValueError(f"No image found in schema for {world_package}")
                            logger.info(
                                f"Resolved world: {world_package}:{world_schema.version} (image={self.world_image})"
                            )
                            status.update("  Verifying images...")
                            with self._startup_profiler.time("setup.images.ensure_ecr"):
                                await self._ensure_images()

                        async def _create_session():
                            with self._startup_profiler.time("setup.session.create"):
                                return await self._create_chronos_session()

                        _, chronos_session = await asyncio.gather(
                            _fetch_schema(),
                            _create_session(),
                        )
                        with self._startup_profiler.time("setup.session.s3_credentials"):
                            s3_config = self._generate_s3_config(session_id=chronos_session.public_id)
                        self.config = self.config.model_copy(
                            update={
                                "session": self.config.session.model_copy(
                                    update={
                                        "session_id": chronos_session.public_id,
                                        "otel_url": chronos_session.otel_url or f"{settings.chronos_url}/api/otel",
                                        # The launch backend fills these when it
                                        # builds the VM config; dev must too, or
                                        # the world's Chronos calls (workspace
                                        # repo resolve, checkpoints) go out with
                                        # an empty X-API-Key and 401.
                                        "chronos_url": settings.chronos_url,
                                        "api_key": self.api_key,
                                        "s3": s3_config,
                                    }
                                )
                            }
                        )
                _step("Images resolved")
                _step(f"Session [bold]{self.config.session.session_id}[/bold]")
                _link("Chronos", f"{settings.chronos_url}/sessions/{self.config.session.session_id}")

                # 3. Create World VM
                world_runtime = self.config.world.runtime
                if world_runtime.type != "vm":
                    raise ValueError("World must use VM runtime in dev mode")
                if not isinstance(world_runtime, VMRuntimeConfig):
                    raise ValueError("World must use VM runtime config")

                # 3. Create VM + provision (network, SSH, gateway probe)
                with self._startup_profiler.time("setup.vm.create"):
                    with console.status("  Creating VM...", spinner="dots") as status:
                        env = Env.resource(
                            simulator=f"dev-{world_package}",
                            sim_config=SimConfigCompute(
                                cpus=world_runtime.vm.cpus,
                                memory=world_runtime.vm.memory,
                                disk=world_runtime.vm.disk,
                            ),
                            alias="runtime",
                            docker_image_url=self.world_image,
                            upload_rootfs=False,
                            rootfs_storage_backend="snapshot-store",
                        )
                        self.session = await self.plato.sessions.create(
                            envs=[env],
                            timeout=world_runtime.vm.timeout,
                        )
                        if not self.session:
                            raise RuntimeError("Failed to create session")
                        status.update("  Starting heartbeat...")
                        await self.session.start_heartbeat()
                        await self._link_plato_session(self.session.session_id)
                _step(f"Session [bold]{self.session.session_id}[/bold]")

                # 4. Provision: connect network → SSH → gateway probe
                with self._startup_profiler.time("setup.provision"):
                    with console.status("  Provisioning VM...", spinner="dots"):
                        result = await provision_vm(
                            session=self.session,
                            copy_ssh_key_to_vm=True,
                            ensure_rsync=True,
                            verbose=self.verbose,
                        )
                        self.world_env = result.env
                        self.ssh_key = result.ssh_key
                        self.config = self.config.model_copy(
                            update={
                                "dev": self.config.dev.model_copy(
                                    update={"ssh_key_path": Path("/root/.ssh/agent_key")}
                                ),
                            }
                        )
                        self._serialized_session = self.session.dump()
                _step(f"VM [bold]{self.world_env.job_id}[/bold] provisioned")

                # 5. Sync code
                with self._startup_profiler.time("setup.sync.total"):
                    with console.status("  Syncing code...", spinner="dots") as status:
                        self.sync_manager = SyncManager(self.ssh_key.private_key_path, verbose=self.verbose)
                        sync_manager = self.sync_manager
                        await self._setup_sync_targets()
                        _synced: list[str] = []

                        def _target_metric_key(remote_path: str) -> str:
                            if remote_path == "/world":
                                return "world"
                            if remote_path == "/sdk":
                                return "sdk"
                            if remote_path.startswith("/agents/"):
                                return f"agent.{remote_path.removeprefix('/agents/')}"
                            return remote_path.strip("/").replace("/", ".") or "unknown"

                        def _on_synced(target, elapsed: float):
                            _synced.append(target.local_path.name)
                            metric_name = f"setup.sync.target.{_target_metric_key(target.remote_path)}"
                            self._startup_profiler.record(metric_name, elapsed)
                            remaining = [
                                t.local_path.name for t in sync_manager.targets if t.local_path.name not in _synced
                            ]
                            if remaining:
                                status.update(f"  Syncing {', '.join(remaining)}...")

                        await sync_manager.initial_sync(on_synced=_on_synced)
                _step(f"Code synced ({len(sync_manager.targets)} targets)")

                # 6. Install packages, ECR auth, VS Code Server, write config (parallel)
                with self._startup_profiler.time("setup.environment.total"):
                    with console.status("  Writing config...", spinner="dots") as status:
                        # Track sub-task completion for status updates
                        _env_done: set[str] = set()

                        def _env_status() -> str:
                            remaining = {"packages", "ecr", "vscode", "config"} - _env_done
                            if not remaining:
                                return "  Finalizing..."
                            labels = {
                                "packages": "packages",
                                "ecr": "ECR auth",
                                "vscode": "VS Code",
                                "config": "config",
                            }
                            parts = [labels[r] for r in ("packages", "ecr", "vscode", "config") if r in remaining]
                            return f"  Waiting on {', '.join(parts)}..."

                        async def _track(name: str, metric_name: str, coro):
                            with self._startup_profiler.time(metric_name):
                                result = await coro
                            _env_done.add(name)
                            status.update(_env_status())
                            return result

                        status.update(_env_status())
                        results = await asyncio.gather(
                            _track("packages", "setup.env.packages", self._install_packages()),
                            _track("ecr", "setup.env.ecr_auth", self._setup_ecr_auth()),
                            _track("vscode", "setup.env.vscode", self._setup_vscode_server()),
                            _track("config", "setup.env.config_write", self._write_config()),
                            return_exceptions=True,
                        )
                        labels = ["Package install", "ECR auth", "VS Code", "Config write"]
                        errors = [(labels[i], r) for i, r in enumerate(results) if isinstance(r, Exception)]
                # VS Code is a convenience — a slow/failed code-server must not
                # kill the session (worlds like webclone human-review start
                # their own anyway). Warn and continue.
                vscode_errors = [(label, err) for label, err in errors if label == "VS Code"]
                errors = [(label, err) for label, err in errors if label != "VS Code"]
                for label, err in vscode_errors:
                    console.print(f"  [yellow]⚠ {label} setup failed (continuing without IDE): {err}[/yellow]")
                if errors:
                    for label, err in errors:
                        _error(f"{label} failed: {err}")
                    raise RuntimeError("Environment setup failed")
                _step("Environment ready")

            setup_time = self._startup_profiler.durations().get("setup.total", time.time() - total_start)
            console.print()

            # Print connection info
            vscode_url = f"https://{self.world_env.job_id}--8080.sims.plato.so"
            ssh_cmd = f"plato sandbox ssh -J {self.world_env.job_id}"
            info_lines = Text()
            info_lines.append("  SSH     ", style="dim")
            info_lines.append(ssh_cmd, style="bold")
            info_lines.append("\n  VS Code ", style="dim")
            info_lines.append(vscode_url, style="blue")
            info_lines.append("\n  Setup   ", style="dim")
            info_lines.append(f"{setup_time:.1f}s", style="green")
            console.print(Panel(info_lines, border_style="dim", padding=(0, 1)))
            console.print()
            self._print_startup_profile()
            self._write_startup_profile_json()

            # 7. Run with hot reload
            await self._run_with_hot_reload()

        except asyncio.CancelledError:
            pass
        except KeyboardInterrupt:
            pass
        except Exception as e:
            _error(str(e))
            if self.config.session.session_id:
                await self._complete_chronos_session("failed", 1, str(e)[:500])
            raise
        else:
            if self.config.session.session_id:
                await self._complete_chronos_session("completed", 0)
        finally:
            await self._cleanup()

    def _generate_s3_config(self, session_id: str) -> dict:
        """Generate STS credentials for S3 artifact uploads."""
        try:
            from plato.utils.ecr import _clean_aws_env

            result = subprocess.run(
                ["aws", "sts", "get-session-token", "--duration-seconds", "43200", "--output", "json"],
                capture_output=True,
                text=True,
                env=_clean_aws_env(),
            )
            if result.returncode != 0:
                logger.warning(f"Failed to generate STS credentials: {result.stderr}")
                return {}
            creds = json.loads(result.stdout)["Credentials"]
            return {
                "bucket": "plato-browser-session-data-prod",
                "region": "us-west-1",
                "prefix": f"sessions/{session_id}/artifacts",
                "aws_access_key_id": creds["AccessKeyId"],
                "aws_secret_access_key": creds["SecretAccessKey"],
                "aws_session_token": creds["SessionToken"],
            }
        except Exception as e:
            logger.warning(f"Failed to generate STS credentials: {e}")
            return {}

    def _get_agent_fields(self) -> dict[str, dict]:
        """Get agent fields from world config."""
        world_config = self.config.world.config or {}
        agent_names = set(self.config.dev.agents.keys())
        return {
            name: world_config[name]
            for name in agent_names
            if name in world_config and isinstance(world_config[name], dict)
        }

    async def _ensure_images(self) -> None:
        """Ensure images exist in ECR."""
        images: list[tuple[str, str]] = [("World", self.world_image)]

        all_agents = self._get_agent_fields()
        world_config = self.config.world.config or {}
        all_agents.update(find_agent_configs(world_config))

        await resolve_agent_images(world_config, self.api_key)

        for name, agent in all_agents.items():
            image = agent.get("image")
            if image:
                images.append((f"Agent ({name})", image))

        for label, image in images:
            await ensure_image_exists(image)

    async def _create_chronos_session(self) -> CreateSessionResponse:
        """Create a session in Chronos for OTel traces."""
        import httpx

        world_config = self.config.world.config or {}
        tags = list({*self.config.tags, "dev"})
        body = CreateSessionRequest(
            world_name=self.config.world.package or "",
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
        chronos_session_id = self.config.session.session_id
        if not chronos_session_id:
            return

        body = LinkPlatoSessionRequest(plato_session_id=plato_session_id)
        try:
            async with httpx.AsyncClient(
                base_url=settings.chronos_url.rstrip("/"),
                timeout=30.0,
            ) as client:
                await link_plato_session.asyncio(
                    client,
                    public_id=chronos_session_id,
                    body=body,
                    x_api_key=self.api_key,
                )
        except Exception:  # noqa: BLE001
            logger.warning("Failed to link Plato session to Chronos", exc_info=True)

    async def _complete_chronos_session(
        self,
        status: str,
        exit_code: int,
        error_message: str | None = None,
    ) -> None:
        """Mark Chronos session as complete."""
        import httpx

        try:
            body = CompleteSessionRequest(
                status=Status1(status),
                exit_code=exit_code,
                error_message=error_message,
            )
            async with httpx.AsyncClient(
                base_url=settings.chronos_url.rstrip("/"),
                timeout=30.0,
            ) as client:
                await complete_session.asyncio(
                    client, public_id=self.config.session.session_id, body=body, x_api_key=self.api_key
                )
        except Exception:
            pass

    async def _setup_sync_targets(self) -> None:
        """Setup sync targets for world and agents."""
        if not self.sync_manager or not self.world_env:
            raise RuntimeError("sync_manager and world_env must be initialized")

        for target in build_sync_targets(self.config.dev, self.config_path.parent):
            self.sync_manager.add_target(
                local_path=target.local_path,
                remote_path=target.remote_path,
                job_id=self.world_env.job_id,
            )

    async def _install_packages(self) -> None:
        """Install packages in editable mode."""
        if not self.world_env:
            raise RuntimeError("world_env must be initialized")

        # Ensure fuse3 userspace tools are present for the Rust plato-fuse binary.
        with self._startup_profiler.time("setup.env.packages.system_deps"):
            await self.world_env.execute(ENSURE_FUSE3_COMMAND, timeout=60)

        # Sync local plato-fuse binary to VM if PLATO_FUSE_BINARY is set.
        fuse_binary = os.environ.get("PLATO_FUSE_BINARY")
        if fuse_binary and Path(fuse_binary).is_file():
            if not self.sync_manager:
                raise RuntimeError("sync_manager must be initialized")
            sync_manager = self.sync_manager
            with self._startup_profiler.time("setup.env.packages.sync_fuse_binary"):
                console.print(f"  [dim]Syncing local plato-fuse binary: {fuse_binary}[/dim]")
                from plato.cli.chronos.dev.ssh import build_ssh_command_string

                ssh_cmd = build_ssh_command_string(self.world_env.job_id, sync_manager.ssh_key_path)
                proc = await asyncio.create_subprocess_exec(
                    "rsync",
                    "-az",
                    "-e",
                    ssh_cmd,
                    fuse_binary,
                    f"root@{self.world_env.job_id}.plato:/usr/local/bin/plato-fuse",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                _, stderr = await proc.communicate()
                if proc.returncode != 0:
                    raise RuntimeError(f"Failed to sync plato-fuse binary: {stderr.decode().strip()}")
                await self.world_env.execute("chmod +x /usr/local/bin/plato-fuse", timeout=10)
                console.print("  [dim]plato-fuse binary synced to VM[/dim]")

        # Uninstall existing world package from Docker image
        if self.config.dev.world:
            with self._startup_profiler.time("setup.env.packages.uninstall_world"):
                result = await self.world_env.execute(DISCOVER_WORLD_PACKAGES_COMMAND, timeout=30)
                if result.stdout.strip():
                    pkgs = result.stdout.strip()
                    await self.world_env.execute(f"uv pip uninstall --system {pkgs}", timeout=60)

        # Uninstall existing SDK so editable install properly overrides it
        if self.config.dev.sync_sdk:
            with self._startup_profiler.time("setup.env.packages.uninstall_sdk"):
                await self.world_env.execute("uv pip uninstall --system plato-sdk-v2", timeout=60)

        editable_paths = []
        if self.config.dev.sync_sdk:
            editable_paths.append("/sdk")
        if self.config.dev.world:
            with self._startup_profiler.time("setup.env.packages.prepare_world"):
                await self.world_env.execute(CLEAN_WORLD_BUILD_ARTIFACTS_COMMAND, timeout=10)
            editable_paths.append("/world")

        if not editable_paths:
            return

        install_cmds = build_editable_install_commands(editable_paths)
        with self._startup_profiler.time("setup.env.packages.editable_install"):
            for cmd in install_cmds:
                result = await self.world_env.execute(cmd, timeout=120)
                if result.exit_code != 0:
                    raise RuntimeError(f"Package install failed: {result.stderr}")

        # Editable installs are --no-deps, so deps added to the world's
        # pyproject.toml after its image was baked are missing on the VM.
        if self.config.dev.world:
            with self._startup_profiler.time("setup.env.packages.world_deps_sync"):
                result = await self.world_env.execute(build_world_deps_sync_command(), timeout=300)
                if result.exit_code != 0:
                    raise RuntimeError(f"World dependency sync failed: {result.stderr}")

    async def _setup_ecr_auth(self) -> None:
        """Setup ECR authentication on world VM."""
        if not self.world_env:
            raise RuntimeError("world_env must be initialized")

        from plato.utils.ecr import _clean_aws_env

        ecr_result = subprocess.run(
            ["aws", "ecr", "get-login-password", "--region", "us-west-1"],
            capture_output=True,
            text=True,
            env=_clean_aws_env(),
        )
        if ecr_result.returncode != 0:
            raise RuntimeError(f"ECR get-login-password failed: {ecr_result.stderr.strip()}")

        ecr_token = ecr_result.stdout.strip()
        ecr_registry = "383806609161.dkr.ecr.us-west-1.amazonaws.com"

        result = await self.world_env.execute(
            f"echo '{ecr_token}' | docker login --username AWS --password-stdin {ecr_registry}",
            timeout=30,
        )
        if result.exit_code != 0:
            raise RuntimeError(f"Docker login on VM failed: {result.stderr.strip()}")

    async def _setup_vscode_server(self) -> None:
        """Install and start VS Code Server (code-server) on the world VM."""
        if not self.world_env:
            raise RuntimeError("world_env must be initialized")

        VSCODE_PORT = 8080

        # Probe by version output, not `which`: VM images can carry a VS Code
        # terminal-integration shim named `code-server` on PATH that prints
        # "Command is only available in WSL or inside a Visual Studio Code
        # terminal." and exits — `which` finding it used to skip installation
        # and then "start" the shim, so health never came up. The standalone
        # install location is checked first for the same reason.
        version_probe = (
            "for c in /root/.local/bin/code-server "
            "$(which code-server 2>/dev/null) "
            "$(find /root/.local/lib -name code-server -type f -executable 2>/dev/null); do "
            '"$c" --version 2>/dev/null | grep -q "with Code" && echo "$c" && break; '
            "done"
        )
        with self._startup_profiler.time("setup.env.vscode.find_binary"):
            probe_result = await self.world_env.execute(version_probe, timeout=15)
        cs_bin = probe_result.stdout.strip().split("\n")[0]

        if not cs_bin:
            with self._startup_profiler.time("setup.env.vscode.install"):
                result = await self.world_env.execute(
                    "curl -fsSL https://code-server.dev/install.sh | sh -s -- --method=standalone",
                    timeout=120,
                )
            if result.exit_code != 0:
                raise RuntimeError(f"VS Code Server installation failed: {result.stderr.strip()}")
            probe_result = await self.world_env.execute(version_probe, timeout=15)
            cs_bin = probe_result.stdout.strip().split("\n")[0]

        if not cs_bin:
            raise RuntimeError(
                "Could not find a working code-server binary after installation "
                "(candidates failed the `--version` probe — PATH may hold a VS Code terminal shim)"
            )
        logger.info("code-server binary: %s", cs_bin)

        # Configure dark mode
        with self._startup_profiler.time("setup.env.vscode.configure"):
            await self.world_env.execute(
                "mkdir -p /root/.local/share/code-server/User && "
                """echo '{"workbench.colorTheme":"Default Dark Modern"}' > /root/.local/share/code-server/User/settings.json""",
                timeout=10,
            )

        start_cmd = (
            f"nohup {cs_bin} --bind-addr 0.0.0.0:{VSCODE_PORT} --auth none "
            f'--disable-telemetry /workspace > /tmp/code-server.log 2>&1 & echo "pid=$!"'
        )
        with self._startup_profiler.time("setup.env.vscode.start"):
            start_result = await self.world_env.execute(start_cmd, timeout=10)
        logger.info("code-server start: %s (binary=%s)", start_result.stdout.strip(), cs_bin)

        # Wait for healthy. Generous window: the cold start shares the VM with
        # the parallel editable install / deps sync. Every few polls check the
        # process is still alive so a killed/crashed code-server fails fast
        # with diagnostics instead of timing out silently.
        last_health = "000"
        elapsed = 0
        with self._startup_profiler.time("setup.env.vscode.health_wait"):
            for i in range(90):
                health = await self.world_env.execute(
                    f"curl -s -o /dev/null -w '%{{http_code}}' http://localhost:{VSCODE_PORT}/healthz 2>/dev/null || echo 000",
                    timeout=5,
                )
                last_health = health.stdout.strip()
                if last_health == "200":
                    return
                if i % 5 == 4:
                    alive = await self.world_env.execute("pgrep -c -f code-server || echo 0", timeout=5)
                    alive_count = alive.stdout.strip() or "0"
                    logger.info("code-server wait: health=%s processes=%s after ~%ds", last_health, alive_count, i + 1)
                    if alive_count == "0":
                        elapsed = i + 1
                        break
                await asyncio.sleep(1)
            else:
                elapsed = 90

        diagnostics = await self._collect_vscode_diagnostics(VSCODE_PORT, cs_bin)
        raise RuntimeError(
            f"VS Code Server failed to become healthy after ~{elapsed}s (last health={last_health}).\n{diagnostics}"
        )

    async def _collect_vscode_diagnostics(self, port: int, cs_bin: str) -> str:
        """Gather evidence for why code-server isn't serving: process table,
        port binding, server log, resource pressure, OOM kills."""
        if not self.world_env:
            return "(no world_env)"
        checks = {
            "process": "pgrep -af code-server || echo '(no code-server process)'",
            "port": (
                f"(ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null) | grep ':{port}' "
                f"|| echo '(port {port} not listening)'"
            ),
            "version": f"{cs_bin} --version 2>&1 | head -1",
            "log": "cat /tmp/code-server.log 2>/dev/null || echo '(no /tmp/code-server.log)'",
            "resources": "free -m | sed -n '1,2p'; uptime",
            "oom": "dmesg 2>/dev/null | grep -iE 'killed process|out of memory' | tail -3 || true",
        }
        sections = []
        for label, cmd in checks.items():
            try:
                result = await self.world_env.execute(cmd, timeout=10)
                output = (result.stdout or result.stderr or "").strip() or "(empty)"
            except Exception as exc:
                output = f"(diagnostic failed: {exc})"
            sections.append(f"--- {label} ---\n{output}")
        return "\n".join(sections)

    async def _write_config(self) -> None:
        """Write config to VM."""
        if not self.world_env:
            raise RuntimeError("world_env must be initialized")

        config_dict = self.config.model_dump(mode="json")
        # Inject serialized Plato session into runtime_info for the world runner
        serialized = self._serialized_session
        if serialized:
            config_dict.setdefault("world", {})["runtime_info"] = {
                "runtime_id": self.world_env.job_id,
                "hostname": "localhost",
                "serialized_session": serialized.model_dump(mode="json"),
            }
        config_json = json.dumps(config_dict)
        await self._write_file_to_vm("/tmp/config.json", config_json)

        if serialized:
            session_json = json.dumps(serialized.model_dump(mode="json"))
            try:
                await self._write_file_to_vm("/etc/plato/session.json", session_json, mkdir=True)
            except RuntimeError as exc:
                logger.warning("Failed to write session.json: %s", exc)

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

    def _print_startup_profile(self) -> None:
        """Print startup timing summary sorted by slowest steps."""
        durations = self._startup_profiler.durations()
        total = durations.get("setup.total")
        if not total:
            return

        rows = self._startup_profiler.sorted_durations(exclude={"setup.total"})
        if not self.verbose:
            rows = rows[:8]

        table = Table(title="Startup Timing", title_style="bold", show_header=True, header_style="bold")
        table.add_column("Step", overflow="fold")
        table.add_column("Seconds", justify="right")
        table.add_column("% of setup", justify="right")

        for name, seconds in rows:
            pct = (seconds / total * 100.0) if total else 0.0
            table.add_row(name, f"{seconds:.2f}", f"{pct:.1f}%")

        table.add_row("setup.total", f"{total:.2f}", "100.0%")
        console.print(table)
        console.print()

    def _startup_profile_payload(self) -> dict:
        """Build startup profile payload for JSON export."""
        durations = self._startup_profiler.durations()
        return {
            "generated_at": datetime.now(UTC).isoformat(),
            "world_package": self.config.world.package,
            "session_id": self.config.session.session_id,
            "metadata": self._startup_profiler.metadata,
            "durations_s": durations,
            "totals": {
                "setup.total": durations.get("setup.total", 0.0),
            },
        }

    def _write_startup_profile_json(self) -> None:
        """Write startup profile JSON if output path was provided."""
        if not self.startup_profile_out:
            return
        payload = self._startup_profile_payload()
        output_path = self.startup_profile_out.expanduser()
        if not output_path.is_absolute():
            output_path = (Path.cwd() / output_path).resolve()
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
            _step(f"Startup profile saved to {output_path}")
        except Exception as e:
            _warn(f"Failed to write startup profile JSON: {e}")

    async def _sweep_stale_agent_vms(self) -> None:
        """Remove agent (warm-pool) VMs left running by a dead world run.

        Clean world exits release their warm pools through the stage
        teardown; this only catches abrupt deaths (OOM, force-kill, crashes
        that skip cleanup). It runs while no world process exists, so any
        non-terminal warm-pool job is stale by definition. Best-effort —
        a sweep failure must never block the next run.
        """
        if not self.session:
            return
        try:
            jobs = await self.session.list_jobs()
        except Exception as exc:
            _warn(f"Stale agent VM sweep skipped (list_jobs failed): {exc}")
            return
        stale = [
            j
            for j in jobs
            if (j.alias or "").startswith("warm-pool-")
            and not any(terminal in str(j.status or "").upper() for terminal in ("COMPLETED", "FAILED", "CANCELLED"))
        ]
        if not stale:
            return
        _step(f"Sweeping {len(stale)} stale warm-pool VM(s) from the previous run")
        for job in stale:
            try:
                await self.session.remove_job(job.job_id)
                _info(f"Removed stale agent VM {job.alias} ({job.job_id})")
            except Exception as exc:
                _warn(f"Failed to remove stale agent VM {job.alias}: {exc}")

    async def _run_with_hot_reload(self) -> None:
        """Run the world with hot reload watching."""
        if not self.sync_manager:
            raise RuntimeError("sync_manager must be initialized")

        world_name = self.config.world.world_name
        if not world_name:
            world_name, _ = parse_package_string(self.config.world.package)

        # Start file watcher
        watch_task = asyncio.create_task(self.sync_manager.watch())

        try:
            run_count = 0
            while not self._shutdown_requested:
                run_count += 1
                self._sigint_count = 0

                # Restart file watcher if it died
                if watch_task.done():
                    await self.sync_manager.initial_sync()
                    watch_task = asyncio.create_task(self.sync_manager.watch())

                run_label = f" [dim](run #{run_count})[/dim]" if run_count > 1 else ""
                console.rule(f"[bold]{world_name}[/bold]{run_label}", style="blue")

                # While no world process is running, any agent VM still alive
                # was leaked by an abrupt world death (OOM, force-kill, crash
                # that skipped stage cleanup) — clean exits release their warm
                # pools themselves. Sweep before every run (including the
                # first: a prior force-killed dev invocation on the same
                # session leaves leaks behind) so Enter/r restarts don't
                # accumulate N agent VMs per crash.
                await self._sweep_stale_agent_vms()

                # Re-read config from disk so env var / .env changes take effect
                old_config = self.config
                self.config = Config.from_file(self.config_path)
                self.config = self.config.model_copy(
                    update={
                        "dev": old_config.dev,
                        "session": old_config.session,
                    }
                )
                if self._force_fresh_next_run:
                    world_config = dict(self.config.world.config or {})
                    state_config = world_config.get("state")
                    if isinstance(state_config, dict):
                        state_config = dict(state_config)
                        state_config.pop("resume_from", None)
                        state_config.pop("resume_session", None)
                        world_config["state"] = state_config
                    self.config = self.config.model_copy(
                        update={"world": self.config.world.model_copy(update={"config": world_config})}
                    )
                    self._force_fresh_next_run = False
                # Resolve ${VAR} placeholders the local env couldn't fill from
                # the Chronos analyzer-env (org + user scope) — the same
                # backend resolution `chronos test` and `launch` use. Local
                # values (Config.from_file expands from the shell/.env) win;
                # the backend fills the rest.
                if self.config.world.config:
                    await resolve_config_env_vars(self.config.world.config, self.api_key)
                # Copy previously resolved agent images
                old_agents = find_agent_configs(old_config.world.config or {})
                new_agents = find_agent_configs(self.config.world.config or {})
                for name, new_agent in new_agents.items():
                    old_agent = old_agents.get(name)
                    if old_agent and "image" in old_agent and "image" not in new_agent:
                        new_agent["image"] = old_agent["image"]
                # Write config to VM (chunked to avoid ARG_MAX on large configs)
                config_dict = self.config.model_dump(mode="json")
                serialized = self._serialized_session
                if serialized:
                    config_dict.setdefault("world", {})["runtime_info"] = {
                        "runtime_id": self.world_env.job_id,
                        "hostname": "localhost",
                        "serialized_session": serialized.model_dump(mode="json"),
                    }
                await self._write_file_to_vm("/tmp/config.json", json.dumps(config_dict))
                if serialized:
                    session_json = json.dumps(serialized.model_dump(mode="json"))
                    try:
                        await self._write_file_to_vm("/etc/plato/session.json", session_json, mkdir=True)
                    except RuntimeError as exc:
                        logger.warning("Failed to write session.json: %s", exc)

                # Only reinstall editable packages on the first run;
                # subsequent resumes reuse the existing editable install
                # (file watcher keeps source synced, -e installs pick up changes automatically)
                reinstall_cmd = ""
                if run_count == 1:
                    reinstall_parts = []
                    if self.config.dev.sync_sdk:
                        reinstall_parts.append("-e /sdk")
                    if self.config.dev.world:
                        reinstall_parts.append("-e /world")
                    if reinstall_parts:
                        editables = " ".join(reinstall_parts)
                        reinstall_cmd = (
                            f"uv pip install --python /opt/plato-venv/bin/python --no-deps {editables} -q 2>/dev/null; "
                        )
                # Editable installs are --no-deps; sync the world's declared
                # deps every run so a pyproject.toml edit picked up by the
                # file sync gets its new deps installed before the world boots
                # (no-op when already satisfied).
                if self.config.dev.world:
                    reinstall_cmd += f"{build_world_deps_sync_command()}; "

                # Run the world
                runner_cmd = (
                    f"/opt/plato-venv/bin/plato-world-runner run --world {world_name} --config /tmp/config.json"
                )
                if self.memray:
                    reinstall_cmd += "uv pip install --python /opt/plato-venv/bin/python memray -q 2>/dev/null; "
                    runner_cmd = f"memray run --output /tmp/memray.bin --force -m plato.worlds.runner -- run --world {world_name} --config /tmp/config.json"
                debug_env = self._forwarded_debug_env_assignments()
                debug_prefix = f"{debug_env} " if debug_env else ""
                core_env = build_world_process_env(self.api_key, self.world_env.job_id)
                env_assignments = " ".join(f"{k}={shlex.quote(v)}" for k, v in core_env.items())
                world_cmd = f"{reinstall_cmd}{debug_prefix}{env_assignments} PLATO_WORLD_DEV_MODE='1' {runner_cmd}"

                exit_code = await self._run_world_command(world_cmd)

                # Copy memray output from VM
                if self.memray:
                    await self._fetch_memray_output()

                if self._shutdown_requested:
                    break

                console.print()
                if exit_code == 0:
                    console.rule("[green]completed[/green]", style="green")
                else:
                    console.rule(f"[red]exited ({exit_code})[/red]", style="red")

                # Restart prompt
                console.print()
                console.print(
                    "  [bold]Enter[/bold] resume  [dim]·[/dim]  [bold]r[/bold] restart fresh  [dim]·[/dim]  [bold]Ctrl+C[/bold] exit"
                )
                try:
                    choice = await self._read_input("  > ")
                    choice = choice.strip().lower()
                except (EOFError, KeyboardInterrupt):
                    break

                if choice == "r":
                    await self._clear_state()
                    await self._clear_workspace_data()
                    self._force_fresh_next_run = True

                # Explicit sync before next run so code changes are guaranteed
                console.print("  [dim]Syncing code...[/dim]")
                synced = await self.sync_manager.initial_sync()
                console.print(f"  [dim]Synced {synced}/{len(self.sync_manager.targets)} target(s)[/dim]")
                console.print()

        finally:
            watch_task.cancel()
            try:
                await watch_task
            except asyncio.CancelledError:
                pass

    async def _fetch_memray_output(self) -> None:
        """Generate flamegraph on VM, then SCP both .bin and .html locally."""
        from plato.cli.chronos.dev.ssh import build_ssh_command, build_ssh_command_string

        if not self.world_env or not self.ssh_key:
            return

        _info("Generating memray flamegraph...")
        fg_cmd = build_ssh_command(
            self.world_env.job_id,
            self.ssh_key.private_key_path,
        ) + ["python -m memray flamegraph /tmp/memray.bin -o /tmp/flamegraph.html --force"]
        proc = await asyncio.create_subprocess_exec(
            *fg_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()

        local_dir = Path("memray_output")
        local_dir.mkdir(exist_ok=True)

        ssh_str = build_ssh_command_string(self.world_env.job_id, self.ssh_key.private_key_path)
        host = f"root@{self.world_env.job_id}.plato"

        for remote_file, local_file, label in [
            ("/tmp/memray.bin", local_dir / "memray.bin", "Memray binary"),
            ("/tmp/flamegraph.html", local_dir / "flamegraph.html", "Flamegraph"),
        ]:
            proc = await asyncio.create_subprocess_exec(
                *["rsync", "-e", ssh_str, f"{host}:{remote_file}", str(local_file)],
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            _, stderr = await proc.communicate()
            if proc.returncode == 0:
                _step(f"{label} saved to {local_file.resolve()}")
            else:
                _warn(f"Failed to fetch {label}")

    async def _run_world_command(self, command: str) -> int:
        """Run world command via SSH, streaming output.

        Ctrl-C handling is the linchpin for not leaking warm-pool agent VMs:
        the remote world runner converts SIGTERM into a graceful asyncio
        shutdown that unwinds the stage ``finally`` blocks (each calls
        ``WarmPool.shutdown`` → destroys the ~5 pooled agent VMs via several
        Chronos API calls). That cleanup takes real wall-clock time, so on the
        first Ctrl-C we forward SIGTERM and WAIT for the world to exit on its
        own before tearing anything down; only a second Ctrl-C (or a blown
        grace window) force-kills.
        """
        if not self.world_env or not self.ssh_key:
            raise RuntimeError("world_env and ssh_key must be initialized")

        ssh_cmd = build_ssh_command(self.world_env.job_id, self.ssh_key.private_key_path)
        ssh_cmd.append(command)

        # start_new_session puts the local ssh client in its own session so the
        # terminal's Ctrl-C (SIGINT, delivered to our foreground process group)
        # does NOT reach it. Only this process catches SIGINT; we then forward a
        # graceful SIGTERM to the remote world ourselves and keep the SSH
        # channel open so the world's async cleanup streams through and finishes
        # before the channel drops. Without this shield, Ctrl-C kills the local
        # ssh, the channel tears down, sshd SIGHUPs the half-cleaned world, and
        # it is abandoned mid-shutdown — leaking its warm-pool VMs every
        # restart. stdin=DEVNULL keeps the now-backgrounded ssh from taking
        # SIGTTIN when it tries to read the controlling terminal.
        self._world_process = await asyncio.create_subprocess_exec(
            *ssh_cmd,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            start_new_session=True,
        )

        loop = asyncio.get_running_loop()
        original_handler = signal.getsignal(signal.SIGINT)
        self._graceful_requested = False
        self._force_killed = False
        graceful_task: asyncio.Task[None] | None = None

        def _begin_graceful() -> None:
            nonlocal graceful_task
            if graceful_task is None:
                graceful_task = loop.create_task(self._graceful_stop_remote())

        def sigint_handler(signum: int, frame: object) -> None:
            self._sigint_count += 1
            if self._sigint_count == 1:
                self._graceful_requested = True
                console.print("\n  [yellow]Stopping world (graceful)...[/yellow] [dim](Ctrl+C again to force)[/dim]")
                # Signal handlers can't await; the graceful path must SSH to the
                # VM and wait for cleanup, so hand it off to the event loop.
                loop.call_soon_threadsafe(_begin_graceful)
            else:
                console.print("\n  [red]Force killing...[/red]")
                self._shutdown_requested = True
                loop.call_soon_threadsafe(self._force_kill_remote)

        signal.signal(signal.SIGINT, sigint_handler)

        try:
            stdout = self._world_process.stdout
            if stdout:
                while True:
                    line = await stdout.readline()
                    if not line:
                        break
                    sys.stdout.write(line.decode(errors="replace"))
                    sys.stdout.flush()

            await self._world_process.wait()
            exit_code = self._world_process.returncode or 0
            if self._force_killed:
                _warn("World force-killed before cleanup finished — warm-pool VMs may have leaked")
            elif self._graceful_requested:
                _step("World shut down gracefully — warm-pool VMs released")
            return exit_code
        finally:
            if graceful_task is not None:
                graceful_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await graceful_task
            signal.signal(signal.SIGINT, original_handler)
            self._world_process = None

    async def _graceful_stop_remote(self) -> None:
        """Forward SIGTERM to the remote world and wait for its cleanup.

        The world runner turns SIGTERM into a graceful asyncio shutdown, which
        unwinds the stage ``finally`` blocks (``WarmPool.shutdown`` destroys the
        pooled agent VMs). We give it a generous window — VM destruction is
        several Chronos API calls per VM — and only force-kill if it overruns.
        A second Ctrl-C skips this wait via :meth:`_force_kill_remote`.
        """
        proc = self._world_process
        if proc is None or not self.world_env or not self.ssh_key:
            return
        ssh_base = build_ssh_command(self.world_env.job_id, self.ssh_key.private_key_path)

        await self._ssh_run(ssh_base + ["pkill -TERM -f plato-world-runner"], timeout=15)

        grace_s = 90
        _info(f"Waiting up to {grace_s}s for world cleanup (releasing warm-pool VMs)...")
        for elapsed in range(1, grace_s + 1):
            if proc.returncode is not None:
                # World exited on its own; _run_world_command logs the result.
                return
            if elapsed % 15 == 0:
                _info(f"Still cleaning up... ({elapsed}/{grace_s}s)")
            await asyncio.sleep(1)

        if proc.returncode is None:
            self._force_killed = True
            _warn(f"World cleanup exceeded {grace_s}s — force killing")
            await self._ssh_run(ssh_base + ["pkill -KILL -f plato-world-runner"], timeout=10)
            with contextlib.suppress(ProcessLookupError):
                proc.kill()

    def _force_kill_remote(self) -> None:
        """Hard-kill the remote world and drop the local SSH channel (2nd Ctrl-C)."""
        self._force_killed = True
        proc = self._world_process
        if self.world_env and self.ssh_key:
            ssh_base = build_ssh_command(self.world_env.job_id, self.ssh_key.private_key_path)
            asyncio.ensure_future(self._ssh_run(ssh_base + ["pkill -KILL -f plato-world-runner"], timeout=10))
        if proc is not None and proc.returncode is None:
            with contextlib.suppress(ProcessLookupError):
                proc.kill()

    async def _ssh_run(self, cmd: list[str], timeout: float) -> str:
        """Run a one-shot SSH command on the world VM, returning combined output.

        Best-effort: swallows failures/timeouts so signal-path callers never
        raise. The persistent ControlMaster keeps these connections cheap.
        """
        proc: asyncio.subprocess.Process | None = None
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )
            out, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            return out.decode(errors="replace") if out else ""
        except Exception:
            if proc is not None and proc.returncode is None:
                with contextlib.suppress(ProcessLookupError):
                    proc.kill()
            return ""

    async def _read_input(self, prompt: str) -> str:
        """Read a line of input, async-friendly."""
        import select

        loop = asyncio.get_event_loop()
        sys.stdout.write(prompt)
        sys.stdout.flush()

        def _read() -> str:
            while True:
                ready, _, _ = select.select([sys.stdin], [], [], 0.1)
                if ready:
                    return sys.stdin.readline()

        return await loop.run_in_executor(None, _read)

    async def _clear_state(self) -> None:
        """Clear world state in Chronos DB so next run starts fresh."""
        import httpx

        session_id = self.config.session.session_id
        if not session_id:
            return
        try:
            base_url = settings.chronos_url.rstrip("/")
            async with httpx.AsyncClient(timeout=10) as client:
                await client.put(
                    f"{base_url}/api/sessions/{session_id}/state",
                    json={},
                    headers={"X-API-Key": self.api_key},
                )
        except Exception as e:
            _warn(f"Could not clear state: {e}")

    async def _clear_workspace_data(self) -> None:
        """Delete workspace data dirs on the world VM so next run starts clean."""
        from plato.cli.chronos.dev.ssh import build_ssh_command

        if not self.world_env or not self.ssh_key:
            return
        try:
            ssh_cmd = build_ssh_command(self.world_env.job_id, self.ssh_key.private_key_path)
            # Remove all data/ dirs under /workspace/*, plus durable state
            ssh_cmd.append("rm -rf /workspace/*/data /workspace/*/.webclone")
            proc = await asyncio.create_subprocess_exec(
                *ssh_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc.communicate()
            _step("Cleared workspace data")
        except Exception as e:
            _warn(f"Could not clear workspace data: {e}")

    async def _cleanup(self) -> None:
        """Clean up resources."""
        console.print()
        with console.status("  Cleaning up...", spinner="dots"):
            if self.config.session and self.config.session.session_id:
                await self._complete_chronos_session(status="completed", exit_code=0)
            if self.sync_manager:
                self.sync_manager.stop()
            if self.session:
                await self.session.close()
            if self.plato:
                await self.plato.close()
        _step("Cleanup complete")
