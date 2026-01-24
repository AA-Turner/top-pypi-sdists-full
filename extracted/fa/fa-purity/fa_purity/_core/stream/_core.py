from __future__ import (
    annotations,
)

import functools
from collections.abc import Callable, Iterable
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
)
from fa_purity._core.frozen import (
    FrozenList,
)
from fa_purity._core.maybe import (
    Maybe,
)

_T = TypeVar("_T")
_R = TypeVar("_R")


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class Stream(Generic[_T]):
    _private: _Private = field(repr=False, hash=False, compare=False)
    _new_iter: Cmd[Iterable[_T]]

    def map(self, function: Callable[[_T], _R]) -> Stream[_R]:
        items: Cmd[Iterable[_R]] = self._new_iter.map(lambda i: iter(map(function, i)))
        return Stream(_Private(), items)

    def reduce(self, function: Callable[[_R, _T], _R], init: _R) -> Cmd[_R]:
        return self._new_iter.map(lambda i: functools.reduce(function, i, init))

    def bind(self, function: Callable[[_T], Stream[_R]]) -> Stream[_R]:
        items = (
            self.map(function)
            .unsafe_to_iter(_Private())
            .map(lambda items: iter(i.unsafe_to_iter(_Private()) for i in items))
            .bind(lambda x: iter_factory.squash(x))
            .map(lambda x: iter_factory.chain(x))
        )
        return Stream(_Private(), items)

    def filter(self, function: Callable[[_T], bool]) -> Stream[_T]:
        items: Cmd[Iterable[_T]] = self._new_iter.map(lambda i: iter(filter(function, i)))
        return Stream(_Private(), items)

    def find_first(self, criteria: Callable[[_T], bool]) -> Cmd[Maybe[_T]]:
        return self._new_iter.map(lambda i: iter_factory.find_first(criteria, i)).map(
            lambda x: Maybe.from_optional(x),
        )

    def chunked(self, size: int) -> Stream[FrozenList[_T]]:
        items: Cmd[Iterable[FrozenList[_T]]] = self._new_iter.map(
            lambda i: iter_factory.chunked(i, size),
        )
        return Stream(_Private(), items)

    def transform(self, function: Callable[[Stream[_T]], _R]) -> _R:
        return function(self)

    def to_list(self) -> Cmd[FrozenList[_T]]:
        return self._new_iter.map(tuple)

    def unsafe_to_iter(self, _: _Private) -> Cmd[Iterable[_T]]:
        """Private method [WARNING] Do not use."""
        return self._new_iter


def unsafe_to_iter(stream: Stream[_T]) -> Cmd[Iterable[_T]]:
    # if possible iterables should not be used directly
    return stream.unsafe_to_iter(_Private())


def unsafe_from_cmd(cmd: Cmd[Iterable[_T]]) -> Stream[_T]:
    # [WARNING] unsafe constructor
    # - Type-check cannot ensure its proper use
    # - Do not use until is strictly necessary
    # - Do unit test over the function defined by this
    #
    # As with `PureIter unsafe_from_cmd` the cmd must return a new iterable
    # object in each call to ensure that the stream is never consumed,
    # nevertheless they can be semanticly different iterables.
    return Stream(_Private(), cmd)
