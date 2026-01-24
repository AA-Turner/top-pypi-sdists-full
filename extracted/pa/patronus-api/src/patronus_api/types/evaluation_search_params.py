# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from typing_extensions import Literal, TypedDict

__all__ = ["EvaluationSearchParams", "Filter"]


class EvaluationSearchParams(TypedDict, total=False):
    filters: Optional[Iterable[Filter]]

    log_id_in: Optional[List[str]]
    """Deprecated, please use 'filters' instead."""

    trace_id: Optional[str]
    """Deprecated, please use 'filters' instead."""


class Filter(TypedDict, total=False):
    and_: Optional[Iterable[object]]

    field: Optional[str]

    operation: Optional[Literal["starts_with", "ends_with", "like", "ilike", "eq", "ne", "lt", "le", "gt", "ge", "in"]]

    or_: Optional[Iterable[object]]

    value: Union[Iterable[object], object, None]
