# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo
from .filter_param import FilterParam
from .select_item_param import SelectItemParam

__all__ = ["SeriesQueryParam", "OrderBy"]


class OrderBy(TypedDict, total=False):
    """Column in ORDER BY clause"""

    column: Required[str]
    """Column name to sort by"""

    direction: Literal["ASC", "DESC"]
    """Sort direction"""

    source: str
    """Column source: 'data' or 'task_result_cache'"""


class SeriesQueryParam(TypedDict, total=False):
    """
    Query that returns a series of records (used for table/bar/histogram/donut/scatter widgets).

    Used for widget types: table, bar, histogram, donut, scatter.
    Returns: {"type": "series", "data": [...]}

    Example SQL equivalent:
        SELECT category, AVG(score) as avg_score, COUNT(*) as count
        FROM evaluation_items
        WHERE score > 0.5 AND category = 'test'
        GROUP BY category
        ORDER BY avg_score DESC
        LIMIT 100
    """

    select: Required[Iterable[SelectItemParam]]

    evaluation_ids: SequenceNotStr[str]
    """Optional subset of evaluation IDs to compute on.

    Only applicable for evaluation group dashboards. If omitted, computes on all
    evaluations in the group.
    """

    filter: FilterParam
    """Filter conditions (WHERE clause)"""

    group_by: Annotated[SequenceNotStr[str], PropertyInfo(alias="groupBy")]
    """Columns to group by"""

    limit: int
    """Max rows to return"""

    order_by: Annotated[Iterable[OrderBy], PropertyInfo(alias="orderBy")]
    """Sort order"""
