"""An Iceberg index of what actually landed in the generic tables.

Lakekeeper records only a location for a generic table — no file list — so
neither the catalog nor the console can say which objects exist under one. This
table is that record.

The schema deliberately carries no source-format knowledge: `product`,
`run_date`, `cycle` and `forecast_hour` are all optional, and anything else goes
in `attributes`. The prior art required `product` and `forecast_hour`, which is
numerical-weather-prediction knowledge that a package indexing invoices should
not have to satisfy.
"""

from __future__ import annotations

import logging
import random
import time
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, Protocol

from databaas_utils.catalog import CatalogClient, rest_catalog
from databaas_utils.settings import LakehouseSettings

if TYPE_CHECKING:
    import pyarrow as pa

log = logging.getLogger(__name__)

DEFAULT_INDEX_TABLE = "files"
COMMIT_ATTEMPTS = 5


@dataclass
class FileRecord:
    """One stored object, as the index describes it.

    Args:
        uri: The object's full URI.
        key: Its key within the generic table.
        size_bytes: Size in bytes.
        product: Optional product/dataset name.
        run_date: Optional run date, ``YYYYMMDD``.
        cycle: Optional cycle within the run date, e.g. ``"00"``.
        forecast_hour: Optional forecast lead time in hours.
        attributes: Free-form string metadata.
        ingested_at: When it landed; defaults to now (UTC).
    """

    uri: str
    key: str
    size_bytes: int
    product: str | None = None
    run_date: str | None = None
    cycle: str | None = None
    forecast_hour: int | None = None
    attributes: dict[str, str] = field(default_factory=dict)
    ingested_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def as_row(self) -> dict[str, Any]:
        """The record as a column-name to value mapping, matching :func:`arrow_schema`."""
        return {
            "uri": self.uri,
            "key": self.key,
            "product": self.product,
            "run_date": self.run_date,
            "cycle": self.cycle,
            "forecast_hour": self.forecast_hour,
            "size_bytes": self.size_bytes,
            "attributes": self.attributes or None,
            "ingested_at": self.ingested_at,
        }


def iceberg_schema():
    """The index table's Iceberg schema. Field ids are part of the table format."""
    from pyiceberg.schema import Schema
    from pyiceberg.types import (
        IntegerType,
        LongType,
        MapType,
        NestedField,
        StringType,
        TimestamptzType,
    )

    return Schema(
        NestedField(1, "uri", StringType(), required=True),
        NestedField(2, "key", StringType(), required=True),
        NestedField(3, "product", StringType(), required=False),
        NestedField(4, "run_date", StringType(), required=False),
        NestedField(5, "cycle", StringType(), required=False),
        NestedField(6, "forecast_hour", IntegerType(), required=False),
        NestedField(7, "size_bytes", LongType(), required=True),
        NestedField(
            9,
            "attributes",
            # value_required=False matches pyarrow's map_(), whose value field
            # is nullable. Requiring it here makes pyiceberg reject every
            # append with a schema mismatch on field 11.
            MapType(10, StringType(), 11, StringType(), value_required=False),
            required=False,
        ),
        NestedField(8, "ingested_at", TimestamptzType(), required=True),
    )


def arrow_schema() -> pa.Schema:
    """The pyarrow mirror of `iceberg_schema()`, used to build the append batch."""
    import pyarrow as pa

    return pa.schema(
        [
            pa.field("uri", pa.string(), nullable=False),
            pa.field("key", pa.string(), nullable=False),
            pa.field("product", pa.string(), nullable=True),
            pa.field("run_date", pa.string(), nullable=True),
            pa.field("cycle", pa.string(), nullable=True),
            pa.field("forecast_hour", pa.int32(), nullable=True),
            pa.field("size_bytes", pa.int64(), nullable=False),
            pa.field("attributes", pa.map_(pa.string(), pa.string()), nullable=True),
            pa.field("ingested_at", pa.timestamp("us", tz="UTC"), nullable=False),
        ]
    )


class Index(Protocol):
    """Something that records ingested files and knows the newest run.

    Implemented by :class:`FileIndex` and :class:`NullIndex`.
    """

    def record(self, *records: FileRecord) -> None:
        """Record that these files landed."""
        ...

    def latest(self) -> str | None:
        """The newest ``run_date`` + ``cycle`` recorded, or ``None``."""
        ...


