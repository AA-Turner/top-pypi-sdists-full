from abc import ABC, abstractmethod
from collections.abc import Sequence
from types import TracebackType
from typing import Any, Protocol, Self

from csrd.models.model_parser import PayloadExtractor

from .execute_result import ExecuteResult


class DBProtocol(Protocol):
    """Protocol defining a pluggable interface for database operations.

    Implementations must support an async lifecycle (``connect`` / ``close``)
    and the standard query / mutation methods.
    """

    @property
    def extractor(self) -> PayloadExtractor:
        """The extractor used to parse raw DB rows into structured data."""
        ...

    async def connect(self) -> None:
        """Open the underlying database connection (or pool)."""
        ...

    async def close(self) -> None:
        """Close the underlying database connection (or pool)."""
        ...

    async def fetch_one(self, query: str, params: dict[str, Any] | None = None) -> dict | None:
        """Fetch a single row from the database."""
        ...

    async def fetch_all(self, query: str, params: dict[str, Any] | None = None) -> Sequence[dict]:
        """Fetch multiple rows from the database."""
        ...

    async def execute(self, query: str, params: dict[str, Any] | None = None) -> int:
        """Execute a DML statement and return the number of rows affected."""
        ...

    async def execute_returning(
        self, query: str, params: dict[str, Any] | None = None
    ) -> ExecuteResult:
        """Execute a statement and return an ``ExecuteResult`` with metadata."""
        ...

    async def insert(self, table: str, values: dict[str, Any]) -> Any:
        """Insert a new row into the specified table."""
        ...

    async def update(self, table: str, values: dict[str, Any], where: dict[str, Any]) -> int:
        """Update existing rows in the table matching the condition."""
        ...

    async def upsert(self, table: str, values: dict[str, Any], where: dict[str, Any]) -> int:
        """Insert or update a row depending on whether the condition is met."""
        ...

    async def delete(self, table: str, where: dict[str, Any]) -> int:
        """Delete rows matching the condition."""
        ...


class ABCDatabaseAdapter(ABC, DBProtocol):
    """Abstract base for concrete database adapters.

    Subclasses must implement ``connect``, ``close``, and all query methods.
    The ``async with`` context-manager protocol is provided for free.
    """

    _dsn: str
    _extractor: PayloadExtractor

    def __init__(self, dsn: str, extractor: PayloadExtractor):
        self._dsn = dsn
        self._extractor = extractor

    @property
    def extractor(self) -> PayloadExtractor:
        return self._extractor

    # ── Lifecycle ────────────────────────────────────────────────────────

    @abstractmethod
    async def connect(self) -> None:
        """Open the underlying connection (or pool). Idempotent."""

    @abstractmethod
    async def close(self) -> None:
        """Close the underlying connection (or pool). Idempotent."""

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    # ── Query interface ──────────────────────────────────────────────────

    @abstractmethod
    async def fetch_one(self, query: str, params: dict[str, Any] | None = None) -> dict | None:
        """Fetch a single row from the database."""

    @abstractmethod
    async def fetch_all(self, query: str, params: dict[str, Any] | None = None) -> Sequence[dict]:
        """Fetch multiple rows from the database."""

    @abstractmethod
    async def execute(self, query: str, params: dict[str, Any] | None = None) -> int:
        """Execute a DML statement and return the number of rows affected."""

    @abstractmethod
    async def execute_returning(
        self, query: str, params: dict[str, Any] | None = None
    ) -> ExecuteResult:
        """Execute a statement and return an ``ExecuteResult`` with metadata."""

    @abstractmethod
    async def insert(self, table: str, values: dict[str, Any]) -> Any:
        """Insert a new row into the specified table."""

    @abstractmethod
    async def update(self, table: str, values: dict[str, Any], where: dict[str, Any]) -> int:
        """Update existing rows in the table matching the condition."""

    @abstractmethod
    async def upsert(self, table: str, values: dict[str, Any], where: dict[str, Any]) -> int:
        """Insert or update a row depending on whether the condition is met."""

    @abstractmethod
    async def delete(self, table: str, where: dict[str, Any]) -> int:
        """Delete rows matching the condition."""
