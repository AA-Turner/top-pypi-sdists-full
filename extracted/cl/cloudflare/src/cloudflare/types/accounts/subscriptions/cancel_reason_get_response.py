# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from ...._models import BaseModel

__all__ = ["CancelReasonGetResponse"]


class CancelReasonGetResponse(BaseModel):
    id: Optional[str] = None
    """The cancel reason identifier."""

    other: Optional[str] = None
    """Additional cancellation details."""

    reason_code: Optional[List[str]] = None
    """The cancellation reason codes."""

    submitted: Optional[datetime] = None
    """When the cancel reason was submitted."""

    subscription_id: Optional[str] = None
    """The subscription identifier."""
