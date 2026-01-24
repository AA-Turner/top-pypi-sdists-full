# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Literal, TypedDict

__all__ = ["SpanSearchParams", "Filter"]


class SpanSearchParams(TypedDict, total=False):
    filters: Iterable[Filter]

    limit: int

    order: Literal["timestamp asc", "timestamp desc"]


class Filter(TypedDict, total=False):
    and_: Optional[Iterable[object]]

    field: Optional[str]

    op: Optional[Literal["eq", "ne", "gt", "ge", "lt", "le", "starts_with", "ends_with", "in"]]

    or_: Optional[Iterable[object]]

    value: object
