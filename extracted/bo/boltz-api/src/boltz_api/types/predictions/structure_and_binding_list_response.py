# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["StructureAndBindingListResponse", "Error"]


class Error(BaseModel):
    """Error details when failed"""

    code: str
    """Machine-readable error code"""

    message: str
    """Human-readable error message"""

    details: Optional[object] = None
    """Additional field-level error details keyed by input path, when available."""


class StructureAndBindingListResponse(BaseModel):
    id: str
    """Unique prediction identifier"""

    completed_at: Optional[datetime] = None

    created_at: datetime

    data_deleted_at: Optional[datetime] = None
    """When the input/output data was deleted, or null if still available"""

    error: Optional[Error] = None
    """Error details when failed"""

    expires_at: Optional[datetime] = None
    """When this resource and its associated data will be permanently deleted.

    Null while still in progress.
    """

    livemode: bool
    """Whether this resource was created with a live API key."""

    model: Literal["boltz-2.1"]
    """Model used for prediction"""

    started_at: Optional[datetime] = None

    status: Literal["pending", "running", "succeeded", "failed"]

    version: str
    """Model version used for prediction"""

    workspace_id: str
    """Workspace ID"""

    idempotency_key: Optional[str] = None
    """Client-provided idempotency key"""
