from typing import List
from .document_loading_base import DocumentLoadingBase
from ..helpers.azure_form_recognizer_helper import AzureFormRecognizerClient
from ..common.source_document import SourceDocument

from ...utilities.helpers.env_helper import EnvHelper
from mgmt_config import logger
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT


class ReadDocumentLoading(DocumentLoadingBase):
    def __init__(self) -> None:
        super().__init__()

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=False)
    def load(self, document_url: str) -> List[SourceDocument]:
        logger.info(f"Loading document from URL: {document_url}")
        try:
            azure_form_recognizer_client = AzureFormRecognizerClient()
            pages_content = (
                azure_form_recognizer_client.begin_analyze_document_from_url(
                    document_url, use_layout=False
                )
            )
            documents = [
                SourceDocument(
                    content=page["page_text"],
                    source=document_url,
                    page_number=page["page_number"],
                    offset=page["offset"],
                )
                for page in pages_content
            ]
            logger.info(
                f"Successfully loaded {len(documents)} pages from {document_url}"
            )
            return documents
        except Exception as e:
            logger.error(
                f"Error loading document from {document_url}: {e}", exc_info=True
            )
            raise
