"""
AGENTICSTAR Platform SDK
エンタープライズAIエージェント基盤のためのSDK

外部サービス（PostgreSQL、Qdrant、Azure Blob/S3/GCS、Content Safety/PII等）との通信機能を提供
"""

import importlib
import importlib.util
from typing import TYPE_CHECKING

__version__ = "3.0.10"

# Common utilities are internal - not exported as public API
# Use agenticstar_platform.common for internal SDK development only

# ---------------------------------------------------------------------------
# 遅延 import (PEP 562)
#
# 以前は本ファイルが全モジュールを無条件 import していたため、README が案内する
# 軽量インストール (`pip install agenticstar-platform` / `[db]` / `[rag]` など) では
# `import agenticstar_platform` 自体が ModuleNotFoundError で失敗していた
# (core → asyncpg 無し / [db] → openai 無し)。実質 `[all]` 以外は使えない状態だった。
#
# シンボルへ最初にアクセスした時点で実装モジュールを import することで、
# pyproject.toml の extra 分割どおりの軽量インストールが実際に機能する。
# 公開 API 名 (__all__) と import 文の書き方は従来どおり変わらない。
# ---------------------------------------------------------------------------

# 公開シンボル → 実装モジュール
_SYMBOL_MODULES = {
    # Database
    "PostgreSQLManager": ".db",
    "ApiPostgreSQLManager": ".db",
    "PostgreSQLConfig": ".db",
    "AzureADConfig": ".db",
    "DataAccess": ".db",
    "ConfigAccess": ".db",
    # RAG
    "EmbeddingGenerator": ".rag",
    "EmbeddingConfig": ".rag",
    "QdrantManager": ".rag",
    "QdrantConfig": ".rag",
    # Events
    "EventType": ".events",
    "SubEventType": ".events",
    "StreamingEvent": ".events",
    "SequencedEvent": ".events",
    "ExecutionMessage": ".events",
    "EventEmitter": ".events",
    "EventHandler": ".events",
    "create_sse_handler": ".events",
    "create_json_handler": ".events",
    "DatabaseEventHandler": ".events",
    "WebhookEventHandler": ".events",
    "CompositeEventHandler": ".events",
    "create_marketplace_handler": ".events",
    # Memory
    "SemanticMemoryClient": ".memory",
    "SemanticMemoryConfig": ".memory",
    "LLMProviderConfig": ".memory",
    # Storage
    "StorageProvider": ".storage",
    "StorageConfig": ".storage",
    "AzureBlobConfig": ".storage",
    "S3Config": ".storage",
    "GCSConfig": ".storage",
    "AzureBlobStorageClient": ".storage",
    "S3StorageClient": ".storage",
    "GCSStorageClient": ".storage",
    "UploadResult": ".storage",
    "DownloadResult": ".storage",
    "ObjectInfo": ".storage",
    "ListResult": ".storage",
    "StoragePaths": ".storage",
    # Security
    "SecurityProvider": ".security",
    "ContentCategory": ".security",
    "PIICategory": ".security",
    "SecurityError": ".security",
    "SecurityConfigError": ".security",
    "SecurityAPIError": ".security",
    "ContentModerationResult": ".security",
    "PromptShieldResult": ".security",
    "PIIEntity": ".security",
    "PIIDetectionResult": ".security",
    "SecurityCheckResult": ".security",
    "AzureSecurityConfig": ".security",
    "AWSSecurityConfig": ".security",
    "GCPSecurityConfig": ".security",
    "AzureSecurityClient": ".security",
    "AWSSecurityClient": ".security",
    "GCPSecurityClient": ".security",
    # Auth
    "AgenticStarAuthClient": ".auth",
    "AgenticStarAuthConfig": ".auth",
    "AuthError": ".auth",
    "AuthConfigError": ".auth",
    "AuthAPIError": ".auth",
    "AuthUnauthorizedError": ".auth",
    "AuthNotFoundError": ".auth",
    "AuthRateLimitError": ".auth",
    "ApiUser": ".auth",
    "DeviceInfo": ".auth",
    "LoginHistoryEntry": ".auth",
    "UserPagination": ".auth",
    "MCPTokenInfo": ".auth",
    "MCPTokenError": ".auth",
    "OAuthProviderName": ".auth",
    "GetUsersResult": ".auth",
    "GetUserResult": ".auth",
    "GetMCPTokensResult": ".auth",
    # Metering
    "UsageMeter": ".metering",
    "default_cost_fn": ".metering",
    "extract_usage": ".metering",
    "round_cost_usd": ".metering",
    # Action audit
    "ActionAudit": ".audit",
    "GatewayActionAudit": ".audit",
    "ActionAuditWriteError": ".audit",
    "canonical_digest": ".audit",
    # Runtime
    "wait_for_egress": ".runtime",
    # Marketplace runner
    "run_marketplace_agent": ".runner",
    "arun_marketplace_agent": ".runner",
    "MarketplaceRunnerConfigError": ".runner",
}

