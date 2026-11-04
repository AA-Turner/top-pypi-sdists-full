# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.mcp_update_params."""

from __future__ import annotations

from typing_extensions import TypedDict
from .._types import SequenceNotStr


class McpUpdateParams(TypedDict, total=False):
    name: str
    "Human-readable name to identify this MCP server instance (4-30 characters,\nalphanumeric, spaces, and hyphens only)"
    toolkits: SequenceNotStr[str]
    "List of toolkit slugs this server should be configured to work with."
    allowed_tools: SequenceNotStr[str]
    "List of action identifiers that should be enabled for this server"
    managed_auth_via_composio: bool
    "Whether the MCP server is managed by Composio"
    auth_config_ids: SequenceNotStr[str]
    "List of auth config IDs to use for this MCP server."


__all__ = [
    "McpUpdateParams",
]
