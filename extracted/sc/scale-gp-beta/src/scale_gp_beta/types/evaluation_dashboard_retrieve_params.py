# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["EvaluationDashboardRetrieveParams"]


class EvaluationDashboardRetrieveParams(TypedDict, total=False):
    include_archived: bool

    views: List[Literal["widgets", "widget_results"]]
    """Optional relationships to include: 'widgets', 'widget_results'"""
