r"""Duplicate document detection."""

from __future__ import annotations

__all__ = ["find_duplicate_content_document_ids"]

import hashlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterable

    from langchain_core.documents import Document


def find_duplicate_content_document_ids(documents: Iterable[Document]) -> list[list[Any]]:
    r"""Group document ids that share exactly the same ``page_content``.

    Documents are consumed one at a time, so this works with generators
    or other iterables whose full contents cannot fit in memory. Only a
    hash of each document's content is retained (rather than the full
    content itself), making this more memory-efficient for large
    corpora.

    Args:
        documents: A list, generator, or other iterable of
            ``langchain_core.documents.Document`` objects. Consumed
            exactly once; if a generator/iterator is passed in, it will
            be exhausted by this call.

    Returns:
        A list of groups of document ``id``s whose ``page_content`` is
        identical. Each group contains two or more ids, in the order
        their documents were encountered; groups are in the order their
        first member was encountered. Documents with unique content are
        not included in the result.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents.analysis import find_duplicate_content_document_ids
        >>> docs = [
        ...     Document(id="a", page_content="hello"),
        ...     Document(id="b", page_content="hello"),
        ...     Document(id="c", page_content="world"),
        ... ]
        >>> find_duplicate_content_document_ids(docs)
        [['a', 'b']]

        ```
    """
    groups: dict[bytes, list[Any]] = {}
    for document in documents:
        content = document.page_content
        content_hash = hashlib.sha256(content.encode("utf-8", errors="ignore")).digest()
        groups.setdefault(content_hash, []).append(document.id)
    return [group for group in groups.values() if len(group) > 1]
