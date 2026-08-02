r"""Provide sorting utilities for LangChain document collections."""

from __future__ import annotations

__all__ = ["sort_by_metadata"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.documents import Document


def sort_by_metadata(
    docs: list[Document],
    metadata_key: str,
    *,
    keep_missing: bool = True,
    reverse: bool = False,
) -> list[Document]:
    """Sort a list of documents by the value of a metadata key.

    Documents are sorted in ascending order by the value of
    ``metadata_key`` by default, or descending order if
    ``reverse=True``.  Documents that do not contain ``metadata_key``
    in their metadata are placed at the end of the result by default,
    or removed entirely if ``keep_missing=False``.

    Args:
        docs: The list of :class:`~langchain_core.documents.Document`
            instances to sort.
        metadata_key: The metadata key to sort by.
        keep_missing: If ``True`` (the default), documents without
            ``metadata_key`` in their metadata are kept and placed at
            the end of the result.  If ``False``, they are excluded
            from the result entirely.
        reverse: If ``True``, the result is sorted in descending order.
            Defaults to ``False``, matching the behaviour of
            :func:`sorted`.

    Returns:
        A new sorted list of :class:`~langchain_core.documents.Document`
        instances.  The original list is not modified.

    Raises:
        TypeError: If the metadata values for ``metadata_key`` are not
            mutually comparable (e.g. mixing ``str`` and ``int``).

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import sort_by_metadata
        >>> docs = [
        ...     Document(page_content="B", metadata={"source": "b.txt"}),
        ...     Document(page_content="A", metadata={"source": "a.txt"}),
        ...     Document(page_content="C"),
        ... ]
        >>> sorted_docs = sort_by_metadata(docs, "source")
        >>> [doc.metadata.get("source") for doc in sorted_docs]
        ['a.txt', 'b.txt', None]
        >>> sorted_docs = sort_by_metadata(docs, "source", reverse=True)
        >>> [doc.metadata.get("source") for doc in sorted_docs]
        ['b.txt', 'a.txt', None]
        >>> sorted_docs = sort_by_metadata(docs, "source", keep_missing=False)
        >>> [doc.metadata.get("source") for doc in sorted_docs]
        ['a.txt', 'b.txt']

        ```
    """
    missing = object()

    def sort_key(doc: Document) -> tuple:
        value = doc.metadata.get(metadata_key, missing)
        return (value is missing, value if value is not missing else None)

    if not keep_missing:
        docs = [doc for doc in docs if metadata_key in doc.metadata]

    present = [doc for doc in docs if metadata_key in doc.metadata]
    missing = [doc for doc in docs if metadata_key not in doc.metadata]
    return sorted(present, key=sort_key, reverse=reverse) + missing
