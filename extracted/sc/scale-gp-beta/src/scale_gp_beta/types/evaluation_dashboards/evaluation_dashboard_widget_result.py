# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .evaluation_dashboard_widget import EvaluationDashboardWidget

__all__ = ["EvaluationDashboardWidgetResult"]


class EvaluationDashboardWidgetResult(BaseModel):
    id: str
    """Unique identifier of the widget result"""

    account_id: str
    """Account that owns this widget result"""

    computation_status: Literal["pending", "completed", "failed"]
    """Status of the computation"""

    created_at: datetime
    """When the widget result was created"""

    widget_id: str
    """Unique identifier of the widget"""

    computation_job_id: Optional[str] = None
    """Temporal workflow ID or job ID for async computation tracking"""

    computed_at: Optional[datetime] = None
    """Timestamp when computation completed successfully"""

    computed_result: Optional[Dict[str, object]] = None
    """Cached computation results"""

    error_message: Optional[str] = None
    """Error message if computation failed"""

    evaluation_group_id: Optional[str] = None
    """FK to evaluation_groups. Null if result is for a single evaluation."""

    evaluation_id: Optional[str] = None
    """FK to evaluations. Null if result is for an evaluation group."""

    object: Optional[Literal["evaluation_dashboard_widget_result"]] = None

    widget: Optional[EvaluationDashboardWidget] = None
    """Widget that this result is for"""
