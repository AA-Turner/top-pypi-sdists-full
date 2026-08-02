r"""Provide a document loader backed by a document store."""

from __future__ import annotations

__all__ = ["DocumentStoreLoader"]


from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin
from langchain_core.document_loaders import BaseLoader

if TYPE_CHECKING:
    from collections.abc import Iterator

    from langchain_core.documents import Document

    from zenpyre.document_stores.base import BaseDocumentStore


class DocumentStoreLoader(BaseLoader, MultilineDisplayMixin):
    """A loader that yields documents from a :class:`BaseDocumentStore`.

    Use this when documents already live in a document store and you
    need to wrap them in a
    :class:`~langchain_core.document_loaders.BaseLoader` interface —
    for example, to feed a store's contents into a pipeline (e.g. a
    vector store indexer) that expects a loader.

    Args:
        store: The :class:`~zenpyre.document_stores.base
            .BaseDocumentStore` to load documents from.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.document_loaders import DocumentStoreLoader
        >>> from zenpyre.document_stores import InMemoryDocumentStore
        >>> store = InMemoryDocumentStore()
        >>> store.add_documents(
        ...     [Document(id="1", page_content="Hello"), Document(id="2", page_content="World")]
        ... )
        >>> loader = DocumentStoreLoader(store)
        >>> docs = loader.load()

        ```
    """

    def __init__(self, store: BaseDocumentStore) -> None:
        self._store = store

    def lazy_load(self) -> Iterator[Document]:
        yield from self._store.lazy_all()

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"store": self._store}
