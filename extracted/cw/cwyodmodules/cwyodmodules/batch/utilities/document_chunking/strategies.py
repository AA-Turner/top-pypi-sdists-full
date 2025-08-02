from .chunking_strategy import ChunkingStrategy
from .layout import LayoutDocumentChunking
from .page import PageDocumentChunking
from .fixed_size_overlap import FixedSizeOverlapDocumentChunking
from .paragraph import ParagraphDocumentChunking
from .json import JSONDocumentChunking

from ...utilities.helpers.env_helper import EnvHelper
from mgmt_config import logger
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT


@logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
def get_document_chunker(chunking_strategy: str):
    if chunking_strategy == ChunkingStrategy.LAYOUT.value:
        return LayoutDocumentChunking()
    elif chunking_strategy == ChunkingStrategy.PAGE.value:
        return PageDocumentChunking()
    elif chunking_strategy == ChunkingStrategy.FIXED_SIZE_OVERLAP.value:
        return FixedSizeOverlapDocumentChunking()
    elif chunking_strategy == ChunkingStrategy.PARAGRAPH.value:
        return ParagraphDocumentChunking()
    elif chunking_strategy == ChunkingStrategy.JSON.value:
        return JSONDocumentChunking()
    else:
        raise Exception(f"Unknown chunking strategy: {chunking_strategy}")