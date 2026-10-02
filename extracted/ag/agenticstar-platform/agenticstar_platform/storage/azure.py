"""
AGENTICSTAR Platform SDK - Azure Blob Storage Client
Azure Blob Storageへのファイル操作を提供
"""

import asyncio
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from .base import (
    AzureBlobConfig,
    DownloadResult,
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

# Azure SDK availability check
try:
    from azure.storage.blob import BlobServiceClient, ContentSettings
    AZURE_BLOB_AVAILABLE = True
except ImportError:
    BlobServiceClient = None
    ContentSettings = None
    AZURE_BLOB_AVAILABLE = False


class AzureBlobStorageClient(StorageClientBase):
    """
    Azure Blob Storageクライアント

    Features:
    - ファイルアップロード・ダウンロード
    - オブジェクト一覧・削除
    - カスタムドメイン対応
    - 日本語ファイル名対応（URLエンコード）
    - メタデータサニタイズ（Base64エンコード）

    Example:
        config = AzureBlobConfig(
            bucket_name="my-container",
            connection_string="DefaultEndpointsProtocol=https;...",
        )
        client = AzureBlobStorageClient(config)
        result = await client.upload_file("/path/to/file.txt")
    """

    def __init__(self, config: AzureBlobConfig):
        """
        Initialize Azure Blob Storage Client

        Args:
            config: AzureBlobConfig instance

        Raises:
            StorageConfigError: 設定が不正な場合
            StorageConnectionError: 接続に失敗した場合
        """
        super().__init__(config)

        if not AZURE_BLOB_AVAILABLE:
            raise StorageConfigError(
                "azure-storage-blob package is not installed. "
                "Install with: pip install 'agenticstar-platform[storage-azure]'"
            )

        if not config.connection_string:
            raise StorageConfigError(
                "Azure Blob connection_string is required"
            )

        if not config.bucket_name:
            raise StorageConfigError(
                "Azure Blob bucket_name (container_name) is required"
            )

        self._azure_config: AzureBlobConfig = config
        self._blob_service_client: Optional[BlobServiceClient] = None

        try:
            self._blob_service_client = BlobServiceClient.from_connection_string(
                conn_str=self._get_api_key(config.connection_string),
                max_block_size=config.max_block_size,
                max_single_put_size=config.max_single_put_size,
                connection_timeout=config.connection_timeout,
                read_timeout=config.read_timeout,
            )
            self._enabled = config.enabled
            logger.info(
                f"AzureBlobStorageClient initialized - "
                f"container={config.bucket_name}"
            )
        except Exception as e:
            logger.error(f"Failed to initialize Azure Blob client: {e}")
            raise StorageConnectionError(
                f"Failed to connect to Azure Blob Storage: {e}"
            ) from e

    @property
    def provider(self) -> StorageProvider:
        return StorageProvider.AZURE_BLOB

    @property
    def container_name(self) -> str:
        """コンテナ名（bucket_nameのエイリアス）"""
        return self._azure_config.bucket_name

    def _get_container_client(self):
        """コンテナクライアントを取得"""
        return self._blob_service_client.get_container_client(self.container_name)

    def _get_blob_client(self, blob_name: str):
        """Blobクライアントを取得"""
        return self._blob_service_client.get_blob_client(
            container=self.container_name,
            blob=blob_name,
        )

    def _encode_blob_name(self, blob_name: str) -> str:
        """Blob 名は Unicode literal で扱う規約 (Azure 公式 UTF-8 サポート)。

        HTTP transit 段で Azure SDK が percent-encode するため、ここでは no-op。
        日本語・タイ語・ベトナム語など全 Unicode で動作する。
        """
        return blob_name

    def _generate_public_url(self, blob_url: str) -> str:
        """公開URLを生成（カスタムドメイン対応）"""
        custom_domain = self._azure_config.custom_domain
        if not custom_domain:
            return blob_url

        try:
            parsed = urlparse(blob_url)
            return f"https://{custom_domain}{parsed.path}"
        except Exception as e:
            logger.warning(f"Failed to generate custom domain URL: {e}")
            return blob_url

    async def ensure_bucket_exists(self) -> bool:
        """コンテナの存在確認・作成"""
        if not self._enabled:
            return False

        try:
            container_client = self._get_container_client()

            exists = await asyncio.get_event_loop().run_in_executor(
                None, container_client.exists
            )

            if not exists:
                if self._azure_config.auto_create_bucket:
                    await asyncio.get_event_loop().run_in_executor(
                        None, container_client.create_container
                    )
                    logger.info(f"Created container: {self.container_name}")
                else:
                    logger.error(
                        f"Container {self.container_name} does not exist "
                        "and auto_create_bucket is disabled"
                    )
                    return False

            return True

        except Exception as e:
            logger.error(f"Failed to ensure container exists: {e}")
            return False

    async def upload_file(
        self,
        file_path: str,
        object_name: Optional[str] = None,
        prefix: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> UploadResult:
        """
        ファイルをAzure Blobにアップロード

        Args:
            file_path: アップロードするファイルのローカルパス
            object_name: Blob名（省略時はファイル名が使用される）
            prefix: オブジェクト名プレフィックス（フォルダ構造を作成）
            metadata: 追加メタデータ（日本語はBase64エンコードされる）

        Returns:
            UploadResult: アップロード結果
                - success: 成功/失敗
                - object_name: アップロード先のBlob名
                - object_url: 公開URL
                - file_size: ファイルサイズ（bytes）
                - content_type: MIMEタイプ

        Example:
            >>> # 基本的なアップロード
            >>> result = await client.upload_file("/tmp/report.pdf")
            >>> if result.success:
            ...     print(f"Uploaded: {result.object_url}")
            >>>
            >>> # プレフィックス指定でフォルダ構造を作成
            >>> result = await client.upload_file(
            ...     file_path="/tmp/image.png",
            ...     prefix="uploads/2024/01",
            ...     metadata={"author": "user-123"}
            ... )
        """
        if not self._enabled:
            return UploadResult(
                success=False,
                error="Azure Blob Storage is not enabled",
                error_code="STORAGE_NOT_ENABLED",
            )

        try:
            # ファイルサイズ検証
            self._validate_file_size(file_path)

            file_path_obj = Path(file_path)

            # オブジェクト名決定
            if not object_name:
                object_name = file_path_obj.name

            # URLエンコード
            safe_object_name = self._encode_blob_name(object_name)

            # プレフィックス適用（呼び出し側が指定したprefixのみ使用）
            if prefix:
                full_object_name = f"{prefix}/{safe_object_name}"
            else:
                full_object_name = safe_object_name

            # コンテナ確認
            if not await self.ensure_bucket_exists():
                return UploadResult(
                    success=False,
                    error="Container is not available",
                    error_code="CONTAINER_NOT_AVAILABLE",
                )

            # Content-Type設定
            content_type = self._get_content_type(file_path)
            content_settings = ContentSettings(content_type=content_type)

            # メタデータサニタイズ
            safe_metadata = self._sanitize_metadata(metadata)

            # アップロード実行
            blob_client = self._get_blob_client(full_object_name)
            file_size = file_path_obj.stat().st_size

            with open(file_path_obj, 'rb') as data:
                await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: blob_client.upload_blob(
                        data,
                        overwrite=True,
                        content_settings=content_settings,
                        metadata=safe_metadata if safe_metadata else None,
                    )
                )

            # URL生成
            blob_url = self._generate_public_url(blob_client.url)

            logger.info("Successfully uploaded file to Azure Blob")

            return UploadResult(
                success=True,
                object_name=full_object_name,
                object_url=blob_url,
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
        ファイルをダウンロード（ストリーミング）

        大きなファイルでもメモリを圧迫しないよう、
        チャンク単位でストリーミングダウンロードします。

        Args:
            object_name: ダウンロードするBlob名
            download_path: ダウンロード先のローカルパス

        Returns:
            DownloadResult: ダウンロード結果
                - success: 成功/失敗
                - local_path: ダウンロード先パス
                - file_size: ファイルサイズ（bytes）
                - error: エラーメッセージ（失敗時）

        Example:
            >>> # Blobをダウンロード
            >>> result = await client.download_file(
            ...     object_name="uploads/2024/01/report.pdf",
            ...     download_path="/tmp/downloaded_report.pdf"
            ... )
            >>> if result.success:
            ...     print(f"Downloaded to: {result.local_path}")
            ...     print(f"Size: {result.file_size} bytes")
            >>> else:
            ...     print(f"Error: {result.error}")

        Note:
            ダウンロード先ディレクトリが存在しない場合は自動作成されます。
        """
        if not self._enabled:
            return DownloadResult(
                success=False,
                error="Azure Blob Storage is not enabled",
                error_code="STORAGE_NOT_ENABLED",
            )

        try:
            blob_client = self._get_blob_client(object_name)

            # 存在確認
            exists = await asyncio.get_event_loop().run_in_executor(
                None, blob_client.exists
            )
            if not exists:
                return DownloadResult(
                    success=False,
                    object_name=object_name,
                    error=f"Blob not found: {object_name}",
                    error_code="BLOB_NOT_FOUND",
                )

            # ダウンロード先ディレクトリ作成
            download_path_obj = Path(download_path)
            download_path_obj.parent.mkdir(parents=True, exist_ok=True)

            # ストリーミングダウンロード（メモリ効率化）
            def _streaming_download():
                with open(download_path_obj, 'wb') as f:
                    download_stream = blob_client.download_blob()
                    # chunks()でチャンク単位でダウンロード
                    for chunk in download_stream.chunks():
                        f.write(chunk)

            await asyncio.get_event_loop().run_in_executor(
                None, _streaming_download
            )

            file_size = download_path_obj.stat().st_size
            logger.info("Successfully downloaded blob")

            return DownloadResult(
                success=True,
                object_name=object_name,
                local_path=str(download_path_obj),
                file_size=file_size,
            )

        except Exception as e:
            logger.error(f"Failed to download blob: {e}")
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

        指定したプレフィックスに一致するBlobの一覧を取得します。

        Args:
            prefix: プレフィックスフィルタ（フォルダパスとして機能）
            max_results: 最大取得数（省略時は全件取得）

        Returns:
            ListResult: 一覧結果
                - success: 成功/失敗
                - objects: ObjectInfoのリスト
                - count: 取得件数

        Example:
            >>> # 全オブジェクト一覧
            >>> result = await client.list_objects()
            >>> print(f"Total: {result.count} objects")
            >>>
            >>> # プレフィックスでフィルタ
            >>> result = await client.list_objects(
            ...     prefix="uploads/2024/",
            ...     max_results=100
            ... )
            >>> for obj in result.objects:
            ...     print(f"{obj.name}: {obj.size} bytes")
        """
        if not self._enabled:
            return ListResult(
                success=False,
                error="Azure Blob Storage is not enabled",
                error_code="STORAGE_NOT_ENABLED",
            )

        try:
            container_client = self._get_container_client()

            blob_list = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: list(container_client.list_blobs(name_starts_with=prefix))
            )

            objects = []
            for blob in blob_list:
                if max_results and len(objects) >= max_results:
                    break
                objects.append(ObjectInfo(
                    name=blob.name,
                    size=blob.size,
                    last_modified=blob.last_modified.isoformat() if blob.last_modified else None,
                    content_type=blob.content_settings.content_type if blob.content_settings else None,
                ))

            logger.info(f"Listed {len(objects)} blobs")

            return ListResult(
                success=True,
                objects=objects,
                count=len(objects),
                prefix=prefix,
            )

        except Exception as e:
            logger.error(f"Failed to list blobs: {e}")
            return ListResult(
                success=False,
                error=f"List failed: {e}",
                error_code="LIST_FAILED",
            )

    async def delete_object(self, object_name: str) -> bool:
        """
        オブジェクトを削除

        Args:
            object_name: 削除するBlob名

        Returns:
            成功した場合True
        """
        if not self._enabled:
            return False

        try:
            blob_client = self._get_blob_client(object_name)

            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: blob_client.delete_blob(delete_snapshots="include")
            )

            logger.info("Successfully deleted blob")
            return True

        except Exception as e:
            logger.error(f"Failed to delete blob: {e}")
            return False

    async def object_exists(self, object_name: str) -> bool:
        """
        オブジェクトの存在確認

        Args:
            object_name: 確認するBlob名

        Returns:
            存在する場合True
        """
        if not self._enabled:
            return False

        try:
            blob_client = self._get_blob_client(object_name)
            return await asyncio.get_event_loop().run_in_executor(
                None, blob_client.exists
            )
        except Exception as e:
            logger.error(f"Failed to check blob existence: {e}")
            return False

    async def get_object_url(
        self,
        object_name: str,
        expires_in: Optional[int] = None,
    ) -> str:
        """
        オブジェクトのURLを取得

        Args:
            object_name: Blob名
            expires_in: SAS有効期限（秒）- 未実装、将来拡張用

        Returns:
            オブジェクトURL
        """
        if not self._enabled:
            return ""

        blob_client = self._get_blob_client(object_name)
        return self._generate_public_url(blob_client.url)

    def _sanitize_path(self, path: str) -> str:
        """パスをサニタイズ（パストラバーサル防止）

        Args:
            path: サニタイズするパス

        Returns:
            サニタイズされたパス（危険な文字を除去）
        """
        import re
        # パストラバーサル攻撃防止: ../ や ..\\ を除去
        # 先頭の / も除去
        sanitized = re.sub(r'\.\.[\\/]', '', path)
        sanitized = re.sub(r'^[\\/]+', '', sanitized)
        # NULL文字や制御文字を除去
        sanitized = re.sub(r'[\x00-\x1f]', '', sanitized)
        return sanitized

    async def download_objects_by_prefix(
        self,
        prefix: str,
        download_dir: str,
        max_concurrency: int = 8,
    ) -> Dict[str, Any]:
        """
        プレフィックスに一致するオブジェクトをすべてダウンロード（並列）

        Args:
            prefix: プレフィックス
            download_dir: ダウンロード先ディレクトリ
            max_concurrency: 並列ダウンロード数（環境変数 BLOB_DL_CONCURRENCY で上書き可、既定 8）

        Returns:
            ダウンロード結果サマリー

        Security:
            パストラバーサル攻撃を防ぐため、オブジェクト名をサニタイズし、
            ダウンロード先がdownload_dir配下であることを検証します。
            セキュリティチェックは download 実行前に同期的に完了させ、
            実 I/O のみを並列化します。
        """
        import asyncio
        import os

        list_result = await self.list_objects(prefix)
        if not list_result.success:
            return {
                "success": False,
                "error": list_result.error,
                "downloaded": [],
                "failed": [],
            }

        # 環境変数による上書き（運用調整用）
        env_concurrency = os.environ.get("BLOB_DL_CONCURRENCY")
        if env_concurrency:
            try:
                max_concurrency = max(1, int(env_concurrency))
            except ValueError:
                pass

        download_dir_obj = Path(download_dir).resolve()
        downloaded = []
        failed = []
        skipped = []

        # Phase 1: セキュリティチェック（同期）— DL 並列実行前に全件決着
        download_tasks = []  # (obj, download_path) のリスト
        for obj in list_result.objects:
            # プレフィックス除去
            relative_path = obj.name
            if obj.name.startswith(prefix):
                relative_path = obj.name[len(prefix):]

            # パスサニタイズ（パストラバーサル防止）
            relative_path = self._sanitize_path(relative_path)

            if not relative_path:
                skipped.append({
                    "object_name": obj.name,
                    "reason": "Invalid path after sanitization",
                })
                continue

            download_path = (download_dir_obj / relative_path).resolve()

            # パストラバーサル検証: download_dir配下であることを確認
            try:
                download_path.relative_to(download_dir_obj)
            except ValueError:
                logger.warning(
                    f"Path traversal attempt detected, skipping object"
                )
                skipped.append({
                    "object_name": obj.name,
                    "reason": "Path traversal detected",
                })
                continue

            download_tasks.append((obj, download_path))

        # Phase 2: 並列ダウンロード（Semaphore で同時実行数を制限）
        sem = asyncio.Semaphore(max_concurrency)

        async def _do_download(obj, download_path):
            async with sem:
                try:
                    result = await self.download_file(obj.name, str(download_path))
                    return obj, result, None
                except Exception as e:
                    return obj, None, e

        if download_tasks:
            results = await asyncio.gather(
                *[_do_download(obj, p) for obj, p in download_tasks],
                return_exceptions=False,
            )
            for obj, result, exc in results:
                if exc is not None:
                    failed.append({
                        "object_name": obj.name,
                        "error": str(exc),
                    })
                elif result.success:
                    downloaded.append({
                        "object_name": obj.name,
                        "local_path": result.local_path,
                        "file_size": result.file_size,
                    })
                else:
                    failed.append({
                        "object_name": obj.name,
                        "error": result.error,
                    })

        return {
            "success": True,
            "downloaded": downloaded,
            "failed": failed,
            "skipped": skipped,
            "success_count": len(downloaded),
            "failed_count": len(failed),
            "skipped_count": len(skipped),
        }

    async def close(self) -> None:
        """クライアントリソースをクローズ

        Note:
            例外が発生してもリソースを確実にクリーンアップします。
        """
        try:
            if self._blob_service_client:
                # BlobServiceClientはclose()メソッドを持たないが、
                # 将来のバージョンで追加される可能性があるため確認
                if hasattr(self._blob_service_client, 'close'):
                    self._blob_service_client.close()
        except Exception as e:
            logger.warning(f"Error closing Azure Blob client: {e}")
        finally:
            self._blob_service_client = None
            self._enabled = False
            logger.debug("AzureBlobStorageClient closed")
