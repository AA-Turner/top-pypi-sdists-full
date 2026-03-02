"""Docker runtime for agent execution."""

from __future__ import annotations

import asyncio
import logging
import os
import platform
import uuid
from pathlib import Path

from plato.agents.runtime.base import AgentContext, OTelContext, PreparedAgent, Runtime

logger = logging.getLogger(__name__)


class DockerRuntime(Runtime):
    """Run agents in Docker containers."""

    async def run(self, ctx: AgentContext) -> str:
        """Run an agent in a Docker container."""
        await self._pull_image(ctx.image)

        container_name = f"agent-{uuid.uuid4().hex[:8]}"
        workspace_volume = self._get_workspace_volume(ctx.workspace)
        logs_volume = await self._create_volume(f"logs-{uuid.uuid4().hex[:8]}")

        try:
            docker_cmd = await self._build_command(ctx, container_name, workspace_volume, logs_volume)
            await self._run_container(docker_cmd, container_name)
        finally:
            await self._cleanup_volume(logs_volume)

        return container_name

    async def prepare(self, ctx: AgentContext) -> PreparedAgent:
        """Start agent container with desktop/Chrome but without running the task.

        The container starts with its native entrypoint (desktop, Chrome, etc.)
        and waits. No --instruction is passed, so the entrypoint falls through
        to `tail -f /dev/null`.
        """
        await self._pull_image(ctx.image)

        container_name = f"agent-{uuid.uuid4().hex[:8]}"
        workspace_volume = self._get_workspace_volume(ctx.workspace)

        cmd = await self._build_prepare_command(ctx, container_name, workspace_volume)

        logger.debug(f"Starting prepared container: {container_name}")
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout_bytes, stderr_bytes = await proc.communicate()

        if proc.returncode != 0:
            error_detail = stderr_bytes.decode(errors="replace").strip() if stderr_bytes else "No stderr"
            raise RuntimeError(f"Failed to start container: {error_detail}")

        container_id = stdout_bytes.decode(errors="replace").strip()
        if container_id:
            logger.info(f"Started prepared container: {container_name} ({container_id[:12]})")

        return PreparedAgent(
            agent_id=container_name,
            hostname="127.0.0.1",
            runtime=self,
        )

    async def execute(self, prepared: PreparedAgent, ctx: AgentContext) -> None:
        """Execute agent task inside a prepared container via docker exec."""
        container_name = prepared.agent_id
        logger.info(f"Executing agent in container {container_name}")

        # Build the setup + agent command (same dev-mode logic as _build_command)
        setup_cmds = self._build_setup_commands(ctx)
        agent_cmd = f'plato-agent-runner run --instruction-b64 "{ctx.instruction_b64}"'
        shell_cmd = " && ".join(setup_cmds + [agent_cmd]) if setup_cmds else agent_cmd

        exec_cmd = [
            "docker",
            "exec",
            container_name,
            "/bin/bash",
            "-c",
            shell_cmd,
        ]

        process = await asyncio.create_subprocess_exec(
            *exec_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            limit=100 * 1024 * 1024,
        )

        output_lines = await self._stream_output(process)
        await process.wait()

        if process.returncode != 0:
            error_context = "\n".join(output_lines[-50:]) if output_lines else "No output captured"
            raise RuntimeError(f"Agent failed with exit code {process.returncode}\n\nAgent output:\n{error_context}")

        logger.info("Agent execution completed")

    async def cleanup(self, agent_id: str, error: bool = False) -> None:
        """Stop and remove a container."""
        try:
            proc = await asyncio.create_subprocess_exec(
                "docker",
                "stop",
                agent_id,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await proc.wait()
        except Exception as e:
            logger.warning(f"Failed to stop container {agent_id}: {e}")

    async def _pull_image(self, image: str) -> None:
        """Pull a Docker image."""
        logger.info(f"Pulling image: {image}")
        proc = await asyncio.create_subprocess_exec(
            "docker",
            "pull",
            image,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        await proc.wait()

    def _get_workspace_volume(self, workspace: str | None) -> str:
        """Get or create workspace volume."""
        return os.environ.get("WORKSPACE_VOLUME") or workspace or f"workspace-{uuid.uuid4().hex[:8]}"

    async def _create_volume(self, name: str) -> str:
        """Create a Docker volume."""
        await asyncio.create_subprocess_exec(
            "docker",
            "volume",
            "create",
            name,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        return name

    async def _cleanup_volume(self, name: str) -> None:
        """Remove a Docker volume."""
        await asyncio.create_subprocess_exec(
            "docker",
            "volume",
            "rm",
            "-f",
            name,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )

    async def _build_command(
        self,
        ctx: AgentContext,
        container_name: str,
        workspace_volume: str,
        logs_volume: str,
    ) -> list[str]:
        """Build the docker run command."""
        cmd = ["docker", "run", "--rm", "--privileged", "--name", container_name]

        # Network configuration
        if await self._needs_host_network():
            cmd.extend(["--network=host", "--add-host=localhost:127.0.0.1"])

        # Volumes
        cmd.extend(
            [
                "-v",
                f"{workspace_volume}:/workspace",
                "-v",
                f"{logs_volume}:/logs",
                "-v",
                "/var/run/docker.sock:/var/run/docker.sock",
                "-w",
                "/workspace",
            ]
        )

        # Dev mode: mount SDK and agent code if they exist on host (world VM)
        # This mirrors the VM runtime behavior - detect dev mode by /sdk existence
        sdk_path = Path("/sdk")
        is_dev_mode = sdk_path.exists()

        if is_dev_mode:
            cmd.extend(["-v", "/sdk:/sdk"])
            logger.debug("Dev mode: mounting /sdk into container")

        # Mount all agents from /agents if it exists (dev mode)
        agents_path = Path("/agents")
        if agents_path.exists():
            cmd.extend(["-v", "/agents:/agents"])
            logger.debug("Dev mode: mounting /agents into container")

        # Mount specific agent code if provided (overrides /agents)
        if ctx.agent_code_path and ctx.agent_code_path.exists():
            cmd.extend(["-v", f"{ctx.agent_code_path}:/app"])
            logger.debug(f"Dev mode: mounting agent code {ctx.agent_code_path} into container")

        # Config
        cmd.extend(["-e", f"AGENT_CONFIG_B64={ctx.config_b64}"])
        if ctx.runtime_b64:
            cmd.extend(["-e", f"AGENT_RUNTIME_B64={ctx.runtime_b64}"])

        # OTel context
        otel = OTelContext.from_env()
        for env_var in otel.to_env_vars():
            cmd.extend(["-e", env_var])

        # Override entrypoint to run shell for dev mode setup
        cmd.extend(["--entrypoint", "/bin/bash"])

        # Image and command - install dev packages then run agent
        cmd.append(ctx.image)

        # Build shell command: fix permissions, install dev packages, then run agent
        # Use uv for installation (pip is broken on Python 3.12+ without distutils)
        # Run installs as root to avoid permission issues with mounted volumes
        setup_cmds = []

        # Fix workspace ownership for superman user
        setup_cmds.append("sudo chown -R superman:superman /workspace 2>/dev/null || true")

        if is_dev_mode:
            setup_cmds.append("sudo uv pip install --system -e /sdk -q")
        # Install all agents from /agents directory
        if agents_path.exists():
            for agent_dir in agents_path.iterdir():
                if agent_dir.is_dir() and (agent_dir / "pyproject.toml").exists():
                    setup_cmds.append(f"sudo uv pip install --system -e /agents/{agent_dir.name} -q")
        # Install specific agent if provided
        if ctx.agent_code_path and ctx.agent_code_path.exists():
            setup_cmds.append("sudo uv pip install --system -e /app -q")

        agent_cmd = f'plato-agent-runner run --instruction-b64 "{ctx.instruction_b64}"'

        shell_cmd = " && ".join(setup_cmds) + " && " + agent_cmd

        cmd.extend(["-c", shell_cmd])

        return cmd

    async def _build_prepare_command(
        self,
        ctx: AgentContext,
        container_name: str,
        workspace_volume: str,
    ) -> list[str]:
        """Build docker run command for prepare() - detached, native entrypoint, no instruction."""
        cmd = ["docker", "run", "-d", "--rm", "--privileged", "--name", container_name]

        # Always use host network for prepare() - the world needs to reach
        # container services (CDP, noVNC) at 127.0.0.1:<port>
        cmd.extend(["--network=host", "--add-host=localhost:127.0.0.1"])

        # Volumes
        cmd.extend(
            [
                "-v",
                f"{workspace_volume}:/workspace",
                "-v",
                "/var/run/docker.sock:/var/run/docker.sock",
                "-w",
                "/workspace",
            ]
        )

        # Dev mode: mount SDK and agent code
        sdk_path = Path("/sdk")
        is_dev_mode = sdk_path.exists()
        if is_dev_mode:
            cmd.extend(["-v", "/sdk:/sdk"])
        agents_path = Path("/agents")
        if agents_path.exists():
            cmd.extend(["-v", "/agents:/agents"])
        if ctx.agent_code_path and ctx.agent_code_path.exists():
            cmd.extend(["-v", f"{ctx.agent_code_path}:/app"])

        # Config env var
        cmd.extend(["-e", f"AGENT_CONFIG_B64={ctx.config_b64}"])
        if ctx.runtime_b64:
            cmd.extend(["-e", f"AGENT_RUNTIME_B64={ctx.runtime_b64}"])

        # OTel context
        otel = OTelContext.from_env()
        for env_var in otel.to_env_vars():
            cmd.extend(["-e", env_var])

        # Image with native entrypoint (no --entrypoint override, no instruction)
        cmd.append(ctx.image)

        return cmd

    def _build_setup_commands(self, ctx: AgentContext) -> list[str]:
        """Build dev-mode setup commands (pip installs) for use in docker exec."""
        setup_cmds = []

        # Fix workspace ownership
        setup_cmds.append("sudo chown -R superman:superman /workspace 2>/dev/null || true")

        sdk_path = Path("/sdk")
        is_dev_mode = sdk_path.exists()

        if is_dev_mode:
            setup_cmds.append("sudo uv pip install --system -e /sdk -q")

        agents_path = Path("/agents")
        if agents_path.exists():
            for agent_dir in agents_path.iterdir():
                if agent_dir.is_dir() and (agent_dir / "pyproject.toml").exists():
                    setup_cmds.append(f"sudo uv pip install --system -e /agents/{agent_dir.name} -q")

        if ctx.agent_code_path and ctx.agent_code_path.exists():
            setup_cmds.append("sudo uv pip install --system -e /app -q")

        return setup_cmds

    async def _needs_host_network(self) -> bool:
        """Check if host networking is needed (no iptables on Linux)."""
        if platform.system() == "Darwin":
            return False

        try:
            proc = await asyncio.create_subprocess_exec(
                "iptables",
                "-L",
                "-n",
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await proc.wait()
            return proc.returncode != 0
        except (FileNotFoundError, PermissionError):
            return True

    async def _run_container(self, cmd: list[str], container_name: str) -> None:
        """Run the container and stream output."""
        logger.debug(f"Starting container: {container_name}")
        logger.debug(f"Docker command args: {len(cmd)} args, instruction length: {len(cmd[-1]) if cmd else 0}")

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            limit=100 * 1024 * 1024,
        )

        output_lines = await self._stream_output(process)
        await process.wait()

        if process.returncode != 0:
            error_context = "\n".join(output_lines[-50:]) if output_lines else "No output captured"
            raise RuntimeError(f"Agent failed with exit code {process.returncode}\n\nAgent output:\n{error_context}")

    async def _stream_output(self, process: asyncio.subprocess.Process) -> list[str]:
        """Stream process output and return captured lines."""
        output_lines: list[str] = []
        buffer = ""
        stdout = process.stdout

        if not stdout:
            return output_lines

        while True:
            try:
                chunk = await stdout.read(65536)
            except Exception:
                break
            if not chunk:
                break

            buffer += chunk.decode(errors="replace")
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                output_lines.append(line)
                print(f"[agent] {line}")

        if buffer.strip():
            output_lines.append(buffer)
            print(f"[agent] {buffer}")

        return output_lines
