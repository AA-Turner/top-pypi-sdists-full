"""
MCP configuration types and status tracking.

Server config types aligned with the capability spec's MCP server definition
(contract.md § MCP Server Definition). Transport is inferred from config type:
StdioServerConfig → stdio, HttpServerConfig → streamable-http.
"""

import typing as t
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

import typing_extensions as te

DEFAULT_INIT_TIMEOUT = 30
"""Timeout (seconds) for MCP session init + tool discovery."""

INITIALIZE_TIMEOUT = DEFAULT_INIT_TIMEOUT
"""Deprecated: use DEFAULT_INIT_TIMEOUT."""

DEFAULT_HTTP_TIMEOUT = 30
DEFAULT_SSE_READ_TIMEOUT = 60 * 5

Transport = t.Literal["stdio", "streamable-http"]


class MCPStatus(StrEnum):
    """Status of an MCP server connection."""

    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    FAILED = "failed"
    NEEDS_AUTH = "needs_auth"
    DISABLED = "disabled"


@dataclass
class OAuthConfig:
    """OAuth configuration for remote MCP servers.

    Supports dynamic client registration via the MCP SDK's OAuthClientProvider.
    Pre-registered client credentials (client_id/client_secret) will be added
    when the OAuth callback server lands (Layer 3).
    """

    client_name: str = "dreadnode"
    scope: str | None = None


@dataclass
class StdioServerConfig:
    """Config for stdio MCP servers (capability spec: command → stdio)."""

    command: str
    args: list[str] = field(default_factory=list)
    env: dict[str, str] | None = None
    cwd: str | Path | None = None
    init_timeout: float = DEFAULT_INIT_TIMEOUT


@dataclass
class HttpServerConfig:
    """Config for remote MCP servers (capability spec: url → streamable-http)."""

    url: str
    headers: dict[str, str] | None = None
    oauth: OAuthConfig | None = None
    timeout: float = DEFAULT_HTTP_TIMEOUT
    sse_read_timeout: float = DEFAULT_SSE_READ_TIMEOUT
    init_timeout: float = DEFAULT_INIT_TIMEOUT


ServerConfig = StdioServerConfig | HttpServerConfig


# --- Backward-compat TypedDicts (deprecated) ---


class StdioConnection(te.TypedDict):
    """Deprecated: Use StdioServerConfig instead."""

    command: str
    args: list[str]
    cwd: str | Path | None
    env: dict[str, str] | None


class SSEConnection(te.TypedDict):
    """Deprecated: Use HttpServerConfig instead."""

    url: str
    headers: dict[str, t.Any] | None
    timeout: float
    sse_read_timeout: float
