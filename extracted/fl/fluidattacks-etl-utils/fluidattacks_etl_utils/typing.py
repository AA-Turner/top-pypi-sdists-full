from collections.abc import Callable, Generator, Iterable, Iterator, Sequence
from re import Pattern
from typing import (
    IO,
    Any,
    AnyStr,
    BinaryIO,
    Generic,
    Literal,
    NoReturn,
    ParamSpec,
    ParamSpecArgs,
    ParamSpecKwargs,
    TextIO,
    TypeAlias,
    TypeVar,
    TypeVarTuple,
    Union,
)

from fa_purity import UnitType, unit

_T_arr = TypeVarTuple("_T_arr")
_T = TypeVar("_T")
Dict = dict
Tuple: TypeAlias = tuple[*_T_arr]  # type: ignore[misc]
Set = set
FrozenSet = frozenset
Optional: TypeAlias = _T | None  # type: ignore[misc]
Type = type  # type: ignore[misc]
List = list
__all__ = [
    "IO",
    "Any",
    "AnyStr",
    "BinaryIO",
    "Callable",
    "Generator",
    "Generic",
    "Iterable",
    "Iterator",
    "List",
    "Literal",
    "NoReturn",
    "Optional",
    "ParamSpec",
    "ParamSpecArgs",
    "ParamSpecKwargs",
    "Pattern",
    "Sequence",
    "Set",
    "TextIO",
    "Type",
    "TypeVar",
    "Union",
]


def unit_to_none(_: UnitType) -> None:
    return None


def none_to_unit(_: None) -> UnitType:
    return unit
