# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.mcp_delete_response."""

from __future__ import annotations

from pydantic import ConfigDict
from .._base_model import BaseModel


class McpDeleteResponse(BaseModel):
    "Response indicating the success of the delete operation"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    deleted: bool
    "Indicates whether the MCP server was successfully deleted"
    id: str
    "Unique identifier of the MCP server to retrieve, update, or delete"


__all__ = [
    "McpDeleteResponse",
]
