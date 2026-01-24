from __future__ import (
    annotations,
)

import inspect
import logging
from collections.abc import (
    Iterable,
)
from dataclasses import (
    dataclass,
    field,
)

from fa_purity import (
    Cmd,
    CmdUnwrapper,
    FrozenDict,
    FrozenTools,
    Maybe,
    PureIter,
    Result,
    ResultFactory,
    Stream,
    Unsafe,
)
from fa_purity.json import (
    Primitive,
)
from fluidattacks_etl_utils.bug import (
    Bug,
)
from fluidattacks_etl_utils.typing import (
    Callable,
    Dict,
    Generic,
    Tuple,
    TypeVar,
)
from redshift_client.client import (
    TableClient,
)
from redshift_client.core.id_objs import (
    DbTableId,
)
from redshift_client.core.table import (
    Table,
)
from redshift_client.sql_client import (
    DbPrimitiveFactory,
    Query,
    QueryValues,
    SqlCursor,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")
_S = TypeVar("_S")
_A = TypeVar("_A")
_F = TypeVar("_F")
_K = TypeVar("_K")
_V = TypeVar("_V")


def set_queue_group(client: SqlCursor, group: str) -> Cmd[None]:
    statement = "SET query_group TO %(group)s"
    args: Dict[str, Primitive] = {"group": group}
    return client.execute(
        Query.new_query(statement),
        QueryValues(DbPrimitiveFactory.from_raw_prim_dict(FrozenTools.freeze(args))),
    ).map(lambda r: Bug.assume_success("set_queue_group", inspect.currentframe(), (group,), r))


def add_missing_columns(
    client: TableClient,
    source: Table,
    target: Tuple[DbTableId, Table],
) -> Cmd[None]:
    """Add missing columns to target in respect to source."""
    missing_columns = frozenset(source.columns.keys()) - frozenset(target[1].columns.keys())
    missing = FrozenDict(
        {
            m: Bug.assume_success(
                "get_missing_columns",
                inspect.currentframe(),
                (str(source.columns),),
                Maybe.from_optional(source.columns.get(m)).to_result(),
            )
            for m in missing_columns
        },
    )
    msg = Cmd.wrap_impure(
        lambda: LOG.info("adding missing columns (%s) into %s", missing_columns, target[0]),
    )
    return msg + client.add_columns(target[0], missing).map(
        lambda r: Bug.assume_success(
            "get_missing_columns",
            inspect.currentframe(),
            (str(target[0]), str(missing)),
            r,
        ),
    )


def cast_exception(err: Exception) -> Exception:
    return err


def append_to_stream(stream: Stream[_T], item: _T) -> Stream[_T]:
    def _iter(unwrapper: CmdUnwrapper) -> Iterable[_T]:
        yield from unwrapper.act(Unsafe.stream_to_iter(stream))
        yield item

    new_iter = Cmd.new_cmd(_iter)
    return Unsafe.stream_from_cmd(new_iter)


def join_stream(stream_1: Stream[_T], stream_2: Stream[_T]) -> Stream[_T]:
    def _iter(unwrapper: CmdUnwrapper) -> Iterable[_T]:
        yield from unwrapper.act(Unsafe.stream_to_iter(stream_1))
        yield from unwrapper.act(Unsafe.stream_to_iter(stream_2))

    new_iter = Cmd.new_cmd(_iter)
    return Unsafe.stream_from_cmd(new_iter)


def chain_cmd_result(
    cmd_1: Cmd[Result[_S, _F]],
    cmd_2: Callable[[_S], Cmd[Result[_A, _F]]],
) -> Cmd[Result[_A, _F]]:
    factory: ResultFactory[_A, _F] = ResultFactory()
    return cmd_1.bind(
        lambda r: r.map(cmd_2).alt(lambda e: Cmd.wrap_value(factory.failure(e))).to_union(),
    )


def consume_results(cmds: PureIter[Cmd[Result[None, _F]]]) -> Cmd[Result[None, _F]]:
    def _action(unwrapper: CmdUnwrapper) -> Result[None, _F]:
        for cmd in cmds:
            result = unwrapper.act(cmd)
            success = result.map(lambda _: True).value_or(False)
            if not success:
                return result
        return Result.success(None)

    return Cmd.new_cmd(_action)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class MutableMap(Generic[_K, _V]):
    _private: _Private = field(repr=False, hash=False, compare=False)
    _inner: Dict[_K, _V]

    @staticmethod
    def new() -> Cmd[MutableMap[_K, _V]]:
        return Cmd.wrap_impure(lambda: MutableMap(_Private(), {}))

    def get(self, key: _K) -> Cmd[Maybe[_V]]:
        def _action() -> Maybe[_V]:
            if key in self._inner:
                return Maybe.some(self._inner[key])
            return Maybe.empty()

        return Cmd.wrap_impure(_action)

    def get_or(self, key: _K, if_not_exist: Cmd[_V]) -> Cmd[_V]:
        return self.get(key).bind(
            lambda m: m.map(lambda v: Cmd.wrap_value(v)).value_or(if_not_exist),
        )

    def override(self, key: _K, value: _V) -> Cmd[None]:
        def _action() -> None:
            self._inner[key] = value

        return Cmd.wrap_impure(_action)

    def get_or_create(self, key: _K, value: Cmd[_V]) -> Cmd[_V]:
        return self.get(key).bind(
            lambda m: m.map(lambda v: Cmd.wrap_value(v)).value_or(
                value.bind(lambda v: self.override(key, v).map(lambda _: v)),
            ),
        )

    def add_or(self, key: _K, value: _V, if_exist: Cmd[None]) -> Cmd[None]:
        def _action(unwrapper: CmdUnwrapper) -> None:
            if key not in self._inner:
                self._inner[key] = value
            else:
                unwrapper.act(if_exist)

        return Cmd.new_cmd(_action)

    def update(self, items: FrozenDict[_K, _V]) -> Cmd[None]:
        return Cmd.wrap_impure(lambda: self._inner.update(items))

    def freeze(self) -> Cmd[FrozenDict[_K, _V]]:
        return Cmd.wrap_impure(lambda: FrozenDict(self._inner))
