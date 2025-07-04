import json
from typing import Any, Dict, List

from langchain_text_splitters import RecursiveJsonSplitter

from whiskerrag_types.interface.parser_interface import BaseParser, ParseResult
from whiskerrag_types.model import JSONSplitConfig, Knowledge
from whiskerrag_types.model.knowledge import KnowledgeTypeEnum
from whiskerrag_types.model.multi_modal import Text
from whiskerrag_utils.registry import RegisterTypeEnum, register


def parse_json_content(content: str) -> Dict[str, Any]:
    """
    Parse JSON content with better compatibility.

    Args:
        content: JSON string content

    Returns:
        Parsed JSON object as dictionary (arrays are converted to {"data": [...]})

    Raises:
        ValueError: If content is not valid JSON or is not a dict/list
    """
    try:
        json_content = json.loads(content)

        # Support both dict and list formats
        if isinstance(json_content, dict):
            return json_content
        elif isinstance(json_content, list):
            # Convert list to dict format for processing
            return {"data": json_content}
        else:
            raise ValueError("JSON content must be a dictionary or array.")

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON content provided for splitting: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing JSON content: {str(e)}")


@register(RegisterTypeEnum.PARSER, KnowledgeTypeEnum.JSON)
class JSONParser(BaseParser[Text]):
    async def parse(
        self,
        knowledge: Knowledge,
        content: Text,
    ) -> ParseResult:
        """Splits JSON content into smaller chunks based on the provided configuration."""
        split_config = knowledge.split_config
        if not isinstance(split_config, JSONSplitConfig):
            raise TypeError("knowledge.split_config must be of type JSONSplitConfig")

        # Use the new helper function for better JSON compatibility
        json_content = parse_json_content(content.content)

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
