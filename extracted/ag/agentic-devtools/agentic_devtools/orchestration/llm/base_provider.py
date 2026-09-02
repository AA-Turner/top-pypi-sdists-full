"""Abstract base class for LLM providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Mapping
from typing import Any

from agentic_devtools.orchestration.llm.types import (
    LLMMessage,
    LLMResponse,
    StreamChunk,
)


def omit_none_values(values: Mapping[str, Any]) -> dict[str, Any]:
    """Return a shallow copy without None-valued entries."""
    return {key: value for key, value in values.items() if value is not None}


class LLMProvider(ABC):
    """Abstract interface that all provider implementations conform to.

    Defines methods for completion calls (standard and streaming),
    and structured output calls. Carries immutable configuration once
    instantiated.
    """

    @abstractmethod
    async def complete(
        self,
        messages: list[LLMMessage],
        **kwargs: Any,
    ) -> LLMResponse:
        """Make a standard completion call.

        Args:
            messages: List of messages forming the conversation.
            **kwargs: Additional provider-specific parameters.

        Returns:
            LLMResponse with generated text and metadata.
        """

    @abstractmethod
    async def complete_structured(
        self,
        messages: list[LLMMessage],
        schema: dict[str, Any],
        **kwargs: Any,
    ) -> LLMResponse:
        """Make a structured output call with JSON schema validation.

        Args:
            messages: List of messages forming the conversation.
            schema: JSON schema that the response must conform to.
            **kwargs: Additional provider-specific parameters.

        Returns:
            LLMResponse with JSON text conforming to the schema.

        Raises:
            StructuredOutputValidationError: If response doesn't match schema.
        """

    @abstractmethod
    async def stream(
        self,
        messages: list[LLMMessage],
        **kwargs: Any,
    ) -> AsyncIterator[StreamChunk]:
        """Stream a completion response as an async iterator.

        Args:
            messages: List of messages forming the conversation.
            **kwargs: Additional provider-specific parameters.

        Yields:
            StreamChunk objects with text deltas and metadata.
            Final chunk carries token_usage.

        Raises:
            StreamInterruptedError: If stream is interrupted mid-response.
        """
        # Abstract method - must yield to make this an async generator
        if False:  # pragma: no cover
            yield StreamChunk(text_delta="")  # pragma: no cover
