from typing import List

from whiskerrag_types.interface.loader_interface import BaseLoader
from whiskerrag_types.model.knowledge import Knowledge, KnowledgeSourceEnum
from whiskerrag_types.model.knowledge_source import YuqueSourceConfig
from whiskerrag_types.model.multi_modal import Text
from whiskerrag_utils.helper.yuque import ExtendedYuqueLoader
from whiskerrag_utils.registry import RegisterTypeEnum, register


@register(RegisterTypeEnum.KNOWLEDGE_LOADER, KnowledgeSourceEnum.YUQUE)
class WhiskerYuqueLoader(BaseLoader[Text]):

    async def load(self) -> List[Text]:
        if not isinstance(self.knowledge.source_config, YuqueSourceConfig):
            raise AttributeError("Invalid source config type for YuqueLoader")
        group_login = self.knowledge.source_config.group_login
        book_slug = self.knowledge.source_config.book_slug
        document_id = self.knowledge.source_config.document_id
        text_list: List[Text] = []
        try:
            loader = ExtendedYuqueLoader(
                access_token=self.knowledge.source_config.auth_info,
                api_url=self.knowledge.source_config.api_url,
            )
            # Extract book_id and document_id from source_config
            group_login = self.knowledge.source_config.group_login
            book_slug = self.knowledge.source_config.book_slug
            document_id = self.knowledge.source_config.document_id
            if not group_login:
                raise ValueError("group_login is needed for WhiskerYuqueLoader")
            if not book_slug:
                raise ValueError("book_slug is needed for WhiskerYuqueLoader")
            if not document_id:
                raise ValueError("document_id is needed for WhiskerYuqueLoader")

            try:
                parsed_document = loader.load_document_by_path(
                    group_login, book_slug, document_id
                )
                text_list.append(
                    Text(
                        content=parsed_document.page_content,
                        metadata=parsed_document.metadata,
                    )
                )

            except Exception as e:
                raise ValueError(f"Failed to get document: {e}")
            # Check if only book_id is provided
            return text_list

        except Exception as e:
            raise Exception(f"Failed to load content from Yuque: {e}")

    async def decompose(self) -> List[Knowledge]:
        return []

    async def on_load_finished(self) -> None:
        pass
