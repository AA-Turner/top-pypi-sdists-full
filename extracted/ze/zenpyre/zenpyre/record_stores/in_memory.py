"""Provide an in-memory implementation of BaseRecordStore."""

from __future__ import annotations

__all__ = ["InMemoryRecordStore"]

import copy
import logging
from typing import TYPE_CHECKING, Any

from coola.display import InlineDisplayMixin

from zenpyre.record_stores.base import BaseRecordStore

if TYPE_CHECKING:
    from collections.abc import Iterator

    from zenpyre.records import Record

logger: logging.Logger = logging.getLogger(__name__)


class InMemoryRecordStore(BaseRecordStore, InlineDisplayMixin):
    """A :class:`~zenpyre.record_stores.base.BaseRecordStore`
    implementation backed by a plain ``dict``.

    Records are keyed by their ``id`` and held entirely in process
    memory -- nothing is persisted to disk. This is primarily useful
    for testing, small-scale exploration, or pipelines that don't need
    durability.

    Records are deep-copied on both write and read so that mutating a
    :class:`~zenpyre.records.Record` returned by this store (or a
    record passed into :meth:`add_records`) never affects the store's
    internal state. This still matters even though ``Record`` is a
    frozen dataclass: ``frozen=True`` only prevents reassigning the
    ``metadata`` attribute itself, not mutating the dict it points to
    in place (e.g. ``record.metadata["key"] = "value"`` still works).
    This trades some performance for isolation; for very large
    metadata payloads or hot loops, consider a store that doesn't copy
    on every access.

    Example:
        ```pycon
        >>> from zenpyre.records import Record
        >>> from zenpyre.record_stores import InMemoryRecordStore
        >>> store = InMemoryRecordStore()
        >>> store.add_records([Record(id="1", metadata={"source": "hello"})])
        >>> store.count()
        1
        >>> store.get("1").metadata
        {'source': 'hello'}

        ```
    """

    def __init__(self) -> None:
        self._records: dict[str, Record] = {}

    def close(self) -> None:
        # Discard all records: an in-memory store has nothing to persist,
        # so closing (and later reopening via the context manager) it is
        # equivalent to starting over with a fresh, empty store.
        self._records.clear()

    def add_records(self, records: list[Record]) -> None:
        missing_ids = [i for i, record in enumerate(records) if not record.id]
        if missing_ids:
            msg = f"All records must have a non-empty id. Missing id at index(es): {missing_ids}"
            raise ValueError(msg)

        for record in records:
            self._records[record.id] = copy.deepcopy(record)

        logger.debug("Added/replaced %d record(s)", len(records))

    def get(self, record_id: str) -> Record | None:
        record = self._records.get(record_id)
        return copy.deepcopy(record) if record is not None else None

    def get_many(self, record_ids: list[str]) -> list[Record | None]:
        return [self.get(record_id) for record_id in record_ids]

    def filter(self, **metadata_filters: Any) -> list[Record]:
        if not metadata_filters:
            return self.all()

        matches = [
            record
            for record in self._records.values()
            if all(record.metadata.get(key) == value for key, value in metadata_filters.items())
        ]
        return [copy.deepcopy(record) for record in matches]

    def delete(self, record_id: str) -> None:
        self._records.pop(record_id, None)

    def delete_many(self, record_ids: list[str]) -> None:
        for record_id in record_ids:
            self.delete(record_id)

    def check_ids(self, record_ids: list[str]) -> tuple[list[str], list[str]]:
        found = [record_id for record_id in record_ids if record_id in self._records]
        missing = [record_id for record_id in record_ids if record_id not in self._records]
        return found, missing

    def all(self) -> list[Record]:
        return [copy.deepcopy(record) for record in self._records.values()]

    def iter_batches(self, batch_size: int = 1000) -> Iterator[list[Record]]:
        if batch_size < 1:
            msg = f"batch_size must be a positive integer, got {batch_size}"
            raise ValueError(msg)

        batch = []
        for record in self._records.values():
            batch.append(copy.deepcopy(record))
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

    def count(self) -> int:
        return len(self._records)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {}
