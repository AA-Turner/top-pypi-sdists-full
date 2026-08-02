r"""Empty document detection."""

from __future__ import annotations

__all__ = ["find_empty_document_ids", "find_empty_documents"]

from typing import TYPE_CHECKING, Any

from zenpyre.documents.empty import is_document_empty

if TYPE_CHECKING:
    from collections.abc import Iterable

    from langchain_core.documents import Document


def find_empty_documents(
    documents: Iterable[Document], *, treat_whitespace_as_empty: bool = False
) -> list[Document]:
    r"""Find documents whose ``page_content`` is empty.

    Documents are consumed one at a time, so this works with generators
    or other iterables whose full contents cannot fit in memory.

    Args:
        documents: A list, generator, or other iterable of
            ``langchain_core.documents.Document`` objects. Consumed
            exactly once; if a generator/iterator is passed in, it will
            be exhausted by this call.
        treat_whitespace_as_empty: If ``True``, documents whose
            ``page_content`` contains only whitespace are also
            considered empty.

    Returns:
        The documents, in their original order, whose ``page_content``
        is the empty string (or is not a string, e.g. ``None``), and,
        if ``treat_whitespace_as_empty`` is ``True``, whose
        ``page_content`` is non-empty but contains only whitespace.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents.analysis import find_empty_documents
        >>> docs = [
        ...     Document(id="a", page_content="hello"),
        ...     Document(id="b", page_content=""),
        ... ]
        >>> find_empty_documents(docs)
        [Document(id='b', metadata={}, page_content='')]

        ```
    """
    return [
        document
        for document in documents
        if is_document_empty(document, treat_whitespace_as_empty=treat_whitespace_as_empty)
    ]


def find_empty_document_ids(
    documents: Iterable[Document], *, treat_whitespace_as_empty: bool = False
) -> list[Any]:
    r"""Find the ``id``s of documents whose ``page_content`` is empty.

    Documents are consumed one at a time, so this works with generators
    or other iterables whose full contents cannot fit in memory.

    Args:
        documents: A list, generator, or other iterable of
            ``langchain_core.documents.Document`` objects. Consumed
            exactly once; if a generator/iterator is passed in, it will
            be exhausted by this call.
        treat_whitespace_as_empty: If ``True``, documents whose
            ``page_content`` contains only whitespace are also
            considered empty.

    Returns:
        The ``id``s, in their original order, of documents whose
        ``page_content`` is the empty string (or is not a string, e.g.
        ``None``), and, if ``treat_whitespace_as_empty`` is ``True``, of
        documents whose ``page_content`` is non-empty but contains only
        whitespace.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents.analysis import find_empty_document_ids
        >>> docs = [
        ...     Document(id="a", page_content="hello"),
        ...     Document(id="b", page_content=""),
        ... ]
        >>> find_empty_document_ids(docs)
        ['b']

        ```
    """
    return [
        document.id
        for document in documents
        if is_document_empty(document, treat_whitespace_as_empty=treat_whitespace_as_empty)
    ]
