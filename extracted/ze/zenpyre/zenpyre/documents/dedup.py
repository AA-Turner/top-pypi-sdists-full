r"""Provide a deduplication utility for LangChain document
collections."""

from __future__ import annotations

__all__ = ["deduplicate_documents"]

import json
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.documents import Document

logger: logging.Logger = logging.getLogger(__name__)


def deduplicate_documents(docs: list[Document], log: bool = False) -> list[Document]:
    """Remove duplicate documents from a list.

    Two documents are considered duplicates only if their ``id``,
    ``page_content``, and ``metadata`` are all equal. ``metadata`` is
    compared via a canonical JSON serialization
    (:func:`json.dumps` with ``sort_keys=True``), so metadata key
    order does not affect equality. This means metadata values must
    be JSON-serializable.

    Args:
        docs: The list of :class:`~langchain_core.documents.Document`
            instances to deduplicate.
        log: If ``True``, log the initial and final number of
            documents, along with the number of duplicates removed.

    Returns:
        A new list containing the first occurrence of each unique
        ``(id, page_content, metadata)`` combination, in the original
        relative order. The input list is not modified.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import deduplicate_documents
        >>> docs = [
        ...     Document(page_content="A", metadata={"source": "a.txt"}),
        ...     Document(page_content="B", metadata={"source": "b.txt"}),
        ...     Document(page_content="A", metadata={"source": "a.txt"}),
        ... ]
        >>> result = deduplicate_documents(docs)
        >>> [doc.page_content for doc in result]
        ['A', 'B']

        ```
    """
    seen: set[tuple[str | None, str, str]] = set()
    result: list[Document] = []
    for doc in docs:
        key = (doc.id, doc.page_content, json.dumps(doc.metadata, sort_keys=True))
        if key in seen:
            continue
        seen.add(key)
        result.append(doc)
    if log:
        logger.info(
            "Deduplicated documents: %d -> %d (%d duplicate(s) removed)",
            len(docs),
            len(result),
            len(docs) - len(result),
        )
    return result
