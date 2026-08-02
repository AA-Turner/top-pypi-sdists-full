r"""Provide a configurable factory for LangChain vector store models."""

from __future__ import annotations

__all__ = ["ConfigurableVectorStoreFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.vectorstores.factory.base import BaseVectorStoreFactory
from zenpyre.vectorstores.resolve import resolve_vector_store

if TYPE_CHECKING:
    from langchain_core.vectorstores import VectorStore


class ConfigurableVectorStoreFactory(BaseVectorStoreFactory, MultilineDisplayMixin):
    """A concrete vector store factory that accepts either a pre-built
    :class:`~langchain_core.vectorstores.VectorStore` instance or a
    configuration dictionary.

    When a dict is provided it is resolved at each
    :meth:`make_vector_store` call via :func:`~resolve_vector_store`,
    which uses ``objectory`` to instantiate the configured class.
    When an instance is provided it is returned as-is.

    Args:
        vector_store: A fully configured
            :class:`~langchain_core.vectorstores.VectorStore` instance,
            or a :class:`dict` containing an ``objectory`` factory
            specification (must include a ``"_target_"`` key pointing to
            the fully-qualified class name).

    Example:
        ```pycon
        >>> from langchain_core.embeddings.fake import FakeEmbeddings
        >>> from langchain_core.vectorstores import InMemoryVectorStore
        >>> from zenpyre.vectorstores.factory import ConfigurableVectorStoreFactory
        >>> factory = ConfigurableVectorStoreFactory(InMemoryVectorStore(FakeEmbeddings(size=128)))
        >>> vector_store = factory.make_vector_store()

        ```
    """

    def __init__(self, vector_store: VectorStore | dict[str, Any]) -> None:
        self._vector_store = vector_store

    def make_vector_store(self) -> VectorStore:
        return resolve_vector_store(self._vector_store)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"vector_store": self._vector_store}
