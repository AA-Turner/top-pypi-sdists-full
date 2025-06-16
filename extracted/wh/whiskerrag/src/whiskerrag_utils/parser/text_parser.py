from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from whiskerrag_types.interface.parser_interface import BaseParser, ParseResult
from whiskerrag_types.model import Knowledge, TextSplitConfig
from whiskerrag_types.model.multi_modal import Text
from whiskerrag_utils.registry import RegisterTypeEnum, register


@register(RegisterTypeEnum.PARSER, "text")
class TextParser(BaseParser[Text]):
    async def parse(
        self,
        knowledge: Knowledge,
        content: Text,
    ) -> ParseResult:
        split_config = knowledge.split_config
        if not isinstance(split_config, TextSplitConfig):
            raise TypeError("knowledge.split_config must be of type TextSplitConfig")
        separators = split_config.separators or [
            # First, try to split along Markdown headings (starting with level 2)
            "\n#{1,6} ",
            # Note the alternative syntax for headings (below) is not handled here
            # Heading level 2
            # ---------------
            # End of code block
            "```\n",
            # Horizontal lines
            "\n\\*\\*\\*+\n",
            "\n---+\n",
            "\n___+\n",
            # Note that this splitter doesn't handle horizontal lines defined
            # by *three or more* of ***, ---, or ___, but this is not handled
            "\n\n",
            "\n",
            " ",
            "",
        ]
        if "" not in separators:
            separators.append("")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=split_config.chunk_size,
            chunk_overlap=split_config.chunk_overlap,
            separators=separators,
            is_separator_regex=split_config.is_separator_regex,
            keep_separator=split_config.keep_separator or False,
        )
        split_texts = splitter.split_text(content.content)
        return [Text(content=text, metadata=content.metadata) for text in split_texts]

    async def batch_parse(
        self,
        knowledge: Knowledge,
        content_list: List[Text],
    ) -> List[ParseResult]:
        return [await self.parse(knowledge, content) for content in content_list]
