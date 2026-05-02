# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel
from .metric_query import MetricQuery
from .series_query import SeriesQuery
from .evaluation_widget_type_enum import EvaluationWidgetTypeEnum

__all__ = ["EvaluationDashboardWidget", "Query"]

Query: TypeAlias = Union[SeriesQuery, MetricQuery]


class EvaluationDashboardWidget(BaseModel):
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

    archived_at: Optional[datetime] = None
    """When the widget was archived (soft-deleted)"""

    config: Optional[Dict[str, object]] = None
    """Chart-specific display configuration"""

    object: Optional[Literal["evaluation_dashboard_widget"]] = None

    query: Optional[Query] = None
    """Structured query AST for metric computation (SeriesQuery or MetricQuery)"""
