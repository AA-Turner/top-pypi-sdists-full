r"""Provide a document loader backed by an in-memory list of
documents."""

from __future__ import annotations

__all__ = ["DocumentListLoader"]


from typing import TYPE_CHECKING

from langchain_core.document_loaders import BaseLoader

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence

    from langchain_core.documents import Document


class DocumentListLoader(BaseLoader):
    """A loader that yields documents from a pre-built sequence.

    Use this when documents are already in memory and you need to wrap
    them in a :class:`~langchain_core.document_loaders.BaseLoader`
    interface — for example, in tests or when constructing a pipeline
    that expects a factory.

    Args:
        documents: A sequence of
            :class:`~langchain_core.documents.Document` instances to
            yield from :meth:`lazy_load`.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.document_loaders import DocumentListLoader
        >>> loader = DocumentListLoader(
        ...     [Document(page_content="Hello"), Document(page_content="World")]
        ... )
        >>> docs = loader.load()

        ```
    """

    def __init__(self, documents: Sequence[Document]) -> None:
        self._documents = documents

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(num_docs={len(self._documents):,})"

    def lazy_load(self) -> Iterator[Document]:
        yield from self._documents
