"""Tiny client-flow wire contract helpers shared by delivery paths."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from runlayer_cli import __version__
from runlayer_cli.command_contract import detect_os, detect_source

CLIENT_FLOWS_SCHEMA_VERSION = 1
MAX_FLOWS_PER_ENVELOPE = 10
MAX_STEPS_PER_FLOW = 50

CLIENT_FLOW_OPERATIONS: frozenset[str] = frozenset(
    {
        "cli.call_tool",
        "cli.list_tools",
        "cli.sync_capabilities",
        "cli.hook_pre_tool",
        "cli.hook_post_tool",
        "cli.hook_stop",
        "cli.hook_event",
    }
)
CLIENT_FLOW_STEPS: frozenset[str] = frozenset(
    {
        "pre",
        "upstream",
        "post",
        "introspect",
        "upload",
        "credentials",
        "policy_check",
        "enforce",
        "tool_pre",
        "tool_post",
        "event_post",
        "transcript_read",
        "device_context",
        "daemon_ipc",
        "daemon_fallback",
        "credential_rejected_cached",
        "host_override",
        "harness_closed",
        "harness_departed",
    }
)
# Closed vocabulary for the sanitized failure classification on errored flows.
# Derived client-side by classifying the caught exception (see
# ``error_classification.py`` — OUTSIDE this stdlib-only closure because it
# needs httpx/mcp types); the backend rejects anything not in this set. Only
# the category (plus an optional integer HTTP status) crosses the wire —
# never exception messages, URLs, or response bodies.
CLIENT_FLOW_ERROR_CATEGORIES: frozenset[str] = frozenset(
    {
        "dns",
        "connect",
        "connect_timeout",
        "timeout",
        "tls",
        "http_401",
        "http_403",
        "http_404",
        "http_4xx",
        "http_5xx",
        "oauth_registration_rejected",
        "oauth_flow_timeout",
        "oauth_callback_port_in_use",
        "oauth_callback_listener",
        "oauth_flow_error",
        "mcp_protocol",
        "cancelled",
        "other",
    }
)

# Detected harness a hook flow ran under (``hook.clients.Client`` values).
# Duplicated rather than imported: ``clients.py`` drags the response-shaping
# machinery into this stdlib-only closure. ``tests/test_flow_contract.py``
# pins the copy to the enum.
CLIENT_FLOW_CLIENTS: frozenset[str] = frozenset(
    {
        "unknown",
        "cursor",
        "vscode",
        "claude_code",
        "codex",
        "hermes",
        "goose",
        "github-copilot-cli",
        "windsurf",
        "qwen-code",
        "gemini-cli",
        "grok-cli",
        "cline-cli",
        "devin-cli",
    }
)
# Normalized hook event names a hook flow may report: every
# ``EVENT_NORMALIZE`` target, every ``_DISPATCH_TABLE`` key, and the
# PascalCase / camelCase observational names the installers register that
# ``normalize_event_name`` passes through verbatim. Anything else collapses
# to "other" before it enters a summary so the wire vocabulary stays bounded
# (the backend drops values outside this set).
CLIENT_FLOW_HOOK_EVENTS: frozenset[str] = frozenset(
    {
        "PreToolUse",
        "PostToolUse",
        "PostToolUseFailure",
        "PermissionRequest",
        "PermissionDenied",
        "UserPromptSubmit",
        "Stop",
        "SessionStart",
        "SessionEnd",
        "SubagentStart",
        "SubagentStop",
        "PreCompact",
        "PostCompact",
        "Notification",
        "ErrorOccurred",
        "BeforeReadFile",
        "AfterReadFile",
        "AfterFileEdit",
        "BeforeShellExecution",
        "AfterShellExecution",
        "WorktreeCreate",
        "TeammateIdle",
        "TaskCompleted",
        "ConfigChange",
        "InstructionsLoaded",
        "beforeMCPExecution",
        "afterMCPExecution",
        "beforeReadFile",
        "afterFileEdit",
        "beforeShellExecution",
        "afterShellExecution",
        "afterAgentThought",
        "afterAgentResponse",
        "beforeTabFileRead",
        "other",
    }
)


def build_envelope(flows: list[dict[str, Any]], dropped: int) -> dict[str, Any]:
    """Wire envelope attached to existing request bodies as ``client_flows``.

    Carries ``os`` + ``source`` so the backend can re-record hook flows as
    ``runlayer.cli.command.*`` metrics (see ``client_flow_ingest``) with the same
    OS / binary attribution as directly-reported commands.
    """
    return {
        "v": CLIENT_FLOWS_SCHEMA_VERSION,
        "cli_version": __version__,
        "os": detect_os(),
        "source": detect_source(),
        "flows": flows,
        "dropped": dropped,
    }


def attach_client_flows(
    body: dict[str, Any],
    drain: Callable[[], dict[str, Any] | None] | None,
) -> dict[str, Any]:
    """Return ``body`` with queued client-flow summaries attached when present."""
    if drain is None or "client_flows" in body:
        return body

    try:
        client_flows = drain()
    except Exception:
        return body

    if client_flows is None:
        return body
    return {**body, "client_flows": client_flows}
