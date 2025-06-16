from typing import List

import boto3  # type: ignore
from botocore.client import Config  # type: ignore

from whiskerrag_types.interface.loader_interface import BaseLoader
from whiskerrag_types.model.knowledge import (
    Knowledge,
    KnowledgeSourceEnum,
    KnowledgeTypeEnum,
)
from whiskerrag_types.model.knowledge_source import OpenUrlSourceConfig, S3SourceConfig
from whiskerrag_types.model.multi_modal import Image
from whiskerrag_utils.registry import RegisterTypeEnum, register


@register(RegisterTypeEnum.KNOWLEDGE_LOADER, KnowledgeSourceEnum.CLOUD_STORAGE_IMAGE)
class CloudStorageTextLoader(BaseLoader[Image]):
    def read_file_content(self, file_path: str) -> str:
        """读取文件内容"""
        try:
            knowledge_type = self.knowledge.knowledge_type
            if knowledge_type is not KnowledgeTypeEnum.IMAGE:
                raise NotImplementedError("knowledge_type only image can be loaded ")

            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

        except UnicodeDecodeError:
            # 如果UTF-8解码失败，尝试使用其他编码或忽略错误
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

    def get_download_url(self, config: S3SourceConfig, expires_in: int = 3600) -> str:
        """
        生成 S3 对象的预签名下载 URL

        Args:
            config: S3 配置信息
            expires_in: URL 有效期(秒),默认1小时

        Returns:
            预签名下载 URL
        """
        # 创建 S3 客户端
        s3_client = boto3.client(
            "s3",
            region_name=config.region,
            aws_access_key_id=config.access_key,
            aws_secret_access_key=config.secret_key,
            aws_session_token=config.auth_info,
            config=Config(signature_version="s3v4"),
        )

        # 生成预签名 URL
        try:
            url: str = s3_client.generate_presigned_url(
                "get_object",
                Params=(
                    {
                        "Bucket": config.bucket,
                        "Key": config.key,
                        "VersionId": config.version_id,
                    }
                    if config.version_id
                    else {"Bucket": config.bucket, "Key": config.key}
                ),
                ExpiresIn=expires_in,
            )
            return url
        except Exception as e:
            raise Exception(f"Failed to generate download URL: {str(e)}")

    async def load(self) -> List[Image]:
        """加载文件内容"""
        try:
            if isinstance(self.knowledge.source_config, S3SourceConfig):
                url = self.get_download_url(self.knowledge.source_config)

            elif isinstance(self.knowledge.source_config, OpenUrlSourceConfig):
                url = self.knowledge.source_config.url

            else:
                raise AttributeError(
                    "Invalid source config type for CloudStorageTextLoader"
                )
            return [Image(url=url)]

        except Exception as e:
            raise Exception(f"Failed to load content from cloud storage: {e}")

    async def decompose(self) -> List[Knowledge]:
        return []

    async def on_load_finished(self) -> None:
        # No specific cleanup needed for CloudStorageTextLoader
        pass
