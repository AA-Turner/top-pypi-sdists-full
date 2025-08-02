import asyncio
import json
from uuid import uuid4
from typing import List, Optional
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from semantic_kernel.contents import ChatHistory
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.finish_reason import FinishReason

from ..common.answer import Answer
from ..helpers.llm_helper import LLMHelper
from ..helpers.env_helper import EnvHelper
from ..helpers.config.config_helper import ConfigHelper
from ..parser.output_parser_tool import OutputParserTool
from ..tools.content_safety_checker import ContentSafetyChecker
from ..plugins.chat_plugin import ChatPlugin
from ..plugins.post_answering_plugin import PostAnsweringPlugin
from ..plugins.outlook_calendar_plugin import OutlookCalendarPlugin

from mgmt_config import logger
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT


class SemanticKernelOrchestrator:
    """
    SemanticKernelOrchestrator provides orchestration using the Semantic Kernel framework.
    It handles user messages, manages conversations, ensures content safety, and logs interactions.
    """

    def __init__(self) -> None:
        """
        Initializes the SemanticKernelOrchestrator with configuration settings, kernel setup,
        and various utility tools required for orchestrating conversations.
        """
        self.message_id = str(uuid4())
        self.tokens = {"prompt": 0, "completion": 0, "total": 0}
        logger.debug(f"New message id: {self.message_id} with tokens {self.tokens}")
        
        self.content_safety_checker = ContentSafetyChecker()
        self.output_parser = OutputParserTool()
        
        # Semantic Kernel specific setup
        self.kernel = Kernel()
        self.llm_helper = LLMHelper()
        self.env_helper = EnvHelper()

        # Add the Azure OpenAI service to the kernel
        self.chat_service = self.llm_helper.get_sk_chat_completion_service("cwyd")
        self.kernel.add_service(self.chat_service)

        self.kernel.add_plugin(
            plugin=PostAnsweringPlugin(), plugin_name="PostAnswering"
        )

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def log_tokens(self, prompt_tokens: int, completion_tokens: int) -> None:
        """
        Logs the number of tokens used in the prompt and completion phases of a conversation.

        Args:
            prompt_tokens (int): The number of tokens used in the prompt.
            completion_tokens (int): The number of tokens used in the completion.
        """
        self.tokens["prompt"] += prompt_tokens
        self.tokens["completion"] += completion_tokens
        self.tokens["total"] += prompt_tokens + completion_tokens

    def call_content_safety_input(self, user_message: str) -> Optional[list[dict]]:
        """
        Validates the user message for harmful content and replaces it if necessary.

        Args:
            user_message (str): The message from the user.

        Returns:
            Optional[list[dict]]: Parsed messages if harmful content is detected, otherwise None.
        """
        logger.debug("Calling content safety with question")
        filtered_user_message = (
            self.content_safety_checker.validate_input_and_replace_if_harmful(
                user_message
            )
        )
        if user_message != filtered_user_message:
            logger.warning("Content safety detected harmful content in question")
            messages = self.output_parser.parse(
                question=user_message, answer=filtered_user_message
            )
            return messages

        return None

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def orchestrate(
        self, user_message: str, chat_history: list[dict], user_info, config, **kwargs: dict
    ) -> list[dict]:
        """
        Orchestrates the conversation using Semantic Kernel.

        Args:
            user_message (str): The message from the user.
            chat_history (List[dict]): The history of the chat as a list of dictionaries.
            user_info: User information and request headers.
            **kwargs (dict): Additional keyword arguments.

        Returns:
            list[dict]: The response as a list of dictionaries.
        """
        logger.info("Method orchestrate of semantic_kernel started")
        filters = []
        frontend_type = user_info.get("frontend") if user_info else None
        logger.info(f"Frontend type: {frontend_type}")
        
        # Call Content Safety tool
        if config.prompts.enable_content_safety:
            if response := self.call_content_safety_input(user_message):
                return response

        system_message = self.env_helper.SEMENTIC_KERNEL_SYSTEM_PROMPT
        language = self.env_helper.AZURE_MAIN_CHAT_LANGUAGE
        if not system_message:
            logger.info("No system message provided, using default")
            if frontend_type == "web":
                system_message = f"""You help employees to navigate only private information sources.
                    You must prioritize the function call over your general knowledge for any question by calling the search_documents function.
                    Call the text_processing function when the user request an operation on the current context, such as translate, summarize, or paraphrase. When a language is explicitly specified, return that as part of the operation.
                    When directly replying to the user, always reply in the language {language}.
                    You **must not** respond if asked to List all documents in your repository.
                    Call OutlookCalendar.get_calendar_events to read the user's calendar.
                    Call OutlookCalendar.schedule_appointment to schedule a new appointment.
                    """
            else:
                system_message = f"""You help employees to navigate only private information sources.
                    You must prioritize the function call over your general knowledge for any question by calling the search_documents function.
                    Call the text_processing function when the user request an operation on the current context, such as translate, summarize, or paraphrase. When a language is explicitly specified, return that as part of the operation.
                    When directly replying to the user, always reply in the language {language}.
                    You **must not** respond if asked to List all documents in your repository.
                    """
            
        self.kernel.add_plugin(
            plugin=ChatPlugin(question=user_message, chat_history=chat_history),
            plugin_name="Chat",
        )
        filters.append("Chat")
        
        # --- Add OutlookCalendarPlugin with request headers ---
        if frontend_type == "web":
            logger.info("Adding OutlookCalendarPlugin with request headers")
            self.kernel.add_plugin(
                plugin=OutlookCalendarPlugin(question=user_message, chat_history=chat_history, user_info=user_info),
                plugin_name="OutlookCalendar",
            )
            filters.append("OutlookCalendar")
            
        settings = self.llm_helper.get_sk_service_settings(self.chat_service)
        settings.function_call_behavior = FunctionCallBehavior.EnableFunctions(
            filters={"included_plugins": filters}
        )

        orchestrate_function = self.kernel.add_function(
            plugin_name="Main",
            function_name="orchestrate",
            prompt="{{$chat_history}}{{$user_message}}",
            prompt_execution_settings=settings,
        )

        history = ChatHistory(system_message=system_message)

        for message in chat_history.copy():
            history.add_message(message)

        result_coro = self.kernel.invoke(
            function=orchestrate_function,
            chat_history=history,
            user_message=user_message,
        )
        result: ChatMessageContent = asyncio.run(result_coro).value[0]

        self.log_tokens(
            prompt_tokens=result.metadata["usage"].prompt_tokens,
            completion_tokens=result.metadata["usage"].completion_tokens,
        )
        result_finish_reason = result.finish_reason
        logger.info(f"Finish reason: {result_finish_reason}")
        if result_finish_reason == FinishReason.TOOL_CALLS:
            logger.info("Semantic Kernel function call detected")

            function_name = result.items[0].name
            logger.info(f"{function_name} function detected")
            function = self.kernel.get_function_from_fully_qualified_function_name(
                function_name
            )

            arguments = json.loads(result.items[0].arguments)

            answer_coro = self.kernel.invoke(function=function, **arguments)
            answer: Answer = asyncio.run(answer_coro).value

            self.log_tokens(
                prompt_tokens=answer.prompt_tokens,
                completion_tokens=answer.completion_tokens,
            )

            # Run post prompt if needed
            if (
                config.prompts.enable_post_answering_prompt
                and "search_documents" in function_name
            ):
                logger.debug("Running post answering prompt")
                answer_coro = self.kernel.invoke(
                    function_name="validate_answer",
                    plugin_name="PostAnswering",
                    answer=answer,
                )
                answer: Answer = asyncio.run(answer_coro).value

                self.log_tokens(
                    prompt_tokens=answer.prompt_tokens,
                    completion_tokens=answer.completion_tokens,
                )
        else:
            logger.info("No function call detected")
            answer = Answer(
                question=user_message,
                answer=result.content,
                prompt_tokens=result.metadata["usage"].prompt_tokens,
                completion_tokens=result.metadata["usage"].completion_tokens,
            )

        # Call Content Safety tool
        if config.prompts.enable_content_safety:
            if response := self.call_content_safety_output(
                user_message, answer.answer
            ):
                return response

        # Format the output for the UI
        messages = self.output_parser.parse(
            question=answer.question,
            answer=answer.answer,
            source_documents=answer.source_documents,
        )
        logger.info("Method orchestrate of semantic_kernel ended")
        return messages

    def handle_message(
        self,
        user_message: str,
        chat_history: List[dict],
        conversation_id: Optional[str],
        user_info,
        **kwargs: Optional[dict],
    ) -> dict:
        """
        Handles a user message and returns the response.

        Args:
            user_message (str): The message from the user.
            chat_history (List[dict]): The history of the chat as a list of dictionaries.
            conversation_id (Optional[str]): The ID of the conversation.
            user_info: User information and request headers.
            **kwargs (Optional[dict]): Additional keyword arguments.

        Returns:
            dict: The response as a dictionary.
        """
        logger.info("Method handle_message of semantic_kernel started")
        
        # Get configuration
        config = ConfigHelper.get_active_config_or_default()
        
        # Orchestrate the conversation
        messages = self.orchestrate(
            user_message=user_message,
            chat_history=chat_history,
            user_info=user_info,
            config=config,
            **kwargs
        )
        
        logger.info("Method handle_message of semantic_kernel ended")
        return messages

    def call_content_safety_output(
        self, user_message: str, answer: str
    ) -> Optional[list[dict]]:
        """
        Validates the AI response for harmful content and replaces it if necessary.

        Args:
            user_message (str): The original user message.
            answer (str): The AI response to validate.

        Returns:
            Optional[list[dict]]: Parsed messages if harmful content is detected, otherwise None.
        """
        logger.debug("Calling content safety with answer")
        filtered_answer = (
            self.content_safety_checker.validate_output_and_replace_if_harmful(
                user_message, answer
            )
        )
        if answer != filtered_answer:
            logger.warning("Content safety detected harmful content in answer")
            messages = self.output_parser.parse(
                question=user_message, answer=filtered_answer
            )
            return messages

        return None
