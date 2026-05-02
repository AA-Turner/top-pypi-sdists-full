# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["EvaluationDashboardWidgetResultResponse"]


class EvaluationDashboardWidgetResultResponse(BaseModel):
    """Computed result for a widget - used in widget creation response"""

    id: str
    """Unique identifier of the widget result"""

    computation_status: str
    """Status: pending, completed, or failed"""

    widget_id: str
    """Widget ID this result belongs to"""

    computed_at: Optional[datetime] = None
    """When computation completed"""

    computed_result: Optional[Dict[str, object]] = None
    """Computed result data.

    Metric: {type: 'metric', data: 42}, Series: {type: 'series', data: [{x: 'A', y:
    10}, ...]}
    """

    error_message: Optional[str] = None
    """Error message if computation failed"""
