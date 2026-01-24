from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    cast,
)

from fa_purity import (
    FrozenDict,
)
from psycopg2.sql import (
    SQL,
    Identifier,
)


def _purifier(statement: str, identifiers: FrozenDict[str, str]) -> SQL:
    raw_sql = SQL(statement)
    safe_args = FrozenDict(
        {key: Identifier(value) for key, value in identifiers.items()},
    )
    return cast("SQL", raw_sql.format(**safe_args))


def _pretty(raw: str) -> str:
    return " ".join(raw.strip(" \n\t").split())


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class Query:
    _private: _Private = field(repr=False, hash=False, compare=False)
    statement: SQL

    @staticmethod
    def new_query(stm: str) -> Query:
        return Query(_Private(), SQL(_pretty(stm)))

    @staticmethod
    def dynamic_query(stm: str, identifiers: FrozenDict[str, str]) -> Query:
        return Query(_Private(), _purifier(_pretty(stm), identifiers))
