# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.mcp_list_instances_params."""

from __future__ import annotations

from typing import Literal

from typing_extensions import NotRequired, TypedDict


class McpListInstancesParams(TypedDict, total=False):
    page_no: NotRequired[float | None]
    limit: NotRequired[float | None]
    search: NotRequired[str]
    order_by: NotRequired[Literal["created_at", "updated_at"]]
    order_direction: NotRequired[Literal["asc", "desc"]]


__all__ = [
    "McpListInstancesParams",
]
