"""Canonical package for SDK MCP support capabilities."""

from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "ConnectorMcpAdapter",
    "ConnectorMcpConfig",
    "ConnectorMcpDirectTransport",
    "ConnectorMcpSdkTransport",
    "ConnectorMcpTransport",
    "HttpMcpAdapter",
    "HttpMcpConfig",
    "McpCallToolContext",
    "McpConfigBase",
    "McpPort",
    "StdioMcpAdapter",
    "StdioMcpConfig",
    "mcp_call_tool",
]

if TYPE_CHECKING:
    from mistralai.vibe.sdk.capabilities.mcp.adapters.connector_mcp import (
        ConnectorMcpAdapter,
    )
    from mistralai.vibe.sdk.capabilities.mcp.adapters.http_mcp import (
        HttpMcpAdapter,
    )
    from mistralai.vibe.sdk.capabilities.mcp.adapters.stdio_mcp import (
        StdioMcpAdapter,
    )
    from mistralai.vibe.sdk.capabilities.mcp.call_tool import (
        McpCallToolContext,
        mcp_call_tool,
    )
    from mistralai.vibe.sdk.capabilities.mcp.config import (
        ConnectorMcpConfig,
        ConnectorMcpDirectTransport,
        ConnectorMcpSdkTransport,
        ConnectorMcpTransport,
        HttpMcpConfig,
        McpConfigBase,
        StdioMcpConfig,
    )
    from mistralai.vibe.sdk.capabilities.mcp.port import (
        McpPort,
    )

_LAZY_EXPORTS = {
    "ConnectorMcpAdapter": "mistralai.vibe.sdk.capabilities.mcp.adapters.connector_mcp",
    "HttpMcpAdapter": "mistralai.vibe.sdk.capabilities.mcp.adapters.http_mcp",
    "StdioMcpAdapter": "mistralai.vibe.sdk.capabilities.mcp.adapters.stdio_mcp",
    "McpCallToolContext": "mistralai.vibe.sdk.capabilities.mcp.call_tool",
    "mcp_call_tool": "mistralai.vibe.sdk.capabilities.mcp.call_tool",
    "ConnectorMcpConfig": "mistralai.vibe.sdk.capabilities.mcp.config",
    "ConnectorMcpDirectTransport": "mistralai.vibe.sdk.capabilities.mcp.config",
    "ConnectorMcpSdkTransport": "mistralai.vibe.sdk.capabilities.mcp.config",
    "ConnectorMcpTransport": "mistralai.vibe.sdk.capabilities.mcp.config",
    "HttpMcpConfig": "mistralai.vibe.sdk.capabilities.mcp.config",
    "McpConfigBase": "mistralai.vibe.sdk.capabilities.mcp.config",
    "StdioMcpConfig": "mistralai.vibe.sdk.capabilities.mcp.config",
    "McpPort": "mistralai.vibe.sdk.capabilities.mcp.port",
}


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    value = getattr(import_module(_LAZY_EXPORTS[name]), name)
    globals()[name] = value
    return value
