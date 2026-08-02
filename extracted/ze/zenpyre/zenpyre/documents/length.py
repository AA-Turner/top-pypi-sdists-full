r"""Document content length utilities."""

from __future__ import annotations

__all__ = [
    "get_document_id_lengths",
    "get_document_length",
    "get_document_lengths",
    "get_longest_document",
    "get_shortest_document",
]

from typing import TYPE_CHECKING, Any

from zenpyre.documents.empty import is_document_empty

if TYPE_CHECKING:
    from collections.abc import Iterable

    from langchain_core.documents import Document


def get_document_length(document: Document) -> int:
    r"""Compute the number of characters in a document's
    ``page_content``.

    Args:
        document: The ``langchain_core.documents.Document`` to
            measure.

    Returns:
        The length, in characters, of ``page_content``, or ``0`` if
        ``page_content`` is not a string (e.g. ``None``).

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import get_document_length
        >>> get_document_length(Document(page_content="hello"))
        5

        ```
    """
    content = document.page_content
    return len(content) if isinstance(content, str) else 0


def get_document_lengths(documents: Iterable[Document]) -> list[int]:
    r"""Compute the number of characters in each document's
    ``page_content``.

    Args:
        documents: A list, generator, or other iterable of
            ``langchain_core.documents.Document`` objects. Consumed
            exactly once; if a generator/iterator is passed in, it will
            be exhausted by this call.

    Returns:
        A list of character counts, one per input document, in the
        same order as ``documents``. A document whose ``page_content``
        is not a string (e.g. ``None``) is treated as having a length
        of ``0``.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import get_document_lengths
        >>> docs = [
        ...     Document(id="a", page_content="hello"),
        ...     Document(id="b", page_content="hello world"),
        ... ]
        >>> get_document_lengths(docs)
        [5, 11]

        ```
    """
    return [get_document_length(doc) for doc in documents]


def get_document_id_lengths(
    documents: Iterable[Document], *, sort: bool = False
) -> list[tuple[Any, int]]:
    r"""Compute the number of characters in each document's
    ``page_content``.

    Args:
        documents: A list, generator, or other iterable of
            ``langchain_core.documents.Document`` objects. Consumed
            exactly once; if a generator/iterator is passed in, it will
            be exhausted by this call.
        sort: If ``True``, sort the output by character count, from
            shortest to longest. If ``False``, the output preserves the
            order of ``documents``.

    Returns:
        A list of ``(document_id, char_count)`` tuples, one per input
        document. A document whose ``page_content`` is not a string
        (e.g. ``None``) is treated as having a length of ``0``.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import get_document_id_lengths
        >>> docs = [
        ...     Document(id="a", page_content="hello"),
        ...     Document(id="b", page_content="hello world"),
        ... ]
        >>> get_document_id_lengths(docs)
        [('a', 5), ('b', 11)]
        >>> get_document_id_lengths(docs, sort=True)
        [('a', 5), ('b', 11)]

        ```
    """
    result = [(doc.id, get_document_length(doc)) for doc in documents]
    if sort:
        result.sort(key=lambda item: item[1])
    return result


def get_shortest_document(
    documents: Iterable[Document],
    *,
    ignore_empty: bool = False,
    treat_whitespace_as_empty: bool = False,
) -> Document | None:
    r"""Find the document with the shortest ``page_content``.

    Streams through ``documents`` one at a time and keeps only the
    current shortest document, so memory usage is O(1) regardless of
    how many documents are processed (aside from whatever the input
    iterable itself holds in memory).

    Args:
        documents: A list, generator, or other iterable of
            ``langchain_core.documents.Document`` objects. Consumed
            exactly once; if a generator/iterator is passed in, it will
            be exhausted by this call.
        ignore_empty: If ``True``, documents whose ``page_content`` is
            empty are skipped, so the shortest non-empty document is
            returned instead.
        treat_whitespace_as_empty: If ``True``, a ``page_content`` that
            contains only whitespace is also considered empty for the
            purpose of ``ignore_empty``. Has no effect if
            ``ignore_empty`` is ``False``.

    Returns:
        The first document with the smallest ``page_content`` length
        (ties broken by the earliest occurrence in ``documents``), or
        ``None`` if ``documents`` is empty or, when ``ignore_empty`` is
        ``True``, if every document is empty (or whitespace-only, when
        ``treat_whitespace_as_empty`` is also ``True``).

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import get_shortest_document
        >>> docs = [
        ...     Document(id="a", page_content="hello world"),
        ...     Document(id="b", page_content=""),
        ...     Document(id="c", page_content="hi"),
        ... ]
        >>> get_shortest_document(docs).id
        'b'
        >>> get_shortest_document(docs, ignore_empty=True).id
        'c'

        ```
    """
    shortest: Document | None = None
    shortest_length: int | None = None
    for doc in documents:
        if ignore_empty and is_document_empty(
            doc, treat_whitespace_as_empty=treat_whitespace_as_empty
        ):
            continue
        length = get_document_length(doc)
        if shortest_length is None or length < shortest_length:
            shortest, shortest_length = doc, length
    return shortest


def get_longest_document(
    documents: Iterable[Document],
    *,
    ignore_empty: bool = False,
    treat_whitespace_as_empty: bool = False,
) -> Document | None:
    r"""Find the document with the longest ``page_content``.

    Streams through ``documents`` one at a time and keeps only the
    current longest document, so memory usage is O(1) regardless of
    how many documents are processed (aside from whatever the input
    iterable itself holds in memory).

    Args:
        documents: A list, generator, or other iterable of
            ``langchain_core.documents.Document`` objects. Consumed
            exactly once; if a generator/iterator is passed in, it will
            be exhausted by this call.
        ignore_empty: If ``True``, documents whose ``page_content`` is
            empty are skipped, so the longest non-empty document is
            returned instead.
        treat_whitespace_as_empty: If ``True``, a ``page_content`` that
            contains only whitespace is also considered empty for the
            purpose of ``ignore_empty``. Has no effect if
            ``ignore_empty`` is ``False``.

    Returns:
        The first document with the largest ``page_content`` length
        (ties broken by the earliest occurrence in ``documents``), or
        ``None`` if ``documents`` is empty or, when ``ignore_empty`` is
        ``True``, if every document is empty (or whitespace-only, when
        ``treat_whitespace_as_empty`` is also ``True``).

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import get_longest_document
        >>> docs = [
        ...     Document(id="a", page_content="hello world"),
        ...     Document(id="b", page_content=""),
        ...     Document(id="c", page_content="hi"),
        ... ]
        >>> get_longest_document(docs).id
        'a'

        ```
    """
    longest: Document | None = None
    longest_length: int | None = None
    for doc in documents:
        if ignore_empty and is_document_empty(
            doc, treat_whitespace_as_empty=treat_whitespace_as_empty
        ):
            continue
        length = get_document_length(doc)
        if longest_length is None or length > longest_length:
            longest, longest_length = doc, length
    return longest
