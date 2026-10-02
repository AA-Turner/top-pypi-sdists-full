r"""Define a processor that sorts a sequence of dicts by a key's
value."""

from __future__ import annotations

__all__ = ["SortByKeyProcessor"]

import logging
from collections.abc import Sequence
from typing import Any

from coola.display import InlineDisplayMixin

from zenpyre.data_processors.base import BaseProcessor

logger: logging.Logger = logging.getLogger(__name__)


class SortByKeyProcessor(
    BaseProcessor[Sequence[dict[str, Any]], list[dict[str, Any]]], InlineDisplayMixin
):
    """Processor that sorts a sequence of dicts by the value at a given
    key.

    Args:
        key: The dict key whose value is used as the sort key.  Every
            dict in the input must contain this key, and the values
            must be mutually comparable (support ``<``).
        reverse: If ``True``, sort in descending order.  Defaults to
            ``False`` (ascending order), matching the built-in
            :func:`sorted` function.

    Raises:
        KeyError: If ``key`` is missing from a dict in the input.

    Example:
        ```pycon
        >>> from zenpyre.data_processors import SortByKeyProcessor
        >>> processor = SortByKeyProcessor(key="score")
        >>> processor.process([{"score": 3}, {"score": 1}, {"score": 2}])
        [{'score': 1}, {'score': 2}, {'score': 3}]
        >>> processor = SortByKeyProcessor(key="score", reverse=True)
        >>> processor.process([{"score": 3}, {"score": 1}, {"score": 2}])
        [{'score': 3}, {'score': 2}, {'score': 1}]

        ```
    """

    def __init__(self, key: str, *, reverse: bool = False) -> None:
        self._key = key
        self._reverse = reverse

    def process(self, data: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
        """Sort the dicts by the value at :attr:`_key`.

        Args:
            data: The sequence of dicts to sort.  Every dict must
                contain :attr:`_key`.

        Returns:
            A new list of dicts sorted by the value at :attr:`_key`,
            in ascending order, or descending order if
            ``reverse=True``.

        Raises:
            KeyError: If :attr:`_key` is missing from a dict.
        """
        result = sorted(data, key=lambda item: item[self._key], reverse=self._reverse)
        logger.info(
            "Sorted %s item(s) by key %r (reverse=%s)",
            f"{len(result):,}",
            self._key,
            self._reverse,
        )
        return result

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"key": self._key, "reverse": self._reverse}
