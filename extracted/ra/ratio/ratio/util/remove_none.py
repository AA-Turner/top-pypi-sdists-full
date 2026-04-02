from typing import TypeVar, TypeGuard, Iterable

_T = TypeVar("_T")


def _filter_none(item: _T | None) -> TypeGuard[_T]:
    return item is not None


def remove_none(
    list_: Iterable[_T | None],
) -> list[_T]:
    return list(filter(_filter_none, list_))
