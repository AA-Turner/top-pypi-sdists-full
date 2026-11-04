# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.mcp.generate_url_params."""

from __future__ import annotations

from typing_extensions import Required, TypedDict
from ..._types import SequenceNotStr


class GenerateURLParams(TypedDict, total=False):
    mcp_server_id: Required[str]
    "Unique identifier of the MCP server to generate URL for"
    managed_auth_by_composio: bool
    "Flag indicating if Composio manages authentication"
    user_ids: SequenceNotStr[str]
    "List of user identifiers for whom the URL is generated"
    connected_account_ids: SequenceNotStr[str]
    "List of connected account identifiers"


__all__ = [
    "GenerateURLParams",
]
