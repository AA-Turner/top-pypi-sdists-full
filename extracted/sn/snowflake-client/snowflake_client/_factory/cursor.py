from __future__ import (
    annotations,
)

import inspect
import re
from collections.abc import Iterable
from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    datetime,
)
from logging import (
    Logger,
)
from types import (
    FrameType,
)
from typing import (
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
from redshift_client.sql_client import (
    DbPrimitive,
    DbPrimitiveFactory,
    Limit,
    QueryValues,
    RowData,
    Template,
)
from snowflake.connector.cursor import (
    SnowflakeCursor as RawSnowflakeCursor,
)

from snowflake_client._core import (
    QueryError,
    SnowflakeCursor,
    SnowflakeQuery,
)

_T = TypeVar("_T")
_F = TypeVar("_F")


def _frame_location(frame: FrameType | None) -> str:
    if frame is not None:
        return str(inspect.getframeinfo(frame))
    return "?? Unknown ??"


def _db_primitive_to_raw(item: DbPrimitive) -> Primitive | datetime:
    def _cast(item: Primitive) -> Primitive:
        return item

    return item.map(
        lambda j: j.map(
            lambda x: _cast(x),
            lambda x: _cast(x),
            lambda x: _cast(x),
            lambda x: _cast(x),
            lambda x: _cast(x),
            lambda: None,
        ),
        lambda d: d,
    )


def _decode_row(
    raw_row: FrozenList[_T],
) -> ResultE[RowData]:
    return DbPrimitiveFactory.to_list_of(raw_row, DbPrimitiveFactory.from_any).map(RowData)


def _decode_row_from_any(
    raw_row: _T,
) -> ResultE[RowData]:
    if isinstance(raw_row, (tuple, list)):
        return _decode_row(tuple(raw_row))  # type: ignore[misc]
    err = TypeError(f"_decode_row_from_any row it not a Tuple nor List i.e. `{type(raw_row)}`")
    return Result.failure(err).alt(cast_exception)


def _decode_fetch_rows_from_any(
    result: _T,
) -> ResultE[FrozenList[RowData]]:
    if isinstance(result, (tuple, list)):
        return DbPrimitiveFactory.to_list_of(
            tuple(result),  # type: ignore[misc]
            _decode_row_from_any,
        ).alt(lambda e: TypeError(f"_decode_fetch_rows_from_any i.e. {e}"))
    error = TypeError(f"Unexpected fetch_all result; got {type(result)}")
    return Result.failure(cast_exception(error))


def _util_empty_or_error(
    stream: Stream[ResultE[Maybe[_T]]],
) -> Stream[ResultE[_T]]:
    """
    Stop stream when value is on of these.

    - successful and empty value
    - failure
    Failure result is the final emitted item, but an empty value is omitted
    """

    def _until(items: Iterable[Result[Maybe[_T], _F]]) -> Iterable[Result[_T, _F]]:
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

    return Unsafe.stream_from_cmd(Unsafe.stream_to_iter(stream).map(lambda i: _until(i)))


@dataclass(frozen=True)
class _RawCursor:
    _logger: Logger
    _cursor: RawSnowflakeCursor

    def execute(self, query: SnowflakeQuery) -> Cmd[ResultE[None]]:
        def _action() -> ResultE[None]:
            try:
                self._cursor.execute(query.statement)
                return Result.success(None)
            except Exception as err:  # noqa: BLE001
                return Result.failure(
                    QueryError(
                        "execute",
                        _frame_location(inspect.currentframe()),
                        err,
                        (query.statement,),
                    ),
                ).alt(cast_exception)

        return Cmd.wrap_impure(_action)

    def execute_with_values(
        self,
        query: SnowflakeQuery,
        raw_values: FrozenDict[str, Primitive | datetime],
    ) -> Cmd[ResultE[None]]:
        def _action() -> ResultE[None]:
            items: dict[str, Primitive | datetime] = dict(raw_values)
            try:
                self._cursor.execute(query.statement, items)
                return Result.success(None)
            except Exception as err:  # noqa: BLE001
                return Result.failure(
                    QueryError(
                        "execute_with_values",
                        _frame_location(inspect.currentframe()),
                        err,
                        (query.statement, str(raw_values)),
                    ),
                ).alt(cast_exception)

        return Cmd.wrap_impure(_action)

    def execute_many(
        self,
        query: SnowflakeQuery,
        raw_values: FrozenList[FrozenList[Primitive | datetime]]
        | FrozenList[dict[str, Primitive | datetime]],
    ) -> Cmd[ResultE[None]]:
        def _action() -> ResultE[None]:
            try:
                self._cursor.executemany(query.statement, raw_values)
                return Result.success(None)
            except Exception as err:  # noqa: BLE001
                return Result.failure(
                    QueryError(
                        "execute_many",
                        _frame_location(inspect.currentframe()),
                        err,
                        (query.statement, str(raw_values)),
                    ),
                ).alt(cast_exception)

        return Cmd.wrap_impure(_action)

    def fetch_one(self) -> Cmd[ResultE[Maybe[RowData]]]:
        def _action() -> ResultE[Maybe[RowData]]:
            try:
                items = self._cursor.fetchone()  # type: ignore[misc]
            except Exception as err:  # noqa: BLE001
                return Result.failure(
                    QueryError(
                        "fetch_one",
                        _frame_location(inspect.currentframe()),
                        err,
                        (),
                    ),
                ).alt(cast_exception)
            if items is None:  # type: ignore[misc]
                return Result.success(Maybe.empty())
            return _decode_row_from_any(items).map(  # type: ignore[misc]
                lambda r: Maybe.some(r),
            )

        return Cmd.wrap_impure(_action)

    def fetch_all(self) -> Cmd[ResultE[FrozenList[RowData]]]:
        def _action() -> ResultE[FrozenList[RowData]]:
            try:
                return _decode_fetch_rows_from_any(
                    self._cursor.fetchall(),  # type: ignore[misc]
                )
            except Exception as err:  # noqa: BLE001
                return Result.failure(
                    QueryError(
                        "fetch_all",
                        _frame_location(inspect.currentframe()),
                        err,
                        (),
                    ),
                ).alt(cast_exception)

        return Cmd.wrap_impure(_action)

    def fetch_chunk(self, chunk: int) -> Cmd[ResultE[FrozenList[RowData]]]:
        def _action() -> ResultE[FrozenList[RowData]]:
            try:
                return _decode_fetch_rows_from_any(
                    self._cursor.fetchmany(chunk),  # type: ignore[misc]
                )
            except Exception as err:  # noqa: BLE001
                return Result.failure(
                    QueryError(
                        "fetch_chunk",
                        _frame_location(inspect.currentframe()),
                        err,
                        (),
                    ),
                ).alt(cast_exception)

        return Cmd.wrap_impure(_action)


@dataclass(frozen=True)
class SnowflakeCursorFactory:
    @dataclass(frozen=True)
    class __Private:
        pass

    _private: SnowflakeCursorFactory.__Private = field(repr=False, hash=False, compare=False)
    _logger: Logger
    cursor: _RawCursor

    def execute(self, query: SnowflakeQuery, values: QueryValues | None) -> Cmd[ResultE[None]]:
        values_dict = Maybe.from_optional(values).map(
            lambda v: v.values.map(lambda k: k, _db_primitive_to_raw),
        )
        return values_dict.map(lambda v: self.cursor.execute_with_values(query, v)).value_or(
            self.cursor.execute(query),
        )

    def batch(self, query: SnowflakeQuery, values: FrozenList[QueryValues]) -> Cmd[ResultE[None]]:
        raw_values: FrozenList[dict[str, Primitive | datetime]] = (
            PureIterFactory.from_list(values)
            .map(lambda v: v.values.map(lambda k: k, _db_primitive_to_raw))
            .map(dict)
            .to_list()
        )
        return self.cursor.execute_many(query, raw_values)

    def values(
        self,
        query: SnowflakeQuery,
        data: PureIter[RowData],
        _: Limit,
    ) -> Cmd[ResultE[None]]:
        def _get_first() -> ResultE[RowData]:
            try:
                return Result.success(next(iter(data)))
            except StopIteration as err:
                return Result.failure(err).alt(cast_exception)

        pattern = r"VALUES\s+%s"
        row_len = _get_first().map(lambda r: len(r.data))
        template = row_len.map(
            lambda i: ",".join(PureIterFactory.from_range(range(i)).map(lambda _: "%s")),
        )
        output_statement = template.map(
            lambda t: re.sub(
                pattern,
                "VALUES (" + t + ")",
                query.statement,
                flags=re.IGNORECASE,
            ),
        ).map(SnowflakeQuery.new_query)
        raw_values: FrozenList[FrozenList[Primitive | datetime]] = data.map(
            lambda r: PureIterFactory.from_list(r.data).map(_db_primitive_to_raw).to_list(),
        ).to_list()

        result = output_statement.map(lambda q: self.cursor.execute_many(q, raw_values))
        factory: ResultFactory[None, Exception] = ResultFactory()
        return Cmd.wrap_value(result).bind(
            lambda r: r.to_coproduct().map(
                lambda x: x,
                lambda e: Cmd.wrap_value(factory.failure(e)),
            ),
        )

    def named_values(
        self,
        query: SnowflakeQuery,
        template: Template,
        values: FrozenList[QueryValues],
    ) -> Cmd[ResultE[None]]:
        pattern = r"VALUES\s+%s"
        output_statement = re.sub(
            pattern,
            "VALUES (" + ",".join(template.keys) + ")",
            query.statement,
            flags=re.IGNORECASE,
        )
        raw_values: FrozenList[dict[str, Primitive | datetime]] = (
            PureIterFactory.from_list(values)
            .map(lambda v: v.values.map(lambda k: k, _db_primitive_to_raw))
            .map(dict)
            .to_list()
        )

        return self.cursor.execute_many(
            SnowflakeQuery.new_query(output_statement),
            raw_values,
        )

    def fetch_chunks_stream(self, chunk: int) -> Stream[ResultE[FrozenList[RowData]]]:
        return (
            PureIterFactory.infinite_range(0, 1)
            .map(
                lambda _: self.cursor.fetch_chunk(chunk).map(
                    lambda r: r.map(lambda i: Maybe.from_optional(i if i else None)),
                ),
            )
            .transform(lambda i: StreamFactory.from_commands(i))
            .transform(lambda s: _util_empty_or_error(s))
        )

    @staticmethod
    def new_cursor(logger: Logger, raw: RawSnowflakeCursor) -> SnowflakeCursor:
        _cursor = SnowflakeCursorFactory(
            SnowflakeCursorFactory.__Private(),
            logger,
            _RawCursor(logger, raw),
        )
        return SnowflakeCursor(
            _cursor.execute,
            _cursor.batch,
            _cursor.values,
            _cursor.named_values,
            _cursor.cursor.fetch_one(),
            _cursor.cursor.fetch_all(),
            _cursor.cursor.fetch_chunk,
            _cursor.fetch_chunks_stream,
        )
