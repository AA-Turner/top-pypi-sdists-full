# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Required, TypeAlias, TypedDict

from .metric_query_param import MetricQueryParam
from .series_query_param import SeriesQueryParam

__all__ = ["WidgetUpdateParams", "Query"]


class WidgetUpdateParams(TypedDict, total=False):
    dashboard_id: Required[str]

    config: Dict[str, object]
    """Chart-specific display configuration"""

    query: Query
    """Structured query AST for metric computation (SeriesQuery or MetricQuery)"""

    title: str
    """Widget title"""


Query: TypeAlias = Union[SeriesQueryParam, MetricQueryParam]
