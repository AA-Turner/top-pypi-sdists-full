# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["LibraryScreenListResponse", "Error", "Progress", "ProgressRejectionSummary"]


class Error(BaseModel):
    code: str
    """Machine-readable error code"""

    message: str
    """Human-readable error message"""

    details: Optional[object] = None
    """Additional field-level error details keyed by input path, when available."""


class ProgressRejectionSummary(BaseModel):
    filtered_count: int
    """Number of submitted molecules removed by server-side filtering rules."""

    invalid_count: int
    """Number of submitted molecules rejected as invalid input."""


class Progress(BaseModel):
    num_molecules_failed: int
    """Number of accepted molecules that reached terminal failure during screening."""

    num_molecules_screened: int
    """Number of accepted molecules that produced usable screening results."""

    total_molecules_to_screen: int
    """
    Total number of molecules accepted into screening after server-side validation
    and filtering.
    """

    latest_result_id: Optional[str] = None
    """ID of the most recently screened result"""

    rejection_summary: Optional[ProgressRejectionSummary] = None


class LibraryScreenListResponse(BaseModel):
    """Summary of a small molecule library screening pipeline run (excludes input)"""

    id: str
    """Unique SmScreenSummary identifier"""

    completed_at: Optional[datetime] = None

    created_at: datetime

    data_deleted_at: Optional[datetime] = None
    """When the input, output, and result data was permanently deleted.

    Null if data has not been deleted.
    """

    engine: Literal["boltzmol"]
    """Deprecated. Use pipeline instead."""

    engine_version: Literal["1.0"]
    """Deprecated. Use pipeline_version instead."""

    error: Optional[Error] = None

    livemode: bool
    """Whether this resource was created with a live API key."""

    pipeline: Literal["boltzmol"]
    """Pipeline used for small molecule library screen"""

    pipeline_version: Literal["1.0"]
    """Pipeline version used for small molecule library screen"""

    progress: Optional[Progress] = None

    started_at: Optional[datetime] = None

    status: Literal["pending", "running", "succeeded", "failed", "stopped"]

    stopped_at: Optional[datetime] = None

    workspace_id: str
    """Workspace ID"""

    idempotency_key: Optional[str] = None
    """Client-provided idempotency key"""
