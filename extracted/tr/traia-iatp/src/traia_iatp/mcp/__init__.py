"""MCP (Model Context Protocol) integration module with lazy imports."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import MCPClient
    from .mcp_agent_template import MCPServerConfig, MCPAgentBuilder, run_with_mcp_tools, MCPServerInfo
    from .traia_mcp_adapter import TraiaMCPAdapter, create_mcp_adapter
    from .d402_mcp_tool_adapter import D402MCPToolAdapter, create_d402_mcp_adapter
    from .mcp_server_template_generator import MCPServerTemplateGenerator, LocalMCPServerConfig

_LAZY_IMPORTS = {
    "MCPClient": ".client",
    "MCPServerConfig": ".mcp_agent_template",
    "MCPAgentBuilder": ".mcp_agent_template",
    "run_with_mcp_tools": ".mcp_agent_template",
    "MCPServerInfo": ".mcp_agent_template",
    "TraiaMCPAdapter": ".traia_mcp_adapter",
    "create_mcp_adapter": ".traia_mcp_adapter",
    "D402MCPToolAdapter": ".d402_mcp_tool_adapter",
    "create_d402_mcp_adapter": ".d402_mcp_tool_adapter",
    "MCPServerTemplateGenerator": ".mcp_server_template_generator",
    "LocalMCPServerConfig": ".mcp_server_template_generator",
}

__all__ = list(_LAZY_IMPORTS.keys())


def __getattr__(name: str):
    if name in _LAZY_IMPORTS:
        from importlib import import_module

        module = import_module(_LAZY_IMPORTS[name], package=__package__)
        attr = getattr(module, name)
        globals()[name] = attr
        return attr

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
