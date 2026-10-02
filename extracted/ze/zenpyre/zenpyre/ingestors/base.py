r"""Define the abstract interface for data ingestors."""

from __future__ import annotations

__all__ = ["BaseIngestor"]

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseIngestor(ABC, Generic[T]):
    """Abstract base class for data ingestors.

    A generic base for any component that ingests data — reads it from
    a source, transforms it, writes it to a store, or any combination
    thereof.  Works with any payload type ``T``, including
    :class:`~langchain_core.documents.Document` objects, plain strings,
    dataclasses, or ``None`` (for ingestors that write to a store and
    return nothing).

    The contract intentionally leaves the source, transport, and schema
    to the concrete implementation.  Subclasses must implement
    :meth:`ingest`.

    Example:
        ```pycon
        >>> from zenpyre.ingestors import BaseIngestor
        >>> from langchain_core.documents import Document
        >>> class MyDocumentIngestor(BaseIngestor[list[Document]]):
        ...     def ingest(self) -> list[Document]:
        ...         return [Document(page_content="Hello")]
        ...
        >>> ingestor = MyDocumentIngestor()
        >>> docs = ingestor.ingest()

        ```
    """

    @abstractmethod
    def ingest(self) -> T:
        """Ingest data from the configured source.

        Depending on the implementation, this may read from a file,
        database, API, or any other source, optionally transform the
        data, and return it or write it to a destination store.

        Returns:
            The ingested payload.  Its type and structure are defined
            by the concrete implementation.  May be ``None`` for
            ingestors that write to a store as a side effect.
        """
