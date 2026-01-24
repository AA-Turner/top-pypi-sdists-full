from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Generic,
    TypeVar,
)

from fa_purity import (
    FrozenDict,
    FrozenList,
    Result,
    ResultE,
    cast_exception,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class SnowflakeIdentifier:
    @dataclass(frozen=True)
    class __Private:  # pylint: disable=invalid-name
        pass

    _private: SnowflakeIdentifier.__Private = field(repr=False, hash=False, compare=False)
    raw: str
    escaped_id: str

    @staticmethod
    def from_raw(identifier: str) -> SnowflakeIdentifier:
        escaped = identifier.replace('"', '""').replace("%", r"%%")
        return SnowflakeIdentifier(
            SnowflakeIdentifier.__Private(),
            identifier,
            escaped,
        )


def _purifier(statement: str, identifiers: FrozenDict[str, SnowflakeIdentifier]) -> ResultE[str]:
    safe_args = FrozenDict(
        {key: '"' + value.escaped_id + '"' for key, value in identifiers.items()},
    )
    try:
        return Result.success(statement.format(**safe_args))
    except KeyError as err:
        return Result.failure(err).alt(cast_exception)


def _pretty(raw: str) -> str:
    return " ".join(raw.strip(" \n\t").split())


@dataclass(frozen=True)
class SnowflakeQuery:
    @dataclass(frozen=True)
    class __Private:  # pylint: disable=invalid-name
        pass

    __private: SnowflakeQuery.__Private = field(repr=False, hash=False, compare=False)
    statement: str

    @staticmethod
    def new_query(stm: str) -> SnowflakeQuery:
        return SnowflakeQuery(SnowflakeQuery.__Private(), _pretty(stm))

    @staticmethod
    def dynamic_query(statement: str, identifiers: FrozenDict[str, str]) -> ResultE[SnowflakeQuery]:
        return _purifier(
            _pretty(statement),
            identifiers.map(lambda k: k, lambda v: SnowflakeIdentifier.from_raw(v)),
        ).map(lambda s: SnowflakeQuery(SnowflakeQuery.__Private(), s))


@dataclass
class QueryError(Exception, Generic[_T]):
    obj_id: str
    location: str
    parent_error: _T | None
    context: FrozenList[str]
