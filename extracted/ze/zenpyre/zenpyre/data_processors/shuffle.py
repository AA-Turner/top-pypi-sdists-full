r"""Define a processor that shuffles the items of a sequence."""

from __future__ import annotations

__all__ = ["ShuffleProcessor"]

import logging
import random
from collections.abc import Sequence
from typing import Any, TypeVar

from coola.display import MultilineDisplayMixin

from zenpyre.data_processors.base import BaseProcessor

T = TypeVar("T")

logger: logging.Logger = logging.getLogger(__name__)


class ShuffleProcessor(BaseProcessor[Sequence[T], list[T]], MultilineDisplayMixin):
    r"""Processor that shuffles the items of a sequence.

        Takes an iterable (e.g. ``list``, ``tuple``) as input and returns
        a new ``list`` with the same elements in random order. The result
        is always materialized as a new ``list``, so the original sequence
        type of the input is not preserved.

        The shuffling uses its own :class:`random.Random` instance, so it
        does not affect and is not affected by the global ``random``
        module state. Note that the internal random generator is created
        once, in ``__init__``, and its state advances with each call to
        :meth:`process`. This means calling ``process`` multiple times on
        the same instance — even with a fixed ``seed`` — will generally
        produce a *different* shuffle order each time, since each call
        consumes further random state rather than resetting it.

    Args:
            seed: Seed for the internal random number generator, to make
                the shuffle order reproducible across runs. If ``None``,
                the generator is seeded unpredictably (e.g. from system
                entropy).

    Example:
    ```pycon
    >>> from zenpyre.data_processors import ShuffleProcessor
    >>> processor = ShuffleProcessor(seed=42)
    >>> shuffled = processor.process([1, 2, 3, 4, 5])
    >>> sorted(shuffled)
    [1, 2, 3, 4, 5]

    ```
    """

    def __init__(self, *, seed: int | None = None) -> None:
        self._seed = seed
        self._rng = random.Random(seed)  # noqa: S311

    def process(self, data: Sequence[T]) -> list[T]:
        r"""Shuffle the items of the input sequence.

        Converts the input to a ``list`` and shuffles it in place
        using the internal random generator.

        Args:
            data: The sequence to shuffle. Can be any iterable (e.g.
                ``list``, ``tuple``).

        Returns:
            A new ``list`` containing the same elements as ``data``,
            in a random order.

        Raises:
            TypeError: If ``data`` is not iterable.
        """
        logger.debug("Shuffling data")
        items = list(data)
        self._rng.shuffle(items)
        logger.debug("Shuffled %d items", len(items))
        return items

    def _get_repr_kwargs(self) -> dict[str, Any]:
        r"""Return the keyword arguments used to build the display
        representation.

        Returns:
            A dictionary containing the seed used to initialize the
            random generator, for use by
            :class:`~coola.display.MultilineDisplayMixin`.
        """
        return {"seed": self._seed}
