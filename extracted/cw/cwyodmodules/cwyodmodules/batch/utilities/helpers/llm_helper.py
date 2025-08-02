from openai import AzureOpenAI
from typing import List, Union, cast
# Removed LangChain dependencies - using direct OpenAI SDK instead
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)
from ...utilities.helpers.env_helper import EnvHelper

from mgmt_config import logger, identity
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT


class LLMHelper:
    def __init__(self):
        logger.info("Initializing LLMHelper")
        self.env_helper: EnvHelper = EnvHelper()

        self.auth_type_keys = self.env_helper.AZURE_AUTH_TYPE == "keys"
        self.token_provider = self.env_helper.AZURE_TOKEN_PROVIDER

        if self.auth_type_keys:
            self.openai_client = AzureOpenAI(
                azure_endpoint=self.env_helper.AZURE_OPENAI_ENDPOINT,
                api_version=self.env_helper.AZURE_OPENAI_API_VERSION,
                api_key=self.env_helper.OPENAI_API_KEY,
            )
        else:
            self.openai_client = AzureOpenAI(
                azure_endpoint=self.env_helper.AZURE_OPENAI_ENDPOINT,
                api_version=self.env_helper.AZURE_OPENAI_API_VERSION,
                azure_ad_token_provider=self.token_provider,
            )

        self.llm_model = self.env_helper.AZURE_OPENAI_MODEL
        self.llm_max_tokens = (
            int(self.env_helper.AZURE_OPENAI_MAX_TOKENS)
            if self.env_helper.AZURE_OPENAI_MAX_TOKENS != ""
            else None
        )
        self.embedding_model = self.env_helper.AZURE_OPENAI_EMBEDDING_MODEL

        logger.info("Initializing LLMHelper completed")

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=False)
    def get_llm(self):
        # Return the OpenAI client directly instead of LangChain wrapper
        return self.openai_client

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=False)
    def get_streaming_llm(self):
        # Return the OpenAI client directly - streaming is handled via stream=True parameter
        return self.openai_client

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=False)
    def get_embedding_model(self):
        # Return a simple embedding model wrapper that uses the OpenAI client directly
        class EmbeddingModel:
            def __init__(self, openai_client, embedding_model):
                self.openai_client = openai_client
                self.embedding_model = embedding_model
            
            def embed_query(self, text: str) -> List[float]:
                return (
                    self.openai_client.embeddings.create(
                        input=[text], model=self.embedding_model
                    )
                    .data[0]
                    .embedding
                )
        
        return EmbeddingModel(self.openai_client, self.embedding_model)

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def generate_embeddings(self, input: Union[str, list[int]]) -> List[float]:
        return (
            self.openai_client.embeddings.create(
                input=[input], model=self.embedding_model
            )
            .data[0]
            .embedding
        )

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def get_chat_completion_with_functions(
        self, messages: list[dict], functions: list[dict], function_call: str = "auto"
    ):
        return self.openai_client.chat.completions.create(
            model=self.llm_model,
            messages=messages,
            functions=functions,
            function_call=function_call,
        )

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def get_chat_completion(
        self, messages: list[dict], model: str | None = None, **kwargs
    ):
        return self.openai_client.chat.completions.create(
            model=model or self.llm_model,
            messages=messages,
            max_tokens=self.llm_max_tokens,
            **kwargs,
        )

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def get_sk_chat_completion_service(self, service_id: str):
        if self.auth_type_keys:
            return AzureChatCompletion(
                service_id=service_id,
                deployment_name=self.llm_model,
                endpoint=self.env_helper.AZURE_OPENAI_ENDPOINT,
                api_version=self.env_helper.AZURE_OPENAI_API_VERSION,
                api_key=self.env_helper.OPENAI_API_KEY,
            )
        else:
            logger.warning("service_id: %s", service_id)
            logger.warning("self.llm_model: %s", self.llm_model)
            logger.warning(
                "self.env_helper.AZURE_OPENAI_ENDPOINT: %s",
                self.env_helper.AZURE_OPENAI_ENDPOINT,
            )
            logger.warning(
                "self.env_helper.AZURE_OPENAI_API_VERSION: %s",
                self.env_helper.AZURE_OPENAI_API_VERSION,
            )
            logger.warning("self.token_provider: %s", self.token_provider)
            return AzureChatCompletion(
                service_id=service_id,
                deployment_name=self.llm_model,
                endpoint=self.env_helper.AZURE_OPENAI_ENDPOINT,
                api_version=self.env_helper.AZURE_OPENAI_API_VERSION,
                ad_token_provider=self.token_provider,
            )

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def get_sk_service_settings(self, service: AzureChatCompletion):
        return cast(
            AzureChatPromptExecutionSettings,
            service.instantiate_prompt_execution_settings(
                service_id=service.service_id,
                temperature=0,
                max_tokens=self.llm_max_tokens,
            ),
        )
