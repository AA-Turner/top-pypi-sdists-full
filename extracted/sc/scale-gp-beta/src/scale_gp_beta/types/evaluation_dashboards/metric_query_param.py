# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from ..._types import SequenceNotStr
from .filter_param import FilterParam
from .select_item_param import SelectItemParam

__all__ = ["MetricQueryParam"]


class MetricQueryParam(TypedDict, total=False):
    """Query that returns a single metric value (used for metric widgets).

    Used for widget type: metric.
    Enforces exactly 1 aggregation in select.
    Returns: {"type": "metric", "data": ...}

    Example SQL equivalent:
        SELECT AVG(score) as average_score
        FROM evaluation_items
    """

    select: Required[Iterable[SelectItemParam]]

    evaluation_ids: SequenceNotStr[str]
    """Optional subset of evaluation IDs to compute on.

    Only applicable for evaluation group dashboards. If omitted, computes on all
    evaluations in the group.
    """

    filter: FilterParam
    """Filter conditions (WHERE clause)"""
