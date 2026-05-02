# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["VectorStoreUpsertResponse", "Failed"]


class Failed(BaseModel):
    """A document that failed during a batch upsert operation."""

    id: str
    """Document ID"""

    error: str
    """Error message describing why the document failed"""


class VectorStoreUpsertResponse(BaseModel):
    """Response for batch insert/upsert operations."""

    failure_count: int
    """Number of failed documents"""

    success_count: int
    """Number of successfully processed documents"""

    failed: Optional[List[Failed]] = None
    """Failed documents with their error messages"""

    succeeded: Optional[List[str]] = None
    """IDs of successfully processed documents"""
