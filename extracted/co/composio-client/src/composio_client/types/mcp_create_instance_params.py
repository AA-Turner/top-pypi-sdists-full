# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.mcp_create_instance_params."""

from __future__ import annotations

from typing_extensions import Required, TypedDict


class McpCreateInstanceParams(TypedDict, total=False):
    user_id: Required[str]


__all__ = [
    "McpCreateInstanceParams",
]
