"""Mock LLM provider for deterministic testing.

Returns predefined responses from fixture data, enabling integration tests
without real LLM API calls.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from agentic_devtools.orchestration.llm.base_provider import LLMProvider
from agentic_devtools.orchestration.llm.types import (
    LLMMessage,
    LLMResponse,
    ProviderType,
    StreamChunk,
    TokenUsage,
)


class MockLLMProvider(LLMProvider):
    """Deterministic LLM provider that returns predefined responses.

    Useful for unit and integration tests where real LLM calls are
    unnecessary or undesirable.

    Args:
        responses: List of response texts to return in order.
            Cycles when exhausted.
        model: Model identifier to report.
        usage: Optional token usage to include in responses.
    """

    def __init__(
        self,
        responses: list[str] | None = None,
        *,
        model: str = "mock-model",
        usage: TokenUsage | None = None,
    ) -> None:
        self._responses = responses or ['{"result": "mock response"}']
        self._model = model
        self._usage = usage
        self._call_count = 0
        self._call_history: list[dict[str, Any]] = []

    @property
    def call_count(self) -> int:
        """Number of calls made to this provider."""
        return self._call_count

    @property
    def call_history(self) -> list[dict[str, Any]]:
        """History of all calls made to this provider."""
        return list(self._call_history)

    def _next_response(self) -> str:
        """Get the next response text, cycling if needed."""
        idx = self._call_count % len(self._responses)
        return self._responses[idx]

    async def complete(
        self,
        messages: list[LLMMessage],
        **kwargs: Any,
    ) -> LLMResponse:
        """Return the next predefined response."""
        response_text = self._next_response()
        self._call_history.append(
            {
                "method": "complete",
                "messages": messages,
                "kwargs": kwargs,
            }
        )
        self._call_count += 1

        return LLMResponse(
            text=response_text,
            model=self._model,
            provider_type=ProviderType.LOCAL_MODEL,
            usage=self._usage,
            served_from_fixture=True,
        )

    async def complete_structured(
        self,
        messages: list[LLMMessage],
        schema: dict[str, Any],
        **kwargs: Any,
    ) -> LLMResponse:
        """Return the next predefined response (assumes valid JSON for schema)."""
        response_text = self._next_response()
        self._call_history.append(
            {
                "method": "complete_structured",
                "messages": messages,
                "schema": schema,
                "kwargs": kwargs,
            }
        )
        self._call_count += 1

        return LLMResponse(
            text=response_text,
            model=self._model,
            provider_type=ProviderType.LOCAL_MODEL,
            usage=self._usage,
            served_from_fixture=True,
        )

    async def stream(
        self,
        messages: list[LLMMessage],
        **kwargs: Any,
    ) -> AsyncIterator[StreamChunk]:
        """Stream the next predefined response as a single chunk."""
        response_text = self._next_response()
        self._call_history.append(
            {
                "method": "stream",
                "messages": messages,
                "kwargs": kwargs,
            }
        )
        self._call_count += 1

        yield StreamChunk(
            text_delta=response_text,
            chunk_index=0,
            finish_reason="stop",
            token_usage=self._usage,
        )
