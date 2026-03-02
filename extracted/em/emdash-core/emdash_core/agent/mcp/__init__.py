"""MCP (Model Context Protocol) integration for dynamic tool loading.

This module provides:
- MCPServerManager: Manages lifecycle of MCP servers
- GenericMCPClient: Client for communicating with MCP servers
- MCPConfigFile: Configuration loading/saving
- Tool factory functions for creating tools from MCP servers
"""

from .config import (
    MCPServerConfig,
    MCPConfigFile,
    get_default_mcp_config_path,
    ensure_mcp_config,
    get_default_mcp_servers,
    get_open_agent_mcp_servers,
    get_document_mcp_servers,
    get_productivity_mcp_servers,
    get_coworker_mcp_servers,
)
from .client import (
    GenericMCPClient,
    MCPToolInfo,
    MCPResponse,
    MCPError,
)
from .manager import (
    MCPServerManager,
    get_mcp_manager,
    reset_mcp_manager,
)
from .tool_factory import (
    MCPDynamicTool,
    create_tools_from_mcp,
)

__all__ = [
    # Config
    "MCPServerConfig",
    "MCPConfigFile",
    "get_default_mcp_config_path",
    "ensure_mcp_config",
    "get_default_mcp_servers",
    "get_open_agent_mcp_servers",
    "get_document_mcp_servers",
    "get_productivity_mcp_servers",
    "get_coworker_mcp_servers",
    # Client
    "GenericMCPClient",
    "MCPToolInfo",
    "MCPResponse",
    "MCPError",
    # Manager
    "MCPServerManager",
    "get_mcp_manager",
    "reset_mcp_manager",
    # Tool factory
    "MCPDynamicTool",
    "create_tools_from_mcp",
]
