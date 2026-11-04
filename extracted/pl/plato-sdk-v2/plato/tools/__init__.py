"""World-hosted MCP tool definitions and server helpers.

Worlds define ``ToolDefinition`` objects and expose them through ``ToolServer``.
Agents connect to those world-hosted tools over MCP HTTP using ``write_mcp_config``.

Handlers should use ``get_workspace()`` for paths instead of closing over
absolute paths, since the workspace path differs between world and agent.
"""

from plato.tools.definition import ToolDefinition, get_workspace, set_workspace
from plato.tools.mcp import (
    EnvMcpUrl,
    McpRemoteServer,
    resolve_mcp_servers,
    resolve_mcp_url,
    write_mcp_config,
)
from plato.tools.request_context import ToolRequestContext, get_request_context
from plato.tools.server import ToolServer

__all__ = [
    "ToolDefinition",
    "ToolServer",
    "ToolRequestContext",
    "get_request_context",
    "get_workspace",
    "set_workspace",
    "write_mcp_config",
    "EnvMcpUrl",
    "McpRemoteServer",
    "resolve_mcp_url",
    "resolve_mcp_servers",
]
