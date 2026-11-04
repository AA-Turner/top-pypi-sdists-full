# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.mcp.generate_url_response."""

from __future__ import annotations

from pydantic import ConfigDict
from ..._base_model import BaseModel


class GenerateURLResponse(BaseModel):
    "Response containing the generated MCP URLs"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    connected_account_urls: list[str]
    "List of URLs generated for each connected account ID"
    mcp_url: str
    "Base MCP URL without any query parameters"
    user_ids_url: list[str]
    "List of URLs generated for each user ID"


__all__ = [
    "GenerateURLResponse",
]
