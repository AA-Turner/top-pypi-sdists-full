# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.webhook_endpoint_list_params."""

from __future__ import annotations

from typing_extensions import NotRequired, TypedDict


class WebhookEndpointListParams(TypedDict, total=False):
    toolkit_slug: NotRequired[str]


__all__ = [
    "WebhookEndpointListParams",
]
