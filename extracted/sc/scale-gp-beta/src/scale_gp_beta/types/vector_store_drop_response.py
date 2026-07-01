# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["VectorStoreDropResponse"]


class VectorStoreDropResponse(BaseModel):
    """Response for vector store deletion."""

    name: str
    """The name of the deleted vector store"""
