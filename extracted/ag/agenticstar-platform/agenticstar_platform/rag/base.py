"""
AGENTICSTAR Platform SDK - RAG Base
ベクトルデータベースクライアントの基底クラス・インターフェース定義

将来的なマルチプロバイダー対応（Qdrant、Pinecone、Weaviate等）のための基盤
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

logger = logging.getLogger(__name__)


class VectorStoreProvider(str, Enum):
    """ベクトルストアプロバイダー種別"""
    QDRANT = "qdrant"
    # 将来的な拡張用
    # PINECONE = "pinecone"
    # WEAVIATE = "weaviate"
    # MILVUS = "milvus"


class VectorStoreError(Exception):
    """VectorStore操作の基底エラー"""
    pass


class VectorStoreConfigError(VectorStoreError):
    """VectorStore設定エラー"""
    pass


class VectorStoreConnectionError(VectorStoreError):
    """VectorStore接続エラー"""
    pass


@dataclass
class SearchResult:
    """検索結果"""
    point_id: str
    payload: Dict[str, Any]
    score: float
    similarity: float = 0.0  # 0-1 normalized


@dataclass
class UpsertResult:
    """Upsert結果"""
    success: bool
    point_id: str = ""
    error: Optional[str] = None
    error_code: Optional[str] = None


@dataclass
class SearchResponse:
    """検索レスポンス"""
    success: bool
    results: List[SearchResult] = field(default_factory=list)
    total_found: int = 0
    query: str = ""
    error: Optional[str] = None
    error_code: Optional[str] = None


@runtime_checkable
class VectorStoreClientProtocol(Protocol):
    """ベクトルストアクライアントプロトコル

    すべてのベクトルストアプロバイダー実装が満たすべきインターフェース
    """

    def is_initialized(self) -> bool:
        """初期化されているかどうか"""
        ...

    async def initialize(self) -> None:
        """クライアントを初期化"""
        ...

    async def ensure_initialized(self) -> None:
        """初期化されていなければ初期化"""
        ...

    async def upsert(
        self,
        point_id: str,
        text: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """ベクトルデータをUpsert"""
        ...

    async def batch_upsert(
        self,
        items: List[Dict[str, Any]],
        batch_size: int = 256,
    ) -> Dict[str, Any]:
        """バッチUpsert"""
        ...

    async def search(
        self,
        query_text: str,
        limit: int = 10,
        score_threshold: float = 0.4,
        filter_conditions: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """セマンティック検索"""
        ...

    async def delete(self, point_ids: List[str]) -> Dict[str, Any]:
        """ポイントを削除"""
        ...

    async def get_statistics(self) -> Dict[str, Any]:
        """統計情報を取得"""
        ...

    async def close(self) -> None:
        """クライアントをクローズ"""
        ...


class VectorStoreClientBase(ABC):
    """ベクトルストアクライアント基底クラス

    共通のユーティリティメソッドとContext Manager実装を提供

    Example:
        async with QdrantManager(config, embedding_gen) as client:
            result = await client.search("query text")
    """

    def __init__(self):
        self._initialized = False

    async def __aenter__(self) -> "VectorStoreClientBase":
        """Context Manager: 開始時に初期化"""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context Manager: 終了時にクローズ"""
        await self.close()

    def is_initialized(self) -> bool:
        """初期化されているかどうか"""
        return self._initialized

    async def ensure_initialized(self) -> None:
        """初期化されていなければ初期化"""
        if not self._initialized:
            await self.initialize()

    @abstractmethod
    async def initialize(self) -> None:
        """クライアントを初期化"""
        pass

    @abstractmethod
    async def upsert(
        self,
        point_id: str,
        text: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """ベクトルデータをUpsert"""
        pass

    @abstractmethod
    async def batch_upsert(
        self,
        items: List[Dict[str, Any]],
        batch_size: int = 256,
    ) -> Dict[str, Any]:
        """バッチUpsert"""
        pass

    @abstractmethod
    async def search(
        self,
        query_text: str,
        limit: int = 10,
        score_threshold: float = 0.4,
        filter_conditions: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """セマンティック検索"""
        pass

    @abstractmethod
    async def delete(self, point_ids: List[str]) -> Dict[str, Any]:
        """ポイントを削除"""
        pass

    @abstractmethod
    async def get_statistics(self) -> Dict[str, Any]:
        """統計情報を取得"""
        pass

    @abstractmethod
    async def close(self) -> None:
        """クライアントをクローズ"""
        pass
