import json
from typing import List
from .document_chunking_base import DocumentChunkingBase
from langchain.text_splitter import RecursiveJsonSplitter
from .chunking_strategy import ChunkingSettings
from ..common.source_document import SourceDocument
from ...utilities.helpers.env_helper import EnvHelper

from mgmt_config import logger
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT

class JSONDocumentChunking(DocumentChunkingBase):
    def __init__(self) -> None:
        pass

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def chunk(
        self, documents: List[SourceDocument], chunking: ChunkingSettings
    ) -> List[SourceDocument]:
        full_document_content = "".join(
            list(map(lambda document: str(document.content), documents))
        )
        document_url = documents[0].source
        json_data = json.loads(full_document_content)
        splitter = RecursiveJsonSplitter(max_chunk_size=chunking.chunk_size)
        chunked_content_list = splitter.split_json(json_data)
        # Create document for each chunk
        documents = []
        chunk_offset = 0
        for idx, chunked_content in enumerate(chunked_content_list):
            documents.append(
                SourceDocument.from_metadata(
                    content=str(chunked_content),
                    document_url=document_url,
                    metadata={"offset": chunk_offset},
                    idx=idx,
                )
            )

            chunk_offset += len(chunked_content)
        return documents