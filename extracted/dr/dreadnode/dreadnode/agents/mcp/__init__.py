"""
MCP (Model Context Protocol) client and server utilities.

Provides:
- MCPClient: Connect to MCP servers (stdio, streamable-http)
- mcp(): Factory function for creating clients
- as_mcp(): Serve tools as an MCP server
- FileTokenStorage: Persistent OAuth token storage
- Server config types aligned with the capability spec
"""

from dreadnode.agents.mcp.client import MCPClient, mcp
from dreadnode.agents.mcp.config import (
    DEFAULT_HTTP_TIMEOUT,
    DEFAULT_INIT_TIMEOUT,
    DEFAULT_SSE_READ_TIMEOUT,
    INITIALIZE_TIMEOUT,
    HttpServerConfig,
    MCPStatus,
    OAuthConfig,
    ServerConfig,
    SSEConnection,
    StdioConnection,
    StdioServerConfig,
    Transport,
)
from dreadnode.agents.mcp.server import as_mcp

__all__ = [
    "DEFAULT_HTTP_TIMEOUT",
    "DEFAULT_INIT_TIMEOUT",
    "DEFAULT_SSE_READ_TIMEOUT",
    "INITIALIZE_TIMEOUT",
    "FileTokenStorage",
    "HttpServerConfig",
    "MCPClient",
    "MCPStatus",
    "OAuthConfig",
    "SSEConnection",
    "ServerConfig",
    "StdioConnection",
    "StdioServerConfig",
    "Transport",
    "as_mcp",
    "create_oauth_provider",
    "mcp",
]


def __getattr__(name: str) -> object:
    """Lazy import for optional components."""
    if name == "FileTokenStorage":
        from dreadnode.agents.mcp.auth import FileTokenStorage

        return FileTokenStorage
    if name == "create_oauth_provider":
        from dreadnode.agents.mcp.auth import create_oauth_provider

        return create_oauth_provider
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
