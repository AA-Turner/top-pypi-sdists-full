r"""Provide the base factory interface for creating zenpyre
BaseDocumentStore models."""

from __future__ import annotations

__all__ = ["BaseDocumentStoreFactory"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zenpyre.document_stores.base import BaseDocumentStore


class BaseDocumentStoreFactory(ABC):
    """Abstract base class for
    :class:`~zenpyre.document_stores.base.BaseDocumentStore` factories.

    Subclasses implement :meth:`make_document_store` to instantiate
    and return a configured
    :class:`~zenpyre.document_stores.base.BaseDocumentStore` object.
    This pattern decouples document store creation from the rest of
    the codebase, making it easy to swap document stores (e.g.
    in-memory, SQLite, DuckDB) without changing call sites.

    Example:
        ```pycon
        >>> from zenpyre.document_stores import InMemoryDocumentStore
        >>> from zenpyre.document_stores.base import BaseDocumentStore
        >>> from zenpyre.document_stores.factory import BaseDocumentStoreFactory
        >>> class MyDocumentStoreFactory(BaseDocumentStoreFactory):
        ...     def make_document_store(self) -> BaseDocumentStore:
        ...         return InMemoryDocumentStore()
        ...
        >>> factory = MyDocumentStoreFactory()
        >>> document_store = factory.make_document_store()

        ```
    """

    @abstractmethod
    def make_document_store(self) -> BaseDocumentStore:
        """Create and return a configured BaseDocumentStore instance.

        Returns:
            A :class:`~zenpyre.document_stores.base.BaseDocumentStore`
            instance ready for use.
        """
