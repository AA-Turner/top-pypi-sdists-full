from collections.abc import Callable
from typing import (
    TypeVar,
)

_T = TypeVar("_T")
_R = TypeVar("_R")


def chain_items(
    items: tuple[frozenset[_T] | tuple[_T, ...], ...],
) -> tuple[_T, ...]:
    all_items: list[_T] = []
    for item_set in items:
        for item in item_set:
            all_items.append(item)  # noqa: PERF402
    return tuple(all_items)


def assert_set(
    items: tuple[_T, ...],
    encode: Callable[[_T], str],
) -> frozenset[_T] | Exception:
    item_set: set[_T] = set()
    for i in items:
        if i in item_set:
            return Exception(f"Duplicated item i.e. {encode(i)}")
        item_set.add(i)
    return frozenset(item_set)


def transform_items(
    items: tuple[_T, ...],
    transform: Callable[[_T], _R | Exception],
) -> tuple[_R, ...] | Exception:
    result: list[_R] = []
    for i in items:
        item = transform(i)
        if isinstance(item, Exception):
            return item
        result.append(item)
    return tuple(result)


def transform_sets(
    items: frozenset[_T],
    transform: Callable[[_T], _R | Exception],
) -> frozenset[_R] | Exception:
    _items: tuple[_T, ...] = tuple(items)
    result = transform_items(_items, transform)
    if isinstance(result, Exception):
        return result
    return frozenset(result)


def to_tuple(item: tuple[str, ...] | str) -> tuple[str, ...]:
    if isinstance(item, tuple):
        return item
    return (item,)


def raise_or_value(item: _T | Exception) -> _T:
    if isinstance(item, Exception):
        raise item
    return item
