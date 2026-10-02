"""
AGENTICSTAR Platform SDK - Embedding Generator
Azure OpenAI Embedding生成機能を提供

汎用Embedding生成（ビジネスロジック非依存）
"""

import asyncio
import hashlib
import logging
import random
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from .._config_utils import load_toml_section

from openai import AsyncAzureOpenAI, AsyncOpenAI

try:
    import tiktoken
except ImportError:  # pragma: no cover - tiktoken はオプション（無ければ char fallback）
    tiktoken = None  # type: ignore[assignment]


logger = logging.getLogger(__name__)

# embedding 入力の token 予算（8192 上限系への安全マージン）
_EMBED_TOKEN_BUDGET = 8000
# Cohere embed-v4 等の 128k 系。cl100k は Cohere tokenizer と一致しないため
# 実上限 128k に対して余裕を持った sanity cap
_EMBED_TOKEN_BUDGET_LONG_CONTEXT = 100_000

_encoder_cache: List[Any] = []  # [encoder or None] 判定済みなら要素1つ


def _budget_for_model(model: str) -> int:
    """モデル名から embedding token 予算を決める。"""
    if isinstance(model, str) and "embed-v" in model.lower():
        return _EMBED_TOKEN_BUDGET_LONG_CONTEXT
    return _EMBED_TOKEN_BUDGET


def _get_embed_encoder():
    """cl100k_base エンコーダを遅延初期化して返す（利用不可なら None）"""
    if not _encoder_cache:
        encoder = None
        if tiktoken is not None:
            try:
                encoder = tiktoken.get_encoding("cl100k_base")
            except Exception as e:  # pragma: no cover
                logger.warning(f"tiktoken encoder unavailable, using char fallback: {e}")
        _encoder_cache.append(encoder)
    return _encoder_cache[0]


def _truncate_for_embedding(text: str, max_tokens: int) -> str:
    """embedding 入力を max_tokens 以内に切り詰める（超過時のみ動作）。

    トークン上限超過による 400 を防ぐ。encoder 不在時は char 数で保守的に
    切り詰める（CJK ~2 tokens/char 想定で max_tokens//2 文字）。
    """
    if not isinstance(text, str) or not text:
        return text
    encoder = _get_embed_encoder()
    if encoder is None:
        char_fallback = max_tokens // 2
        if len(text) > char_fallback:
            logger.warning(
                f"Embedding input truncated (char fallback) - {len(text)} -> {char_fallback} chars"
            )
            return text[:char_fallback]
        return text
    # disallowed_special=(): "<|endoftext|>" 等のリテラルで encode が例外化するのを回避
    tokens = encoder.encode(text, disallowed_special=())
    if len(tokens) <= max_tokens:
        return text
    truncated = encoder.decode(tokens[:max_tokens]).rstrip("�")
    logger.warning(
        f"Embedding input truncated - {len(tokens)} -> {max_tokens} tokens "
        f"({len(text)} -> {len(truncated)} chars)"
    )
    return truncated


class EmbeddingError(Exception):
    """Embedding生成エラー"""
    pass


class RateLimitExceededError(EmbeddingError):
    """レートリミット超過エラー"""
    pass


