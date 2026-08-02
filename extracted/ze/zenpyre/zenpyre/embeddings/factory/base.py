r"""Provide the base factory interface for creating LangChain embedding
models."""

from __future__ import annotations

__all__ = ["BaseEmbeddingsFactory"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.embeddings import Embeddings


class BaseEmbeddingsFactory(ABC):
    """Abstract base class for embedding model factories.

    Subclasses implement :meth:`make_embedding` to instantiate and return
    a configured :class:`~langchain_core.factory.Embeddings` object.
    This pattern decouples embedding creation from the rest of the
    codebase, making it easy to swap providers (e.g. Ollama, OpenAI,
    HuggingFace) without changing call sites.

    Example:
        ```pycon
        >>> from langchain_ollama import OllamaEmbeddings
        >>> from zenpyre.embeddings.factory import BaseEmbeddingsFactory
        >>> class OllamaEmbeddingsFactory(BaseEmbeddingsFactory):
        ...     def make_embeddings(self) -> OllamaEmbeddings:
        ...         return OllamaEmbeddings(model="nomic-embed-text")
        ...

        ```
    """

    @abstractmethod
    def make_embeddings(self) -> Embeddings:
        """Create and return a configured embedding model instance.

        Returns:
            A :class:`~langchain_core.factory.Embeddings` instance
                ready for use.
        """
