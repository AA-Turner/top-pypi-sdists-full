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

from .coproduct import (
    Coproduct,
    CoproductFactory,
    UnionFactory,
)

_S = TypeVar("_S")
_F = TypeVar("_F")
_T = TypeVar("_T")


@dataclass(frozen=True)
class _Result(Generic[_S, _F]):
    value: Coproduct[_S, _F]


@dataclass(frozen=True)
class Result(Generic[_S, _F]):
    """
    Represents a success or failure value.

    Equivalent to Coproduct[_S, _F], but designed to handle explicit errors
    """

    _inner: _Result[_S, _F]

    @staticmethod
    def success(val: _S, _type: type[_F] | None = None) -> Result[_S, _F]:
        item: Coproduct[_S, _F] = Coproduct.inl(val)
        return Result(_Result(item))

    @staticmethod
    def failure(val: _F, _type: type[_S] | None = None) -> Result[_S, _F]:
        item: Coproduct[_S, _F] = Coproduct.inr(val)
        return Result(_Result(item))

    def map(self, function: Callable[[_S], _T]) -> Result[_T, _F]:
        factory: CoproductFactory[_T, _F] = CoproductFactory()
        val = self._inner.value.map(
            lambda s: factory.inl(function(s)),
            lambda f: factory.inr(f),
        )
        return Result(_Result(val))

    def alt(self, function: Callable[[_F], _T]) -> Result[_S, _T]:
        factory: CoproductFactory[_S, _T] = CoproductFactory()
        val = self._inner.value.map(
            lambda s: factory.inl(s),
            lambda f: factory.inr(function(f)),
        )
        return Result(_Result(val))

    def to_coproduct(self) -> Coproduct[_S, _F]:
        return self._inner.value

    def bind(self, function: Callable[[_S], Result[_T, _F]]) -> Result[_T, _F]:
        factory: CoproductFactory[_T, _F] = CoproductFactory()
        val = self._inner.value.map(
            lambda s: function(s).to_coproduct(),
            lambda f: factory.inr(f),
        )
        return Result(_Result(val))

    def lash(self, function: Callable[[_F], Result[_S, _T]]) -> Result[_S, _T]:
        factory: CoproductFactory[_S, _T] = CoproductFactory()
        val = self._inner.value.map(
            lambda s: factory.inl(s),
            lambda f: function(f).to_coproduct(),
        )
        return Result(_Result(val))

    def swap(self) -> Result[_F, _S]:
        def _right(item: _F) -> Coproduct[_F, _S]:
            return Coproduct.inl(item)

        def _left(item: _S) -> Coproduct[_F, _S]:
            return Coproduct.inr(item)

        val = self._inner.value.map(_left, _right)
        return Result(_Result(val))

    def apply(self, wrapped: Result[Callable[[_S], _T], _F]) -> Result[_T, _F]:
        return wrapped.bind(lambda f: self.map(f))

    def cop_value_or(self, default: _T) -> Coproduct[_S, _T]:
        factory: CoproductFactory[_S, _T] = CoproductFactory()
        return self._inner.value.map(
            lambda s: factory.inl(s),
            lambda _: factory.inr(default),
        )

    def cop_or_else_call(self, function: Callable[[], _T]) -> Coproduct[_S, _T]:
        factory: CoproductFactory[_S, _T] = CoproductFactory()
        return self._inner.value.map(
            lambda s: factory.inl(s),
            lambda _: factory.inr(function()),
        )

    def value_or(self, default: _T) -> _S | _T:
        factory: UnionFactory[_S, _T] = UnionFactory()
        return self.cop_value_or(default).map(
            lambda i: factory.inl(i),
            lambda r: factory.inr(r),
        )

    def or_else_call(self, function: Callable[[], _T]) -> _S | _T:
        factory: UnionFactory[_S, _T] = UnionFactory()
        return self.cop_or_else_call(function).map(
            lambda i: factory.inl(i),
            lambda r: factory.inr(r),
        )

    def to_union(self) -> _S | _F:
        factory: UnionFactory[_S, _F] = UnionFactory()
        return self._inner.value.map(
            lambda i: factory.inl(i),
            lambda r: factory.inr(r),
        )

    def __str__(self) -> str:
        return self.__class__.__name__ + self.to_coproduct().map(
            lambda x: ".success(" + str(x) + ")",
            lambda x: ".failure(" + str(x) + ")",
        )

    def __repr__(self) -> str:
        return str(self)


@dataclass(frozen=True)
class ResultFactory(Generic[_S, _F]):
    """
    Factory of `Result` objects.

    Generic types cannot be passed as type arguments
    on success and failure constructors.
    This factory handles the generic type use case.
    """

    def success(self, value: _S) -> Result[_S, _F]:
        return Result.success(value)

    def failure(self, value: _F) -> Result[_S, _F]:
        return Result.failure(value)


ResultE = Result[_T, Exception]  # type: ignore[misc]
