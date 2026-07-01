# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ...._models import BaseModel

__all__ = ["ChunkDeleteResponse"]


class ChunkDeleteResponse(BaseModel):
    artifact_id: str
    """The ID of the artifact from which the chunk was deleted"""

    chunk_id: str
    """The ID of the chunk that was deleted"""

    deleted: bool
    """Whether or not the artifact was successfully deleted"""
