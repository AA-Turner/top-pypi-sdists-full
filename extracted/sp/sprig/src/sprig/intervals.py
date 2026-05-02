"""Utilities for working with intervals."""
import itertools
from typing import (
    Any,
    Collection,
    Dict,
    FrozenSet,
    Hashable,
    Iterable,
    Iterator,
    List,
    Mapping,
    Sequence,
    Set,
    Tuple,
    TypeVar,
)

from typing_extensions import Literal, Protocol

End = Literal["L", "R"]


class SupportsLessThan(Protocol):
    # pylint: disable=too-few-public-methods
    def __lt__(self, __other: Any) -> bool:
        ...


SupportsLessThanT = TypeVar("SupportsLessThanT", bound=SupportsLessThan)
HashableT = TypeVar("HashableT", bound=Hashable)
T = TypeVar("T")

_LEFT = "L"
_RIGHT = "R"


def _subsets(items: Collection[T]) -> Iterator[Tuple[T, ...]]:
    """Iterate over all possible subsets of `items`.

    The order in which subsets appear is not guaranteed.

    >>> sorted(_subsets([0]))
    [(0,)]
    >>> sorted(_subsets([0, 1]))
    [(0,), (0, 1), (1,)]

    >>> sorted(_subsets([0, 1, 2]))
    [(0,), (0, 1), (0, 1, 2), (0, 2), (1,), (1, 2), (2,)]
    """
    return itertools.chain.from_iterable(
        itertools.combinations(items, i + 1) for i in range(len(items))
    )


def _intersection(
    intervals: Iterable[Tuple[SupportsLessThanT, SupportsLessThanT]]
) -> Tuple[SupportsLessThanT, SupportsLessThanT]:
    """Return the biggest interval that is a subset of all given intervals

    >>> _intersection([(10,60), (40, 90)])
    (40, 60)
    >>> _intersection([(10,60), (40, 90), (45, 55)])
    (45, 55)
    """
    lefts, rights = zip(*intervals)
    left = max(lefts)
    right = min(rights)
    # TODO: Consider raising on degenerate
    return left, right


def _endpoints(
    intervals: Iterable[Tuple[HashableT, Tuple[SupportsLessThanT, SupportsLessThanT]]]
) -> Iterator[Tuple[SupportsLessThanT, int, HashableT, End]]:
    for tie_breaker, (key, (left, right)) in enumerate(intervals):
        yield left, tie_breaker, key, "L"
        yield right, tie_breaker, key, "R"


def _intervals(
    endpoints: Iterable[Tuple[SupportsLessThanT, int, HashableT, End]]
) -> Iterator[Tuple[HashableT, Tuple[SupportsLessThanT, SupportsLessThanT]]]:
    active = {}
    for when, _, key, side in endpoints:
        if side is _LEFT:
            active[key] = when
        else:
            yield key, (active.pop(key), when)


def _intersecting_subsets(
    endpoints: Iterable[Tuple[SupportsLessThanT, int, HashableT, End]]
) -> Iterator[Tuple[SupportsLessThanT, int, FrozenSet[HashableT], End]]:
    active: Dict[HashableT, SupportsLessThanT] = {}
    for when, tie_breaker, key, side in endpoints:
        if side is _RIGHT:
            del active[key]

        yield when, tie_breaker, frozenset([key]), side
        for keys in _subsets(active):
            yield when, tie_breaker, frozenset((key,) + keys), side

        if side is _LEFT:
            active[key] = when


def intersecting_subsets(
    intervals: Mapping[HashableT, Tuple[SupportsLessThanT, SupportsLessThanT]]
) -> Dict[FrozenSet[HashableT], Tuple[SupportsLessThanT, SupportsLessThanT]]:
    """All intervals formed by reducing subsets with intersection

    In no particular order.
    """
    items = intervals.items()
    input_endpoints = sorted(_endpoints(items))
    output_endpoints = _intersecting_subsets(input_endpoints)
    return dict(_intervals(output_endpoints))


