r"""Define a processor that filters LangChain documents by a set of
metadata values."""

from __future__ import annotations

__all__ = ["FilterDocumentsByMetadataValuesProcessor"]

import logging
from typing import Any

from coola.display import InlineDisplayMixin
from langchain_core.documents import Document

from zenpyre.data_processors.base import BaseProcessor
from zenpyre.documents import filter_by_metadata_values

logger: logging.Logger = logging.getLogger(__name__)


class FilterDocumentsByMetadataValuesProcessor(
    BaseProcessor[list[Document], list[Document]], InlineDisplayMixin
):
    """Processor that filters a list of LangChain documents by checking
    if a metadata value is in a set of accepted values.

    Wraps :func:`~zenpyre.documents.filter_by_metadata_values` as a
    :class:`~zenpyre.data_processors.base.BaseProcessor` so it can be
    composed in a :class:`~zenpyre.data_processors.SequentialProcessor`
    pipeline.

    Args:
        metadata_key: The metadata key to filter by.
        values: The set of accepted values.  Documents whose
            ``metadata_key`` is in this set are kept.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.data_processors import FilterDocumentsByMetadataValuesProcessor
        >>> processor = FilterDocumentsByMetadataValuesProcessor(
        ...     metadata_key="category", values={"Science", "Technology"}
        ... )
        >>> docs = [
        ...     Document(page_content="A", metadata={"category": "Science"}),
        ...     Document(page_content="B", metadata={"category": "Cooking"}),
        ...     Document(page_content="C", metadata={"category": "Technology"}),
        ... ]
        >>> result = processor.process(docs)
        >>> sorted(doc.page_content for doc in result)
        ['A', 'C']

        ```
    """

    def __init__(self, metadata_key: str, values: set[Any]) -> None:
        self._metadata_key = metadata_key
        self._values = values

    def process(self, data: list[Document]) -> list[Document]:
        """Filter ``data`` by the configured metadata key and set of
        values.

        Args:
            data: The list of
                :class:`~langchain_core.documents.Document` instances
                to filter.

        Returns:
            A new list containing only the
            :class:`~langchain_core.documents.Document` instances whose
            ``metadata_key`` value is in ``values``.  The original list
            is not modified.
        """
        return filter_by_metadata_values(data, self._metadata_key, self._values)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"metadata_key": self._metadata_key, "values": self._values}
