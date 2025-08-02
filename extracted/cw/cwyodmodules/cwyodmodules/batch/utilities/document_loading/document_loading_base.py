# Create an abstract class for document loading
from typing import List
from abc import ABC, abstractmethod
from ..common.source_document import SourceDocument
from mgmt_config import logger
from ...utilities.helpers.env_helper import EnvHelper

env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT

class DocumentLoadingBase(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def load(self, document_url: str) -> List[SourceDocument]:
        pass
