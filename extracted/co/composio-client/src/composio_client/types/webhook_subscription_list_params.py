# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.webhook_subscription_list_params."""

from __future__ import annotations

from typing_extensions import NotRequired, TypedDict


class WebhookSubscriptionListParams(TypedDict, total=False):
    limit: NotRequired[float | None]
    cursor: NotRequired[str]


__all__ = [
    "WebhookSubscriptionListParams",
]
