"""
Some utility functions for working with iterators.
"""
import heapq
from typing import Any, Callable, Iterable, Iterator, List, Tuple, TypeVar, Optional
import itertools
import more_itertools

T = TypeVar("T")
U = TypeVar("U")


def imerge(
    iterables: Iterable[Iterable[T]],
    key: Callable[[T], Any] = lambda x: x,
) -> Iterator[T]:
    """Merge individually sorted iterables to a single sorted iterator.

    This is similar to the merge step in merge-sort except

    * it handles an arbitrary number of iterators, and
    * eagerly consumes only one item from each iterator.

    If the laziness is not needed, it is probably better to concatenate and sort.

    **Sorted normally**

    >>> list(imerge([[1, 4], [2, 3]]))
    [1, 2, 3, 4]

    **Key changes order (Note that the sorted order of inputs is different)s**

    >>> list(imerge([[4, 1], [2, 3]], key=lambda x: (x%2, x)))
    [2, 4, 1, 3]
    """
    if not callable(key):
        raise TypeError("Key must be callable")

    heap: List[Tuple[Any, int, T, Iterator[T]]] = []
    for i, iterable in enumerate(iterables):
        iterator = iter(iterable)
        try:
            v = next(iterator)
        except StopIteration:
            continue
        k = key(v)
        heapq.heappush(heap, (k, i, v, iterator))

    while heap:
        k, i, v, iterator = heapq.heappop(heap)
        yield v
        try:
            v = next(iterator)
        except StopIteration:
            continue

        k = key(v)
        heapq.heappush(heap, (k, i, v, iterator))


def bucket_merge(
    iterable: Iterable[T],
    sort_key: Callable[[T], Any],
    bucket_key: Callable[[T], U],
    buckets: Iterable[U],
) -> Iterator[T]:
    """Sort a partially sorted iterable lazily

    If the iterable can be split into individually sorted buckets then this function
    will sort it.
    """
    buckets_ = set(buckets)
    iterables = more_itertools.bucket(iterable, bucket_key, lambda x: x in buckets_)
    yield from imerge((iterables[bucket] for bucket in buckets_), key=sort_key)


def split(
    iterable: Iterable[T],
    edges: Iterable[U],
    cmp: Optional[Callable[[T, U], bool]] = None,
) -> Iterator[List[T]]:
    """Yield lists of items from ``iterable`` grouped by ``edges``

    By default this function will insert a split before an item that is equal to an
    edge but this can be adjusted using ``cmp``.

    ``cmp`` can also be used if the items in ``iterable`` cannot directly be compared
    to the edges.

    The number of lists yielded is guaranteed to be ``len(edges) + 1``.

    Note that whereas :func:`more_itertools.split_before` will not yield empty buckets,
    this function will.

    >>> list(split([0, 2, 4, 6, 8], [3, 4]))
    [[0, 2], [], [4, 6, 8]]

    >>> after = lambda item, edge: item <= edge
    >>> list(split([0, 2, 4, 6, 8], [3, 4], after))
    [[0, 2], [4], [6, 8]]

    >>> list(split([2], [1, 3]))
    [[], [2], []]
    """

    def before(item, edge):
        return item < edge

    if cmp is None:
        cmp = before

    iterable = iter(iterable)
    edges = iter(edges)

    try:
        edge = next(edges)
    except StopIteration:
        yield list(iterable)
        return

    bucket: List[T] = []
    for item in iterable:
        while not cmp(item, edge):
            yield bucket
            bucket = []
            try:
                edge = next(edges)
            except StopIteration:
                bucket.append(item)
                bucket.extend(iterable)
                yield bucket
                return
        bucket.append(item)

    yield bucket
    yield []
    for _ in edges:
        yield []


def split_annotated(
    iterable: Iterable[T],
    edges: Iterable[U],
    cmp: Optional[Callable[[T, U], bool]] = None,
) -> Iterator[Tuple[Optional[U], Optional[U], List[T]]]:
    """Like :func:`split` but annotates the buckets with their edges

    >>> list(split_annotated([0, 2, 4, 6, 8], [3, 4]))
    [(None, 3, [0, 2]), (3, 4, []), (4, None, [4, 6, 8])]
    """
    teed = itertools.tee(edges, 3)
    yield from zip(
        itertools.chain([None], teed[0]),
        itertools.chain(teed[1], [None]),
        split(iterable, teed[2], cmp),
    )
