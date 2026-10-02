"""
AGENTICSTAR Platform SDK - Memory Module
セマンティックメモリ（Mem0 + Qdrant）を提供

Note:
- 組織階層（personal/role/org/global）は提供しない
- PIIマスキングは提供しない（利用側で実装）
- 基本的なメモリ保存・検索機能のみ提供
"""

from .semantic import (
    SemanticMemoryClient,
    SemanticMemoryConfig,
    LLMProviderConfig,
    QdrantVectorStoreConfig,
    SemanticMemoryError,
    SemanticMemoryConfigError,
    # ユーティリティ関数（autonomousからも使用可能）
    normalize_provider,
    parse_model_string,
    get_api_key,
    convert_llm_to_mem0,
    convert_embedder_to_mem0,
)

__all__ = [
    # Semantic Memory (Mem0)
    "SemanticMemoryClient",
    "SemanticMemoryConfig",
    "QdrantVectorStoreConfig",
    "SemanticMemoryError",
    "SemanticMemoryConfigError",
    # Shared
    "LLMProviderConfig",
    # ユーティリティ関数
    "normalize_provider",
    "parse_model_string",
    "get_api_key",
    "convert_llm_to_mem0",
    "convert_embedder_to_mem0",
]
