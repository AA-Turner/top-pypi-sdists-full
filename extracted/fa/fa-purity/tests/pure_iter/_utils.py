from typing import (
    TypeVar,
)

from fa_purity import (
    FrozenList,
    PureIter,
)

_T = TypeVar("_T")


def to_tuple(items: PureIter[_T], limit: int) -> FrozenList[_T]:
    result = []
    for n, i in enumerate(items):
        result.append(i)
        if n + 1 >= limit:
            break
    return tuple(result)


def assert_immutability(piter: PureIter[_T], only_count: bool = False) -> None:
    # for finite PureIter
    if only_count:
        assert sum(1 for _ in piter) == sum(1 for _ in piter)
    else:
        assert tuple(piter) == tuple(piter)


def assert_immutability_inf(piter: PureIter[_T]) -> None:
    # for infinite PureIter
    assert to_tuple(piter, 10) == to_tuple(piter, 10)
