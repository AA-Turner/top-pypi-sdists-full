"""Coproduct module."""

from __future__ import (
    annotations,
)

from collections.abc import Callable
from dataclasses import (
    dataclass,
)
from typing import (
    Generic,
    TypeVar,
)

from fa_purity._bug import (
    LibraryBug,
)

_L = TypeVar("_L")
_R = TypeVar("_R")
_T = TypeVar("_T")


@dataclass(frozen=True)
class _Empty:
    pass


def _assert_non_empty(item: _T | _Empty) -> _T:
    """Ensure item is not `_Empty` or raise failure."""
    if isinstance(item, _Empty):
        LibraryBug.new(ValueError("assert_non_empty received empty input"))
    return item


@dataclass(frozen=True)
class Coproduct(Generic[_L, _R]):
    """
    Represents discriminated unions of types.

    Also know as the union type, `Coproduct` unambiguously
    differentiate between the left and right case. This enables
    a better way of handling generic union types where `isinstance`
    cannot be used to differentiate the left-right cases.

    e.g. Union[None, None] = None # left and right injections are equal
    Coproduct[None, None] = Bool # left and right injections are NOT equal
    """

    @dataclass(frozen=True)
    class _Private:
        pass

    _private: Coproduct._Private
    _left: _L | _Empty
    _right: _R | _Empty
    _left_val: bool

    @staticmethod
    def inl(value: _L) -> Coproduct[_L, _R]:
        """Left injection: constructs a `Coproduct` from a value of a left type `_L`."""
        return Coproduct(Coproduct._Private(), value, _Empty(), True)

    @staticmethod
    def inr(value: _R) -> Coproduct[_L, _R]:
        """Right injection: constructs a `Coproduct` from a value of a right type `_R`."""
        return Coproduct(Coproduct._Private(), _Empty(), value, False)

    def map(self, transform_1: Callable[[_L], _T], transform_2: Callable[[_R], _T]) -> _T:
        """Core transform from a `Coproduct` into some other type `_T`."""
        if self._left_val:
            return transform_1(_assert_non_empty(self._left))
        return transform_2(_assert_non_empty(self._right))

    def __str__(self) -> str:
        return self.__class__.__name__ + self.map(
            lambda lv: ".inl(" + str(lv) + ")",
            lambda rv: ".inr(" + str(rv) + ")",
        )

    def __repr__(self) -> str:
        return str(self)


@dataclass(frozen=True)
class CoproductFactory(Generic[_L, _R]):
    """
    Factory for `Coproduct`.

    When type induction fails to recognize the left or right type,
    this factory can be used to explicitly indicate the types.
    """

    def inl(self, value: _L) -> Coproduct[_L, _R]:
        """Left injection for `Coproduct`."""
        return Coproduct.inl(value)

    def inr(self, value: _R) -> Coproduct[_L, _R]:
        """Right injection for `Coproduct`."""
        return Coproduct.inr(value)


@dataclass(frozen=True)
class UnionFactory(Generic[_L, _R]):
    """
    Factory of union types.

    When type induction fails to recognize the left or right type
    on the built in Union this factory can help to set the types
    explicitly.
    """

    def inl(self, value: _L) -> _L | _R:
        """Left injection for builtin `Union`."""
        return value

    def inr(self, value: _R) -> _L | _R:
        """Right injection for builtin `Union`."""
        return value
