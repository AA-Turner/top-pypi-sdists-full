# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["AgentexCloudDeployEvent"]


class AgentexCloudDeployEvent(BaseModel):
    """Slim event representation for the API response."""

    message: Optional[str] = None
    """Full event message."""

    reason: Optional[str] = None
    """Short reason, e.g. 'Pulling', 'Scheduled'."""

    timestamp: Optional[datetime] = None
    """When the event was observed."""

    type: Optional[str] = None
    """Event type, e.g. 'Normal' or 'Warning'."""
