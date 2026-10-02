r"""Provide a concrete default factory for LangChain vector store
models."""

from __future__ import annotations

__all__ = ["VectorStoreFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.vectorstores.factory.base import BaseVectorStoreFactory

if TYPE_CHECKING:
    from langchain_core.vectorstores import VectorStore


class VectorStoreFactory(BaseVectorStoreFactory, MultilineDisplayMixin):
    """A concrete vector store factory that wraps a pre-built
    :class:`~langchain_core.vectorstores.VectorStore` instance.

    Use this when the vector store is already instantiated and you
    simply want to wrap it in the :class:`~BaseVectorStoreFactory`
    interface — for example, when injecting a fixed vector store into
    a component that expects a factory.

    Args:
        vector_store: A fully configured
            :class:`~langchain_core.vectorstores.VectorStore` instance
            to return from :meth:`make_vector_store`.

    Example:
        ```pycon
        >>> from langchain_core.embeddings.fake import FakeEmbeddings
        >>> from langchain_core.vectorstores import InMemoryVectorStore
        >>> from zenpyre.vectorstores.factory import VectorStoreFactory
        >>> factory = VectorStoreFactory(InMemoryVectorStore(FakeEmbeddings(size=128)))
        >>> vector_store = factory.make_vector_store()

        ```
    """

    def __init__(self, vector_store: VectorStore) -> None:
        self._vector_store = vector_store

    def make_vector_store(self) -> VectorStore:
        return self._vector_store

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"vector_store": self._vector_store}
