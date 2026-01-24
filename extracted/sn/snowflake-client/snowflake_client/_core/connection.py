from __future__ import (
    annotations,
)

from collections.abc import Callable
from dataclasses import (
    dataclass,
)
from logging import (
    Logger,
)
from typing import (
    TypeVar,
)

from fa_purity import (
    Cmd,
    CmdUnwrapper,
)

from .cursor import (
    SnowflakeCursor,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class SnowflakeCredentials:
    user: str
    private_key: str
    account: str

    def __repr__(self) -> str:
        return "[MASKED]"

    def __str__(self) -> str:
        return "[MASKED]"


@dataclass(frozen=True)
class SnowflakeWarehouse:
    name: str


@dataclass(frozen=True)
class SnowflakeDatabase:
    name: str


@dataclass(frozen=True)
class SnowflakeConnection:
    """Interface for database connections."""

    close: Cmd[None]
    commit: Cmd[None]
    cursor: Callable[[Logger], Cmd[SnowflakeCursor]]

    @staticmethod
    def connect_and_execute(
        new_connection: Cmd[SnowflakeConnection],
        action: Callable[[SnowflakeConnection], Cmd[_T]],
    ) -> Cmd[_T]:
        """Ensure that connection is closed regardless of action errors."""

        def _inner(connection: SnowflakeConnection) -> Cmd[_T]:
            def _action(unwrapper: CmdUnwrapper) -> _T:
                try:
                    return unwrapper.act(action(connection))
                finally:
                    unwrapper.act(connection.close)

            return Cmd.new_cmd(_action)

        return new_connection.bind(_inner)
