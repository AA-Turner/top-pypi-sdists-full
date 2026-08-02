r"""Provide filtering utilities for LangChain document collections."""

from __future__ import annotations

__all__ = ["filter_by_metadata", "filter_by_metadata_range", "filter_by_metadata_values"]

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from langchain_core.documents import Document


def filter_by_metadata(
    docs: list[Document],
    metadata_key: str,
    value: Any,
) -> list[Document]:
    """Filter a list of documents by the value of a metadata key.

    Returns a new list containing only documents whose metadata
    contains ``metadata_key`` with a value equal to ``value``.
    Documents missing ``metadata_key`` are excluded.

    Args:
        docs: The list of :class:`~langchain_core.documents.Document`
            instances to filter.
        metadata_key: The metadata key to filter by.
        value: The value to match against. Documents whose
            ``metadata_key`` equals this value are kept.

    Returns:
        A new list of :class:`~langchain_core.documents.Document`
        instances whose metadata matches the filter.  The original
        list is not modified.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import filter_by_metadata
        >>> docs = [
        ...     Document(page_content="A", metadata={"category": "Science"}),
        ...     Document(page_content="B", metadata={"category": "Cooking"}),
        ...     Document(page_content="C", metadata={"category": "Science"}),
        ... ]
        >>> result = filter_by_metadata(docs, "category", "Science")
        >>> [doc.page_content for doc in result]
        ['A', 'C']

        ```
    """
    return [doc for doc in docs if doc.metadata.get(metadata_key) == value]


def filter_by_metadata_range(
    docs: list[Document],
    metadata_key: str,
    lower: Any = None,
    upper: Any = None,
) -> list[Document]:
    """Filter a list of documents by a range of values for a metadata
    key.

    Returns a new list containing only documents whose metadata contains
    ``metadata_key`` with a value within the specified range
    ``[lower, upper]`` (inclusive on both ends).  Either bound can be
    set to ``None`` to indicate no constraint on that side.  If both
    bounds are ``None``, all documents that contain ``metadata_key``
    are returned.  Documents missing ``metadata_key`` are always
    excluded.

    Args:
        docs: The list of :class:`~langchain_core.documents.Document`
            instances to filter.
        metadata_key: The metadata key to filter by.
        lower: The inclusive lower bound.  Pass ``None`` (the default)
            for no lower bound.
        upper: The inclusive upper bound.  Pass ``None`` (the default)
            for no upper bound.

    Returns:
        A new list of :class:`~langchain_core.documents.Document`
        instances whose ``metadata_key`` value falls within
        ``[lower, upper]``.  The original list is not modified.

    Raises:
        TypeError: If the metadata values are not comparable with the
            provided bounds (e.g. comparing ``str`` with ``int``).

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import filter_by_metadata_range
        >>> docs = [
        ...     Document(page_content="A", metadata={"page": 1}),
        ...     Document(page_content="B", metadata={"page": 5}),
        ...     Document(page_content="C", metadata={"page": 10}),
        ... ]
        >>> result = filter_by_metadata_range(docs, "page", lower=2, upper=8)
        >>> [doc.page_content for doc in result]
        ['B']
        >>> result = filter_by_metadata_range(docs, "page", lower=5)
        >>> [doc.page_content for doc in result]
        ['B', 'C']
        >>> result = filter_by_metadata_range(docs, "page", upper=5)
        >>> [doc.page_content for doc in result]
        ['A', 'B']

        ```
    """

    def in_range(doc: Document) -> bool:
        value = doc.metadata.get(metadata_key)
        if value is None and metadata_key not in doc.metadata:
            return False
        if lower is not None and value < lower:
            return False
        return not (upper is not None and value > upper)

    return [doc for doc in docs if in_range(doc)]


def filter_by_metadata_values(
    docs: list[Document],
    metadata_key: str,
    values: set[Any],
) -> list[Document]:
    """Filter a list of documents by checking if a metadata value is in
    a set.

    Returns a new list containing only documents whose metadata contains
    ``metadata_key`` with a value that is a member of ``values``.
    Documents missing ``metadata_key`` are excluded.

    Args:
        docs: The list of :class:`~langchain_core.documents.Document`
            instances to filter.
        metadata_key: The metadata key to filter by.
        values: The set of accepted values.  Documents whose
            ``metadata_key`` is in this set are kept.

    Returns:
        A new list of :class:`~langchain_core.documents.Document`
        instances whose ``metadata_key`` value is in ``values``.  The
        original list is not modified.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import filter_by_metadata_values
        >>> docs = [
        ...     Document(page_content="A", metadata={"category": "Science"}),
        ...     Document(page_content="B", metadata={"category": "Cooking"}),
        ...     Document(page_content="C", metadata={"category": "Technology"}),
        ...     Document(page_content="D", metadata={"category": "Science"}),
        ... ]
        >>> result = filter_by_metadata_values(docs, "category", {"Science", "Technology"})
        >>> sorted(doc.page_content for doc in result)
        ['A', 'C', 'D']

        ```
    """
    return [doc for doc in docs if doc.metadata.get(metadata_key) in values]
