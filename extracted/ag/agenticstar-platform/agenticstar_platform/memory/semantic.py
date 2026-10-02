"""
AGENTICSTAR Platform SDK - Semantic Memory (Mem0)
汎用セマンティックメモリクライアント

組織階層やPIIマスキングは提供せず、一般的なメモリ保存・検索機能を提供
"""

import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .._config_utils import load_toml_section

logger = logging.getLogger(__name__)

# Module-level flag to track telemetry setup
_telemetry_configured = False


def _configure_mem0_telemetry() -> None:
    """Mem0のテレメトリと設定を無効化（初回のみ実行）"""
    global _telemetry_configured
    if _telemetry_configured:
        return

    # Disable Mem0 config file creation and telemetry
    os.environ["MEM0_TELEMETRY"] = "false"
    os.environ["MEM0_CONFIG_PATH"] = "/dev/null"

    # Suppress mem0 verbose logging
    logging.getLogger("mem0").setLevel(logging.WARNING)
    logging.getLogger("mem0.memory").setLevel(logging.WARNING)
    logging.getLogger("mem0.memory.main").setLevel(logging.WARNING)

    _telemetry_configured = True
    logger.debug("Mem0 telemetry and logging configured")


class SemanticMemoryError(Exception):
    """Semantic Memory操作エラー"""
    pass


class SemanticMemoryConfigError(SemanticMemoryError):
    """Semantic Memory設定エラー"""
    pass


# ============================================================
# 共通ユーティリティ関数（autonomousからも使用可能）
# ============================================================

def normalize_provider(provider: str) -> str:
    """プロバイダー名を正規化（エイリアス対応）

    Args:
        provider: プロバイダー名

    Returns:
        正規化されたプロバイダー名
    """
    provider_aliases = {
        # Azure
        "azure": "azure",
        "azure_openai": "azure",
        "azure-openai": "azure",
        # Bedrock
        "bedrock": "bedrock",
        "aws_bedrock": "bedrock",
        "aws-bedrock": "bedrock",
        # Google
        "gemini": "gemini",
        "google": "gemini",
        "google-genai": "gemini",
        "google_genai": "gemini",
    }
    return provider_aliases.get(provider.lower(), provider.lower())


def parse_model_string(model: str) -> tuple[str, str]:
    """モデル文字列をプロバイダーとモデル名に分離

    Args:
        model: "provider/model-name" or "model-name" format

    Returns:
        (provider, model_name) tuple
    """
    if "/" in model:
        provider = model.split("/")[0]
        model_name = model.split("/", 1)[1]
    else:
        provider = "openai"
        model_name = model
    return normalize_provider(provider), model_name


def mem0_classification_model(model: str) -> str:
    """mem0 の ``_is_reasoning_model`` 判定用の model 名を返す。

    mem0 2.x は gpt-5.x 系を非 reasoning 扱いして ``max_tokens`` を送出するが、
    Azure の gpt-5.x デプロイは ``max_tokens`` を拒否し ``max_completion_tokens``
    を要求する（→ ``memory.add`` が 400）。実 API の宛先は ``azure_deployment`` が
    決めるため、mem0 の分類用 ``model`` だけを reasoning と認識されるトークンへ
    正規化して ``max_tokens`` の送出を抑止する。

    - ``gpt-5*`` → ``"gpt-5"``（mem0 の reasoning 集合に存在）
    - o系 (``o1*``/``o3*``) は mem0 が prefix 判定するため実名のまま
    - それ以外（gpt-4o 等）は実名のまま（``max_tokens`` を正しく送る）
    """
    base = model.lower().rsplit("/", 1)[-1]
    if base.startswith("gpt-5"):
        return "gpt-5"
    return model


