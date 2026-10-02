r"""Provide utilities for truncating document content."""

from __future__ import annotations

__all__ = ["truncate_documents"]

from typing import TYPE_CHECKING

from langchain_core.documents import Document

if TYPE_CHECKING:
    from collections.abc import Iterable


def truncate_documents(
    documents: Iterable[Document],
    max_length: int,
    *,
    suffix: str = "",
) -> list[Document]:
    r"""Truncate each document's ``page_content`` to at most
    ``max_length`` characters.

    Args:
        documents: A list, generator, or other iterable of
            ``langchain_core.documents.Document`` objects. Consumed
            exactly once; if a generator/iterator is passed in, it will
            be exhausted by this call.
        max_length: The maximum number of characters to keep in each
            document's ``page_content``, including ``suffix`` when it
            is applied.
        suffix: A string appended to the truncated content when a
            document is actually truncated (documents that already fit
            within ``max_length`` are left unchanged). The total length
            of the result, including ``suffix``, never exceeds
            ``max_length``. Defaults to ``""``.

    Returns:
        A new list of ``Document`` instances with truncated
        ``page_content``, preserving each document's ``id`` and
        ``metadata``. The input documents are not modified. A document
        whose ``page_content`` is not a string (e.g. ``None``) is
        treated as having empty content.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from docculus.transform import truncate_documents
        >>> docs = [Document(page_content="hello world")]
        >>> result = truncate_documents(docs, max_length=8, suffix="...")
        >>> result[0].page_content
        'hello...'

        ```
    """
    truncated = []
    for doc in documents:
        content = doc.page_content if isinstance(doc.page_content, str) else ""
        if len(content) > max_length:
            keep = max(max_length - len(suffix), 0)
            content = content[:keep] + suffix
        truncated.append(Document(id=doc.id, page_content=content, metadata=doc.metadata))
    return truncated
