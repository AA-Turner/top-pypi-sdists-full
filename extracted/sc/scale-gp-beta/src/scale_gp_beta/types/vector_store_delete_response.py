# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["VectorStoreDeleteResponse"]


class VectorStoreDeleteResponse(BaseModel):
    """Response for delete operation."""

    deleted_count: int
    """Number of documents deleted"""
