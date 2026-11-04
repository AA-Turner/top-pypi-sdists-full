# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.cli.realtime_auth_params."""

from __future__ import annotations

from typing_extensions import Required, TypedDict


class RealtimeAuthParams(TypedDict, total=False):
    channel_name: Required[str]
    "The channel name to authenticate for"
    socket_id: Required[str]
    "The socket ID for Pusher authentication"


__all__ = [
    "RealtimeAuthParams",
]
