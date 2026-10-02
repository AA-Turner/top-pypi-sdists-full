r"""Provide document hashing functions."""

from __future__ import annotations

__all__ = ["hash_document", "hash_documents"]

import json
from typing import TYPE_CHECKING

from coola.hashing import hash_object, hash_string

if TYPE_CHECKING:
    from langchain_core.documents import Document


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
        >>> from docculus.hashing import hash_document
        >>> doc = Document(page_content="Hello", metadata={"source": "cats.txt"})
        >>> len(hash_document(doc))
        64

        ```
    """
    content = doc.page_content + json.dumps(doc.metadata, sort_keys=True)
    return hash_string(content, length=length)


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
        >>> from docculus.hashing import hash_documents
        >>> docs = [
        ...     Document(page_content="Hello", metadata={"source": "a.txt"}),
        ...     Document(page_content="World", metadata={"source": "b.txt"}),
        ... ]
        >>> len(hash_documents(docs))
        64

        ```
    """
    return hash_object(docs, length=length)
