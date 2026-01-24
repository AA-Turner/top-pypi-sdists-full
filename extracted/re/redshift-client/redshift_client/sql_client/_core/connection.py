from __future__ import (
    annotations,
)

from collections.abc import Callable
from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from logging import (
    Logger,
)
from typing import (
    TypeVar,
)

import psycopg2.extensions as postgres_extensions
from fa_purity import (
    Cmd,
    CmdUnwrapper,
)

from redshift_client.sql_client._core.cursor import (
    SqlCursor,
)

_T = TypeVar("_T")


class IsolationLvl(Enum):
    READ_UNCOMMITTED = postgres_extensions.ISOLATION_LEVEL_READ_UNCOMMITTED
    READ_COMMITTED = postgres_extensions.ISOLATION_LEVEL_READ_COMMITTED
    REPEATABLE_READ = postgres_extensions.ISOLATION_LEVEL_REPEATABLE_READ
    SERIALIZABLE = postgres_extensions.ISOLATION_LEVEL_SERIALIZABLE


@dataclass(frozen=True)
class DatabaseId:
    db_name: str
    host: str
    port: int


@dataclass(frozen=True)
class Credentials:
    user: str
    password: str

    def __repr__(self) -> str:
        return f"Creds(user={self.user})"


@dataclass(frozen=True)
class DbConnection:
    """Interface for database connections."""

    close: Cmd[None]
    commit: Cmd[None]
    cursor: Callable[[Logger], Cmd[SqlCursor]]

    @staticmethod
    def connect_and_execute(
        new_connection: Cmd[DbConnection],
        action: Callable[[DbConnection], Cmd[_T]],
    ) -> Cmd[_T]:
        """Ensure that connection is closed regardless of action errors."""

        def _inner(connection: DbConnection) -> Cmd[_T]:
            def _action(unwrapper: CmdUnwrapper) -> _T:
                try:
                    return unwrapper.act(action(connection))
                finally:
                    unwrapper.act(connection.close)

            return Cmd.new_cmd(_action)

        return new_connection.bind(_inner)
