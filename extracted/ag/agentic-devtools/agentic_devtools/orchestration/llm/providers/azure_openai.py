"""Azure OpenAI provider implementation."""

from __future__ import annotations

import json
import time
from collections.abc import AsyncIterator
from typing import Any

import jsonschema

from agentic_devtools.orchestration.llm.base_provider import LLMProvider, omit_none_values
from agentic_devtools.orchestration.llm.errors import (
    StreamInterruptedError,
    StructuredOutputValidationError,
)
from agentic_devtools.orchestration.llm.retry import execute_with_retry
from agentic_devtools.orchestration.llm.types import (
    LLMMessage,
    LLMResponse,
    ProviderType,
    StreamChunk,
    TokenUsage,
)


class AzureOpenAIProvider(LLMProvider):
    """Azure OpenAI provider using the openai SDK."""

    def __init__(
        self,
        api_key: str,
        endpoint: str,
        model: str,
        api_version: str = "2024-02-01",
        temperature: float | None = None,
        max_tokens: int | None = None,
        timeout_seconds: int | None = None,
    ) -> None:
        self._api_key = api_key
        self._endpoint = endpoint
        self._model = model
        self._api_version = api_version
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._timeout_seconds = timeout_seconds
        self._client: Any = None

    def _get_client(self) -> Any:
        """Lazily initialize the AsyncAzureOpenAI client."""
        if self._client is None:
            from openai import AsyncAzureOpenAI

            self._client = AsyncAzureOpenAI(
                api_key=self._api_key,
                azure_endpoint=self._endpoint,
                api_version=self._api_version,
                timeout=self._timeout_seconds if self._timeout_seconds is not None else 60,
            )
        return self._client

    def _build_messages(self, messages: list[LLMMessage]) -> list[dict[str, str]]:
        """Convert LLMMessage list to OpenAI API format."""
        result = []
        for msg in messages:
            d: dict[str, str] = {"role": msg.role, "content": msg.content}
            if msg.name:
                d["name"] = msg.name
            result.append(d)
        return result

    async def complete(
        self,
        messages: list[LLMMessage],
        **kwargs: Any,
    ) -> LLMResponse:
        """Make a completion call to Azure OpenAI."""
        client = self._get_client()
        start = time.perf_counter()

        params: dict[str, Any] = {
            "model": self._model,
            "messages": self._build_messages(messages),
        }
        if self._temperature is not None:
            params["temperature"] = self._temperature
        if self._max_tokens is not None:
            params["max_tokens"] = self._max_tokens
        params.update(omit_none_values(kwargs))

        response = await execute_with_retry(client.chat.completions.create, **params)
        latency_ms = int((time.perf_counter() - start) * 1000)

        choice = response.choices[0]
        usage = None
        if response.usage:
            usage = TokenUsage(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            )

        return LLMResponse(
            text=choice.message.content or "",
            model=response.model or self._model,
            provider_type=ProviderType.AZURE_OPENAI,
            usage=usage,
            latency_ms=latency_ms,
        )

    async def complete_structured(
        self,
        messages: list[LLMMessage],
        schema: dict[str, Any],
        **kwargs: Any,
    ) -> LLMResponse:
        """Make a structured output call with JSON schema validation."""
        kwargs["response_format"] = {"type": "json_object"}

        # Add schema instruction to system message
        schema_instruction = f"\nRespond with valid JSON conforming to this schema:\n{json.dumps(schema)}"
        augmented_messages = list(messages)
        if augmented_messages and augmented_messages[0].role == "system":
            augmented_messages[0] = LLMMessage(
                role="system",
                content=augmented_messages[0].content + schema_instruction,
                name=augmented_messages[0].name,
            )
        else:
            augmented_messages.insert(
                0,
                LLMMessage(role="system", content=schema_instruction.strip()),
            )

        response = await self.complete(augmented_messages, **kwargs)

        # Validate response against schema
        try:
            parsed = json.loads(response.text)
            jsonschema.validate(parsed, schema)
        except (json.JSONDecodeError, jsonschema.ValidationError) as e:
            raise StructuredOutputValidationError(
                f"Response does not conform to schema: {e}",
                schema=schema,
                response_text=response.text,
                validation_errors=[str(e)],
            ) from e

        return response

    async def stream(
        self,
        messages: list[LLMMessage],
        **kwargs: Any,
    ) -> AsyncIterator[StreamChunk]:
        """Stream a completion response from Azure OpenAI."""
        client = self._get_client()

        params: dict[str, Any] = {
            "model": self._model,
            "messages": self._build_messages(messages),
            "stream": True,
            "stream_options": {"include_usage": True},
        }
        if self._temperature is not None:
            params["temperature"] = self._temperature
        if self._max_tokens is not None:
            params["max_tokens"] = self._max_tokens
        params.update(omit_none_values(kwargs))

        partial_response = ""
        chunk_index = 0

        try:
            response_stream = await execute_with_retry(client.chat.completions.create, **params)
            async for chunk in response_stream:
                if not chunk.choices and chunk.usage:
                    # Final usage-only chunk
                    yield StreamChunk(
                        text_delta="",
                        chunk_index=chunk_index,
                        finish_reason="stop",
                        token_usage=TokenUsage(
                            input_tokens=chunk.usage.prompt_tokens,
                            output_tokens=chunk.usage.completion_tokens,
                            total_tokens=chunk.usage.total_tokens,
                        ),
                    )
                    return

                if chunk.choices:
                    delta = chunk.choices[0].delta
                    text_delta = delta.content or "" if delta else ""
                    finish_reason = chunk.choices[0].finish_reason
                    partial_response += text_delta

                    token_usage = None
                    if finish_reason and chunk.usage:
                        token_usage = TokenUsage(
                            input_tokens=chunk.usage.prompt_tokens,
                            output_tokens=chunk.usage.completion_tokens,
                            total_tokens=chunk.usage.total_tokens,
                        )

                    yield StreamChunk(
                        text_delta=text_delta,
                        chunk_index=chunk_index,
                        finish_reason=finish_reason,
                        token_usage=token_usage,
                    )
                    chunk_index += 1
        except Exception as e:
            if chunk_index > 0:
                raise StreamInterruptedError(
                    f"Stream interrupted: {e}",
                    partial_response=partial_response,
                    chunks_received=chunk_index,
                ) from e
            raise
