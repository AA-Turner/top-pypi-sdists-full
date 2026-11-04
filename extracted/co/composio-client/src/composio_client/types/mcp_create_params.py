# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.mcp_create_params."""

from __future__ import annotations

from typing_extensions import Required, TypedDict
from .._types import SequenceNotStr


class McpCreateParams(TypedDict, total=False):
    name: Required[str]
    "Human-readable name to identify this MCP server instance (4-30 characters,\nalphanumeric, spaces, and hyphens only)"
    auth_config_ids: Required[SequenceNotStr[str]]
    "ID references to existing authentication configurations"
    no_auth_apps: SequenceNotStr[str]
    "List of NO_AUTH apps to enable for this MCP server"
    allowed_tools: SequenceNotStr[str]
    "List of tool slugs that should be allowed for this server.\n\nIf not provided, all available tools for the authentication configuration will\nbe enabled."
    managed_auth_via_composio: bool
    "Whether the MCP server is managed by Composio"


__all__ = [
    "McpCreateParams",
]
