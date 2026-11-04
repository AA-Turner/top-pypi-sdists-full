# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.custom_sync_params."""

from __future__ import annotations

from typing_extensions import NotRequired, Required, TypedDict


class CustomSyncParams(TypedDict, total=False):
    slug: Required[str]
    connected_account_id: NotRequired[str]


__all__ = [
    "CustomSyncParams",
]
