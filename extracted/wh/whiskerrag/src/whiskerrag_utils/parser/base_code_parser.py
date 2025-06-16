from typing import List, Union

from langchain_text_splitters import RecursiveCharacterTextSplitter

from whiskerrag_types.interface.parser_interface import BaseParser, ParseResult
from whiskerrag_types.model.knowledge import Knowledge
from whiskerrag_types.model.multi_modal import Image, Text
from whiskerrag_types.model.splitter import BaseCodeSplitConfig
from whiskerrag_utils.registry import RegisterTypeEnum, register


@register(RegisterTypeEnum.PARSER, "base_code")
class CodeParser(BaseParser[Text]):

    def _calculate_line_position(
        self, content: str, chunk: str, char_start: int
    ) -> dict:
        """
        Calculate line-based position information for a code chunk

        Args:
            content: Original full content
            chunk: The code chunk
            char_start: Character start position in the original content

        Returns:
            dict: Position information including line numbers
        """
        # Split content into lines for position calculation
        lines = content.split("\n")

        # Calculate start line
        current_char = 0
        start_line = 1
        start_column = 1

        for line_num, line in enumerate(lines, 1):
            line_length = len(line) + 1  # +1 for newline character
            if current_char + line_length > char_start:
                start_line = line_num
                start_column = char_start - current_char + 1
                break
            current_char += line_length

        # Calculate end line
        chunk_lines = chunk.split("\n")
        end_line = start_line + len(chunk_lines) - 1

        # Calculate end column
        if len(chunk_lines) == 1:
            end_column = start_column + len(chunk_lines[0]) - 1
        else:
            end_column = len(chunk_lines[-1])

        return {
            "start_line": start_line,
            "end_line": end_line,
            "start_column": start_column,
            "end_column": end_column,
            "total_lines": len(chunk_lines),
        }

    async def parse(
        self,
        knowledge: Knowledge,
        content: Text,
    ) -> ParseResult:
        split_config = knowledge.split_config
        if not isinstance(split_config, BaseCodeSplitConfig):
            raise TypeError("knowledge.split_config must be of type CodeSplitConfig")
        splitter = RecursiveCharacterTextSplitter.from_language(
            split_config.language,
            chunk_size=split_config.chunk_size,
            chunk_overlap=split_config.chunk_overlap,
        )
        split_docs = splitter.split_text(
            content.content,
        )

        # Create Text objects with proper metadata inheritance and position info
        results: List[Union[Text, Image]] = []
        current_position = 0

        for chunk_index, doc in enumerate(split_docs):
            # Start with knowledge.metadata as base
            combined_metadata = {**knowledge.metadata}

            # Add Text.metadata from content (loader/previous parser stage)
            if content.metadata:
                combined_metadata.update(content.metadata)

            # Find the actual start position of this chunk in the original content
            doc_start = content.content.find(doc, current_position)
            if doc_start == -1:
                # Fallback if exact match not found
                doc_start = current_position

            doc_end = doc_start + len(doc)

            # Calculate line-based position information
            line_position = self._calculate_line_position(
                content.content, doc, doc_start
            )
            # Add processing information from current parser stage
            parser_metadata = {
                "chunk_index": chunk_index,
                "parser_type": "base_code",
                "position": line_position,
            }

            combined_metadata.update(parser_metadata)

            results.append(Text(content=doc, metadata=combined_metadata))
            current_position = doc_end

        return results

    async def batch_parse(
        self,
        knowledge: Knowledge,
        content_list: List[Text],
    ) -> List[ParseResult]:
        return [await self.parse(knowledge, content) for content in content_list]
