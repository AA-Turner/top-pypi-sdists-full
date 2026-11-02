"""Requests sized for the service's body limit."""

from collections.abc import Callable, Iterator, Sequence
from typing import TypeVar

ItemT = TypeVar("ItemT")


class ValueBatches:
    """Split many values into requests of at most a thousand values and about four mebibytes."""

    COUNT = 1_000
    BYTES = 4 * 1_048_576

    @staticmethod
    def split(items: Sequence[ItemT], size: Callable[[ItemT], int]) -> Iterator[list[ItemT]]:
        """Yield consecutive batches in order; a value larger than a batch still travels alone."""
        batch: list[ItemT] = []
        total = 0
        for item in items:
            weight = size(item)
            if batch and (len(batch) == ValueBatches.COUNT or total + weight > ValueBatches.BYTES):
                yield batch
                batch, total = [], 0
            batch.append(item)
            total += weight
        if batch:
            yield batch