@dataclass
class EmbeddingConfig:
    """Embedding設定

    Azure OpenAI Embedding APIへの接続設定を管理します。

    Attributes:
        base_url: Azure OpenAI エンドポイントURL（例: "https://your-resource.openai.azure.com/"）
        api_key: APIキー
        model: デプロイメント名/モデル名（例: "text-embedding-3-small"）
        api_version: APIバージョン（デフォルト: "2024-02-15-preview"）
        dimensions: Embedding次元数（text-embedding-3-smallは1536）
        max_cache_size: キャッシュ最大サイズ（デフォルト: 10000）
        max_retries: リトライ回数（デフォルト: 5）
        base_delay: 基本待機時間秒（デフォルト: 1.0）
        max_delay: 最大待機時間秒（デフォルト: 60.0）

    Example:
        >>> # 標準的な作成方法
        >>> config = EmbeddingConfig(
        ...     base_url="https://your-resource.openai.azure.com/",
        ...     api_key="your-api-key",
        ...     model="text-embedding-3-small",
        ...     dimensions=1536,
        ... )

        >>> # 辞書から作成
        >>> config = EmbeddingConfig.from_dict({
        ...     "base_url": "https://your-resource.openai.azure.com/",
        ...     "api_key": "your-api-key",
        ...     "model": "text-embedding-3-small"
        ... })

        >>> # TOMLファイルから作成
        >>> config = EmbeddingConfig.from_toml("config.toml", section="rag.embedding")
    """
    # 標準パラメータ名（業界標準に準拠）
    base_url: str
    api_key: str
    model: str = "text-embedding-ada-002"
    api_version: str = "2024-02-15-preview"
    max_cache_size: int = 10000
    dimensions: int = 1536  # text-embedding-ada-002のデフォルト
    # 接続プロバイダー: "azure" = Azure OpenAI (deployments パス) /
    # "openai" = OpenAI 互換エンドポイント (Azure AI inference の embed-v-4-0 等。
    # base_url に /models まで含めて指定し、api_version は使わない)
    provider: str = "azure"
    # リトライ設定
    max_retries: int = 5
    base_delay: float = 1.0
    max_delay: float = 60.0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EmbeddingConfig":
        """辞書からEmbeddingConfigを作成

        Args:
            data: 設定辞書（base_url, api_key, model 等）

        Returns:
            EmbeddingConfig instance

        Example:
            >>> config = EmbeddingConfig.from_dict({
            ...     "base_url": "https://your-resource.openai.azure.com/",
            ...     "api_key": "your-api-key",
            ...     "model": "text-embedding-3-small",
            ...     "dimensions": 1536
            ... })
        """
        base_url = data.get("base_url")
        if not base_url:
            raise ValueError("'base_url' is required")

        model = data.get("model", "text-embedding-ada-002")

        return cls(
            base_url=base_url,
            api_key=data["api_key"],
            model=model,
            api_version=data.get("api_version", "2024-02-15-preview"),
            max_cache_size=data.get("max_cache_size", 10000),
            dimensions=data.get("dimensions", 1536),
            provider=data.get("provider", "azure"),
            max_retries=data.get("max_retries", 5),
            base_delay=data.get("base_delay", 1.0),
            max_delay=data.get("max_delay", 60.0),
        )

    @classmethod
    def from_toml(cls, toml_path: str, section: str = "rag.embedding") -> "EmbeddingConfig":
        """TOMLファイルからEmbeddingConfigを作成

        Args:
            toml_path: TOMLファイルパス
            section: セクション名（ドット区切りでネスト対応）

        Returns:
            EmbeddingConfig instance

        Example:
            >>> # config.toml の [rag.embedding] セクションを読み込み
            >>> config = EmbeddingConfig.from_toml("config.toml")
        """
        data = load_toml_section(toml_path, section)
        return cls.from_dict(data)


