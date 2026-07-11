# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .filter import Filter
from ..._models import BaseModel
from .select_item import SelectItem

__all__ = ["SeriesQuery", "OrderBy"]


class OrderBy(BaseModel):
    """Column in ORDER BY clause"""

    column: str
    """Column name to sort by"""

    direction: Optional[Literal["ASC", "DESC"]] = None
    """Sort direction"""

    source: Optional[str] = None
    """Column source: 'data' or 'task_result_cache'"""


class SeriesQuery(BaseModel):
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

    select: List[SelectItem]

    evaluation_ids: Optional[List[str]] = None
    """Optional subset of evaluation IDs to compute on.

    Only applicable for evaluation group dashboards. If omitted, computes on all
    evaluations in the group.
    """

    filter: Optional[Filter] = None
    """Filter conditions (WHERE clause)"""

    group_by: Optional[List[str]] = FieldInfo(alias="groupBy", default=None)
    """Columns to group by"""

    latest_only: Optional[bool] = None
    """
    When True, the widget computes against rows from only the most recent active
    evaluation in the group (by EvaluationORM.created_at). Only applicable for
    evaluation group dashboards. Composes with evaluation_ids (latest within the
    subset). Cannot be combined with per-aggregation evaluation_ids; the use case
    enforces these rules.
    """

    limit: Optional[int] = None
    """Max rows to return"""

    order_by: Optional[List[OrderBy]] = FieldInfo(alias="orderBy", default=None)
    """Sort order"""
