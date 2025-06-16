from typing import List

from whiskerrag_types.interface.parser_interface import BaseParser, ParseResult
from whiskerrag_types.model.knowledge import Knowledge
from whiskerrag_types.model.multi_modal import Image
from whiskerrag_utils.registry import RegisterTypeEnum, register


@register(RegisterTypeEnum.PARSER, "base_image")
class BaseTextParser(BaseParser[Image]):

    async def parse(
        self,
        knowledge: Knowledge,
        content: Image,
    ) -> ParseResult:
        return [content]

    async def batch_parse(
        self,
        knowledge: Knowledge,
        content_list: List[Image],
    ) -> List[ParseResult]:
        return [await self.parse(knowledge, content) for content in content_list]