class EmbeddingGenerator:
    """
    Azure OpenAI Embedding生成クラス

    テキストをベクトル表現に変換します。
    LRUキャッシュとレートリミット対応により、効率的かつ安定的にEmbeddingを生成します。

    Features:
        - 非同期バッチEmbedding生成（batch_generate）
        - LRUメモリキャッシュによる重複リクエスト削減
        - 指数バックオフ+ジッターによるレートリミット対応
        - Azure OpenAI text-embedding-ada-002モデル対応
        - キャッシュ統計とキャッシュクリア機能

    Example:
        >>> from agenticstar_platform import EmbeddingGenerator, EmbeddingConfig
        >>>
        >>> # 設定を作成
        >>> config = EmbeddingConfig.from_toml("config.toml", section="rag.embedding")
        >>>
        >>> # クライアント初期化
        >>> generator = EmbeddingGenerator(config)
        >>>
        >>> # 単一テキストのEmbedding生成
        >>> embedding = await generator.generate("Azure OpenAIの使い方を教えてください")
        >>> print(f"Embedding dimensions: {len(embedding)}")  # 1536
        >>>
        >>> # バッチEmbedding生成（効率的）
        >>> texts = ["テキスト1", "テキスト2", "テキスト3"]
        >>> embeddings = await generator.batch_generate(texts, batch_size=16)
        >>> print(f"Generated {len(embeddings)} embeddings")
        >>>
        >>> # キャッシュ統計確認
        >>> stats = generator.get_cache_stats()
        >>> print(f"Cache utilization: {stats['cache_utilization']:.1%}")
    """

    def __init__(self, config: EmbeddingConfig):
        """
        Initialize Embedding Generator

        Args:
            config: EmbeddingConfig instance
        """
        # LiteLLM 形式 ("azure/xxx" / "openai/xxx") の model が渡された場合は
        # プレフィックスから provider を導出し、デプロイメント名からは剥がす。
        # (DB agent_configurations の設定をそのまま渡す利用者への互換)
        model = config.model
        provider = config.provider
        if "/" in model:
            prefix, model = model.split("/", 1)
            prefix_lower = prefix.lower()
            if prefix_lower in ("azure", "azure_openai", "azure-openai"):
                provider = "azure"
            elif prefix_lower == "openai":
                provider = "openai"
            # 他プレフィックス（bedrock 等）は本クライアント非対応のため config.provider に従う

        if provider == "openai":
            # OpenAI 互換エンドポイント（Azure AI inference の embed-v-4-0 等）。
            # base_url は /models まで含む完全な互換 URL を渡す。
            self.client = AsyncOpenAI(
                base_url=config.base_url,
                api_key=config.api_key,
            )
        else:
            self.client = AsyncAzureOpenAI(
                azure_endpoint=config.base_url,
                api_key=config.api_key,
                api_version=config.api_version,
            )
        self.deployment_name = model
        # embedding token 予算（モデル別: 8192 上限系 8000 / embed-v4 等 128k 系 100k）
        self._token_budget = _budget_for_model(model)
        self.model_name = config.model  # For model_version tracking
        self.dimensions = config.dimensions

        # リトライ設定
        self._max_retries = config.max_retries
        self._base_delay = config.base_delay
        self._max_delay = config.max_delay

        # LRU Cache
        self._memory_cache: Dict[str, List[float]] = {}
        self._cache_order: List[str] = []  # LRU tracking
        self._max_cache_size = config.max_cache_size

        logger.info(
            f"EmbeddingGenerator initialized - model={config.model}, "
            f"cache_size={config.max_cache_size}, max_retries={config.max_retries}"
        )

    async def generate(self, text: str) -> List[float]:
        """
        単一テキストのEmbeddingを生成（キャッシュ対応）

        同一テキストは自動的にキャッシュからEmbeddingを取得します。
        レートリミットに達した場合は自動リトライを行います。

        Args:
            text: Embedding対象のテキスト

        Returns:
            List[float]: Embeddingベクトル（text-embedding-ada-002の場合は1536次元）

        Raises:
            RateLimitExceededError: レートリミット超過でリトライ上限到達時
            EmbeddingError: その他のAPIエラー

        Example:
            >>> # 単一テキストのEmbedding生成
            >>> embedding = await generator.generate("質問に回答する方法")
            >>> print(f"Dimensions: {len(embedding)}")  # 1536
            >>>
            >>> # キャッシュ済みの場合は即座に返る
            >>> embedding_cached = await generator.generate("質問に回答する方法")
        """
        # トークン上限超過による 400 を防ぐ（キャッシュキーも切り詰め後で統一）
        text = _truncate_for_embedding(text, self._token_budget)

        # Cache key
        cache_key = self._make_cache_key(text)

        # Cache check
        if cache_key in self._memory_cache:
            logger.debug(f"Cache hit for key={cache_key[:16]}...")
            return self._memory_cache[cache_key]

        # API call with retry
        last_error = None
        for attempt in range(self._max_retries):
            try:
                logger.debug(f"Generating embedding - text_len={len(text)} chars, attempt={attempt + 1}")
                # molt#1329: 単一入力も 1 要素 list で送る。Azure AI Foundry Models API
                # (embed-v-4-0 等の OpenAI 互換 endpoint) は input に list を要求し、
                # 素の文字列は 422 "Input should be a valid list" になる。list 入力は
                # OpenAI / Azure OpenAI 双方が受理し、応答 shape (data[0].embedding) も不変。
                response = await self.client.embeddings.create(
                    input=[text], model=self.deployment_name
                )
                embedding = response.data[0].embedding

                # Cache update
                self._update_memory_cache(cache_key, embedding)

                logger.debug(f"Embedding generated - dims={len(embedding)}")
                return embedding

            except Exception as e:
                last_error = e
                if "429" in str(e) or "rate" in str(e).lower():
                    delay = self._calculate_backoff_delay(attempt)
                    logger.warning(
                        f"Rate limit hit (attempt {attempt + 1}/{self._max_retries}), "
                        f"retrying after {delay:.1f}s..."
                    )
                    await asyncio.sleep(delay)
                    continue
                else:
                    logger.error(f"Embedding generation failed: {e}")
                    raise EmbeddingError(f"Embedding generation failed: {e}") from e

        # リトライ上限到達
        raise RateLimitExceededError(
            f"Rate limit exceeded after {self._max_retries} retries: {last_error}"
        )

    async def batch_generate(
        self, texts: List[str], batch_size: int = 16
    ) -> List[List[float]]:
        """
        複数テキストのEmbeddingを一括生成（バッチ処理）

        大量のテキストを効率的にEmbedding化します。
        キャッシュ済みのテキストはスキップし、APIコール数を削減します。

        Args:
            texts: Embedding対象のテキストリスト
            batch_size: APIバッチサイズ（推奨: 16-32）。大きすぎるとレートリミットに達しやすくなる

        Returns:
            List[List[float]]: Embeddingベクトルのリスト（入力と同じ順序）

        Raises:
            RateLimitExceededError: レートリミット超過でリトライ上限到達時
            EmbeddingError: その他のAPIエラー

        Example:
            >>> # バッチEmbedding生成
            >>> texts = [
            ...     "ドキュメント1の内容",
            ...     "ドキュメント2の内容",
            ...     "ドキュメント3の内容"
            ... ]
            >>> embeddings = await generator.batch_generate(texts, batch_size=16)
            >>> print(f"Generated {len(embeddings)} embeddings")
            >>>
            >>> # 各Embeddingを確認
            >>> for i, emb in enumerate(embeddings):
            ...     print(f"Text {i}: {len(emb)} dimensions")
        """
        logger.info(
            f"Batch embedding generation - texts={len(texts)}, "
            f"batch_size={batch_size}"
        )

        # トークン上限超過による 400 を防ぐ（キャッシュキーも切り詰め後で統一）
        texts = [_truncate_for_embedding(t, self._token_budget) for t in texts]

        # Check cache
        embeddings: List[Optional[List[float]]] = []
        uncached_texts: List[str] = []
        uncached_indices: List[int] = []

        for i, text in enumerate(texts):
            cache_key = self._make_cache_key(text)
            if cache_key in self._memory_cache:
                embeddings.append(self._memory_cache[cache_key])
            else:
                uncached_texts.append(text)
                uncached_indices.append(i)
                embeddings.append(None)  # Placeholder

        logger.debug(
            f"Cache hits: {len(texts) - len(uncached_texts)}/{len(texts)}"
        )

        # Batch process uncached texts
        if uncached_texts:
            i = 0
            while i < len(uncached_texts):
                batch = uncached_texts[i : i + batch_size]
                batch_indices = uncached_indices[i : i + batch_size]

                last_error = None
                for attempt in range(self._max_retries):
                    try:
                        response = await self.client.embeddings.create(
                            input=batch, model=self.deployment_name
                        )

                        # Map back to original indices
                        for j, embedding_obj in enumerate(response.data):
                            original_index = batch_indices[j]
                            embedding = embedding_obj.embedding
                            embeddings[original_index] = embedding

                            # Cache update
                            cache_key = self._make_cache_key(batch[j])
                            self._update_memory_cache(cache_key, embedding)

                        # Success - move to next batch
                        break

                    except Exception as e:
                        last_error = e
                        if "429" in str(e) or "rate" in str(e).lower():
                            delay = self._calculate_backoff_delay(attempt)
                            logger.warning(
                                f"Rate limit hit in batch (attempt {attempt + 1}/{self._max_retries}), "
                                f"retrying after {delay:.1f}s..."
                            )
                            await asyncio.sleep(delay)
                            continue
                        else:
                            logger.error(f"Batch embedding failed: {e}")
                            raise EmbeddingError(f"Batch embedding failed: {e}") from e
                else:
                    # リトライ上限到達
                    raise RateLimitExceededError(
                        f"Rate limit exceeded after {self._max_retries} retries: {last_error}"
                    )

                i += batch_size

        return embeddings  # type: ignore

    def _calculate_backoff_delay(self, attempt: int) -> float:
        """
        指数バックオフ + ジッターでディレイを計算

        Args:
            attempt: 現在のリトライ回数 (0-indexed)

        Returns:
            待機時間（秒）
        """
        # 指数バックオフ: base_delay * 2^attempt
        delay = self._base_delay * (2 ** attempt)
        # 上限適用
        delay = min(delay, self._max_delay)
        # ジッター追加 (±25%)
        jitter = delay * 0.25 * (2 * random.random() - 1)
        return delay + jitter

    def _make_cache_key(self, text: str) -> str:
        """
        Generate cache key (model_name + text_hash)

        Args:
            text: Input text

        Returns:
            Cache key string
        """
        text_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
        return f"{self.model_name}:{text_hash}"

    def _update_memory_cache(self, key: str, embedding: List[float]) -> None:
        """
        Update LRU cache

        Args:
            key: Cache key
            embedding: Embedding vector
        """
        if key in self._memory_cache:
            # Update order for existing key
            self._cache_order.remove(key)
        elif len(self._memory_cache) >= self._max_cache_size:
            # Evict oldest entry
            oldest_key = self._cache_order.pop(0)
            del self._memory_cache[oldest_key]
            logger.debug(f"Cache evicted - key={oldest_key[:16]}...")

        self._memory_cache[key] = embedding
        self._cache_order.append(key)

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        キャッシュ統計情報を取得

        キャッシュの使用状況を確認し、必要に応じてクリアするか判断できます。

        Returns:
            Dict[str, Any]: キャッシュ統計情報
                - cache_size: 現在のキャッシュエントリ数
                - max_cache_size: 最大キャッシュサイズ
                - cache_utilization: キャッシュ使用率（0.0〜1.0）
                - model_name: 使用中のモデル名

        Example:
            >>> stats = generator.get_cache_stats()
            >>> print(f"Cache: {stats['cache_size']}/{stats['max_cache_size']}")
            >>> print(f"Utilization: {stats['cache_utilization']:.1%}")
            >>> if stats['cache_utilization'] > 0.9:
            ...     generator.clear_cache()
        """
        return {
            "cache_size": len(self._memory_cache),
            "max_cache_size": self._max_cache_size,
            "cache_utilization": len(self._memory_cache) / self._max_cache_size if self._max_cache_size > 0 else 0,
            "model_name": self.model_name,
        }

    def clear_cache(self) -> None:
        """
        キャッシュを全クリア

        メモリ使用量が増えた場合や、新しいモデルに切り替える場合に使用します。

        Example:
            >>> # キャッシュ統計確認
            >>> stats = generator.get_cache_stats()
            >>> print(f"Before: {stats['cache_size']} entries")
            >>>
            >>> # キャッシュクリア
            >>> generator.clear_cache()
            >>> print(f"After: {generator.get_cache_stats()['cache_size']} entries")  # 0
        """
        self._memory_cache.clear()
        self._cache_order.clear()
        logger.info("Embedding cache cleared")
