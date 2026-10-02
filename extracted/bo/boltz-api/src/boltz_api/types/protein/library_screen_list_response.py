# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["LibraryScreenListResponse", "Error", "Progress"]


class Error(BaseModel):
    code: str
    """Machine-readable error code"""

    message: str
    """Human-readable error message"""

    details: Optional[object] = None
    """Additional field-level error details keyed by input path, when available."""


class Progress(BaseModel):
    num_proteins_failed: int
    """Number of accepted proteins that reached terminal failure during screening."""

    num_proteins_screened: int
    """Number of accepted proteins that produced usable screening results."""

    total_proteins_to_screen: int
    """Total number of proteins accepted into the screening run."""

    latest_result_id: Optional[str] = None
    """ID of the latest result"""


class LibraryScreenListResponse(BaseModel):
    """Summary of a protein library screening pipeline run (excludes input)"""

    id: str
    """Unique ProteinLibraryScreenSummary identifier"""

    completed_at: Optional[datetime] = None

    created_at: datetime

    data_deleted_at: Optional[datetime] = None
    """When the input, output, and result data was permanently deleted.

    Null if data has not been deleted.
    """

    engine: Literal["boltzprot"]
    """Deprecated. Use pipeline instead."""

    engine_version: Literal["1.0"]
    """Deprecated. Use pipeline_version instead."""

    error: Optional[Error] = None

    livemode: bool
    """Whether this resource was created with a live API key."""

    pipeline: Literal["boltzprot"]
    """Pipeline used for protein library screen"""

    pipeline_version: Literal["1.0"]
    """Pipeline version used for protein library screen"""

    progress: Optional[Progress] = None

    started_at: Optional[datetime] = None

    status: Literal["pending", "running", "succeeded", "failed", "stopped"]

    stopped_at: Optional[datetime] = None

    workspace_id: str
    """Workspace ID"""

    idempotency_key: Optional[str] = None
    """Client-provided idempotency key"""