def _intersecting_combinations(
    endpoints: Iterable[Tuple[SupportsLessThanT, int, HashableT, End]], k: int
) -> Iterator[Tuple[SupportsLessThanT, int, FrozenSet[HashableT], End]]:
    active: Dict[HashableT, SupportsLessThanT] = {}
    for when, tie_breaker, key, side in endpoints:
        if side is _RIGHT:
            del active[key]

        for keys in itertools.combinations(active, k - 1):
            yield when, tie_breaker, frozenset((key,) + keys), side

        if side is _LEFT:
            active[key] = when


def intersecting_combinations(
    intervals: Mapping[HashableT, Tuple[SupportsLessThanT, SupportsLessThanT]], k: int
) -> Dict[FrozenSet[HashableT], Tuple[SupportsLessThanT, SupportsLessThanT]]:
    """All intervals formed by reducing k-combinations with intersection

    In no particular order.
    """
    items = intervals.items()
    input_endpoints = sorted(_endpoints(items))
    output_endpoints = _intersecting_combinations(input_endpoints, k)
    return dict(_intervals(output_endpoints))


def _intersecting_products(
    factored_endpoints: Iterable[
        Tuple[SupportsLessThanT, int, Tuple[int, HashableT], End]
    ],
    num_factor: int,
) -> Iterator[Tuple[SupportsLessThanT, int, Tuple[HashableT, ...], End]]:
    active: List[Set[HashableT]] = [set() for _ in range(num_factor)]
    for when, tie_breaker, (factor_num, key), side in factored_endpoints:
        if side is _LEFT:
            active[factor_num].add(key)

        tmp = active[:]
        tmp[factor_num] = {key}
        for keys in itertools.product(*tmp):
            yield when, tie_breaker, keys, side

        if side is _RIGHT:
            active[factor_num].remove(key)


def intersecting_products(
    factors: Sequence[Mapping[HashableT, Tuple[SupportsLessThanT, SupportsLessThanT]]]
) -> Mapping[Sequence[HashableT], Tuple[SupportsLessThanT, SupportsLessThanT]]:
    """All intervals formed by reducing products with intersection.

    In other words every interval that can be formed by intersecting exactly one
    interval from each of the `factors`.

    >>> intersecting_products([{0: (1, 7)}, {1:(3, 9)}, {2: (0, 2), 3: (0,4)}])
    {(0, 1, 3): (3, 4)}

    Note that the time complexity worse if intervals within a factor may intersect.
    It is potentially much worse if a large portion of the intervals do intersect.

    """
    items = [
        ((factor_num, key), (left, right))
        for factor_num, factor in enumerate(factors)
        for key, (left, right) in factor.items()
    ]
    input_endpoints = sorted(_endpoints(items))
    output_endpoints = _intersecting_products(input_endpoints, len(factors))
    return dict(_intervals(output_endpoints))


def auto_intersections(
    intervals: Mapping[HashableT, Tuple[SupportsLessThanT, SupportsLessThanT]]
) -> Dict[FrozenSet[HashableT], Tuple[SupportsLessThanT, SupportsLessThanT]]:
    """All intervals formed by intersecting two of the given intervals

    >>> auto_intersections({0:(0,3), 1:(5,6), 2:(2,4)})
    {frozenset({0, 2}): (2, 3)}
    """
    return intersecting_combinations(intervals, 2)


def without_degenerate(
    intervals: Mapping[HashableT, Tuple[SupportsLessThanT, SupportsLessThanT]],
) -> Dict[HashableT, Tuple[SupportsLessThanT, SupportsLessThanT]]:
    """Return only proper intervals

    >>> without_degenerate({0:(1,1), 1:(2,3)})
    {1: (2, 3)}
    """
    return {
        key: (left, right) for key, (left, right) in intervals.items() if left < right
    }
