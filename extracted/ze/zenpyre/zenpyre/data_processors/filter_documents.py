r"""Define a processor that filters LangChain documents by a metadata
key."""

from __future__ import annotations

__all__ = ["FilterDocumentsByMetadataProcessor"]

import logging
from typing import Any

from coola.display import InlineDisplayMixin
from langchain_core.documents import Document

from zenpyre.data_processors.base import BaseProcessor
from zenpyre.documents import filter_by_metadata

logger: logging.Logger = logging.getLogger(__name__)


class FilterDocumentsByMetadataProcessor(
    BaseProcessor[list[Document], list[Document]], InlineDisplayMixin
):
    """Processor that filters a list of LangChain documents by the value
    of a metadata key.

    Wraps :func:`~zenpyre.documents.filter_by_metadata` as a
    :class:`~zenpyre.data_processors.base.BaseProcessor` so it can be
    composed in a :class:`~zenpyre.data_processors.SequentialProcessor`
    pipeline.

    Args:
        metadata_key: The metadata key to filter by.
        value: The value to match against.  Documents whose
            ``metadata_key`` equals this value are kept.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.data_processors import FilterDocumentsByMetadataProcessor
        >>> processor = FilterDocumentsByMetadataProcessor(metadata_key="category", value="Science")
        >>> docs = [
        ...     Document(page_content="A", metadata={"category": "Science"}),
        ...     Document(page_content="B", metadata={"category": "Cooking"}),
        ...     Document(page_content="C", metadata={"category": "Science"}),
        ... ]
        >>> result = processor.process(docs)
        >>> [doc.page_content for doc in result]
        ['A', 'C']

        ```
    """

    def __init__(self, metadata_key: str, value: Any) -> None:
        self._metadata_key = metadata_key
        self._value = value

    def process(self, data: list[Document]) -> list[Document]:
        """Filter ``data`` by the configured metadata key and value.

        Args:
            data: The list of
                :class:`~langchain_core.documents.Document` instances
                to filter.

        Returns:
            A new list containing only the
            :class:`~langchain_core.documents.Document` instances whose
            ``metadata_key`` equals ``value``.  The original list is
            not modified.
        """
        return filter_by_metadata(data, self._metadata_key, self._value)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"metadata_key": self._metadata_key, "value": self._value}
