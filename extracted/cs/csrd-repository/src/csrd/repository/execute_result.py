from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecuteResult:
    """Immutable snapshot of metadata from an executed SQL statement.

    Returned by ``execute_returning`` so callers can inspect ``lastrowid``
    and ``rowcount`` without holding a reference to a raw database cursor
    (which may be invalidated when the connection or transaction closes).
    """

    rowcount: int
    lastrowid: int | None = None
