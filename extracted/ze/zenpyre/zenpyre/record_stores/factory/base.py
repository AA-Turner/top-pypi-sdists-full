r"""Provide the base factory interface for creating zenpyre
BaseRecordStore models."""

from __future__ import annotations

__all__ = ["BaseRecordStoreFactory"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zenpyre.record_stores.base import BaseRecordStore


class BaseRecordStoreFactory(ABC):
    """Abstract base class for
    :class:`~zenpyre.record_stores.base.BaseRecordStore` factories.

    Subclasses implement :meth:`make_record_store` to instantiate
    and return a configured
    :class:`~zenpyre.record_stores.base.BaseRecordStore` object.
    This pattern decouples record store creation from the rest of
    the codebase, making it easy to swap record stores (e.g.
    in-memory, SQLite, DuckDB) without changing call sites.

    Example:
        ```pycon
        >>> from zenpyre.record_stores import InMemoryRecordStore
        >>> from zenpyre.record_stores.base import BaseRecordStore
        >>> from zenpyre.record_stores.factory import BaseRecordStoreFactory
        >>> class MyRecordStoreFactory(BaseRecordStoreFactory):
        ...     def make_record_store(self) -> BaseRecordStore:
        ...         return InMemoryRecordStore()
        ...
        >>> factory = MyRecordStoreFactory()
        >>> record_store = factory.make_record_store()

        ```
    """

    @abstractmethod
    def make_record_store(self) -> BaseRecordStore:
        """Create and return a configured BaseRecordStore instance.

        Returns:
            A :class:`~zenpyre.record_stores.base.BaseRecordStore`
            instance ready for use.
        """
