r"""Define an ingestor that processes the output of another ingestor."""

from __future__ import annotations

__all__ = ["ProcessorIngestor"]

import logging
from typing import TYPE_CHECKING, Any, TypeVar

from coola.display import MultilineDisplayMixin

from zenpyre.ingestors.base import BaseIngestor

if TYPE_CHECKING:
    from zenpyre.data_processors.base import BaseProcessor

T = TypeVar("T")
U = TypeVar("U")

logger: logging.Logger = logging.getLogger(__name__)


class ProcessorIngestor(BaseIngestor[T], MultilineDisplayMixin):
    r"""Ingestor that applies a processor to the output of another
    ingestor.

        Wraps a source :class:`~zenpyre.ingestors.base.BaseIngestor` and a
        :class:`~zenpyre.data_processors.base.BaseProcessor`: it ingests
        data from the source, then passes it through the processor and
        returns the processed result. This makes it possible to compose
        any processor (e.g. :class:`~zenpyre.data_processors.ShuffleProcessor`)
        with any ingestor without needing a dedicated ingestor subclass for
        each processor.

        Type parameters:
            U: The type of data returned by the source ingestor, and
                accepted as input by the processor.
            T: The type of data returned by the processor, and returned by
                :meth:`ingest`.

    Args:
            source: The ingestor used to fetch the raw data.
            processor: The processor used to transform the data ingested
                from ``source``.

    Example:
    ```pycon
    >>> from zenpyre.data_processors import ShuffleProcessor
    >>> from zenpyre.ingestors import InMemoryIngestor, ProcessorIngestor
    >>> ingestor = ProcessorIngestor(
    ...     source=InMemoryIngestor(data=[1, 2, 3, 4, 5]),
    ...     processor=ShuffleProcessor(seed=42),
    ... )
    >>> sorted(ingestor.ingest())
    [1, 2, 3, 4, 5]

    ```
    """

    def __init__(self, source: BaseIngestor[U], processor: BaseProcessor[U, T]) -> None:
        self._source = source
        self._processor = processor

    def ingest(self) -> T:
        r"""Ingest data from the source ingestor and process it.

        Calls :meth:`~zenpyre.ingestors.base.BaseIngestor.ingest` on
        the source ingestor, then passes the result to
        :meth:`~zenpyre.data_processors.base.BaseProcessor.process`.

        Returns:
            The processed output, as returned by the processor.
        """
        logger.debug("Ingesting data from %s", self._source)
        data = self._source.ingest()
        logger.debug("Processing data with %s", self._processor)
        return self._processor.process(data)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        r"""Return the keyword arguments used to build the display
        representation.

        Returns:
            A dictionary containing the source ingestor and the
            processor, for use by
            :class:`~coola.display.MultilineDisplayMixin`.
        """
        return {"source": self._source, "processor": self._processor}
