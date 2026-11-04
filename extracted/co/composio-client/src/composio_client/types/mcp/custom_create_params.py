# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.mcp.custom_create_params."""

from __future__ import annotations

from typing_extensions import Required, TypedDict
from ..._types import SequenceNotStr


class CustomCreateParams(TypedDict, total=False):
    name: Required[str]
    "Human-readable name to identify this custom MCP server (4-30 characters,\nalphanumeric, spaces, and hyphens only)"
    auth_config_ids: SequenceNotStr[str]
    "ID references to existing authentication configurations"
    toolkits: SequenceNotStr[str]
    "List of application/toolkit identifiers to enable for this server"
    allowed_tools: SequenceNotStr[str]
    "Tool identifiers to enable that aren't part of standard toolkits"
    custom_tools: SequenceNotStr[str]
    "DEPRECATED: Use allowed_tools instead.\n\nTool identifiers to enable that aren't part of standard toolkits"
    managed_auth_via_composio: bool
    "Whether to manage authentication via Composio"


__all__ = [
    "CustomCreateParams",
]
