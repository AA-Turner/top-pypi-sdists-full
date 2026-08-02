r"""Provide ID assignment utilities for LangChain document
collections."""

from __future__ import annotations

__all__ = ["assign_ids", "copy_ids_to_metadata"]

from typing import TYPE_CHECKING

from zenpyre.documents import hash_document_uuid

if TYPE_CHECKING:
    from langchain_core.documents import Document


def assign_ids(docs: list[Document], *, force: bool = False) -> list[Document]:
    """Assign a stable UUID to each document that does not already have
    one.

    Iterates over ``docs`` and sets :attr:`~langchain_core.documents.Document.id`
    on any document whose ``id`` is ``None``, using
    :func:`~zenpyre.documents.hash_document_uuid` to derive a
    deterministic UUID from the document's content and metadata.
    Documents that already have an ID are left unchanged unless
    ``force=True``.

    .. note::
        This function mutates the documents in place and also returns
        the same list, allowing it to be used inline.

    Args:
        docs: The list of :class:`~langchain_core.documents.Document`
            instances to assign IDs to.
        force: If ``True``, recomputes and overwrites the ID for every
            document, even those that already have one.  Defaults to
            ``False``.

    Returns:
        The same list of :class:`~langchain_core.documents.Document`
        instances, with ``id`` set on any document that previously had
        ``id=None``, or on all documents if ``force=True``.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import assign_ids
        >>> docs = [
        ...     Document(page_content="Hello"),
        ...     Document(page_content="World", id="existing-id"),
        ... ]
        >>> docs = assign_ids(docs)
        >>> docs[0].id is not None
        True
        >>> docs[1].id
        'existing-id'
        >>> docs = assign_ids(docs, force=True)
        >>> docs[1].id != "existing-id"
        True

        ```
    """
    for doc in docs:
        if force or doc.id is None:
            doc.id = hash_document_uuid(doc)
    return docs


def copy_ids_to_metadata(
    documents: list[Document],
    metadata_key: str = "source_id",
) -> list[Document]:
    """Copy each document's `id` into its metadata under `metadata_key`.

    Text splitters generally copy a parent document's metadata onto every
    chunk they produce, but they do not preserve the parent's `id` (each
    chunk gets its own, usually `None` unless assigned later). Storing the
    parent id in metadata before splitting means every resulting chunk
    retains a reference back to the document it came from, under
    `chunk.metadata[metadata_key]`.

    Documents are mutated in place and the same list is returned. Documents
    whose `id` is `None` are left untouched, so no key is added for them.

    Args:
        documents: The documents to tag. Mutated in place.
        metadata_key: The metadata key to store the id under. Defaults to
            "source_id".

    Returns:
        The same list of documents that was passed in.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import copy_ids_to_metadata
        >>> docs = [Document(page_content="Hello", id="doc-1")]
        >>> copy_ids_to_metadata(docs)
        >>> docs[0].metadata["source_id"]
        'doc-1'

        ```
    """
    for doc in documents:
        if doc.id is not None:
            doc.metadata[metadata_key] = doc.id
    return documents
