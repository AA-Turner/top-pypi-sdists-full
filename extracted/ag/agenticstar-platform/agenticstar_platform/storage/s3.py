"""
AGENTICSTAR Platform SDK - AWS S3 Storage Client
AWS S3へのファイル操作を提供

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
    ListResult,
    ObjectInfo,
    S3Config,
    StorageClientBase,
    StorageConfigError,
    StorageConnectionError,
    StorageOperationError,
    StorageProvider,
    UploadResult,
)

logger = logging.getLogger(__name__)

# boto3 availability check
try:
    import boto3
    from botocore.exceptions import ClientError
    S3_AVAILABLE = True
except ImportError:
    boto3 = None
    ClientError = Exception
    S3_AVAILABLE = False


class S3StorageClient(StorageClientBase):
    """
    AWS S3ストレージクライアント

    Features:
    - ファイルアップロード・ダウンロード
    - オブジェクト一覧・削除
    - 署名付きURL生成（presigned URL）
    - カスタムドメイン対応
    - 日本語ファイル名対応（URLエンコード）
    - メタデータサニタイズ（Base64エンコード）

    Example:
        config = S3Config(
            bucket_name="my-bucket",
            aws_access_key_id="AKIA...",
            aws_secret_access_key="...",
            region_name="ap-northeast-1",
        )
        client = S3StorageClient(config)
        result = await client.upload_file("/path/to/file.txt")
    """

    def __init__(self, config: S3Config):
        """
        Initialize AWS S3 Storage Client

        Args:
            config: S3Config instance

        Raises:
            StorageConfigError: 設定が不正な場合
            StorageConnectionError: 接続に失敗した場合
        """
        super().__init__(config)

        if not S3_AVAILABLE:
            raise StorageConfigError(
                "boto3 package is not installed. "
                "Install with: pip install 'agenticstar-platform[storage-aws]'"
            )

        if not config.bucket_name:
            raise StorageConfigError("S3 bucket_name is required")

        if not config.aws_access_key_id or not config.aws_secret_access_key:
            raise StorageConfigError(
                "S3 requires aws_access_key_id and aws_secret_access_key"
            )

        self._s3_config: S3Config = config
        self._s3_client = None

        try:
            session = boto3.Session(
                aws_access_key_id=self._get_api_key(config.aws_access_key_id),
                aws_secret_access_key=self._get_api_key(config.aws_secret_access_key),
                region_name=config.region_name,
            )

            client_kwargs = {}
            if config.endpoint_url:
                client_kwargs['endpoint_url'] = config.endpoint_url

            self._s3_client = session.client('s3', **client_kwargs)
            self._enabled = config.enabled

            logger.info(
                f"S3StorageClient initialized - bucket={config.bucket_name}, "
                f"region={config.region_name}"
            )

        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {e}")
            raise StorageConnectionError(
                f"Failed to connect to S3: {e}"
            ) from e

    @property
    def provider(self) -> StorageProvider:
        return StorageProvider.AWS_S3

    @property
    def bucket_name(self) -> str:
        return self._s3_config.bucket_name

    # _encode_object_name: StorageClientBase に移動済み
    # _sanitize_path: StorageClientBase に移動済み

    def _generate_public_url(self, object_name: str) -> str:
        """公開URLを生成（カスタムドメイン対応）"""
        custom_domain = self._s3_config.custom_domain
        if custom_domain:
            return f"https://{custom_domain}/{object_name}"

        if self._s3_config.endpoint_url:
            return f"{self._s3_config.endpoint_url}/{self.bucket_name}/{object_name}"

        return f"https://{self.bucket_name}.s3.{self._s3_config.region_name}.amazonaws.com/{object_name}"

    async def ensure_bucket_exists(self) -> bool:
        """バケットの存在確認・作成"""
        if not self._enabled:
            return False

        try:
            await asyncio.get_running_loop().run_in_executor(
                None,
                lambda: self._s3_client.head_bucket(Bucket=self.bucket_name)
            )
            return True
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code in ('404', 'NoSuchBucket'):
                if self._s3_config.auto_create_bucket:
                    try:
                        create_params = {'Bucket': self.bucket_name}
                        if self._s3_config.region_name != 'us-east-1':
                            create_params['CreateBucketConfiguration'] = {
                                'LocationConstraint': self._s3_config.region_name
                            }
                        await asyncio.get_running_loop().run_in_executor(
                            None,
                            lambda: self._s3_client.create_bucket(**create_params)
                        )
                        logger.info(f"Created S3 bucket: {self.bucket_name}")
                        return True
                    except Exception as create_error:
                        logger.error(f"Failed to create bucket: {create_error}")
                        return False
                else:
                    logger.error(f"Bucket {self.bucket_name} does not exist")
                    return False
            logger.error(f"Failed to check bucket: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to ensure bucket exists: {e}")
            return False

    async def upload_file(
        self,
        file_path: str,
        object_name: Optional[str] = None,
        prefix: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> UploadResult:
        """
        ファイルをS3にアップロード

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
                error="S3 Storage is not enabled",
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

            extra_args = {
                'ContentType': content_type,
            }
            if safe_metadata:
                extra_args['Metadata'] = safe_metadata

            file_size = file_path_obj.stat().st_size

            await asyncio.get_running_loop().run_in_executor(
                None,
                lambda: self._s3_client.upload_file(
                    str(file_path_obj),
                    self.bucket_name,
                    full_object_name,
                    ExtraArgs=extra_args,
                )
            )

            object_url = self._generate_public_url(full_object_name)

            logger.info("Successfully uploaded file to S3")

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
        ファイルをS3からダウンロード（ストリーミング）

        Args:
            object_name: ダウンロードするオブジェクト名
            download_path: ダウンロード先のローカルパス

        Returns:
            DownloadResult: ダウンロード結果
        """
        if not self._enabled:
            return DownloadResult(
                success=False,
                error="S3 Storage is not enabled",
                error_code="STORAGE_NOT_ENABLED",
            )

        try:
            # 存在確認
            exists = await self.object_exists(object_name)
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
                lambda: self._s3_client.download_file(
                    self.bucket_name,
                    object_name,
                    str(download_path_obj),
                )
            )

            file_size = download_path_obj.stat().st_size
            logger.info("Successfully downloaded object from S3")

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
                error="S3 Storage is not enabled",
                error_code="STORAGE_NOT_ENABLED",
            )

        try:
            paginator = self._s3_client.get_paginator('list_objects_v2')
            page_config = {
                'Bucket': self.bucket_name,
                'Prefix': prefix,
            }
            if max_results:
                page_config['PaginationConfig'] = {'MaxItems': max_results}

            def _list():
                objects = []
                for page in paginator.paginate(**page_config):
                    for obj in page.get('Contents', []):
                        objects.append(ObjectInfo(
                            name=obj['Key'],
                            size=obj.get('Size', 0),
                            last_modified=obj['LastModified'].isoformat() if obj.get('LastModified') else None,
                            content_type=None,
                        ))
                return objects

            objects = await asyncio.get_running_loop().run_in_executor(None, _list)

            logger.info(f"Listed {len(objects)} objects from S3")

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
            await asyncio.get_running_loop().run_in_executor(
                None,
                lambda: self._s3_client.delete_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                )
            )
            logger.info("Successfully deleted object from S3")
            return True

        except Exception as e:
            logger.error(f"Failed to delete object: {e}")
            return False

    async def object_exists(self, object_name: str) -> bool:
        """オブジェクトの存在確認"""
        if not self._enabled:
            return False

        try:
            await asyncio.get_running_loop().run_in_executor(
                None,
                lambda: self._s3_client.head_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                )
            )
            return True
        except ClientError as e:
            if e.response.get('Error', {}).get('Code', '') == '404':
                return False
            logger.error(f"Failed to check object existence: {e}")
            return False
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
                url = await asyncio.get_running_loop().run_in_executor(
                    None,
                    lambda: self._s3_client.generate_presigned_url(
                        'get_object',
                        Params={
                            'Bucket': self.bucket_name,
                            'Key': object_name,
                        },
                        ExpiresIn=expires_in,
                    )
                )
                return url
            except Exception as e:
                logger.error(f"Failed to generate presigned URL: {e}")
                return ""

        return self._generate_public_url(object_name)

    # download_objects_by_prefix: StorageClientBase に移動済み

    async def close(self) -> None:
        """クライアントリソースをクローズ"""
        try:
            if self._s3_client:
                self._s3_client.close()
        except Exception as e:
            logger.warning(f"Error during S3 client close: {e}")
        finally:
            self._s3_client = None
            self._enabled = False
            logger.debug("S3StorageClient closed")
