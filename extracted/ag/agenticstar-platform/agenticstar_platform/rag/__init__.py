"""
AGENTICSTAR Platform SDK - RAG Module
ベクトルデータベース操作とEmbedding生成機能を提供

Example:
    from agenticstar_platform.rag import (
        QdrantManager,
        QdrantConfig,
        EmbeddingGenerator,
        EmbeddingConfig,
    )

    # Context Managerを使用した安全なリソース管理
    async with QdrantManager(qdrant_config, embedding_gen) as manager:
        result = await manager.search("検索クエリ")
"""

# Base classes and types
from .base import (
    VectorStoreProvider,
    VectorStoreError,
    VectorStoreConfigError,
    VectorStoreConnectionError,
    SearchResult,
    UpsertResult,
    SearchResponse,
    VectorStoreClientProtocol,
    VectorStoreClientBase,
)

from .embedding import (
    EmbeddingGenerator,
    EmbeddingConfig,
    EmbeddingError,
    RateLimitExceededError,
)
from .qdrant_manager import (
    QdrantManager,
    QdrantConfig,
    QdrantConfigError,
    PayloadIndexConfig,
)

__all__ = [
    # Base classes
    "VectorStoreProvider",
    "VectorStoreError",
    "VectorStoreConfigError",
    "VectorStoreConnectionError",
    "SearchResult",
    "UpsertResult",
    "SearchResponse",
    "VectorStoreClientProtocol",
    "VectorStoreClientBase",
    # Embedding
    "EmbeddingGenerator",
    "EmbeddingConfig",
    "EmbeddingError",
    "RateLimitExceededError",
    # Qdrant
    "QdrantManager",
    "QdrantConfig",
    "QdrantConfigError",
    "PayloadIndexConfig",
]
