# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.connected_account_complete_auth_params."""

from __future__ import annotations

from typing_extensions import Required, TypedDict


class ConnectedAccountCompleteAuthParams(TypedDict, total=False):
    session_uri: Required[str]
    user_id: Required[str]


__all__ = [
    "ConnectedAccountCompleteAuthParams",
]
