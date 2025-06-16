from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar, Union

from whiskerrag_types.interface.embed_interface import Image
from whiskerrag_types.model.knowledge import Knowledge
from whiskerrag_types.model.multi_modal import Text

ParseResult = List[Union[Image, Text]]
ContentType = TypeVar("ContentType")


class BaseParser(Generic[ContentType], ABC):
    @abstractmethod
    async def parse(
        self,
        knowledge: Knowledge,
        content: ContentType,
    ) -> ParseResult:
        pass

    @abstractmethod
    async def batch_parse(
        self, knowledge: Knowledge, content: List[ContentType]
    ) -> List[ParseResult]:
        pass