class FileIndex(Index):
    """Appends rows to `<namespace>.<table>`, creating the table on first use.

    Needs the ``iceberg`` extra.

    Args:
        settings: Which warehouse and namespace, as which identity.
        table: Index table name.
        catalog: A pyiceberg catalog to use instead of building one.
        client: A ``CatalogClient`` to reuse.

    Example:
        >>> index = FileIndex(settings)
        >>> index.record(FileRecord(uri=uri, key="run.grib2", size_bytes=1024))
        >>> index.latest()
        '2026093000'
    """

    def __init__(
        self,
        settings: LakehouseSettings,
        table: str = DEFAULT_INDEX_TABLE,
        *,
        catalog: Any = None,
        client: CatalogClient | None = None,
    ) -> None:
        self.settings = settings
        self.table = table
        self._catalog = catalog
        self.client = client

    @property
    def identifier(self) -> str:
        """The Iceberg identifier, ``<namespace>.<table>``."""
        return f"{self.settings.namespace}.{self.table}"

    @property
    def catalog(self) -> Any:
        """The pyiceberg catalog, built on first use."""
        if self._catalog is None:
            self._catalog = rest_catalog(self.settings)
        return self._catalog

    def _load_or_create(self) -> Any:
        from pyiceberg.exceptions import NoSuchTableError, TableAlreadyExistsError

        try:
            return self.catalog.load_table(self.identifier)
        except NoSuchTableError:
            log.info("creating iceberg index table %s", self.identifier)
            self.catalog.create_namespace_if_not_exists(self.settings.namespace)
            try:
                return self.catalog.create_table(self.identifier, schema=iceberg_schema())
            except TableAlreadyExistsError:  # lost the race with a parallel task
                return self.catalog.load_table(self.identifier)

    def record(self, *records: FileRecord) -> None:
        """Append `records` as one commit, retrying if a parallel task wins.

        Raises:
            pyiceberg.exceptions.CommitFailedException: After five conflicting
                attempts.
        """
        if not records:
            return
        from pyiceberg.exceptions import CommitFailedException

        batch = self._batch(records)
        for attempt in range(1, COMMIT_ATTEMPTS + 1):
            table = self._load_or_create()
            try:
                table.append(batch)
                log.info("indexed %d file(s) in %s", len(records), self.identifier)
                return
            except CommitFailedException:
                if attempt == COMMIT_ATTEMPTS:
                    raise
                delay = min(2**attempt, 10) * (0.5 + random.random() / 2)
                log.warning(
                    "commit conflict on %s (attempt %d/%d), retrying in %.1fs",
                    self.identifier,
                    attempt,
                    COMMIT_ATTEMPTS,
                    delay,
                )
                time.sleep(delay)

    def latest(self) -> str | None:
        """The newest ``run_date || cycle``, or None if there is no index yet.

        Three outcomes, kept distinct on purpose: no table means nothing was
        ever ingested (None); a table with no run identity means the same
        (None); a table that exists but cannot be read is a real failure and
        **raises** — it must not look like "nothing ingested" to a caller
        deciding whether to re-ingest.
        """
        from pyiceberg.exceptions import NoSuchTableError

        try:
            table = self.catalog.load_table(self.identifier)
        except NoSuchTableError:
            log.info("no index table %s yet — nothing has been ingested", self.identifier)
            return None

        rows = table.scan(selected_fields=("run_date", "cycle")).to_arrow()
        stamps = [
            f"{run_date}{cycle}"
            for run_date, cycle in zip(
                rows.column("run_date").to_pylist(),
                rows.column("cycle").to_pylist(),
                strict=True,
            )
            if run_date and cycle
        ]
        latest = max(stamps, default=None)
        log.info(
            "newest run in %s: %s (%d row(s))", self.identifier, latest, rows.num_rows
        )
        return latest

    def scan(self, **kwargs: Any) -> pa.Table:
        """The index as an Arrow table. Raises if the table does not exist.

        Args:
            **kwargs: Passed to pyiceberg's ``Table.scan`` (``row_filter``,
                ``selected_fields``, ``limit``, ...).
        """
        return self.catalog.load_table(self.identifier).scan(**kwargs).to_arrow()

    def _batch(self, records: Sequence[FileRecord]) -> pa.Table:
        import pyarrow as pa

        return pa.Table.from_pylist([r.as_row() for r in records], schema=arrow_schema())


@dataclass
class NullIndex(Index):
    """No catalog to index into (laptop runs) — just say what would happen."""

    def record(self, *records: FileRecord) -> None:
        """Log what would have been indexed."""
        for record in records:
            log.info("would index %s (%d bytes)", record.uri, record.size_bytes)

    def latest(self) -> str | None:
        """Always ``None``."""
        return None
