r"""Provide a hashing utility for LangChain documents."""

from __future__ import annotations

__all__ = ["hash_document_to_uuid"]

import json
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.documents import Document

# Project-specific namespace for deterministic document UUIDs.
# Generated once with uuid.uuid4() and fixed here so hashes are
# stable across runs and reproducible across environments.
_NAMESPACE = uuid.UUID("21e6c43e-bc36-4f09-8e20-98201adab5df")


def hash_document_to_uuid(doc: Document) -> str:
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
        >>> from docculus.hashing import hash_document_to_uuid
        >>> doc = Document(page_content="Hello", metadata={"source": "cats.txt"})
        >>> len(hash_document_to_uuid(doc))
        36

        ```
    """
    content = doc.page_content + json.dumps(doc.metadata, sort_keys=True)
    return str(uuid.uuid5(_NAMESPACE, content))
