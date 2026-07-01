# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["VectorStoreCountResponse"]


class VectorStoreCountResponse(BaseModel):
    """Response for count operation."""

    count: int
    """Number of documents matching the criteria"""
