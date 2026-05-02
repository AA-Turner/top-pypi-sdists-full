# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["DeployLogsResponse", "Line"]


class Line(BaseModel):
    """A single structured log line from the deployment process."""

    id: str
    """Unique log line identifier (time-ordered)"""

    message: str
    """Log line content after the K8s timestamp"""

    log_level: Optional[str] = None
    """Parsed log level (INFO, ERROR, WARN, DEBUG, FATAL)"""

    timestamp: Optional[datetime] = None
    """Parsed K8s log timestamp"""


class DeployLogsResponse(BaseModel):
    """
    Response containing structured deployment log lines with cursor-based pagination.

    The CLI can poll this endpoint to stream logs incrementally:
    1. First call: no after_id
    2. Subsequent calls: after_id=next_cursor from previous response
    3. Stop polling when has_more is False and the deployment reaches a terminal status
    """

    deployment_id: str
    """The deployment ID"""

    has_more: bool
    """True if there may be more lines beyond this page (len(lines) == limit)."""

    lines: Optional[List[Line]] = None
    """Structured log lines"""

    next_cursor: Optional[str] = None
    """Cursor for the next page.

    Pass this as the after_id query parameter to get subsequent logs.
    """
