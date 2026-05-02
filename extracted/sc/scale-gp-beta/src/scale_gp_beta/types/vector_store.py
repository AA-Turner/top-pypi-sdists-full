# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .embedding_config import EmbeddingConfig

__all__ = ["VectorStore"]


class VectorStore(BaseModel):
    """Response model for vector store operations."""

    created_at: datetime
    """Timestamp of creation"""

    embedding_dimensions: int
    """Dimensionality of the embedding vectors"""

    name: str
    """The name of the vector store"""

    updated_at: datetime
    """Timestamp of last update"""

    embedding_config: Optional[EmbeddingConfig] = None
    """Embedding configuration identifying the model and its type.

    None for raw-embedding-only stores.
    """

    indexed_metadata_fields: Optional[Dict[str, Literal["string", "number", "boolean"]]] = None
    """Dictionary mapping metadata field names to their types"""
