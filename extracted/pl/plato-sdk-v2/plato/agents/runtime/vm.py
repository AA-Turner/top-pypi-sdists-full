"""VM runtime for agent execution in Firecracker VMs."""

from __future__ import annotations

import asyncio
import logging
import os
import re
import time as _time
import uuid
from pathlib import Path
from typing import TYPE_CHECKING

import tenacity
from opentelemetry import trace
from pydantic import BaseModel

from plato.agents.runtime.base import AgentContext, OTelContext, PreparedAgent, Runtime
from plato.agents.runtime.dev import _find_agent_code, install_production_agent, sync_dev_code
from plato.agents.runtime.transport import Transport
from plato.utils.subprocess import build_ssh_command, run_local, run_ssh, run_ssh_streaming
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
        self.last_execution_span_id: str = ""  # hex span ID of latest agent.execution.output span

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
        """Start agent VM with desktop/Chrome but without running the task.

        Network join is handled server-side: add_env registers the VM as a
        network member and wait_for_ready blocks until the VM is both RUNNING
        and network-joined. No client-side lock or explicit connect_network
        call is needed.
        """
        tracer = trace.get_tracer(__name__)
        last_exc: Exception | None = None
        base_alias = _make_agent_alias(ctx.display_name)

        for alias_attempt in range(3):
            agent_alias = _retry_agent_alias(base_alias, alias_attempt)
            try:
                t_total = _time.monotonic()

                with tracer.start_as_current_span("agent.prepare.create_vm") as span:
                    span.set_attribute("agent.alias", agent_alias)
                    agent_env = await self._create_vm(ctx.image, agent_alias)
                    self._agent_envs[agent_alias] = agent_env

                # mesh_ip is cached on the Environment from wait_for_ready
                mesh_ip = agent_env.mesh_ip or await agent_env.get_mesh_ip()
                if not mesh_ip:
                    raise RuntimeError(f"Failed to get mesh IP for agent VM {agent_alias}")
                logger.info("Mesh IP for %s: %s", agent_alias, mesh_ip)

                # Add SSH key to this specific agent VM (per-job, not session-wide)
                with tracer.start_as_current_span("agent.prepare.ssh_key"):
                    if self.ssh_key_path:
                        pub_key = Path(str(self.ssh_key_path) + ".pub").read_text().strip()
                        await agent_env.add_ssh_key(pub_key)

                # sync_code and env_setup run concurrently (both need SSH key ready)
                await asyncio.gather(
                    self._prepare_sync_code(tracer, ctx, agent_env, mesh_ip, agent_alias),
                    self._prepare_env_setup(tracer, mesh_ip),
                )

                logger.info(
                    "Agent VM %s ready: %.1fs total",
                    agent_alias,
                    _time.monotonic() - t_total,
                )
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

    async def _prepare_sync_code(
        self, tracer: trace.Tracer, ctx: AgentContext, agent_env: Environment, mesh_ip: str, alias: str
    ) -> None:
        with tracer.start_as_current_span("agent.prepare.sync_code"):
            logger.info("Syncing code to %s", alias)
            await self._sync_code(ctx, agent_env, mesh_ip)

    async def _prepare_env_setup(self, tracer: trace.Tracer, mesh_ip: str) -> None:
        with tracer.start_as_current_span("agent.prepare.env_setup"):
            env_cmds: list[str] = []

            # Map runtime.plato.internal → world VM mesh IP in /etc/hosts
            for env in self.session.envs:
                if env.alias == "runtime":
                    world_ip = env.mesh_ip or await env.get_mesh_ip()
                    if world_ip:
                        env_cmds.append(
                            f'grep -q "runtime.plato.internal" /etc/hosts '
                            f'|| echo "{world_ip} runtime.plato.internal" >> /etc/hosts'
                        )
                    break

            plato_api_key = os.environ.get("PLATO_API_KEY", "")
            if plato_api_key:
                env_cmds.append(f'echo "PLATO_API_KEY={plato_api_key}" >> /etc/environment')

            if env_cmds:
                await self._run_ssh_streaming(mesh_ip, " && ".join(env_cmds))

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

        # Create a short-lived marker span that the agent VM's spans will
        # reference as their parent.  This span ends immediately so it is
        # exported right away by the batch span processor.  Without this,
        # long-running agents whose SSH call is still in progress when traces
        # are collected appear "orphaned" because the wrapping span hasn't
        # been exported yet.
        agent_attrs = {
            "plato.agent.alias": agent_env.alias or "",
            "agent.user": "root",
            "agent.hostname": hostname,
        }
        if ctx.display_name:
            agent_attrs["atif.agent.name"] = ctx.display_name
            agent_attrs["plato.agent.display_name"] = ctx.display_name

        with tracer.start_as_current_span("agent.execution.output") as marker:
            for k, v in agent_attrs.items():
                marker.set_attribute(k, v)
            # Capture OTel context inside the marker span so the agent VM
            # nests its spans under agent.execution.output
            otel = OTelContext.from_env()
            env_vars.extend(otel.to_env_vars())
        # marker span is now ended and will be exported promptly

        logger.info(f"OTEL URL: {otel.otel_url}")

        env_exports = " ".join(f'export {k}="{v}";' for var in env_vars for k, v in [var.split("=", 1)])
        workdir = self.workspace.agent_mount_path if self.workspace else "/workspace"

        # Pipe instruction via stdin to avoid "Argument list too long"
        # (E2BIG) when the instruction is large.
        instruction_file = "/tmp/.plato_instruction_b64"
        ssh_write_cmd = build_ssh_command(self.ssh_key_path, hostname, extra_opts=_VM_SSH_EXTRA_OPTS)
        ssh_write_cmd.append(f"cat > {instruction_file}")
        proc = await asyncio.create_subprocess_exec(
            *ssh_write_cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, write_err = await asyncio.wait_for(
            proc.communicate(input=ctx.instruction_b64.encode()),
            timeout=30,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"Failed to write instruction file to VM: {write_err.decode()}")

        agent_cmd = (
            f'{env_exports} export PATH="/root/.local/bin:$PATH"; '
            f'cd {workdir} && plato-agent-runner run --instruction-b64 "$(cat {instruction_file})"'
        )

        # Long-lived span for tracking SSH execution duration — not the
        # parent of agent VM spans, so it can stay open without causing
        # orphaned spans in mid-session trace exports.
        with tracer.start_as_current_span("agent.execution.ssh") as ssh_span:
            for k, v in agent_attrs.items():
                ssh_span.set_attribute(k, v)
            exit_code = await run_ssh_streaming(
                self.ssh_key_path,
                hostname,
                agent_cmd,
                user="root",
                extra_opts=_VM_SSH_EXTRA_OPTS,
            )

            if exit_code == 255:
                # SSH disconnect — diagnose but don't retry automatically
                logger.warning("Agent SSH disconnected (exit 255) on %s, diagnosing...", hostname)
                await self._diagnose_agent_vm(hostname)

        logger.info(f"Agent command completed with exit code: {exit_code}")

        if exit_code != 0:
            # Exit code 126 = "cannot execute" — typically bash E2BIG
            # ("Argument list too long").  Log the full instruction so we
            # can diagnose what was too large.
            if exit_code == 126:
                logger.error(
                    "Agent failed with exit code 126 (Argument list too long). "
                    "instruction length=%d chars, instruction_b64 length=%d chars.\n"
                    "--- BEGIN INSTRUCTION ---\n%s\n--- END INSTRUCTION ---",
                    len(ctx.instruction),
                    len(ctx.instruction_b64),
                    ctx.instruction,
                )
            raise RuntimeError(f"Agent failed with exit code {exit_code}")

    async def _diagnose_agent_vm(self, hostname: str) -> None:
        """Run diagnostics on an agent VM after SSH failure (best-effort)."""
        try:
            # 1) Can we ping it?
            rc, out, _ = await run_local(f"ping -c 3 -W 2 {hostname}", timeout=10)
            ping_ok = rc == 0
            ping_summary = out.strip().split("\n")[-1] if out else "no output"
            logger.info("Diagnose %s: ping %s — %s", hostname, "OK" if ping_ok else "FAILED", ping_summary)

            if not ping_ok:
                logger.warning("Diagnose %s: VM unreachable (ping failed)", hostname)
                return

            # 2) Can we SSH?
            assert self.ssh_key_path is not None
            rc, out, err = await run_ssh(self.ssh_key_path, hostname, "echo ok", timeout=10)
            if rc != 0:
                logger.warning("Diagnose %s: SSH failed (rc=%d): %s", hostname, rc, err.strip())
                return

            # 3) Check dmesg for OOM killer, kernel panics
            rc, dmesg, _ = await run_ssh(
                self.ssh_key_path,
                hostname,
                "dmesg --level=err,crit,alert,emerg -T 2>/dev/null | tail -20 || dmesg | tail -20",
                timeout=10,
            )
            if dmesg.strip():
                logger.info("Diagnose %s: dmesg:\n%s", hostname, dmesg.strip())

            # 4) Check if the agent process is still running
            rc, procs, _ = await run_ssh(
                self.ssh_key_path,
                hostname,
                "ps aux | grep -E 'plato-agent|python|node' | grep -v grep | head -10",
                timeout=10,
            )
            logger.info("Diagnose %s: processes:\n%s", hostname, procs.strip() if procs.strip() else "(none)")

            # 5) Check memory
            rc, mem, _ = await run_ssh(
                self.ssh_key_path,
                hostname,
                "free -m | head -3",
                timeout=10,
            )
            if mem.strip():
                logger.info("Diagnose %s: memory:\n%s", hostname, mem.strip())

            # 6) Check network — can agent reach world?
            world_ip = self.workspace.world_vm_ip if self.workspace and hasattr(self.workspace, "world_vm_ip") else None
            if world_ip:
                rc, out, _ = await run_ssh(
                    self.ssh_key_path,
                    hostname,
                    f"ping -c 1 -W 2 {world_ip} && echo 'world reachable' || echo 'world UNREACHABLE'",
                    timeout=10,
                )
                logger.info("Diagnose %s: world connectivity: %s", hostname, out.strip().split("\n")[-1])

        except Exception as e:
            logger.warning("Diagnose %s: diagnostics failed: %s", hostname, e)

    async def _ensure_workspace_writable(self, hostname: str) -> None:
        """No-op — ownership is fixed locally on the world VM before NFS export."""
        pass
