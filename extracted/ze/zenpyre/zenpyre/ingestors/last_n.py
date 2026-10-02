r"""Define an ingestor that returns the last n items of another
ingestor."""

from __future__ import annotations

__all__ = ["LastNIngestor"]

import logging
from typing import TYPE_CHECKING, Any, TypeVar

from coola.display import MultilineDisplayMixin

from zenpyre.ingestors.base import BaseIngestor

if TYPE_CHECKING:
    from collections.abc import Sequence

T = TypeVar("T")

logger: logging.Logger = logging.getLogger(__name__)


class LastNIngestor(BaseIngestor[list[T]], MultilineDisplayMixin):
    """Ingestor that returns the last ``n`` items from another ingestor.

    Wraps a source :class:`~zenpyre.ingestors.BaseIngestor` that
    returns a sequence, and slices the last ``n`` elements from its
    output. If the source ingestor returns fewer than ``n`` items, all
    items are returned.

    Args:
        ingestor: The source ingestor whose output will be sliced.
            Must return a sequence.
        n: The maximum number of items to return from the end of the
            sequence. Must be a positive integer.

    Raises:
        ValueError: If ``n`` is not a positive integer.

    Example:
        ```pycon
        >>> from zenpyre.ingestors import InMemoryIngestor
        >>> ingestor = LastNIngestor(
        ...     source=InMemoryIngestor(data=[1, 2, 3, 4, 5]),
        ...     n=3,
        ... )
        >>> ingestor.ingest()
        [3, 4, 5]

        ```
    """

    def __init__(self, source: BaseIngestor[Sequence[T]], n: int) -> None:
        if n < 1:
            msg = f"n must be a positive integer, got {n}"
            raise ValueError(msg)
        self._source = source
        self._n = n

    def ingest(self) -> list[T]:
        """Return the last ``n`` items from the source ingestor.

        Returns:
            A list containing the last ``n`` elements of the source
            ingestor's output. If fewer than ``n`` items are available,
            all of them are returned.
        """
        items = list(self._source.ingest())
        result = items[-self._n :]
        logger.info(
            "Returning last %d of %d item(s) (n=%d)",
            len(result),
            len(items),
            self._n,
        )
        return result

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"source": self._source, "n": self._n}
