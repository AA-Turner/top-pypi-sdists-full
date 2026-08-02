r"""Provide a hashing utility for LangChain documents."""

from __future__ import annotations

__all__ = ["DocumentHasher", "hash_document", "hash_document_uuid", "hash_documents"]

import json
import uuid

from coola.hashing import (
    BaseHasher,
    HasherRegistry,
    get_default_registry,
    hash_object,
    hash_string,
)
from langchain_core.documents import Document

# Project-specific namespace for deterministic document UUIDs.
# Generated once with uuid.uuid4() and fixed here so hashes are
# stable across runs and reproducible across environments.
_NAMESPACE = uuid.UUID("21e6c43e-bc36-4f09-8e20-98201adab5df")


class DocumentHasher(BaseHasher[Document]):
    r"""Hasher for LangChain ``Document`` objects.

    This hasher delegates to ``hash_document``, which computes a hash
    from the document's ``page_content`` and ``metadata``, so two
    documents with equal content and metadata produce the same hash
    regardless of object identity.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from coola.hashing import HasherRegistry
        >>> from zenpyre.documents import DocumentHasher
        >>> registry = HasherRegistry()
        >>> hasher = DocumentHasher()
        >>> hasher
        DocumentHasher()
        >>> doc = Document(page_content="hello", metadata={"source": "test"})
        >>> len(hasher.hash(doc, registry=registry))
        64

        ```
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def hash(
        self,
        data: Document,
        registry: HasherRegistry,  # noqa: ARG002
        length: int = 64,
        ignore_unhashable: bool = False,  # noqa: ARG002
    ) -> str:
        return hash_document(data, length=length)


def hash_document(doc: Document, length: int = 64) -> str:
    """Compute a stable, reproducible hash of a LangChain document.

    Combines the document's ``page_content`` and ``metadata`` into a
    single canonical string and hashes it.  Metadata is serialised via
    :func:`json.dumps` with ``sort_keys=True`` to guarantee a
    consistent ordering regardless of the dict insertion order.

    Args:
        doc: The :class:`~langchain_core.documents.Document` to hash.
        length: The desired length of the returned hex string.  Must be
            an even number between 2 and 128 inclusive.  Defaults to
            ``64``.

    Returns:
        A lowercase hexadecimal string of exactly ``length`` characters
        that uniquely identifies the document's content and metadata.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import hash_document
        >>> doc = Document(page_content="Hello", metadata={"source": "cats.txt"})
        >>> len(hash_document(doc))
        64

        ```
    """
    content = doc.page_content + json.dumps(doc.metadata, sort_keys=True)
    return hash_string(content, length=length)


def hash_document_uuid(doc: Document) -> str:
    """Compute a stable, reproducible UUID for a LangChain document.

    Uses :func:`uuid.uuid5` (SHA-1 based) with a fixed project-specific
    namespace to derive a deterministic UUID from the document's
    ``page_content`` and ``metadata``.  Metadata is serialised via
    :func:`json.dumps` with ``sort_keys=True`` to guarantee a consistent
    ordering regardless of dict insertion order.

    The returned UUID can be assigned directly to
    :attr:`~langchain_core.documents.Document.id`, which LangChain
    expects to be a UUID string. This makes re-indexing idempotent —
    adding the same document twice with the same ID upserts rather than
    duplicates.

    Args:
        doc: The :class:`~langchain_core.documents.Document` to hash.

    Returns:
        A lowercase UUID string of the form
        ``'xxxxxxxx-xxxx-5xxx-xxxx-xxxxxxxxxxxx'``.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import hash_document_uuid
        >>> doc = Document(page_content="Hello", metadata={"source": "cats.txt"})
        >>> hash_document_uuid(doc)

        ```
    """
    content = doc.page_content + json.dumps(doc.metadata, sort_keys=True)
    return str(uuid.uuid5(_NAMESPACE, content))


def hash_documents(docs: list[Document], length: int = 64) -> str:
    """Compute a stable, reproducible hash of a list of LangChain
    documents.

    Hashes each document individually via :func:`hash_document` and
    combines the results into a single canonical string, then hashes
    that.  The order of documents matters — two lists with the same
    documents in a different order will produce different hashes.

    Args:
        docs: The list of :class:`~langchain_core.documents.Document`
            instances to hash.
        length: The desired length of the returned hex string.  Must be
            an even number between 2 and 128 inclusive.  Defaults to
            ``64``.

    Returns:
        A lowercase hexadecimal string of exactly ``length`` characters
        that uniquely identifies the list's content, metadata, and
        ordering.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import hash_documents
        >>> docs = [
        ...     Document(page_content="Hello", metadata={"source": "a.txt"}),
        ...     Document(page_content="World", metadata={"source": "b.txt"}),
        ... ]
        >>> len(hash_documents(docs))
        64

        ```
    """
    return hash_object(docs, length=length)


get_default_registry().register(Document, DocumentHasher(), exist_ok=True)
