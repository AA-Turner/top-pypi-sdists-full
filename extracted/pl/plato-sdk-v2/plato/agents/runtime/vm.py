"""VM runtime for agent execution in Firecracker VMs."""

from __future__ import annotations

import logging
import uuid
from pathlib import Path
from typing import TYPE_CHECKING

from opentelemetry import trace
from pydantic import BaseModel

from plato.agents.runtime.base import AgentContext, OTelContext, PreparedAgent, Runtime
from plato.agents.runtime.dev import install_production_agent, sync_dev_code
from plato.agents.runtime.transport import Transport
from plato.utils.subprocess import run_ssh, run_ssh_streaming
from plato.v2 import Env
from plato.v2.types import SimConfigCompute

if TYPE_CHECKING:
    from plato.v2.async_.environment import Environment
    from plato.v2.async_.session import Session

logger = logging.getLogger(__name__)

_VM_SSH_EXTRA_OPTS: list[tuple[str, str]] = [
    ("ServerAliveInterval", "30"),
    ("ServerAliveCountMax", "3"),
]


class VMConfig(BaseModel):
    """Configuration for agent VMs."""

    cpus: int = 1
    memory: int = 2048
    disk: int = 10240
    timeout: int = 1800
    """Job timeout in seconds. The VM is killed after this duration (default: 1800 = 30 min)."""


