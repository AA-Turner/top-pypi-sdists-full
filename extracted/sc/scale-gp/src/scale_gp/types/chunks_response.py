# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from .._models import BaseModel

__all__ = ["ChunksResponse", "Chunk"]


class Chunk(BaseModel):
    chunk_id: str
    """The unique ID of the chunk with embedding"""

    text: str
    """The text associated with the chunk"""

    attachment_url: Optional[str] = None
    """Original attachment URL from which this chunk got its data from"""

    embedding: Optional[List[float]] = None
    """The vector embedding of the text associated with the chunk"""

    metadata: Optional[Dict[str, object]] = None
    """
    Any additional key value pairs of information stored by you on the chunk with
    embedding
    """

    title: Optional[str] = None
    """Title for this chunk, for example the file name"""

    user_supplied_metadata: Optional[Dict[str, object]] = None
    """
    Any additional key value pairs of information returned from the custom chunking.
    """


class ChunksResponse(BaseModel):
    chunks: List[Chunk]
    """List of chunks that match the chunk_id and metadata filters"""
