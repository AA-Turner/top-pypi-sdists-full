r"""Provide the abstract base class for record stores."""

from __future__ import annotations

__all__ = ["BaseRecordStore"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Generator, Iterator
    from typing import Self

    from zenpyre.records import Record


class BaseRecordStore(ABC):
    """Abstract base class for record stores.

    Defines the common interface that all record store implementations
    must provide.  A concrete implementation would be, for example,
    :class:`~zenpyre.record_stores.InMemoryRecordStore`.

    To implement a custom record store, subclass
    :class:`BaseRecordStore` and implement all abstract methods.

    Implementations are expected to support use as a context manager
    (``with SomeRecordStore(...) as store: ...``), which calls
    :meth:`close` automatically on exit.
    """

    @abstractmethod
    def add_records(self, records: list[Record]) -> None:
        """Add or replace records in the store.

        Records whose ``id`` already exists are replaced (upsert
        semantics).  Since :class:`~zenpyre.records.Record` always has
        a required ``id``, implementations do not need to validate its
        presence, though they may still choose to reject an empty
        string.

        Args:
            records: The list of :class:`~zenpyre.records.Record`
                instances to add.
        """

    @abstractmethod
    def get(self, record_id: str) -> Record | None:
        """Retrieve a single record by its ID.

        Args:
            record_id: The record ID to look up.

        Returns:
            The :class:`~zenpyre.records.Record`, or ``None`` if not
                found.
        """

    @abstractmethod
    def get_many(self, record_ids: list[str]) -> list[Record | None]:
        """Retrieve multiple records by their IDs.

        Args:
            record_ids: The record IDs to look up.

        Returns:
            A list the same length as ``record_ids``, with the
                corresponding :class:`~zenpyre.records.Record` for
                each ID that exists, or ``None`` for IDs not found.
        """

    @abstractmethod
    def filter(self, **metadata_filters: Any) -> list[Record]:
        """Retrieve records matching all provided metadata filters.

        All filters should be combined with ``AND``.  Each keyword
        argument matches the corresponding metadata key exactly.

        Args:
            **metadata_filters: Key-value pairs where each key is a
                metadata field name and the value is the exact value
                to match.  Calling with no arguments should return all
                records.

        Returns:
            A list of matching :class:`~zenpyre.records.Record`
                instances.
        """

    @abstractmethod
    def delete(self, record_id: str) -> None:
        """Delete a record by its ID.

        IDs that do not exist should be silently ignored.

        Args:
            record_id: The ID of the record to delete.
        """

    @abstractmethod
    def delete_many(self, record_ids: list[str]) -> None:
        """Delete multiple records by their IDs.

        IDs that do not exist should be silently ignored.

        Args:
            record_ids: The IDs of the records to delete.
        """

    @abstractmethod
    def check_ids(self, record_ids: list[str]) -> tuple[list[str], list[str]]:
        """Check which record IDs exist in the store.

        Args:
            record_ids: The record IDs to check.

        Returns:
            A tuple of two lists: ``(found, missing)`` where ``found``
                contains the IDs that exist in the store and
                ``missing`` contains the IDs that do not.
        """

    @abstractmethod
    def all(self) -> list[Record]:
        """Return all records in the store.

        Returns:
            A list of all :class:`~zenpyre.records.Record` instances
                currently in the store.
        """

    def lazy_all(self, batch_size: int = 32) -> Iterator[Record]:
        """Lazily iterate over all records without loading them all into
        memory at once.

        This is the streaming equivalent of :meth:`all`. The default
        implementation delegates to :meth:`iter_batches` and flattens
        the batches; implementations may override this with a more
        direct row-by-row cursor for a smaller memory footprint.

        Args:
            batch_size: The batch size used internally when pulling
                records from the underlying store. Does not affect the
                granularity of what is yielded -- records are always
                yielded one at a time.

        Yields:
            One :class:`~zenpyre.records.Record` at a time, in the
                same order as :meth:`all`.

        Example:
            ```pycon
            >>> from zenpyre.record_stores import InMemoryRecordStore
            >>> from zenpyre.records import Record
            >>> store = InMemoryRecordStore()
            >>> store.add_records([Record(id=str(i), metadata={"index": i}) for i in range(3)])
            >>> for record in store.lazy_all():
            ...     print(record.id)
            ...
            0
            1
            2

            ```
        """
        for batch in self.iter_batches(batch_size=batch_size):
            yield from batch

    @abstractmethod
    def iter_batches(self, batch_size: int = 32) -> Generator[list[Record], None, None]:
        """Yield records in batches, avoiding loading the whole store
        into memory at once.

        This is the scalable equivalent of :meth:`all`: instead of
        materializing every record as a single list, it streams them
        from the database in chunks of ``batch_size``.

        Args:
            batch_size: The maximum number of records to yield per
                batch. Must be a positive integer.

        Yields:
            Lists of records, each with at most ``batch_size``
                elements, in the same order as :meth:`all`. The last
                batch may contain fewer than ``batch_size`` records.

        Example:
            ```pycon
            >>> from zenpyre.record_stores import InMemoryRecordStore
            >>> from zenpyre.records import Record
            >>> store = InMemoryRecordStore()
            >>> store.add_records([Record(id=str(i), metadata={"index": i}) for i in range(5)])
            >>> for batch in store.iter_batches(batch_size=2):
            ...     print(len(batch))
            ...
            2
            2
            1

            ```
        """

    @abstractmethod
    def count(self) -> int:
        """Return the total number of records in the store.

        Returns:
            The number of records currently stored.
        """

    @abstractmethod
    def close(self) -> None:
        r"""Close the store and release any underlying resources (e.g.
        database connections, file handles).

        Implementations should make repeated calls to ``close()`` safe
        (i.e. idempotent), since :meth:`__exit__` calls it
        unconditionally and callers may also close a store manually
        before using it as a context manager.
        """

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()
