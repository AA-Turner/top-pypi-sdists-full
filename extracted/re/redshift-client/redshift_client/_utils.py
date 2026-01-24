from __future__ import (
    annotations,
)

from collections.abc import Callable
from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Generic,
    TypeVar,
)

from fa_purity import (
    Cmd,
    CmdUnwrapper,
    FrozenList,
    Maybe,
    PureIter,
    Result,
    ResultE,
    ResultFactory,
    cast_exception,
)

_T = TypeVar("_T")
_S = TypeVar("_S")
_F = TypeVar("_F")


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class NonEmptySet(Generic[_T]):
    _private: _Private = field(repr=False, hash=False, compare=False)
    _inner: frozenset[_T]

    @staticmethod
    def new(item: _T) -> NonEmptySet[_T]:
        return NonEmptySet(_Private(), frozenset([item]))

    @staticmethod
    def optional_non_empty(items: frozenset[_T]) -> Maybe[NonEmptySet[_T]]:
        if items != frozenset([]):
            return Maybe.some(NonEmptySet(_Private(), frozenset(items)))
        return Maybe.empty()

    @classmethod
    def from_set(cls, items: frozenset[_T]) -> ResultE[NonEmptySet[_T]]:
        error = ValueError("`FrozenSet` must not be empty.")
        return cls.optional_non_empty(items).to_result().alt(lambda _: cast_exception(error))

    def to_set(self) -> frozenset[_T]:
        return self._inner

    def __contains__(self, item: _T) -> bool:
        return item in self._inner


def _lazy_all_ok(
    results: PureIter[Cmd[Result[_S, _F]]],
) -> Cmd[Maybe[Result[_S, _F]]]:
    def _action(unwrapper: CmdUnwrapper) -> Maybe[Result[_S, _F]]:
        item: Maybe[Result[_S, _F]] = Maybe.empty()
        for c in results:
            result = unwrapper.act(c)
            item = Maybe.some(result)
            success = result.map(lambda _: True).value_or(False)
            if not success:
                return item
        return item

    return Cmd.new_cmd(_action)


def chain(
    cmd_1: Cmd[ResultE[_T]],
    cmd_2: Callable[[_T], Cmd[_S]],
) -> Cmd[ResultE[_S]]:
    """Execute cmd_1 then if successful execute the cmd_2."""
    _factory: ResultFactory[_S, Exception] = ResultFactory()
    return cmd_1.bind(
        lambda r: r.map(lambda t: cmd_2(t).map(_factory.success))
        .alt(lambda e: Cmd.wrap_value(_factory.failure(e)))
        .to_union(),
    )


def chain_results(
    cmd_1: Cmd[ResultE[None]],
    cmd_2: Cmd[ResultE[_S]],
) -> Cmd[ResultE[_S]]:
    return chain(cmd_1, lambda _: cmd_2).map(lambda r: r.bind(lambda v: v))


def get_index(items: FrozenList[_T], index: int) -> ResultE[_T]:
    try:
        return Result.success(items[index])
    except IndexError as err:
        return Result.failure(cast_exception(err))


def extract_fail(results: PureIter[Cmd[ResultE[None]]]) -> Cmd[ResultE[None]]:
    return _lazy_all_ok(results).map(
        lambda m: m.value_or(Result.success(None, Exception)),
    )
