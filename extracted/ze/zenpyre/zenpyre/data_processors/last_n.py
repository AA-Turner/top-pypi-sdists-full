r"""Define a processor that returns the last n items of a sequence."""

from __future__ import annotations

__all__ = ["LastNProcessor"]

import logging
from collections.abc import Sequence
from typing import Any, TypeVar

from coola.display import InlineDisplayMixin

from zenpyre.data_processors.base import BaseProcessor

T = TypeVar("T")

logger: logging.Logger = logging.getLogger(__name__)


class LastNProcessor(BaseProcessor[Sequence[T], list[T]], InlineDisplayMixin):
    """Processor that returns the last ``n`` items from a sequence.

    Args:
        n: The maximum number of items to return.  Must be a positive
            integer.

    Raises:
        ValueError: If ``n`` is not a positive integer.

    Example:
        ```pycon
        >>> from zenpyre.data_processors import LastNProcessor
        >>> processor = LastNProcessor(n=2)
        >>> processor.process([1, 2, 3, 4, 5])
        [4, 5]
        >>> processor.process([1])
        [1]

        ```
    """

    def __init__(self, n: int) -> None:
        if n < 1:
            msg = f"n must be a positive integer, got {n}"
            raise ValueError(msg)
        self._n = n

    def process(self, data: Sequence[T]) -> list[T]:
        """Return the last ``n`` items from ``data``.

        Args:
            data: The input sequence to slice.

        Returns:
            A list containing the last ``n`` elements of ``data``, or
            all elements if ``len(data) < n``.
        """
        result = list(data[-self._n :])
        logger.info("Last n items: %s -> %s", f"{len(data):,}", f"{len(result):,}")
        return result

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"n": self._n}
