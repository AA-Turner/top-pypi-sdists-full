from __future__ import (
    annotations,
)

import functools
from collections.abc import Callable, Iterable, Iterator
from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Generic,
    TypeVar,
)

from fa_purity._core import (
    iter_factory,
)
from fa_purity._core.cmd import (
    Cmd,
    unsafe_unwrap,
)
from fa_purity._core.frozen import (
    FrozenList,
)
from fa_purity._core.maybe import (
    Maybe,
)

_T = TypeVar("_T")
_R = TypeVar("_R")
_S = TypeVar("_S")


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class PureIter(Generic[_T]):
    """Represents a reproducible iterable."""

    # unsafe_unwrap use is safe due to iters equivalence
    _private: _Private = field(repr=False, hash=False, compare=False)
    _new_iter: Cmd[Iterable[_T]]

    def generate(self, function: Callable[[_S, _T], tuple[_S, _R]], init_state: _S) -> PureIter[_R]:
        """
        Generate `PureIter` from a reduction like process.

        Generate a new iterable by applying the function over each item where:
        - The argument state (_S) comes from a previous computation of the function over
        a previous state-item pair or from `init_state` if it is the first element.
        """
        return PureIter(
            _Private(),
            self._new_iter.map(lambda i: iter_factory.gen_next(function, init_state, i)),
        )

    def enumerate(self, init: int) -> PureIter[tuple[int, _T]]:
        """
        Enumerate a `PureIter`.

        Generate a new iterable by enumerating each item
        starting from the suplied init integer.
        """
        return self.generate(lambda i, t: (i + 1, (i, t)), init)

    def map(self, function: Callable[[_T], _R]) -> PureIter[_R]:
        """
        Apply function to `PureIter`.

        Generate a new iterable by applying the supplied function
        to each of the element of the current iterable.
        """
        return self.generate(lambda _, t: (None, function(t)), None)

    def reduce(self, function: Callable[[_R, _T], _R], init: _R) -> _R:
        """
        Apply the supplied function to the iterable.

        Such that:
        - the second argument `_T` is the current element in the iteration
        - The first argument `_R` is the result of applying the function
        over the previous element i.e. function(previous_item). If there is not
        a previous element then the argument `_R` is set to the supplied init
        - This returns the last result of the function call or init if
        iterator is empty
        """
        return unsafe_unwrap(self._new_iter.map(lambda i: functools.reduce(function, i, init)))

    def bind(self, function: Callable[[_T], PureIter[_R]]) -> PureIter[_R]:
        unchained = self.map(function)
        return PureIter(_Private(), Cmd.wrap_impure(lambda: iter_factory.chain(unchained)))

    def filter(self, function: Callable[[_T], bool]) -> PureIter[_T]:
        _iter: Cmd[Iterable[_T]] = self._new_iter.map(lambda i: iter(filter(function, i)))
        return PureIter(_Private(), _iter)

    def find_first(self, criteria: Callable[[_T], bool]) -> Maybe[_T]:
        result = self._new_iter.map(lambda i: iter_factory.find_first(criteria, i)).map(
            lambda x: Maybe.from_optional(x),
        )
        return unsafe_unwrap(result)

    def chunked(self, size: int) -> PureIter[FrozenList[_T]]:
        return PureIter(
            _Private(),
            self._new_iter.map(lambda i: iter_factory.chunked(i, size)),
        )

    def to_list(self) -> FrozenList[_T]:
        return tuple(self)

    def transform(self, function: Callable[[PureIter[_T]], _R]) -> _R:
        return function(self)

    def __iter__(self) -> Iterator[_T]:
        return iter(unsafe_unwrap(self._new_iter))


def unsafe_from_cmd(cmd: Cmd[Iterable[_T]]) -> PureIter[_T]:
    return PureIter(_Private(), cmd)
