from typing import List

from whiskerrag_types.interface.loader_interface import BaseLoader
from whiskerrag_types.model.knowledge import (
    Knowledge,
    KnowledgeSourceEnum,
    TextSourceConfig,
)
from whiskerrag_types.model.multi_modal import Text
from whiskerrag_utils.registry import RegisterTypeEnum, register


@register(RegisterTypeEnum.KNOWLEDGE_LOADER, KnowledgeSourceEnum.USER_INPUT_TEXT)
class TextLoader(BaseLoader[Text]):

    async def load(self) -> List[Text]:
        if isinstance(self.knowledge.source_config, TextSourceConfig):
            return [
                Text(
                    content=self.knowledge.source_config.text,
                    metadata=self.knowledge.metadata,
                )
            ]
        raise AttributeError(
            "source_config does not have a 'text' attribute for the current type."
        )

    async def decompose(self) -> List[Knowledge]:
        return []

    async def on_load_finished(self) -> None:
        pass
