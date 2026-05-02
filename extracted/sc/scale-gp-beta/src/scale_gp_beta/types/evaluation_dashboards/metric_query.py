# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .filter import Filter
from ..._models import BaseModel
from .select_item import SelectItem

__all__ = ["MetricQuery"]


class MetricQuery(BaseModel):
    """Query that returns a single metric value (used for metric widgets).

    Used for widget type: metric.
    Enforces exactly 1 aggregation in select.
    Returns: {"type": "metric", "data": ...}

    Example SQL equivalent:
        SELECT AVG(score) as average_score
        FROM evaluation_items
    """

    select: List[SelectItem]

    evaluation_ids: Optional[List[str]] = None
    """Optional subset of evaluation IDs to compute on.

    Only applicable for evaluation group dashboards. If omitted, computes on all
    evaluations in the group.
    """

    filter: Optional[Filter] = None
    """Filter conditions (WHERE clause)"""
