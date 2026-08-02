r"""Provide a concrete factory that creates a DuckDB-backed
BaseRecordStore."""

from __future__ import annotations

__all__ = ["DuckDBRecordStoreFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.record_stores import DuckDBRecordStore
from zenpyre.record_stores.factory.base import BaseRecordStoreFactory
from zenpyre.utils.duckdb import prepare_duckdb_path
from zenpyre.utils.imports import check_duckdb

if TYPE_CHECKING:
    from pathlib import Path

    from zenpyre.record_stores.base import BaseRecordStore


class DuckDBRecordStoreFactory(BaseRecordStoreFactory, MultilineDisplayMixin):
    """A concrete BaseRecordStore factory that builds a
    :class:`~zenpyre.record_stores.DuckDBRecordStore` backed by a DuckDB
    file at a given path.

    Use this when you want a factory that lazily constructs a
    fresh :class:`~zenpyre.record_stores.DuckDBRecordStore` at
    ``path`` each time :meth:`make_record_store` is called, rather
    than wrapping an already-instantiated store.

    Args:
        path: The path to the DuckDB file used to back the record
            store.
        **kwargs: Additional keyword arguments forwarded to
            :class:`~zenpyre.record_stores.DuckDBRecordStore`.

    Example:
        ```pycon
        >>> from pathlib import Path
        >>> from zenpyre.record_stores.factory import DuckDBRecordStoreFactory
        >>> factory = DuckDBRecordStoreFactory(Path("/tmp/my_app/records.duckdb"))
        >>> record_store = factory.make_record_store()  # doctest: +SKIP

        ```
    """

    def __init__(self, path: Path | str, **kwargs: Any) -> None:
        check_duckdb()
        self._path = prepare_duckdb_path(path)
        self._kwargs = kwargs

    def make_record_store(self) -> BaseRecordStore:
        return DuckDBRecordStore(self._path, **self._kwargs)

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {"path": self._path} | self._kwargs
