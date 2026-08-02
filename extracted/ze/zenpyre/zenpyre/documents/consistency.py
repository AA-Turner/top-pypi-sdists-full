r"""Provide a consistency check for LangChain document collections."""

from __future__ import annotations

__all__ = ["DocumentConsistencyError", "check_document_consistency"]

import json
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.documents import Document

logger: logging.Logger = logging.getLogger(__name__)


class DocumentConsistencyError(ValueError):
    r"""Raised when two documents share an ``id`` but have different
    ``page_content`` or ``metadata``."""


def check_document_consistency(docs: list[Document], *, raise_error: bool = False) -> bool:
    """Check that documents sharing the same ``id`` have the same
    ``page_content`` and ``metadata``.

    Documents with ``id=None`` are ignored, since ``None`` does not
    identify a single logical document. ``metadata`` is compared via a
    canonical JSON serialization (:func:`json.dumps` with
    ``sort_keys=True``), so metadata key order does not affect equality.
    This means metadata values must be JSON-serializable.

    Args:
        docs: The list of :class:`~langchain_core.documents.Document`
            instances to check.
        raise_error: If ``True``, raises :class:`DocumentConsistencyError`
            on the first inconsistency found. If ``False``, logs a
            warning for each inconsistent document and continues
            checking the rest.

    Returns:
        ``True`` if all documents are consistent, ``False`` if at least
        one inconsistency was found. Always returns ``True`` when
        ``raise_error=True``, because an inconsistency raises instead of
        returning ``False``.

    Raises:
        DocumentConsistencyError: if ``raise_error=True`` and two
            documents with the same ``id`` have different
            ``page_content`` or ``metadata``.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import check_document_consistency
        >>> docs = [
        ...     Document(id="1", page_content="A", metadata={"source": "a.txt"}),
        ...     Document(id="1", page_content="A", metadata={"source": "a.txt"}),
        ... ]
        >>> check_document_consistency(docs)
        True

        ```
    """
    seen: dict[str, tuple[str, str]] = {}
    consistent = True
    for doc in docs:
        if doc.id is None:
            continue
        value = (doc.page_content, json.dumps(doc.metadata, sort_keys=True))
        if doc.id not in seen:
            seen[doc.id] = value
            continue
        if value != seen[doc.id]:
            consistent = False
            msg = f"Inconsistent document found for id={doc.id!r}: page_content or metadata differ"
            if raise_error:
                raise DocumentConsistencyError(msg)
            logger.warning(msg)
    return consistent
