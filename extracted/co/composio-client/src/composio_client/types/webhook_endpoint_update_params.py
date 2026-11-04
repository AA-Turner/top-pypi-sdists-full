# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.webhook_endpoint_update_params."""

from __future__ import annotations

from typing_extensions import Required, TypedDict


class WebhookEndpointUpdateParams(TypedDict, total=False):
    data: Required[dict[str, str]]


__all__ = [
    "WebhookEndpointUpdateParams",
]
