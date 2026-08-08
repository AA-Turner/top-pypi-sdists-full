"""Stateless SSH helper functions for agent VM setup and execution.

These functions operate on a RuntimeInfo object and perform agent-specific
setup via SSH: code installation, environment configuration, workspace
mounting, and agent execution.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import os
import re
import shlex
import time as _time
import tomllib
import uuid
from pathlib import Path
from typing import TYPE_CHECKING

from opentelemetry import trace

from plato.agents.context import AgentContext, OTelContext
from plato.agents.dev import sync_dev_code
from plato.agents.install import install_production_agent
from plato.agents.mounts import AgentWorkspaceMount
from plato.cli.chronos.registry import parse_image_url, parse_package_string
from plato.rpc.client.connection import AgentDaemonClient
from plato.rpc.client.fallback import rpc_or_ssh
from plato.rpc.client.stubs import AgentJobStub, EnvStub, ExecStub, FilesStub, HealthStub
from plato.rpc.errors import AgentJobRecordLostError, AgentUnreachableError
from plato.rpc.models.env import EnvSetupRequest, HostsEntry
from plato.rpc.models.exec_ import ExecRunRequest
from plato.rpc.models.job import AgentJobStartRequest
from plato.rpc.protocol import CAP_AGENT_JOB_START, CAP_ENV_SETUP, CAP_EXEC_RUN
from plato.runtimes.base import RuntimeInfo, VMMetadata
from plato.utils.subprocess import (
    VM_PATH_EXPORT,
    run_local,
    run_ssh,
    run_ssh_streaming,
    scp_content_to_vm,
)

if TYPE_CHECKING:
    from plato.v2.async_.session import Session

logger = logging.getLogger(__name__)

_VM_SSH_EXTRA_OPTS: list[tuple[str, str]] = [
    ("ServerAliveInterval", "30"),
    ("ServerAliveCountMax", "3"),
]

# signal.SIGTERM without importing signal at every call site.
_SIGTERM = 15

# Per-stream cap on the spool tail logged when an agent job fails. The SSH
# path logged the full merged output block; this bounds it deliberately.
_AGENT_FAIL_TAIL_BYTES = 65_536


async def _run_probe_ssh(
    ssh_key: Path,
    hostname: str,
    command: str,
    *,
    timeout: int,
    attempts: int,
    extra_opts: list[tuple[str, str]] | None = None,
) -> tuple[int, str, str]:
    """Run a short SSH probe with bounded retries for transient connection churn."""
    last_error: BaseException | None = None
    last_result: tuple[int, str, str] | None = None
    safe_attempts = max(1, attempts)
    for attempt in range(1, safe_attempts + 1):
        try:
            result = await run_ssh(
                ssh_key,
                hostname,
                command,
                timeout=timeout,
                extra_opts=extra_opts,
            )
            if result[0] == 0:
                return result
            last_result = result
        except Exception as exc:
            last_error = exc
            if attempt >= safe_attempts:
                raise
        if attempt >= safe_attempts:
            break
        delay = min(float(2 ** (attempt - 1)), 5.0)
        reason = str(last_error) if last_error else f"exit {last_result[0]}" if last_result is not None else "unknown"
        logger.warning(
            "SSH probe failed on %s (attempt %d/%d), retrying in %.1fs: %s",
            hostname,
            attempt,
            safe_attempts,
            delay,
            reason,
        )
        await asyncio.sleep(delay)

    if last_result is not None:
        exit_code, stdout, stderr = last_result
        raise RuntimeError(
            f"SSH probe failed after {safe_attempts} attempt(s): "
            f"exit={exit_code}, stdout={stdout or '<empty>'}, stderr={stderr or '<empty>'}"
        )
    assert last_error is not None
    raise last_error


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


def make_agent_pool_prefix(package: str | None, image: str | None, config: dict | None) -> str:
    """Readable alias prefix for a warm pool's VMs: ``<harness>-<model>``.

    Warm pools are per agent profile, so the harness package and model are
    known at pool construction even though the individual agent run isn't.
    Naming pooled VMs after the profile makes them identifiable in the
    Chronos session env list instead of the opaque ``warm-pool-<hex>``.
    """
    harness = ""
    if package:
        harness, _ = parse_package_string(package)
    elif image:
        harness, _ = parse_image_url(image)
    harness = harness or "agent"
    model = ""
    if config:
        model = str(config.get("model_name") or config.get("model") or "")
    return f"{harness}-{model}" if model else harness


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
    """Write /etc/hosts and /etc/environment on the agent VM.

    RPC path (env service) writes /etc/environment as a marker-delimited
    managed block (idempotent upsert) instead of appending, which stops the
    PLATO_API_KEY line accumulating across warm-pool reuse. SSH fallback is the
    original append-based body, unchanged.
    """
    ssh_key = info.ssh_key_path
    if not ssh_key:
        return
    hostname = info.hostname

    hosts: list[HostsEntry] = []
    world_ip: str | None = None
    if session is not None or world_runtime_info is not None:
        world_ip = await _resolve_world_runtime_ip(session, world_runtime_info)
        if not world_ip:
            raise RuntimeError("Could not resolve world runtime mesh IP for runtime.plato.internal")
        hosts.append(HostsEntry(hostname="runtime.plato.internal", ip=world_ip))

    plato_api_key = os.environ.get("PLATO_API_KEY", "")
    env_vars = {"PLATO_API_KEY": plato_api_key} if plato_api_key else {}

    if not hosts and not env_vars:
        return

    async def _rpc(client: AgentDaemonClient) -> None:
        await EnvStub(client).setup(EnvSetupRequest(hosts=hosts, env_vars=env_vars))

    async def _ssh() -> None:
        env_cmds: list[str] = []
        if world_ip:
            env_cmds.append(
                f"sed -i '/runtime\\.plato\\.internal/d' /etc/hosts && "
                f'echo "{world_ip} runtime.plato.internal" >> /etc/hosts'
            )
        if plato_api_key:
            env_cmds.append(f'echo "PLATO_API_KEY={plato_api_key}" >> /etc/environment')
        if env_cmds:
            await run_ssh_streaming(
                ssh_key, hostname, " && ".join(env_cmds), user="root", extra_opts=_VM_SSH_EXTRA_OPTS
            )

    await rpc_or_ssh(hostname, ssh_key, CAP_ENV_SETUP, _rpc, _ssh)


async def resolve_runner_path(info: RuntimeInfo) -> str:
    """Resolve the absolute path for plato-agent-runner on a remote VM."""
    ssh_key = info.ssh_key_path
    if not ssh_key:
        raise RuntimeError("ssh_key_path required to resolve runner path")
    hostname = info.hostname
    command = (
        f"{VM_PATH_EXPORT}; "
        'runner_path="$(command -v plato-agent-runner || true)"; '
        'if [ -n "$runner_path" ] && [ -x "$runner_path" ]; then printf "%s\\n" "$runner_path"; '
        'else echo "plato-agent-runner not found" >&2; exit 1; fi'
    )

    async def _rpc(client: AgentDaemonClient) -> tuple[int, str, str]:
        resp = await ExecStub(client).run(ExecRunRequest(shell=command, timeout_s=30))
        return resp.rc, resp.stdout, resp.stderr

    async def _ssh() -> tuple[int, str, str]:
        return await run_ssh(ssh_key, hostname, command, user="root", timeout=30, extra_opts=_VM_SSH_EXTRA_OPTS)

    exit_code, stdout, stderr = await rpc_or_ssh(hostname, ssh_key, CAP_EXEC_RUN, _rpc, _ssh)
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
    """Execute the agent on a VM.

    RPC path (job service) runs the agent as a daemon-supervised job whose
    lifetime is decoupled from the connection — a network blip no longer looks
    like a crash (the exit-255 fix). SSH fallback is the original
    session-lifetime ``run_ssh_streaming`` body, unchanged.

    Returns the hex span ID of the agent execution span (consumed by
    ``plato/workflows/backend.py`` via ``runner.last_execution_span_id``) — the
    contract is preserved on both paths.
    """
    ssh_key = info.ssh_key_path
    if not ssh_key:
        raise RuntimeError("ssh_key_path required for agent execution")
    hostname = info.hostname

    async def _rpc(client: AgentDaemonClient) -> str:
        return await _execute_agent_rpc(client, info, ctx, runner_path, workdir)

    async def _ssh() -> str:
        return await _execute_agent_ssh(info, ctx, runner_path, workdir)

    return await rpc_or_ssh(hostname, ssh_key, CAP_AGENT_JOB_START, _rpc, _ssh)


async def _execute_agent_rpc(
    client: AgentDaemonClient,
    info: RuntimeInfo,
    ctx: AgentContext,
    runner_path: str,
    workdir: str,
) -> str:
    """Run the agent as a supervised daemon job. Instruction goes via the files
    service (no ARG_MAX games), env via the job spec (no shell export file), and
    the run survives connection drops."""
    hostname = info.hostname
    job_metadata_id = info.metadata.job_id if isinstance(info.metadata, VMMetadata) else ""

    # Ensure localhost resolves (env service upsert; idempotent).
    await EnvStub(client).setup(EnvSetupRequest(hosts=[HostsEntry(hostname="localhost", ip="127.0.0.1")]))

    # Deliver the (potentially large) instruction as a file, not an argument.
    instruction_file = "/tmp/.plato_instruction_b64"  # noqa: S108 - matches runner contract
    await FilesStub(client).push(instruction_file, ctx.instruction_b64.encode())

    env: dict[str, str] = {
        "AGENT_CONFIG_B64": ctx.config_b64,
        "JOB_ID": job_metadata_id,
    }
    if ctx.display_name:
        env["PLATO_AGENT_DISPLAY_NAME"] = ctx.display_name
    if ctx.runtime_b64:
        env["AGENT_RUNTIME_B64"] = ctx.runtime_b64
    plato_api_key = os.environ.get("PLATO_API_KEY", "")
    if plato_api_key:
        env["PLATO_API_KEY"] = plato_api_key

    agent_name = parse_package_string(ctx.package)[0] if ctx.package else ""
    argv = [runner_path, ctx.command]
    if agent_name:
        argv += ["--agent-package", agent_name]
    argv += ["--instruction-file", instruction_file]

    last_execution_span_id = ""
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("agent.execution.rpc") as span:
        span_ctx = span.get_span_context()
        if span_ctx.is_valid:
            last_execution_span_id = format(span_ctx.span_id, "016x")
        span.set_attribute("plato.agent.alias", info.metadata.alias)
        span.set_attribute("agent.hostname", hostname)
        if ctx.display_name:
            span.set_attribute("plato.agent.display_name", ctx.display_name)

        # Capture OTel context INSIDE the span so the remote agent's spans nest
        # under this execution span (same nesting as the SSH path).
        otel = OTelContext.from_env()
        for var in otel.to_env_vars():
            key, _, value = var.partition("=")
            env[key] = value

        agent_job_id = f"agent-{uuid.uuid4().hex}"
        await AgentJobStub(client).start(
            AgentJobStartRequest(agent_job_id=agent_job_id, argv=argv, cwd=workdir, env=env)
        )
        try:
            status = await AgentJobStub(client).wait_for_exit(agent_job_id, poll_s=30.0)
        except asyncio.CancelledError:
            # Caller cancelled (continuation timeout, user abort, teardown):
            # stop the remote agent instead of orphaning it. ONE shielded
            # best-effort request — the daemon runs the TERM→grace→KILL
            # escalation server-side, so cancellation never blocks on the
            # grace window (and a dead daemon must not block it either).
            logger.warning(
                "Agent job %s on %s: caller cancelled — sent TERM with 5s KILL escalation",
                agent_job_id,
                hostname,
            )
            with contextlib.suppress(Exception):
                await asyncio.shield(
                    AgentJobStub(client).signal(agent_job_id, _SIGTERM, escalate_kill_after_s=5.0, deadline_s=5.0)
                )
            raise
        except AgentUnreachableError:
            # Daemon (or the whole VM) died mid-run and stayed down past the
            # retry budget — it cannot report on itself. SSH probes are the
            # surviving role of diagnose_agent_vm (ping, sshd, dmesg/OOM, ps,
            # free), exactly what the SSH path ran on exit-255.
            await diagnose_agent_vm(info)
            raise

    logger.info("Agent job %s finished: state=%s rc=%s", agent_job_id, status.state, status.rc)

    if status.state == "lost":
        # The daemon is reachable (it answered the wait) but the job's outcome
        # is gone — ask the daemon why before raising: dmesg err/crit is where
        # an OOM kill (the most common real cause behind the old exit-255)
        # shows up. Best-effort, parity with diagnose_agent_vm's SSH probes.
        try:
            report = await HealthStub(client).report()
            logger.error(
                "Agent job %s lost on %s: mem_available_kb=%s load_1m=%s dmesg err/crit tail:\n%s",
                agent_job_id,
                hostname,
                report.mem_available_kb,
                report.load_1m,
                "\n".join(report.dmesg_errors_tail[-20:]) or "(empty)",
            )
        except Exception:  # noqa: BLE001 - diagnostics only
            pass
        # Honest successor to exit-255: the daemon restarted and could not
        # determine the outcome. Retryable on a fresh VM (RetryableInfraError).
        raise AgentJobRecordLostError(f"Agent job outcome unknown on {hostname} (daemon lost the job)")
    if status.rc != 0:
        # Parity with the SSH path (run_ssh_streaming), which merged stderr
        # into stdout and logged the whole block on non-zero exit. stdout is
        # where the agent transcript/tool output goes — omitting it left
        # failures with no world-side record of what the agent actually did.
        # Deliberate divergence: SSH logged the block unbounded; each stream
        # is capped at the last _AGENT_FAIL_TAIL_BYTES here.
        for stream in ("stdout", "stderr"):
            try:
                tail = await FilesStub(client).pull_tail(
                    f"/var/lib/plato-agent/jobs/{agent_job_id}/{stream}.log", _AGENT_FAIL_TAIL_BYTES
                )
                if tail:
                    logger.error("Agent job %s %s tail:\n%s", agent_job_id, stream, tail.decode(errors="replace"))
            except Exception:  # noqa: BLE001 - diagnostics only
                pass
        raise RuntimeError(f"Agent failed with exit code {status.rc}")

    return last_execution_span_id


async def _execute_agent_ssh(
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
    exit_code, stdout, stderr = await _run_probe_ssh(
        ssh_key,
        hostname,
        "grep -q localhost /etc/hosts && echo 'ALREADY_EXISTS' || (echo '127.0.0.1 localhost' >> /etc/hosts && echo 'ADDED')",
        timeout=ctx.ssh_probe_timeout,
        attempts=ctx.ssh_probe_retries,
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

    # Write instruction and env vars to files on the VM via scp to
    # avoid E2BIG — the combined base64 payloads (config, instruction,
    # runtime) can easily exceed the kernel's ARG_MAX (~128KB).
    instruction_file = "/tmp/.plato_instruction_b64"
    env_file = "/tmp/.plato_agent_env"

    # Build env file content: export K="V" lines
    env_lines = [f'export {var.split("=", 1)[0]}="{var.split("=", 1)[1]}"' for var in env_vars]
    env_file_content = "\n".join(env_lines) + "\n"

    await asyncio.gather(
        scp_content_to_vm(
            ssh_key, hostname, instruction_file, ctx.instruction_b64.encode(), extra_opts=_VM_SSH_EXTRA_OPTS
        ),
        scp_content_to_vm(ssh_key, hostname, env_file, env_file_content.encode(), extra_opts=_VM_SSH_EXTRA_OPTS),
    )

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

        # OTel vars are small — safe to inline. Large vars (config,
        # runtime, API key) are in env_file, sourced at runtime.
        otel_exports = " ".join(f'export {k}="{v}";' for var in otel_env_vars for k, v in [var.split("=", 1)])
        agent_cmd = (
            f"source {env_file}; {otel_exports} {VM_PATH_EXPORT}; "
            f"cd {workdir} && {shlex.quote(runner_path)} {shlex.quote(ctx.command)}{package_arg} "
            f"--instruction-file {instruction_file}"
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
        rc, out, _ = await run_local(f"ping -c 3 -W 2 {hostname}", timeout=30)
        ping_ok = rc == 0
        ping_summary = out.strip().split("\n")[-1] if out else "no output"
        logger.info("Diagnose %s: ping %s — %s", hostname, "OK" if ping_ok else "FAILED", ping_summary)

        if not ping_ok:
            logger.warning("Diagnose %s: VM unreachable (ping failed)", hostname)
            return

        # 2) Can we SSH?
        rc, out, err = await run_ssh(ssh_key, hostname, "echo ok", timeout=30, extra_opts=_VM_SSH_EXTRA_OPTS)
        if rc != 0:
            logger.warning("Diagnose %s: SSH failed (rc=%d): %s", hostname, rc, err.strip())
            return

        # 3) Check dmesg for OOM killer, kernel panics
        rc, dmesg, _ = await run_ssh(
            ssh_key,
            hostname,
            "dmesg --level=err,crit,alert,emerg -T 2>/dev/null | tail -20 || dmesg | tail -20",
            timeout=30,
            extra_opts=_VM_SSH_EXTRA_OPTS,
        )
        if dmesg.strip():
            logger.info("Diagnose %s: dmesg:\n%s", hostname, dmesg.strip())

        # 4) Check if the agent process is still running
        rc, procs, _ = await run_ssh(
            ssh_key,
            hostname,
            "ps aux | grep -E 'plato-agent|python|node' | grep -v grep | head -10",
            timeout=30,
            extra_opts=_VM_SSH_EXTRA_OPTS,
        )
        logger.info("Diagnose %s: processes:\n%s", hostname, procs.strip() if procs.strip() else "(none)")

        # 5) Check memory
        rc, mem, _ = await run_ssh(
            ssh_key,
            hostname,
            "free -m | head -3",
            timeout=30,
            extra_opts=_VM_SSH_EXTRA_OPTS,
        )
        if mem.strip():
            logger.info("Diagnose %s: memory:\n%s", hostname, mem.strip())

    except Exception as e:
        logger.warning("Diagnose %s: diagnostics failed: %s", hostname, e)
