"""Iterator helpers"""

from typing import Iterable, Generator, Tuple, Any
import itertools


def chunked(iterable: Iterable[Any], size: int) -> Generator[Tuple[Any, ...], None, None]:
    """Divide iterable into chunks of size"""
    itr = iter(iterable)
    chunk = tuple(itertools.islice(itr, size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(itr, size))
