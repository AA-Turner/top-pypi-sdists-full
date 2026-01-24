from __future__ import (
    annotations,
)

from collections.abc import Callable
from dataclasses import (
    dataclass,
)
from typing import (
    TypeVar,
)

from deprecated import deprecated

from fa_purity._bug import (
    LibraryBug,
)
from fa_purity._core.coproduct import Coproduct, CoproductFactory
from fa_purity._core.frozen import (
    FrozenDict,
    FrozenList,
    NewFrozenList,
)
from fa_purity._core.result import (
    Result,
    ResultE,
    ResultFactory,
)
from fa_purity._core.utils import (
    cast_exception,
)

_S = TypeVar("_S")
_F = TypeVar("_F")
_K = TypeVar("_K")
_V = TypeVar("_V")
_T = TypeVar("_T")
_A = TypeVar("_A")
_B = TypeVar("_B")


@dataclass(frozen=True)
class ResultTransform:
    @staticmethod
    def all_ok_2(items: NewFrozenList[Result[_S, _F]]) -> Result[NewFrozenList[_S], _F]:
        ok_list = []
        for i in items:
            if i.map(lambda _: True).value_or(False):
                val: _S = i.or_else_call(
                    lambda: LibraryBug.new(ValueError("all_ok extract value bug")),
                )
                ok_list.append(val)
            else:
                fail: _F = i.swap().or_else_call(
                    lambda: LibraryBug.new(ValueError("all_ok extract fail bug")),
                )
                return Result.failure(fail, NewFrozenList[_S])
        return Result.success(NewFrozenList.new(*ok_list))

    @classmethod
    @deprecated("Prefer `all_ok_2`")  # type: ignore[misc]
    def all_ok(cls, items: FrozenList[Result[_S, _F]]) -> Result[FrozenList[_S], _F]:
        return cls.all_ok_2(NewFrozenList(items)).map(lambda n: n.items)

    @staticmethod
    def get_key(data: FrozenDict[_K, _V], key: _K) -> ResultE[_V]:
        factory: ResultFactory[_V, Exception] = ResultFactory()
        if key in data:
            return factory.success(data[key])
        return factory.failure(KeyError(key)).alt(cast_exception)

    @classmethod
    @deprecated("Renamed to `get_key`")  # type: ignore[misc]
    def try_get(cls, data: FrozenDict[_K, _V], key: _K) -> ResultE[_V]:
        return cls.get_key(data, key)

    @staticmethod
    def get_index(items: NewFrozenList[_T], index: int) -> ResultE[_T]:
        try:
            return Result.success(items.items[index])
        except IndexError as err:
            return Result.failure(cast_exception(err))

    @staticmethod
    def generic_bind(
        result: Result[_S, _F],
        transform: Callable[[_S], Result[_A, _B]],
    ) -> Result[_A, Coproduct[_B, _F]]:
        _factory: CoproductFactory[_B, _F] = CoproductFactory()
        return result.alt(_factory.inr).bind(lambda s: transform(s).alt(_factory.inl))
