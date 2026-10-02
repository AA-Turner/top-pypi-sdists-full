r"""Provide a concrete default factory for docculus
``BaseDocumentStore`` instances."""

from __future__ import annotations

__all__ = ["DocumentStoreFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from docculus.store.factory.base import BaseDocumentStoreFactory

if TYPE_CHECKING:
    from docculus.store.base import BaseDocumentStore


class DocumentStoreFactory(BaseDocumentStoreFactory, MultilineDisplayMixin):
    """A concrete document store factory that wraps a pre-built
    :class:`~docculus.store.BaseDocumentStore` instance.

    Use this when the document store is already instantiated and you
    simply want to wrap it in the :class:`~BaseDocumentStoreFactory`
    interface — for example, when injecting a fixed document store
    into a component that expects a factory.

    Args:
        document_store: A fully configured
            :class:`~docculus.store.BaseDocumentStore`
            instance to return from :meth:`make_document_store`.

    Example:
        ```pycon
        >>> from docculus.store import InMemoryDocumentStore
        >>> from docculus.store.factory import DocumentStoreFactory
        >>> factory = DocumentStoreFactory(InMemoryDocumentStore())
        >>> store = factory.make_document_store()

        ```
    """

    def __init__(self, document_store: BaseDocumentStore) -> None:
        self._document_store = document_store

    def make_document_store(self) -> BaseDocumentStore:
        return self._document_store

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"document_store": self._document_store}
