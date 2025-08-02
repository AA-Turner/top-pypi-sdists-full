from typing import List

from ..common.source_document import SourceDocument
from ..document_loading import LoadingSettings
from ..document_loading.strategies import get_document_loader
from ...utilities.helpers.env_helper import EnvHelper

from mgmt_config import logger, identity
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT



class DocumentLoading:
    def __init__(self) -> None:
        pass

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def load(self, document_url: str, loading: LoadingSettings) -> List[SourceDocument]:
        loader = get_document_loader(loading.loading_strategy.value)
        if loader is None:
            raise Exception(
                f"Unknown loader strategy: {loading.loading_strategy.value}"
            )
        return loader.load(document_url)
