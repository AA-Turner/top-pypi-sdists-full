r"""Provide the base factory interface for creating LangChain vector
store models."""

from __future__ import annotations

__all__ = ["BaseVectorStoreFactory"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.vectorstores import VectorStore


class BaseVectorStoreFactory(ABC):
    """Abstract base class for vector store factories.

    Subclasses implement :meth:`make_vector_store` to instantiate and
    return a configured :class:`~langchain_core.vectorstores.VectorStore`
    object.  This pattern decouples vector store creation from the rest
    of the codebase, making it easy to swap backends (e.g. in-memory,
    Chroma, Pinecone) without changing call sites.

    Example:
        ```pycon
        >>> from langchain_core.embeddings.fake import FakeEmbeddings
        >>> from langchain_core.vectorstores import InMemoryVectorStore
        >>> from zenpyre.vectorstores.factory import BaseVectorStoreFactory
        >>> class InMemoryVectorStoreFactory(BaseVectorStoreFactory):
        ...     def make_vector_store(self) -> InMemoryVectorStore:
        ...         return InMemoryVectorStore(FakeEmbeddings(size=128))
        ...

        ```
    """

    @abstractmethod
    def make_vector_store(self) -> VectorStore:
        """Create and return a configured vector store instance.

        Returns:
            A :class:`~langchain_core.vectorstores.VectorStore` instance
            ready for use.
        """
