from typing import List

from ..common.source_document import SourceDocument
from ..document_chunking.chunking_strategy import ChunkingSettings, ChunkingStrategy
from ..document_chunking.strategies import get_document_chunker
from ...utilities.helpers.env_helper import EnvHelper
from mgmt_config import logger, identity
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT


__all__ = ["ChunkingStrategy"]


class DocumentChunking:
    def __init__(self) -> None:
        pass

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def chunk(
        self, documents: List[SourceDocument], chunking: ChunkingSettings
    ) -> List[SourceDocument]:
        chunker = get_document_chunker(chunking.chunking_strategy.value)
        if chunker is None:
            raise Exception(
                f"Unknown chunking strategy: {chunking.chunking_strategy.value}"
            )
        return chunker.chunk(documents, chunking)
