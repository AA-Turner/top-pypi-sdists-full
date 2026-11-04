# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.logs.trigger_list_params."""

from __future__ import annotations

from typing import Annotated, Iterable, Literal, Optional

from typing_extensions import TypedDict
from ..._types import PropertyInfo


class SearchParam(TypedDict, total=False):
    field: str
    operation: str
    value: str


class TriggerListParams(TypedDict, total=False):
    time: Literal['5m', '30m', '6h', '1d', '1w', '1month', '1y']
    "Return logs from the last N time units"
    from_: Annotated[Optional[float], PropertyInfo(alias='from')]
    "Start time for logs (epoch timestamp in milliseconds)"
    to: Optional[float]
    "End time for logs (epoch timestamp in milliseconds)"
    status: Literal['all', 'success', 'error']
    "Filter logs by their status level"
    search: str
    "Search term to filter logs"
    integration_id: Annotated[str, PropertyInfo(alias='integrationId')]
    entity_id: Annotated[str, PropertyInfo(alias='entityId')]
    user_id: Annotated[str, PropertyInfo(alias='userId')]
    "Filter logs by user ID"
    limit: Optional[float]
    "The limit of trigger logs to return"
    cursor: Optional[str]
    search_params: Iterable[SearchParam]
    "Advanced search parameters for filtering logs"
    include_payload: bool
    "Whether to include payload fields in the response.\n\nSet to false for faster list views."


__all__ = [
    "TriggerListParams",
    "SearchParam",
]
