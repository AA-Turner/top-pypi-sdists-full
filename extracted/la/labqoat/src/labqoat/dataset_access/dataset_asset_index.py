"""Bounded-memory membership for assets discovered only in schema-annotated dataset rows."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import RLock
from typing import TYPE_CHECKING

from labqoat.argument_codec import encode_result
from labqoat.references import AssetRef, ResourceId
from labqoat.schemas.identity import Identity

if TYPE_CHECKING:
    import sqlite3


class DatasetAssetIndex:
    """Own a private disk index so reading large datasets never retains every reference in RAM."""

    def __init__(self) -> None:
        """Defer filesystem work until an annotated reference is actually read."""
        self._directory: TemporaryDirectory[str] | None = None
        self._connection: sqlite3.Connection | None = None
        self._lock = RLock()

    def add(self, assets: Iterable[AssetRef], revision_id: ResourceId) -> None:
        """Deduplicate complete identities while preserving a pinned owner for scoped downloads."""
        with self._lock:
            for asset in assets:
                self._database().execute(
                    "INSERT OR IGNORE INTO refs VALUES (?, ?)",
                    (Identity.bytes(encode_result(asset)), str(revision_id)),
                )

    def revision(self, asset: AssetRef) -> ResourceId | None:
        """Look up exact metadata without granting authority to a changed asset descriptor."""
        with self._lock:
            if self._connection is None:
                return None
            row = self._connection.execute(
                "SELECT revision FROM refs WHERE identity = ?", (Identity.bytes(encode_result(asset)),)
            ).fetchone()
            return None if row is None else ResourceId.parse(str(row[0]))

    def _database(self) -> sqlite3.Connection:
        """Create one private SQLite database with a fixed cache budget under the ownership lock."""
        import sqlite3

        if self._connection is None:
            self._directory = TemporaryDirectory(prefix="labqoat-dataset-references-")
            self._connection = sqlite3.connect(
                Path(self._directory.name) / "references.sqlite3", check_same_thread=False
            )
            self._connection.execute("PRAGMA cache_size = -2048")
            self._connection.execute("CREATE TABLE refs (identity BLOB PRIMARY KEY, revision TEXT NOT NULL)")
        return self._connection

    def close(self) -> None:
        """Release and remove all discovered reference evidence when the provider scope ends."""
        with self._lock:
            if self._connection is not None:
                self._connection.close()
                self._connection = None
            if self._directory is not None:
                self._directory.cleanup()
                self._directory = None
