# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.project.usage_retrieve_params."""

from __future__ import annotations

from typing import Literal

from typing_extensions import NotRequired, TypedDict
from ..._types import SequenceNotStr


class Filters(TypedDict, total=False):
    user_id: NotRequired[SequenceNotStr[str] | None]
    "Filter to events matching these external end-user IDs. OR logic within the array."
    session_id: NotRequired[SequenceNotStr[str] | None]
    "Filter to events matching these session IDs. OR logic within the array."


class UsageRetrieveParams(TypedDict, total=False):
    from_: NotRequired[float]
    to: NotRequired[float]
    group_by: NotRequired[str]
    order_by: NotRequired[Literal["key", "total_quantity", "event_count"]]
    order_direction: NotRequired[Literal["asc", "desc"]]
    limit: NotRequired[int]
    filters: NotRequired[Filters]


__all__ = [
    "UsageRetrieveParams",
    "Filters",
]
