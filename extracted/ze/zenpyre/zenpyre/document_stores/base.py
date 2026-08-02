r"""Provide the abstract base class for document stores."""

from __future__ import annotations

__all__ = ["BaseDocumentStore"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Generator, Iterator
    from typing import Self

    from langchain_core.documents import Document


class BaseDocumentStore(ABC):
    """Abstract base class for document stores.

    Defines the common interface that all document store implementations
    must provide.  Concrete implementations include
    :class:`~zenpyre.document_stores.InMemoryDocumentStore`,
    :class:`~zenpyre.document_stores.SQLiteDocumentStore`,
    :class:`~zenpyre.document_stores.DuckDBDocumentStore`, and their
    typed variants which store known metadata fields as native columns
    for faster filtering.

    To implement a custom document store, subclass
    :class:`BaseDocumentStore` and implement all abstract methods.

    Implementations are expected to support use as a context manager
    (``with SomeDocumentStore(...) as store: ...``), which calls
    :meth:`close` automatically on exit.
    """

    @abstractmethod
    def add_documents(self, docs: list[Document]) -> None:
        """Add or replace documents in the store.

        Documents whose ``id`` already exists should be replaced
        (upsert semantics).

        Args:
            docs: The list of :class:`~langchain_core.documents.Document`
                instances to add.  Each document must have an ``id``.

        Raises:
            ValueError: If any document has no ``id``.
        """

    @abstractmethod
    def get(self, doc_id: str) -> Document | None:
        """Retrieve a single document by its ID.

        Args:
            doc_id: The document ID to look up.

        Returns:
            The :class:`~langchain_core.documents.Document`, or
            ``None`` if not found.
        """

    @abstractmethod
    def get_many(self, doc_ids: list[str]) -> list[Document | None]:
        """Retrieve multiple documents by their IDs.

        Args:
            doc_ids: The document IDs to look up.

        Returns:
            A list the same length as ``doc_ids``, with the
            corresponding :class:`~langchain_core.documents.Document`
            for each ID that exists, or ``None`` for IDs not found.
        """

    @abstractmethod
    def filter(self, **metadata_filters: Any) -> list[Document]:
        """Retrieve documents matching all provided metadata filters.

        All filters should be combined with ``AND``.  Each keyword
        argument matches the corresponding metadata key exactly.

        Args:
            **metadata_filters: Key-value pairs where each key is a
                metadata field name and the value is the exact value
                to match.  Calling with no arguments should return all
                documents.

        Returns:
            A list of matching
            :class:`~langchain_core.documents.Document` instances.
        """

    @abstractmethod
    def delete(self, doc_id: str) -> None:
        """Delete a document by its ID.

        IDs that do not exist should be silently ignored.

        Args:
            doc_id: The ID of the document to delete.
        """

    @abstractmethod
    def delete_many(self, doc_ids: list[str]) -> None:
        """Delete multiple documents by their IDs.

        IDs that do not exist should be silently ignored.

        Args:
            doc_ids: The IDs of the documents to delete.
        """

    @abstractmethod
    def check_ids(self, doc_ids: list[str]) -> tuple[list[str], list[str]]:
        """Check which document IDs exist in the store.

        Args:
            doc_ids: The document IDs to check.

        Returns:
            A tuple of two lists: ``(found, missing)`` where ``found``
            contains the IDs that exist in the store and ``missing``
            contains the IDs that do not.
        """

    @abstractmethod
    def all(self) -> list[Document]:
        """Return all documents in the store.

        Returns:
            A list of all :class:`~langchain_core.documents.Document`
            instances currently in the store.
        """

    def lazy_all(self, batch_size: int = 32) -> Iterator[Document]:
        """Lazily iterate over all documents without loading them all
        into memory at once.

        Args:
            batch_size: The batch size used internally when pulling
                documents from the underlying store. Does not affect
                the granularity of what is yielded — documents are
                always yielded one at a time.

        Yields:
            One :class:`~langchain_core.documents.Document` at a time,
            in the same order as :meth:`all`.
        """
        for batch in self.iter_batches(batch_size=batch_size):
            yield from batch

    @abstractmethod
    def iter_batches(self, batch_size: int = 32) -> Generator[list[Document], None, None]:
        """Yield documents in batches, avoiding loading the whole store
        into memory at once.

        This is the scalable equivalent of :meth:`all`: instead of
        materializing every document as a single list, it streams
        them from the database in chunks of ``batch_size``.

        Args:
            batch_size: The maximum number of documents to yield per
                batch. Must be a positive integer.

        Yields:
            Lists of documents, each with at most ``batch_size``
            elements, in the same order as :meth:`all`. The last batch
            may contain fewer than ``batch_size`` documents.

        Example:
            ```pycon
            >>> from zenpyre.document_stores import InMemoryDocumentStore
            >>> from langchain_core.documents import Document
            >>> store = InMemoryDocumentStore()
            >>> store.add_documents([Document(id=str(i), page_content=str(i)) for i in range(5)])
            >>> for batch in store.iter_batches(batch_size=2):
            ...     print(len(batch))
            ...
            2
            2
            1

            ```
        """

    @abstractmethod
    def count(self) -> int:
        """Return the total number of documents in the store.

        Returns:
            The number of documents currently stored.
        """

    @abstractmethod
    def close(self) -> None:
        r"""Close the store and release any underlying resources (e.g.
        database connections, file handles).

        Implementations should make repeated calls to ``close()`` safe
        (i.e. idempotent), since :meth:`__exit__` calls it
        unconditionally and callers may also close a store manually
        before using it as a context manager.
        """

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()
