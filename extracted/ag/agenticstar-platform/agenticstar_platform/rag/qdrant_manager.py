"""
AGENTICSTAR Platform SDK - Qdrant Manager
Qdrantベクトルデータベース操作機能を提供

汎用ベクトルDB操作（ビジネスロジック非依存）
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field

from urllib.parse import urlparse

from .._config_utils import load_toml_section

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    SearchParams,
    HnswConfigDiff,
    OptimizersConfigDiff,
)

from .base import (
    VectorStoreError,
    VectorStoreConfigError,
    VectorStoreConnectionError,
)
from .embedding import EmbeddingGenerator


logger = logging.getLogger(__name__)


class QdrantConfigError(VectorStoreConfigError):
    """Qdrant設定エラー

    VectorStoreConfigError を継承し、VectorStoreError 階層に属する。
    これにより except VectorStoreConfigError / except VectorStoreError でも捕捉可能。
    """
    pass


@dataclass
class PayloadIndexConfig:
    """Payload Index設定

    Example:
        >>> index = PayloadIndexConfig(field_name="category", field_schema="keyword")
    """
    field_name: str
    field_schema: str = "keyword"  # keyword, integer, float, bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PayloadIndexConfig":
        """辞書からPayloadIndexConfigを作成"""
        return cls(
            field_name=data["field_name"],
            field_schema=data.get("field_schema", "keyword"),
        )


@dataclass
class QdrantConfig:
    """Qdrant設定

    Example:
        >>> # 辞書から作成
        >>> config = QdrantConfig.from_dict({
        ...     "url": "http://localhost:6333",
        ...     "collection_name": "my_collection",
        ...     "vector_size": 1536
        ... })

        >>> # TOMLファイルから作成
        >>> config = QdrantConfig.from_toml("config.toml", section="rag.qdrant")
    """
    url: str
    collection_name: str
    vector_size: int = 1536  # text-embedding-ada-002
    distance: str = "cosine"  # cosine, euclid, dot
    on_disk_vectors: bool = False
    on_disk_payload: bool = True
    hnsw_m: int = 16
    hnsw_ef_construct: int = 256
    # レプリケーション設定（未指定だとQdrantデフォルトRF=1となり、Pod障害時に
    # データの一部が読み書き不能になる）。cluster peer数より大きい値を指定しても
    # Qdrantは実配置を利用可能なpeer数へ自動調整するため、単一ノード構成でも安全。
    replication_factor: int = 3
    write_consistency_factor: int = 2
    # Payload Indexes（カスタマイズ可能）
    payload_indexes: List[PayloadIndexConfig] = field(default_factory=lambda: [
        PayloadIndexConfig(field_name="content_type", field_schema="keyword"),
        PayloadIndexConfig(field_name="created_at", field_schema="integer"),
    ])
    # 認証トークン取得関数（QdrantClientのauth_token_providerに渡す）
    auth_token_provider: Optional[Callable[[], str]] = None
    # gRPC使用（直結時はTrue推奨、HTTP API経由時はFalse）
    prefer_grpc: bool = True
    # 互換性チェック（HTTP API経由時はFalse推奨）
    check_compatibility: bool = True

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QdrantConfig":
        """辞書からQdrantConfigを作成

        Args:
            data: 設定辞書

        Returns:
            QdrantConfig instance

        Example:
            >>> config = QdrantConfig.from_dict({
            ...     "url": "http://localhost:6333",
            ...     "collection_name": "my_collection",
            ...     "vector_size": 1536,
            ...     "distance": "cosine"
            ... })
        """
        # payload_indexesがある場合は変換
        payload_indexes = None
        if "payload_indexes" in data:
            payload_indexes = [
                PayloadIndexConfig.from_dict(idx) if isinstance(idx, dict) else idx
                for idx in data["payload_indexes"]
            ]

        return cls(
            url=data["url"],
            collection_name=data["collection_name"],
            vector_size=data.get("vector_size", 1536),
            distance=data.get("distance", "cosine"),
            on_disk_vectors=data.get("on_disk_vectors", False),
            on_disk_payload=data.get("on_disk_payload", True),
            hnsw_m=data.get("hnsw_m", 16),
            hnsw_ef_construct=data.get("hnsw_ef_construct", 256),
            replication_factor=data.get("replication_factor", 3),
            write_consistency_factor=data.get("write_consistency_factor", 2),
            payload_indexes=payload_indexes if payload_indexes else [
                PayloadIndexConfig(field_name="content_type", field_schema="keyword"),
                PayloadIndexConfig(field_name="created_at", field_schema="integer"),
            ],
            # auth_token_providerは辞書から設定不可（コールバック関数のため）
        )

    @classmethod
    def from_toml(cls, toml_path: str, section: str = "rag.qdrant") -> "QdrantConfig":
        """TOMLファイルからQdrantConfigを作成

        Args:
            toml_path: TOMLファイルパス
            section: セクション名（ドット区切りでネスト対応）

        Returns:
            QdrantConfig instance

        Example:
            >>> # config.toml の [rag.qdrant] セクションを読み込み
            >>> config = QdrantConfig.from_toml("config.toml")

            >>> # カスタムセクション
            >>> config = QdrantConfig.from_toml("config.toml", section="vectordb")
        """
        data = load_toml_section(toml_path, section)
        return cls.from_dict(data)


class QdrantManager:
    """
    Qdrant操作クラス

    ベクトルデータベースQdrantへのアクセスを提供します。
    テキストの埋め込み生成とベクトル検索を統合的に扱えます。

    Features:
        - Collection自動作成（HNSW最適化設定）
        - Payload Index作成（検索フィルタ用）
        - Upsert/Batch Upsert (冪等性保証 - 同一IDは上書き)
        - Semantic Search (フィルタ対応)
        - 統計情報取得

    Example:
        >>> from agenticstar_platform import QdrantManager, QdrantConfig, EmbeddingGenerator, EmbeddingConfig
        >>>
        >>> # 設定を作成
        >>> embedding_config = EmbeddingConfig.from_toml("config.toml", section="rag.embedding")
        >>> qdrant_config = QdrantConfig.from_toml("config.toml", section="rag.qdrant")
        >>>
        >>> # Embeddingジェネレーター作成
        >>> embedding_gen = EmbeddingGenerator(embedding_config)
        >>>
        >>> # コンテキストマネージャーで使用（推奨）
        >>> async with QdrantManager(qdrant_config, embedding_gen) as manager:
        ...     # データ追加
        ...     await manager.upsert(
        ...         id="doc-001",
        ...         content="AIエージェントの設計パターン",
        ...         metadata={"category": "technical", "author": "John"}
        ...     )
        ...
        ...     # 検索
        ...     results = await manager.search(
        ...         query_text="エージェント設計",
        ...         limit=5,
        ...         filter_conditions={"category": "technical"}
        ...     )
        ...     for hit in results["data"]["results"]:
        ...         print(f"Score: {hit['score']:.3f} - {hit['payload']}")
    """

    def __init__(
        self,
        config: QdrantConfig,
        embedding_generator: EmbeddingGenerator,
    ):
        """
        Initialize Qdrant Manager

        Args:
            config: QdrantConfig instance
            embedding_generator: EmbeddingGenerator instance

        Raises:
            QdrantConfigError: vector_sizeとembedding dimensionsの不一致
        """
        # vector_size検証
        if config.vector_size != embedding_generator.dimensions:
            raise QdrantConfigError(
                f"Vector size mismatch: QdrantConfig.vector_size={config.vector_size} "
                f"!= EmbeddingConfig.dimensions={embedding_generator.dimensions}. "
                f"These values must match for proper vector storage."
            )

        # auth_token_provider設定時はhost/port/https/prefixで明示的に指定
        # （QdrantClientはurlパラメータ使用時にポート6333へデフォルト接続するため）
        if config.auth_token_provider is not None:
            parsed = urlparse(config.url)
            host = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == "https" else 80)
            https = parsed.scheme == "https"
            prefix = parsed.path.lstrip("/") if parsed.path and parsed.path != "/" else None

            logger.info(
                f"QdrantManager auth mode - host={host}, port={port}, "
                f"https={https}, prefix={prefix}, prefer_grpc={config.prefer_grpc}"
            )

            self.client = QdrantClient(
                host=host,
                port=port,
                https=https,
                prefix=prefix,
                auth_token_provider=config.auth_token_provider,
                prefer_grpc=config.prefer_grpc,
                check_compatibility=config.check_compatibility,
            )
        else:
            self.client = QdrantClient(
                url=config.url,
                prefer_grpc=config.prefer_grpc,
                check_compatibility=config.check_compatibility,
            )

        self.config = config
        self.collection_name = config.collection_name
        self.embedding_generator = embedding_generator
        self._initialized = False

        logger.info(
            f"QdrantManager initialized - url={config.url}, "
            f"collection={config.collection_name}, vector_size={config.vector_size}"
        )

    async def __aenter__(self) -> "QdrantManager":
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

    async def initialize(self) -> None:
        """
        Collection存在確認・作成・Index作成

        Raises:
            VectorStoreConnectionError: Qdrant初期化に失敗した場合
                （元例外は __cause__ に保持）。
                既に VectorStoreError 階層の例外（例: VectorStoreConfigError）が
                発生した場合は、その型を保ったまま伝播する。
        """
        if self._initialized:
            logger.debug("QdrantManager already initialized")
            return

        logger.info(f"Initializing QdrantManager - collection={self.collection_name}")

        try:
            # Collection existence check (sync call → asyncio.to_thread)
            collections_response = await asyncio.to_thread(
                self.client.get_collections
            )
            collection_names = [col.name for col in collections_response.collections]

            if self.collection_name not in collection_names:
                logger.info(f"Creating collection: {self.collection_name}")
                await self._create_collection()
            else:
                logger.info(f"Collection already exists: {self.collection_name}")

            # Payload index の作成は冪等（既存フィールドへの再作成は no-op）なので、
            # collection が新規/既存いずれの場合も毎回 ensure する。
            # これにより index 作成が途中失敗して再初期化した場合でも
            # （collection は既に存在し else 分岐に入っても）index が確実に作成され、
            # 「_initialized=True なのに index 未作成」という非冪等バグを防ぐ。
            await self._create_payload_indices()

            self._initialized = True
            logger.info("QdrantManager initialized successfully")

        except VectorStoreError:
            # 既に階層化された例外（config/connection）は型を保ったまま伝播させ、
            # Connection への誤ラベル（二重ラップ）を避ける
            raise
        except Exception as e:
            logger.error(f"Failed to initialize QdrantManager: {e}")
            raise VectorStoreConnectionError(
                f"Qdrant initialization failed: {e}"
            ) from e

    async def _create_collection(self) -> None:
        """
        Create Qdrant collection with optimized settings
        """
        # Distance mapping
        distance_map = {
            "cosine": Distance.COSINE,
            "euclid": Distance.EUCLID,
            "dot": Distance.DOT,
        }
        distance = distance_map.get(self.config.distance, Distance.COSINE)

        await asyncio.to_thread(
            self.client.create_collection,
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.config.vector_size,
                distance=distance,
                on_disk=self.config.on_disk_vectors,
            ),
            hnsw_config=HnswConfigDiff(
                m=self.config.hnsw_m,
                ef_construct=self.config.hnsw_ef_construct,
                full_scan_threshold=10000,
                on_disk=True,
            ),
            optimizers_config=OptimizersConfigDiff(
                memmap_threshold=20000,
            ),
            on_disk_payload=self.config.on_disk_payload,
            replication_factor=self.config.replication_factor,
            write_consistency_factor=self.config.write_consistency_factor,
        )
        logger.info(f"Collection created: {self.collection_name}")

    async def _create_payload_indices(self) -> None:
        """
        Create payload indices for filtering performance (configurable)
        """
        for index_config in self.config.payload_indexes:
            await asyncio.to_thread(
                self.client.create_payload_index,
                collection_name=self.collection_name,
                field_name=index_config.field_name,
                field_schema=index_config.field_schema,
            )
            logger.info(f"Payload index created: {index_config.field_name}")

    async def create_payload_index(
        self,
        field_name: str,
        field_schema: str = "keyword"
    ) -> Dict[str, Any]:
        """
        カスタムPayload Indexを作成

        Args:
            field_name: フィールド名
            field_schema: スキーマタイプ ("keyword", "integer", "float", "bool")

        Returns:
            Dict with success status
        """
        try:
            await asyncio.to_thread(
                self.client.create_payload_index,
                collection_name=self.collection_name,
                field_name=field_name,
                field_schema=field_schema,
            )
            logger.info(f"Payload index created: {field_name}")
            return {"success": True, "field_name": field_name}
        except Exception as e:
            logger.error(f"Failed to create payload index: {e}")
            return {"success": False, "error": str(e), "error_code": "INDEX_CREATE_ERROR"}

    async def upsert(
        self,
        id: Optional[str] = None,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        ベクトルデータをUpsert（冪等性保証）

        テキストからEmbeddingを生成し、ベクトルデータベースに保存します。
        同一IDが既に存在する場合は上書きされます（冪等性保証）。

        Args:
            id: ドキュメントID（省略時は自動UUID生成）
            content: 埋め込み対象のテキスト
            metadata: メタデータ（検索時のフィルタリングや結果表示に使用）

        Returns:
            Dict[str, Any]: 実行結果
                - success: bool
                - data: {"id": str} (成功時)
                - error: str, error_code: str (失敗時)

        Example:
            >>> result = await manager.upsert(
            ...     id="doc-001",  # 省略可（自動UUID生成）
            ...     content="Pythonは汎用プログラミング言語です。",
            ...     metadata={"title": "Python入門", "category": "programming"}
            ... )
            >>> if result["success"]:
            ...     print(f"Added: {result['data']['id']}")

            >>> # ID自動生成
            >>> result = await manager.upsert(
            ...     content="テキスト内容",
            ...     metadata={"source": "web"}
            ... )
            >>> print(f"Auto-generated ID: {result['data']['id']}")
        """
        await self.ensure_initialized()

        import uuid as uuid_module
        actual_id = id or str(uuid_module.uuid4())
        actual_metadata = metadata or {}

        if not content:
            return {
                "success": False,
                "error": "'content' is required",
                "error_code": "MISSING_CONTENT",
            }

        try:
            logger.debug(f"Upserting point - id={actual_id}")

            # Generate embedding
            embedding = await self.embedding_generator.generate(content)

            # Add default metadata
            full_payload = {
                **actual_metadata,
                "created_at": int(datetime.now().timestamp()),
                "model_version": self.embedding_generator.model_name,
            }

            # Build Point
            point = PointStruct(
                id=actual_id,
                vector=embedding,
                payload=full_payload,
            )

            # Upsert (idempotent - same ID overwrites, sync call → asyncio.to_thread)
            await asyncio.to_thread(
                self.client.upsert,
                collection_name=self.collection_name,
                points=[point],
            )

            logger.info(f"Point upserted - id={actual_id}")
            return {"success": True, "data": {"id": actual_id}}

        except Exception as e:
            logger.error(f"Failed to upsert point: {e}")
            return {
                "success": False,
                "error": f"Upsert error: {str(e)}",
                "error_code": "QDRANT_UPSERT_ERROR",
            }

    async def batch_upsert(
        self,
        items: List[Dict[str, Any]],
        batch_size: int = 256,
    ) -> Dict[str, Any]:
        """
        バッチUpsert

        Args:
            items: List of {"id": str, "content": str, "metadata": dict}
            batch_size: バッチサイズ

        Returns:
            Dict with success status and total_upserted
        """
        await self.ensure_initialized()

        try:
            logger.info(f"Batch upserting {len(items)} points")

            total_points = 0

            for i in range(0, len(items), batch_size):
                batch = items[i : i + batch_size]

                # Extract texts and generate embeddings
                texts = [item["content"] for item in batch]
                embeddings = await self.embedding_generator.batch_generate(texts)

                # Build Points
                points = []
                for item, embedding in zip(batch, embeddings):
                    full_payload = {
                        **item.get("metadata", {}),
                        "created_at": int(datetime.now().timestamp()),
                        "model_version": self.embedding_generator.model_name,
                    }
                    points.append(
                        PointStruct(
                            id=item["id"],
                            vector=embedding,
                            payload=full_payload,
                        )
                    )

                # Batch Upsert (sync call → asyncio.to_thread)
                await asyncio.to_thread(
                    self.client.upsert,
                    collection_name=self.collection_name,
                    points=points,
                )
                total_points += len(points)

                logger.debug(f"Batch upserted {len(points)} points")

            logger.info(f"Batch upsert completed - total={total_points}")
            return {"success": True, "data": {"total_upserted": total_points}}

        except Exception as e:
            logger.error(f"Failed to batch upsert: {e}")
            return {
                "success": False,
                "error": f"Batch upsert error: {str(e)}",
                "error_code": "QDRANT_BATCH_UPSERT_ERROR",
            }

    async def search(
        self,
        query_text: str,
        limit: int = 10,
        score_threshold: float = 0.4,
        filter_conditions: Optional[Dict[str, Any]] = None,
        ef: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        セマンティック検索

        クエリテキストに意味的に近いドキュメントを検索します。
        フィルタ条件を指定して結果を絞り込むことも可能です。

        Args:
            query_text: 検索クエリ。自然言語で記述
            limit: 結果数上限（デフォルト: 10）
            score_threshold: スコア閾値 (Qdrant cosine: -1〜1、デフォルト: 0.4)
            filter_conditions: フィルタ条件 {"field": value} 形式（オプション）
            ef: HNSW検索深度 (デフォルト: limit * 2)。大きいほど精度が上がるが遅くなる

        Returns:
            Dict[str, Any]: 検索結果
                - success: bool
                - data: {
                    "query": str,
                    "results": [{"point_id": str, "payload": dict, "score": float, "similarity": float}],
                    "total_found": int,
                    "score_threshold": float
                  }
                - error: str, error_code: str (失敗時)

        Example:
            >>> # 基本的な検索
            >>> results = await manager.search(
            ...     query_text="プログラミング言語",
            ...     limit=5
            ... )
            >>> for hit in results["data"]["results"]:
            ...     print(f"Score: {hit['score']:.3f} - {hit['payload']['title']}")
            >>>
            >>> # フィルタ付き検索
            >>> results = await manager.search(
            ...     query_text="データ分析",
            ...     limit=10,
            ...     score_threshold=0.5,
            ...     filter_conditions={"category": "programming"}
            ... )
            >>> print(f"Found {results['data']['total_found']} results")
        """
        await self.ensure_initialized()

        try:
            logger.debug(
                f"Searching - query_len={len(query_text)}, limit={limit}"
            )

            # Generate query embedding
            query_vector = await self.embedding_generator.generate(query_text)

            # Build filter
            query_filter = None
            if filter_conditions:
                must_conditions = [
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value),
                    )
                    for key, value in filter_conditions.items()
                ]
                query_filter = Filter(must=must_conditions)

            # Search params
            search_params = SearchParams(
                hnsw_ef=ef or (limit * 2),
                exact=False,
            )

            # Execute search (sync call → asyncio.to_thread)
            results = await asyncio.to_thread(
                self.client.query_points,
                collection_name=self.collection_name,
                query=query_vector,
                query_filter=query_filter,
                limit=limit,
                score_threshold=score_threshold,
                search_params=search_params,
                with_payload=True,
            )

            # Format results
            formatted_results = [
                {
                    "point_id": hit.id,
                    "payload": hit.payload,
                    "score": hit.score,
                    "similarity": self._score_to_similarity(hit.score),
                }
                for hit in results.points
            ]

            logger.info(
                f"Search completed - found={len(formatted_results)}, "
                f"query_len={len(query_text)}"
            )
            return {
                "success": True,
                "data": {
                    "query": query_text,
                    "results": formatted_results,
                    "total_found": len(formatted_results),
                    "score_threshold": score_threshold,
                },
            }

        except Exception as e:
            logger.error(f"Failed to search: {e}")
            return {
                "success": False,
                "error": f"Search error: {str(e)}",
                "error_code": "QDRANT_SEARCH_ERROR",
            }

    def _score_to_similarity(self, score: float) -> float:
        """
        Qdrant cosine score (-1〜1) → 類似度 (0〜1) 変換
        """
        return max(0.0, min(1.0, (score + 1.0) / 2.0))

    async def delete(self, point_ids: List[str]) -> Dict[str, Any]:
        """
        ポイントを削除

        指定したIDのベクトルデータを削除します。

        Args:
            point_ids: 削除するポイントIDのリスト

        Returns:
            Dict[str, Any]: 削除結果
                - success: bool
                - data: {"deleted_count": int} (成功時)
                - error: str, error_code: str (失敗時)

        Example:
            >>> # 単一ポイントを削除
            >>> result = await manager.delete(["doc-001"])
            >>> print(f"Deleted: {result['data']['deleted_count']}")
            >>>
            >>> # 複数ポイントを削除
            >>> result = await manager.delete(["doc-001", "doc-002", "doc-003"])
            >>> if result["success"]:
            ...     print(f"Deleted {result['data']['deleted_count']} documents")
        """
        await self.ensure_initialized()

        try:
            # Sync call → asyncio.to_thread
            await asyncio.to_thread(
                self.client.delete,
                collection_name=self.collection_name,
                points_selector=point_ids,
            )
            logger.info(f"Deleted {len(point_ids)} points")
            return {"success": True, "data": {"deleted_count": len(point_ids)}}

        except Exception as e:
            logger.error(f"Failed to delete points: {e}")
            return {
                "success": False,
                "error": f"Delete error: {str(e)}",
                "error_code": "QDRANT_DELETE_ERROR",
            }

    async def get_statistics(self) -> Dict[str, Any]:
        """
        コレクション統計情報を取得

        コレクション内のドキュメント数やコンテンツタイプの内訳などを取得します。

        Returns:
            Dict[str, Any]: 統計情報
                - success: bool
                - data: {
                    "total_objects": int,
                    "vectors_count": int,
                    "content_type_breakdown": dict,
                    "collection_name": str,
                    "status": str
                  }
                - error: str, error_code: str (失敗時)

        Example:
            >>> stats = await manager.get_statistics()
            >>> if stats["success"]:
            ...     data = stats["data"]
            ...     print(f"Total documents: {data['total_objects']}")
            ...     print(f"Status: {data['status']}")
            ...     print("Content types:")
            ...     for ctype, count in data["content_type_breakdown"].items():
            ...         print(f"  {ctype}: {count}")
        """
        await self.ensure_initialized()

        try:
            # Sync calls → asyncio.to_thread
            collection_info = await asyncio.to_thread(
                self.client.get_collection,
                self.collection_name,
            )

            # Content type breakdown (sample 1000 points)
            scroll_result = await asyncio.to_thread(
                self.client.scroll,
                collection_name=self.collection_name,
                limit=1000,
                with_payload=["content_type"],
                with_vectors=False,
            )

            content_type_breakdown = {}
            for point in scroll_result[0]:
                content_type = point.payload.get("content_type", "unknown")
                content_type_breakdown[content_type] = (
                    content_type_breakdown.get(content_type, 0) + 1
                )

            # qdrant-client >=1.16.0 で CollectionInfo.vectors_count が削除された。
            # 属性が無い場合は実データ数寄りの points_count にフォールバックする
            # (indexed_vectors_count は未インデックス分を落とすため採用しない)。
            vectors_count = getattr(collection_info, "vectors_count", None)
            if vectors_count is None:
                vectors_count = collection_info.points_count

            stats = {
                "total_objects": collection_info.points_count,
                "vectors_count": vectors_count,
                "content_type_breakdown": content_type_breakdown,
                "collection_name": self.collection_name,
                "status": collection_info.status.value,
            }

            logger.info(f"Statistics retrieved - total={stats['total_objects']}")
            return {"success": True, "data": stats}

        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {
                "success": False,
                "error": f"Statistics error: {str(e)}",
                "error_code": "QDRANT_STATS_ERROR",
            }

    async def delete_collection(self, collection_name: Optional[str] = None) -> Dict[str, Any]:
        """
        コレクションを削除

        Args:
            collection_name: 削除するコレクション名（省略時は現在のコレクション）

        Returns:
            Dict[str, Any]: 削除結果
                - success: bool
                - data: {"collection_name": str} (成功時)
                - error: str, error_code: str (失敗時)

        Example:
            >>> # 現在のコレクションを削除
            >>> result = await manager.delete_collection()
            >>> if result["success"]:
            ...     print(f"Deleted: {result['data']['collection_name']}")

            >>> # 別のコレクションを削除
            >>> result = await manager.delete_collection("old_collection")
        """
        target_collection = collection_name or self.collection_name

        try:
            await asyncio.to_thread(
                self.client.delete_collection,
                target_collection,
            )
            logger.info(f"Collection deleted: {target_collection}")

            # 現在のコレクションを削除した場合は初期化状態をリセット
            if target_collection == self.collection_name:
                self._initialized = False

            return {"success": True, "data": {"collection_name": target_collection}}

        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
            return {
                "success": False,
                "error": f"Delete collection error: {str(e)}",
                "error_code": "QDRANT_DELETE_COLLECTION_ERROR",
            }

    async def collection_exists(self, collection_name: Optional[str] = None) -> bool:
        """
        コレクションが存在するか確認

        Args:
            collection_name: 確認するコレクション名（省略時は現在のコレクション）

        Returns:
            bool: コレクションが存在する場合True

        Example:
            >>> if await manager.collection_exists():
            ...     print("Collection exists")
            >>> else:
            ...     print("Collection does not exist")
        """
        target_collection = collection_name or self.collection_name

        try:
            collections_response = await asyncio.to_thread(
                self.client.get_collections
            )
            collection_names = [col.name for col in collections_response.collections]
            return target_collection in collection_names

        except Exception as e:
            logger.error(f"Failed to check collection existence: {e}")
            return False

    async def close(self) -> None:
        """
        Close Qdrant client

        Note:
            例外が発生してもリソースを確実にクリーンアップします。
        """
        try:
            logger.info("Closing QdrantManager")
            # Qdrantクライアントのクローズ処理（必要に応じて）
            if self.client and hasattr(self.client, 'close'):
                self.client.close()
        except Exception as e:
            logger.warning(f"Error closing Qdrant client: {e}")
        finally:
            self.client = None
            self._initialized = False
            logger.debug("QdrantManager closed")
