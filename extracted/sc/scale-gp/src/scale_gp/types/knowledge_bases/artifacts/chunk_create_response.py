# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["ChunkCreateResponse"]


class ChunkCreateResponse(BaseModel):
    id: str
    """The id of the chunk"""

    artifact_id: str
    """The id of the artifact"""

    chunk_position: int
    """Chunk position"""

    status: Literal["Pending", "Completed", "Failed"]
    """Status of the chunk.

    If Failed or Pending, its possible that the chunk does not reflect in OpenSearch
    """

    text: str
    """The text of the chunk as stored in the database"""

    created_at: Optional[datetime] = None
    """Date and time of chunk creation"""

    metadata: Optional[Dict[str, object]] = None
    """Metadata of the chunk which is stored in OpenSearch"""

    status_reason: Optional[str] = None
    """Status reason of the chunk. May be successful"""

    user_supplied_metadata: Optional[Dict[str, object]] = None
    """
    Metadata of the chunk which is stored in the database only provided via custom
    chunking.
    """
