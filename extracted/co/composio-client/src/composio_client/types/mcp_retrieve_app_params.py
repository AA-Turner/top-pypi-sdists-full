# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.mcp_retrieve_app_params."""

from __future__ import annotations

from typing import Literal, Optional

from typing_extensions import TypedDict


class McpRetrieveAppParams(TypedDict, total=False):
    name: str
    "Filter MCP servers by name (case-insensitive partial match)"
    toolkits: str
    "Comma-separated list of toolkit slugs to filter servers by"
    auth_config_ids: str
    "Comma-separated list of auth config IDs to filter servers by"
    order_by: Literal['created_at', 'updated_at']
    "Field to order results by"
    order_direction: Literal['asc', 'desc']
    "Direction of ordering"
    page_no: Optional[float]
    "Page number for pagination (1-based)"
    limit: Optional[float]
    "Number of items per page (default: 10)"


__all__ = [
    "McpRetrieveAppParams",
]
