r"""Define a processor that filters LangChain documents by a metadata
range."""

from __future__ import annotations

__all__ = ["FilterDocumentsByMetadataRangeProcessor"]

import logging
from typing import Any

from coola.display import InlineDisplayMixin
from langchain_core.documents import Document

from zenpyre.data_processors.base import BaseProcessor
from zenpyre.documents import filter_by_metadata_range

logger: logging.Logger = logging.getLogger(__name__)


class FilterDocumentsByMetadataRangeProcessor(
    BaseProcessor[list[Document], list[Document]], InlineDisplayMixin
):
    """Processor that filters a list of LangChain documents by a range
    of values for a metadata key.

    Wraps :func:`~zenpyre.documents.filter_by_metadata_range` as a
    :class:`~zenpyre.data_processors.base.BaseProcessor` so it can be
    composed in a :class:`~zenpyre.data_processors.SequentialProcessor`
    pipeline.

    Args:
        metadata_key: The metadata key to filter by.
        lower: The inclusive lower bound.  Pass ``None`` (the default)
            for no lower bound.
        upper: The inclusive upper bound.  Pass ``None`` (the default)
            for no upper bound.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.data_processors import FilterDocumentsByMetadataRangeProcessor
        >>> processor = FilterDocumentsByMetadataRangeProcessor(
        ...     metadata_key="page", lower=2, upper=4
        ... )
        >>> docs = [
        ...     Document(page_content="A", metadata={"page": 1}),
        ...     Document(page_content="B", metadata={"page": 3}),
        ...     Document(page_content="C", metadata={"page": 5}),
        ... ]
        >>> result = processor.process(docs)
        >>> [doc.page_content for doc in result]
        ['B']

        ```
    """

    def __init__(
        self,
        metadata_key: str,
        lower: Any = None,
        upper: Any = None,
    ) -> None:
        self._metadata_key = metadata_key
        self._lower = lower
        self._upper = upper

    def process(self, data: list[Document]) -> list[Document]:
        """Filter ``data`` by the configured metadata key and range.

        Args:
            data: The list of
                :class:`~langchain_core.documents.Document` instances
                to filter.

        Returns:
            A new list containing only the
            :class:`~langchain_core.documents.Document` instances whose
            ``metadata_key`` value falls within ``[lower, upper]``.
            The original list is not modified.
        """
        return filter_by_metadata_range(data, self._metadata_key, self._lower, self._upper)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {
            "metadata_key": self._metadata_key,
            "lower": self._lower,
            "upper": self._upper,
        }
