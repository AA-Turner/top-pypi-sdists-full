"""
MCP (Model Context Protocol) Integration for Aetheris (v3.0)

Provides integration with MCP servers for extended tool capabilities.
MCP is optional - if not available, Aetheris will work without it.
"""

from src.mcp.client import MCPClient, MCPConnectionError
from src.mcp.discovery import MCPDiscovery, MCPTool, MCPResource
from src.mcp.skill_bridge import MCPToolBridge

__all__ = [
    "MCPClient",
    "MCPConnectionError",
    "MCPDiscovery",
    "MCPTool",
    "MCPResource",
    "MCPToolBridge",
]
