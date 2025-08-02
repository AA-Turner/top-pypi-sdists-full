from typing import List
from .document_loading_base import DocumentLoadingBase
from ..helpers.azure_form_recognizer_helper import AzureFormRecognizerClient
from ..common.source_document import SourceDocument
from mgmt_config import logger
from ...utilities.helpers.env_helper import EnvHelper

env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT

class LayoutDocumentLoading(DocumentLoadingBase):
    def __init__(self) -> None:
        super().__init__()

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def load(self, document_url: str) -> List[SourceDocument]:
        azure_form_recognizer_client = AzureFormRecognizerClient()
        pages_content = azure_form_recognizer_client.begin_analyze_document_from_url(
            document_url, use_layout=True
        )
        documents = [
            SourceDocument(
                content=page["page_text"],
                source=document_url,
                offset=page["offset"],
                page_number=page["page_number"],
            )
            for page in pages_content
        ]
        return documents
