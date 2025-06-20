from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from whiskerrag_types.interface.parser_interface import BaseParser, ParseResult
from whiskerrag_types.model import Knowledge
from whiskerrag_types.model.knowledge import KnowledgeTypeEnum
from whiskerrag_types.model.multi_modal import Text
from whiskerrag_types.model.splitter import GithubRepoParseConfig
from whiskerrag_utils.registry import RegisterTypeEnum, register


@register(RegisterTypeEnum.PARSER, KnowledgeTypeEnum.GITHUB_REPO)
class GithubRepoParser(BaseParser[Text]):
    """
    Parser for GitHub repository project tree structure, excluding individual code file content
    """

    async def parse(
        self,
        knowledge: Knowledge,
        content: Text,
    ) -> ParseResult:
        split_config = knowledge.split_config
        if not isinstance(split_config, GithubRepoParseConfig):
            raise TypeError(
                "knowledge.split_config must be of type GithubRepoParseConfig"
            )
        separators = [
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
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=split_config.chunk_size,
            chunk_overlap=split_config.chunk_overlap,
            separators=separators,
            is_separator_regex=True,
            keep_separator=False,
        )
        split_texts = splitter.split_text(content.content)
        return [Text(content=text, metadata=content.metadata) for text in split_texts]

    async def batch_parse(
        self,
        knowledge: Knowledge,
        content_list: List[Text],
    ) -> List[ParseResult]:
        return [await self.parse(knowledge, content) for content in content_list]
