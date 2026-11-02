"""Shared types and constants for direct Agent API transport."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

SDK_ENTRYPOINT = "sdk-python"
DEFAULT_MODEL = "claude-sonnet-4-5"
MAX_API_ROUND_TRIPS = 15
DEFAULT_TOOLS = [
    "read",
    "write",
    "edit",
    "bash",
    "bash_output",
    "kill_shell",
    "grep",
    "glob",
    "web_fetch",
    "web_search",
    "snowflake_sql_execute",
]


@dataclass
class _DirectConnection:
    agent_url: str
    rest_url: str
    token: str
    protocol: str = "https"
    is_local: bool = False
    user: str | None = None
    refresh: Callable[[str], None] | None = None
    close: Callable[[], None] | None = None


@dataclass
class _ToolUseData:
    id: str
    name: str
    input: dict[str, Any]
    type: str | None = None
    client_side_execute: bool | None = None
    permission: dict[str, list[str]] | None = None


@dataclass
class _ToolResultData:
    tool_use_id: str
    name: str
    content: str
    is_error: bool = False


@dataclass
class _StreamResponse:
    text: str
    thinking: str
    content: list[dict[str, Any]]
    tool_uses: list[_ToolUseData]
    tool_results: list[_ToolResultData]
    usage: dict[str, int]
    metadata: list[dict[str, str]]
    raw_body: str | None = None
    partial_events: list[dict[str, Any]] | None = None


@dataclass
class _PendingToolUse:
    id: str
    name: str
    input: dict[str, Any]
    type: str | None = None
    client_side_execute: bool | None = None
    permission: dict[str, list[str]] | None = None


@dataclass
class _HttpResponse:
    status: int
    reason: str
    body: str
