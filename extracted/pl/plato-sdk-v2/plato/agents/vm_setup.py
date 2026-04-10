"""Stateless SSH helper functions for agent VM setup and execution.

These functions operate on a RuntimeInfo object and perform agent-specific
setup via SSH: code installation, environment configuration, workspace
mounting, and agent execution.
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
import shlex
import time as _time
import uuid
from pathlib import Path
from typing import TYPE_CHECKING

import tomllib
from opentelemetry import trace

from plato.agents.context import AgentContext, OTelContext
from plato.agents.dev import sync_dev_code
from plato.agents.install import install_production_agent
from plato.agents.mounts import AgentWorkspaceMount
from plato.cli.chronos.registry import parse_image_url, parse_package_string
from plato.runtimes.base import RuntimeInfo, VMMetadata
from plato.utils.subprocess import (
    VM_PATH_EXPORT,
    build_ssh_command,
    run_local,
    run_ssh,
    run_ssh_streaming,
)

if TYPE_CHECKING:
    from plato.v2.async_.session import Session

logger = logging.getLogger(__name__)

_VM_SSH_EXTRA_OPTS: list[tuple[str, str]] = [
    ("ServerAliveInterval", "30"),
    ("ServerAliveCountMax", "3"),
]


def _world_runtime_ip_from_info(world_runtime_info: RuntimeInfo | None) -> str | None:
    """Return the world VM hostname/IP from runtime info when available."""
    if world_runtime_info is None:
        return None

    if isinstance(world_runtime_info.metadata, VMMetadata) and world_runtime_info.metadata.hostname:
        return world_runtime_info.metadata.hostname
    return world_runtime_info.hostname or None


async def _resolve_world_runtime_ip(
    session: Session | None,
    world_runtime_info: RuntimeInfo | None = None,
) -> str | None:
    """Return the world VM mesh IP used for ``runtime.plato.internal``."""
    runtime_ip = _world_runtime_ip_from_info(world_runtime_info)
    if runtime_ip:
        return runtime_ip

    if session is None:
        return None

    for env in session.envs:
        if env.alias != "runtime":
            continue
        return env.mesh_ip or await env.get_mesh_ip()
    return None


def _sdk_declares_agent(package_name: str, sdk_root: Path = Path("/sdk")) -> bool:
    """Check if the SDK pyproject.toml registers an agent entry point for this package.

    In dev mode the SDK may declare the agent directly, so we skip PyPI install
    and use the synced source instead.
    """
    pyproject_path = sdk_root / "pyproject.toml"
    if not pyproject_path.exists():
        return False

    with pyproject_path.open("rb") as handle:
        pyproject = tomllib.load(handle)

    project = pyproject.get("project", {})
    entry_points = project.get("entry-points", {})
    agents = entry_points.get("plato.agents", {})
    return isinstance(agents, dict) and package_name in agents


def make_agent_alias(display_name: str | None) -> str:
    """Build a readable unique alias for an agent VM."""
    suffix = uuid.uuid4().hex[:8]
    if not display_name:
        return f"agent-{suffix}"

    slug = re.sub(r"[^a-z0-9]+", "-", display_name.lower()).strip("-")
    slug = slug[:40].strip("-") or "agent"
    return f"{slug}-{suffix}"


async def install_agent_code(
    info: RuntimeInfo,
    ctx: AgentContext,
) -> None:
    """Install agent code on a VM (dev sync or production install)."""
    ssh_key = info.ssh_key_path
    if not ssh_key:
        raise RuntimeError("ssh_key_path required for code sync")
    hostname = info.hostname

    package_ref = ctx.package or ""
    package_name: str
    version: str | None
    if package_ref:
        package_name, version = parse_package_string(package_ref)
    else:
        package_name, version = parse_image_url(ctx.image)

    if Path("/sdk").exists():
        sdk_declares_agent = bool(package_ref and _sdk_declares_agent(package_name))
        synced_agent_code = await sync_dev_code(
            ssh_key,
            hostname,
            ctx.agent_code_path,
            None if sdk_declares_agent and ctx.agent_code_path is None else package_name,
            None if sdk_declares_agent and ctx.agent_code_path is None else version,
        )
        if not synced_agent_code:
            if sdk_declares_agent:
                logger.info("Using SDK-provided agent %s on %s", package_name, hostname)
                return
            logger.info(
                "Falling back to production agent install for %s==%s",
                package_name,
                version,
            )
            await install_production_agent(
                ssh_key,
                hostname,
                package_name,
                version,
                upgrade_sdk=False,
            )
        return
    await install_production_agent(ssh_key, hostname, package_name, version)


async def setup_agent_env(
    info: RuntimeInfo,
    session: Session | None = None,
    world_runtime_info: RuntimeInfo | None = None,
) -> None:
    """Write /etc/hosts and /etc/environment on the agent VM."""
    ssh_key = info.ssh_key_path
    if not ssh_key:
        return
    hostname = info.hostname

    env_cmds: list[str] = []

    # Map runtime.plato.internal → world VM mesh IP in /etc/hosts
    if session is not None or world_runtime_info is not None:
        world_ip = await _resolve_world_runtime_ip(session, world_runtime_info)
        if not world_ip:
            raise RuntimeError("Could not resolve world runtime mesh IP for runtime.plato.internal")
        env_cmds.append(
            f"sed -i '/runtime\\.plato\\.internal/d' /etc/hosts && "
            f'echo "{world_ip} runtime.plato.internal" >> /etc/hosts'
        )

    plato_api_key = os.environ.get("PLATO_API_KEY", "")
    if plato_api_key:
        env_cmds.append(f'echo "PLATO_API_KEY={plato_api_key}" >> /etc/environment')

    if env_cmds:
        await run_ssh_streaming(ssh_key, hostname, " && ".join(env_cmds), user="root", extra_opts=_VM_SSH_EXTRA_OPTS)


async def resolve_runner_path(info: RuntimeInfo) -> str:
    """Resolve the absolute path for plato-agent-runner on a remote VM."""
    ssh_key = info.ssh_key_path
    if not ssh_key:
        raise RuntimeError("ssh_key_path required to resolve runner path")
    hostname = info.hostname
    exit_code, stdout, stderr = await run_ssh(
        ssh_key,
        hostname,
        f"{VM_PATH_EXPORT}; "
        'runner_path="$(command -v plato-agent-runner || true)"; '
        'if [ -n "$runner_path" ] && [ -x "$runner_path" ]; then printf "%s\\n" "$runner_path"; '
        'else echo "plato-agent-runner not found" >&2; exit 1; fi',
        user="root",
        timeout=30,
        extra_opts=_VM_SSH_EXTRA_OPTS,
    )
    if exit_code != 0:
        raise RuntimeError(f"Failed to resolve plato-agent-runner on {hostname}: {stderr.strip() or stdout.strip()}")
    runner_path = stdout.strip()
    if not runner_path.startswith("/"):
        raise RuntimeError(f"Resolved plato-agent-runner path is not absolute on {hostname}: {runner_path}")
    return runner_path


async def setup_workspaces(info: RuntimeInfo, workspaces: list[AgentWorkspaceMount]) -> None:
    """Mount workspaces on the agent VM via transport.setup_agent()."""
    env = info.env
    hostname = info.hostname

    t0 = _time.monotonic()
    logger.info(
        "Setting up %d workspaces on %s: %s",
        len(workspaces),
        hostname,
        [(ws.transport_kind, ws.world_path, ws.agent_path) for ws in workspaces],
    )
    for ws in workspaces:
        ws_t0 = _time.monotonic()
        logger.info(
            "Starting setup_agent for workspace '%s' (transport=%s, mount=%s) on %s",
            ws.world_path,
            ws.transport_kind,
            ws.agent_path,
            hostname,
        )
        await ws.setup_agent(env, hostname)
        logger.info("Workspace '%s' setup_agent took %.1fs on %s", ws.world_path, _time.monotonic() - ws_t0, hostname)
    logger.info("All workspace setup_agent took %.1fs on %s", _time.monotonic() - t0, hostname)


async def sync_back_workspaces(info: RuntimeInfo, workspaces: list[AgentWorkspaceMount]) -> None:
    """Sync changes back from agent VM to world VM."""
    env = info.env
    hostname = info.hostname

    for ws in workspaces:
        logger.info("Syncing back workspace: %s", ws.world_path)
        await ws.sync_back(env, hostname)
    logger.info("All workspaces synced back")


async def execute_agent(
    info: RuntimeInfo,
    ctx: AgentContext,
    runner_path: str,
    workdir: str,
) -> str:
    """Execute the agent on a VM via SSH.

    Returns the hex span ID of the agent.execution.output span.
    """
    ssh_key = info.ssh_key_path
    if not ssh_key:
        raise RuntimeError("ssh_key_path required for agent execution")
    hostname = info.hostname

    job_id = info.metadata.job_id if isinstance(info.metadata, VMMetadata) else ""

    # Ensure localhost resolves
    exit_code, stdout, stderr = await run_ssh(
        ssh_key,
        hostname,
        "grep -q localhost /etc/hosts && echo 'ALREADY_EXISTS' || (echo '127.0.0.1 localhost' >> /etc/hosts && echo 'ADDED')",
        timeout=10,
        extra_opts=_VM_SSH_EXTRA_OPTS,
    )

    # Build environment variables
    env_vars = [
        f"AGENT_CONFIG_B64={ctx.config_b64}",
        f"JOB_ID={job_id}",
    ]
    if ctx.display_name:
        env_vars.append(f"PLATO_AGENT_DISPLAY_NAME={ctx.display_name}")
    if ctx.runtime_b64:
        env_vars.append(f"AGENT_RUNTIME_B64={ctx.runtime_b64}")
    plato_api_key = os.environ.get("PLATO_API_KEY", "")
    if plato_api_key:
        env_vars.append(f"PLATO_API_KEY={plato_api_key}")

    logger.info("Agent config keys: %s", list(ctx.config.keys()))
    logger.info("Executing agent command on VM via SSH as root...")

    last_execution_span_id = ""

    # Pipe instruction via stdin to avoid E2BIG
    instruction_file = "/tmp/.plato_instruction_b64"
    ssh_write_cmd = build_ssh_command(ssh_key, hostname, extra_opts=_VM_SSH_EXTRA_OPTS)
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

    # Pass only the package name (without version) to the agent runner
    agent_name = parse_package_string(ctx.package)[0] if ctx.package else ""
    package_arg = f" --agent-package {shlex.quote(agent_name)}" if agent_name else ""

    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("agent.execution.ssh") as ssh_span:
        span_ctx = ssh_span.get_span_context()
        if span_ctx.is_valid:
            last_execution_span_id = format(span_ctx.span_id, "016x")
        ssh_span.set_attribute("plato.agent.alias", info.metadata.alias)
        ssh_span.set_attribute("agent.hostname", hostname)
        if ctx.display_name:
            ssh_span.set_attribute("plato.agent.display_name", ctx.display_name)

        # Capture OTel context INSIDE the ssh span so the remote agent's
        # spans nest under agent.execution.ssh, not agent.task.
        otel = OTelContext.from_env()
        otel_env_vars = otel.to_env_vars()
        logger.info("OTEL URL: %s", otel.otel_url)

        all_env_vars = env_vars + otel_env_vars
        env_exports = " ".join(f'export {k}="{v}";' for var in all_env_vars for k, v in [var.split("=", 1)])
        agent_cmd = (
            f"{env_exports} {VM_PATH_EXPORT}; "
            f'cd {workdir} && {shlex.quote(runner_path)} run{package_arg} --instruction-b64 "$(cat {instruction_file})"'
        )

        exit_code = await run_ssh_streaming(
            ssh_key,
            hostname,
            agent_cmd,
            user="root",
            extra_opts=_VM_SSH_EXTRA_OPTS,
        )

        if exit_code == 255:
            logger.warning("Agent SSH disconnected (exit 255) on %s, diagnosing...", hostname)
            await diagnose_agent_vm(info)

    logger.info("Agent command completed with exit code: %d", exit_code)

    if exit_code != 0:
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

    return last_execution_span_id


async def diagnose_agent_vm(info: RuntimeInfo) -> None:
    """Run diagnostics on an agent VM after SSH failure (best-effort)."""
    ssh_key = info.ssh_key_path
    if not ssh_key:
        return
    hostname = info.hostname

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
        rc, out, err = await run_ssh(ssh_key, hostname, "echo ok", timeout=10, extra_opts=_VM_SSH_EXTRA_OPTS)
        if rc != 0:
            logger.warning("Diagnose %s: SSH failed (rc=%d): %s", hostname, rc, err.strip())
            return

        # 3) Check dmesg for OOM killer, kernel panics
        rc, dmesg, _ = await run_ssh(
            ssh_key,
            hostname,
            "dmesg --level=err,crit,alert,emerg -T 2>/dev/null | tail -20 || dmesg | tail -20",
            timeout=10,
            extra_opts=_VM_SSH_EXTRA_OPTS,
        )
        if dmesg.strip():
            logger.info("Diagnose %s: dmesg:\n%s", hostname, dmesg.strip())

        # 4) Check if the agent process is still running
        rc, procs, _ = await run_ssh(
            ssh_key,
            hostname,
            "ps aux | grep -E 'plato-agent|python|node' | grep -v grep | head -10",
            timeout=10,
            extra_opts=_VM_SSH_EXTRA_OPTS,
        )
        logger.info("Diagnose %s: processes:\n%s", hostname, procs.strip() if procs.strip() else "(none)")

        # 5) Check memory
        rc, mem, _ = await run_ssh(
            ssh_key,
            hostname,
            "free -m | head -3",
            timeout=10,
            extra_opts=_VM_SSH_EXTRA_OPTS,
        )
        if mem.strip():
            logger.info("Diagnose %s: memory:\n%s", hostname, mem.strip())

    except Exception as e:
        logger.warning("Diagnose %s: diagnostics failed: %s", hostname, e)
