"""Base class for embedding providers."""

from abc import ABC, abstractmethod
from typing import Optional

from ..models import EmbeddingModel


class EmbeddingProvider(ABC):
    """
    Abstract base class for embedding providers.

    Each provider (OpenAI, Fireworks, etc.) implements this interface.
    The registry uses this to provide a unified embedding API.
    """

    def __init__(self, model: EmbeddingModel):
        """
        Initialize provider with a specific model.

        Args:
            model: The embedding model to use
        """
        self._model = model

    @property
    def model(self) -> EmbeddingModel:
        """Get the embedding model."""
        return self._model

    @property
    def dimensions(self) -> int:
        """Get embedding dimensions for the current model."""
        return self._model.dimensions

    @property
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available (API key configured, etc.)."""
        pass

    @abstractmethod
    def embed_texts(self, texts: list[str]) -> list[Optional[list[float]]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors. None for failed embeddings.
        """
        pass

    def embed_text(self, text: str) -> Optional[list[float]]:
        """
        Generate embedding for a single text.

        Args:
            text: Text string to embed

        Returns:
            Embedding vector or None if failed
        """
        if not text:
            return None
        embeddings = self.embed_texts([text])
        return embeddings[0] if embeddings else None

    def embed_query(self, query: str) -> Optional[list[float]]:
        """
        Generate embedding for a search query.

        Some models treat queries differently from documents.
        Override this method if the model requires special query handling.

        Args:
            query: Search query string

        Returns:
            Embedding vector or None if failed
        """
        return self.embed_text(query)

    def _truncate_text(self, text: str, max_chars: int = 8000) -> str:
        """
        Truncate text to avoid token limits.

        Args:
            text: Text to truncate
            max_chars: Maximum character length (roughly 4 chars per token)

        Returns:
            Truncated text
        """
        if text and len(text) > max_chars:
            return text[:max_chars]
        return text or ""

    def _clean_batch(self, texts: list[str]) -> list[str]:
        """
        Clean and truncate a batch of texts.

        Args:
            texts: List of texts to clean

        Returns:
            Cleaned texts
        """
        # Calculate max chars based on model's max tokens (roughly 4 chars per token)
        max_chars = min(self._model.spec.max_tokens * 4, 32000)
        return [self._truncate_text(t, max_chars) for t in texts]
