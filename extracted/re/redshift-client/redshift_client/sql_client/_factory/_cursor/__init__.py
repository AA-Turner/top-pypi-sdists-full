from collections.abc import Callable, Iterable
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from logging import (
    Logger,
)
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from fa_purity import (
    Cmd,
    FrozenDict,
    FrozenList,
    Maybe,
    PureIter,
    PureIterFactory,
    Result,
    ResultE,
    ResultFactory,
    Stream,
    StreamFactory,
    Unsafe,
    cast_exception,
)
from fa_purity.json import (
    Primitive,
)
from psycopg2 import (
    DatabaseError,
    DataError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
    extras,
)

from redshift_client.sql_client._core.cursor import (
    Limit,
    QueryValues,
    RowData,
    SqlCursor,
    Template,
)
from redshift_client.sql_client._core.primitive import (
    DbPrimitive,
)
from redshift_client.sql_client._core.query import (
    Query,
)

from . import (
    _assert,
)

if TYPE_CHECKING:
    from psycopg2 import (  # type: ignore[attr-defined]
        cursor as CursorStub,
    )
else:
    CursorStub = Any


_T = TypeVar("_T")
_F = TypeVar("_F")


def _handle_psycopg_errors(raw: Callable[[], _T]) -> ResultE[_T]:
    try:
        return Result.success(raw())
    except (
        DatabaseError,  # type:ignore[misc]
        OperationalError,  # type:ignore[misc]
        NotSupportedError,  # type:ignore[misc]
        DataError,  # type:ignore[misc]
        ProgrammingError,  # type:ignore[misc]
        InternalError,  # type:ignore[misc]
    ) as err:
        return Result.failure(cast_exception(err))


def _util_empty_or_error(
    stream: Stream[ResultE[Maybe[_T]]],
) -> Stream[ResultE[_T]]:
    """
    Stop a stream when value is one of the following.

    - successful and empty value
    - failure
    Failure result is the final emitted item, but an empty value is omitted.
    """

    def _until(
        items: Iterable[Result[Maybe[_T], _F]],
    ) -> Iterable[Result[_T, _F]]:
        _factory: ResultFactory[_T, _F] = ResultFactory()
        for item in items:
            successful = item.map(lambda _: True).value_or(False)
            if successful:
                inner_item = item.or_else_call(
                    lambda: Unsafe.raise_exception(Exception("Impossible!")),
                )
                if inner_item.map(lambda _: False).value_or(True):
                    break
                result = inner_item.or_else_call(
                    lambda: Unsafe.raise_exception(Exception("Impossible!")),
                )
                yield _factory.success(result)
            else:
                inner_fail = item.swap().or_else_call(
                    lambda: Unsafe.raise_exception(Exception("Impossible!")),
                )
                yield _factory.failure(inner_fail)
                break

    return Unsafe.stream_from_cmd(
        Unsafe.stream_to_iter(stream).map(lambda i: _until(i)),
    )


def _primitive_to_raw(item: DbPrimitive) -> Primitive | datetime:
    def _cast(item: Primitive) -> Primitive:
        return item

    return item.map(
        lambda p: p.map(
            lambda x: _cast(x),
            lambda x: _cast(x),
            lambda x: _cast(x),
            lambda x: _cast(x),
            lambda x: _cast(x),
            lambda: _cast(None),
        ),
        lambda d: d,
    )


def _to_raw(
    items: FrozenDict[str, DbPrimitive],
) -> FrozenDict[str, Primitive | datetime]:
    return FrozenDict({k: _primitive_to_raw(v) for k, v in items.items()})


