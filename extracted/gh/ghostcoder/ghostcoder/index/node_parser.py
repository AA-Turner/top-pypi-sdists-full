import logging
import traceback
from typing import Sequence, List, Optional, Dict, Any

from langchain.text_splitter import TextSplitter, TokenTextSplitter
from llama_index import Document
from llama_index.callbacks import CBEventType, CallbackManager
from llama_index.callbacks.schema import EventPayload
from llama_index.node_parser import NodeParser
from llama_index.node_parser.node_utils import build_nodes_from_splits
from llama_index.schema import BaseNode, MetadataMode, TextNode, NodeRelationship
from llama_index.utils import get_tqdm_iterable
from pydantic import Field

from ghostcoder.codeblocks import create_parser, CodeBlock, CodeBlockType
from ghostcoder.index.schema import CodeDocument, CodeNode
from ghostcoder.utils import count_tokens


class CodeNodeParser(NodeParser):

    text_splitter: TextSplitter = Field(
        description="Text splitter to use for splitting non code documents into nodes."
    )

    include_non_code_files: bool = Field(
        default=True, description="Whether or not to include non code files."
    )

    non_code_file_extensions: List[str] = Field(
        default=["md", "txt"], description="File extensions to consider as non code files."
    )

    chunk_size: int = Field(
        default=1500, description="Chunk size to use for splitting code documents."
    )

    min_split_size: int = Field(
        default=500, description="Min tokens to split code."
    )

    @classmethod
    def from_defaults(
        cls,
        chunk_size: int = 1500,
        min_split_size: int = 500,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
        text_splitter: Optional[TextSplitter] = None,
        include_non_code_files: bool = True,
        non_code_file_extensions: Optional[List[str]] = ["md", "txt"],
        callback_manager: Optional[CallbackManager] = None,
    ) -> "CodeNodeParser":
        callback_manager = callback_manager or CallbackManager([])

        if not text_splitter:
            text_splitter = TokenTextSplitter(
                chunk_size=chunk_size
            )
        return cls(
            text_splitter=text_splitter,
            chunk_size=chunk_size,
            min_split_size=min_split_size,
            include_non_code_files=include_non_code_files,
            non_code_file_extensions=non_code_file_extensions,
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            callback_manager=callback_manager,
        )

    @classmethod
    def class_name(cls):
        return "CodeNodeParser"

    def _parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
        nodes_with_progress = get_tqdm_iterable(
            nodes, show_progress, "Parsing documents into nodes"
        )

        all_nodes: List[BaseNode] = []
        for doc in nodes_with_progress:

            if isinstance(doc, CodeDocument) and doc.codeblock:
                splitted_blocks = doc.codeblock.get_indexable_blocks()
                for splitted_block in splitted_blocks:
                    node_metadata = doc.metadata.copy()

                    if splitted_block.type in [CodeBlockType.TEST_CASE, CodeBlockType.TEST_SUITE]:
                        node_metadata["purpose"] = "test"
                    else:
                        node_metadata["purpose"] = "code"

                    node_metadata["block_type"] = str(splitted_block.type)

                    if splitted_block.identifier:
                        node_metadata["block_path"] = "/".join(splitted_block.full_path())
                    elif splitted_block.type is not CodeBlockType.MODULE:
                        tree = doc.codeblock.to_tree(debug=False,
                                                     show_tokens=True,
                                                     include_types=[CodeBlockType.FUNCTION, CodeBlockType.CLASS])
                        logging.debug(f"No ID for block {tree}")

                    content = splitted_block.to_context_string(max_tokens=self.chunk_size)

                    tokens = count_tokens(content)
                    if tokens > 4000:
                        logging.info(
                            f"Skip node [{splitted_block.identifier}] in {doc.id_} with {tokens} tokens")
                        logging.debug(splitted_block.to_tree(debug=False,
                                                             show_tokens=True,
                                                             include_types=[CodeBlockType.FUNCTION, CodeBlockType.CLASS]))
                        continue

                    if tokens > self.chunk_size:
                        logging.info(f"Big node [{splitted_block.identifier}] in {doc.id_} with {tokens} tokens")
                        logging.debug(splitted_block.to_tree(debug=False,
                                                             show_tokens=True,
                                                             include_types=[CodeBlockType.FUNCTION, CodeBlockType.CLASS]))

                    # TODO: Add relationships between code blocks
                    node = TextNode(
                        text=content,
                        codeblock=splitted_block,
                        metadata=node_metadata,
                        excluded_embed_metadata_keys=doc.excluded_embed_metadata_keys,
                        excluded_llm_metadata_keys=doc.excluded_llm_metadata_keys,
                        metadata_seperator=doc.metadata_seperator,
                        metadata_template=doc.metadata_template,
                        text_template=doc.text_template,
                        relationships={NodeRelationship.SOURCE: doc.as_related_node_info()},
                    )

                    all_nodes.append(node)
            else:
                if not self.include_non_code_files or node_metadata["file_extension"] not in self.non_code_file_extensions:
                    continue

                splits = self.text_splitter.split_text(doc.get_content())
                all_nodes.extend(build_nodes_from_splits(splits, doc))

        return all_nodes
