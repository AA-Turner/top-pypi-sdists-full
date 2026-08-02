r"""Provide a concrete default factory for zenpyre BaseDocumentStore
models."""

from __future__ import annotations

__all__ = ["DocumentStoreFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.document_stores.factory.base import BaseDocumentStoreFactory

if TYPE_CHECKING:
    from zenpyre.document_stores.base import BaseDocumentStore


class DocumentStoreFactory(BaseDocumentStoreFactory, MultilineDisplayMixin):
    """A concrete BaseDocumentStore factory that wraps a pre-built
    :class:`~zenpyre.document_stores.base.BaseDocumentStore` instance.

    Use this when the document store is already instantiated and you
    simply want to wrap it in the :class:`~BaseDocumentStoreFactory`
    interface — for example, when injecting a fixed document store
    into a component that expects a factory.

    Args:
        document_store: A fully configured
            :class:`~zenpyre.document_stores.base.BaseDocumentStore`
            instance to return from :meth:`make_document_store`.

    Example:
        ```pycon
        >>> from zenpyre.document_stores import InMemoryDocumentStore
        >>> from zenpyre.document_stores.factory import DocumentStoreFactory
        >>> factory = DocumentStoreFactory(InMemoryDocumentStore())
        >>> document_store = factory.make_document_store()

        ```
    """

    def __init__(self, document_store: BaseDocumentStore) -> None:
        self._document_store = document_store

    def make_document_store(self) -> BaseDocumentStore:
        return self._document_store

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"document_store": self._document_store}
