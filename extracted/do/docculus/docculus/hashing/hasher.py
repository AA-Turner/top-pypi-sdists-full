r"""Provide a hashing utility for LangChain documents."""

from __future__ import annotations

__all__ = ["DocumentHasher"]


from coola.hashing import (
    BaseHasher,
    HasherRegistry,
    get_default_registry,
)
from langchain_core.documents import Document

from docculus.hashing.functions import hash_document


class DocumentHasher(BaseHasher[Document]):
    r"""Hasher for LangChain ``Document`` objects.

    This hasher delegates to ``hash_document``, which computes a hash
    from the document's ``page_content`` and ``metadata``, so two
    documents with equal content and metadata produce the same hash
    regardless of object identity.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from coola.hashing import HasherRegistry
        >>> from docculus.hashing import DocumentHasher
        >>> registry = HasherRegistry()
        >>> hasher = DocumentHasher()
        >>> hasher
        DocumentHasher()
        >>> doc = Document(page_content="hello", metadata={"source": "test"})
        >>> len(hasher.hash(doc, registry=registry))
        64

        ```
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def hash(
        self,
        data: Document,
        registry: HasherRegistry,  # noqa: ARG002
        length: int = 64,
        ignore_unhashable: bool = False,  # noqa: ARG002
    ) -> str:
        return hash_document(data, length=length)


def register_document_hasher() -> None:
    r"""Register a hashing utility for LangChain ``Document``
    objects."""
    get_default_registry().register(Document, DocumentHasher(), exist_ok=True)


register_document_hasher()
