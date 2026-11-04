# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.connected_account_update_status_params."""

from __future__ import annotations

from typing_extensions import Required, TypedDict


class ConnectedAccountUpdateStatusParams(TypedDict, total=False):
    enabled: Required[bool]
    "Set to true to enable the account or false to disable it"


__all__ = [
    "ConnectedAccountUpdateStatusParams",
]