# 実装モジュール → 必要な extra 名（未掲載のモジュールは core 依存のみで動く）
_MODULE_EXTRAS = {
    ".db": "db",
    ".rag": "rag",
    ".memory": "memory",
    ".storage": "storage",
    # runner は DB(入力取得/結果保存) + Webhook(通知) の両方を要する
    ".runner": "runner",
}

# extra 名 → その extra が導入するトップレベル依存。
# ModuleNotFoundError を「extra 不足」と案内してよいかの判定に使う
# (実装内部の import ミスや循環 import を extra 不足と誤診しないため)。
_EXTRA_DEPENDENCIES = {
    "db": ("asyncpg", "azure.identity"),
    "rag": ("qdrant_client", "openai"),
    "memory": ("mem0",),
    "storage": ("azure.storage.blob", "boto3", "google.cloud.storage"),
    # provider 別 storage extra (molt#1367)。symbol→extra の対応の正本は
    # storage/__init__.py の _PROVIDER_CLIENTS（一致は contract test で固定）
    "storage-azure": ("azure.storage.blob",),
    "storage-aws": ("boto3",),
    "storage-gcp": ("google.cloud.storage",),
    "webhook": ("aiohttp",),
    "security": ("google.cloud.dlp_v2", "google.cloud.aiplatform"),
    "security-aws": ("boto3",),
    "runner": ("asyncpg", "azure.identity", "aiohttp"),
}

# 個別シンボル単位で追加依存が要るもの → (extra 名, 実際に必要なモジュール)
#
# 対象は「依存が無くても import は成功してしまい、実行時に黙って失敗する」もの。
# 例: WebhookEventHandler は aiohttp が無いとログを残して None を返すだけで、
#     webhook が送られないことに気づけない。シンボル取得の時点で知らせる。
# AWSSecurityClient のようにコンストラクタが明示エラーを出すものは対象外
# (既存の挙動を変えない)。
_SYMBOL_EXTRAS = {
    "WebhookEventHandler": ("webhook", ("aiohttp",)),
    "create_marketplace_handler": ("webhook", ("aiohttp",)),
    "GCPSecurityClient": ("security", ("google.cloud.dlp_v2",)),
    # runner モジュール自体は aiohttp 無しでも import できてしまう
    # (WebhookEventHandler が遅延 import のため)。実行時に黙って通知欠落と
    # ならないよう、シンボル取得の時点で runner extra を要求する。
    "run_marketplace_agent": ("runner", ("asyncpg", "azure.identity", "aiohttp")),
    "arun_marketplace_agent": ("runner", ("asyncpg", "azure.identity", "aiohttp")),
}

# 後方互換: 0.5.24 以前は全モジュールを import していた副作用で
# `agenticstar_platform.db` のようなサブモジュール属性が参照できた
_SUBMODULE_NAMES = frozenset(
    {"audit", "auth", "db", "events", "memory", "metering", "rag", "runner", "runtime",
     "security", "storage"}
)

