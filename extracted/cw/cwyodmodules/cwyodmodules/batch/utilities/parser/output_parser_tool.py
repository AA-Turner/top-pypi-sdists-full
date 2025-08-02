from typing import List
import re
import json
from .parser_base import ParserBase
from ..common.source_document import SourceDocument

from ...utilities.helpers.env_helper import EnvHelper
from mgmt_config import logger
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT


class OutputParserTool(ParserBase):
    """
    OutputParserTool is a class that extends ParserBase to parse answers and extract relevant source document references.
    It provides methods to clean up answers, extract document references, and make document references sequential.
    """

    def __init__(self) -> None:
        """
        Initializes the OutputParserTool with a name attribute.
        """
        self.name = "OutputParser"

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def _clean_up_answer(self, answer: str) -> str:
        """
        Cleans up the answer by replacing double spaces with single spaces.

        Args:
            answer (str): The answer string to be cleaned up.

        Returns:
            str: The cleaned-up answer string.
        """
        return answer.replace("  ", " ")

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def _get_source_docs_from_answer(self, answer: str) -> List[int]:
        """
        Extracts all document references from the answer and returns them as a list of integers.

        Args:
            answer (str): The answer string containing document references.

        Returns:
            List[int]: A list of document reference integers.
        """
        results = re.findall(r"\[doc(\d+)\]", answer)
        return [int(i) for i in results]

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def _make_doc_references_sequential(self, answer: str) -> str:
        """
        Makes document references in the answer sequential.

        Args:
            answer (str): The answer string containing document references.

        Returns:
            str: The answer string with sequential document references.
        """
        doc_matches = list(re.finditer(r"\[doc\d+\]", answer))
        updated_answer = answer
        offset = 0
        for i, match in enumerate(doc_matches):
            start, end = match.start() + offset, match.end() + offset
            updated_answer = (
                updated_answer[:start] + f"[doc{i + 1}]" + updated_answer[end:]
            )
            offset += len(f"[doc{i + 1}]") - (end - start)
        return updated_answer

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def parse(
        self,
        question: str,
        answer: str,
        source_documents: List[SourceDocument] = [],
        **kwargs: dict,
    ) -> List[dict]:
        """
        Parses the answer, extracts document references, and creates a response message object.

        Args:
            question (str): The question string.
            answer (str): The answer string to be parsed.
            source_documents (List[SourceDocument], optional): A list of source documents. Defaults to [].
            **kwargs (dict): Additional keyword arguments.

        Returns:
            List[dict]: A list of response messages.
        """
        logger.info("Method parse of output_parser_tool started")
        answer = self._clean_up_answer(answer)
        doc_ids = self._get_source_docs_from_answer(answer)
        answer = self._make_doc_references_sequential(answer)

        # create return message object
        messages = [
            {
                "role": "tool",
                "content": {"citations": [], "intent": question},
                "end_turn": False,
            }
        ]

        for i in doc_ids:
            idx = i - 1

            if idx >= len(source_documents):
                logger.warning(f"Source document {i} not provided, skipping doc")
                continue

            doc = source_documents[idx]
            logger.debug(f"doc{idx}: {doc}")

            # Then update the citation object in the response, it needs to have filepath and chunk_id to render in the UI as a file
            messages[0]["content"]["citations"].append(
                {
                    "content": doc.get_markdown_url() + "\n\n\n" + doc.content,
                    "id": doc.id,
                    "chunk_id": (
                        re.findall(r"\d+", doc.chunk_id)[-1]
                        if doc.chunk_id is not None
                        else doc.chunk
                    ),
                    "title": doc.title,
                    "filepath": doc.get_filename(include_path=True),
                    "url": doc.get_markdown_url(),
                    "metadata": {
                        "offset": doc.offset,
                        "source": doc.source,
                        "markdown_url": doc.get_markdown_url(),
                        "title": doc.title,
                        "original_url": doc.source,  # TODO: do we need this?
                        "chunk": doc.chunk,
                        "key": doc.id,
                        "filename": doc.get_filename(),
                    },
                }
            )
        if messages[0]["content"]["citations"] == []:
            logger.warning("No citations found in the answer")
            answer = re.sub(r"\[doc\d+\]", "", answer)
        messages.append({"role": "assistant", "content": answer, "end_turn": True})
        # everything in content needs to be stringified to work with Azure BYOD frontend
        messages[0]["content"] = json.dumps(messages[0]["content"])
        logger.info("Method parse of output_parser_tool ended")
        return messages
