# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.mcp_list_response."""

from __future__ import annotations

from typing import Dict

from pydantic import ConfigDict
from .._base_model import BaseModel


class ItemCommands(BaseModel):
    "Set of command line instructions for connecting various clients to this MCP server"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    claude: str
    "Command line instruction for Claude client setup"
    cursor: str
    "Command line instruction for Cursor client setup"
    windsurf: str
    "Command line instruction for Windsurf client setup"


class Item(BaseModel):
    "MCP server configuration and connection details"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    allowed_tools: list[str]
    "Array of tool slugs that this MCP server is allowed to use"
    auth_config_ids: list[str]
    "ID references to the auth configurations used by this server"
    commands: ItemCommands
    "Set of command line instructions for connecting various clients to this MCP\nserver"
    created_at: str
    "Date and time when this server was initially created"
    id: str
    "UUID of the MCP server instance"
    managed_auth_via_composio: bool
    "Whether the MCP server is managed by Composio"
    mcp_url: str
    "[DEPRECATED] Please use the URL with user_id or connected_account_id query param"
    name: str
    "User-defined descriptive name for this MCP server"
    server_instance_count: float
    "Total count of active user instances connected to this server"
    toolkit_icons: Dict[str, str]
    "Object mapping each toolkit slug to its icon/logo URL for display purposes"
    toolkits: list[str]
    "Array of toolkit slugs that this MCP server is allowed to use"
    updated_at: str
    "Date and time when this server configuration was last modified"


class McpListResponse(BaseModel):
    "Paginated response containing MCP servers"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    current_page: float
    "Current page number being returned"
    items: list[Item]
    "Array of MCP server configurations"
    total_pages: float
    "Total number of pages in the paginated response"


__all__ = [
    "McpListResponse",
    "Item",
    "ItemCommands",
]
