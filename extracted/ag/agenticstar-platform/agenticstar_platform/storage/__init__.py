"""
AGENTICSTAR Platform SDK - Storage Module
マルチクラウド対応のオブジェクトストレージクライアント

サポートプロバイダー:
- Azure Blob Storage
- AWS S3
- Google Cloud Storage

Example:
    from agenticstar_platform.storage import (
        AzureBlobStorageClient, AzureBlobConfig,
        S3StorageClient, S3Config,
        GCSStorageClient, GCSConfig,
    )

    # Azure
    client = AzureBlobStorageClient(AzureBlobConfig(
        bucket_name="my-container",
        connection_string="DefaultEndpointsProtocol=https;...",
    ))

    # AWS S3
    client = S3StorageClient(S3Config(
        bucket_name="my-bucket",
        aws_access_key_id="AKIA...",
        aws_secret_access_key="...",
    ))

    # GCS
    client = GCSStorageClient(GCSConfig(
        bucket_name="my-bucket",
        project_id="my-project",
    ))

    result = await client.upload_file("/path/to/file.txt", prefix="uploads")
    print(result.object_url)
    await client.close()
"""

import importlib
from typing import TYPE_CHECKING

# Base classes and types (core — cloud SDK 依存なしで常に import 可能)
from .base import (
    # Enums
    StorageProvider,
    # Errors
    StorageError,
    StorageConfigError,
    StorageConnectionError,
    StorageOperationError,
    # Result types
    UploadResult,
    DownloadResult,
    ObjectInfo,
    ListResult,
    # Config types
    StorageConfig,
    AzureBlobConfig,
    S3Config,
    GCSConfig,
    # Protocol/ABC
    StorageClientProtocol,
    StorageClientBase,
)

# Path conventions (core)
from .paths import StoragePaths

# 親パッケージの extra 案内ヘルパ (メッセージ形式を top-level と統一する)
from .. import _extra_hint, _missing_dependency

# molt#1367: provider client → (SDK extra, 実装モジュール, 必要依存) の単一正本。
# top-level (`agenticstar_platform.S3StorageClient`) も submodule
# (`agenticstar_platform.storage.S3StorageClient`) も、この mapping を通る
# 下の __getattr__ で解決されるため、両 import 経路の成功・失敗境界は常に一致する。
# provider を追加する場合はここへ 1 エントリ足し、pyproject.toml の extra と
# tests/test_storage_provider_extra_contract.py の一致テストを通すこと。
_PROVIDER_CLIENTS = {
    "AzureBlobStorageClient": ("storage-azure", ".azure", ("azure.storage.blob",)),
    "S3StorageClient": ("storage-aws", ".s3", ("boto3",)),
    "GCSStorageClient": ("storage-gcp", ".gcs", ("google.cloud.storage",)),
}

if TYPE_CHECKING:  # 静的解析 / IDE 補完用（実行時には評価されない）
    from .azure import AzureBlobStorageClient
    from .gcs import GCSStorageClient
    from .s3 import S3StorageClient


def __getattr__(name: str):
    """provider client への初回アクセスで実装を import する (PEP 562, molt#1367)。

    従来は本ファイルが 3 provider 実装を一括 import していたため、依存が無くても
    シンボル取得は成功し、constructor で初めて生 package 名のエラーになっていた
    (README の「extra 未導入アクセス時に必要 extra を示す ImportError」と不一致)。
    依存の有無は import 前に検査し、不足時は正しい SDK extra を案内する。
    実装モジュール内部の import 不具合は変換せずそのまま raise する (誤診防止)。
    """
    entry = _PROVIDER_CLIENTS.get(name)
    if entry is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    extra, module_path, required = entry
    missing = _missing_dependency(required)
    if missing:
        raise _extra_hint(name, extra, missing)
    module = importlib.import_module(module_path, __name__)
    value = getattr(module, name)
    globals()[name] = value  # 2 回目以降は __getattr__ を経由しない
    return value


def __dir__():
    return sorted(set(globals()) | set(__all__))

__all__ = [
    # Enums
    "StorageProvider",
    # Errors
    "StorageError",
    "StorageConfigError",
    "StorageConnectionError",
    "StorageOperationError",
    # Result types
    "UploadResult",
    "DownloadResult",
    "ObjectInfo",
    "ListResult",
    # Config types
    "StorageConfig",
    "AzureBlobConfig",
    "S3Config",
    "GCSConfig",
    # Protocol/ABC
    "StorageClientProtocol",
    "StorageClientBase",
    # Provider implementations
    "AzureBlobStorageClient",
    "S3StorageClient",
    "GCSStorageClient",
    # Path conventions
    "StoragePaths",
]
