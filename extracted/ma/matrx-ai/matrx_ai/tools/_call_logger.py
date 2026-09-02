"""Centralized tool-call log writer.

Every tool call's full result — inputs, stdout, stderr, exit code, all
metadata — gets saved to a markdown file the agent can read back later.
The LLM's context still gets the truncated summary, but the file path
appears in that summary so the agent (or a future context-demoter, or
a summarization sub-agent) can fetch the full body on demand.

This is the foundation for "complete tool-call audit trail" — wired
into shell_execute and shell_python today, extended to fs_* / db_* /
ctx_* in follow-up commits with a one-line call from each tool.

Path layout
-----------

    ~/.matrx/runtime/tool-calls/<conversation_id>/<unix_ts>-<tool>-<short_call_id>.md

When ``conversation_id`` is unavailable (rare — batch flows), falls back
to ``_unscoped/``. Files are markdown with YAML frontmatter so the agent
can ``fs_read`` them as documents, and a future context-demoter can
parse the frontmatter to render compact "tool call X happened at Y"
summaries without re-loading bodies.

Frontmatter convention
----------------------

::

    ---
    tool: shell_execute
    call_id: toolu_01MCfbw4u7SeKA9k4mzYo1fU
    message_id: 35bc5701-...
    conversation_id: 048fbfcf-...
    user_id: 4cf62e4e-...
    sandbox_id: sbx-abc123
    timestamp: 2026-04-29T18:42:13.123Z
    unix_ts: 1730000000
    duration_ms: 1234
    success: true
    exit_code: 0
    inputs:
      command: |
        find / -name '*.py' | head -100
      working_dir: /home/agent
      timeout_seconds: 60
    output_summary:
      stdout_bytes: 215000
      stderr_bytes: 0
      truncated_in_response: true
    ---

    ## stdout

    ```
    <full stdout>
    ```

    ## stderr

    ```
    <full stderr>
    ```

Routing
-------

- Sandbox-bound (matrx-ai on aidream's host, request bound to a sandbox):
  writes via the orchestrator's ``/fs/write`` proxy into the container.
- Sandbox-mode (matrx-ai running INSIDE a sandbox via ``mtx aidream serve``):
  writes directly to the local filesystem.
- Multi-tenant aidream (no sandbox): no-op — multi-tenant agents don't
  have a coherent long-lived workspace anyway. Tools still work; their
  results just aren't archived to disk.

Errors during the log write are caught and logged but never propagated —
the agent's tool result must not depend on logging succeeding.
"""

from __future__ import annotations

import json
import logging
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from matrx_ai.tools._sandbox_proxy import (
    SandboxProxyError,
    fs_write as _proxy_fs_write,
    get_active_sandbox,
)
from matrx_ai.tools._sandbox_runtime import sandbox_mode_active

logger = logging.getLogger(__name__)

# Where logs go inside the sandbox/agent home. Resolves to
# /home/agent/.matrx/runtime/tool-calls/<conv>/<file>.md.
_AGENT_HOME = "/home/agent"
_TOOL_CALL_SUBDIR = ".matrx/runtime/tool-calls"


def _short_call_id(call_id: str) -> str:
    """Last 8 chars of the call id — enough to disambiguate within a
    conversation, short enough to fit in the filename's display.
    """
    if not call_id:
        return "anonymous"
    # Strip provider prefixes like ``toolu_`` / ``call_`` for readability.
    cleaned = re.sub(r"^(toolu_|call_)", "", call_id)
    return cleaned[-8:] if len(cleaned) > 8 else cleaned


def _safe_segment(value: str | None, default: str) -> str:
    """Sanitize a string for use as a path segment — strip path separators
    and other characters that would let a malicious value escape the
    intended directory.
    """
    if not value:
        return default
    cleaned = re.sub(r"[^a-zA-Z0-9_\-]", "_", value)
    return cleaned[:64] or default


def _yaml_scalar(value: Any) -> str:
    """Render a value as a YAML scalar. Strings with special chars get
    block-style; everything else is JSON (which is a YAML subset).
    """
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return json.dumps(value)
    if isinstance(value, str):
        if "\n" in value or len(value) > 80 or any(c in value for c in ":#\"'"):
            indented = "\n".join("    " + line for line in value.splitlines())
            return f"|\n{indented}"
        return json.dumps(value)
    # Fallback — JSON-encode complex types
    return json.dumps(value)


def _format_inputs(inputs: dict[str, Any]) -> str:
    if not inputs:
        return "  {}"
    lines: list[str] = []
    for k, v in inputs.items():
        rendered = _yaml_scalar(v)
        if rendered.startswith("|\n"):
            lines.append(f"  {k}: {rendered}")
        else:
            lines.append(f"  {k}: {rendered}")
    return "\n".join(lines)


