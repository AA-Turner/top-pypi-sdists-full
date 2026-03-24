"""VM runtime for agent execution in Firecracker VMs."""

from __future__ import annotations

import asyncio
import logging
import os
import re
import threading
import time as _time
import uuid
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

import tenacity
from opentelemetry import trace
from pydantic import BaseModel

from plato.agents.runtime.base import AgentContext, OTelContext, PreparedAgent, Runtime
from plato.agents.runtime.dev import _find_agent_code, install_production_agent, sync_dev_code
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


def _make_agent_alias(display_name: str | None) -> str:
    """Build a readable unique alias for an agent VM."""
    suffix = uuid.uuid4().hex[:8]
    if not display_name:
        return f"agent-{suffix}"

    slug = re.sub(r"[^a-z0-9]+", "-", display_name.lower()).strip("-")
    slug = slug[:40].strip("-") or "agent"
    return f"{slug}-{suffix}"


def _retry_agent_alias(base_alias: str, retry_attempt: int) -> str:
    if retry_attempt <= 0:
        return base_alias
    return f"{base_alias}-retry-{retry_attempt}"


def _is_duplicate_alias_error(exc: BaseException) -> bool:
    return "Duplicate alias" in str(exc)


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
        self._prepare_lock = asyncio.Lock()
        self.last_execution_span_id: str = ""  # hex span ID of latest agent.execution.output span
        # Process-wide lock guard for VM prepare lifecycle. This prevents
        # concurrent VM bring-up storms across different AgentRunner instances.
        # It is initialized lazily per event loop via _get_global_prepare_lock().

    _global_prepare_lock: ClassVar[asyncio.Lock | None] = None
    _global_prepare_lock_loop_id: ClassVar[int | None] = None
    _global_prepare_lock_guard: ClassVar[threading.Lock] = threading.Lock()

    @classmethod
    def _get_global_prepare_lock(cls) -> asyncio.Lock:
        loop = asyncio.get_running_loop()
        loop_id = id(loop)
        with cls._global_prepare_lock_guard:
            if cls._global_prepare_lock is None or cls._global_prepare_lock_loop_id != loop_id:
                cls._global_prepare_lock = asyncio.Lock()
                cls._global_prepare_lock_loop_id = loop_id
            return cls._global_prepare_lock

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
        global_prepare_lock = self._get_global_prepare_lock()
        last_exc: Exception | None = None
        base_alias = _make_agent_alias(ctx.display_name)

        for alias_attempt in range(3):
            agent_alias = _retry_agent_alias(base_alias, alias_attempt)
            try:
                logger.info("Waiting for global VM prepare lock: %s", agent_alias)
                async with global_prepare_lock:
                    logger.info("Acquired global VM prepare lock: %s", agent_alias)
                    async with self._prepare_lock:
                        agent_env = await self._create_vm(ctx.image, agent_alias)
                        self._agent_envs[agent_alias] = agent_env

                        logger.info(f"Setting up network for {agent_alias}")
                        await self._setup_network()

                        logger.info(f"Getting mesh IP for {agent_alias}")
                        mesh_ip = await agent_env.get_mesh_ip()
                        if not mesh_ip:
                            raise RuntimeError(f"Failed to get mesh IP for agent VM {agent_alias}")
                        logger.info(f"Mesh IP for {agent_alias}: {mesh_ip}")

                        logger.info(f"Syncing code to {agent_alias}")
                        await self._sync_code(ctx, agent_env, mesh_ip)
                        logger.info(f"Code synced to {agent_alias}")

                        # Inject PLATO_API_KEY into the VM so it's available during
                        # on_prepare hooks and agent execution.
                        plato_api_key = os.environ.get("PLATO_API_KEY", "")
                        if plato_api_key:
                            await self._run_ssh_streaming(
                                mesh_ip,
                                f'echo "PLATO_API_KEY={plato_api_key}" >> /etc/environment',
                            )
                    logger.info("Released global VM prepare lock: %s", agent_alias)
            except Exception as exc:
                last_exc = exc
                await self.cleanup(agent_alias, error=True)
                if _is_duplicate_alias_error(exc) and alias_attempt < 2:
                    logger.warning(
                        "Agent alias collision during VM prepare (%s). Retrying with alias %s.",
                        agent_alias,
                        _retry_agent_alias(base_alias, alias_attempt + 1),
                    )
                    continue
                raise

            return PreparedAgent(
                agent_id=agent_alias,
                hostname=mesh_ip,
                runtime=self,
            )

        assert last_exc is not None
        raise last_exc

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

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=10, min=10, max=60),
        before_sleep=tenacity.before_sleep_log(logger, logging.WARNING),
        retry=tenacity.retry_if_exception(lambda exc: not _is_duplicate_alias_error(exc)),
        reraise=True,
    )
    async def _create_vm(self, image: str, alias: str) -> Environment:
        """Create an agent VM with retry and exponential backoff."""
        logger.info(
            "Creating agent VM: %s (image: %s, cpus=%d, mem=%dMB)",
            alias,
            image,
            self.vm_config.cpus,
            self.vm_config.memory,
        )
        t0 = _time.monotonic()
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
        logger.info("Agent VM ready: %s (took %.1fs)", agent_env.job_id, _time.monotonic() - t0)
        return agent_env

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=10, min=10, max=60),
        before_sleep=tenacity.before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    async def _setup_network(self) -> None:
        """Setup network connectivity to agent VM with retry."""
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
        package_name, version = self._parse_image_url(ctx.image)
        if Path("/sdk").exists() and _find_agent_code(ctx.agent_code_path, package_name) is not None:
            synced_agent_code = await sync_dev_code(self.ssh_key_path, hostname, ctx.agent_code_path, package_name)
            if not synced_agent_code:
                logger.info(
                    "Falling back to production agent install for %s==%s (no synced dev agent code found).",
                    package_name,
                    version,
                )
                await install_production_agent(self.ssh_key_path, hostname, package_name, version)
        else:
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
        if ctx.display_name:
            env_vars.append(f"PLATO_AGENT_DISPLAY_NAME={ctx.display_name}")
        if ctx.runtime_b64:
            env_vars.append(f"AGENT_RUNTIME_B64={ctx.runtime_b64}")
        plato_api_key = os.environ.get("PLATO_API_KEY", "")
        if plato_api_key:
            env_vars.append(f"PLATO_API_KEY={plato_api_key}")

        logger.info(f"Agent config keys: {list(ctx.config.keys())}")
        logger.info("Executing agent command on VM via SSH as root...")

        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("agent.execution.output") as span:
            # Capture span ID so callers can link to this span in the trajectory viewer
            span_ctx = span.get_span_context()
            if span_ctx.is_valid:
                self.last_execution_span_id = format(span_ctx.span_id, "016x")

            if ctx.display_name:
                span.set_attribute("atif.agent.name", ctx.display_name)
                span.set_attribute("plato.agent.display_name", ctx.display_name)
            span.set_attribute("plato.agent.alias", agent_env.alias or "")
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
                f'{env_exports} export PATH="/root/.local/bin:$PATH"; '
                f'cd {workdir} && plato-agent-runner run --instruction-b64 "{ctx.instruction_b64}"'
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
