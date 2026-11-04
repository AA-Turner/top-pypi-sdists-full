# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.session_configs_list_params."""

from __future__ import annotations

from typing_extensions import NotRequired, TypedDict


class SessionConfigsListParams(TypedDict, total=False):
    cursor: NotRequired[str]
    limit: NotRequired[int]
    archived: NotRequired[bool | None]


__all__ = [
    "SessionConfigsListParams",
]
