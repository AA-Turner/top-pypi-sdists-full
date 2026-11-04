# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.org.consumer_list_connected_toolkits_params."""

from __future__ import annotations

from typing_extensions import Required, TypedDict


class ConsumerListConnectedToolkitsParams(TypedDict, total=False):
    user_id: Required[str]
    x_user_api_key: Required[str]
    x_org_id: Required[str]


__all__ = [
    "ConsumerListConnectedToolkitsParams",
]
