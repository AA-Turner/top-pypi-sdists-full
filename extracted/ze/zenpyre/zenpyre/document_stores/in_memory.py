"""Provide an in-memory implementation of BaseDocumentStore."""

from __future__ import annotations

__all__ = ["InMemoryDocumentStore"]

import copy
import logging
from typing import TYPE_CHECKING, Any

from coola.display import InlineDisplayMixin

from zenpyre.document_stores.base import BaseDocumentStore

if TYPE_CHECKING:
    from collections.abc import Iterator

    from langchain_core.documents import Document

logger: logging.Logger = logging.getLogger(__name__)


class InMemoryDocumentStore(BaseDocumentStore, InlineDisplayMixin):
    """A :class:`~zenpyre.document_stores.base.BaseDocumentStore`
    implementation backed by a plain ``dict``.

    Documents are keyed by their ``id`` and held entirely in process
    memory -- nothing is persisted to disk. This is primarily useful
    for testing, small-scale exploration, or pipelines that don't need
    durability.

    Documents are deep-copied on both write and read so that mutating
    a :class:`~langchain_core.documents.Document` returned by this
    store (or a document passed into :meth:`add_documents`) never
    affects the store's internal state. This trades some performance
    for isolation; for very large documents or hot loops, consider a
    store that doesn't copy on every access.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.document_stores import InMemoryDocumentStore
        >>> store = InMemoryDocumentStore()
        >>> store.add_documents([Document(id="1", page_content="hello")])
        >>> store.count()
        1
        >>> store.get("1").page_content
        'hello'

        ```
    """

    def __init__(self) -> None:
        self._docs: dict[str, Document] = {}

    def close(self) -> None:
        # Discard all documents: an in-memory store has nothing to
        # persist, so closing (and later reopening via the context
        # manager) it is equivalent to starting over with a fresh, empty
        # store.
        self._docs.clear()

    def add_documents(self, docs: list[Document]) -> None:
        missing_ids = [i for i, doc in enumerate(docs) if not doc.id]
        if missing_ids:
            msg = f"All documents must have an id. Missing id at index(es): {missing_ids}"
            raise ValueError(msg)

        for doc in docs:
            self._docs[doc.id] = copy.deepcopy(doc)

        logger.debug("Added/replaced %d document(s)", len(docs))

    def get(self, doc_id: str) -> Document | None:
        doc = self._docs.get(doc_id)
        return copy.deepcopy(doc) if doc is not None else None

    def get_many(self, doc_ids: list[str]) -> list[Document | None]:
        return [self.get(doc_id) for doc_id in doc_ids]

    def filter(self, **metadata_filters: Any) -> list[Document]:
        if not metadata_filters:
            return self.all()

        matches = [
            doc
            for doc in self._docs.values()
            if all(doc.metadata.get(key) == value for key, value in metadata_filters.items())
        ]
        return [copy.deepcopy(doc) for doc in matches]

    def delete(self, doc_id: str) -> None:
        self._docs.pop(doc_id, None)

    def delete_many(self, doc_ids: list[str]) -> None:
        for doc_id in doc_ids:
            self.delete(doc_id)

    def check_ids(self, doc_ids: list[str]) -> tuple[list[str], list[str]]:
        found = [doc_id for doc_id in doc_ids if doc_id in self._docs]
        missing = [doc_id for doc_id in doc_ids if doc_id not in self._docs]
        return found, missing

    def all(self) -> list[Document]:
        return [copy.deepcopy(doc) for doc in self._docs.values()]

    def iter_batches(self, batch_size: int = 1000) -> Iterator[list[Document]]:
        if batch_size < 1:
            msg = f"batch_size must be a positive integer, got {batch_size}"
            raise ValueError(msg)

        batch = []
        for doc in self._docs.values():
            batch.append(copy.deepcopy(doc))
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

    def count(self) -> int:
        return len(self._docs)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {}