def _build_frontmatter_lines(
    *,
    tool: str,
    call_id: str,
    message_id: str | None,
    conversation_id: str | None,
    user_id: str | None,
    sandbox_id: str | None,
    duration_ms: int,
    success: bool,
    exit_code: int | None,
    inputs: dict[str, Any],
    extra_summary: dict[str, Any] | None = None,
) -> list[str]:
    """Common frontmatter shared by ``write_tool_call_log`` and
    ``write_action_log`` so the on-disk format is identical for shell-style
    tools and service actions (cloud_sync, fs writes, etc.)."""
    now = datetime.now(timezone.utc)
    iso = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    unix_ts = int(now.timestamp())

    lines = [
        "---",
        f"tool: {tool}",
        f"call_id: {json.dumps(call_id or '')}",
        f"message_id: {json.dumps(message_id or '')}",
        f"conversation_id: {json.dumps(conversation_id or '')}",
        f"user_id: {json.dumps(user_id or '')}",
        f"sandbox_id: {json.dumps(sandbox_id or '')}",
        f"timestamp: {iso}",
        f"unix_ts: {unix_ts}",
        f"duration_ms: {duration_ms}",
        f"success: {'true' if success else 'false'}",
    ]
    if exit_code is not None:
        lines.append(f"exit_code: {exit_code}")
    lines.append("inputs:")
    lines.append(_format_inputs(inputs))
    if extra_summary:
        lines.append("output_summary:")
        for k, v in extra_summary.items():
            lines.append(f"  {k}: {_yaml_scalar(v)}")
    lines.append("---")
    return lines


def _build_log_body(
    *,
    tool: str,
    call_id: str,
    message_id: str | None,
    conversation_id: str | None,
    user_id: str | None,
    sandbox_id: str | None,
    duration_ms: int,
    success: bool,
    exit_code: int | None,
    inputs: dict[str, Any],
    stdout: str,
    stderr: str,
    output_truncated_in_response: bool,
) -> str:
    """Shell-tool body — frontmatter + ``## stdout`` / ``## stderr`` blocks."""
    frontmatter = _build_frontmatter_lines(
        tool=tool,
        call_id=call_id,
        message_id=message_id,
        conversation_id=conversation_id,
        user_id=user_id,
        sandbox_id=sandbox_id,
        duration_ms=duration_ms,
        success=success,
        exit_code=exit_code,
        inputs=inputs,
        extra_summary={
            "stdout_bytes": len(stdout.encode("utf-8")),
            "stderr_bytes": len(stderr.encode("utf-8")),
            "truncated_in_response": output_truncated_in_response,
        },
    )

    body_parts = ["\n".join(frontmatter), ""]
    body_parts.append("## stdout\n")
    body_parts.append("```")
    body_parts.append(stdout if stdout else "(empty)")
    body_parts.append("```\n")
    body_parts.append("## stderr\n")
    body_parts.append("```")
    body_parts.append(stderr if stderr else "(empty)")
    body_parts.append("```\n")
    return "\n".join(body_parts)


def _build_action_body(
    *,
    tool: str,
    call_id: str,
    message_id: str | None,
    conversation_id: str | None,
    user_id: str | None,
    sandbox_id: str | None,
    duration_ms: int,
    success: bool,
    inputs: dict[str, Any],
    result: dict[str, Any] | None,
    error: str | None,
) -> str:
    """Generic action body — same frontmatter, but the body holds a JSON
    ``## result`` block instead of stdout/stderr. Used by service actions
    (cloud_sync uploads, fs operations, db writes) where there's no
    captured shell output to surface.
    """
    extra: dict[str, Any] = {}
    if result and isinstance(result, dict):
        # Surface a few easy-to-scan fields in the frontmatter so the
        # context-demoter can reason about magnitude without reading the body.
        for k in ("path", "bytes", "version", "status"):
            if k in result:
                extra[k] = result[k]
    frontmatter = _build_frontmatter_lines(
        tool=tool,
        call_id=call_id,
        message_id=message_id,
        conversation_id=conversation_id,
        user_id=user_id,
        sandbox_id=sandbox_id,
        duration_ms=duration_ms,
        success=success,
        exit_code=None,
        inputs=inputs,
        extra_summary=extra or None,
    )

    body_parts = ["\n".join(frontmatter), ""]
    if result is not None:
        body_parts.append("## result\n")
        body_parts.append("```json")
        body_parts.append(json.dumps(result, indent=2, default=str))
        body_parts.append("```\n")
    if error:
        body_parts.append("## error\n")
        body_parts.append("```")
        body_parts.append(error)
        body_parts.append("```\n")
    return "\n".join(body_parts)


def _resolve_log_path(*, conversation_id: str | None, tool: str, call_id: str, unix_ts: int) -> tuple[str, str]:
    """Return (absolute_path_on_fs, agent_facing_path_string).

    The agent-facing path uses ``~/`` so it reads naturally in the
    truncated message; the absolute path is what the writer actually uses.
    """
    conv_segment = _safe_segment(conversation_id, "_unscoped")
    tool_segment = _safe_segment(tool, "tool")
    short_id = _short_call_id(call_id)
    filename = f"{unix_ts}-{tool_segment}-{short_id}.md"
    relative = f"{_TOOL_CALL_SUBDIR}/{conv_segment}/{filename}"
    abs_path = f"{_AGENT_HOME}/{relative}"
    agent_path = f"~/{relative}"
    return abs_path, agent_path


