r"""Define a processor that sorts LangChain documents by a metadata
key."""

from __future__ import annotations

__all__ = ["SortDocumentsByMetadataProcessor"]

import logging
from typing import Any

from coola.display import InlineDisplayMixin
from langchain_core.documents import Document

from zenpyre.data_processors.base import BaseProcessor
from zenpyre.documents import sort_by_metadata

logger: logging.Logger = logging.getLogger(__name__)


class SortDocumentsByMetadataProcessor(
    BaseProcessor[list[Document], list[Document]], InlineDisplayMixin
):
    """Processor that sorts a list of LangChain documents by the value
    of a metadata key.

    Wraps :func:`~zenpyre.documents.sort_by_metadata` as a
    :class:`~zenpyre.data_processors.base.BaseProcessor` so it can be
    composed in a :class:`~zenpyre.data_processors.SequentialProcessor`
    pipeline.

    Args:
        metadata_key: The metadata key to sort by.
        keep_missing: If ``True`` (the default), documents without
            ``metadata_key`` are kept and placed at the end of the
            result.  If ``False``, they are excluded entirely.
        reverse: If ``True``, the result is sorted in descending order.
            Defaults to ``False``.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.data_processors import SortDocumentsByMetadataProcessor
        >>> processor = SortDocumentsByMetadataProcessor(metadata_key="source")
        >>> docs = [
        ...     Document(page_content="B", metadata={"source": "b.txt"}),
        ...     Document(page_content="A", metadata={"source": "a.txt"}),
        ... ]
        >>> result = processor.process(docs)
        >>> [doc.metadata["source"] for doc in result]
        ['a.txt', 'b.txt']

        ```
    """

    def __init__(
        self,
        metadata_key: str,
        *,
        keep_missing: bool = True,
        reverse: bool = False,
    ) -> None:
        self._metadata_key = metadata_key
        self._keep_missing = keep_missing
        self._reverse = reverse

    def process(self, data: list[Document]) -> list[Document]:
        """Sort ``data`` by the configured metadata key and return the
        result.

        Args:
            data: The list of
                :class:`~langchain_core.documents.Document` instances
                to sort.

        Returns:
            A new sorted list of
            :class:`~langchain_core.documents.Document` instances.
            The original list is not modified.
        """
        return sort_by_metadata(
            data,
            self._metadata_key,
            keep_missing=self._keep_missing,
            reverse=self._reverse,
        )

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {
            "metadata_key": self._metadata_key,
            "keep_missing": self._keep_missing,
            "reverse": self._reverse,
        }
