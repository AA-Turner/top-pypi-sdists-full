import json
from typing import List

from langchain_text_splitters import RecursiveJsonSplitter

from whiskerrag_types.interface.parser_interface import BaseParser, ParseResult
from whiskerrag_types.model import JSONSplitConfig, Knowledge
from whiskerrag_types.model.multi_modal import Text
from whiskerrag_utils.registry import RegisterTypeEnum, register


@register(RegisterTypeEnum.PARSER, "json")
class JSONParser(BaseParser[Text]):
    async def parse(
        self,
        knowledge: Knowledge,
        content: Text,
    ) -> ParseResult:
        """Splits JSON content into smaller chunks based on the provided configuration."""
        json_content = {}
        split_config = knowledge.split_config
        if not isinstance(split_config, JSONSplitConfig):
            raise TypeError("knowledge.split_config must be of type JSONSplitConfig")
        try:
            json_content = json.loads(content.content)
            if not isinstance(json_content, dict):
                raise ValueError("JSON content must be a dictionary.")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON content provided for splitting.")
        except ValueError as e:
            raise ValueError(f"Error processing JSON content: {str(e)}")
        splitter = RecursiveJsonSplitter(
            max_chunk_size=split_config.max_chunk_size,
            min_chunk_size=split_config.min_chunk_size,
        )
        split_texts = splitter.split_text(
            json_content, convert_lists=True, ensure_ascii=False
        )
        return [Text(content=text, metadata=content.metadata) for text in split_texts]

    async def batch_parse(
        self,
        knowledge: Knowledge,
        content_list: List[Text],
    ) -> List[ParseResult]:
        return [await self.parse(knowledge, content) for content in content_list]
