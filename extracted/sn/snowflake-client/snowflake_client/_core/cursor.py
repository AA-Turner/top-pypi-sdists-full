from collections.abc import Callable
from dataclasses import (
    dataclass,
)

from fa_purity import (
    Cmd,
    FrozenList,
    Maybe,
    PureIter,
    ResultE,
    Stream,
)
from redshift_client.sql_client import (
    Limit,
    QueryValues,
    RowData,
    Template,
)

from .query import (
    SnowflakeQuery,
)


@dataclass(frozen=True)
class SnowflakeCursor:
    execute: Callable[[SnowflakeQuery, QueryValues | None], Cmd[ResultE[None]]]
    batch: Callable[[SnowflakeQuery, FrozenList[QueryValues]], Cmd[ResultE[None]]]
    values: Callable[[SnowflakeQuery, PureIter[RowData], Limit], Cmd[ResultE[None]]]
    named_values: Callable[[SnowflakeQuery, Template, FrozenList[QueryValues]], Cmd[ResultE[None]]]
    fetch_one: Cmd[ResultE[Maybe[RowData]]]
    fetch_all: Cmd[ResultE[FrozenList[RowData]]]
    fetch_chunk: Callable[[int], Cmd[ResultE[FrozenList[RowData]]]]
    fetch_chunks_stream: Callable[[int], Stream[ResultE[FrozenList[RowData]]]]
