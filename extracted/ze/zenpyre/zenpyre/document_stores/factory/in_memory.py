r"""Provide a concrete factory that creates an in-memory
BaseDocumentStore."""

from __future__ import annotations

__all__ = ["InMemoryDocumentStoreFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.document_stores import InMemoryDocumentStore
from zenpyre.document_stores.factory.base import BaseDocumentStoreFactory

if TYPE_CHECKING:
    from zenpyre.document_stores.base import BaseDocumentStore


class InMemoryDocumentStoreFactory(BaseDocumentStoreFactory, MultilineDisplayMixin):
    """A concrete BaseDocumentStore factory that builds a fresh
    :class:`~zenpyre.document_stores.InMemoryDocumentStore` on each
    :meth:`make_document_store` call.

    Use this when you want a factory that lazily constructs a new,
    empty :class:`~zenpyre.document_stores.InMemoryDocumentStore` each
    time :meth:`make_document_store` is called, rather than wrapping
    an already-instantiated store (see
    :class:`~zenpyre.document_stores.factory.DocumentStoreFactory` for
    that).

    Example:
        ```pycon
        >>> from zenpyre.document_stores.factory import InMemoryDocumentStoreFactory
        >>> factory = InMemoryDocumentStoreFactory()
        >>> document_store = factory.make_document_store()

        ```
    """

    def make_document_store(self) -> BaseDocumentStore:
        return InMemoryDocumentStore()

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {}