@dataclass(frozen=True)
class _SqlClient1:
    _log: Logger
    _cursor: CursorStub

    def execute(
        self,
        query: Query,
        args: QueryValues | None,
    ) -> Cmd[ResultE[None]]:
        _values: FrozenDict[str, Primitive | datetime] = (
            _to_raw(args.values) if args else FrozenDict({})
        )
        preview = self._cursor.mogrify(
            query.statement,
            _values,
        )

        def _action() -> ResultE[None]:
            self._log.debug("Executing: %s", preview)
            return _handle_psycopg_errors(
                lambda: self._cursor.execute(query.statement, _values),
            )

        return Cmd.wrap_impure(_action)

    def batch(
        self,
        query: Query,
        args: FrozenList[QueryValues],
    ) -> Cmd[ResultE[None]]:
        def _action() -> ResultE[None]:
            _args: FrozenList[FrozenDict[str, Primitive | datetime]] = tuple(
                _to_raw(v.values) for v in args
            )
            self._log.debug(
                "Batch execution (%s items): %s",
                len(_args),
                query.statement,
            )
            return _handle_psycopg_errors(
                lambda: extras.execute_batch(
                    self._cursor,
                    query.statement,
                    _args,
                ),
            )

        return Cmd.wrap_impure(_action)

    def values(
        self,
        query: Query,
        args: PureIter[RowData],
        limit: Limit,
    ) -> Cmd[ResultE[None]]:
        def _action() -> ResultE[None]:
            self._log.debug("Executing query over values: %s", query.statement)
            _args: PureIter[FrozenList[Primitive | datetime]] = args.map(
                lambda r: PureIterFactory.from_list(r.data).map(_primitive_to_raw).to_list(),
            )
            return _handle_psycopg_errors(
                lambda: extras.execute_values(  # type: ignore[misc]
                    self._cursor,
                    query.statement,
                    _args,
                    page_size=limit.limit,
                ),
            )

        return Cmd.wrap_impure(_action)

    def named_values(
        self,
        query: Query,
        template: Template,
        args: FrozenList[QueryValues],
    ) -> Cmd[ResultE[None]]:
        def _action() -> ResultE[None]:
            self._log.debug("Executing query over values: %s", query.statement)
            _args: PureIter[FrozenDict[str, Primitive | datetime]] = PureIterFactory.from_list(
                args,
            ).map(
                lambda q: _to_raw(q.values),
            )
            return _handle_psycopg_errors(
                lambda: extras.execute_values(  # type: ignore[misc]
                    self._cursor,
                    query.statement,
                    _args,
                    template="(" + ",".join(template.keys) + ")",
                ),
            )

        return Cmd.wrap_impure(_action)

    def fetch_one(self) -> Cmd[ResultE[Maybe[RowData]]]:
        def _action() -> ResultE[Maybe[RowData]]:
            self._log.debug("Fetching one row")
            return (
                _handle_psycopg_errors(
                    lambda: _assert.assert_fetch_one(self._cursor.fetchone()),  # type: ignore[misc]
                )
                .bind(lambda r: r)
                .map(lambda m: m.map(RowData))
            )

        return Cmd.wrap_impure(_action)

    def fetch_all(self) -> Cmd[ResultE[FrozenList[RowData]]]:
        def _action() -> ResultE[FrozenList[RowData]]:
            self._log.debug("Fetching all rows")
            items = _assert.assert_fetch_list(tuple(self._cursor.fetchall()))  # type: ignore[misc]
            return items.map(lambda i: tuple(map(RowData, i)))

        return Cmd.wrap_impure(_action)

    def fetch_chunk(self, chunk: int) -> Cmd[ResultE[FrozenList[RowData]]]:
        def _action() -> ResultE[FrozenList[RowData]]:
            self._log.debug("Fetching %s rows", chunk)
            items = _assert.assert_fetch_list(
                tuple(self._cursor.fetchmany(chunk)),  # type: ignore[misc]
            )
            return items.map(lambda i: tuple(map(RowData, i)))

        return Cmd.wrap_impure(_action)

    def fetch_chunks_stream(
        self,
        chunk: int,
    ) -> Stream[ResultE[FrozenList[RowData]]]:
        return (
            PureIterFactory.infinite_range(0, 1)
            .map(
                lambda _: self.fetch_chunk(chunk).map(
                    lambda r: r.map(
                        lambda i: Maybe.from_optional(i if i else None),
                    ),
                ),
            )
            .transform(lambda i: StreamFactory.from_commands(i))
            .transform(lambda s: _util_empty_or_error(s))
        )


def new_sql_client(_log: Logger, _cursor: CursorStub) -> SqlCursor:
    _client = _SqlClient1(_log, _cursor)
    return SqlCursor(
        _client.execute,
        _client.batch,
        _client.values,
        _client.named_values,
        _client.fetch_one(),
        _client.fetch_all(),
        _client.fetch_chunk,
        _client.fetch_chunks_stream,
    )
