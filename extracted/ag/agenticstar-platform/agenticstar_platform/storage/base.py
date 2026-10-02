"""
AGENTICSTAR Platform SDK - Storage Base
マルチクラウド対応ストレージクライアントの基底クラス・インターフェース定義

サポート予定プロバイダー:
- Azure Blob Storage
- AWS S3
- Google Cloud Storage
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

logger = logging.getLogger(__name__)


class StorageProvider(str, Enum):
    """ストレージプロバイダー種別"""
    AZURE_BLOB = "azure_blob"
    AWS_S3 = "aws_s3"
    GCS = "gcs"


class StorageError(Exception):
    """Storage操作の基底エラー"""
    pass


class StorageConfigError(StorageError):
    """Storage設定エラー"""
    pass


class StorageConnectionError(StorageError):
    """Storage接続エラー"""
    pass


class StorageOperationError(StorageError):
    """Storage操作エラー"""

    def __init__(self, message: str, error_code: str = "OPERATION_ERROR"):
        super().__init__(message)
        self.error_code = error_code


@dataclass
class UploadResult:
    """アップロード結果"""
    success: bool
    object_name: str = ""
    object_url: str = ""
    file_size: int = 0
    content_type: str = ""
    error: Optional[str] = None
    error_code: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DownloadResult:
    """ダウンロード結果"""
    success: bool
    object_name: str = ""
    local_path: str = ""
    file_size: int = 0
    error: Optional[str] = None
    error_code: Optional[str] = None


@dataclass
class ObjectInfo:
    """オブジェクト情報"""
    name: str
    size: int
    last_modified: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ListResult:
    """一覧取得結果"""
    success: bool
    objects: List[ObjectInfo] = field(default_factory=list)
    count: int = 0
    prefix: str = ""
    error: Optional[str] = None
    error_code: Optional[str] = None


@dataclass
class StorageConfig:
    """共通ストレージ設定"""
    provider: StorageProvider
    bucket_name: str  # Azure: container_name, S3: bucket, GCS: bucket
    enabled: bool = True
    # 共通オプション
    max_file_size: int = 5 * 1024 * 1024 * 1024  # 5GB
    auto_create_bucket: bool = False
    prefix: str = ""  # オブジェクト名プレフィックス
    custom_domain: Optional[str] = None
    # 接続設定
    connection_timeout: int = 30
    read_timeout: int = 300  # 大容量ファイル対応


@dataclass
class AzureBlobConfig:
    """Azure Blob Storage設定

    Example:
        >>> # 辞書から作成
        >>> config = AzureBlobConfig.from_dict({
        ...     "bucket_name": "my-container",
        ...     "connection_string": "DefaultEndpointsProtocol=https;...",
        ...     "prefix": "uploads/"
        ... })
        >>>
        >>> # クライアント初期化
        >>> client = AzureBlobStorageClient(config)

    Note:
        connection_stringはrepr=Falseでログ出力から除外されます。
    """
    bucket_name: str  # container_name
    connection_string: str = field(repr=False)  # シークレット: reprから除外
    # 共通オプション
    enabled: bool = True
    max_file_size: int = 5 * 1024 * 1024 * 1024  # 5GB
    auto_create_bucket: bool = False
    prefix: str = ""
    custom_domain: Optional[str] = None
    connection_timeout: int = 30
    read_timeout: int = 300  # 大容量ファイル対応
    # Azure固有オプション
    max_block_size: int = 8 * 1024 * 1024  # 8MB (5GBファイルで625ブロック)
    max_single_put_size: int = 256 * 1024 * 1024  # 256MB

    @property
    def provider(self) -> StorageProvider:
        return StorageProvider.AZURE_BLOB

    def __str__(self) -> str:
        return f"AzureBlobConfig(bucket_name={self.bucket_name!r}, connection_string=***)"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AzureBlobConfig":
        """辞書からAzureBlobConfigを作成

        Args:
            data: 設定辞書

        Returns:
            AzureBlobConfig instance

        Example:
            >>> config = AzureBlobConfig.from_dict({
            ...     "bucket_name": "my-container",
            ...     "connection_string": "DefaultEndpointsProtocol=https;..."
            ... })
        """
        return cls(
            bucket_name=data["bucket_name"],
            connection_string=data["connection_string"],
            enabled=data.get("enabled", True),
            max_file_size=data.get("max_file_size", 5 * 1024 * 1024 * 1024),
            auto_create_bucket=data.get("auto_create_bucket", False),
            prefix=data.get("prefix", ""),
            custom_domain=data.get("custom_domain"),
            connection_timeout=data.get("connection_timeout", 30),
            read_timeout=data.get("read_timeout", 300),
            max_block_size=data.get("max_block_size", 8 * 1024 * 1024),
            max_single_put_size=data.get("max_single_put_size", 256 * 1024 * 1024),
        )


@dataclass
class S3Config:
    """AWS S3設定

    Example:
        >>> # 辞書から作成
        >>> config = S3Config.from_dict({
        ...     "bucket_name": "my-bucket",
        ...     "aws_access_key_id": "AKIAXXXXXXX",
        ...     "aws_secret_access_key": "secretkey",
        ...     "region_name": "ap-northeast-1"
        ... })
        >>>
        >>> # クライアント初期化
        >>> client = S3StorageClient(config)

    Note:
        aws_access_key_id, aws_secret_access_keyはrepr=Falseでログ出力から除外されます。
    """
    bucket_name: str
    aws_access_key_id: str = field(repr=False)  # シークレット: reprから除外
    aws_secret_access_key: str = field(repr=False)  # シークレット: reprから除外
    region_name: str = "us-east-1"
    # 共通オプション
    enabled: bool = True
    max_file_size: int = 5 * 1024 * 1024 * 1024  # 5GB
    auto_create_bucket: bool = False
    prefix: str = ""
    custom_domain: Optional[str] = None
    connection_timeout: int = 30
    read_timeout: int = 300  # 大容量ファイル対応
    # S3固有オプション
    endpoint_url: Optional[str] = None  # MinIO等のS3互換ストレージ用

    @property
    def provider(self) -> StorageProvider:
        return StorageProvider.AWS_S3

    def __str__(self) -> str:
        return f"S3Config(bucket_name={self.bucket_name!r}, region_name={self.region_name!r}, credentials=***)"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "S3Config":
        """辞書からS3Configを作成

        Args:
            data: 設定辞書

        Returns:
            S3Config instance

        Example:
            >>> config = S3Config.from_dict({
            ...     "bucket_name": "my-bucket",
            ...     "aws_access_key_id": "AKIAXXXXXXX",
            ...     "aws_secret_access_key": "secretkey",
            ...     "region_name": "ap-northeast-1"
            ... })
        """
        return cls(
            bucket_name=data["bucket_name"],
            aws_access_key_id=data["aws_access_key_id"],
            aws_secret_access_key=data["aws_secret_access_key"],
            region_name=data.get("region_name", "us-east-1"),
            enabled=data.get("enabled", True),
            max_file_size=data.get("max_file_size", 5 * 1024 * 1024 * 1024),
            auto_create_bucket=data.get("auto_create_bucket", False),
            prefix=data.get("prefix", ""),
            custom_domain=data.get("custom_domain"),
            connection_timeout=data.get("connection_timeout", 30),
            read_timeout=data.get("read_timeout", 300),
            endpoint_url=data.get("endpoint_url"),
        )


@dataclass
class GCSConfig:
    """Google Cloud Storage設定

    Example:
        >>> # 辞書から作成
        >>> config = GCSConfig.from_dict({
        ...     "bucket_name": "my-bucket",
        ...     "project_id": "my-project",
        ...     "credentials_path": "/path/to/service-account.json"
        ... })
        >>>
        >>> # クライアント初期化
        >>> client = GCSStorageClient(config)

    Note:
        credentials_path, credentials_jsonはrepr=Falseでログ出力から除外されます。
    """
    bucket_name: str
    project_id: str
    # 共通オプション
    enabled: bool = True
    max_file_size: int = 5 * 1024 * 1024 * 1024  # 5GB
    auto_create_bucket: bool = False
    prefix: str = ""
    custom_domain: Optional[str] = None
    connection_timeout: int = 30
    read_timeout: int = 300  # 大容量ファイル対応
    # GCS固有オプション（シークレット: reprから除外）
    credentials_path: Optional[str] = field(default=None, repr=False)
    credentials_json: Optional[str] = field(default=None, repr=False)
    credentials_base64: Optional[str] = field(default=None, repr=False)  # Base64-encoded JSON (TOML-safe)

    @property
    def provider(self) -> StorageProvider:
        return StorageProvider.GCS

    def __str__(self) -> str:
        return f"GCSConfig(bucket_name={self.bucket_name!r}, project_id={self.project_id!r}, credentials=***)"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GCSConfig":
        """辞書からGCSConfigを作成

        Args:
            data: 設定辞書

        Returns:
            GCSConfig instance

        Example:
            >>> config = GCSConfig.from_dict({
            ...     "bucket_name": "my-bucket",
            ...     "project_id": "my-project",
            ...     "credentials_path": "/path/to/service-account.json"
            ... })
        """
        return cls(
            bucket_name=data["bucket_name"],
            project_id=data["project_id"],
            enabled=data.get("enabled", True),
            max_file_size=data.get("max_file_size", 5 * 1024 * 1024 * 1024),
            auto_create_bucket=data.get("auto_create_bucket", False),
            prefix=data.get("prefix", ""),
            custom_domain=data.get("custom_domain"),
            connection_timeout=data.get("connection_timeout", 30),
            read_timeout=data.get("read_timeout", 300),
            credentials_path=data.get("credentials_path"),
            credentials_json=data.get("credentials_json"),
            credentials_base64=data.get("credentials_base64"),
        )


@runtime_checkable
class StorageClientProtocol(Protocol):
    """ストレージクライアントプロトコル

    すべてのストレージプロバイダー実装が満たすべきインターフェース
    """

    @property
    def enabled(self) -> bool:
        """クライアントが有効かどうか"""
        ...

    @property
    def provider(self) -> StorageProvider:
        """プロバイダー種別"""
        ...

    async def ensure_bucket_exists(self) -> bool:
        """バケット/コンテナの存在確認・作成"""
        ...

    async def upload_file(
        self,
        file_path: str,
        object_name: Optional[str] = None,
        prefix: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> UploadResult:
        """ファイルをアップロード"""
        ...

    async def download_file(
        self,
        object_name: str,
        download_path: str,
    ) -> DownloadResult:
        """ファイルをダウンロード"""
        ...

    async def list_objects(
        self,
        prefix: str = "",
        max_results: Optional[int] = None,
    ) -> ListResult:
        """オブジェクト一覧を取得"""
        ...

    async def delete_object(
        self,
        object_name: str,
    ) -> bool:
        """オブジェクトを削除"""
        ...

    async def object_exists(
        self,
        object_name: str,
    ) -> bool:
        """オブジェクトの存在確認"""
        ...

    async def get_object_url(
        self,
        object_name: str,
        expires_in: Optional[int] = None,
    ) -> str:
        """オブジェクトのURLを取得（署名付きURL対応）"""
        ...

    async def close(self) -> None:
        """クライアントリソースをクローズ"""
        ...


class StorageClientBase(ABC):
    """ストレージクライアント基底クラス

    共通のユーティリティメソッドを提供

    Example:
        async with AzureBlobStorageClient(config) as client:
            result = await client.upload_file("local/file.txt")
    """

    def __init__(self, config: StorageConfig):
        self._config = config
        self._enabled = False

    async def __aenter__(self) -> "StorageClientBase":
        """Context Manager: 開始時の処理"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context Manager: 終了時にリソースをクローズ"""
        await self.close()

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    @abstractmethod
    def provider(self) -> StorageProvider:
        """プロバイダー種別"""
        pass

    def _get_api_key(self, value: Any) -> str:
        """APIキーを取得（SecretStr対応）"""
        if hasattr(value, 'get_secret_value'):
            return value.get_secret_value()
        return str(value) if value else ""

    def _sanitize_metadata_key(self, key: str) -> Optional[str]:
        """メタデータキーをサニタイズ

        Args:
            key: 元のキー

        Returns:
            サニタイズされたキー、または無効な場合はNone
        """
        import re
        # 安全なキー: 英数字、アンダースコア、ハイフン、ドットのみ
        if not re.match(r'^[A-Za-z0-9._-]+$', key):
            # 安全な文字以外を除去
            sanitized = re.sub(r'[^A-Za-z0-9._-]', '', key)
            if not sanitized:
                return None
            return sanitized
        return key

    def _sanitize_metadata(self, metadata: Optional[Dict[str, Any]]) -> Dict[str, str]:
        """メタデータをサニタイズ（キーと値の両方を検証）

        Args:
            metadata: 元のメタデータ

        Returns:
            サニタイズされたメタデータ（無効なエントリは除外）
        """
        if not metadata:
            return {}

        import base64
        safe_metadata = {}

        for key, value in metadata.items():
            # キーのサニタイズ
            safe_key = self._sanitize_metadata_key(key)
            if not safe_key:
                logger.warning(f"Skipping metadata with invalid key")
                continue

            # 値のサニタイズ
            try:
                str_value = str(value)
                str_value.encode('ascii')
                safe_metadata[safe_key] = str_value
            except (UnicodeEncodeError, UnicodeDecodeError):
                encoded_value = base64.b64encode(str_value.encode('utf-8')).decode('ascii')
                safe_metadata[f"{safe_key}_base64"] = encoded_value

        return safe_metadata

    def _get_content_type(self, file_path: str) -> str:
        """ファイルのMIMEタイプを推定"""
        import mimetypes
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type or 'application/octet-stream'

    def _validate_file_size(self, file_path: str) -> None:
        """ファイルサイズを検証"""
        path = Path(file_path)
        if not path.exists():
            raise StorageOperationError(
                f"File not found: {file_path}",
                error_code="FILE_NOT_FOUND"
            )

        file_size = path.stat().st_size
        if file_size > self._config.max_file_size:
            raise StorageOperationError(
                f"File size {file_size} exceeds maximum {self._config.max_file_size}",
                error_code="FILE_TOO_LARGE"
            )

    @abstractmethod
    async def ensure_bucket_exists(self) -> bool:
        pass

    @abstractmethod
    async def upload_file(
        self,
        file_path: str,
        object_name: Optional[str] = None,
        prefix: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> UploadResult:
        pass

    @abstractmethod
    async def download_file(
        self,
        object_name: str,
        download_path: str,
    ) -> DownloadResult:
        pass

    @abstractmethod
    async def list_objects(
        self,
        prefix: str = "",
        max_results: Optional[int] = None,
    ) -> ListResult:
        pass

    @abstractmethod
    async def delete_object(
        self,
        object_name: str,
    ) -> bool:
        pass

    @abstractmethod
    async def object_exists(
        self,
        object_name: str,
    ) -> bool:
        pass

    @abstractmethod
    async def get_object_url(
        self,
        object_name: str,
        expires_in: Optional[int] = None,
    ) -> str:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    # =========================================================
    # 共通ユーティリティ（S3/GCS/Azure共通）
    # =========================================================

    def _encode_object_name(self, name: str) -> str:
        """オブジェクト名をURLエンコード（日本語ファイル名対応）

        '/' はパス区切りとして保持する。
        """
        from urllib.parse import quote, unquote
        # 既にエンコード済みの場合はデコードしてから再エンコード
        decoded = unquote(name)
        parts = decoded.split('/')
        encoded_parts = [quote(part, safe='') for part in parts]
        return '/'.join(encoded_parts)

    def _sanitize_path(self, path: str) -> str:
        """パスをサニタイズ（パストラバーサル防止）

        Pathコンポーネント分解で '..' と '.' を安全に除去する。
        """
        import re
        # 制御文字を除去
        sanitized = re.sub(r'[\x00-\x1f]', '', path)
        # Pathコンポーネント分解で '..' と '.' を安全に除去
        parts = Path(sanitized).parts
        safe_parts = [p for p in parts if p not in ('..', '.') and not p.startswith(('/', '\\'))]
        return str(Path(*safe_parts)) if safe_parts else ''

    async def download_objects_by_prefix(
        self,
        prefix: str,
        download_dir: str,
        max_concurrency: int = 8,
    ) -> Dict[str, Any]:
        """プレフィックス指定でオブジェクトを一括ダウンロード（並列）

        パストラバーサル防止（resolve + relative_to二重防御）を実装。
        サブクラスでlist_objects/download_fileが実装されていれば動作する。

        Args:
            prefix: ダウンロード対象のプレフィックス
            download_dir: ダウンロード先ディレクトリ
            max_concurrency: 並列ダウンロード数（環境変数 BLOB_DL_CONCURRENCY で上書き可、既定 8）

        Returns:
            dict: downloaded, failed, skipped, success_count, failed_count, skipped_count
        """
        import asyncio
        import os

        download_base = Path(download_dir).resolve()
        download_base.mkdir(parents=True, exist_ok=True)

        list_result = await self.list_objects(prefix=prefix)
        if not list_result.success:
            return {
                "success": False,
                "error": list_result.error,
                "downloaded": [], "failed": [], "skipped": [],
                "success_count": 0, "failed_count": 0, "skipped_count": 0,
            }

        # 環境変数による上書き（運用調整用）
        env_concurrency = os.environ.get("BLOB_DL_CONCURRENCY")
        if env_concurrency:
            try:
                max_concurrency = max(1, int(env_concurrency))
            except ValueError:
                pass

        downloaded = []
        failed = []
        skipped = []

        # Phase 1: セキュリティチェック（同期）— DL 並列実行前に全件決着
        download_tasks = []  # (obj, target_path) のリスト
        for obj in list_result.objects:
            # プレフィックスを除いた相対パスを計算
            relative = obj.name[len(prefix):] if obj.name.startswith(prefix) else obj.name
            if not relative or relative.endswith('/'):
                skipped.append({"object_name": obj.name, "reason": "directory_marker"})
                continue

            # サニタイズ
            sanitized = self._sanitize_path(relative)
            if not sanitized:
                skipped.append({"object_name": obj.name, "reason": "sanitized_to_empty"})
                continue

            # パストラバーサル防止: resolve後にdownload_dir配下であることを検証
            target_path = (download_base / sanitized).resolve()
            try:
                target_path.relative_to(download_base)
            except ValueError:
                logger.warning(f"Path traversal attempt blocked: {relative}")
                failed.append({"object_name": obj.name, "error": "path traversal blocked"})
                continue

            # 親ディレクトリ作成（並列実行中の競合を避けるため事前に同期作成）
            target_path.parent.mkdir(parents=True, exist_ok=True)

            download_tasks.append((obj, target_path))

        # Phase 2: 並列ダウンロード（Semaphore で同時実行数を制限）
        sem = asyncio.Semaphore(max_concurrency)

        async def _do_download(obj, target_path):
            async with sem:
                try:
                    dl_result = await self.download_file(obj.name, str(target_path))
                    return obj, dl_result, None
                except Exception as e:
                    return obj, None, e

        if download_tasks:
            results = await asyncio.gather(
                *[_do_download(obj, p) for obj, p in download_tasks],
                return_exceptions=False,
            )
            for obj, dl_result, exc in results:
                if exc is not None:
                    failed.append({"object_name": obj.name, "error": str(exc)})
                elif dl_result.success:
                    downloaded.append({
                        "object_name": obj.name,
                        "local_path": dl_result.local_path,
                        "file_size": dl_result.file_size,
                    })
                else:
                    failed.append({"object_name": obj.name, "error": dl_result.error})

        return {
            "success": True,
            "downloaded": downloaded,
            "failed": failed,
            "skipped": skipped,
            "success_count": len(downloaded),
            "failed_count": len(failed),
            "skipped_count": len(skipped),
        }
