from ..common.answer import Answer
from ..helpers.llm_helper import LLMHelper
from ..helpers.config.config_helper import ConfigHelper

from ...utilities.helpers.env_helper import EnvHelper
from mgmt_config import logger
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT


class PostPromptTool:
    def __init__(self) -> None:
        pass

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def validate_answer(self, answer: Answer) -> Answer:
        logger.info("Validating answer using post-answering prompt.")
        config = ConfigHelper.get_active_config_or_default()
        llm_helper = LLMHelper()

        sources = "\n".join(
            [
                f"[doc{i+1}]: {source.content}"
                for i, source in enumerate(answer.source_documents)
            ]
        )
        message = config.prompts.post_answering_prompt.format(
            question=answer.question,
            answer=answer.answer,
            sources=sources,
        )
        logger.debug(f"Post-answering prompt message: {message}")
        response = llm_helper.get_chat_completion(
            [
                {
                    "role": "user",
                    "content": message,
                }
            ]
        )
        result = response.choices[0].message.content
        logger.debug(f"LLM response content: {result}")
        was_message_filtered = result.lower() not in ["true", "yes"]
        logger.debug(f"Was message filtered: {was_message_filtered}")
        # Return filtered answer or just the original one
        if was_message_filtered:
            logger.info("Message was filtered; returning filtered answer.")
            return Answer(
                question=answer.question,
                answer=config.messages.post_answering_filter,
                source_documents=[],
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
            )
        else:
            logger.info("Message was not filtered; returning original answer.")
            return Answer(
                question=answer.question,
                answer=answer.answer,
                source_documents=answer.source_documents,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
            )
