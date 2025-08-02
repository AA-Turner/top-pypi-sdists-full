from semantic_kernel.functions import kernel_function
from semantic_kernel.functions.kernel_arguments import KernelArguments
from ...utilities.helpers.env_helper import EnvHelper

from ..common.answer import Answer
from ..tools.post_prompt_tool import PostPromptTool
from mgmt_config import logger, identity
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT

class PostAnsweringPlugin:
    """
    A plugin class for post-answering operations, specifically designed to validate answers.

    Methods
    -------
    validate_answer(arguments: KernelArguments) -> Answer
        Executes a post-answering prompt to validate the provided answer.

    Validates the given answer using a post-answering prompt.

    Parameters
    ----------
    arguments : KernelArguments
        A dictionary containing the arguments required for validation. 
        It must include the key "answer" which holds the answer to be validated.

    Returns
    -------
    Answer
        The validated answer after running the post-answering prompt.
    """
    @kernel_function(description="Run post answering prompt to validate the answer.")
    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def validate_answer(self, arguments: KernelArguments) -> Answer:
        return PostPromptTool().validate_answer(arguments["answer"])
