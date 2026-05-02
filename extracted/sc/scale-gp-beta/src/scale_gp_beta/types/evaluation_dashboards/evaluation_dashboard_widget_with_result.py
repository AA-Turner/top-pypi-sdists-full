# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel
from .metric_query import MetricQuery
from .series_query import SeriesQuery
from .evaluation_widget_type_enum import EvaluationWidgetTypeEnum
from .evaluation_dashboard_widget_result_response import EvaluationDashboardWidgetResultResponse

__all__ = ["EvaluationDashboardWidgetWithResult", "Query"]

Query: TypeAlias = Union[SeriesQuery, MetricQuery]


class EvaluationDashboardWidgetWithResult(BaseModel):
    """Response model for widget creation - includes widget and computed result"""

    id: str
    """Unique identifier of the widget"""

    account_id: str
    """Account that owns this widget"""

    created_at: datetime
    """When the widget was created"""

    title: str
    """Widget title"""

    type: EvaluationWidgetTypeEnum
    """Widget type"""

    config: Optional[Dict[str, object]] = None
    """Display configuration"""

    object: Optional[Literal["evaluation_widget"]] = None

    query: Optional[Query] = None
    """Structured query AST for computation (SeriesQuery or MetricQuery)"""

    result: Optional[EvaluationDashboardWidgetResultResponse] = None
    """Computed result for this widget"""
