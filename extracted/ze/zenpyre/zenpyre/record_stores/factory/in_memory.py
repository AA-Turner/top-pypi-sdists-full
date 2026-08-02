r"""Provide a concrete factory that creates an in-memory
BaseRecordStore."""

from __future__ import annotations

__all__ = ["InMemoryRecordStoreFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.record_stores import InMemoryRecordStore
from zenpyre.record_stores.factory.base import BaseRecordStoreFactory

if TYPE_CHECKING:
    from zenpyre.record_stores.base import BaseRecordStore


class InMemoryRecordStoreFactory(BaseRecordStoreFactory, MultilineDisplayMixin):
    """A concrete BaseRecordStore factory that builds a fresh
    :class:`~zenpyre.record_stores.InMemoryRecordStore` on each
    :meth:`make_record_store` call.

    Use this when you want a factory that lazily constructs a new,
    empty :class:`~zenpyre.record_stores.InMemoryRecordStore` each
    time :meth:`make_record_store` is called, rather than wrapping an
    already-instantiated store (see
    :class:`~zenpyre.record_stores.factory.RecordStoreFactory` for
    that).

    Example:
        ```pycon
        >>> from zenpyre.record_stores.factory import InMemoryRecordStoreFactory
        >>> factory = InMemoryRecordStoreFactory()
        >>> record_store = factory.make_record_store()

        ```
    """

    def make_record_store(self) -> BaseRecordStore:
        return InMemoryRecordStore()

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {}
