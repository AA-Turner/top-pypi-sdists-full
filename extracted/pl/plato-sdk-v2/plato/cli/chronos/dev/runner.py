"""Dev mode runner - orchestrates VM creation, sync, and execution."""

from __future__ import annotations

import asyncio
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
    Status1,
)
from plato.cli.chronos.config import Config
from plato.cli.chronos.dev.ecr import ensure_image_exists
from plato.cli.chronos.dev.paths import get_sdk_root
from plato.cli.chronos.dev.profiling import StartupProfiler
from plato.cli.chronos.dev.ssh import SSHKeyPair
from plato.cli.chronos.dev.sync import SyncManager
from plato.cli.chronos.provision import provision_vm
from plato.cli.chronos.registry import parse_package_string
from plato.cli.chronos.settings import get_settings
from plato.utils.pypi_index import plato_token_simple_index

if TYPE_CHECKING:
    from plato.v2 import AsyncPlato
    from plato.v2.environment import Environment
    from plato.v2.session import Session

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

    Mutates agent dicts in-place, setting ``image`` from the registry.
    """
    agents = find_agent_configs(config)
    for name, agent in agents.items():
        image = agent.get("image")
        package = agent.get("package")
        version = agent.get("version")

        if package and ":" in package and not version:
            package, version = parse_package_string(package)

        if package and not image:
            image = await _fetch_agent_image_from_registry(package, version, api_key)
            if image:
                agent["image"] = image
                logger.info(f"Resolved agent '{name}': {package}:{version or 'latest'} -> {image}")
            else:
                raise ValueError(f"Could not resolve image for agent '{name}' (package={package})")


async def _fetch_agent_image_from_registry(
    package: str, version: str | None = None, api_key: str | None = None
) -> str | None:
    """Fetch agent image URL from Chronos registry API."""
    import httpx

    try:
        async with httpx.AsyncClient(
            base_url=settings.chronos_url.rstrip("/"),
            timeout=30.0,
            headers={"X-API-Key": api_key} if api_key else {},
        ) as client:
            resp = await get_agent_schema_api.asyncio(client, agent_name=package, version=version)
            return resp.image if resp.image else None
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
        self._shutdown_requested = False
        self._force_fresh_next_run = False
        self._startup_profiler = StartupProfiler(metadata={"config_path": str(config_path)})

    def _resolve_path(self, path: Path | None) -> Path | None:
        """Resolve a path relative to config file directory."""
        if path is None:
            return None
        if path.is_absolute():
            return path
        return (self.config_path.parent / path).resolve()

    def _forwarded_debug_env_assignments(self) -> str:
        parts: list[str] = []
        for key in ("PLATO_FUSE_DEBUG", "PLATO_SMART_COMMIT_DEBUG", "RUST_LOG"):
            value = os.environ.get(key)
            if value:
                parts.append(f"{key}={shlex.quote(value)}")
        return " ".join(parts)

    async def run(self) -> None:
        """Run the dev workflow."""
        from plato.runtime import VMRuntimeConfig
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
                            timeout=world_runtime.vm.timeout or 7200,
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
                                "session": self.config.session.model_copy(
                                    update={"plato_session": self.session.dump()}
                                ),
                            }
                        )
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

        world_path = self._resolve_path(self.config.dev.world)
        if world_path:
            self.sync_manager.add_target(
                local_path=world_path,
                remote_path="/world",
                job_id=self.world_env.job_id,
            )

        for name, agent_path in self.config.dev.agents.items():
            resolved = self._resolve_path(agent_path)
            if resolved:
                self.sync_manager.add_target(
                    local_path=resolved,
                    remote_path=f"/agents/{name}",
                    job_id=self.world_env.job_id,
                )

        for name, extra_path in self.config.dev.extra_sync.items():
            resolved = self._resolve_path(extra_path)
            if resolved:
                self.sync_manager.add_target(
                    local_path=resolved,
                    remote_path=f"/extra/{name}",
                    job_id=self.world_env.job_id,
                )

        if self.config.dev.sync_sdk:
            if isinstance(self.config.dev.sync_sdk, Path):
                sdk_root = self.config.dev.sync_sdk.resolve()
            else:
                sdk_root = get_sdk_root()
            if sdk_root and (sdk_root / "pyproject.toml").exists():
                self.sync_manager.add_target(
                    local_path=sdk_root,
                    remote_path="/sdk",
                    job_id=self.world_env.job_id,
                )

    async def _install_packages(self) -> None:
        """Install packages in editable mode."""
        if not self.world_env:
            raise RuntimeError("world_env must be initialized")

        # Ensure fuse3 userspace tools are present for the Rust plato-fuse binary.
        with self._startup_profiler.time("setup.env.packages.system_deps"):
            await self.world_env.execute(
                "dpkg -s fuse3 > /dev/null 2>&1 || "
                "(apt-get update -qq && apt-get install -y -qq fuse3) > /dev/null 2>&1",
                timeout=60,
            )

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
                result = await self.world_env.execute(
                    "python3 -c \"import importlib.metadata; eps = importlib.metadata.entry_points(group='plato.worlds'); print(' '.join(set(ep.dist.name for ep in eps)))\" 2>/dev/null || true",
                    timeout=30,
                )
                if result.stdout.strip():
                    pkgs = result.stdout.strip()
                    await self.world_env.execute(f"uv pip uninstall --system {pkgs}", timeout=60)

        # Uninstall existing SDK so editable install properly overrides it
        if self.config.dev.sync_sdk:
            with self._startup_profiler.time("setup.env.packages.uninstall_sdk"):
                await self.world_env.execute("uv pip uninstall --system plato-sdk-v2", timeout=60)

        editable_paths = []
        if self.config.dev.sync_sdk:
            editable_paths.append("'/sdk[worlds]'")
        if self.config.dev.world:
            with self._startup_profiler.time("setup.env.packages.prepare_world"):
                await self.world_env.execute(
                    "rm -rf /world/dist /world/*.egg-info /world/src/*.egg-info /world/build", timeout=10
                )
            editable_paths.append("/world")

        if not editable_paths:
            return

        editables = " ".join(f"-e {p}" for p in editable_paths)
        pypi_store_idx = plato_token_simple_index("pypi-store", api_key=self.api_key)
        with self._startup_profiler.time("setup.env.packages.editable_install"):
            result = await self.world_env.execute(
                f"uv pip install --system --index-url {shlex.quote(pypi_store_idx)} {editables}",
                timeout=300,
            )
        if result.exit_code != 0:
            raise RuntimeError(f"Package install failed: {result.stderr}")

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

        install_cmd = (
            "which code-server > /dev/null 2>&1 || "
            "curl -fsSL https://code-server.dev/install.sh | sh -s -- --method=standalone"
        )
        with self._startup_profiler.time("setup.env.vscode.install"):
            result = await self.world_env.execute(install_cmd, timeout=120)
        if result.exit_code != 0:
            raise RuntimeError(f"VS Code Server installation failed: {result.stderr.strip()}")

        # Configure dark mode
        with self._startup_profiler.time("setup.env.vscode.configure"):
            await self.world_env.execute(
                "mkdir -p /root/.local/share/code-server/User && "
                """echo '{"workbench.colorTheme":"Default Dark Modern"}' > /root/.local/share/code-server/User/settings.json""",
                timeout=10,
            )

        with self._startup_profiler.time("setup.env.vscode.find_binary"):
            which_result = await self.world_env.execute(
                "which code-server 2>/dev/null || find /root/.local/lib -name code-server -type f -executable 2>/dev/null | head -1",
                timeout=10,
            )
        cs_bin = which_result.stdout.strip().split("\n")[0]
        if not cs_bin:
            raise RuntimeError("Could not find code-server binary after installation")

        start_cmd = (
            f"nohup {cs_bin} --bind-addr 0.0.0.0:{VSCODE_PORT} --auth none "
            f"--disable-telemetry /workspace > /tmp/code-server.log 2>&1 &"
        )
        with self._startup_profiler.time("setup.env.vscode.start"):
            await self.world_env.execute(start_cmd, timeout=10)

        # Wait for healthy
        with self._startup_profiler.time("setup.env.vscode.health_wait"):
            for i in range(30):
                health = await self.world_env.execute(
                    f"curl -s -o /dev/null -w '%{{http_code}}' http://localhost:{VSCODE_PORT}/healthz 2>/dev/null || echo 000",
                    timeout=5,
                )
                if health.stdout.strip() == "200":
                    return
                await asyncio.sleep(1)

        raise RuntimeError("VS Code Server failed to become healthy after 30s")

    async def _write_config(self) -> None:
        """Write config to VM."""
        if not self.world_env:
            raise RuntimeError("world_env must be initialized")

        config_dict = self.config.model_dump(mode="json")
        config_json = json.dumps(config_dict)
        escaped_config = config_json.replace("'", "'\\''")
        result = await self.world_env.execute(f"echo '{escaped_config}' > /tmp/config.json", timeout=30)
        if result.exit_code != 0:
            raise RuntimeError(f"Failed to write config: {result.stderr}")

        # Write serialized session to a well-known path so integration tests
        # running on the VM can reuse the active Plato session.
        if self.config.session.plato_session:
            session_json = json.dumps(self.config.session.plato_session.model_dump(mode="json"))
            escaped_session = session_json.replace("'", "'\\''")
            result = await self.world_env.execute(
                f"mkdir -p /etc/plato && echo '{escaped_session}' > /etc/plato/session.json",
                timeout=30,
            )
            if result.exit_code != 0:
                logger.warning("Failed to write session.json: %s", result.stderr)

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

    async def _run_with_hot_reload(self) -> None:
        """Run the world with hot reload watching."""
        if not self.sync_manager:
            raise RuntimeError("sync_manager must be initialized")

        world_name, _ = parse_package_string(self.config.world.package)
        pypi_store_idx = plato_token_simple_index("pypi-store", api_key=self.api_key)

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
                # Copy previously resolved agent images
                old_agents = find_agent_configs(old_config.world.config or {})
                new_agents = find_agent_configs(self.config.world.config or {})
                for name, new_agent in new_agents.items():
                    old_agent = old_agents.get(name)
                    if old_agent and "image" in old_agent and "image" not in new_agent:
                        new_agent["image"] = old_agent["image"]
                # Inline config write into the world command to save an SSH round-trip
                config_json = json.dumps(self.config.model_dump(mode="json"))
                escaped_config = config_json.replace("'", "'\\''")
                write_config_cmd = f"echo '{escaped_config}' > /tmp/config.json; "
                if self.config.session.plato_session:
                    session_json = json.dumps(self.config.session.plato_session.model_dump(mode="json"))
                    escaped_session = session_json.replace("'", "'\\''")
                    write_config_cmd += f"mkdir -p /etc/plato && echo '{escaped_session}' > /etc/plato/session.json; "

                # Only reinstall editable packages on the first run;
                # subsequent resumes reuse the existing editable install
                # (file watcher keeps source synced, -e installs pick up changes automatically)
                reinstall_cmd = ""
                if run_count == 1:
                    reinstall_parts = []
                    if self.config.dev.sync_sdk:
                        reinstall_parts.append("-e '/sdk[worlds]'")
                    if self.config.dev.world:
                        reinstall_parts.append("-e /world")
                    if reinstall_parts:
                        editables = " ".join(reinstall_parts)
                        reinstall_cmd = (
                            f"uv pip install --system --no-deps "
                            f"--index-url {shlex.quote(pypi_store_idx)} {editables} -q 2>/dev/null; "
                        )

                # Run the world
                runner_cmd = f"plato-world-runner run --world {world_name} --config /tmp/config.json"
                if self.memray:
                    reinstall_cmd += (
                        f"uv pip install --system --index-url {shlex.quote(pypi_store_idx)} memray -q 2>/dev/null; "
                    )
                    runner_cmd = f"memray run --output /tmp/memray.bin --force -m plato.worlds.runner -- run --world {world_name} --config /tmp/config.json"
                debug_env = self._forwarded_debug_env_assignments()
                debug_prefix = f"{debug_env} " if debug_env else ""
                world_cmd = (
                    f"{write_config_cmd}{reinstall_cmd}"
                    f"{debug_prefix}PLATO_API_KEY={shlex.quote(self.api_key)} PLATO_WORLD_DEV_MODE='1' {runner_cmd}"
                )

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
        """Run world command via SSH, streaming output."""
        import subprocess

        from plato.cli.chronos.dev.ssh import build_ssh_command

        if not self.world_env or not self.ssh_key:
            raise RuntimeError("world_env and ssh_key must be initialized")

        ssh_cmd = build_ssh_command(self.world_env.job_id, self.ssh_key.private_key_path)
        ssh_cmd.append(command)

        self._world_process = await asyncio.create_subprocess_exec(
            *ssh_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        # Setup signal handler for Ctrl+C
        original_handler = signal.getsignal(signal.SIGINT)

        def sigint_handler(signum: int, frame: object) -> None:
            self._sigint_count += 1
            if self._sigint_count == 1:
                console.print("\n  [yellow]Stopping world (graceful)...[/yellow] [dim](Ctrl+C again to force)[/dim]")
                # Send SIGTERM to the remote world process so close() runs
                # (cleans up agents, tailscale, etc.) before SSH drops.
                if self.world_env and self.ssh_key:
                    try:
                        subprocess.run(
                            build_ssh_command(self.world_env.job_id, self.ssh_key.private_key_path)
                            + ["pkill -TERM -f 'plato-world-runner'"],
                            timeout=5,
                            capture_output=True,
                        )
                    except Exception:
                        pass
            else:
                console.print("\n  [red]Force killing...[/red]")
                self._shutdown_requested = True
                if self._world_process:
                    self._world_process.kill()

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
            return self._world_process.returncode or 0
        finally:
            signal.signal(signal.SIGINT, original_handler)
            self._world_process = None

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
