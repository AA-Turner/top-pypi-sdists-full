from collections.abc import Callable, Iterable, Iterator
from typing import Generic, NoReturn, TypeAlias, TypeVar, TypeVarTuple, Union

_T_arr = TypeVarTuple("_T_arr")
Dict = dict
Tuple: TypeAlias = tuple[*_T_arr]  # type: ignore[misc]
FrozenSet = frozenset

__all__ = [
    "Callable",
    "Generic",
    "Iterable",
    "Iterator",
    "NoReturn",
    "TypeVar",
    "Union",
]
