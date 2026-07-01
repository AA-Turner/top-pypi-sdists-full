# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal, Required, TypedDict

from .chat.sort_order import SortOrder
from .evaluation_views import EvaluationViews

__all__ = ["EvaluationFilterParams", "Filter"]


class EvaluationFilterParams(TypedDict, total=False):
    filters: Required[Iterable[Filter]]
    """List of metadata filters to apply (maximum 10)"""

    ending_before: str

    include_archived: bool

    limit: int

    sort_by: str

    sort_order: SortOrder

    starting_after: str

    views: List[EvaluationViews]


class Filter(TypedDict, total=False):
    """Individual metadata filter specification"""

    key: Required[str]
    """The metadata key to filter on"""

    operator: Required[Literal["==", "!=", ">=", "<=", "IN", "NOT_IN"]]
    """The comparison operator to use"""

    value: Required[str]
    """The value to compare against (string for all types)"""

    object: Literal["metadata_filter"]
