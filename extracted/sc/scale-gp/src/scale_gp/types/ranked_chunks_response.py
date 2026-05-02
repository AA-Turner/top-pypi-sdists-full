# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .shared.chunk import Chunk

__all__ = ["RankedChunksResponse"]


class RankedChunksResponse(BaseModel):
    relevant_chunks: List[Chunk]
    """List of chunks ranked by the requested rank strategy"""
