"""Iceberg writes that survive a concurrent commit.

pyiceberg asserts that the branch still points at the snapshot it saw when the
table was loaded, so any commit that lands in between, such as the platform's
table maintenance rewriting files, fails the write with
``CommitFailedException``. The write itself is still valid; the fix is to load
the table again and redo the whole operation, which is what these helpers do.

Only ``CommitFailedException`` is retried. ``CommitStateUnknownException``
means the commit may have landed, so repeating it could write twice.
"""

from __future__ import annotations

import logging
import random
import time
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pyarrow as pa
    from pyiceberg.catalog import Catalog
    from pyiceberg.expressions import BooleanExpression
    from pyiceberg.table import Table

log = logging.getLogger(__name__)

COMMIT_ATTEMPTS = 5
BASE_DELAY = 0.5
MAX_DELAY = 10.0

__all__ = [
    "COMMIT_ATTEMPTS",
    "append",
    "commit_with_retry",
    "delete",
    "overwrite",
    "upsert",
]


def retry_commit[T](
    load: Callable[[], Table],
    operation: Callable[[Table], T],
    *,
    name: str,
    attempts: int = COMMIT_ATTEMPTS,
    base_delay: float = BASE_DELAY,
    max_delay: float = MAX_DELAY,
) -> T:
    """Run ``operation(load())``, loading again and repeating on a commit conflict."""
    from pyiceberg.exceptions import CommitFailedException

    if attempts < 1:
        raise ValueError("attempts must be at least 1")
    for attempt in range(1, attempts + 1):
        table = load()
        try:
            return operation(table)
        except CommitFailedException:
            if attempt == attempts:
                raise
            delay = min(base_delay * 2 ** (attempt - 1), max_delay) * (
                0.5 + random.random() / 2
            )
            log.warning(
                "commit conflict on %s (attempt %d/%d), retrying in %.1fs",
                name,
                attempt,
                attempts,
                delay,
            )
            time.sleep(delay)
    raise AssertionError("unreachable")


def commit_with_retry[T](
    catalog: Catalog,
    identifier: str,
    operation: Callable[[Table], T],
    *,
    attempts: int = COMMIT_ATTEMPTS,
    base_delay: float = BASE_DELAY,
    max_delay: float = MAX_DELAY,
) -> T:
    """Run a write against a freshly loaded table, repeating it on a commit conflict.

    ``operation`` receives the table and is called again, with a newly loaded
    table, each time the commit conflicts, so it must do all of its reading
    inside the call and be safe to run again from scratch.

    Args:
        catalog: The catalog to load the table from.
        identifier: Fully qualified ``namespace.table``.
        operation: The write, e.g. ``lambda t: t.append(batch)``.
        attempts: Total tries, including the first.
        base_delay: Seconds before the second try; doubles per retry, with jitter.
        max_delay: Upper bound for one wait, in seconds.

    Returns:
        Whatever ``operation`` returns.

    Raises:
        pyiceberg.exceptions.CommitFailedException: After ``attempts`` conflicts.

    Example:
        >>> commit_with_retry(catalog, "sales.orders", lambda t: t.append(batch))
    """
    return retry_commit(
        lambda: catalog.load_table(identifier),
        operation,
        name=identifier,
        attempts=attempts,
        base_delay=base_delay,
        max_delay=max_delay,
    )


def append(catalog: Catalog, identifier: str, data: pa.Table, **retry: Any) -> None:
    """``table.append(data)``, retried on a commit conflict. See `commit_with_retry`."""
    commit_with_retry(catalog, identifier, lambda t: t.append(data), **retry)


def overwrite(
    catalog: Catalog,
    identifier: str,
    data: pa.Table,
    overwrite_filter: BooleanExpression | str | None = None,
    **retry: Any,
) -> None:
    """``table.overwrite(data, overwrite_filter)``, retried on a commit conflict."""
    from pyiceberg.expressions import AlwaysTrue

    where = AlwaysTrue() if overwrite_filter is None else overwrite_filter
    commit_with_retry(
        catalog, identifier, lambda t: t.overwrite(data, overwrite_filter=where), **retry
    )


def upsert(
    catalog: Catalog,
    identifier: str,
    data: pa.Table,
    join_cols: list[str] | None = None,
    **retry: Any,
) -> Any:
    """``table.upsert(data, join_cols)``, retried on a commit conflict.

    Returns:
        pyiceberg's ``UpsertResult`` from the attempt that succeeded.
    """
    return commit_with_retry(
        catalog, identifier, lambda t: t.upsert(data, join_cols=join_cols), **retry
    )


def delete(
    catalog: Catalog,
    identifier: str,
    delete_filter: BooleanExpression | str,
    **retry: Any,
) -> None:
    """``table.delete(delete_filter)``, retried on a commit conflict."""
    commit_with_retry(catalog, identifier, lambda t: t.delete(delete_filter), **retry)
