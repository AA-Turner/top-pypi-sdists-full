# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.custom_delete_toolkit_params."""

from __future__ import annotations

from typing_extensions import NotRequired, TypedDict


class CustomDeleteToolkitParams(TypedDict, total=False):
    revoke_on_delete: NotRequired[bool | None]


__all__ = [
    "CustomDeleteToolkitParams",
]
