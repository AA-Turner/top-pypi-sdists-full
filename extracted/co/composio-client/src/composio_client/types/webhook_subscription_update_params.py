# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.webhook_subscription_update_params."""

from __future__ import annotations

from typing import Literal

from typing_extensions import NotRequired, TypedDict
from .._types import SequenceNotStr


class WebhookSubscriptionUpdateParams(TypedDict, total=False):
    webhook_url: NotRequired[str]
    enabled_events: NotRequired[SequenceNotStr[str]]
    version: NotRequired[Literal["V1", "V2", "V3"]]


__all__ = [
    "WebhookSubscriptionUpdateParams",
]
