r"""Provide ID assignment utilities for LangChain document
collections."""

from __future__ import annotations

__all__ = ["generate_deterministic_id", "generate_id", "generate_random_id"]

import uuid
from typing import TYPE_CHECKING

from docculus.hashing import hash_document_to_uuid

if TYPE_CHECKING:
    from langchain_core.documents import Document


def generate_id(doc: Document, mode: str = "deterministic") -> str:
    r"""Generate a unique identifier for a document.

    Dispatches to :func:`generate_deterministic_id` or
    :func:`generate_random_id` depending on ``mode``.

    Args:
        doc: The ``langchain_core.documents.Document`` to generate an
            identifier for. Ignored when ``mode`` is ``'random'``.
        mode: The generation strategy. ``'deterministic'`` derives the
            identifier from ``doc``'s ``page_content`` and ``metadata``,
            so the same content always yields the same identifier.
            ``'random'`` generates a fresh, unrelated identifier on
            every call.

    Returns:
        A UUID string identifying the document.

    Raises:
        ValueError: If ``mode`` is not ``'deterministic'`` or
            ``'random'``.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from docculus.document import generate_id
        >>> doc = Document(page_content="Hello", metadata={"source": "cats.txt"})
        >>> len(generate_id(doc))
        36
        >>> generate_id(doc, mode="deterministic") == generate_id(doc, mode="deterministic")
        True

        ```
    """
    if mode == "deterministic":
        return generate_deterministic_id(doc)
    if mode == "random":
        return generate_random_id()
    msg = f"Invalid mode: {mode}"
    raise ValueError(msg)


def generate_random_id() -> str:
    r"""Generate a random identifier.

    Each call returns a fresh, independently random UUID, regardless
    of any document content. Use this when documents do not need
    idempotent, content-derived identifiers.

    Returns:
        A random UUID string of the form
        ``'xxxxxxxx-xxxx-4xxx-xxxx-xxxxxxxxxxxx'``.

    Example:
        ```pycon
        >>> from docculus.document import generate_random_id
        >>> len(generate_random_id())
        36
        >>> generate_random_id() == generate_random_id()
        False

        ```
    """
    return str(uuid.uuid4())


def generate_deterministic_id(doc: Document) -> str:
    r"""Generate a deterministic identifier for a document.

    The identifier is derived from ``doc``'s ``page_content`` and
    ``metadata``, so re-generating an identifier for the same content
    always returns the same value. This is useful for idempotent
    indexing: adding the same document twice yields the same ID,
    which upserts rather than duplicates.

    Args:
        doc: The ``langchain_core.documents.Document`` to generate an
            identifier for.

    Returns:
        A deterministic UUID string of the form
        ``'xxxxxxxx-xxxx-5xxx-xxxx-xxxxxxxxxxxx'``.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from docculus.document import generate_deterministic_id
        >>> doc = Document(page_content="Hello", metadata={"source": "cats.txt"})
        >>> generate_deterministic_id(doc) == generate_deterministic_id(doc)
        True

        ```
    """
    return hash_document_to_uuid(doc)
