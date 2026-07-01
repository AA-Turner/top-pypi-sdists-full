# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from .._models import BaseModel
from .text_content import TextContent
from .embedding_config import EmbeddingConfig

__all__ = ["VectorStoreQueryResponse", "Metadata", "Vector"]


class Metadata(BaseModel):
    """Query execution metadata"""

    search_type: str
    """Type of search performed (semantic, lexical, hybrid)"""

    total_query_time_ms: int
    """Total end-to-end query execution time in milliseconds"""

    embedding_config: Optional[EmbeddingConfig] = None
    """Embedding configuration used for query vectorization.

    None for lexical queries on model-less stores.
    """

    embedding_time_ms: Optional[int] = None
    """Time spent generating embeddings in milliseconds (None for lexical queries)"""

    index_query_time_ms: Optional[int] = None
    """Time spent querying the vector index (OpenSearch) in milliseconds"""

    reranking_model: Optional[str] = None
    """Reranking model used (None if reranking not enabled)"""

    reranking_time_ms: Optional[int] = None
    """Time spent reranking results in milliseconds (None if reranking not enabled)"""


class Vector(BaseModel):
    """A document in query/search responses with similarity score.

    Extends VectorDocumentResponse to add a similarity score field for ranked search results.
    """

    id: str
    """Document ID"""

    score: float
    """Similarity score indicating relevance"""

    content: Optional[TextContent] = None
    """Text content for documents."""

    metadata: Optional[Dict[str, object]] = None
    """Key-value metadata"""

    vector: Optional[List[float]] = None
    """Embedding vector (if requested)"""


class VectorStoreQueryResponse(BaseModel):
    """Response for query operation."""

    metadata: Metadata
    """Query execution metadata"""

    vectors: List[Vector]
    """Array of matching documents"""
