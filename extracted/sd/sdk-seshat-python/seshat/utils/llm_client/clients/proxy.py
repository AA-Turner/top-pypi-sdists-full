import json
import logging
import os
from typing import Union, Any, Optional, Iterator, Mapping, List

import requests
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, AIMessageChunk
from langchain_core.outputs import ChatGenerationChunk, ChatResult, ChatGeneration

from seshat.utils.llm_client.clients.aws import BedrockModels
from seshat.utils.llm_client.clients.google import GeminiModels
from seshat.utils.llm_client.clients.openai import OpenAIModels
from seshat.utils.llm_client.llm_provider import LLMProvider

ProxyServerAIModels = Union[BedrockModels, GeminiModels, OpenAIModels]

PROXY_SERVER_DEFAULT_TEMPERATURE = 0.6
PROXY_SERVER_DEFAULT_MAX_TOKENS = 8192

logger = logging.getLogger(__name__)

def create_proxy_client(provider: LLMProvider, model: ProxyServerAIModels, **kwargs) -> BaseChatModel:
    api_key = kwargs.pop('api_key', os.environ.get("PROXY_API_KEY"))
    base_url = kwargs.pop('base_url', os.environ.get("PROXY_BASE_URL"))
    return ChatProxyModel(
        provider=provider,
        model=model,
        api_key=api_key,
        base_url=base_url,
        **kwargs,
    )


class ChatProxyModel(BaseChatModel):
    model: ProxyServerAIModels
    provider: LLMProvider
    api_key: str = ""
    base_url: str = ""
    temperature: float = 0.6
    max_tokens: int = 8192

    def __init__(
            self,
            provider: LLMProvider,
            model: ProxyServerAIModels,
            *args,
            **kwargs
    ):
        api_key = kwargs.pop("api_key", "")
        base_url = kwargs.pop("base_url", "")
        temperature = kwargs.pop("temperature", PROXY_SERVER_DEFAULT_TEMPERATURE)
        max_tokens = kwargs.pop("max_tokens", PROXY_SERVER_DEFAULT_MAX_TOKENS)

        super().__init__(
            provider=provider,
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens,
            *args,
            **kwargs
        )

    def _get_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key,
        }

    def _convert_messages(self, messages: List[BaseMessage], **kwargs) -> dict:
        """Convert LangChain messages to proxy server request format."""
        system_prompt = ""
        user_prompt = ""
        context_parts = []

        for i, msg in enumerate(messages):
            if isinstance(msg, SystemMessage):
                system_prompt = str(msg.content)
            elif isinstance(msg, HumanMessage):
                # Last human message becomes user_prompt, others go to context
                if i == len(messages) - 1 or not any(
                        isinstance(m, HumanMessage) for m in messages[i + 1:]
                ):
                    user_prompt = str(msg.content)
                else:
                    context_parts.append(f"User: {msg.content}")
            elif isinstance(msg, AIMessage):
                context_parts.append(f"Assistant: {msg.content}")
            else:
                context_parts.append(str(msg.content))

        return {
            "provider": self.provider.value if hasattr(self.provider, 'value') else str(self.provider),
            "model": self.model.value if hasattr(self.model, 'value') else str(self.model),
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "context": "\n".join(context_parts),
            "directives": kwargs.get("directives", []),
            "exemplars": kwargs.get("exemplars", []),
            "output": kwargs.get("output", ""),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
        }

    def _unwrap_response(self, response: Any) -> Any:
        if not isinstance(response, dict):
            raise InvalidProxyResponse()
        if response.get("error") is not None:
            raise ProxyResponseError(f"status code: {response.get('status')}, error: {response.get('error')}")
        if "data" not in response:
            raise InvalidProxyResponse()
        return response.get("data")

    def _generate(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> ChatResult:
        payload = self._convert_messages(messages, **kwargs)

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            headers=self._get_headers(),
        )
        response.raise_for_status()

        data = response.json()
        output = self._unwrap_response(data).get("output", "")

        generation = ChatGeneration(message=AIMessage(content=output))
        return ChatResult(generations=[generation])

    def _stream(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        payload = self._convert_messages(messages, **kwargs)

        response = requests.post(
            f"{self.base_url}/api/stream",
            json=payload,
            headers=self._get_headers(),
            stream=True,
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if not line:
                continue

            line_str = line.decode("utf-8")

            if line_str.startswith("data:"):
                json_str = line_str[5:].strip()
            else:
                json_str = line_str.strip()

            if not json_str:
                continue

            try:
                event = json.loads(json_str)
            except json.JSONDecodeError:
                logger.error(f"Received non-decodable SSE data from proxy server: {json_str}")
                continue

            event_type = event.get("type")
            data = event.get("data")

            if event_type == "initial":
                continue
            elif event_type == "token" and data:
                text = data.get("text", "")
                if text:
                    chunk = ChatGenerationChunk(
                        message=AIMessageChunk(content=text)
                    )
                    if run_manager:
                        run_manager.on_llm_new_token(text)
                    yield chunk
            elif event_type == "end":
                break

    @property
    def _llm_type(self) -> str:
        return "proxy-chat-model"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"provider": self.provider, "model": self.model}


class InvalidProxyResponse(Exception):
    def __init__(self, message: str = "invalid proxy response format"):
        self.message = message
        super().__init__(self.message)


class ProxyResponseError(Exception):
    def __init__(self, message: str = "error received from proxy server"):
        self.message = message
        super().__init__(self.message)
