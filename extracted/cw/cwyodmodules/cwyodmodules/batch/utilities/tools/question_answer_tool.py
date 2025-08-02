import json
import warnings
from ..common.answer import Answer
from ..common.source_document import SourceDocument
from ..helpers.config.config_helper import ConfigHelper
from ..helpers.env_helper import EnvHelper
from ..helpers.llm_helper import LLMHelper
from ..search.search import Search
from .answering_tool_base import AnsweringToolBase
from openai.types.chat import ChatCompletion
from typing import Union

from mgmt_config import logger, storage_accounts
storage_account = storage_accounts.get("main") if storage_accounts else None

env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT


class QuestionAnswerTool(AnsweringToolBase):
    """
    The QuestionAnswerTool class is responsible for handling the process of answering questions
    using a combination of search and language model capabilities. It extends the AnsweringToolBase
    class and provides methods for generating messages, cleaning chat history, and formatting answers.
    """

    def __init__(self) -> None:
        """
        Initialize the QuestionAnswerTool with necessary helpers and configurations.
        """
        logger.info("Initializing QuestionAnswerTool...")
        self.name = "QuestionAnswer"
        self.env_helper = EnvHelper()
        self.llm_helper = LLMHelper()
        self.search_handler = Search.get_search_handler(env_helper=self.env_helper)
        self.verbose = True

        self.config = ConfigHelper.get_active_config_or_default()
        logger.info("QuestionAnswerTool initialized with configuration.")

    def __str__(self):
        return self.answer

    @staticmethod
    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def json_remove_whitespace(obj: str) -> str:
        """
        Remove whitespace from a JSON string.

        Args:
            obj (str): The JSON string from which to remove whitespace.

        Returns:
            str: The JSON string without whitespace.
        """
        try:
            return json.dumps(json.loads(obj), separators=(",", ":"))
        except json.JSONDecodeError:
            logger.exception("Failed to parse JSON in json_remove_whitespace.")
            return obj

    @staticmethod
    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def clean_chat_history(chat_history: list[dict]) -> list[dict]:
        """
        Clean the chat history by retaining only the content and role of each message.

        Args:
            chat_history (list[dict]): The chat history to clean.

        Returns:
            list[dict]: The cleaned chat history.
        """
        logger.info("Cleaning chat history...")
        cleaned_history = [
            {
                "content": message["content"],
                "role": message["role"],
            }
            for message in chat_history
        ]
        logger.info(
            f"Chat history cleaned. Returning {len(cleaned_history)} messages."
        )
        return cleaned_history

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def generate_messages(self, question: str, sources: list[SourceDocument]):
        """
        Generate messages for the language model based on the question and source documents.

        Args:
            question (str): The question to be answered.
            sources (list[SourceDocument]): The source documents to use for generating the answer.

        Returns:
            list[dict]: The generated messages.
        """
        sources_text = "\n\n".join(
            [f"[doc{i+1}]: {source.content}" for i, source in enumerate(sources)]
        )

        logger.info(
            f"Generating messages for question: {question} with {len(sources)} sources."
        )
        messages = [
            {
                "content": self.config.prompts.answering_user_prompt.format(
                    question=question, sources=sources_text
                ),
                "role": "user",
            },
        ]
        logger.debug(f"Generated messages: {messages}")
        return messages

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def generate_on_your_data_messages(
        self,
        question: str,
        chat_history: list[dict],
        sources: list[SourceDocument],
        image_urls: list[str] = [],
    ) -> list[dict]:
        """
        Generate messages for the language model using the "On Your Data" format.

        Args:
            question (str): The question to be answered.
            chat_history (list[dict]): The chat history.
            sources (list[SourceDocument]): The source documents to use for generating the answer.
            image_urls (list[str], optional): The list of image URLs. Defaults to [].

        Returns:
            list[dict]: The generated messages.
        """
        logger.info(f"Generating On Your Data messages for question: {question}")
        examples = []

        few_shot_example = {
            "sources": self.config.example.documents.strip(),
            "question": self.config.example.user_question.strip(),
            "answer": self.config.example.answer.strip(),
        }

        if few_shot_example["sources"]:
            few_shot_example["sources"] = QuestionAnswerTool.json_remove_whitespace(
                few_shot_example["sources"]
            )

        if any(few_shot_example.values()):
            if all((few_shot_example.values())):
                examples.append(
                    {
                        "content": self.config.prompts.answering_user_prompt.format(
                            sources=few_shot_example["sources"],
                            question=few_shot_example["question"],
                        ),
                        "name": "example_user",
                        "role": "system",
                    }
                )
                examples.append(
                    {
                        "content": few_shot_example["answer"],
                        "name": "example_assistant",
                        "role": "system",
                    }
                )
            else:
                warnings.warn(
                    "Not all example fields are set in the config. Skipping few-shot example."
                )

        documents = json.dumps(
            {
                "retrieved_documents": [
                    {f"[doc{i+1}]": {"content": source.content}}
                    for i, source in enumerate(sources)
                ],
            },
            separators=(",", ":"),
        )

        messages = [
            {
                "role": "system",
                "content": self.config.prompts.answering_system_prompt,
            },
            *examples,
            {
                "role": "system",
                "content": self.env_helper.AZURE_OPENAI_SYSTEM_MESSAGE,
            },
            *QuestionAnswerTool.clean_chat_history(chat_history),
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": self.config.prompts.answering_user_prompt.format(
                            sources=documents,
                            question=question,
                        ),
                    },
                    *(
                        [
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url},
                            }
                            for image_url in image_urls
                        ]
                    ),
                ],
            },
        ]
        logger.debug(f"Generated On Your Data messages: {messages}")
        return messages

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def answer_question(self, question: str, chat_history: list[dict], **kwargs):
        """
        Answer the given question using the chat history and additional parameters.

        Args:
            question (str): The question to be answered.
            chat_history (list[dict]): The chat history.
            **kwargs: Additional parameters.

        Returns:
            Answer: The formatted answer.
        """
        logger.info("Answering question")
        source_documents = Search.get_source_documents(
            self.search_handler, question
        )

        if self.env_helper.USE_ADVANCED_IMAGE_PROCESSING:
            image_urls = self.create_image_url_list(source_documents)
            logger.info(
                f"Generated {len(image_urls)} image URLs for advanced image processing."
            )
        else:
            image_urls = []

        model = self.env_helper.AZURE_OPENAI_VISION_MODEL if image_urls else None

        if self.config.prompts.use_on_your_data_format:
            messages = self.generate_on_your_data_messages(
                question, chat_history, source_documents, image_urls
            )
        else:
            warnings.warn(
                "Azure OpenAI On Your Data prompt format is recommended and should be enabled in the Admin app.",
            )
            messages = self.generate_messages(question, source_documents)

        llm_helper = LLMHelper()

        response = llm_helper.get_chat_completion(
            messages, model=model, temperature=0
        )
        clean_answer = self.format_answer_from_response(
            response, question, source_documents
        )
        logger.info("Cleaned answer generated successfully.")
        logger.debug(f"Answer: {clean_answer.answer}")
        return clean_answer

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=log_result)
    def create_image_url_list(self, source_documents):
        """
        Create a list of image URLs from the source documents using storage_account from mgmt_config.

        Args:
            source_documents (list[SourceDocument]): The source documents.

        Returns:
            list[str]: The list of image URLs.
        """
        image_types = self.config.get_advanced_image_processing_image_types()

        # Use storage_account from mgmt_config instead of direct AzureBlobStorageClient instantiation
        if not storage_account:
            logger.warning("Storage account not configured. Image URLs cannot be generated.")
            return []
            
        # Generate container SAS using storage_account from mgmt_config
        try:
            container_sas = storage_account.get_container_sas(
                container_name=self.env_helper.AZURE_BLOB_CONTAINER_NAME,
                permission="r"
            )
        except Exception as e:
            logger.error(f"Failed to generate container SAS: {e}")
            return []

        image_urls = [
            doc.source.replace("_SAS_TOKEN_PLACEHOLDER_", f"?{container_sas}")
            for doc in source_documents
            if doc.title is not None and doc.title.split(".")[-1] in image_types
        ][: self.env_helper.ADVANCED_IMAGE_PROCESSING_MAX_IMAGES]

        logger.info(
            f"Generated {len(image_urls)} image URLs for {len(source_documents)} source documents."
        )
        return image_urls

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def format_answer_from_response(
        self,
        response: ChatCompletion,
        question: str,
        source_documents: list[SourceDocument],
    ):
        """
        Format the answer from the language model response.

        Args:
            response (ChatCompletion): The response from the language model.
            question (str): The question that was asked.
            source_documents (list[SourceDocument]): The source documents used for generating the answer.

        Returns:
            Answer: The formatted answer.
        """
        answer = response.choices[0].message.content
        logger.debug(f"Answer format_answer_from_response: {answer}")

        # Append document citations to the answer
        citations = "".join([
            f"[doc{i+1}]"
            for i in range(len(source_documents))
            if f"[doc{i+1}]" not in answer
        ])
        answer_with_citations = f"{answer} {citations}"
        # Generate Answer Object
        clean_answer = Answer(
            question=question,
            answer=answer_with_citations,  # Use the answer with citations
            source_documents=source_documents,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
        )

        return clean_answer
