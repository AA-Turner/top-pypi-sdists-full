"""
A collection of utils for doing combinatorics.
"""
import bisect
import collections
import functools
import itertools
import math
import operator
from typing import (
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Tuple,
    TypeVar,
    Union,
    overload,
)


def comb(n: int, k: int) -> int:
    """Compute binomial coefficient n choose k"""
    if not 0 <= k <= n:
        return 0

    k = min(k, n - k)
    numerator = functools.reduce(operator.mul, range(n, n - k, -1), 1)
    denominator = functools.reduce(operator.mul, range(1, k + 1), 1)
    return numerator // denominator


T = TypeVar("T")


class IntervalCache(Generic[T]):
    def __init__(self):
        self._data: List[Tuple[Tuple[float, float], T]] = []

    def get(self, item: float) -> T:
        i = bisect.bisect(self._data, ((item, math.inf),))
        (_, lower), result = self._data[i]
        if item < lower:
            raise LookupError
        return result

    def set(self, lower: float, upper: float, value: T) -> None:
        record = (upper, lower), value
        i = bisect.bisect(self._data, record)
        if i and self._data[i - 1] == record:
            return
        self._data.insert(i, record)


class Combinations(Generic[T]):
    """
    Create an object that represent a collection of combinations.

    Useful for slicing or sampling from series too long to iterate over with
    `itertools.combinations`.
    """

    def __init__(self, s: Iterable[T], k: int) -> None:
        """
        Return a sequence of all k-combinations from the collection s.
        The sequence is consistent with itertools.combinations but can be
        accessed randomly at near-constant time.
        """
        self._s = list(s)
        self._n = len(self._s)
        self._k = k
        self._len = int(comb(self._n, self._k))

    def __len__(self) -> int:
        return self._len

    def __str__(self) -> str:
        if self._len == 0:
            return "Combinations({n}, {k}) = ()".format(n=self._n, k=self._k)

        if self._len == 1:
            return "Combinations({n}, {k}) = ({first})".format(
                n=self._n, k=self._k, first=self[0]
            )

        if self._len == 2:
            return "Combinations({n}, {k}) = ({first}, {last})".format(
                n=self._n, k=self._k, first=self[0], last=self[-1]
            )

        return "Combinations({n}, {k}) = ({first}, ..., {last})".format(
            n=self._n, k=self._k, first=self[0], last=self[-1]
        )

    def __iter__(self) -> Iterator[Tuple[T, ...]]:
        yield from itertools.combinations(self._s, self._k)

    @overload
    def __getitem__(self, index: int) -> Tuple[T, ...]:
        ...

    @overload
    def __getitem__(self, index: slice) -> Iterable[Tuple[T, ...]]:
        ...

    def __getitem__(
        self,
        index: Union[int, slice],
    ) -> Union[Tuple[T, ...], Iterable[Tuple[T, ...]]]:
        """
        Get the index'th combination in lexicographical order.

        >>> Combinations(range(5), 3)[0]
        (0, 1, 2)

        >>> Combinations(range(5), 3)[5]
        (0, 3, 4)

        >>> Combinations(range(5), 3)[0:6]
        [(0, 1, 2), (0, 1, 3), (0, 1, 4), (0, 2, 3), (0, 2, 4), (0, 3, 4)]
        """

        # If asked to return a slice, return a list of all indices included in slice
        if isinstance(index, slice):
            return [self[i] for i in range(*index.indices(self._len))]  # type: ignore

        # Allow negative indexing from the end of the sequence
        if index < 0:
            index += self._len

        if not 0 <= index < self._len:
            raise IndexError(
                "Index {index} out of bounds for {self}. "
                "Must be in range [{start}, {end}].".format(
                    index=index, self=self, start=-self._len, end=self._len - 1
                )
            )

        # Compute the combinadic of the complement of the index
        combinadic = self.gen_combinadic(self._len - 1 - index)

        # Convert the combinadic (descending order) to a combination (ascending order)
        return tuple(self._s[self._n - 1 - i] for i in combinadic)

    def __contains__(self, selection: Tuple[T, ...]) -> bool:
        # A selection is a k-combination of a collection iff it contains k
        # elements ...
        subset = collections.Counter(selection)
        if sum(subset.values()) != self._k:
            return False
        # ... and it is a subset of the collection.
        superset = collections.Counter(self._s)
        return all(subset[k] <= superset[k] for k in subset)

    def gen_combinadic(self, index: int) -> Iterator[int]:
        """
        Compute the index'th combinadic.

        e.g. 4 = 4 choose 3 + 1 choose 2 + 0 choose 1, thus

        >>> tuple(Combinations(range(5), 3).gen_combinadic(4))
        (4, 1, 0)
        """

        n = self._n

        for k in range(self._k, 0, -1):
            n, nck = Combinations.max_n_choose_k_below_limit(n, k, index)
            index -= nck
            yield n

    caches: Dict[int, IntervalCache[Tuple[int, int]]] = collections.defaultdict(
        IntervalCache
    )

    @staticmethod
    def max_n_choose_k_below_limit(
        n: int,
        k: int,
        limit: int,
    ) -> Tuple[int, int]:
        """
        Compute the largest n s.t. n choose k < limit.
        Return also the corresponding value of n choose k for optimization.

        e.g. 5 choose 3 = 10 > 5 but 4 choose 3 = 4 < 5, thus

        >>> Combinations.max_n_choose_k_below_limit(5, 3, 5)
        (4, 4)
        """
        try:
            return Combinations.caches[k].get(limit)
        except LookupError:
            pass

        lower = int(comb(n, k))
        if lower > limit:
            n, lower = Combinations.max_n_choose_k_below_limit(n - 1, k, limit)

        upper = int(comb(n + 1, k))

        Combinations.caches[k].set(lower, upper, (n, lower))
        return n, lower

    @staticmethod
    def clear_cache():
        Combinations.caches.clear()
