import abc
from types import TracebackType
from typing import (
    AsyncContextManager,
    Awaitable,
    Callable,
    Generic,
    Optional,
    Type,
    TypeVar,
)

TRawConnection = TypeVar("TRawConnection")
TReturn = TypeVar("TReturn")


class AbstractDatabaseConnection(abc.ABC):
    "Interface that database connections shall implement in a database plugin."

    @abc.abstractmethod
    async def commit(self) -> None:
        """
        Commits the current database transaction.
        """
        ...

    @abc.abstractmethod
    def lock(self) -> AsyncContextManager:
        """
        Locks this connection from other concurrent tasks. This lock is not thread safe.
        """
        ...

    @abc.abstractmethod
    async def __aenter__(self) -> "AbstractDatabaseConnection":
        """
        The connection shall be an asynchronous context manager. Leaving the context without calling the `commit` method shall
        result in a rollback.
        """
        ...

    @abc.abstractmethod
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """
        The connection shall be an asynchronous context manager. Leaving the context without calling the `commit` method shall
        result in a rollback.
        """
        ...


class AbstractQueryExecutor(AbstractDatabaseConnection, Generic[TRawConnection]):
    "Interface that database connections are expected to implement in a database plugin."

    @abc.abstractmethod
    async def execute(
        self,
        query: Callable[[TRawConnection], Awaitable[TReturn]],
        return_type: Optional[Type[TReturn]] = None,
    ) -> TReturn:
        """
        Executes the given database query with the given type of return value.
        """
        ...
