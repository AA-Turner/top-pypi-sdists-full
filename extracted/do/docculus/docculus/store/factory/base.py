r"""Provide the base factory interface for creating docculus
``BaseDocumentStore`` instances."""

from __future__ import annotations

__all__ = ["BaseDocumentStoreFactory"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from docculus.store.base import BaseDocumentStore


class BaseDocumentStoreFactory(ABC):
    """Abstract base class for
    :class:`~docculus.store.BaseDocumentStore` factories.

    Subclasses implement :meth:`make_document_store` to instantiate
    and return a configured
    :class:`~docculus.store.BaseDocumentStore` object.
    This pattern decouples document store creation from the rest of
    the codebase, making it easy to swap how a document store is
    built (e.g. a shared instance vs. a fresh one per call) without
    changing call sites.

    Example:
        ```pycon
        >>> from docculus.store import BaseDocumentStore, InMemoryDocumentStore
        >>> from docculus.store.factory import BaseDocumentStoreFactory
        >>> class MyDocumentStoreFactory(BaseDocumentStoreFactory):
        ...     def make_document_store(self) -> BaseDocumentStore:
        ...         return InMemoryDocumentStore()
        ...
        >>> factory = MyDocumentStoreFactory()
        >>> store = factory.make_document_store()

        ```
    """

    @abstractmethod
    def make_document_store(self) -> BaseDocumentStore:
        """Create and return a configured BaseDocumentStore instance.

        Returns:
            A :class:`~docculus.store.BaseDocumentStore`
            instance ready for use.
        """
