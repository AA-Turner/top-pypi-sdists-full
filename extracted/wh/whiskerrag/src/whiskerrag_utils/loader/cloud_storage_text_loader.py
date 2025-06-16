import os
from typing import List, Tuple

from whiskerrag_types.interface.loader_interface import BaseLoader
from whiskerrag_types.model.knowledge import (
    Knowledge,
    KnowledgeSourceEnum,
    KnowledgeTypeEnum,
)
from whiskerrag_types.model.knowledge_source import OpenUrlSourceConfig, S3SourceConfig
from whiskerrag_types.model.multi_modal import Text
from whiskerrag_utils.loader.utils import (
    download_from_s3_to_local,
    download_from_url_to_local,
)
from whiskerrag_utils.registry import RegisterTypeEnum, register


@register(RegisterTypeEnum.KNOWLEDGE_LOADER, KnowledgeSourceEnum.CLOUD_STORAGE_TEXT)
class CloudStorageTextLoader(BaseLoader[Text]):
    def read_file_content(self, file_path: str) -> str:
        """读取文件内容"""
        try:
            knowledge_type = self.knowledge.knowledge_type
            if knowledge_type in [
                KnowledgeTypeEnum.JSON,
                KnowledgeTypeEnum.TEXT,
                KnowledgeTypeEnum.MARKDOWN,
            ]:
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()

            # Word文档
            elif knowledge_type is KnowledgeTypeEnum.DOCX:
                raise NotImplementedError("Word document processing not implemented")

            # PDF文档
            elif knowledge_type is KnowledgeTypeEnum.PDF:
                raise NotImplementedError("PDF processing not implemented")

            else:
                raise ValueError(f"Unsupported file format: {knowledge_type}")

        except UnicodeDecodeError:
            # 如果UTF-8解码失败，尝试使用其他编码或忽略错误
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

    async def download_from_s3(self, config: S3SourceConfig) -> Tuple[str, dict]:
        """从S3下载文件内容"""
        try:
            temp_file, file_metadata = download_from_s3_to_local(config)

            try:
                content = self.read_file_content(temp_file)
                return content, file_metadata

            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)

        except Exception as e:
            raise Exception(f"Failed to process S3 file: {str(e)}")

    async def download_from_url(self, config: OpenUrlSourceConfig) -> Tuple[str, dict]:
        """从URL下载文件内容"""
        try:
            temp_file, file_metadata = download_from_url_to_local(config.url)

            try:
                content = self.read_file_content(temp_file)
                return content, file_metadata

            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)

        except Exception as e:
            raise Exception(f"Failed to process file: {str(e)}")

    async def load(self) -> List[Text]:
        """加载文件内容"""
        try:
            if isinstance(self.knowledge.source_config, S3SourceConfig):
                content, source_metadata = await self.download_from_s3(
                    self.knowledge.source_config
                )

            elif isinstance(self.knowledge.source_config, OpenUrlSourceConfig):
                content, source_metadata = await self.download_from_url(
                    self.knowledge.source_config
                )

            else:
                raise AttributeError(
                    "Invalid source config type for CloudStorageTextLoader"
                )
            combined_metadata = {**self.knowledge.metadata, **source_metadata}
            return [Text(content=content, metadata=combined_metadata)]

        except Exception as e:
            raise Exception(f"Failed to load content from cloud storage: {e}")

    async def decompose(self) -> List[Knowledge]:
        return []

    async def on_load_finished(self) -> None:
        pass
