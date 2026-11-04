# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.logs.tool_list_params."""

from __future__ import annotations

from typing import Annotated, Iterable, Optional

from typing_extensions import Required, TypedDict
from ..._types import PropertyInfo


class SearchParam(TypedDict, total=False):
    field: str
    operation: str
    value: str


class ToolListParams(TypedDict, total=False):
    cursor: Required[Optional[float]]
    "cursor_that_can_be_used_to_paginate_through_the_logs"
    limit: float
    "number_of_logs_to_return"
    case_sensitive: Optional[bool]
    "whether_the_search_is_case_sensitive_or_not"
    from_: Annotated[float, PropertyInfo(alias='from')]
    "start_time_of_the_logs_in_epoch_time"
    to: float
    "end_time_of_the_logs_in_epoch_time"
    search_params: Iterable[SearchParam]


__all__ = [
    "ToolListParams",
    "SearchParam",
]
