import itertools
from typing import Iterable
from typing import TypeVar


T = TypeVar("T")


def batched_iterator(iterable: Iterable[T], batch_size: int) -> Iterable[Iterable[T]]:
    it = iterable.__iter__()
    if batch_size < 1:
        msg = "Batch size must be at least 1"
        raise ValueError(msg)
    while True:
        try:
            peeked = next(it)
        except StopIteration:
            return

        def batch():
            yield peeked
            yield from itertools.islice(it, batch_size - 1)

        yield batch()
