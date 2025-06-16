from typing import List, Union

from langchain_text_splitters import RecursiveCharacterTextSplitter

from whiskerrag_types.interface.parser_interface import BaseParser, ParseResult
from whiskerrag_types.model.knowledge import Knowledge
from whiskerrag_types.model.multi_modal import Image, Text
from whiskerrag_types.model.splitter import BaseCharSplitConfig
from whiskerrag_utils.registry import RegisterTypeEnum, register


@register(RegisterTypeEnum.PARSER, "base_text")
class BaseTextParser(BaseParser[Text]):
    async def parse(
        self,
        knowledge: Knowledge,
        content: Text,
    ) -> ParseResult:
        split_config = knowledge.split_config
        if not isinstance(split_config, BaseCharSplitConfig):
            raise TypeError(
                "knowledge.split_config must be of type BaseCharSplitConfig"
            )
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
            keep_separator=False,
        )
        split_texts = splitter.split_text(content.content)

        # Create Text objects with proper metadata inheritance
        results: List[Union[Text, Image]] = []
        for text in split_texts:
            # Start with knowledge.metadata as base
            combined_metadata = {**knowledge.metadata}

            # Add Text.metadata from content (loader/previous parser stage)
            if content.metadata:
                combined_metadata.update(content.metadata)

            parser_metadata: dict[str, str] = {}

            combined_metadata.update(parser_metadata)
            results.append(Text(content=text, metadata=combined_metadata))

        return results

    async def batch_parse(
        self,
        knowledge: Knowledge,
        content_list: List[Text],
    ) -> List[ParseResult]:
        return [await self.parse(knowledge, content) for content in content_list]
