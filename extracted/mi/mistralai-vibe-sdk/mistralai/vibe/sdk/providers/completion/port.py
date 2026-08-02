"""CompletionModel port.

The CompletionModel protocol defines the interface for LLM completion.
It receives a standardized CompletionRequest and returns an async iterator
of CompletionChunk objects (streaming). Adapters are thin API wrappers
with no event knowledge.
"""

from collections.abc import AsyncIterator
from typing import Protocol, runtime_checkable

from mistralai.vibe.sdk.providers.completion.types import (
    CompletionChunk,
    CompletionRequest,
)


@runtime_checkable
class CompletionModel(Protocol):
    """Protocol for LLM completion (streaming).

    Implementations receive a standardized CompletionRequest and
    return an async iterator of CompletionChunk objects.
    They know nothing about events.
    """

    def complete(self, request: CompletionRequest) -> AsyncIterator[CompletionChunk]:
        """Stream the completion as chunks.

        Args:
            request: Standardized completion request with messages and tools.

        Returns:
            Async iterator of CompletionChunk objects.
        """
        ...


__all__ = ["CompletionModel"]