async def write_tool_call_log(
    *,
    tool: str,
    call_id: str,
    inputs: dict[str, Any],
    stdout: str = "",
    stderr: str = "",
    success: bool,
    exit_code: int | None = None,
    duration_ms: int = 0,
    message_id: str | None = None,
    conversation_id: str | None = None,
    user_id: str | None = None,
    output_truncated_in_response: bool = False,
) -> str | None:
    """Write a per-call log file. Returns the agent-facing path (``~/...``)
    on success, or ``None`` if logging was a no-op (multi-tenant aidream)
    or failed silently. Never raises.

    Routing decision happens here based on AppContext / runtime mode.
    """
    binding = get_active_sandbox()
    in_sandbox_mode = sandbox_mode_active()

    if binding is None and not in_sandbox_mode:
        # Multi-tenant aidream — no coherent long-lived workspace to log to.
        # Logs would scatter across /tmp/workspaces/<uid>/<pid>/ with no UI
        # to read them. Skip cleanly.
        return None

    unix_ts = int(time.time())
    abs_path, agent_path = _resolve_log_path(
        conversation_id=conversation_id,
        tool=tool,
        call_id=call_id,
        unix_ts=unix_ts,
    )

    sandbox_id = binding.sandbox_id if binding else None
    body = _build_log_body(
        tool=tool,
        call_id=call_id,
        message_id=message_id,
        conversation_id=conversation_id,
        user_id=user_id,
        sandbox_id=sandbox_id,
        duration_ms=duration_ms,
        success=success,
        exit_code=exit_code,
        inputs=inputs,
        stdout=stdout,
        stderr=stderr,
        output_truncated_in_response=output_truncated_in_response,
    )

    try:
        if binding is not None:
            await _proxy_fs_write(
                binding,
                abs_path,
                body,
                encoding="utf8",
                create_parents=True,
            )
        else:
            # sandbox-mode: write locally
            p = Path(abs_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body, encoding="utf-8")
    except SandboxProxyError as exc:
        logger.warning("tool-call log write failed (proxy): %s", exc)
        return None
    except Exception as exc:
        logger.warning("tool-call log write failed: %s", exc)
        return None

    return agent_path


async def write_action_log(
    *,
    tool: str,
    inputs: dict[str, Any],
    result: dict[str, Any] | None = None,
    success: bool = True,
    error: str | None = None,
    duration_ms: int = 0,
    call_id: str = "",
    message_id: str | None = None,
    conversation_id: str | None = None,
    user_id: str | None = None,
) -> str | None:
    """General-purpose action log — for tools whose result isn't shell
    stdout/stderr. Same on-disk path + frontmatter shape as
    ``write_tool_call_log``; the body contains a ``## result`` JSON block
    plus an optional ``## error`` block instead of stdout/stderr.

    Used (or callable) by:
      - matrx-ai's fs_*/db_*/ctx_* tools when extended (today they don't log).
      - The matrx_agent service inside the sandbox, via a sibling helper
        in ``sandbox-image/sdk/matrx_agent/audit.py`` that mirrors this
        function's contract for actions originating inside the container.

    Routing is identical to ``write_tool_call_log`` — sandbox-bound writes
    via the proxy, sandbox-mode writes locally, multi-tenant skips. Errors
    in the log path are caught and never propagated.
    """
    binding = get_active_sandbox()
    in_sandbox_mode = sandbox_mode_active()
    if binding is None and not in_sandbox_mode:
        return None

    unix_ts = int(time.time())
    abs_path, agent_path = _resolve_log_path(
        conversation_id=conversation_id,
        tool=tool,
        call_id=call_id,
        unix_ts=unix_ts,
    )

    sandbox_id = binding.sandbox_id if binding else None
    body = _build_action_body(
        tool=tool,
        call_id=call_id,
        message_id=message_id,
        conversation_id=conversation_id,
        user_id=user_id,
        sandbox_id=sandbox_id,
        duration_ms=duration_ms,
        success=success,
        inputs=inputs,
        result=result,
        error=error,
    )

    try:
        if binding is not None:
            await _proxy_fs_write(
                binding,
                abs_path,
                body,
                encoding="utf8",
                create_parents=True,
            )
        else:
            p = Path(abs_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body, encoding="utf-8")
    except SandboxProxyError as exc:
        logger.warning("action log write failed (proxy): %s", exc)
        return None
    except Exception as exc:
        logger.warning("action log write failed: %s", exc)
        return None

    return agent_path


__all__ = ["write_tool_call_log", "write_action_log"]
