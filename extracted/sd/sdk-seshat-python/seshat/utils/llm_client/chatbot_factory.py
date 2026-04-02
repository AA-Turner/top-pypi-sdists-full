from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict

from langchain_core.language_models.chat_models import BaseChatModel

from seshat.utils.llm_client.clients.aws import BedrockModels, create_bedrock_client
from seshat.utils.llm_client.clients.google import GeminiModels, create_google_client
from seshat.utils.llm_client.clients.openai import OpenAIModels, create_openai_client
from seshat.utils.llm_client.clients.proxy import create_proxy_client
from seshat.utils.llm_client.llm_provider import LLMProvider


@dataclass
class LLMConfig:
    model_name: str
    provider: str


class AvailableLLMs(Enum):
    GPT_4O = LLMConfig(model_name=OpenAIModels.GPT_4O, provider=LLMProvider.OPENAI)
    GPT_4O_MINI = LLMConfig(
        model_name=OpenAIModels.GPT_4O_MINI, provider=LLMProvider.OPENAI
    )
    GPT_4 = LLMConfig(model_name=OpenAIModels.GPT_4, provider=LLMProvider.OPENAI)
    GPT_3_5_TURBO = LLMConfig(
        model_name=OpenAIModels.GPT_3_5_TURBO, provider=LLMProvider.OPENAI
    )
    GPT_4_1 = LLMConfig(model_name=OpenAIModels.GPT_4_1, provider=LLMProvider.OPENAI)
    GPT_4_1_MINI = LLMConfig(
        model_name=OpenAIModels.GPT_4_1_MINI, provider=LLMProvider.OPENAI
    )
    GPT_4_1_NANO = LLMConfig(
        model_name=OpenAIModels.GPT_4_1_NANO, provider=LLMProvider.OPENAI
    )
    GPT_5_MINI = LLMConfig(
        model_name=OpenAIModels.GPT_5_MINI, provider=LLMProvider.OPENAI
    )
    GPT_5_NANO = LLMConfig(
        model_name=OpenAIModels.GPT_5_NANO, provider=LLMProvider.OPENAI
    )

    BEDROCK_MISTRAL_SMALL = LLMConfig(
        model_name=BedrockModels.MISTRAL_SMALL, provider=LLMProvider.BEDROCK
    )
    BEDROCK_MISTRAL_LARGE = LLMConfig(
        model_name=BedrockModels.MISTRAL_LARGE, provider=LLMProvider.BEDROCK
    )

    BEDROCK_LLAMA_4_Maverick_17B_Instruct = LLMConfig(
        model_name=BedrockModels.LLAMA_4_Maverick_17B_Instruct,
        provider=LLMProvider.BEDROCK,
    )
    BEDROCK_LLAMA_4_Scout_17B_Instruct = LLMConfig(
        model_name=BedrockModels.LLAMA_4_Scout_17B_Instruct,
        provider=LLMProvider.BEDROCK,
    )
    BEDROCK_LLAMA3_3_70B_Instruct = LLMConfig(
        model_name=BedrockModels.LLAMA3_3_70B_Instruct, provider=LLMProvider.BEDROCK
    )
    BEDROCK_LLAMA_3_2_1B_Instruct = LLMConfig(
        model_name=BedrockModels.LLAMA_3_2_1B_Instruct, provider=LLMProvider.BEDROCK
    )
    BEDROCK_LLAMA_3_2_3B_Instruct = LLMConfig(
        model_name=BedrockModels.LLAMA_3_2_3B_Instruct, provider=LLMProvider.BEDROCK
    )
    BEDROCK_LLAMA_3_1_8B_Instruct = LLMConfig(
        model_name=BedrockModels.LLAMA_3_1_8B_Instruct, provider=LLMProvider.BEDROCK
    )

    BEDROCK_AMAZON_Nova_Premier = LLMConfig(
        model_name=BedrockModels.AMAZON_Nova_Premier, provider=LLMProvider.BEDROCK
    )
    BEDROCK_AMAZON_Nova_Pro = LLMConfig(
        model_name=BedrockModels.AMAZON_Nova_Pro, provider=LLMProvider.BEDROCK
    )
    BEDROCK_AMAZON_Nova_Lite = LLMConfig(
        model_name=BedrockModels.AMAZON_Nova_Lite, provider=LLMProvider.BEDROCK
    )
    BEDROCK_AMAZON_Nova_Micro = LLMConfig(
        model_name=BedrockModels.AMAZON_Nova_Micro, provider=LLMProvider.BEDROCK
    )

    BEDROCK_CLAUDE_3_5_Haiku = LLMConfig(
        model_name=BedrockModels.CLAUDE_3_5_Haiku, provider=LLMProvider.BEDROCK
    )
    BEDROCK_CLAUDE_3_Haiku = LLMConfig(
        model_name=BedrockModels.CLAUDE_3_Haiku, provider=LLMProvider.BEDROCK
    )
    # Google models
    GEMINI_2_5_PRO = LLMConfig(
        model_name=GeminiModels.GEMINI_2_5_PRO, provider=LLMProvider.GOOGLE
    )
    GEMINI_2_5_FLASH = LLMConfig(
        model_name=GeminiModels.GEMINI_2_5_FLASH, provider=LLMProvider.GOOGLE
    )
    GEMINI_2_0_FLASH_LITE = LLMConfig(
        model_name=GeminiModels.GEMINI_2_0_FLASH_LITE, provider=LLMProvider.GOOGLE
    )


class LLMClientFactory:
    """Factory class for creating LLM clients based on model name."""

    _provider_handlers: Dict[str, Callable] = {
        LLMProvider.OPENAI: create_openai_client,
        LLMProvider.BEDROCK: create_bedrock_client,
        LLMProvider.GOOGLE: create_google_client,
        LLMProvider.PROXY: create_proxy_client,
    }

    @classmethod
    def register_provider(cls, provider: str, handler_func: Callable):
        cls._provider_handlers[provider] = handler_func

    @classmethod
    def create(cls, model_name: AvailableLLMs, **kwargs) -> BaseChatModel:
        model_config = model_name.value

        use_proxy = kwargs.get("use_proxy", False)
        if use_proxy:
            return cls._provider_handlers[LLMProvider.PROXY](model_config.provider, model_config.model_name, **kwargs)
        elif model_config.provider in cls._provider_handlers:
            return cls._provider_handlers[model_config.provider](
                model_config.model_name, **kwargs
            )

        raise ValueError(f"Provider {model_config.provider} is not implemented.")