class PlatoVMRuntime(Runtime):
    """Run agents in Firecracker VMs.

    Supports two modes:
    - Dev mode (dev_mode=True): Syncs SDK and agent code from world VM to agent VMs
      for hot-reload development
    - Non-dev mode (dev_mode=False): Uses code from Docker image, only syncs workspace

    Agent code syncing flow (dev mode only):
    1. Dev runner syncs code from local machine → world VM at /agents/<name>/
    2. World calls run_agent() with agent_code_path=/agents/<name>/ and dev_mode=True
    3. PlatoVMRuntime creates agent VM and syncs /agents/<name>/ → /app on agent VM
    4. Agent runs with the synced code
    """

    def __init__(
        self,
        session: Session,
        ssh_key_path: Path | None = None,
        vm_config: VMConfig | None = None,
        workspace: Transport | None = None,
        workspaces: list[Transport] | None = None,
    ):
        self.session = session
        self.ssh_key_path = ssh_key_path
        self.vm_config = vm_config or VMConfig()
        self.workspace = workspace  # backward compat — single workspace
        self.workspaces: list[Transport] = workspaces or []
        self._agent_envs: dict[str, Environment] = {}

    def _all_workspaces(self) -> list[Transport]:
        """Return all workspaces (single + list) for setup/sync."""
        result = list(self.workspaces)
        if self.workspace and self.workspace not in result:
            result.insert(0, self.workspace)
        return result

    async def run(self, ctx: AgentContext) -> str:
        """Run an agent in a Firecracker VM: create → setup → execute → cleanup."""
        try:
            prepared = await self.prepare(ctx)
        except Exception:
            logger.exception("Failed to prepare agent VM (image=%s)", ctx.image)
            raise
        try:
            await self.execute(prepared, ctx)
        except Exception:
            logger.exception("Agent execution failed (agent_id=%s, image=%s)", prepared.agent_id, ctx.image)
            await self.cleanup(prepared.agent_id, error=True)
            raise
        else:
            await self.cleanup(prepared.agent_id)
        return prepared.agent_id

    async def prepare(self, ctx: AgentContext) -> PreparedAgent:
        """Start agent VM with desktop/Chrome but without running the task."""
        agent_alias = f"agent-{uuid.uuid4().hex[:8]}"

        agent_env = await self._create_vm(ctx.image, agent_alias)
        self._agent_envs[agent_alias] = agent_env

        try:
            await self._setup_network()

            mesh_ip = await agent_env.get_mesh_ip()
            if not mesh_ip:
                raise RuntimeError(f"Failed to get mesh IP for agent VM {agent_alias}")

            await self._sync_code(ctx, agent_env, mesh_ip)
        except Exception:
            await self.cleanup(agent_alias, error=True)
            raise

        return PreparedAgent(
            agent_id=agent_alias,
            hostname=mesh_ip,
            runtime=self,
        )

    async def execute(self, prepared: PreparedAgent, ctx: AgentContext) -> None:
        """Execute agent task in a prepared VM via SSH."""
        agent_env = self._agent_envs.get(prepared.agent_id)
        if not agent_env:
            raise RuntimeError(f"No VM found for agent {prepared.agent_id}")

        logger.info(f"Executing agent on {prepared.hostname} (job={agent_env.job_id})")
        await self._execute_agent(ctx, agent_env, prepared.hostname)
        logger.info(f"Agent finished on {prepared.hostname}, syncing workspaces back")

        for ws in self._all_workspaces():
            logger.info(f"Syncing back workspace: {ws.path}")
            await ws.sync_back(agent_env, prepared.hostname)
        logger.info("All workspaces synced back")

    async def cleanup(self, agent_id: str, error: bool = False) -> None:
        """Clean up an agent VM."""
        agent_env = self._agent_envs.pop(agent_id, None)
        if not agent_env:
            for alias, env in list(self._agent_envs.items()):
                if env.job_id == agent_id:
                    agent_env = self._agent_envs.pop(alias)
                    break

        if agent_env:
            try:
                logger.info(f"Cleaning up agent VM: {agent_env.job_id}")
                await self.session.remove_env(agent_env)
            except Exception as e:
                logger.warning(f"Failed to clean up agent VM: {e}")

    async def _create_vm(self, image: str, alias: str) -> Environment:
        """Create an agent VM."""
        logger.info(
            f"Creating agent VM: {alias} (image: {image}, cpus={self.vm_config.cpus}, mem={self.vm_config.memory}MB)"
        )

        try:
            agent_env = await self.session.add_env(
                Env.resource(
                    simulator=alias,
                    sim_config=SimConfigCompute(
                        cpus=self.vm_config.cpus,
                        memory=self.vm_config.memory,
                        disk=self.vm_config.disk,
                    ),
                    alias=alias,
                    docker_image_url=image,
                    upload_rootfs=False,
                    rootfs_storage_backend="snapshot-store",
                ),
                timeout=self.vm_config.timeout,
            )
        except Exception:
            logger.exception("Failed to create agent VM %s (image=%s)", alias, image)
            raise

        logger.info(f"Agent VM ready: {agent_env.job_id}")
        return agent_env

    async def _setup_network(self) -> None:
        """Setup network connectivity to agent VM."""
        await self.session.connect_network()

        if not self.ssh_key_path:
            raise RuntimeError("ssh_key_path must be set before running agents")

        pub_key = Path(str(self.ssh_key_path) + ".pub").read_text().strip()
        await self.session.add_ssh_key(pub_key)

    def _parse_image_url(self, image: str) -> tuple[str, str]:
        """Extract package name and version from image URL."""
        last_part = image.split("/")[-1]
        if ":" in last_part:
            name, version = last_part.rsplit(":", 1)
            return name, version
        return last_part, "latest"

    async def _sync_code(self, ctx: AgentContext, agent_env: Environment, hostname: str) -> None:
        """Sync workspaces and install agent code on VM."""
        import time

        t0 = time.monotonic()
        for ws in self._all_workspaces():
            ws_t0 = time.monotonic()
            await ws.setup_agent(agent_env, hostname)
            logger.info("Workspace '%s' setup_agent took %.1fs", ws.path, time.monotonic() - ws_t0)
        logger.info("All workspace setup_agent took %.1fs", time.monotonic() - t0)

        if not self.ssh_key_path:
            raise RuntimeError("ssh_key_path required for code sync")

        t1 = time.monotonic()
        if Path("/sdk").exists():
            package_name, _ = self._parse_image_url(ctx.image)
            synced_agent_code = await sync_dev_code(self.ssh_key_path, hostname, ctx.agent_code_path, package_name)
            if not synced_agent_code:
                _, version = self._parse_image_url(ctx.image)
                logger.info(
                    "Falling back to production agent install for %s==%s (no synced dev agent code found).",
                    package_name,
                    version,
                )
                await install_production_agent(self.ssh_key_path, hostname, package_name, version)
        else:
            package_name, version = self._parse_image_url(ctx.image)
            await install_production_agent(self.ssh_key_path, hostname, package_name, version)
        logger.info("Agent code sync/install took %.1fs", time.monotonic() - t1)

    async def _run_ssh(
        self,
        hostname: str,
        command: str,
        user: str = "root",
        timeout: int = 300,
    ) -> tuple[int, str, str]:
        """Run a command via SSH. Delegates to shared helper."""
        assert self.ssh_key_path is not None
        return await run_ssh(
            self.ssh_key_path, hostname, command, user=user, timeout=timeout, extra_opts=_VM_SSH_EXTRA_OPTS
        )

    async def _run_ssh_streaming(
        self,
        hostname: str,
        command: str,
        user: str = "root",
    ) -> int:
        """Run a command via SSH with streaming output. Delegates to shared helper."""
        assert self.ssh_key_path is not None
        return await run_ssh_streaming(self.ssh_key_path, hostname, command, user=user, extra_opts=_VM_SSH_EXTRA_OPTS)

    async def _execute_agent(self, ctx: AgentContext, agent_env: Environment, hostname: str) -> None:
        """Execute the agent on the VM."""
        assert self.ssh_key_path is not None

        # Ensure localhost resolves
        exit_code, stdout, stderr = await run_ssh(
            self.ssh_key_path,
            hostname,
            "grep -q localhost /etc/hosts && echo 'ALREADY_EXISTS' || (echo '127.0.0.1 localhost' >> /etc/hosts && echo 'ADDED')",
            timeout=10,
            extra_opts=_VM_SSH_EXTRA_OPTS,
        )
        result = stdout.strip()
        if result == "ADDED":
            logger.debug(f"Added localhost to /etc/hosts on {hostname}")
        else:
            logger.debug(f"localhost already in /etc/hosts on {hostname}")

        # Best-effort ownership normalization so files created by root during
        # world hooks remain writable by the non-root agent user.
        await self._ensure_workspace_writable(hostname)

        # Build environment variables
        env_vars = [
            f"AGENT_CONFIG_B64={ctx.config_b64}",
            f"JOB_ID={agent_env.job_id}",
        ]
        if ctx.runtime_b64:
            env_vars.append(f"AGENT_RUNTIME_B64={ctx.runtime_b64}")

        logger.info(f"Agent config keys: {list(ctx.config.keys())}")
        logger.info("Executing agent command on VM via SSH as root...")

        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("agent.execution.output") as span:
            span.set_attribute("agent.user", "root")
            span.set_attribute("agent.hostname", hostname)

            # Capture OTel context inside the span so the agent VM
            # nests its spans under agent.execution.output
            otel = OTelContext.from_env()
            env_vars.extend(otel.to_env_vars())
            logger.info(f"OTEL URL: {otel.otel_url}")

            env_exports = " ".join(f'export {k}="{v}";' for var in env_vars for k, v in [var.split("=", 1)])
            workdir = self.workspace.agent_mount_path if self.workspace else "/workspace"
            agent_cmd = (
                f'{env_exports} cd {workdir} && plato-agent-runner run --instruction-b64 "{ctx.instruction_b64}"'
            )

            exit_code = await run_ssh_streaming(
                self.ssh_key_path,
                hostname,
                agent_cmd,
                user="root",
                extra_opts=_VM_SSH_EXTRA_OPTS,
            )

        logger.info(f"Agent command completed with exit code: {exit_code}")

        if exit_code != 0:
            raise RuntimeError(f"Agent failed with exit code {exit_code}")

    async def _ensure_workspace_writable(self, hostname: str) -> None:
        """No-op — ownership is fixed locally on the world VM before NFS export."""
        pass
