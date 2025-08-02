from enum import Enum
from .layout import LayoutDocumentLoading
from .read import ReadDocumentLoading
from .web import WebDocumentLoading
from .word_document import WordDocumentLoading
from ...utilities.helpers.env_helper import EnvHelper

from mgmt_config import logger
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT


class LoadingStrategy(Enum):
    LAYOUT = "layout"
    READ = "read"
    WEB = "web"
    DOCX = "docx"


@logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
def get_document_loader(loader_strategy: str):
    if loader_strategy == LoadingStrategy.LAYOUT.value:
        return LayoutDocumentLoading()
    elif loader_strategy == LoadingStrategy.READ.value:
        return ReadDocumentLoading()
    elif loader_strategy == LoadingStrategy.WEB.value:
        return WebDocumentLoading()
    elif loader_strategy == LoadingStrategy.DOCX.value:
        return WordDocumentLoading()
    else:
        raise Exception(f"Unknown loader strategy: {loader_strategy}")
