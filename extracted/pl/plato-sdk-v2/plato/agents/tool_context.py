"""Tool execution context setup on the agent VM."""

from __future__ import annotations

import json
import logging
import os

from opentelemetry import trace

from plato.runtimes.base import RuntimeInfo
from plato.utils.subprocess import run_ssh
from plato.utils.tool_execution import DEFAULT_TOOL_EXECUTION_CONTEXT_PATH, ToolExecutionContext

logger = logging.getLogger(__name__)

# Under fork-burst pressure (many agent VMs set up at once) a 10s SSH round-trip
# times out; a timeout still raises, just later.
_SSH_TIMEOUT_S = 60


def default_agent_name(agent_image: str) -> str:
    return agent_image.split("/")[-1].split(":")[0]


def build_tool_execution_context_payload(
    info: RuntimeInfo,
    *,
    agent_image: str,
    default_display_name: str | None,
    display_name: str | None,
) -> ToolExecutionContext:
    ctx = trace.get_current_span().get_span_context()
    agent_name = display_name or default_display_name or default_agent_name(agent_image)
    return ToolExecutionContext(
        session_id=os.environ.get("SESSION_ID", ""),
        agent_id=info.runtime_id,
        agent_name=agent_name,
        display_name=display_name or default_display_name or agent_name,
        trace_id=format(ctx.trace_id, "032x") if ctx.is_valid else "",
        span_id=format(ctx.span_id, "016x") if ctx.is_valid else "",
    )


async def write_tool_execution_context(
    info: RuntimeInfo,
    *,
    agent_image: str,
    default_display_name: str | None,
    display_name: str | None,
    watch_paths: list[str],
    file_trigger_patterns: list[str] | None,
    trigger_server_url: str | None,
) -> None:
    """Write tool execution context and optional file watcher config to the agent VM.

    Raises on failure: tool hooks parent their spans from this context, and a
    configured file watcher is what fires file-triggered checkpoints.
    """
    ssh_key = info.ssh_key_path
    if not ssh_key:
        return

    tool_context_json = build_tool_execution_context_payload(
        info,
        agent_image=agent_image,
        default_display_name=default_display_name,
        display_name=display_name,
    ).model_dump_json()
    exit_code, _, stderr = await run_ssh(
        ssh_key,
        info.hostname,
        f"cat > {DEFAULT_TOOL_EXECUTION_CONTEXT_PATH} << 'TOOL_EOF'\n{tool_context_json}\nTOOL_EOF",
        timeout=_SSH_TIMEOUT_S,
    )
    if exit_code != 0:
        raise RuntimeError(f"Failed to write tool execution context on {info.hostname}: {stderr.strip()}")
    logger.debug("Wrote tool execution context to agent VM")

    if not (file_trigger_patterns and trigger_server_url and watch_paths):
        return

    watcher_config = json.dumps(
        {
            "server_url": trigger_server_url,
            "patterns": file_trigger_patterns,
            "watch_paths": watch_paths,
            "poll_interval_s": 2.0,
        }
    )
    exit_code, _, stderr = await run_ssh(
        ssh_key,
        info.hostname,
        (
            f"cat > /tmp/plato-file-watcher-config.json << 'WATCHER_EOF'\n"
            f"{watcher_config}\n"
            "WATCHER_EOF\n"
            "nohup python3 -m plato.utils.file_watcher "
            "/tmp/plato-file-watcher-config.json "
            "> /tmp/plato-file-watcher.log 2>&1 &\n"
            "echo $! > /tmp/plato-file-watcher.pid"
        ),
        timeout=_SSH_TIMEOUT_S,
    )
    if exit_code != 0:
        raise RuntimeError(f"Failed to start file watcher sidecar on {info.hostname}: {stderr.strip()}")
    logger.info(
        "Started file watcher sidecar on %s (patterns=%s, server=%s)",
        info.hostname,
        file_trigger_patterns,
        trigger_server_url,
    )
