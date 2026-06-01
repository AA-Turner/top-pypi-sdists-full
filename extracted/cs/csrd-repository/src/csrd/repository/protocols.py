"""Backend-agnostic protocols for database cursor and row objects."""

from collections.abc import Iterator
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class CursorLike(Protocol):
    """Backend-agnostic contract for DB cursor-like objects."""

    @property
    def rowcount(self) -> int:
        """Number of rows affected by last operation."""
        ...

    @property
    def lastrowid(self) -> int | None:
        """ID of the last inserted row, if applicable."""
        ...

    def __getitem__(self, key: Any) -> Any:
        """Support for key or index access to rows."""
        ...

    def __iter__(self) -> Iterator[Any]:
        """Support for iteration over rows."""
        ...


@runtime_checkable
class RowLike(Protocol):
    """Represents a single row from a database cursor result."""

    def __getitem__(self, key: Any) -> Any:
        """Allows key or index-based access to column values."""
        ...

    def keys(self) -> list[str]:
        """Returns a list of column names for key-based access."""
        ...

    def __iter__(self) -> Iterator[Any]:
        """Allows iteration over column values."""
        ...
