"""Abstract base for all Sage model providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class ModelInfo:
    """Metadata about an available model."""

    id: str  # Unique ID used in commands, e.g. "gemini-2.0-flash"
    provider: str  # Provider name, e.g. "gemini"
    name: str  # Human-readable label
    local: bool  # True for GGUF / local, False for API
    description: str = ""  # Brief description of model capabilities
    pros: str = ""  # Advantages/strengths
    cons: str = ""  # Disadvantages/limitations


@dataclass(frozen=True)
class Message:
    """A single conversation message."""

    role: str  # "system", "user", or "assistant"
    content: str


class ProviderBase(ABC):
    """Interface that every model provider must implement."""

    name: str  # Short identifier, e.g. "gemini"

    @abstractmethod
    def generate(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """Return the full response text (non-streaming)."""

    @abstractmethod
    def stream(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Iterator[str]:
        """Yield response tokens one at a time."""

    @abstractmethod
    def list_models(self) -> list[ModelInfo]:
        """Return models this provider can serve right now."""

    @abstractmethod
    def is_available(self) -> bool:
        """Can this provider handle requests right now?"""
