# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.webhook_endpoint_create_params."""

from __future__ import annotations

from typing_extensions import Required, TypedDict


class WebhookEndpointCreateParams(TypedDict, total=False):
    toolkit_slug: Required[str]
    client_id: Required[str]


__all__ = [
    "WebhookEndpointCreateParams",
]
