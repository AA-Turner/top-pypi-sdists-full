# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Required, TypedDict

__all__ = ["Chunk"]


class Chunk(TypedDict, total=False):
    chunk_id: Required[str]
    """The unique ID of the chunk with embedding"""

    score: Required[float]
    """
    A number between 0 and 1 representing how similar a chunk's embedding is to the
    query embedding. Higher numbers mean that this chunk with embedding is more
    similar.
    """

    text: Required[str]
    """The text associated with the chunk"""

    attachment_url: str
    """Original attachment URL from which this chunk got its data from"""

    embedding: Iterable[float]
    """The vector embedding of the text associated with the chunk"""

    metadata: Dict[str, object]
    """
    Any additional key value pairs of information stored by you on the chunk with
    embedding
    """

    title: str
    """Title for this chunk, for example the file name"""

    user_supplied_metadata: Dict[str, object]
    """
    Any additional key value pairs of information returned from the custom chunking.
    """
