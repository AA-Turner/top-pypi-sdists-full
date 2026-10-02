"""
AGENTICSTAR Platform SDK - Google Cloud Storage Client
Google Cloud Storageへのファイル操作を提供

Features:
- ファイルアップロード・ダウンロード（ストリーミング）
- オブジェクト一覧・削除・存在確認
- 署名付きURL生成
- カスタムドメイン対応
- 日本語ファイル名対応（URLエンコード）
- メタデータサニタイズ（Base64エンコード）
- パストラバーサル防止
"""

import asyncio
import logging
import time
from pathlib import Path
from typing import Any, Dict, Optional

from .base import (
    DownloadResult,
    GCSConfig,
    ListResult,
    ObjectInfo,
    StorageClientBase,
    StorageConfigError,
    StorageConnectionError,
    StorageOperationError,
    StorageProvider,
    UploadResult,
)

logger = logging.getLogger(__name__)

# google-cloud-storage availability check
try:
    from google.cloud import storage as gcs_storage
    from google.oauth2 import service_account
    GCS_AVAILABLE = True
except ImportError:
    gcs_storage = None
    service_account = None
    GCS_AVAILABLE = False


class GCSStorageClient(StorageClientBase):
    """
    Google Cloud Storageクライアント

    Features:
    - ファイルアップロード・ダウンロード
    - オブジェクト一覧・削除
    - 署名付きURL生成
    - カスタムドメイン対応
    - 日本語ファイル名対応（URLエンコード）
    - メタデータサニタイズ（Base64エンコード）

    Example:
        config = GCSConfig(
            bucket_name="my-bucket",
            project_id="my-project",
            credentials_path="/path/to/service-account.json",
        )
        client = GCSStorageClient(config)
        result = await client.upload_file("/path/to/file.txt")
    """

    def __init__(self, config: GCSConfig):
        """
        Initialize Google Cloud Storage Client

        Args:
            config: GCSConfig instance

        Raises:
            StorageConfigError: 設定が不正な場合
            StorageConnectionError: 接続に失敗した場合
        """
        super().__init__(config)

        if not GCS_AVAILABLE:
            raise StorageConfigError(
                "google-cloud-storage package is not installed. "
                "Install with: pip install 'agenticstar-platform[storage-gcp]'"
            )

        if not config.bucket_name:
            raise StorageConfigError("GCS bucket_name is required")

        if not config.project_id:
            raise StorageConfigError("GCS project_id is required")

        self._gcs_config: GCSConfig = config
        self._gcs_client = None
        self._bucket = None

        try:
            credentials_json = config.credentials_json
            # Base64エンコード済みの場合はデコード (Helm TOML-safe format)
            if not credentials_json and config.credentials_base64:
                import base64
                credentials_json = base64.b64decode(config.credentials_base64).decode('utf-8')

            if config.credentials_path:
                credentials = service_account.Credentials.from_service_account_file(
                    config.credentials_path
                )
                self._gcs_client = gcs_storage.Client(
                    project=config.project_id,
                    credentials=credentials,
                )
            elif credentials_json:
                import json
                credentials_info = json.loads(credentials_json)
                credentials = service_account.Credentials.from_service_account_info(
                    credentials_info
                )
                self._gcs_client = gcs_storage.Client(
                    project=config.project_id,
                    credentials=credentials,
                )
            else:
                # デフォルト認証（環境変数 GOOGLE_APPLICATION_CREDENTIALS）
                self._gcs_client = gcs_storage.Client(project=config.project_id)

            self._enabled = config.enabled

            logger.info(
                f"GCSStorageClient initialized - bucket={config.bucket_name}, "
                f"project={config.project_id}"
            )

        except Exception as e:
            logger.error(f"Failed to initialize GCS client: {e}")
            raise StorageConnectionError(
                f"Failed to connect to GCS: {e}"
            ) from e

    @property
    def provider(self) -> StorageProvider:
        return StorageProvider.GCS

    @property
    def bucket_name(self) -> str:
        return self._gcs_config.bucket_name

    # _encode_object_name: StorageClientBase に移動済み
    # _sanitize_path: StorageClientBase に移動済み

    def _generate_public_url(self, object_name: str) -> str:
        """公開URLを生成（カスタムドメイン対応）"""
        custom_domain = self._gcs_config.custom_domain
        if custom_domain:
            return f"https://{custom_domain}/{object_name}"

        return f"https://storage.googleapis.com/{self.bucket_name}/{object_name}"

    async def ensure_bucket_exists(self) -> bool:
        """バケットの存在確認・作成"""
        if not self._enabled:
            return False

        try:
            self._bucket = self._gcs_client.bucket(self.bucket_name)

            exists = await asyncio.get_running_loop().run_in_executor(
                None, self._bucket.exists
            )
            if exists:
                return True

            if self._gcs_config.auto_create_bucket:
                self._bucket = await asyncio.get_running_loop().run_in_executor(
                    None,
                    lambda: self._gcs_client.create_bucket(self.bucket_name)
                )
                logger.info(f"Created GCS bucket: {self.bucket_name}")
                return True
            else:
                logger.error(f"Bucket {self.bucket_name} does not exist")
                return False

        except Exception as e:
            logger.error(f"Failed to ensure bucket exists: {e}")
            return False

    def _get_bucket(self):
        """バケットオブジェクトを取得（キャッシュ付き）"""
        if self._bucket is None:
            self._bucket = self._gcs_client.bucket(self.bucket_name)
        return self._bucket

    async def upload_file(
        self,
        file_path: str,
        object_name: Optional[str] = None,
        prefix: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> UploadResult:
        """
        ファイルをGCSにアップロード

        Args:
            file_path: アップロードするファイルのローカルパス
            object_name: オブジェクト名（省略時はファイル名が使用される）
            prefix: オブジェクト名プレフィックス（フォルダ構造を作成）
            metadata: 追加メタデータ（日本語はBase64エンコードされる）

        Returns:
            UploadResult: アップロード結果
        """
        if not self._enabled:
            return UploadResult(
                success=False,
                error="GCS Storage is not enabled",
                error_code="STORAGE_NOT_ENABLED",
            )

        try:
            self._validate_file_size(file_path)

            file_path_obj = Path(file_path)

            if not object_name:
                object_name = file_path_obj.name

            safe_object_name = self._encode_object_name(object_name)

            if prefix:
                full_object_name = f"{prefix}/{safe_object_name}"
            else:
                full_object_name = safe_object_name

            if not await self.ensure_bucket_exists():
                return UploadResult(
                    success=False,
                    error="Bucket is not available",
                    error_code="BUCKET_NOT_AVAILABLE",
                )

            content_type = self._get_content_type(file_path)
            safe_metadata = self._sanitize_metadata(metadata)

            bucket = self._get_bucket()
            blob = bucket.blob(full_object_name)

            if safe_metadata:
                blob.metadata = safe_metadata

            file_size = file_path_obj.stat().st_size

            await asyncio.get_running_loop().run_in_executor(
                None,
                lambda: blob.upload_from_filename(
                    str(file_path_obj),
                    content_type=content_type,
                )
            )

            object_url = self._generate_public_url(full_object_name)

            logger.info("Successfully uploaded file to GCS")

            return UploadResult(
                success=True,
                object_name=full_object_name,
                object_url=object_url,
                file_size=file_size,
                content_type=content_type,
                metadata={
                    "uploaded_at": time.time(),
                    "prefix": prefix,
                    **(safe_metadata or {}),
                },
            )

        except StorageOperationError:
            raise
        except Exception as e:
            logger.error(f"Failed to upload file: {e}")
            return UploadResult(
                success=False,
                error=f"Upload failed: {e}",
                error_code="UPLOAD_FAILED",
            )

    async def download_file(
        self,
        object_name: str,
        download_path: str,
    ) -> DownloadResult:
        """
        ファイルをGCSからダウンロード

        Args:
            object_name: ダウンロードするオブジェクト名
            download_path: ダウンロード先のローカルパス

        Returns:
            DownloadResult: ダウンロード結果
        """
        if not self._enabled:
            return DownloadResult(
                success=False,
                error="GCS Storage is not enabled",
                error_code="STORAGE_NOT_ENABLED",
            )

        try:
            bucket = self._get_bucket()
            blob = bucket.blob(object_name)

            exists = await asyncio.get_running_loop().run_in_executor(
                None, blob.exists
            )
            if not exists:
                return DownloadResult(
                    success=False,
                    object_name=object_name,
                    error=f"Object not found: {object_name}",
                    error_code="OBJECT_NOT_FOUND",
                )

            download_path_obj = Path(download_path)
            download_path_obj.parent.mkdir(parents=True, exist_ok=True)

            await asyncio.get_running_loop().run_in_executor(
                None,
                lambda: blob.download_to_filename(str(download_path_obj))
            )

            file_size = download_path_obj.stat().st_size
            logger.info("Successfully downloaded object from GCS")

            return DownloadResult(
                success=True,
                object_name=object_name,
                local_path=str(download_path_obj),
                file_size=file_size,
            )

        except Exception as e:
            logger.error(f"Failed to download object: {e}")
            return DownloadResult(
                success=False,
                object_name=object_name,
                error=f"Download failed: {e}",
                error_code="DOWNLOAD_FAILED",
            )

    async def list_objects(
        self,
        prefix: str = "",
        max_results: Optional[int] = None,
    ) -> ListResult:
        """
        オブジェクト一覧を取得

        Args:
            prefix: プレフィックスフィルタ
            max_results: 最大取得数

        Returns:
            ListResult: 一覧結果
        """
        if not self._enabled:
            return ListResult(
                success=False,
                error="GCS Storage is not enabled",
                error_code="STORAGE_NOT_ENABLED",
            )

        try:
            bucket = self._get_bucket()

            list_kwargs = {}
            if prefix:
                list_kwargs['prefix'] = prefix
            if max_results:
                list_kwargs['max_results'] = max_results

            def _list():
                blobs = list(bucket.list_blobs(**list_kwargs))
                objects = []
                for blob in blobs:
                    objects.append(ObjectInfo(
                        name=blob.name,
                        size=blob.size or 0,
                        last_modified=blob.updated.isoformat() if blob.updated else None,
                        content_type=blob.content_type,
                    ))
                return objects

            objects = await asyncio.get_running_loop().run_in_executor(None, _list)

            logger.info(f"Listed {len(objects)} objects from GCS")

            return ListResult(
                success=True,
                objects=objects,
                count=len(objects),
                prefix=prefix,
            )

        except Exception as e:
            logger.error(f"Failed to list objects: {e}")
            return ListResult(
                success=False,
                error=f"List failed: {e}",
                error_code="LIST_FAILED",
            )

    async def delete_object(self, object_name: str) -> bool:
        """オブジェクトを削除"""
        if not self._enabled:
            return False

        try:
            bucket = self._get_bucket()
            blob = bucket.blob(object_name)

            await asyncio.get_running_loop().run_in_executor(
                None, blob.delete
            )
            logger.info("Successfully deleted object from GCS")
            return True

        except Exception as e:
            logger.error(f"Failed to delete object: {e}")
            return False

    async def object_exists(self, object_name: str) -> bool:
        """オブジェクトの存在確認"""
        if not self._enabled:
            return False

        try:
            bucket = self._get_bucket()
            blob = bucket.blob(object_name)
            return await asyncio.get_running_loop().run_in_executor(
                None, blob.exists
            )
        except Exception as e:
            logger.error(f"Failed to check object existence: {e}")
            return False

    async def get_object_url(
        self,
        object_name: str,
        expires_in: Optional[int] = None,
    ) -> str:
        """
        署名付きURLを生成

        Args:
            object_name: オブジェクト名
            expires_in: 有効期限（秒）。省略時は公開URLを返す

        Returns:
            署名付きURL or 公開URL
        """
        if not self._enabled:
            return ""

        if expires_in:
            try:
                import datetime
                bucket = self._get_bucket()
                blob = bucket.blob(object_name)
                url = await asyncio.get_running_loop().run_in_executor(
                    None,
                    lambda: blob.generate_signed_url(
                        expiration=datetime.timedelta(seconds=expires_in),
                        method='GET',
                    )
                )
                return url
            except Exception as e:
                logger.error(f"Failed to generate signed URL: {e}")
                return ""

        return self._generate_public_url(object_name)

    # download_objects_by_prefix: StorageClientBase に移動済み

    async def close(self) -> None:
        """クライアントリソースをクローズ"""
        try:
            if self._gcs_client:
                self._gcs_client.close()
        except Exception as e:
            logger.warning(f"Error closing GCS client: {e}")
        finally:
            self._gcs_client = None
            self._bucket = None
            self._enabled = False
            logger.debug("GCSStorageClient closed")
