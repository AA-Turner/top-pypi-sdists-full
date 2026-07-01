# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .shared.identity import Identity
from .evaluation_dashboards.evaluation_dashboard_widget import EvaluationDashboardWidget
from .evaluation_dashboards.evaluation_dashboard_widget_result import EvaluationDashboardWidgetResult

__all__ = ["EvaluationDashboard"]


class EvaluationDashboard(BaseModel):
    id: str
    """Unique identifier of the dashboard"""

    account_id: str
    """Account that owns this dashboard"""

    created_at: datetime
    """When the dashboard was created"""

    created_by: Identity
    """The identity that created the entity."""

    name: str
    """Dashboard name"""

    tags: List[str]
    """The tags associated with the entity"""

    updated_at: datetime
    """When the dashboard was last updated"""

    archived_at: Optional[datetime] = None
    """When the dashboard was archived (soft-deleted)"""

    description: Optional[str] = None
    """Dashboard description"""

    error_message: Optional[str] = None
    """Error message if computation failed"""

    evaluation_group_id: Optional[str] = None
    """Evaluation group ID"""

    evaluation_id: Optional[str] = None
    """Evaluation ID"""

    object: Optional[Literal["evaluation_dashboard"]] = None

    widget_order: Optional[List[str]] = None
    """Ordered array of widget IDs"""

    widget_results: Optional[List[EvaluationDashboardWidgetResult]] = None
    """Widget results for this dashboard. Populated with 'widget_results' view."""

    widgets: Optional[List[EvaluationDashboardWidget]] = None
    """Widgets associated with this dashboard. Populated with 'widgets' view."""
