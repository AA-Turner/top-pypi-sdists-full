r"""Provide a concrete factory that creates a SQLite-backed
BaseRecordStore."""

from __future__ import annotations

__all__ = ["SQLiteRecordStoreFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin
from coola.utils.path import sanitize_path

from zenpyre.record_stores import SQLiteRecordStore
from zenpyre.record_stores.factory.base import BaseRecordStoreFactory

if TYPE_CHECKING:
    from pathlib import Path

    from zenpyre.record_stores.base import BaseRecordStore


class SQLiteRecordStoreFactory(BaseRecordStoreFactory, MultilineDisplayMixin):
    """A concrete BaseRecordStore factory that builds a
    :class:`~zenpyre.record_stores.SQLiteRecordStore` backed by a SQLite
    file at a given path.

    Use this when you want a factory that lazily constructs a
    fresh :class:`~zenpyre.record_stores.SQLiteRecordStore` at
    ``path`` (via
    :meth:`~zenpyre.record_stores.SQLiteRecordStore.from_path`) each
    time :meth:`make_record_store` is called, rather than wrapping an
    already-instantiated store.

    Args:
        path: The path to the SQLite file used to back the record
            store, or ``":memory:"`` for an in-memory database.
        read_only: If ``True``, open the database in read-only mode.
            The database file must already exist.
        **kwargs: Additional keyword arguments forwarded to
            :meth:`~zenpyre.record_stores.SQLiteRecordStore.from_path`.

    Example:
        ```pycon
        >>> from pathlib import Path
        >>> from zenpyre.record_stores.factory import SQLiteRecordStoreFactory
        >>> factory = SQLiteRecordStoreFactory(Path("/tmp/my_app/records.sqlite"))
        >>> record_store = factory.make_record_store()  # doctest: +SKIP

        ```
    """

    def __init__(self, path: Path | str, read_only: bool = False, **kwargs: Any) -> None:
        self._path = sanitize_path(path) if str(path) != ":memory:" else path
        self._read_only = read_only
        self._kwargs = kwargs

    def make_record_store(self) -> BaseRecordStore:
        return SQLiteRecordStore.from_path(self._path, read_only=self._read_only, **self._kwargs)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"path": self._path, "read_only": self._read_only} | self._kwargs
