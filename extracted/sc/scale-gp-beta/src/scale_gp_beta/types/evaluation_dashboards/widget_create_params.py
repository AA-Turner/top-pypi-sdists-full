# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Required, TypeAlias, TypedDict

from .metric_query_param import MetricQueryParam
from .series_query_param import SeriesQueryParam
from .evaluation_widget_type_enum import EvaluationWidgetTypeEnum

__all__ = ["WidgetCreateParams", "Query"]


class WidgetCreateParams(TypedDict, total=False):
    title: Required[str]
    """Widget title"""

    type: Required[EvaluationWidgetTypeEnum]
    """Widget type"""

    config: Dict[str, object]
    """Chart-specific display configuration"""

    query: Query
    """Structured query AST for metric computation (SeriesQuery or MetricQuery)"""


Query: TypeAlias = Union[SeriesQueryParam, MetricQueryParam]