if TYPE_CHECKING:  # 静的解析 / IDE 補完用（実行時には評価されない）
    from .auth import (
        AgenticStarAuthClient,
        AgenticStarAuthConfig,
        ApiUser,
        AuthAPIError,
        AuthConfigError,
        AuthError,
        AuthNotFoundError,
        AuthRateLimitError,
        AuthUnauthorizedError,
        DeviceInfo,
        GetMCPTokensResult,
        GetUserResult,
        GetUsersResult,
        LoginHistoryEntry,
        MCPTokenError,
        MCPTokenInfo,
        OAuthProviderName,
        UserPagination,
    )
    from .db import (
        ApiPostgreSQLManager,
        AzureADConfig,
        ConfigAccess,
        DataAccess,
        PostgreSQLConfig,
        PostgreSQLManager,
    )
    from .events import (
        CompositeEventHandler,
        DatabaseEventHandler,
        EventEmitter,
        EventHandler,
        EventType,
        ExecutionMessage,
        SequencedEvent,
        StreamingEvent,
        SubEventType,
        WebhookEventHandler,
        create_json_handler,
        create_marketplace_handler,
        create_sse_handler,
    )
    from .audit import (
        ActionAudit,
        ActionAuditWriteError,
        GatewayActionAudit,
        canonical_digest,
    )
    from .memory import LLMProviderConfig, SemanticMemoryClient, SemanticMemoryConfig
    from .metering import UsageMeter, default_cost_fn, extract_usage, round_cost_usd
    from .rag import EmbeddingConfig, EmbeddingGenerator, QdrantConfig, QdrantManager
    from .runner import (
        MarketplaceRunnerConfigError,
        arun_marketplace_agent,
        run_marketplace_agent,
    )
    from .runtime import wait_for_egress
    from .security import (
        AWSSecurityClient,
        AWSSecurityConfig,
        AzureSecurityClient,
        AzureSecurityConfig,
        ContentCategory,
        ContentModerationResult,
        GCPSecurityClient,
        GCPSecurityConfig,
        PIICategory,
        PIIDetectionResult,
        PIIEntity,
        PromptShieldResult,
        SecurityAPIError,
        SecurityCheckResult,
        SecurityConfigError,
        SecurityError,
        SecurityProvider,
    )
    from .storage import (
        AzureBlobConfig,
        AzureBlobStorageClient,
        DownloadResult,
        GCSConfig,
        GCSStorageClient,
        ListResult,
        ObjectInfo,
        S3Config,
        S3StorageClient,
        StorageConfig,
        StoragePaths,
        StorageProvider,
        UploadResult,
    )


def _missing_dependency(distribution_packages: tuple) -> str | None:
    """未インストールの依存トップレベルモジュール名を返す（全て揃っていれば None）。"""
    for module_name in distribution_packages:
        try:
            if importlib.util.find_spec(module_name) is None:
                return module_name
        except (ImportError, ValueError):
            # 親パッケージ自体が無い場合も find_spec は ImportError を投げる
            return module_name
    return None


def _extra_hint(name: str, extra: str, missing: str) -> ImportError:
    return ImportError(
        f"'{name}' requires the '{extra}' extra of agenticstar-platform. "
        f"Install it with:  pip install 'agenticstar-platform[{extra}]'  "
        f"(missing dependency: {missing})"
    )


