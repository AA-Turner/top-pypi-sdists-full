import abc
import asyncio
from contextlib import asynccontextmanager
from types import TracebackType
from typing import (
    AsyncContextManager,
    AsyncIterator,
    Awaitable,
    Callable,
    Optional,
    Type,
    TypeVar,
)

from .database_errors import DatabaseConnectionError
from .connection import AbstractDatabaseConnection, AbstractQueryExecutor

TRawConnection = TypeVar("TRawConnection", bound=AsyncContextManager)
TReturn = TypeVar("TReturn")


class RawDatabaseConnectionWrapper(AbstractQueryExecutor[TRawConnection]):
    """
    The abstract base class of database connections that can be implemented as a simple wrapper over a raw connection.

    Plugin developers should typically derive from this class.
    """

    _raw_connection: TRawConnection
    _lock: asyncio.Lock

    def __init__(self, raw_connection: TRawConnection) -> None:
        self._raw_connection = raw_connection
        self._lock = asyncio.Lock()

    async def execute(
        self,
        query: Callable[[TRawConnection], Awaitable[TReturn]],
        return_type: Optional[Type[TReturn]] = None,
    ) -> TReturn:
        return await query(self._raw_connection)

    async def commit(self) -> None:
        await self.commit_impl(self._raw_connection)

    @asynccontextmanager
    async def lock(self) -> AsyncIterator:
        async with self._lock:
            yield self

    async def __aenter__(self) -> AbstractDatabaseConnection:
        try:
            await self._raw_connection.__aenter__()
        except Exception as e:
            # in this case either host/port or database name is invalid
            raise DatabaseConnectionError(f"database connection error: {e}") from e
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self._raw_connection.__aexit__(exc_type, exc_val, exc_tb)

    @abc.abstractmethod
    async def commit_impl(self, raw_connection: TRawConnection) -> None:
        """
        Commits the current database transaction on the given raw connection.
        """
        ...
