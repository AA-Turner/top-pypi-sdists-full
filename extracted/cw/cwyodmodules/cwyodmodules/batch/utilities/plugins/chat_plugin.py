from typing import Annotated

from semantic_kernel.functions import kernel_function
from ...utilities.helpers.env_helper import EnvHelper
from ..common.answer import Answer
from ..tools.question_answer_tool import QuestionAnswerTool
from ..tools.text_processing_tool import TextProcessingTool
from mgmt_config import logger, identity
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT

class ChatPlugin:
    """
    ChatPlugin is a class designed to handle user queries and perform various text processing operations.
    It utilizes tools to answer questions based on chat history and to apply transformations on text.
    
    Attributes:
        question (str): The user's question.
        chat_history (list[dict]): The history of the chat in the form of a list of dictionaries.
    """

    def __init__(self, question: str, chat_history: list[dict]) -> None:
        """
        Initializes the ChatPlugin with a question and chat history.

        Args:
            question (str): The user's question.
            chat_history (list[dict]): The history of the chat in the form of a list of dictionaries.
        """
        self.question = question
        self.chat_history = chat_history

    @kernel_function(
        description="Provide answers to any fact question coming from users."
    )
    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def search_documents(
        self,
        question: Annotated[
            str, "A standalone question, converted from the chat history"
        ],
    ) -> Answer:
        """
        Searches documents to provide answers to factual questions from users.

        Args:
            question (Annotated[str]): A standalone question, converted from the chat history.

        Returns:
            Answer: The answer to the question.
        """
        answer_obj = QuestionAnswerTool().answer_question(
            question=question, chat_history=self.chat_history
        )
        return answer_obj

    @kernel_function(
        description="Useful when you want to apply a transformation on the text, like translate, summarize, rephrase and so on."
    )
    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def text_processing(
        self,
        text: Annotated[str, "The text to be processed"],
        operation: Annotated[
            str,
            "The operation to be performed on the text. Like Translate to German, Spanish, Paraphrase, etc. If a language is specified, return that as part of the operation. Preserve the operation name in the user language.",
        ],
    ) -> Answer:
        """
        Applies a specified transformation on the given text.

        Args:
            text (Annotated[str]): The text to be processed.
            operation (Annotated[str]): The operation to be performed on the text. Examples include translating to a different language, summarizing, or paraphrasing.

        Returns:
            Answer: The result of the text processing operation.
        """
        return TextProcessingTool().answer_question(
            question=self.question,
            chat_history=self.chat_history,
            text=text,
            operation=operation,
        )