@dataclass
class LLMProviderConfig:
    """LLMプロバイダー設定

    マルチプロバイダー対応:
    - azure: Azure OpenAI
    - openai: OpenAI
    - anthropic: Anthropic Claude
    - bedrock: AWS Bedrock
    - gemini: Google Gemini
    - groq: Groq

    Example:
        >>> # 辞書から作成
        >>> config = LLMProviderConfig.from_dict({
        ...     "model": "azure/gpt-4",
        ...     "api_key": "your-api-key",
        ...     "base_url": "https://your-resource.openai.azure.com/",
        ...     "api_version": "2024-02-15-preview"
        ... })

        >>> # TOMLファイルから作成
        >>> config = LLMProviderConfig.from_toml("config.toml", section="memory.llm")
    """
    model: str  # "azure/gpt-4" or "openai/gpt-4" format
    api_key: str
    base_url: Optional[str] = None  # For Azure
    api_version: Optional[str] = None  # For Azure
    # AWS Bedrock specific
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LLMProviderConfig":
        """辞書からLLMProviderConfigを作成

        Args:
            data: 設定辞書

        Returns:
            LLMProviderConfig instance

        Example:
            >>> config = LLMProviderConfig.from_dict({
            ...     "model": "azure/gpt-4",
            ...     "api_key": "your-api-key",
            ...     "base_url": "https://your-resource.openai.azure.com/",
            ...     "api_version": "2024-02-15-preview"
            ... })
        """
        return cls(
            model=data["model"],
            api_key=data["api_key"],
            base_url=data.get("base_url"),
            api_version=data.get("api_version"),
            aws_access_key_id=data.get("aws_access_key_id"),
            aws_secret_access_key=data.get("aws_secret_access_key"),
            aws_region_name=data.get("aws_region_name"),
        )

    @classmethod
    def from_toml(cls, toml_path: str, section: str) -> "LLMProviderConfig":
        """TOMLファイルからLLMProviderConfigを作成

        Args:
            toml_path: TOMLファイルパス
            section: セクション名（ドット区切りでネスト対応）

        Returns:
            LLMProviderConfig instance

        Example:
            >>> # config.toml の [memory.llm] セクションを読み込み
            >>> config = LLMProviderConfig.from_toml("config.toml", section="memory.llm")

            >>> # embedder設定の読み込み
            >>> embedder = LLMProviderConfig.from_toml("config.toml", section="memory.embedder")
        """
        data = load_toml_section(toml_path, section)
        return cls.from_dict(data)

    @classmethod
    def from_env(cls, prefix: str = "LLM_") -> "LLMProviderConfig":
        """環境変数からLLMProviderConfigを作成

        環境変数名は {prefix}{FIELD_NAME} の形式で読み込みます。

        Args:
            prefix: 環境変数名のプレフィックス（デフォルト: "LLM_"）

        Returns:
            LLMProviderConfig instance

        Raises:
            ValueError: 必須の環境変数（MODEL, API_KEY）が設定されていない場合

        Example:
            >>> # 環境変数から作成（LLM_MODEL, LLM_API_KEY, etc.）
            >>> config = LLMProviderConfig.from_env()

            >>> # Memory用LLM設定（MEMORY_LLM_MODEL, MEMORY_LLM_API_KEY, etc.）
            >>> config = LLMProviderConfig.from_env(prefix="MEMORY_LLM_")

            >>> # Embedder設定（EMBEDDER_MODEL, EMBEDDER_API_KEY, etc.）
            >>> embedder = LLMProviderConfig.from_env(prefix="EMBEDDER_")

        Environment Variables:
            {prefix}MODEL: モデル名（必須）例: "azure/gpt-4", "openai/gpt-4"
            {prefix}API_KEY: APIキー（必須）
            {prefix}BASE_URL: ベースURL（Azure等で必要）
            {prefix}API_VERSION: APIバージョン（Azure等で必要）
            {prefix}AWS_ACCESS_KEY_ID: AWS Bedrock用
            {prefix}AWS_SECRET_ACCESS_KEY: AWS Bedrock用
            {prefix}AWS_REGION_NAME: AWS Bedrock用
        """
        def get_env(key: str) -> Optional[str]:
            return os.environ.get(f"{prefix}{key}") or None

        model = get_env("MODEL")
        api_key = get_env("API_KEY")

        if not model:
            raise ValueError(f"環境変数 {prefix}MODEL が設定されていません")
        if not api_key:
            raise ValueError(f"環境変数 {prefix}API_KEY が設定されていません")

        return cls(
            model=model,
            api_key=api_key,
            base_url=get_env("BASE_URL"),
            api_version=get_env("API_VERSION"),
            aws_access_key_id=get_env("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=get_env("AWS_SECRET_ACCESS_KEY"),
            aws_region_name=get_env("AWS_REGION_NAME"),
        )


def get_api_key(config: LLMProviderConfig) -> str:
    """APIキーを取得（SecretStr対応）

    Args:
        config: LLMProviderConfig

    Returns:
        APIキー文字列
    """
    api_key = config.api_key
    if hasattr(api_key, 'get_secret_value'):
        return api_key.get_secret_value()
    return api_key


def convert_llm_to_mem0(llm_config: LLMProviderConfig) -> Dict[str, Any]:
    """LLMProviderConfigからMem0形式のLLM設定に変換

    Args:
        llm_config: LLMProviderConfig instance

    Returns:
        Mem0形式のLLM設定dict
    """
    provider, model_name = parse_model_string(llm_config.model)
    api_key = get_api_key(llm_config)

    if provider == "azure":
        return {
            'provider': 'azure_openai',
            'config': {
                # 分類用 model（gpt-5.x の max_tokens 送出抑止）。実宛先は azure_deployment。
                'model': mem0_classification_model(model_name),
                'azure_kwargs': {
                    'api_key': api_key,
                    'azure_endpoint': llm_config.base_url,
                    'azure_deployment': model_name,
                    'api_version': llm_config.api_version or "2024-02-15-preview"
                }
            }
        }
    elif provider == "openai":
        config = {
            'model': model_name,
            'api_key': api_key,
        }
        # OpenAI 互換エンドポイント（private gateway 等）は base_url 必須。
        # 未指定なら公式 api.openai.com に接続する（embedder 側と同一契約）。
        if getattr(llm_config, 'base_url', None):
            config['openai_base_url'] = llm_config.base_url
        return {
            'provider': 'openai',
            'config': config,
        }
    elif provider == "anthropic":
        return {
            'provider': 'anthropic',
            'config': {
                'model': model_name,
                'api_key': api_key,
            }
        }
    elif provider == "bedrock":
        return {
            'provider': 'aws_bedrock',
            'config': {
                'model': model_name,
                'aws_access_key_id': llm_config.aws_access_key_id,
                'aws_secret_access_key': llm_config.aws_secret_access_key,
                'aws_region_name': llm_config.aws_region_name,
            }
        }
    elif provider == "gemini":
        return {
            'provider': 'gemini',
            'config': {
                'model': model_name,
                'api_key': api_key,
            }
        }
    elif provider == "groq":
        return {
            'provider': 'groq',
            'config': {
                'model': model_name,
                'api_key': api_key,
            }
        }
    else:
        return {
            'provider': provider,
            'config': {
                'model': model_name,
                'api_key': api_key,
            }
        }


def convert_embedder_to_mem0(embedder_config: LLMProviderConfig) -> Dict[str, Any]:
    """LLMProviderConfigからMem0形式のEmbedder設定に変換

    Args:
        embedder_config: LLMProviderConfig instance

    Returns:
        Mem0形式のEmbedder設定dict
    """
    provider, model_name = parse_model_string(embedder_config.model)
    api_key = get_api_key(embedder_config)

    if provider == "azure":
        return {
            'provider': 'azure_openai',
            'config': {
                'model': model_name,
                'azure_kwargs': {
                    'api_key': api_key,
                    'azure_endpoint': embedder_config.base_url,
                    'azure_deployment': model_name,
                    'api_version': embedder_config.api_version or "2024-02-15-preview"
                }
            }
        }
    elif provider == "openai":
        config = {
            'model': model_name,
            'api_key': api_key,
        }
        # OpenAI 互換エンドポイント（Azure AI inference の embed-v-4-0 等）は
        # base_url 必須。未指定なら公式 api.openai.com に接続する。
        if getattr(embedder_config, 'base_url', None):
            config['openai_base_url'] = embedder_config.base_url
        return {
            'provider': 'openai',
            'config': config,
        }
    elif provider == "bedrock":
        return {
            'provider': 'aws_bedrock',
            'config': {
                'model': model_name,
                'aws_access_key_id': embedder_config.aws_access_key_id,
                'aws_secret_access_key': embedder_config.aws_secret_access_key,
                'aws_region_name': embedder_config.aws_region_name,
            }
        }
    elif provider == "gemini":
        return {
            'provider': 'gemini',
            'config': {
                'model': model_name,
                'api_key': api_key,
            }
        }
    else:
        return {
            'provider': provider,
            'config': {
                'model': model_name,
                'api_key': api_key,
            }
        }


@dataclass
class QdrantVectorStoreConfig:
    """Qdrant Vector Store設定

    SemanticMemoryClientで使用するQdrant設定を簡潔に作成できます。

    Attributes:
        url: QdrantサーバーURL（例: "http://localhost:6333"）
        collection_name: コレクション名
        embedding_dims: Embedding次元数（デフォルト: 1536）

    Example:
        >>> # 簡単な作成方法
        >>> vector_config = QdrantVectorStoreConfig(
        ...     url="http://localhost:6333",
        ...     collection_name="my_memories",
        ... )
        >>>
        >>> # SemanticMemoryConfigで使用
        >>> memory_config = SemanticMemoryConfig(
        ...     llm_config=llm_config,
        ...     embedder_config=embedder_config,
        ...     vector_store=vector_config.to_dict(),
        ... )
    """
    url: str
    collection_name: str
    embedding_dims: int = 1536
    # collection先行作成時のレプリケーション設定(Mem0はRFを指定できないため、
    # SemanticMemoryClientがこの値でcollectionを先行作成する)
    replication_factor: int = 3
    write_consistency_factor: int = 2

    def to_dict(self) -> Dict[str, Any]:
        """Mem0形式の辞書に変換"""
        return {
            "provider": "qdrant",
            "config": {
                "url": self.url,
                "collection_name": self.collection_name,
                "embedding_model_dims": self.embedding_dims,
                "replication_factor": self.replication_factor,
                "write_consistency_factor": self.write_consistency_factor,
            },
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QdrantVectorStoreConfig":
        """辞書からQdrantVectorStoreConfigを作成

        Args:
            data: 設定辞書

        Returns:
            QdrantVectorStoreConfig instance
        """
        config = data.get("config", data)
        return cls(
            url=config.get("url", "http://localhost:6333"),
            collection_name=config.get("collection_name", "memories"),
            embedding_dims=config.get("embedding_model_dims", config.get("embedding_dims", 1536)),
            replication_factor=config.get("replication_factor", 3),
            write_consistency_factor=config.get("write_consistency_factor", 2),
        )


@dataclass
class SemanticMemoryConfig:
    """Semantic Memory設定

    Example:
        >>> # 辞書から作成
        >>> config = SemanticMemoryConfig.from_dict({
        ...     "llm": {
        ...         "model": "azure/gpt-4",
        ...         "api_key": "key",
        ...         "base_url": "https://...",
        ...         "api_version": "2024-02-15-preview"
        ...     },
        ...     "embedder": {
        ...         "model": "azure/text-embedding-ada-002",
        ...         "api_key": "key",
        ...         "base_url": "https://...",
        ...         "api_version": "2024-02-15-preview"
        ...     }
        ... })

        >>> # TOMLファイルから作成
        >>> config = SemanticMemoryConfig.from_toml("config.toml", section="memory")

        >>> # Qdrant Vector Store付きで作成
        >>> config = SemanticMemoryConfig(
        ...     llm_config=llm_config,
        ...     embedder_config=embedder_config,
        ...     vector_store=QdrantVectorStoreConfig(
        ...         url="http://localhost:6333",
        ...         collection_name="my_memories",
        ...     ).to_dict(),
        ... )
    """
    llm_config: LLMProviderConfig
    embedder_config: LLMProviderConfig
    vector_store: Optional[Dict[str, Any]] = None
    rerank: Optional[Dict[str, Any]] = None
    custom_fact_extraction_prompt: Optional[str] = None
    custom_update_memory_prompt: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SemanticMemoryConfig":
        """辞書からSemanticMemoryConfigを作成

        Args:
            data: 設定辞書。"llm"と"embedder"キーを含む必要がある

        Returns:
            SemanticMemoryConfig instance

        Example:
            >>> config = SemanticMemoryConfig.from_dict({
            ...     "llm": {"model": "azure/gpt-4", "api_key": "key", "base_url": "..."},
            ...     "embedder": {"model": "azure/text-embedding-ada-002", "api_key": "key", "base_url": "..."}
            ... })
        """
        return cls(
            llm_config=LLMProviderConfig.from_dict(data["llm"]),
            embedder_config=LLMProviderConfig.from_dict(data["embedder"]),
            vector_store=data.get("vector_store"),
            rerank=data.get("rerank"),
            custom_fact_extraction_prompt=data.get("custom_fact_extraction_prompt"),
            custom_update_memory_prompt=data.get("custom_update_memory_prompt"),
        )

    @classmethod
    def from_toml(cls, toml_path: str, section: str = "memory") -> "SemanticMemoryConfig":
        """TOMLファイルからSemanticMemoryConfigを作成

        Args:
            toml_path: TOMLファイルパス
            section: セクション名（ドット区切りでネスト対応）

        Returns:
            SemanticMemoryConfig instance

        Example:
            >>> # config.toml の [memory] セクションを読み込み
            >>> config = SemanticMemoryConfig.from_toml("config.toml")

            >>> # 以下のTOML構造を期待:
            >>> # [memory.llm]
            >>> # model = "azure/gpt-4"
            >>> # api_key = "..."
            >>> #
            >>> # [memory.embedder]
            >>> # model = "azure/text-embedding-ada-002"
            >>> # api_key = "..."
        """
        data = load_toml_section(toml_path, section)
        return cls.from_dict(data)


class SemanticMemoryClient:
    """
    汎用セマンティックメモリクライアント（Mem0ベース）

    会話やコンテキストをセマンティック検索可能な形式で保存・検索します。
    LLMとEmbedderを使用してメモリの抽出・ベクトル化を行います。

    Features:
        - マルチプロバイダーLLM/Embedder対応（Azure, OpenAI, Anthropic, Bedrock, Gemini, Groq）
        - 基本的なメモリ追加・検索（add, search, get_all, delete, delete_all）
        - カスタムプロンプト対応（ファクト抽出・メモリ更新プロンプトのカスタマイズ）
        - ベクトルストア設定対応（Qdrant等）

    Note:
        - 組織階層（personal/role/org/global）は提供しない（利用側で実装）
        - PIIマスキングは提供しない（利用側で実装）

    Example:
        >>> from agenticstar_platform import SemanticMemoryClient, SemanticMemoryConfig
        >>>
        >>> # 設定を作成
        >>> config = SemanticMemoryConfig.from_toml("config.toml")
        >>>
        >>> # クライアント初期化
        >>> client = SemanticMemoryClient(config)
        >>>
        >>> # メモリを追加
        >>> client.add(
        ...     messages=[
        ...         {"role": "user", "content": "私の名前は田中です"},
        ...         {"role": "assistant", "content": "こんにちは、田中さん"}
        ...     ],
        ...     user_id="user-123"
        ... )
        >>>
        >>> # メモリを検索
        >>> results = client.search(query="名前", user_id="user-123")
        >>> print(results)
        {'results': [{'memory': 'ユーザーの名前は田中', 'score': 0.95}]}
    """

    def _get_api_key(self, config: LLMProviderConfig) -> str:
        """APIキーを取得（モジュール関数 get_api_key へ委譲。SecretStr対応）"""
        return get_api_key(config)

    def _validate_provider_config(self, config: LLMProviderConfig, context: str) -> None:
        """プロバイダー固有の設定を検証

        Args:
            config: LLMProviderConfig
            context: 検証コンテキスト（エラーメッセージ用）

        Raises:
            SemanticMemoryConfigError: 必須設定が不足している場合
        """
        provider, _ = self._parse_model_string(config.model)

        if provider == "azure":
            if not config.base_url:
                raise SemanticMemoryConfigError(
                    f"{context}: Azure provider requires 'base_url' (azure_endpoint)"
                )
            if not config.api_version:
                logger.warning(
                    f"{context}: Azure provider 'api_version' not set, using default"
                )

        elif provider == "bedrock":
            missing = []
            if not config.aws_access_key_id:
                missing.append("aws_access_key_id")
            if not config.aws_secret_access_key:
                missing.append("aws_secret_access_key")
            if not config.aws_region_name:
                missing.append("aws_region_name")
            if missing:
                raise SemanticMemoryConfigError(
                    f"{context}: Bedrock provider requires: {', '.join(missing)}"
                )

    def _ensure_qdrant_collection(self, vector_store: Dict[str, Any]) -> Dict[str, Any]:
        """Qdrant collectionをレプリケーション設定付きで先行作成する

        Mem0の ``create_col`` は ``vectors_config`` のみを渡すため
        ``replication_factor`` を指定できず、Qdrantデフォルト(RF=1)で作成される。
        RF=1ではシャードが複製されないため、Pod障害時にデータの一部が読み書き
        不能になる。

        Mem0は「collectionが既に存在する場合は作成をスキップ」する実装のため、
        ここでRF付きで先行作成しておけば、Mem0はそのcollectionをそのまま使う。

        既存collectionには介入しない(既存分の是正は運用ツールで行う)。
        collection作成に失敗してもMem0初期化は継続する(RF未設定でMem0側が
        作成するため機能自体は動作する)。

        なお ``replication_factor`` / ``write_consistency_factor`` はSDK独自の
        拡張キーであり、Mem0の ``QdrantConfig`` は未知キーを拒否する
        (``validate_extra_fields``)。そのためMem0へ渡す設定からは必ず除去する。

        Args:
            vector_store: Mem0形式のvector_store設定(SDK拡張キーを含みうる)

        Returns:
            Mem0へ渡せるようSDK拡張キーを除去したvector_store設定
        """
        if not isinstance(vector_store, dict):
            return vector_store
        if vector_store.get("provider") != "qdrant":
            return vector_store

        vs_config = dict(vector_store.get("config") or {})
        replication_factor = vs_config.pop("replication_factor", 3)
        write_consistency_factor = vs_config.pop("write_consistency_factor", 2)
        # Mem0へはSDK拡張キーを除いた設定を渡す(元の辞書は変更しない)
        sanitized = {**vector_store, "config": vs_config}

        url = vs_config.get("url")
        collection_name = vs_config.get("collection_name")
        if not url or not collection_name:
            logger.debug(
                "Qdrant collection pre-creation skipped: url/collection_name not configured"
            )
            return sanitized

        vector_size = vs_config.get("embedding_model_dims", 1536)

        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Distance, VectorParams

            client = QdrantClient(url=url, api_key=vs_config.get("api_key"))
            try:
                if client.collection_exists(collection_name):
                    return sanitized

                client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=vector_size,
                        distance=Distance.COSINE,
                        on_disk=vs_config.get("on_disk", False),
                    ),
                    replication_factor=replication_factor,
                    write_consistency_factor=write_consistency_factor,
                )
                logger.info(
                    f"Qdrant collection pre-created with replication: "
                    f"collection={collection_name}, replication_factor={replication_factor}, "
                    f"write_consistency_factor={write_consistency_factor}"
                )
            finally:
                client.close()
        except Exception as e:
            # Mem0側の作成にフォールバックする(RF=1になるが機能は動作する)。
            # 是正は運用ツール(remediate_qdrant_replication)で行う。
            logger.warning(
                f"Qdrant collection pre-creation failed, falling back to Mem0 default "
                f"(replication_factor will be 1): collection={collection_name}, "
                f"error={type(e).__name__}: {e}"
            )

        return sanitized

    def __init__(self, config: SemanticMemoryConfig):
        """
        Initialize Semantic Memory Client

        Args:
            config: SemanticMemoryConfig instance

        Raises:
            SemanticMemoryConfigError: 設定が不正な場合
        """
        if not config:
            raise SemanticMemoryConfigError("SemanticMemoryConfig is required")

        if not config.llm_config or not config.embedder_config:
            raise SemanticMemoryConfigError(
                "Both llm_config and embedder_config are required"
            )

        # Validate provider-specific configurations
        self._validate_provider_config(config.llm_config, "llm_config")
        self._validate_provider_config(config.embedder_config, "embedder_config")

        self._config = config
        self._memory = None
        self._enabled = False

        try:
            # Configure Mem0 telemetry before importing
            _configure_mem0_telemetry()

            from mem0 import Memory

            # Build Mem0 format config
            mem0_config = {
                'llm': self._convert_llm_to_mem0(config.llm_config),
                'embedder': self._convert_embedder_to_mem0(config.embedder_config),
            }

            if config.vector_store:
                # Mem0はRFを指定できないため、レプリケーション設定付きで先行作成し、
                # Mem0が拒否するSDK拡張キーを除いた設定を渡す
                mem0_config['vector_store'] = self._ensure_qdrant_collection(
                    config.vector_store
                )

            if config.rerank:
                mem0_config['rerank'] = config.rerank

            if config.custom_fact_extraction_prompt:
                mem0_config['custom_fact_extraction_prompt'] = config.custom_fact_extraction_prompt

            if config.custom_update_memory_prompt:
                mem0_config['custom_update_memory_prompt'] = config.custom_update_memory_prompt

            self._memory = Memory.from_config(mem0_config)
            self._enabled = True

            logger.info(
                f"SemanticMemoryClient initialized - "
                f"llm={config.llm_config.model}, "
                f"embedder={config.embedder_config.model}"
            )

        except ImportError as e:
            logger.error(f"mem0 library not installed: {e}")
            raise SemanticMemoryConfigError(
                "mem0 library is required: pip install mem0ai"
            ) from e
        except Exception as e:
            logger.error(f"Failed to initialize SemanticMemoryClient: {e}")
            raise SemanticMemoryConfigError(
                f"Failed to initialize Mem0: {e}"
            ) from e

    @property
    def enabled(self) -> bool:
        """クライアントが有効かどうか"""
        return self._enabled

    # 変換ロジックの正はモジュールレベル関数（normalize_provider 等）。
    # 二重実装のドリフト（openai_base_url 欠落 / gpt-5 分類漏れ）再発防止のため、
    # インスタンスメソッドは互換維持の委譲のみとする。
    def _normalize_provider(self, provider: str) -> str:
        """プロバイダー名を正規化（モジュール関数 normalize_provider へ委譲）"""
        return normalize_provider(provider)

    def _parse_model_string(self, model: str) -> tuple[str, str]:
        """モデル文字列をプロバイダーとモデル名に分離（parse_model_string へ委譲）"""
        return parse_model_string(model)

    def _convert_llm_to_mem0(self, llm_config: LLMProviderConfig) -> Dict[str, Any]:
        """LLM設定をMem0形式へ変換（convert_llm_to_mem0 へ委譲）"""
        return convert_llm_to_mem0(llm_config)

    def _convert_embedder_to_mem0(self, embedder_config: LLMProviderConfig) -> Dict[str, Any]:
        """Embedder設定をMem0形式へ変換（convert_embedder_to_mem0 へ委譲）"""
        return convert_embedder_to_mem0(embedder_config)

    def add(
        self,
        messages: List[Dict[str, str]],
        user_id: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        メモリを追加

        会話メッセージをセマンティックメモリに保存します。
        保存されたメモリは後でsearch()メソッドで検索できます。

        Args:
            messages: メッセージリスト。各要素は {"role": "user"|"assistant", "content": "..."} 形式
            user_id: ユーザーID（必須）。ユーザーごとにメモリが分離されます
            metadata: 追加メタデータ（オプション）。検索時のフィルタリングに使用可能

        Returns:
            Dict[str, Any]: 追加結果。成功時は {"results": [...]} 形式

        Raises:
            SemanticMemoryError: メモリ追加に失敗した場合

        Example:
            >>> # 会話を保存
            >>> result = memory_client.add(
            ...     messages=[
            ...         {"role": "user", "content": "東京の天気は？"},
            ...         {"role": "assistant", "content": "東京は晴れです。"}
            ...     ],
            ...     user_id="user-123",
            ...     metadata={"topic": "weather"}
            ... )
            >>> print(result)
            {'results': [...]}
        """
        if not self._enabled:
            return {"error": "SemanticMemoryClient is not enabled"}

        try:
            result = self._memory.add(
                messages=messages,
                user_id=user_id,
                metadata=metadata or {},
            )
            logger.debug(f"Memory added for user_id={user_id}")
            return result

        except Exception as e:
            logger.error(f"Failed to add memory: {e}")
            raise SemanticMemoryError(f"Failed to add memory: {e}") from e

    def search(
        self,
        query: str,
        user_id: str,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """
        メモリを検索

        保存されたメモリからセマンティック検索を行います。
        クエリに意味的に関連するメモリを関連度順に返します。

        Args:
            query: 検索クエリ。自然言語で記述。例: "天気に関する会話"
            user_id: ユーザーID。add()で指定したuser_idと同じ値を使用
            limit: 結果数上限（デフォルト: 10）

        Returns:
            Dict[str, Any]: 検索結果。{"results": [{"id": "...", "memory": "...", "score": 0.9}, ...]}

        Raises:
            SemanticMemoryError: 検索に失敗した場合

        Example:
            >>> # メモリを検索
            >>> results = memory_client.search(
            ...     query="天気について教えて",
            ...     user_id="user-123",
            ...     limit=5
            ... )
            >>> for item in results.get("results", []):
            ...     print(f"Score: {item['score']:.2f} - {item['memory']}")
        """
        if not self._enabled:
            return {"error": "SemanticMemoryClient is not enabled", "results": []}

        try:
            # mem0 2.x: user_id はトップレベル不可 → filters へ、limit → top_k へ移行
            result = self._memory.search(
                query=query,
                filters={"user_id": user_id},
                top_k=limit,
            )
            logger.debug(
                f"Memory searched for user_id={user_id}, "
                f"results={len(result.get('results', []))}"
            )
            return result

        except Exception as e:
            logger.error(f"Failed to search memory: {e}")
            raise SemanticMemoryError(f"Failed to search memory: {e}") from e

    def get_all(self, user_id: str) -> Dict[str, Any]:
        """
        ユーザーの全メモリを取得

        指定されたユーザーに紐づく全てのメモリを取得します。
        検索ではなく、保存された全てのメモリを一覧表示する場合に使用します。

        Args:
            user_id: ユーザーID

        Returns:
            Dict[str, Any]: メモリリスト。{"results": [{"id": "...", "memory": "...", "created_at": "..."}, ...]}

        Raises:
            SemanticMemoryError: 取得に失敗した場合

        Example:
            >>> # ユーザーの全メモリを取得
            >>> all_memories = memory_client.get_all(user_id="user-123")
            >>> print(f"Total memories: {len(all_memories.get('results', []))}")
            >>> for mem in all_memories.get("results", []):
            ...     print(f"[{mem['id']}] {mem['memory']}")
        """
        if not self._enabled:
            return {"error": "SemanticMemoryClient is not enabled", "results": []}

        try:
            # mem0 2.x: get_all は user_id トップレベル不可 → filters へ移行
            result = self._memory.get_all(filters={"user_id": user_id})
            logger.debug(
                f"All memories retrieved for user_id={user_id}, "
                f"count={len(result.get('results', []))}"
            )
            return result

        except Exception as e:
            logger.error(f"Failed to get all memories: {e}")
            raise SemanticMemoryError(f"Failed to get all memories: {e}") from e

    def delete(self, memory_id: str) -> Dict[str, Any]:
        """
        メモリを削除

        指定されたIDのメモリを削除します。
        メモリIDはget_all()やsearch()で取得できます。

        Args:
            memory_id: 削除するメモリのID

        Returns:
            Dict[str, Any]: 削除結果。{"message": "Memory deleted successfully"}

        Raises:
            SemanticMemoryError: 削除に失敗した場合

        Example:
            >>> # 特定のメモリを削除
            >>> result = memory_client.delete(memory_id="mem-abc123")
            >>> print(result)
            {'message': 'Memory deleted successfully'}
        """
        if not self._enabled:
            return {"error": "SemanticMemoryClient is not enabled"}

        try:
            result = self._memory.delete(memory_id=memory_id)
            logger.debug(f"Memory deleted: {memory_id}")
            return result

        except Exception as e:
            logger.error(f"Failed to delete memory: {e}")
            raise SemanticMemoryError(f"Failed to delete memory: {e}") from e

    def delete_all(self, user_id: str) -> Dict[str, Any]:
        """
        ユーザーの全メモリを削除

        指定されたユーザーに紐づく全てのメモリを削除します。
        この操作は取り消せません。注意して使用してください。

        Args:
            user_id: ユーザーID

        Returns:
            Dict[str, Any]: 削除結果。{"message": "All memories deleted successfully"}

        Raises:
            SemanticMemoryError: 削除に失敗した場合

        Example:
            >>> # ユーザーの全メモリを削除
            >>> result = memory_client.delete_all(user_id="user-123")
            >>> print(result)
            {'message': 'All memories deleted successfully'}

        Warning:
            この操作は取り消せません。全てのメモリが永久に削除されます。
        """
        if not self._enabled:
            return {"error": "SemanticMemoryClient is not enabled"}

        try:
            result = self._memory.delete_all(user_id=user_id)
            logger.debug(f"All memories deleted for user_id={user_id}")
            return result

        except Exception as e:
            logger.error(f"Failed to delete all memories: {e}")
            raise SemanticMemoryError(f"Failed to delete all memories: {e}") from e

    async def cleanup(self) -> None:
        """
        クライアントリソースのクリーンアップ

        明示的にリソースを解放する場合に呼び出します。

        Example:
            >>> # 明示的なクリーンアップ
            >>> await memory_client.cleanup()
        """
        logger.debug("SemanticMemoryClient cleanup called")
        # No specific cleanup needed for mem0 at this time
