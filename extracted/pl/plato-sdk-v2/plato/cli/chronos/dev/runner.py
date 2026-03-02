"""Dev mode runner - orchestrates VM creation, sync, and execution."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import TYPE_CHECKING

from plato.chronos.api.registry import (
    get_agent_schema_api_registry_agents__agent_name__schema_get as get_agent_schema_api,
)
from plato.chronos.api.sessions import complete_session, create_session
from plato.chronos.models import CompleteSessionRequest, CreateSessionRequest, CreateSessionResponse
from plato.cli.chronos.config import Config
from plato.cli.chronos.dev.ecr import ensure_image_exists
from plato.cli.chronos.dev.paths import get_sdk_root
from plato.cli.chronos.dev.ssh import SSHKeyPair
from plato.cli.chronos.dev.sync import SyncManager
from plato.cli.chronos.registry import get_world_schema, parse_package_string
from plato.cli.chronos.settings import get_settings

if TYPE_CHECKING:
    from plato.v2 import AsyncPlato
    from plato.v2.environment import Environment
    from plato.v2.session import Session

settings = get_settings()
logger = logging.getLogger(__name__)


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
    ):
        self.config = config
        self.config_path = config_path
        self.api_key: str = api_key or os.environ.get("PLATO_API_KEY") or ""
        self.verbose = verbose

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

    def _resolve_path(self, path: Path | None) -> Path | None:
        """Resolve a path relative to config file directory."""
        if path is None:
            return None
        if path.is_absolute():
            return path
        return (self.config_path.parent / path).resolve()

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

        logger.info(f"Chronos Dev Mode - {world_package}")

        self.plato = AsyncPlato()

        try:
            # 1. Fetch world schema to get image
            logger.info("Fetching world schema...")
            world_schema = await get_world_schema(world_package, world_version)
            self.world_image = world_schema.get("image", "")
            if not self.world_image:
                raise ValueError(f"No image found in schema for {world_package}")
            logger.info(f"World image: {self.world_image}")

            # 2. Ensure images exist
            await self._ensure_images()

            # 3. Create Chronos session
            logger.info("Creating Chronos session...")
            chronos_session = await self._create_chronos_session()

            # Generate STS credentials for S3 artifact uploads
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

            logger.info(f"Session: {self.config.session.session_id}")
            logger.info(f"  {settings.chronos_url}/sessions/{self.config.session.session_id}")

            # 4. Create World VM
            world_runtime = self.config.world.runtime
            if world_runtime.type != "vm":
                raise ValueError("World must use VM runtime in dev mode")
            if not isinstance(world_runtime, VMRuntimeConfig):
                raise ValueError("World must use VM runtime config")

            logger.info("Creating world VM...")
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
                connect_network=True,
            )
            if not self.session:
                raise RuntimeError("Failed to create session")
            await self.session.start_heartbeat()
            self.world_env = self.session.envs[0]
            if not self.world_env:
                raise RuntimeError("Failed to get world environment")

            logger.info(f"World VM: {self.world_env.job_id}")

            # 5. Setup SSH
            logger.info("Setting up SSH...")
            self.ssh_key = SSHKeyPair.generate()
            ssh_response = await self.session.add_ssh_key(self.ssh_key.public_key)
            if not ssh_response.success:
                raise RuntimeError(f"SSH key setup failed: {ssh_response}")

            await self.world_env.execute("which rsync || apt-get update && apt-get install -y rsync", timeout=60)
            await self._copy_ssh_key_to_vm()

            self.config = self.config.model_copy(
                update={
                    "dev": self.config.dev.model_copy(update={"ssh_key_path": Path("/root/.ssh/agent_key")}),
                    "session": self.config.session.model_copy(update={"plato_session": self.session.dump()}),
                }
            )

            logger.info("SSH configured")

            # 6. Sync code
            self.sync_manager = SyncManager(self.ssh_key.private_key_path, verbose=self.verbose)
            await self._setup_sync_targets()
            await self.sync_manager.initial_sync()

            # 7. Install packages
            await self._install_packages()

            # 8. Setup ECR auth
            await self._setup_ecr_auth()

            # 9. Install VS Code Server
            await self._setup_vscode_server()

            # 10. Write config to VM
            logger.info("Writing config...")
            await self._write_config()

            setup_time = time.time() - total_start
            logger.info(f"Setup complete in {setup_time:.1f}s")
            logger.info(f"SSH: plato sandbox ssh -J {self.world_env.job_id}")

            # 9. Run with hot reload
            await self._run_with_hot_reload()

        except asyncio.CancelledError:
            logger.warning("Interrupted")
        except KeyboardInterrupt:
            logger.warning("Interrupted")
        except Exception as e:
            logger.error(f"Error: {e}")
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

        for name, agent in self._get_agent_fields().items():
            image = agent.get("image")
            package = agent.get("package")
            version = agent.get("version")

            # Parse package:version format (e.g., "computer-use-agent:0.0.0.dev3")
            if package and ":" in package and not version:
                package, version = parse_package_string(package)

            # If package specified, fetch image from registry
            if package and not image:
                logger.info(f"Fetching image for agent '{name}' from registry (package={package})...")
                image = await _fetch_agent_image_from_registry(package, version, self.api_key)
                if image:
                    logger.info(f"Agent ({name}) image: {image}")
                    # Update the config with resolved image
                    agent["image"] = image
                else:
                    raise ValueError(f"Could not resolve image for agent '{name}' (package={package})")

            if image:
                images.append((f"Agent ({name})", image))

        for label, image in images:
            logger.info(f"Checking {label} image...")
            await ensure_image_exists(image)

        logger.info("All images verified")

    async def _create_chronos_session(self) -> CreateSessionResponse:
        """Create a session in Chronos for OTel traces."""
        import httpx

        world_config = self.config.world.config or {}
        body = CreateSessionRequest(
            world_name=self.config.world.package or "",
            world_config=world_config,
            tags=self.config.tags,
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
        error_message: str | None = None,
    ) -> None:
        """Mark Chronos session as complete."""
        import httpx

        try:
            body = CompleteSessionRequest(
                status=status,
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

    async def _copy_ssh_key_to_vm(self) -> None:
        """Copy SSH key pair to world VM."""
        if not self.ssh_key or not self.world_env:
            return

        private_key = self.ssh_key.private_key_path.read_text()
        public_key = self.ssh_key.public_key

        escaped_private = private_key.replace("'", "'\\''")
        escaped_public = public_key.replace("'", "'\\''")
        await self.world_env.execute(
            f"mkdir -p /root/.ssh && "
            f"echo '{escaped_private}' > /root/.ssh/agent_key && chmod 600 /root/.ssh/agent_key && "
            f"echo '{escaped_public}' > /root/.ssh/agent_key.pub && chmod 644 /root/.ssh/agent_key.pub",
            timeout=30,
        )

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

        if self.config.dev.sync_sdk:
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

        # First, uninstall any existing world package from the Docker image
        # This ensures entry points are updated when package name changes
        if self.config.dev.world:
            logger.info("Uninstalling existing world package...")
            # Find and remove ALL world packages from ALL site-packages
            result = await self.world_env.execute(
                "python3 -c \"import importlib.metadata; eps = importlib.metadata.entry_points(group='plato.worlds'); print(' '.join(set(ep.dist.name for ep in eps)))\" 2>/dev/null || true",
                timeout=30,
            )
            if result.stdout.strip():
                pkgs = result.stdout.strip()
                logger.info(f"Found world packages to uninstall: {pkgs}")
                await self.world_env.execute(f"uv pip uninstall --system {pkgs}", timeout=60)

        # Uninstall existing SDK so editable install properly overrides it
        if self.config.dev.sync_sdk:
            logger.info("Uninstalling existing SDK package...")
            await self.world_env.execute("uv pip uninstall --system plato-sdk-v2", timeout=60)

        editable_paths = []
        if self.config.dev.sync_sdk:
            editable_paths.append("/sdk")
        if self.config.dev.world:
            # Clear any build cache/artifacts
            await self.world_env.execute(
                "rm -rf /world/dist /world/*.egg-info /world/src/*.egg-info /world/build", timeout=10
            )
            editable_paths.append("/world")

        if not editable_paths:
            return

        # Install all editables in a single command so uv resolves the editable
        # SDK as satisfying the world's plato-sdk-v2 dependency (avoids re-pulling from PyPI)
        editables = " ".join(f"-e {p}" for p in editable_paths)
        logger.info(f"Installing packages: {editable_paths}")
        result = await self.world_env.execute(f"uv pip install --system {editables}", timeout=300)
        if result.exit_code != 0:
            raise RuntimeError(f"Package install failed: {result.stderr}")

        logger.info("Packages installed")

    async def _setup_ecr_auth(self) -> None:
        """Setup ECR authentication on world VM."""
        if not self.world_env:
            raise RuntimeError("world_env must be initialized")

        from plato.utils.ecr import _clean_aws_env

        logger.info("Setting up ECR auth...")
        ecr_result = subprocess.run(
            ["aws", "ecr", "get-login-password", "--region", "us-west-1"],
            capture_output=True,
            text=True,
            env=_clean_aws_env(),
        )
        if ecr_result.returncode != 0:
            logger.warning("ECR auth failed (AWS CLI). Docker pulls may fail.")
            return

        ecr_token = ecr_result.stdout.strip()
        ecr_registry = "383806609161.dkr.ecr.us-west-1.amazonaws.com"

        result = await self.world_env.execute(
            f"echo '{ecr_token}' | docker login --username AWS --password-stdin {ecr_registry}",
            timeout=30,
        )
        if result.exit_code != 0:
            logger.warning("Docker login on VM failed")
        else:
            logger.info("ECR auth configured")

    async def _setup_vscode_server(self) -> None:
        """Install and start VS Code Server (code-server) on the world VM."""
        if not self.world_env:
            raise RuntimeError("world_env must be initialized")

        VSCODE_PORT = 8080

        logger.info("Installing VS Code Server...")
        install_cmd = (
            "which code-server > /dev/null 2>&1 || "
            "curl -fsSL https://code-server.dev/install.sh | sh -s -- --method=standalone"
        )
        result = await self.world_env.execute(install_cmd, timeout=120)
        if result.exit_code != 0:
            logger.warning(f"VS Code Server installation failed: {result.stderr}")
            return

        # Start code-server in the background with no auth (VM is already behind SSH)
        start_cmd = (
            f"nohup code-server --bind-addr 0.0.0.0:{VSCODE_PORT} --auth none "
            f"--disable-telemetry > /tmp/code-server.log 2>&1 &"
        )
        await self.world_env.execute(start_cmd, timeout=10)

        vscode_url = f"https://{self.world_env.job_id}--{VSCODE_PORT}.sims.plato.so"
        logger.info(f"VS Code Server: {vscode_url}")

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

    async def _run_with_hot_reload(self) -> None:
        """Run the world with hot reload watching."""
        if not self.sync_manager:
            raise RuntimeError("sync_manager must be initialized")

        world_name, _ = parse_package_string(self.config.world.package)

        # Start file watcher
        watch_task = asyncio.create_task(self.sync_manager.watch())

        try:
            run_count = 0
            while not self._shutdown_requested:
                run_count += 1
                self._sigint_count = 0

                # Restart file watcher if it died (e.g. from Ctrl+C killing fswatch)
                if watch_task.done():
                    logger.info("Restarting file watcher...")
                    await self.sync_manager.initial_sync()
                    watch_task = asyncio.create_task(self.sync_manager.watch())

                logger.info(f"Running: {world_name}" + (f" (run #{run_count})" if run_count > 1 else ""))

                # Reinstall editable packages on each restart so synced code takes effect
                reinstall_parts = []
                if self.config.dev.sync_sdk:
                    reinstall_parts.append("-e /sdk")
                if self.config.dev.world:
                    reinstall_parts.append("-e /world")
                reinstall_cmd = ""
                if reinstall_parts:
                    editables = " ".join(reinstall_parts)
                    reinstall_cmd = f"uv pip install --system --no-deps {editables} -q 2>/dev/null; "

                # Run the world
                world_cmd = f"{reinstall_cmd}PLATO_API_KEY='{self.api_key}' plato-world-runner run --world {world_name} --config /tmp/config.json"

                exit_code = await self._run_world_command(world_cmd)

                if self._shutdown_requested:
                    break

                if exit_code == 0:
                    logger.info("World completed successfully")
                else:
                    logger.error(f"World exited with code {exit_code}")

                # Show controls and wait for input using select for interruptibility
                print("\nPress Enter to restart • Ctrl+C to exit")

                try:
                    await self._wait_for_enter()
                except (EOFError, KeyboardInterrupt):
                    break

        finally:
            watch_task.cancel()
            try:
                await watch_task
            except asyncio.CancelledError:
                pass

    async def _wait_for_enter(self) -> None:
        """Wait for Enter key using select() for clean cancellation."""
        import select

        loop = asyncio.get_event_loop()

        def _check_stdin() -> bool:
            """Check if stdin has data ready (non-blocking)."""
            ready, _, _ = select.select([sys.stdin], [], [], 0.1)
            return bool(ready)

        while not self._shutdown_requested:
            has_input = await loop.run_in_executor(None, _check_stdin)
            if has_input:
                sys.stdin.readline()  # Consume the input
                return

    async def _run_world_command(self, command: str) -> int:
        """Run world command via SSH, streaming output."""
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
                print("\nStopping world... (Ctrl+C again to exit)")
                if self._world_process:
                    self._world_process.terminate()
            else:
                print("\nShutting down...")
                self._shutdown_requested = True
                if self._world_process:
                    self._world_process.kill()

        signal.signal(signal.SIGINT, sigint_handler)

        try:
            # Stream output line by line
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

    async def _cleanup(self) -> None:
        """Clean up resources."""
        logger.info("Cleaning up...")
        if self.config.session and self.config.session.session_id:
            await self._complete_chronos_session(status="completed", exit_code=0)
        if self.sync_manager:
            self.sync_manager.stop()
        if self.session:
            await self.session.close()
        if self.plato:
            await self.plato.close()
        logger.info("Cleanup complete")
