r"""Define an ingestor that shuffles the output of another ingestor."""

from __future__ import annotations

__all__ = ["ShuffleIngestor"]

import logging
import random
from typing import TYPE_CHECKING, Any, TypeVar

from coola.display import MultilineDisplayMixin

from zenpyre.ingestors.base import BaseIngestor

if TYPE_CHECKING:
    from collections.abc import Sequence

T = TypeVar("T")

logger: logging.Logger = logging.getLogger(__name__)


class ShuffleIngestor(BaseIngestor[list[T]], MultilineDisplayMixin):
    r"""Ingestor that shuffles the output of another ingestor.

    Wraps a source :class:`~zenpyre.ingestors.base.BaseIngestor` and
    returns its ingested payload as a ``list`` with elements shuffled
    in random order. The source ingestor's output must be an iterable
    (e.g. ``list``, ``tuple``) whose elements can be reordered; the
    result is always materialized as a new ``list``, so the original
    sequence type of ``T`` is not preserved.

    The shuffling uses its own :class:`random.Random` instance, so it
    does not affect and is not affected by the global ``random``
    module state. Note that the internal random generator is created
    once, in ``__init__``, and its state advances with each call to
    :meth:`ingest`. This means calling ``ingest`` multiple times on
    the same instance — even with a fixed ``seed`` — will generally
    produce a *different* shuffle order each time, since each call
    consumes further random state rather than resetting it.

    Args:
        source: The ingestor whose output will be shuffled.
        seed: Seed for the internal random number generator, to make
            the shuffle order reproducible across runs. If ``None``,
            the generator is seeded unpredictably (e.g. from system
            entropy).

    Example:
        ```pycon
        >>> from zenpyre.ingestors import ShuffleIngestor, InMemoryIngestor
        >>> ingestor = ShuffleIngestor(InMemoryIngestor([1, 2, 3, 4, 5]), seed=42)
        >>> shuffled = ingestor.ingest()
        >>> sorted(shuffled)
        [1, 2, 3, 4, 5]

        ```
    """

    def __init__(self, source: BaseIngestor[Sequence[T]], *, seed: int | None = None) -> None:
        self._source = source
        self._seed = seed
        self._rng = random.Random(seed)  # noqa: S311

    def ingest(self) -> list[T]:
        r"""Ingest data from the source ingestor and shuffle it.

        Calls :meth:`~zenpyre.ingestors.base.BaseIngestor.ingest` on
        the wrapped source ingestor, converts the result to a
        ``list``, and shuffles it in place using the internal random
        generator.

        Returns:
            A new ``list`` containing the same elements as the
            source ingestor's output, in a random order.

        Raises:
            TypeError: If the source ingestor's output is not
                iterable.
        """
        logger.debug("Ingesting data from %s before shuffling", self._source)
        data = list(self._source.ingest())
        self._rng.shuffle(data)
        logger.debug("Shuffled %d items", len(data))
        return data

    def _get_repr_kwargs(self) -> dict[str, Any]:
        r"""Return the keyword arguments used to build the display
        representation.

        Returns:
            A dictionary containing the source ingestor and the seed
            used to initialize the random generator, for use by
            :class:`~coola.display.MultilineDisplayMixin`.
        """
        return {"source": self._source, "seed": self._seed}
