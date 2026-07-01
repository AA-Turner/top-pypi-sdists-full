# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel
from .shared.chunk import Chunk

__all__ = ["KnowledgeBaseQueryResponse"]


class KnowledgeBaseQueryResponse(BaseModel):
    chunks: List[Chunk]
    """
    An ordered list of the k most similar chunks and their similarity scores from
    most to least similar
    """

    completed_at: Optional[datetime] = None
    """Timestamp at which the query was completed by the server."""

    request_id: Optional[str] = None
    """query request ID for verbose logging"""

    started_at: Optional[datetime] = None
    """Timestamp at which the query was begun by the server."""
