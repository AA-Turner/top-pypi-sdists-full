from collections.abc import Callable
from dataclasses import (
    dataclass,
)

from fa_purity import (
    Cmd,
    FrozenDict,
    FrozenList,
    Maybe,
    PureIter,
    ResultE,
    Stream,
)

from .primitive import (
    DbPrimitive,
)
from .query import (
    Query,
)


@dataclass(frozen=True)
class RowData:
    data: FrozenList[DbPrimitive]


@dataclass(frozen=True)
class QueryValues:
    values: FrozenDict[str, DbPrimitive]


@dataclass(frozen=True)
class Template:
    keys: FrozenList[str]


@dataclass(frozen=True)
class Limit:
    limit: int


@dataclass(frozen=True)
class SqlCursor:
    execute: Callable[[Query, QueryValues | None], Cmd[ResultE[None]]]
    batch: Callable[[Query, FrozenList[QueryValues]], Cmd[ResultE[None]]]
    values: Callable[[Query, PureIter[RowData], Limit], Cmd[ResultE[None]]]
    named_values: Callable[
        [Query, Template, FrozenList[QueryValues]],
        Cmd[ResultE[None]],
    ]
    fetch_one: Cmd[ResultE[Maybe[RowData]]]
    fetch_all: Cmd[ResultE[FrozenList[RowData]]]
    fetch_chunk: Callable[[int], Cmd[ResultE[FrozenList[RowData]]]]
    fetch_chunks_stream: Callable[[int], Stream[ResultE[FrozenList[RowData]]]]
