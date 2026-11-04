# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.mcp.custom_create_response."""

from __future__ import annotations

from pydantic import ConfigDict
from ..._base_model import BaseModel


class Commands(BaseModel):
    "Set of command line instructions for connecting various clients to this MCP server"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    claude: str
    "Command line instruction for Claude client setup"
    cursor: str
    "Command line instruction for Cursor client setup"
    windsurf: str
    "Command line instruction for Windsurf client setup"


class CustomCreateResponse(BaseModel):
    "Response for a successfully created custom MCP server with multiple applications"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    allowed_tools: list[str]
    "List of tool identifiers that are enabled for this server"
    auth_config_ids: list[str]
    "ID references to the auth configurations used by this server"
    commands: Commands
    "Set of command line instructions for connecting various clients to this MCP\nserver"
    id: str
    "Unique identifier for the newly created custom MCP server"
    mcp_url: str
    "URL endpoint for establishing connection to this MCP server"
    name: str
    "Human-readable name of the custom MCP server"


__all__ = [
    "CustomCreateResponse",
    "Commands",
]
