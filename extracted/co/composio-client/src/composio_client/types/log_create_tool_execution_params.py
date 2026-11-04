# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.log_create_tool_execution_params."""

from __future__ import annotations

from typing import Iterable, Literal

from typing_extensions import NotRequired, Required, TypedDict


class Filter(TypedDict, total=False):
    field: Required[Literal["tool_slug", "toolkit_slug", "connected_account_id", "auth_config_id", "status", "user_id", "session_id", "sandbox_id", "request_id", "log_id"]]
    operator: Required[Literal["==", "!=", "contains", "not_contains"]]
    value: Required[str]


_TimeRangeReservedKeywords = TypedDict(  # noqa: UP013 - a wire key is not a Python identifier
    "_TimeRangeReservedKeywords",
    {
        "from": Required[float],
    },
    total=False,
)


class TimeRange(_TimeRangeReservedKeywords, total=False):
    to: Required[float]
    "End time in epoch milliseconds"


class LogCreateToolExecutionParams(TypedDict, total=False):
    limit: NotRequired[float]
    cursor: NotRequired[str | None]
    filters: NotRequired[Iterable[Filter]]
    time_range: NotRequired[TimeRange]


__all__ = [
    "LogCreateToolExecutionParams",
    "Filter",
    "TimeRange",
]
