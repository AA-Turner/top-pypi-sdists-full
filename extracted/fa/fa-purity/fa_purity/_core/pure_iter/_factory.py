from collections.abc import Callable
from dataclasses import (
    dataclass,
)
from typing import (
    TypeVar,
)

from fa_purity._core import (
    iter_factory,
)
from fa_purity._core.cmd import (
    Cmd,
)
from fa_purity._core.frozen import (
    FrozenList,
)

from ._core import (
    PureIter,
    unsafe_from_cmd,
)

_T = TypeVar("_T")
_I = TypeVar("_I")
_R = TypeVar("_R")


@dataclass(frozen=True)
class PureIterFactory:
    """`PureIter` safe constructors."""

    @staticmethod
    def from_list(items: list[_T] | FrozenList[_T]) -> PureIter[_T]:
        """Generate a PureIter from a list or tuple."""
        _items = tuple(items) if isinstance(items, list) else items
        return unsafe_from_cmd(Cmd.wrap_impure(lambda: _items))

    @staticmethod
    def from_range(range_obj: range) -> PureIter[int]:
        """Generate a PureIter from a range."""
        return unsafe_from_cmd(Cmd.wrap_impure(lambda: range_obj))

    @staticmethod
    def infinite_gen(function: Callable[[_T], _T], init: _T) -> PureIter[_T]:
        """
        Generate an infinite PureIter starting from init.

        The next item is the result of applying the function over the previous element.
        """
        return unsafe_from_cmd(Cmd.wrap_impure(lambda: iter_factory.infinite_gen(function, init)))

    @classmethod
    def infinite_range(cls, start: int, step: int) -> PureIter[int]:
        """
        Infinite `PureIter` starting from start (first-arg).

        The next element is the previous one + the  supplied step (second-arg).
        """
        return cls.infinite_gen(lambda x: x + step, start)

    @classmethod
    def pure_map(
        cls,
        function: Callable[[_I], _R],
        items: list[_I] | FrozenList[_I],
    ) -> PureIter[_R]:
        """
        Apply a function to each item.

        As built-in map function but produces a `PureIter` instead of a normal iterable.
        """
        return cls.from_list(items).map(function)
