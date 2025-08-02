from typing import List
from ..orchestrator.semantic_kernel_orchestrator import SemanticKernelOrchestrator
from ...utilities.helpers.env_helper import EnvHelper
from mgmt_config import logger, identity
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT

__all__ = ["Orchestrator"]


class Orchestrator:
    def __init__(self) -> None:
        self.orchestrator = SemanticKernelOrchestrator()

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def handle_message(
        self,
        user_message: str,
        chat_history: List[dict],
        conversation_id: str,
        user_info,
        **kwargs: dict,
    ) -> dict:
        return self.orchestrator.handle_message(
            user_message, chat_history, conversation_id, user_info, **kwargs
        )
