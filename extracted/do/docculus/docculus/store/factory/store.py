r"""Provide a DocumentStore factory backed by a persista BaseStore
factory."""

from __future__ import annotations

__all__ = ["StoreDocumentStoreFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from docculus.store.document import DocumentStore
from docculus.store.factory.base import BaseDocumentStoreFactory

if TYPE_CHECKING:
    from persista.store.factory.base import BaseStoreFactory

    from docculus.store.document import MetadataMode


class StoreDocumentStoreFactory(BaseDocumentStoreFactory, MultilineDisplayMixin):
    """A concrete document store factory that builds its backing store
    from a :class:`~persista.store.factory.BaseStoreFactory`.

    Use this when the underlying key-value store needs to be freshly
    created (e.g. a new connection, a new in-memory dict) each time a
    :class:`~docculus.store.DocumentStore` is requested, rather than
    sharing one store instance across every document store.

    Args:
        store_factory: The factory used to create the backing
            key-value store passed to each
            :class:`~docculus.store.DocumentStore` built by
            :meth:`make_document_store`.
        metadata_mode: Forwarded to each created
            :class:`~docculus.store.DocumentStore`. See
            :class:`~docculus.store.DocumentStore` for details.

    Example:
        ```pycon
        >>> from docculus.store.factory import StoreDocumentStoreFactory
        >>> from persista.store.factory import StoreFactory
        >>> from persista.store import InMemoryStore
        >>> factory = StoreDocumentStoreFactory(StoreFactory(InMemoryStore()))
        >>> store = factory.make_document_store()
        >>> store.open()

        ```
    """

    def __init__(
        self,
        store_factory: BaseStoreFactory,
        metadata_mode: MetadataMode = "flat",
    ) -> None:
        self._store_factory = store_factory
        self._metadata_mode = metadata_mode

    def make_document_store(self) -> DocumentStore:
        return DocumentStore(
            store=self._store_factory.make_store(),
            metadata_mode=self._metadata_mode,
        )

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {
            "store_factory": self._store_factory,
            "metadata_mode": self._metadata_mode,
        }