def __getattr__(name: str):
    """公開シンボル / サブモジュールへの初回アクセスで実装を import する (PEP 562)。

    extra 未導入の場合は、生の ModuleNotFoundError ではなく
    「どの extra を入れれば直るか」を示す ImportError にして返す。
    実装内部の循環 import や `cannot import name` を extra 不足と誤診しないよう、
    変換するのは「その extra が担う依存パッケージが実際に無い」ときだけに限定する。
    """
    # 従来 (0.5.24 以前) は本ファイルが全モジュールを import していた副作用で
    # `agenticstar_platform.db` のようなサブモジュール属性アクセスが成立していた。
    # 後方互換のため、サブモジュール名でのアクセスも解決する。
    if name in _SUBMODULE_NAMES:
        module = importlib.import_module(f".{name}", __name__)
        globals()[name] = module
        return module

    module_path = _SYMBOL_MODULES.get(name)
    if module_path is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    # シンボル単位で追加依存が要るもの（モジュール自体は core で import できるため、
    # import の失敗では検知できない）。実際に依存が無いときだけ先回りして知らせる。
    symbol_extra = _SYMBOL_EXTRAS.get(name)
    if symbol_extra:
        extra, required = symbol_extra
        missing = _missing_dependency(required)
        if missing:
            raise _extra_hint(name, extra, missing)

    try:
        module = importlib.import_module(module_path, __name__)
    except ModuleNotFoundError as exc:
        extra = _MODULE_EXTRAS.get(module_path)
        # exc.name が当該 extra の担う依存であるときだけ extra 不足として案内する
        # (実装内部の import ミスや循環 import はそのまま raise して原因を隠さない)
        known_roots = {dep.split(".")[0] for dep in _EXTRA_DEPENDENCIES.get(extra, ())}
        if extra and exc.name and exc.name.split(".")[0] in known_roots:
            raise _extra_hint(name, extra, exc.name) from exc
        raise

    value = getattr(module, name)
    globals()[name] = value  # 2 回目以降は __getattr__ を経由しない
    return value


def __dir__():
    return sorted(set(globals()) | set(__all__) | _SUBMODULE_NAMES)


__all__ = [
    # Metering
    "UsageMeter",
    "default_cost_fn",
    "extract_usage",
    "round_cost_usd",
    # Action audit
    "ActionAudit",
    "GatewayActionAudit",
    "ActionAuditWriteError",
    "canonical_digest",
    # Database
    "PostgreSQLManager",
    "ApiPostgreSQLManager",
    "PostgreSQLConfig",
    "AzureADConfig",
    "DataAccess",
    "ConfigAccess",
    # RAG
    "EmbeddingGenerator",
    "EmbeddingConfig",
    "QdrantManager",
    "QdrantConfig",
    # Events
    "EventType",
    "SubEventType",
    "StreamingEvent",
    "SequencedEvent",
    "ExecutionMessage",
    "EventEmitter",
    "EventHandler",
    "create_sse_handler",
    "create_json_handler",
    # Event Handlers（マーケットプレイスUI連携用）
    "DatabaseEventHandler",
    "WebhookEventHandler",
    "CompositeEventHandler",
    "create_marketplace_handler",
    # Memory
    "SemanticMemoryClient",
    "SemanticMemoryConfig",
    "LLMProviderConfig",
    # Storage
    "StorageProvider",
    "StorageConfig",
    "AzureBlobConfig",
    "S3Config",
    "GCSConfig",
    "AzureBlobStorageClient",
    "S3StorageClient",
    "GCSStorageClient",
    "UploadResult",
    "DownloadResult",
    "ObjectInfo",
    "ListResult",
    "StoragePaths",
    # Runtime
    "wait_for_egress",
    # Marketplace runner
    "run_marketplace_agent",
    "arun_marketplace_agent",
    "MarketplaceRunnerConfigError",
    # Security
    "SecurityProvider",
    "ContentCategory",
    "PIICategory",
    "SecurityError",
    "SecurityConfigError",
    "SecurityAPIError",
    "ContentModerationResult",
    "PromptShieldResult",
    "PIIEntity",
    "PIIDetectionResult",
    "SecurityCheckResult",
    "AzureSecurityConfig",
    "AWSSecurityConfig",
    "GCPSecurityConfig",
    "AzureSecurityClient",
    "AWSSecurityClient",
    "GCPSecurityClient",
    # Auth
    "AgenticStarAuthClient",
    "AgenticStarAuthConfig",
    "AuthError",
    "AuthConfigError",
    "AuthAPIError",
    "AuthUnauthorizedError",
    "AuthNotFoundError",
    "AuthRateLimitError",
    "ApiUser",
    "DeviceInfo",
    "LoginHistoryEntry",
    "UserPagination",
    "MCPTokenInfo",
    "MCPTokenError",
    "OAuthProviderName",
    "GetUsersResult",
    "GetUserResult",
    "GetMCPTokensResult",
]
