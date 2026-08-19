# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import contextlib
import hashlib
import itertools
import json
import logging
import os
import platform
import threading
import time
import uuid
import warnings
from collections.abc import Callable, Iterable, Iterator, Sequence
from datetime import timedelta
from functools import cached_property
from typing import Any, Literal, cast
from urllib.parse import unquote, urlparse

import attrs
import lance
import lancedb
import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
from lancedb import AsyncConnection
from lancedb._lancedb import MergeResult, UpdateFieldMetadataResult
from lancedb.common import DATA, VECTOR_COLUMN_NAME, Credential
from lancedb.index import IndexConfig
from lancedb.merge import LanceMergeInsertBuilder
from lancedb.namespace import AsyncLanceNamespaceDBConnection
from lancedb.query import LanceQueryBuilder, LanceTakeQueryBuilder
from lancedb.query import Query as LanceQuery
from lancedb.table import IndexStatistics, TableStatistics, Tags
from lancedb.table import LanceTable as LanceLocalTable
from lancedb.table import Table as LanceTable
from lancedb.types import BlobMode, OnBadVectorsType

# Python 3.10 compatibility
from typing_extensions import TYPE_CHECKING, Never, Optional, override  # noqa: UP035
from yarl import URL

from geneva import telemetry
from geneva._context import get_current_context
from geneva._namespace_client import with_geneva_user_agent
from geneva.checkpoint import CheckpointStore
from geneva.committer import get_committer
from geneva.credentials import refresh_storage_options
from geneva.db import (
    SYSTEM_NAMESPACE,
    Connection,
    NamespaceConfig,
    _as_namespace_client_properties,
    _directory_namespace_storage_properties,
    _get_db_uri,
    connect,
    resolve_table_physical_uri,
)
from geneva.field_metadata_writer import get_field_metadata_writer
from geneva.partitioning import _VECTOR_INDEX_TYPE_URLS
from geneva.plan import BackfillPlan, RefreshPlan
from geneva.query import (
    MATVIEW_META_BASE_VERSION,
    MATVIEW_META_CHUNKER,
    MATVIEW_META_QUERY,
    MATVIEW_META_SCALAR_UDTF,
    MATVIEW_META_UDTF,
    MATVIEW_META_VERSION,
    MATVIEW_VERSION_CHUNKER,
    MATVIEW_VERSION_SCALAR_UDTF,
    GenevaQueryBuilder,
)
from geneva.table_writer import get_table_writer
from geneva.transformer import (
    UDF,
    UDTF,
    Chunker,
    UDFArgType,
    UnpackedUDF,
    UnpackedUDFField,
)
from geneva.utils import redact_dict_values, status_updates
from geneva.utils.batch_size import resolve_batch_size
from geneva.utils.remote_options import build_remote_request
from geneva.utils.schema import canonical_field_paths, resolve_arrow_field_path

if TYPE_CHECKING:
    import pandas as pd
    from lance_namespace import LanceNamespace

    from geneva.jobs.types import BackfillJobResult, Job, RefreshJobResult


def _normalize_file_uri(uri: str) -> str:
    parsed = urlparse(uri)
    if parsed.scheme == "file":
        return unquote(parsed.path)
    return uri


_LOG = logging.getLogger(__name__)

_IVF_PARTITION_COL = "_ivf_partition"
_UDTF_INDEX_ROW_ID_CHUNK_SIZE = 100_000
_UDTF_PARTITION_DISTINCT_BATCH_SIZE = 65_536
_LANCE_INCLUDE_VECTOR_CENTROIDS_ENV = "LANCE_INCLUDE_VECTOR_CENTROIDS"
_INDEX_STATS_ENV_LOCK = threading.Lock()

# Lance internal columns are virtual: they are synthesized per query rather than
# stored, so they never appear in the physical schema ``Table.schema`` returns.
# ``take_row_ids()`` still surfaces them, both as uint64.
_LANCE_INTERNAL_COLUMN_TYPES: dict[str, pa.DataType] = {
    "_rowid": pa.uint64(),
    "_rowaddr": pa.uint64(),
}

# Blob columns are stored as ``large_binary`` but read back as a descriptor
# struct, so a projected schema has to mirror the read rather than storage.
_LANCE_BLOB_ENCODING_META_KEY = b"lance-encoding:blob"
_LANCE_BLOB_DESCRIPTOR_TYPE = pa.struct(
    [
        pa.field("position", pa.uint64()),
        pa.field("size", pa.uint64()),
    ]
)

# Metadata key for tracking the last successfully refreshed source version
MATVIEW_LAST_REFRESHED_VERSION = "geneva::mv::last_refreshed_version"
_IMPLICIT_LOCAL_RAY_WARNING = (
    "You are implicitly using a local Ray cluster for %s. "
    "If you want this to continue to work and ensure proper cleanup, "
    "wrap your call in a context: conn.local_ray_context()."
)
# Lance computed columns are SQL expressions evaluated by Lance itself, and are
# distinct from Geneva's UDF-backed virtual columns. Geneva declares neither
# kind through the Lance API, so declaring one warns and refreshing one raises.
_COMPUTED_COLUMN_MIN_LANCEDB = "0.38"
_COMPUTED_COLUMN_SIGNATURE = 'add_columns(computed={"<column>": "<sql expr>"})'
_VIRTUAL_COLUMN_META_FLAG = "virtual_column"
_UNPACK_META_FLAG = "virtual_column.unpack"
_UNPACK_META_GROUP = "virtual_column.unpack_group"
_UNPACK_META_FIELD = "virtual_column.unpack_field"
_UNPACK_META_FIELDS = "virtual_column.unpack_fields"


def _computed_column_unsupported(operation: str) -> NotImplementedError:
    """Build the error for a Lance computed column operation Geneva lacks."""
    return NotImplementedError(
        f"{operation} is not supported. It fills Lance computed columns, "
        f"added in lancedb {_COMPUTED_COLUMN_MIN_LANCEDB}; Geneva does not "
        f"declare them yet, see {_COMPUTED_COLUMN_SIGNATURE}."
    )


@attrs.define(frozen=True)
class _UnpackBackfillContext:
    fields: tuple[UnpackedUDFField, ...]

    @property
    def columns(self) -> list[str]:
        return [field.output_column for field in self.fields]

    @property
    def checkpoint_column(self) -> str:
        return self.columns[0]

    @property
    def default_where(self) -> str:
        return " OR ".join(f"{col} IS NULL" for col in self.columns)


def _is_intentional_full_reprocess_where(where: str | None) -> bool:
    if where is None:
        return False
    return "".join(where.split()) == "1=1"


def _request_model_supports_field(request_cls: type[Any], field_name: str) -> bool:
    fields = getattr(request_cls, "model_fields", None)
    if fields is None:
        fields = getattr(request_cls, "__fields__", {})
    return field_name in fields


def _metadata_to_str_dict(metadata: dict[bytes, bytes] | None) -> dict[str, str]:
    if not metadata:
        return {}
    result: dict[str, str] = {}
    for key, value in metadata.items():
        key_str = key.decode("utf-8") if isinstance(key, bytes) else str(key)
        value_str = value.decode("utf-8") if isinstance(value, bytes) else str(value)
        result[key_str] = value_str
    return result


def _without_virtual_column_metadata(field: pa.Field) -> pa.Field:
    metadata = {}
    for key, value in (field.metadata or {}).items():
        try:
            key_str = key.decode("utf-8") if isinstance(key, bytes) else str(key)
        except UnicodeDecodeError:
            metadata[key] = value
            continue
        if key_str == _VIRTUAL_COLUMN_META_FLAG or key_str.startswith(
            f"{_VIRTUAL_COLUMN_META_FLAG}."
        ):
            continue
        metadata[key] = value
    return pa.field(
        field.name,
        field.type,
        nullable=field.nullable,
        metadata=metadata or None,
    )


def _unpack_group_id(udf: UDF, output_columns: list[str]) -> str:
    hasher = hashlib.sha256()
    hasher.update(udf.name.encode("utf-8"))
    hasher.update(b"\0")
    hasher.update((udf.version or "").encode("utf-8"))
    hasher.update(b"\0")
    hasher.update("\n".join(output_columns).encode("utf-8"))
    return hasher.hexdigest()[:16]


def _normalize_backfill_columns(columns: "str | list[str]") -> str:
    """Normalize the ``columns`` argument accepted by ``backfill()`` and
    ``backfill_async()``.

    The new signature accepts either a single column name (string) or a
    list of column names (future-proofing for multi-column backfill,
    currently unsupported). A single-element list is unwrapped. An empty
    list is rejected. Multi-element lists raise ``NotImplementedError``.
    """
    if isinstance(columns, str):
        return columns
    if isinstance(columns, list):
        if len(columns) == 0:
            raise ValueError(
                "columns list cannot be empty; pass a column name string "
                "or a non-empty list."
            )
        if len(columns) == 1:
            inner = columns[0]
            if not isinstance(inner, str):
                raise TypeError(
                    f"columns list must contain strings, got {type(inner).__name__}"
                )
            return inner
        raise NotImplementedError(
            "Multi-column backfill is not yet supported. Pass a single "
            "column name string."
        )
    raise TypeError(f"columns must be str or list[str], got {type(columns).__name__}")


def _get_last_refreshed_version(table: "Table") -> int | None:
    """Read last refreshed version from __source_row_id column metadata.

    Returns None if the table doesn't have __source_row_id column or
    if the metadata key doesn't exist (backwards compatibility).
    """
    schema = table.schema
    if "__source_row_id" not in schema.names:
        return None
    field = schema.field("__source_row_id")
    if field.metadata is None:
        return None
    version_bytes = field.metadata.get(MATVIEW_LAST_REFRESHED_VERSION.encode())
    if version_bytes is None:
        return None
    return int(version_bytes.decode())


def _set_last_refreshed_version(table: "Table", version: int) -> None:
    """Write last refreshed version to __source_row_id column metadata."""
    field = table.schema.field("__source_row_id")
    # Convert existing bytes metadata to string dict for update
    existing: dict[str, str] = {}
    if field.metadata:
        for k, v in field.metadata.items():
            key = k.decode() if isinstance(k, bytes) else k
            val = v.decode() if isinstance(v, bytes) else v
            existing[key] = val
    existing[MATVIEW_LAST_REFRESHED_VERSION] = str(version)
    get_field_metadata_writer().update(
        table._ltbl,
        {"path": "__source_row_id", "metadata": existing, "replace": True},
    )


def _await_job_future(
    fut: "JobFuture", timeout_secs: float | None, *, what: str
) -> Any:
    """Block on a job future, honoring an optional timeout.

    ``fut.result(timeout=...)`` surfaces Ray's ``GetTimeoutError`` on expiry, so
    wait via ``fut.done(timeout=...)`` (``False`` on timeout) and raise a plain
    ``TimeoutError``, matching ``backfill``'s timeout behavior. A ``timeout_secs``
    of ``None`` waits unbounded.
    """
    if timeout_secs is None:
        return fut.result()
    if not fut.done(timeout=timeout_secs):
        raise TimeoutError(f"{what} did not complete within {timeout_secs}s")
    return fut.result()


def _plain_api_key(api_key: Any) -> Any:
    """Convert masked Credential wrappers back to their raw string value."""
    if isinstance(api_key, Credential):
        return api_key[:]
    return api_key


def _is_chunker_mv_version(version: str | None) -> bool:
    return version in (MATVIEW_VERSION_CHUNKER, MATVIEW_VERSION_SCALAR_UDTF)


def _get_chunker_metadata(metadata: dict[bytes, bytes]) -> bytes | None:
    return metadata.get(MATVIEW_META_CHUNKER.encode()) or metadata.get(
        MATVIEW_META_SCALAR_UDTF.encode()
    )


class _IndexPartitionSource:
    """Wraps a query builder to inject a constant ``_partition_id`` column.

    When UDTFs are dispatched via ``partition_by_indexed_column``, the
    framework knows the IVF partition ordinal but the UDTF callable only
    sees the source data.  This wrapper intercepts ``to_arrow()`` and
    appends a ``_partition_id`` column so UDTFs can propagate the
    partition identity into their output without requiring the column
    to exist on the source table.
    """

    def __init__(self, inner: Any, partition_id: int) -> None:
        self._inner = inner
        self._partition_id = partition_id

    def _inject_partition_id(
        self, data: pa.Table | pa.RecordBatch
    ) -> pa.Table | pa.RecordBatch:
        if "_partition_id" in data.column_names:
            data = data.remove_column(data.column_names.index("_partition_id"))
        return data.append_column(
            "_partition_id",
            pa.array([self._partition_id] * data.num_rows, type=pa.int32()),
        )

    def to_arrow(self) -> pa.Table:
        return cast("pa.Table", self._inject_partition_id(self._inner.to_arrow()))

    def to_batches(self, *args: Any, **kwargs: Any) -> Iterator[pa.RecordBatch]:
        for batch in self._inner.to_batches(*args, **kwargs):
            yield cast("pa.RecordBatch", self._inject_partition_id(batch))

    def __getattr__(self, name: str) -> Any:
        return getattr(self._inner, name)


class _ChunkedTakeSource:
    """Read source rows via bounded take_row_ids() calls.

    This avoids building one giant Python list of row IDs for a large
    IVF partition before issuing the table reads. ``to_batches()``
    stays bounded across chunked ``take_row_ids()`` calls. ``to_arrow()``
    still materializes the full Arrow table, but streams chunk batches
    into the final result instead of buffering all chunk tables first.
    """

    def __init__(
        self,
        table: "Table",
        row_ids: pa.Array | pa.ChunkedArray,
        *,
        selected_columns: list[str] | None = None,
        chunk_size: int = _UDTF_INDEX_ROW_ID_CHUNK_SIZE,
    ) -> None:
        self._table = table
        self._row_ids = row_ids
        self._selected_columns = selected_columns
        self._chunk_size = chunk_size

    def _iter_queries(self) -> Iterator[Any]:
        for row_id_chunk in _iter_row_id_chunks(self._row_ids, self._chunk_size):
            query_builder = self._table.take_row_ids(row_id_chunk)
            if self._selected_columns:
                query_builder = query_builder.select(self._selected_columns)
            yield query_builder

    def select(self, columns: list[str]) -> "_ChunkedTakeSource":
        return _ChunkedTakeSource(
            self._table,
            self._row_ids,
            selected_columns=columns,
            chunk_size=self._chunk_size,
        )

    def to_batches(self, *args: Any, **kwargs: Any) -> Iterator[pa.RecordBatch]:
        for query_builder in self._iter_queries():
            yield from query_builder.to_batches(*args, **kwargs)

    def to_arrow(self, *args: Any, **kwargs: Any) -> pa.Table:
        batches = self.to_batches(*args, **kwargs)
        try:
            first_batch = next(batches)
        except StopIteration:
            schema = self._table.schema
            if self._selected_columns:
                schema = pa.schema(
                    [
                        _selected_field(schema, column)
                        for column in self._selected_columns
                    ],
                    metadata=cast(
                        "dict[bytes | str, bytes | str] | None", schema.metadata
                    ),
                )
            return schema.empty_table()
        return pa.Table.from_batches(
            itertools.chain([first_batch], batches),
            schema=first_batch.schema,
        )


def _selected_field(schema: pa.Schema, column: str) -> pa.Field:
    """Resolve a selected column to the field ``take_row_ids()`` would return.

    ``schema`` is the physical Lance schema, which diverges from a read's schema
    in three ways an indexed UDTF can hit:

    * internal columns (``_rowid``/``_rowaddr``) are virtual, so they are
      synthesized per query and absent from ``schema`` entirely;
    * nested paths such as ``meta.author`` are not top-level fields, and read
      back as one flat field named with the whole dotted path;
    * blob columns are stored as ``large_binary`` but read back as a
      ``struct<position, size>`` descriptor.

    Resolving through all three keeps an empty partition's schema identical to
    the one a non-empty take produces, so a UDTF sees a single shape either way.
    Physical fields still win over the internal-column fallback, and a column
    matching none of these raises ``KeyError``, so typos stay visible.
    """
    internal_type = _LANCE_INTERNAL_COLUMN_TYPES.get(column)
    if internal_type is not None and column not in schema.names:
        return pa.field(column, internal_type)
    field = _physical_field(schema, column)
    metadata = field.metadata or {}
    if _LANCE_BLOB_ENCODING_META_KEY in metadata:
        return field.with_type(_LANCE_BLOB_DESCRIPTOR_TYPE)
    return field


def _physical_field(schema: pa.Schema, column: str) -> pa.Field:
    """Resolve ``column`` against ``schema``, following dotted nested paths.

    A stored column whose own name contains a dot takes precedence over path
    traversal. The returned field keeps the dotted name a read projects it
    under, so callers can build a projected schema directly from it.
    """
    if column in schema.names or "." not in column:
        # Raises KeyError for an unknown top-level column.
        return schema.field(column)

    root, *rest = column.split(".")
    field = schema.field(root)
    for part in rest:
        if not pa.types.is_struct(field.type):
            raise KeyError(f"Column {column} does not exist in schema")
        try:
            field = field.type.field(part)
        except KeyError as exc:
            raise KeyError(f"Column {column} does not exist in schema") from exc
    return field.with_name(column)


def _iter_row_id_chunks(
    row_ids: pa.Array | pa.ChunkedArray,
    chunk_size: int = _UDTF_INDEX_ROW_ID_CHUNK_SIZE,
) -> Iterator[list[int]]:
    """Yield bounded Python row-id lists from an Arrow array."""
    if chunk_size <= 0:
        raise ValueError(f"chunk_size must be > 0, got {chunk_size}")

    total_rows = len(row_ids)
    for offset in range(0, total_rows, chunk_size):
        yield cast("list[int]", row_ids.slice(offset, chunk_size).to_pylist())


def _sorted_distinct_partition_values(
    src_tbl: "Table", partition_col: str
) -> list[Any]:
    """Return sorted distinct partition values without full-column materialization.

    The working set is bounded by one scanner batch plus the distinct values
    accumulated so far. Each batch is released before the next one is read, so
    peak memory is O(batch_size + cardinality) instead of O(total_rows).

    For example, with a 2M-row table, 3 distinct partition values, and a 65K
    scanner batch size, this processes 31 batches while keeping only the
    current batch and the 3 distinct values in memory.
    """
    from geneva.query import open_read_dataset

    partition_values: set[Any] = set()
    scanner = open_read_dataset(src_tbl).scanner(
        columns=[partition_col],
        batch_size=_UDTF_PARTITION_DISTINCT_BATCH_SIZE,
    )
    for batch in scanner.to_batches():
        partition_values.update(pc.unique(batch.column(partition_col)).to_pylist())
    partition_values.discard(None)
    return sorted(partition_values)


def _iter_udtf_batches_with_stats(
    batches: Iterable[pa.RecordBatch],
) -> tuple[Iterator[pa.RecordBatch] | None, Callable[[], tuple[int, int]]]:
    """Build a streaming batch iterator and a stats getter."""
    iterator = iter(batches)
    try:
        first_batch = next(iterator)
    except StopIteration:
        return None, lambda: (0, 0)

    total_rows = 0
    batch_count = 0

    def _iter_batches() -> Iterator[pa.RecordBatch]:
        nonlocal total_rows, batch_count

        total_rows += first_batch.num_rows
        batch_count += 1
        yield first_batch

        for batch in iterator:
            total_rows += batch.num_rows
            batch_count += 1
            yield batch

    def _stats() -> tuple[int, int]:
        return total_rows, batch_count

    return _iter_batches(), _stats


def _make_udtf_batch_reader(
    batches: Iterable[pa.RecordBatch],
    schema: pa.Schema,
) -> tuple[pa.RecordBatchReader | None, Callable[[], tuple[int, int]]]:
    """Build a streaming RecordBatchReader and a stats getter."""
    tracked_batches, get_stats = _iter_udtf_batches_with_stats(batches)
    if tracked_batches is None:
        return None, get_stats
    return pa.RecordBatchReader.from_batches(schema, tracked_batches), get_stats


def _make_udtf_processor_actor() -> Any:
    """Lazily define the UDTFProcessorActor Ray actor class.

    We wrap the definition in a factory to defer the ``import ray`` until
    Ray is actually needed (table.py is imported even in non-Ray contexts).
    """
    import attrs
    import ray

    @ray.remote  # type: ignore[misc]
    @attrs.define
    class UDTFProcessorActor:  # pyright: ignore[reportRedeclaration]
        """Ray actor that processes a single UDTF partition.

        Expensive initialisation (deserialise the UDTF, open source connection,
        open checkpoint store) happens once in ``__ray_ready__`` so it is
        amortised across all partitions dispatched to this actor.
        """

        udtf_pickle_bytes: bytes
        source_uri: str
        source_name: str
        source_query_json_bytes: bytes | None
        ckp_store_uri: str
        source_api_key: Any = attrs.field(default=None, repr=False)
        source_host_override: str | None = attrs.field(default=None)
        error_handling_pickle_bytes: bytes | None = attrs.field(default=None)
        job_id: str = attrs.field(default="")
        dest_table_uri: str = attrs.field(default="")
        dest_table_name: str = attrs.field(default="")
        source_version: int | None = attrs.field(default=None)
        # Namespace config for source table connection
        namespace_config: NamespaceConfig | None = attrs.field(default=None)
        namespace_path: list[str] | None = attrs.field(default=None)
        dest_data_storage_version: str | None = attrs.field(default=None)

        # Initialised lazily on first process_partition call
        _udtf: Any = attrs.field(init=False, default=None, repr=False)
        _conn: Any = attrs.field(init=False, default=None, repr=False)
        _tbl: Any = attrs.field(init=False, default=None, repr=False)
        _store: Any = attrs.field(init=False, default=None, repr=False)
        _error_config: Any = attrs.field(init=False, default=None, repr=False)
        _storage_options: Any = attrs.field(init=False, default=None, repr=False)
        _initialized: bool = attrs.field(init=False, default=False, repr=False)

        def __ray_ready__(self) -> None:
            self._ensure_initialized()

        def _ensure_initialized(self) -> None:
            if self._initialized:
                return
            import geneva.checkpoint as _ckp
            import geneva.cloudpickle as _cp
            from geneva.db import connect as _connect

            self._udtf = _cp.loads(self.udtf_pickle_bytes)

            ns = self.namespace_config
            assert ns is not None
            self._conn = _connect(
                namespace_client_impl=ns.namespace_client_impl,
                namespace_client_properties=ns.namespace_client_properties,
            )
            self._tbl = self._conn.open_table(
                self.source_name, namespace=self.namespace_path
            )

            if self.source_version is not None:
                self._tbl.checkout(self.source_version)
            self._store = _ckp.CheckpointStore.from_uri(self.ckp_store_uri)
            if self.error_handling_pickle_bytes is not None:
                self._error_config = _cp.loads(self.error_handling_pickle_bytes)

            # Storage options will be fetched when needed with table_id
            self._storage_options = None

            self._initialized = True

        def __repr__(self) -> str:
            try:
                return (
                    f"UDTFProcessorActor(source={self.source_name!r}, "
                    f"store={self.ckp_store_uri!r})"
                )
            except Exception:
                return "<UDTFProcessorActor (repr failed)>"

        def _build_source_query(self, partition_filter: str | None) -> Any:
            """Build the source query, optionally scoped to a partition."""
            from geneva.query import GenevaQuery, GenevaQueryBuilder

            if self.source_query_json_bytes is not None:
                _query = GenevaQuery.model_validate_json(
                    self.source_query_json_bytes.decode()
                )
                query_builder = GenevaQueryBuilder.from_query_object(self._tbl, _query)
            else:
                query_builder = self._tbl.search(None)

            if partition_filter is not None:
                query_builder = query_builder.where(partition_filter)
            return query_builder

        def _execute_with_fragment_write(
            self,
            query_builder: Any,
            partition_prefix: str,
        ) -> tuple[str | None, dict]:
            """Run the UDTF over *query_builder* and write output as a Lance fragment.

            Streams UDTF output batches through a ``RecordBatchReader``
            into ``LanceFragment.create()`` so only one batch is in
            memory at a time.  Checkpoints the lightweight
            ``FragmentMetadata`` JSON for fault-tolerant resume.

            If the actor crashes partway through, the entire partition
            is re-executed on retry.  Orphaned data files from partial
            runs are not referenced by the final commit and are cleaned
            up by Lance GC.

            Returns
            -------
            tuple[str | None, dict]
                ``(fragment_json, stats)`` where *fragment_json* is the
                JSON-serialised ``FragmentMetadata`` (or ``None`` if the
                UDTF produced no output rows), and *stats* contains
                execution timing information.
            """
            import json as _json
            import time

            import pyarrow as pa
            from lance.fragment import LanceFragment

            import geneva.checkpoint_utils as _ckp_utils

            store = self._store
            schema = self._udtf.output_schema
            t_exec_start = time.monotonic()

            fragment_json: str | None = None
            checkpoint_time = 0.0

            reader, get_batch_stats = _make_udtf_batch_reader(
                self._udtf.execute(query_builder),
                schema,
            )

            if reader is not None:
                # Write data files directly into the dest dataset.
                # mode="append" validates against the existing dataset
                # schema and reuses its field IDs.
                # write-guard-ok: chunker/UDTF fragment write, not yet routed
                frag_meta = LanceFragment.create(
                    self.dest_table_uri,
                    reader,
                    schema=schema,
                    mode="append",
                    storage_options=self._storage_options or {},
                    data_storage_version=self.dest_data_storage_version,
                )
                fragment_json = _json.dumps(frag_meta.to_json())

                # Checkpoint the fragment metadata (tiny).  The presence
                # of this key is the completion signal for the partition.
                frag_key = _ckp_utils.format_udtf_fragment_key(partition_prefix)
                t_ckp = time.monotonic()
                store[frag_key] = pa.RecordBatch.from_pydict(
                    {"fragment_json": [fragment_json]}
                )
                checkpoint_time += time.monotonic() - t_ckp

            total_rows, batch_count = get_batch_stats()

            stats = {
                "rows": total_rows,
                "batches": batch_count,
                "execute_time_s": time.monotonic() - t_exec_start,
                "checkpoint_time_s": checkpoint_time,
            }
            return (fragment_json, stats)

        def _build_index_source(
            self,
            index_partition_info: tuple[int, str, str],
        ) -> Any:
            """Build a source from an index partition ordinal.

            Opens a ``VectorIndexReader`` on the remote side, reads the
            partition's row IDs, and uses ``take_row_ids`` for efficient
            direct row access — bypassing SQL filter construction.

            The returned source injects a ``_partition_id`` column
            (constant value = *partition_ordinal*) so that UDTFs can
            include it in their output without requiring the column to
            exist on the source table.

            Parameters
            ----------
            index_partition_info : tuple[int, str, str]
                A ``(partition_ordinal, index_name, column)`` triple where
                *partition_ordinal* is the zero-based IVF partition ID,
                *index_name* is the Lance index identifier, and *column*
                is the indexed vector column name.
            """
            from lance.dataset import VectorIndexReader

            from geneva.query import open_read_dataset

            ordinal, index_name, _column = index_partition_info
            lance_ds = open_read_dataset(self._tbl)
            reader = VectorIndexReader(lance_ds, index_name)
            part = reader.read_partition(ordinal)
            query_builder = _ChunkedTakeSource(
                self._tbl,
                part.column("_rowid"),
                selected_columns=self._udtf.input_columns,
            )
            return _IndexPartitionSource(query_builder, ordinal)

        def process_partition(
            self,
            partition_filter: str | None,
            partition_prefix: str,
            index_partition_info: tuple[int, str, str] | None = None,
            trace_carrier: dict | None = None,
        ) -> tuple[str | None, list[dict], dict]:
            """Execute the UDTF for one partition, writing a fragment directly.

            The actor writes output data files directly into the destination
            dataset via ``LanceFragment.create()`` and checkpoints the
            lightweight ``FragmentMetadata`` JSON for fault-tolerant resume.

            Parameters
            ----------
            partition_filter : str | None
                SQL filter expression to scope the source scan to a
                single partition (e.g. ``"group = 'a'"``), or *None*
                for unpartitioned execution.
            partition_prefix : str
                Checkpoint key prefix that uniquely identifies this
                partition within the checkpoint store.
            index_partition_info : tuple[int, str, str] | None
                Optional ``(partition_ordinal, index_name, column)``
                tuple.  When provided, the actor loads row IDs from
                the index locally instead of using a SQL filter.

            Returns
            -------
            tuple[str | None, list[dict], dict]
                A triple of ``(fragment_json, error_dicts, stats)`` where
                *fragment_json* is the JSON-serialised ``FragmentMetadata``
                (or ``None`` if no rows produced),
                *error_dicts* contains serialised ``ErrorRecord``
                dicts (empty on success), and *stats* contains
                execution timing information.
            """
            # Tie this actor's work back into the job's trace via the
            # propagated context (the actor runs in its own process).
            span, span_token = telemetry.start_linked_span(
                trace_carrier,
                "process_partition",
                {
                    "partition_prefix": partition_prefix,
                    "table": self.dest_table_name or "",
                    "table_uri": self.dest_table_uri or "",
                },
            )
            span_exc: BaseException | None = None
            try:
                self._ensure_initialized()

                if index_partition_info is not None:
                    query_builder = self._build_index_source(index_partition_info)
                else:
                    query_builder = self._build_source_query(partition_filter)

                _empty_stats: dict = {
                    "rows": 0,
                    "batches": 0,
                    "execute_time_s": 0.0,
                    "checkpoint_time_s": 0.0,
                }

                def _do_execute() -> tuple[str | None, dict]:
                    return self._execute_with_fragment_write(
                        query_builder, partition_prefix
                    )

                # No error handling configured — fail fast (current behaviour)
                if self._error_config is None:
                    fragment_json, stats = _do_execute()
                    return (fragment_json, [], stats)

                try:
                    # If retry is configured, wrap _do_execute with tenacity
                    from tenacity import Retrying
                    from tenacity.stop import stop_after_attempt as _stop1

                    retry_cfg = self._error_config.retry_config
                    if retry_cfg.stop != _stop1(1):  # has non-trivial retry
                        retrying = Retrying(
                            retry=retry_cfg.retry,
                            stop=retry_cfg.stop,
                            wait=retry_cfg.wait,
                            reraise=True,
                        )
                        fragment_json, stats = retrying(_do_execute)
                        return (fragment_json, [], stats)
                    else:
                        fragment_json, stats = _do_execute()
                        return (fragment_json, [], stats)
                except Exception as exc:
                    from geneva.debug.error_store import (
                        Outcome,
                        get_exception_outcome,
                        make_error_record_from_exception,
                    )

                    outcome = get_exception_outcome(exc, self._error_config)
                    if outcome == Outcome.SKIP:
                        logging.warning(
                            "UDTF: skipping partition %s due to %s: %s",
                            partition_prefix,
                            type(exc).__name__,
                            exc,
                        )
                        error_record = make_error_record_from_exception(
                            exc,
                            job_id=self.job_id,
                            table_uri=self.dest_table_uri,
                            table_name=self.dest_table_name,
                            table_version=None,
                            column_name="*",
                            udf_name=self._udtf.name,
                            udf_version=str(self._udtf.version),
                            batch_index=0,
                        )
                        return (None, [attrs.asdict(error_record)], _empty_stats)
                    raise  # FAIL or unmatched → propagate
            except Exception as _exc:
                span_exc = _exc
                raise
            finally:
                telemetry.end_job_span(span, span_token, span_exc)

        def flush_telemetry(self) -> None:
            """Force-export this worker's buffered spans/metrics before the
            pool kills the actor. The actor is long-lived, so its
            BatchSpanProcessor may not have exported the ``process_partition``
            spans yet, and ``atexit`` does not run under ``ray.kill``."""
            telemetry.flush()

    return UDTFProcessorActor


# Lazily initialised by _refresh_udtf_matview on first use
_UDTFProcessorActor: Any = None


def _get_udtf_processor_actor() -> Any:
    """Return the UDTFProcessorActor class, creating it on first call."""
    global _UDTFProcessorActor  # noqa: PLW0603
    if _UDTFProcessorActor is None:
        _UDTFProcessorActor = _make_udtf_processor_actor()
    return _UDTFProcessorActor


@attrs.frozen
class _IndexPartitionInfo:
    """Lightweight metadata for an index-based partition.

    Passed to the remote actor so it can load row IDs locally
    instead of receiving a giant ``_rowid IN (...)`` filter string.
    """

    partition_ordinal: int
    index_name: str
    column: str


def _index_stats_for_partition_planning(
    lance_ds: Any, index_name: str
) -> dict[str, Any]:
    """Read index statistics without materializing unused IVF centroids.

    Lance currently controls centroid inclusion with a process environment
    variable.  Serialize the temporary override and restore the caller's value
    immediately after the statistics call.
    """
    with _INDEX_STATS_ENV_LOCK:
        previous = os.environ.get(_LANCE_INCLUDE_VECTOR_CENTROIDS_ENV)
        os.environ[_LANCE_INCLUDE_VECTOR_CENTROIDS_ENV] = "false"
        try:
            return cast("dict[str, Any]", lance_ds.stats.index_stats(index_name))
        finally:
            if previous is None:
                os.environ.pop(_LANCE_INCLUDE_VECTOR_CENTROIDS_ENV, None)
            else:
                os.environ[_LANCE_INCLUDE_VECTOR_CENTROIDS_ENV] = previous


def _index_partition_ids_from_stats(index_stats: dict[str, Any]) -> list[int]:
    """Return non-empty IVF partition ordinals without reading index rows.

    Lance reports one entry per index segment.  A partition is non-empty when
    any segment reports a positive size for that ordinal.  Older or partial
    statistics may omit partition sizes; in that case all known ordinals are
    returned so workers can determine emptiness when they read their assigned
    partitions.
    """
    segments = index_stats.get("indices")
    if not isinstance(segments, list) or not segments:
        segments = index_stats.get("segments")

    if not isinstance(segments, list) or not segments:
        top_level_count = index_stats.get("num_partitions")
        if isinstance(top_level_count, int) and top_level_count >= 0:
            _LOG.warning(
                "IVF index statistics omit segment metadata; scheduling all %d "
                "partition ordinals",
                top_level_count,
            )
            return list(range(top_level_count))
        raise ValueError("Index statistics do not include IVF partition metadata")

    first_segment = segments[0]
    first_count = (
        first_segment.get("num_partitions") if isinstance(first_segment, dict) else None
    )
    top_level_count = index_stats.get("num_partitions")
    if not isinstance(first_count, int) or first_count < 0:
        if isinstance(top_level_count, int) and top_level_count >= 0:
            _LOG.warning(
                "First IVF index segment omits its partition count; scheduling "
                "all %d top-level partition ordinals",
                top_level_count,
            )
            return list(range(top_level_count))
        raise ValueError("Index statistics do not include IVF partition counts")

    num_partitions = first_count

    def _schedule_all(reason: str) -> list[int]:
        _LOG.warning(
            "%s; scheduling all %d reader-visible partition ordinals",
            reason,
            num_partitions,
        )
        return list(range(num_partitions))

    if (
        isinstance(top_level_count, int)
        and top_level_count >= 0
        and top_level_count != num_partitions
    ):
        return _schedule_all(
            "Top-level and first-segment IVF partition counts disagree"
        )

    segment_sizes: list[list[int]] = []
    for segment in segments:
        if not isinstance(segment, dict):
            return _schedule_all("IVF index segment metadata is malformed")
        if segment.get("num_partitions") != num_partitions:
            return _schedule_all("IVF index segments report different counts")
        partitions = segment.get("partitions")
        if not isinstance(partitions, list) or len(partitions) < num_partitions:
            return _schedule_all("IVF index partition-size metadata is incomplete")

        sizes: list[int] = []
        for partition in partitions[:num_partitions]:
            if not isinstance(partition, dict):
                return _schedule_all("IVF index partition metadata is malformed")
            size = partition.get("size")
            if not isinstance(size, int) or size < 0:
                return _schedule_all("IVF index partition size is unavailable")
            sizes.append(size)
        segment_sizes.append(sizes)

    partition_ids = [
        pid
        for pid in range(num_partitions)
        if any(sizes[pid] > 0 for sizes in segment_sizes)
    ]
    if not partition_ids and num_partitions:
        _LOG.warning(
            "IVF index statistics report all %d partitions empty", num_partitions
        )
    return partition_ids


def _build_column_partition_work_items(
    src_tbl: "Table",
    partition_col: str,
    top_prefix: str,
    checkpoint_store: CheckpointStore,
) -> tuple[list[tuple[str | None, str, _IndexPartitionInfo | None]], list[Any]]:
    """Build work items by scanning distinct values of a partition column.

    Returns ``(work_items, distinct_values)`` where each work item
    is a ``(sql_filter, checkpoint_prefix, None)`` triple.
    Completed partitions (those with a ``_fragment`` key in the
    checkpoint store) are skipped.
    """
    from geneva.checkpoint_utils import (
        format_udtf_fragment_key,
        format_udtf_partition_prefix,
    )

    distinct_values = _sorted_distinct_partition_values(src_tbl, partition_col)

    work_items: list[tuple[str | None, str, _IndexPartitionInfo | None]] = []
    for v in distinct_values:
        part_prefix = format_udtf_partition_prefix(
            top_prefix,
            partition_col=partition_col,
            partition_value=v,
        )
        frag_key = format_udtf_fragment_key(part_prefix)
        if frag_key in checkpoint_store:
            _LOG.info(
                "UDTF partition %s=%s completed, loading from checkpoint",
                partition_col,
                v,
            )
        else:
            if isinstance(v, str):
                escaped = str(v).replace("'", "''")
                pf = f"{partition_col} = '{escaped}'"
            else:
                pf = f"{partition_col} = {v}"
            work_items.append((pf, part_prefix, None))

    return work_items, distinct_values


def _build_index_partition_work_items(
    src_tbl: "Table",
    column: str,
    top_prefix: str,
    checkpoint_store: CheckpointStore,
    *,
    completed_fragment_keys: set[str] | None = None,
) -> tuple[list[tuple[str | None, str, _IndexPartitionInfo | None]], list[int]]:
    """Build work items from an existing IVF vector index.

    Returns ``(work_items, distinct_partition_ids)`` where each work item
    is a ``(None, checkpoint_prefix, _IndexPartitionInfo)`` triple.
    Completed partitions (those with a ``_fragment`` key in the
    checkpoint store) are skipped.
    """
    from geneva.checkpoint_utils import (
        format_udtf_fragment_key,
        format_udtf_partition_prefix,
    )
    from geneva.query import open_read_dataset

    lance_ds = open_read_dataset(src_tbl)
    # TODO: describe_indices should not require filtering by type_url;
    # this is a workaround for a current limitation in the API.
    try:
        idx_info = next(
            idx
            for idx in lance_ds.describe_indices()
            if column in idx.field_names and idx.type_url in _VECTOR_INDEX_TYPE_URLS
        )
    except StopIteration:
        raise ValueError(
            f"No IVF vector index found on column '{column}'. "
            f"Create one first (e.g. create_ivf_flat_index())."
        ) from None

    partition_ids = _index_partition_ids_from_stats(
        _index_stats_for_partition_planning(lance_ds, idx_info.name)
    )
    if completed_fragment_keys is None:
        completed_fragment_keys = set(checkpoint_store.list_keys(top_prefix))

    partition_col = _IVF_PARTITION_COL
    work_items: list[tuple[str | None, str, _IndexPartitionInfo | None]] = []
    for pid in partition_ids:
        part_prefix = format_udtf_partition_prefix(
            top_prefix,
            partition_col=partition_col,
            partition_value=pid,
        )
        frag_key = format_udtf_fragment_key(part_prefix)
        if frag_key in completed_fragment_keys:
            _LOG.info(
                "UDTF partition %s=%d completed, loading from checkpoint",
                partition_col,
                pid,
            )
        else:
            info = _IndexPartitionInfo(
                partition_ordinal=pid,
                index_name=idx_info.name,
                column=column,
            )
            work_items.append((None, part_prefix, info))

    return work_items, partition_ids


def _get_udf_name_from_field(field: pa.Field) -> str | None:
    """Extract UDF name from column field metadata."""
    if field.metadata is None:
        return None
    udf_name = field.metadata.get(b"virtual_column.udf_name")
    if udf_name is None:
        return None
    return udf_name.decode() if isinstance(udf_name, bytes) else udf_name


@attrs.define
class JobFuture:
    job_id: str
    # Optional root job-type span (backfill/bulk_load) tied to this future by
    # the async entry point; closed exactly once when the job resolves.
    _otel_span: Any = attrs.field(default=None, init=False)
    _span_closed: bool = attrs.field(default=False, init=False)

    def _close_span(self, exc: BaseException | None = None) -> None:
        """Close the future-tied root span exactly once (best-effort).

        No-op when no span was tied (the sync wrappers own their own span and
        never set ``_otel_span``). Subclass ``result()`` overrides call this —
        the authoritative close point, since it surfaces job failures. ``done()``
        is deliberately not a close point: it is polled in loops and carries no
        exception, so closing there could mark a failed job OK.
        """
        if self._otel_span is None or self._span_closed:
            return
        self._span_closed = True
        telemetry.close_span(self._otel_span, exc)

    def done(self, timeout: float | None = None) -> bool:
        raise NotImplementedError("JobFuture.done() must be implemented in subclasses")

    def result(self, timeout: float | None = None) -> Any:
        raise NotImplementedError(
            "JobFuture.result() must be implemented in subclasses"
        )

    def status(self, timeout: float | None = None) -> None:
        raise NotImplementedError(
            "JobFuture.status() must be implemented in subclasses"
        )


class _ThreadJobFuture(JobFuture):
    """A :class:`JobFuture` backed by a background thread.

    Used by :meth:`Table.refresh_async` to wrap a synchronous
    ``refresh()`` call so callers see the same async surface as
    ``backfill_async``. The wrapped thread populates ``result_holder``
    or ``error_holder`` and signals ``done_event`` when complete.
    """

    def __init__(
        self,
        job_id: str,
        done_event: "threading.Event",
        result_holder: "dict[str, Any]",
        error_holder: "dict[str, BaseException]",
    ) -> None:
        super().__init__(job_id=job_id)
        self._done_event = done_event
        self._result_holder = result_holder
        self._error_holder = error_holder

    def done(self, timeout: float | None = None) -> bool:
        if timeout is None:
            return self._done_event.is_set()
        return self._done_event.wait(timeout)

    def result(self, timeout: float | None = None) -> Any:
        if not self._done_event.wait(timeout):
            raise TimeoutError(f"job {self.job_id} did not complete in {timeout}s")
        if "error" in self._error_holder:
            raise self._error_holder["error"]
        return self._result_holder.get("value")

    def status(self, timeout: float | None = None) -> None:
        return None


@attrs.define(order=True, init=False)
class TableReference:
    """
    Serializable reference to a Geneva Table.

    Used to pass through ray.remote calls
    """

    table_id: list[str]
    version: int | None

    api_key: Any = attrs.field(default=None, repr=False)
    host_override: str | None = attrs.field(default=None)
    namespace_client_impl: str | None = attrs.field(default=None)
    namespace_client_properties: dict[str, str] | None = attrs.field(
        default=None, repr=redact_dict_values
    )
    namespace_client_pushdown_operations: list[str] | None = attrs.field(default=None)
    system_namespace: list[str] = attrs.field(factory=lambda: [SYSTEM_NAMESPACE])
    is_system_table: bool = attrs.field(default=False)
    co_located_system_tables: bool = attrs.field(default=False)
    # Physical table URI and storage options - cached to avoid describe_table calls
    table_uri: str | None = attrs.field(default=None)
    storage_options: dict[str, str] | None = attrs.field(
        default=None, repr=redact_dict_values
    )

    def __init__(
        self,
        table_id: list[str],
        version: int | None,
        db_uri: str | None = None,
        *,
        api_key: Any = None,
        host_override: str | None = None,
        namespace_client_impl: str | None = None,
        namespace_client_properties: dict[str, str] | None = None,
        namespace_client_pushdown_operations: list[str] | None = None,
        system_namespace: list[str] | None = None,
        is_system_table: bool = False,
        co_located_system_tables: bool = False,
        table_uri: str | None = None,
        storage_options: dict[str, str] | None = None,
    ) -> None:
        if (
            namespace_client_impl is None
            and namespace_client_properties is None
            and db_uri is not None
            and not co_located_system_tables
        ):
            (
                namespace_client_impl,
                namespace_client_properties,
                namespace_client_pushdown_operations,
                system_namespace,
            ) = self._namespace_from_legacy_db_uri(
                db_uri=str(db_uri),
                api_key=api_key,
                host_override=host_override,
                storage_options=storage_options,
                system_namespace=system_namespace,
                namespace_client_pushdown_operations=(
                    namespace_client_pushdown_operations
                ),
            )

        self.table_id = table_id
        self.version = version
        self.api_key = api_key
        self.host_override = host_override
        self.namespace_client_impl = namespace_client_impl
        self.namespace_client_properties = _as_namespace_client_properties(
            namespace_client_properties
        )
        self.namespace_client_pushdown_operations = namespace_client_pushdown_operations
        self.system_namespace = (
            system_namespace if system_namespace is not None else [SYSTEM_NAMESPACE]
        )
        self.is_system_table = is_system_table
        self.co_located_system_tables = co_located_system_tables
        self.table_uri = table_uri
        self.storage_options = storage_options

    @staticmethod
    def _namespace_from_legacy_db_uri(
        *,
        db_uri: str,
        api_key: Any,
        host_override: str | None,
        storage_options: dict[str, str] | None,
        system_namespace: list[str] | None,
        namespace_client_pushdown_operations: list[str] | None,
    ) -> tuple[
        str | None,
        dict[str, str] | None,
        list[str] | None,
        list[str] | None,
    ]:
        if db_uri.startswith("db://"):
            if host_override is None:
                return (
                    None,
                    None,
                    namespace_client_pushdown_operations,
                    system_namespace,
                )
            database_name = db_uri[5:].rstrip("/")
            namespace_client_properties = {"uri": host_override}
            api_key_str = _plain_api_key(api_key)
            if api_key_str:
                namespace_client_properties["header.x-api-key"] = api_key_str
            namespace_client_properties["header.x-lancedb-database"] = database_name
            if namespace_client_pushdown_operations is None:
                namespace_client_pushdown_operations = ["QueryTable", "CreateTable"]
            if system_namespace is None:
                system_namespace = [SYSTEM_NAMESPACE]
            return (
                "rest",
                namespace_client_properties,
                namespace_client_pushdown_operations,
                system_namespace,
            )

        namespace_client_properties = {"root": db_uri}
        if storage_options:
            namespace_client_properties.update(
                _directory_namespace_storage_properties(storage_options)
            )
        if system_namespace is None:
            system_namespace = [SYSTEM_NAMESPACE]
        return (
            "dir",
            namespace_client_properties,
            namespace_client_pushdown_operations,
            system_namespace,
        )

    @property
    def db_uri(self) -> str | None:
        """Best-effort legacy URI derived from namespace properties."""
        props = self.namespace_client_properties or {}
        if self.namespace_client_impl == "dir":
            return props.get("root")
        if self.namespace_client_impl == "rest":
            database = props.get("header.x-lancedb-database")
            return f"db://{database}" if database else None
        return None

    @property
    def table_name(self) -> str:
        """Return the table name (last element of table_id)."""
        return self.table_id[-1] if self.table_id else ""

    @property
    def namespace_config(self) -> NamespaceConfig:
        """Bundled namespace configuration."""
        return NamespaceConfig(
            namespace_client_impl=self.namespace_client_impl,
            namespace_client_properties=_as_namespace_client_properties(
                self.namespace_client_properties
            ),
            namespace_client_pushdown_operations=self.namespace_client_pushdown_operations,
            system_namespace=self.system_namespace,
        )

    def as_system_table(self, table_name: str) -> "TableReference":
        """Create a sibling reference that targets a system table."""
        table_id = self.system_namespace + [table_name]
        return TableReference(
            table_id=table_id,
            version=None,
            api_key=self.api_key,
            host_override=self.host_override,
            namespace_client_impl=self.namespace_client_impl,
            namespace_client_properties=self.namespace_client_properties,
            namespace_client_pushdown_operations=self.namespace_client_pushdown_operations,
            system_namespace=self.system_namespace,
            is_system_table=not self.co_located_system_tables,
            co_located_system_tables=self.co_located_system_tables,
            storage_options=self.storage_options,
        )

    def open_checkpoint_store(
        self, *, use_worker_props: bool = False
    ) -> CheckpointStore:
        """Open a Lance checkpoint store for this table."""
        try:
            namespace_config = (
                self.namespace_config.for_worker()
                if use_worker_props
                else self.namespace_config
            )
            namespace_client = namespace_config.connect_namespace_client()
            table_location = self.table_uri or resolve_table_physical_uri(
                self.table_id,
                db_uri=None,
                namespace_client_impl=self.namespace_client_impl,
                namespace_client_properties=self.namespace_client_properties,
                use_worker_props=use_worker_props,
            )

            # Pick the store class first so the per-table subdir tracks the
            # layout: flat stays at ``_ckp`` (backward-compatible) while
            # hierarchical lands at a sibling root and can never collide.
            # Precedence: ``GENEVA_CHECKPOINT_SUBDIR`` blanket env override →
            # per-layout config field (``flat_subdir`` / ``hierarchical_subdir``,
            # also overridable via ``CHECKPOINT__FLAT_SUBDIR`` /
            # ``CHECKPOINT__HIERARCHICAL_SUBDIR``) → class constant
            # ``DEFAULT_TABLE_SUBDIR``.
            from geneva.checkpoint import (
                CheckpointConfig,
                _select_store_class,
            )

            store_cls = _select_store_class()
            subdir = os.environ.get("GENEVA_CHECKPOINT_SUBDIR")
            if subdir is None:
                try:
                    cfg = CheckpointConfig.get()
                    subdir = (
                        cfg.hierarchical_subdir
                        if cfg.store_layout == "hierarchical"
                        else cfg.flat_subdir
                    )
                except Exception:
                    subdir = store_cls.DEFAULT_TABLE_SUBDIR
            checkpoint_uri = str(URL(table_location) / subdir)

            return store_cls(
                checkpoint_uri,
                namespace_client=namespace_client,
                namespace_client_impl=namespace_config.namespace_client_impl,
                namespace_client_properties=(
                    namespace_config.namespace_client_properties
                ),
                table_id=self.table_id,
                storage_options=self.storage_options,
                session_root_subdir=subdir,
            )
        except Exception as exc:
            raise RuntimeError(
                f"Failed to open checkpoint store for table {self.table_id}"
            ) from exc

    def open_db(self) -> Connection:
        """Open a connection to the Lance database.
        Set read consistency interval to 0 for strongly consistent reads.

        When called from a worker context with worker_uri configured,
        the worker endpoint is used instead of the external endpoint.
        """
        try:
            cp = self.open_checkpoint_store(use_worker_props=True)
        except Exception:
            _LOG.warning(
                "open_db: failed to open checkpoint store for %s",
                self.table_id,
                exc_info=True,
            )
            cp = None
        interval = timedelta(0)

        assert self.namespace_config.namespace_client_impl is not None, (
            "TableReference requires namespace_client_impl"
        )
        assert self.namespace_config.namespace_client_properties is not None, (
            "TableReference requires namespace_client_properties"
        )
        system_namespace = self.system_namespace
        worker_ns = self.namespace_config.for_worker()
        connect_kwargs: dict[str, Any] = {
            "namespace_client_impl": worker_ns.namespace_client_impl,
            "namespace_client_properties": worker_ns.namespace_client_properties,
            "namespace_client_pushdown_operations": (
                worker_ns.namespace_client_pushdown_operations
            ),
            "api_key": self.api_key,
            "host_override": self.host_override,
            "system_namespace": system_namespace,
            "read_consistency_interval": interval,
        }
        if cp is not None:
            connect_kwargs["checkpoint"] = cp
        # Workers must inherit explicit storage credentials for every namespace
        # impl; otherwise a non-"dir" worker opens storage with no credentials
        # and falls back to the ambient credential chain. Re-vend near-expiry
        # credentials so a backfill that outlives the plan-time token doesn't
        # sign requests with a dead credential (see _refreshed_storage_options).
        connect_kwargs["storage_options"] = self._refreshed_storage_options()
        return connect(**connect_kwargs)

    def _refreshed_storage_options(self) -> dict[str, str] | None:
        """Re-vend this reference's vended credentials when they are near expiry.

        The driver vends a short-lived token once at plan time and ships it in
        ``self.storage_options``; a backfill that outlives it would otherwise
        sign every object-store request with a dead credential (400
        ExpiredToken). No-op for static credentials or a token not yet within
        the safety window.
        """
        return refresh_storage_options(
            self.storage_options,
            table_id=self.table_id,
            namespace_client_factory=lambda: self.connect_namespace(
                use_worker_props=True
            ),
        )

    def _open_async_db(self) -> AsyncLanceNamespaceDBConnection:
        """Shared body for the async connection openers (re-vends creds)."""
        namespace = self.connect_namespace(use_worker_props=True)
        assert namespace is not None, "TableReference requires namespace credentials"
        return AsyncLanceNamespaceDBConnection(
            namespace,
            read_consistency_interval=timedelta(0),
            storage_options=self._refreshed_storage_options(),
            namespace_client_pushdown_operations=self.namespace_client_pushdown_operations,
        )

    async def open_db_async(
        self,
    ) -> AsyncConnection | AsyncLanceNamespaceDBConnection:
        """Open an async connection to the Lance database.
        This uses native lancedb AsyncConnection and doesn't support checkpoint store.
        Currently used by JobTracker only.
        """
        return self._open_async_db()

    async def open_system_db_async(
        self,
    ) -> AsyncConnection | AsyncLanceNamespaceDBConnection:
        """Open an async connection suitable for system-table operations."""
        return self._open_async_db()

    def open(self) -> "Table":
        # Extract namespace from table_id (everything except the last element)
        namespace = self.table_id[:-1] if len(self.table_id) > 1 else []
        tbl = self.open_db().open_table(
            self.table_name, version=self.version, namespace=namespace
        )
        # Seed the URI cache so worker reads skip the describe_table (GEN-758).
        if self.table_uri:
            vars(tbl)["uri"] = self.table_uri
        return tbl

    def connect_namespace(
        self,
        *,
        use_worker_props: bool = False,
    ) -> Optional["LanceNamespace"]:
        """Connect using the Lance namespace if configured.

        Set use_worker_props when called from a worker context with worker_uri
        configured.
        """
        return self.namespace_config.connect_namespace_client(
            use_worker_props=use_worker_props
        )


class Table(LanceTable):
    """Table in Geneva.

    A Table is a Lance dataset.

    The ``NativeTable`` and ``RemoteTable`` subclasses distinguish
    object-storage-backed tables from Phalanx-backed tables. For
    historical reasons, ``Table`` itself remains instantiable so
    existing callers and helpers continue to work. New code should
    expect ``NativeTable`` from native-mode connections and
    ``RemoteTable`` from ``db://`` connections (when GENEVA_REMOTE_V2
    is enabled).
    """

    def __init__(
        self,
        conn: Connection,
        name: str,
        *,
        namespace: list[str] | None = None,
        version: int | None = None,
        storage_options: dict[str, str] | None = None,
        index_cache_size: int | None = None,
        **kwargs,
    ) -> None:
        self._conn_uri = conn.uri
        self._name = name

        if namespace is None:
            namespace = []
        self._namespace = namespace
        self._table_id = namespace + [name]

        self._conn = conn

        self._version: int | None = version
        self._index_cache_size = index_cache_size
        self._storage_options = storage_options

        # Load table
        self._ltbl  # noqa

    def __repr__(self) -> str:
        return f"<Table {self._table_id}>"

    # TODO: This annotation sucks
    def __reduce__(self):  # noqa: ANN204
        return (self.__class__, (self._conn, self._name))

    def get_reference(self) -> TableReference:
        table_uri = self.uri
        co_located_system_tables = (
            self._conn._host_override is not None and self._conn.system_namespace == []
        )
        # Merge storage options: start with connection's options, override with latest
        storage_options = dict(self._conn._storage_options or {})
        latest = self._ltbl.latest_storage_options()  # pyright: ignore[reportAttributeAccessIssue]
        if latest:
            storage_options.update(latest)
        ns = self._conn._ns_config
        namespace_client_impl = ns.namespace_client_impl
        namespace_client_properties = ns.namespace_client_properties
        if namespace_client_impl is None:
            namespace_client_impl = "dir"
            namespace_client_properties = {"root": _get_db_uri(table_uri)}
        return TableReference(
            table_id=self._table_id,
            version=self._version,
            api_key=_plain_api_key(self._conn._api_key),
            host_override=self._conn._host_override,
            namespace_client_impl=namespace_client_impl,
            namespace_client_properties=namespace_client_properties,
            namespace_client_pushdown_operations=ns.namespace_client_pushdown_operations,
            system_namespace=self._conn.system_namespace,
            is_system_table=False,
            co_located_system_tables=co_located_system_tables,
            table_uri=table_uri,
            storage_options=storage_options or None,
        )

    def get_fragments(self) -> list[lance.LanceFragment]:
        from geneva.query import open_read_dataset

        return open_read_dataset(self).get_fragments()

    @cached_property
    def _ltbl(self) -> lancedb.table.Table:
        """Return the inner LanceDB table.
        This might be a LanceTable or a RemoteTable depending on the connection
        configuration
        """
        inner = self._conn._connect

        # Forward storage_options so cloud credentials supplied via
        # storage_options (rather than env vars) reach the underlying open.
        # Merge (not ``or``) the connection's options with the table's: a
        # truthy-but-partial table dict (e.g. {"new_table_enable_stable_row_ids":
        # "true"} built by view creation) must not drop the connection's
        # credentials, or opening on Azure fails with "no Azure account name in
        # URI". Table options override the connection's on key conflicts.
        storage_options = {
            **(self._conn._storage_options or {}),
            **(self._storage_options or {}),
        } or None

        storage_options = refresh_storage_options(
            storage_options,
            table_id=self._table_id,
            namespace_config=getattr(self._conn, "_ns_config", None),
        )

        # remote db, open table directly
        if self._conn.is_remote_uri():
            tbl = inner.open_table(
                self._name,
                namespace_path=self._namespace,
                storage_options=storage_options,
            )
        else:
            _LOG.debug(
                f"opening table {self._table_id} {type(self)=} {self._namespace=} "
            )
            tbl = inner.open_table(
                self.name,
                namespace_path=self._namespace,
                storage_options=storage_options,
            )

        # Check out the specified version regardless of database type
        if self._version:
            tbl.checkout(self._version)
        return tbl

    @property
    def name(self) -> str:
        """Get the name of the table."""
        return self._name

    @property
    def version(self) -> int:
        """Get the current version of the table"""
        return self._ltbl.version

    @property
    def schema(self) -> pa.Schema:
        """The Arrow Schema of the Table."""
        return self._ltbl.schema

    @cached_property
    def uri(self) -> str:
        from lance_namespace import DescribeTableRequest

        conn = self._conn
        ns = conn.namespace_client()
        response = ns.describe_table(DescribeTableRequest(id=self._table_id))
        if response.location is None:
            raise ValueError(f"Table location is None for table {self._table_id}")
        return _normalize_file_uri(response.location.rstrip("?"))

    @property
    def embedding_functions(self) -> Never:
        raise NotImplementedError("Embedding functions are not supported.")

    def add(
        self,
        data,
        mode: str = "append",
        on_bad_vectors: str = "error",
        fill_value: float = 0.0,
    ) -> None:
        get_table_writer().add(
            self._ltbl,
            data,
            mode=mode,  # type: ignore[arg-type]
            on_bad_vectors=on_bad_vectors,  # type: ignore[arg-type]
            fill_value=fill_value,
        )

    def checkout(self, version: int) -> None:
        self._version = version
        self._ltbl.checkout(version)

    def checkout_latest(self) -> None:
        self._version = None
        self._ltbl.checkout_latest()

    def add_columns(
        self,
        transforms: dict[str, str | UDF | tuple[UDF, list[str]]] | UDF | UnpackedUDF,
        *args,
        **kwargs,
    ) -> None:
        """
        Add columns or UDF-based columns to the Geneva table.

        For UDF columns, this method validates that:
        - All input columns exist in the table schema
        - Column types are compatible with UDF type annotations (if present)
        - RecordBatch UDFs do not have input_columns defined

        This early validation helps catch configuration errors before job execution.

        Parameters
        ----------
        transforms : dict[str, str | UDF | tuple[UDF, list[str]]]
            The key is the column name to add and the value is a
            specification of the column type/value.

            * If the spec is a string, it is expected to be a datafusion
              sql expression. (e.g "cast(null as string)")
            * If the spec is a UDF, a virtual column is added with input
              columns inferred from the UDF's argument names.
            * If the spec is a tuple, the first element is a UDF and the
              second element is a list of input column names.

        Raises
        ------
        ValueError
            If UDF validation fails (missing columns, type mismatches, etc.)

        Warns
        -----
        UserWarning
            If type validation is skipped due to missing type annotations
        UserWarning
            If ``computed=`` is passed. It is accepted for forward
            compatibility with LanceDB's ``add_columns`` and ignored here.

        Examples
        --------
        >>> @udf(data_type=pa.int32())
        ... def double(a: int) -> int:
        ...     return a * 2
        >>> table.add_columns({"doubled": double})  # Validates 'a' column exists

        """
        # ``computed=`` belongs to LanceDB's add_columns, which Geneva's does
        # not mirror. Accept and ignore it so forward-looking callers still
        # run, but say the column was not added.
        if kwargs.pop("computed", None) is not None:
            warnings.warn(
                "add_columns ignored computed=: Geneva does not declare Lance "
                f"computed columns yet. {_COMPUTED_COLUMN_SIGNATURE} needs "
                f"lancedb {_COMPUTED_COLUMN_MIN_LANCEDB} or newer; pass a UDF "
                "to add a Geneva computed column.",
                UserWarning,
                stacklevel=2,
            )

        if isinstance(transforms, UDF):
            if not transforms.is_multi_output:
                raise ValueError(
                    "table.add_columns(udf) is only supported for UDFs annotated "
                    "as returning Columns[T]. Use table.add_columns({'name': udf}) "
                    "for single-column UDFs."
                )
            self._add_unpacked_virtual_columns(UnpackedUDF(transforms), *args, **kwargs)
            return

        if isinstance(transforms, UnpackedUDF):
            self._add_unpacked_virtual_columns(transforms, *args, **kwargs)
            return

        # Remote (db://) path: route through namespace API.
        if self._conn.use_remote_dispatch():
            return self._add_columns_remote(transforms)

        t = self._ltbl
        t.checkout_latest()

        # handle basic columns
        basic_cols = {k: v for k, v in transforms.items() if isinstance(v, str)}
        if len(basic_cols) > 0:
            t.add_columns(basic_cols, *args)

        # handle UDF virtual columns
        udf_cols = {k: v for k, v in transforms.items() if not isinstance(v, str)}
        for k, v in udf_cols.items():
            if isinstance(v, (UDTF, Chunker)):
                raise TypeError(
                    f"add_columns received a {type(v).__name__} for column "
                    f"'{k}'. UDTFs and chunkers change row cardinality and "
                    "are not supported in add_columns — use "
                    "db.create_udtf_view() instead."
                )
            if isinstance(v, UDF):
                if v.is_multi_output:
                    raise ValueError(
                        "Columns[T] UDFs must be added directly with "
                        "table.add_columns(udf). Adding a Columns[T] UDF as a "
                        "single struct column will be supported by a future "
                        "as_struct() API."
                    )
                # infer column names from udf arguments
                udf = v
                self._add_virtual_columns(
                    {k: udf}, *args, input_columns=udf.input_columns, **kwargs
                )
            else:
                # explicitly specify input columns
                (udf, cols) = v
                if udf.is_multi_output:
                    raise ValueError(
                        "Columns[T] UDFs must be added directly with "
                        "table.add_columns(udf). Explicit input column overrides for "
                        "multi-column UDFs are not supported in this API."
                    )
                self._add_virtual_columns({k: udf}, *args, input_columns=cols, **kwargs)

    def _add_virtual_columns(
        self,
        mapping: dict[str, UDF],  # this breaks the non udf mapping
        *args,
        input_columns: list[str] | None = None,
        **kwargs,
    ) -> None:
        """
        This is an internal method and not intended to be called directly.

        Add udf based virtual columns to the Geneva table.
        """

        if len(mapping) != 1:
            raise ValueError("Only one UDF is supported for now.")

        _LOG.info("Adding column: udf=%s", mapping)
        col_name = next(iter(mapping))
        udf = mapping[col_name]

        if not isinstance(udf, UDF):
            # Stateful udfs are implemenated as Callable classses, and look
            # like partial functions here.  Instantiate to get the return
            # data_type annotations.
            udf = udf()

        # Validate input columns exist in table schema before adding the column
        self._validate_udf_input_columns(udf, input_columns)

        # Check for circular dependencies before adding the column
        cols_to_check = (
            input_columns if input_columns is not None else udf.input_columns
        )
        if (
            udf.arg_type != UDFArgType.RECORD_BATCH
            and cols_to_check
            and col_name in cols_to_check
        ):
            raise ValueError(
                f"UDF output column {col_name} is not allowed to be in"
                f" input {cols_to_check}"
            )

        self._ltbl.checkout_latest()
        self._ltbl.add_columns(pa.field(col_name, udf.data_type))
        self._configure_computed_column(col_name, udf, input_columns)

    def _add_unpacked_virtual_columns(
        self,
        unpacked: UnpackedUDF,
        *args,
        input_columns: list[str] | None = None,
        **kwargs,
    ) -> None:
        if args or kwargs:
            raise ValueError(
                "Columns[T] multi-column add_columns does not accept extra arguments"
            )
        if self._conn.use_remote_dispatch():
            raise NotImplementedError(
                "RemoteTable.add_columns() does not yet support Columns[T] "
                "multi-column UDFs."
            )
        if not isinstance(self._ltbl, LanceLocalTable):
            raise TypeError(
                "adding udf column is currently only supported for local tables"
            )

        udf = unpacked.udf
        self._validate_udf_input_columns(udf, input_columns)

        input_cols = input_columns if input_columns is not None else udf.input_columns
        canonical_input_cols = canonical_field_paths(self._ltbl.schema, input_cols)
        cols_to_check = input_cols or []
        output_columns = [field.output_column for field in unpacked.fields]
        circular = sorted(set(output_columns) & set(cols_to_check))
        if udf.arg_type != UDFArgType.RECORD_BATCH and circular:
            raise ValueError(
                f"Multi-column UDF output columns {circular} are not allowed to be in"
                f" input {cols_to_check}"
            )

        existing = set(self._ltbl.schema.names)
        collisions = sorted(existing & set(output_columns))
        if collisions:
            raise ValueError(
                "Columns[T] UDF output columns already exist in table schema: "
                f"{collisions}"
            )

        udf_spec = self._conn._packager.marshal(udf, table_ref=self.get_reference())
        checksum = hashlib.sha256(udf_spec.udf_payload).hexdigest()
        udf_location = f"_udfs/{checksum}"
        self._upload_udf(udf_spec.udf_payload, udf_location)

        group_id = _unpack_group_id(udf, output_columns)
        fields_payload = [
            {"field": field.struct_field_name, "column": field.output_column}
            for field in unpacked.fields
        ]
        schema_fields: list[pa.Field] = []
        for unpacked_field in unpacked.fields:
            child_field = unpacked_field.field
            base_field_metadata = udf.field_metadata | _metadata_to_str_dict(
                child_field.metadata
            )
            field_metadata = base_field_metadata | {
                "virtual_column": "true",
                "virtual_column.udf_backend": udf_spec.backend,
                "virtual_column.udf_name": udf_spec.name,
                "virtual_column.udf": udf_location,
                "virtual_column.udf_inputs": json.dumps(canonical_input_cols),
                "virtual_column.platform.system": platform.system(),
                "virtual_column.platform.arch": platform.machine(),
                "virtual_column.platform.python_version": platform.python_version(),
                "virtual_column.auto_backfill": (
                    "true" if udf.auto_backfill else "false"
                ),
                _UNPACK_META_FLAG: "true",
                _UNPACK_META_GROUP: group_id,
                _UNPACK_META_FIELD: unpacked_field.struct_field_name,
                _UNPACK_META_FIELDS: json.dumps(fields_payload),
            }
            if udf.manifest is not None:
                field_metadata["virtual_column.manifest"] = udf.manifest.to_json()
                field_metadata["virtual_column.manifest_checksum"] = (
                    udf.manifest.compute_checksum()
                )
            schema_fields.append(
                pa.field(
                    unpacked_field.output_column,
                    child_field.type,
                    nullable=child_field.nullable,
                    metadata=field_metadata,
                )
            )

        self._ltbl.checkout_latest()
        self._ltbl.add_columns(pa.schema(schema_fields))

    def _validate_udf_input_columns(
        self, udf: UDF, input_columns: list[str] | None
    ) -> None:
        """
        Validate that UDF input columns exist in the table schema.

        This method delegates to the UDF's validate_against_schema() method
        for consolidated validation logic.

        Parameters
        ----------
        udf: UDF
            The UDF to validate
        input_columns: list[str] | None
            The input column names to validate

        Raises
        ------
        ValueError: If input columns don't exist in table schema or have type mismatches
        """
        # Delegate to UDF's consolidated validation method
        udf.validate_against_schema(self._ltbl.schema, input_columns)

    def refresh(
        self,
        *,
        where: str | None = None,
        src_version: int | None = None,
        max_rows_per_fragment: int | None = None,
        concurrency: int = 8,
        intra_applier_concurrency: int = 1,
        cluster: str | None = None,
        manifest: str | None = None,
        output_limit: int | None = None,
        source_task_size: int | None = None,
        timeout: timedelta | None = None,
        job_id: str | None = None,
        _admission_check: bool | None = None,
        _admission_strict: bool | None = None,
        **kwargs,
    ) -> "RefreshJobResult":
        """
        Refresh the specified materialized view.

        Parameters
        ----------
        where: str | None
            SQL expression filter used to only refresh selected rows.
            Not yet implemented.
        src_version: int | None
            Optional source table version to refresh from. If None (default),
            uses the latest version of the source table.
        max_rows_per_fragment: int | None
            Optional maximum number of rows per destination fragment when adding
            placeholder rows for new source data. If None, uses LanceDB's default
            (1 million rows). Use smaller values to control fragment granularity.
        concurrency: int
            (default = 8) This controls the number of processes that tasks run
            concurrently. For max throughput, ideally this is larger than the number
            of nodes in the k8s cluster. This is the number of Ray actor processes
            that are started.
        intra_applier_concurrency: int
            (default = 1) This controls the number of threads used to execute tasks
            within a process. Multiplying this times `concurrency` roughly corresponds
            to the number of cpu's being used.
        cluster: str | None
            Optional cluster name (operational override) used by remote
            dispatch to route the refresh to a specific Ray cluster. Ignored
            for native connections.
        manifest: str | None
            Optional inline JSON-serialized ``GenevaManifest`` used for this
            refresh only. Does not mutate the manifest snapshotted on the view.
            Ignored for native connections.
        output_limit: int | None
            Post-trim cap on view row count after expansion. Valid only for
            chunker-backed materialized views; raises ``ValueError`` otherwise.
        source_task_size: int | None
            Chunker-backed views only: number of source row IDs per expansion
            work item (default 1024). Smaller values increase parallelism and
            lower per-actor memory; ignored for non-chunker views.
        timeout: datetime.timedelta | None
            (default = None) Maximum time to wait for the job to reach
            a terminal state. When the deadline elapses, the call raises
            ``TimeoutError``; note the job itself is not cancelled
            and may continue running. ``None`` waits indefinitely.
        _admission_check: bool | None
            Whether to run admission control to validate cluster resources before
            starting the job. If None, uses config (default: true). Set to False to
            skip the check.
            **Experimental**: Parameters starting with `_` are subject to change.
        _admission_strict: bool | None
            If True, raises ResourcesUnavailableError when resources are
            insufficient. If False, logs a warning but allows the job to proceed.
            If None, uses config (default: false, i.e. warn and proceed).
            **Experimental**: Parameters starting with `_` are subject to change.

        Raises
        ------
        RuntimeError
            If attempting to refresh to a different version without stable row IDs
            enabled on the source table. This is because compaction may have
            invalidated the __source_row_id values, breaking incremental refresh.
        ValueError
            If ``output_limit`` is set on a non-chunker materialized view.
        """
        if output_limit is not None:
            self._require_chunker_view("output_limit")

        # Remote (db://) path: dispatch via namespace API and block on completion.
        if self._conn.use_remote_dispatch():
            from typing import cast

            job = self._refresh_async_remote(
                src_version=src_version,
                max_rows_per_fragment=max_rows_per_fragment,
                concurrency=concurrency,
                intra_applier_concurrency=intra_applier_concurrency,
                cluster=cluster,
                manifest=manifest,
                output_limit=output_limit,
                source_task_size=source_task_size,
                **kwargs,
            )
            timeout_secs = timeout.total_seconds() if timeout is not None else None
            result = cast("RefreshJobResult", job.result(timeout=timeout_secs))
            self.checkout_latest()
            return result

        # Status transitions (PENDING -> RUNNING -> DONE/FAILED) for the
        # phalanx-issued job_id are driven from the JobTracker actor
        # inside the Ray cluster; see pipeline.run_ray_copy_table and
        # _refresh_udtf_matview. The driver only threads job_id through.
        return self._refresh(
            job_id=job_id,
            where=where,
            src_version=src_version,
            max_rows_per_fragment=max_rows_per_fragment,
            concurrency=concurrency,
            intra_applier_concurrency=intra_applier_concurrency,
            output_limit=output_limit,
            source_task_size=source_task_size,
            timeout=timeout,
            _admission_check=_admission_check,
            _admission_strict=_admission_strict,
        )

    def _refresh(
        self,
        *,
        job_id: str | None,
        where: str | None,
        src_version: int | None,
        max_rows_per_fragment: int | None,
        concurrency: int,
        intra_applier_concurrency: int,
        output_limit: int | None,
        _admission_check: bool | None,
        _admission_strict: bool | None,
        source_task_size: int | None = None,
        timeout: timedelta | None = None,
    ) -> "RefreshJobResult":
        # Mint the job_id up front so the root span carries the real id (the
        # same value hist.launch will reuse) rather than an empty string.
        if job_id is None:
            job_id = uuid.uuid4().hex
        _rf_ref = self.get_reference()
        # Root span for the whole refresh: attached across dispatch + the
        # blocking wait in each branch, so the worker's geneva.job span
        # (any MV kind) nests inside it.
        with telemetry.span(
            "refresh",
            {
                "job_id": job_id,
                "job_type": "refresh",
                "table": _rf_ref.table_name,
                "table_uri": _rf_ref.table_uri or "",
            },
        ):
            if where:
                raise NotImplementedError(
                    "where clauses on materialized view refresh not implemented yet."
                )

            # Honor an explicit timeout on the native path, like the remote
            # db:// path. None means an unbounded wait.
            timeout_secs = timeout.total_seconds() if timeout is not None else None

            # Check source stable row IDs and validate version compatibility
            schema = self.schema
            metadata = schema.metadata or {}

            # Check if this is a UDTF-backed materialized view
            mv_version_bytes = metadata.get(MATVIEW_META_VERSION.encode(), b"1")
            mv_version_str = mv_version_bytes.decode()

            self._validate_refresh_admission(
                mv_version_str=mv_version_str,
                metadata=metadata,
                concurrency=concurrency,
                intra_applier_concurrency=intra_applier_concurrency,
                _admission_check=_admission_check,
                _admission_strict=_admission_strict,
            )

            if mv_version_str == "udtf":
                # UDTF-backed view - routes through the worker-side remote
                # wrapper which mirrors backfill's run_ray_add_column_remote
                # (drives _geneva_jobs PENDING -> RUNNING -> DONE/FAILED).
                from geneva.runners.ray.pipeline import dispatch_run_ray_refresh

                fut = dispatch_run_ray_refresh(
                    self.get_reference(),
                    job_id=job_id,
                    src_version=src_version,
                    max_rows_per_fragment=max_rows_per_fragment,
                    concurrency=concurrency,
                    intra_applier_concurrency=intra_applier_concurrency,
                    output_limit=output_limit,
                    _admission_check=_admission_check,
                    _admission_strict=_admission_strict,
                )
                _await_job_future(fut, timeout_secs, what="refresh")
                self.checkout_latest()
                return self._build_refresh_result(job_id)

            if _is_chunker_mv_version(mv_version_str):
                # Chunker-backed view (1:N) — same worker-side dispatch.
                from geneva.runners.ray.pipeline import dispatch_run_ray_refresh

                fut = dispatch_run_ray_refresh(
                    self.get_reference(),
                    job_id=job_id,
                    src_version=src_version,
                    max_rows_per_fragment=max_rows_per_fragment,
                    concurrency=concurrency,
                    intra_applier_concurrency=intra_applier_concurrency,
                    output_limit=output_limit,
                    source_task_size=source_task_size,
                    _admission_check=_admission_check,
                    _admission_strict=_admission_strict,
                )
                _await_job_future(fut, timeout_secs, what="refresh")
                self.checkout_latest()
                return self._build_refresh_result(job_id)

            # Get MV format version from metadata
            # Version 1: fragment+offset encoding, no stable row IDs
            # Version 2: stable row IDs enabled
            mv_version_bytes = metadata.get(MATVIEW_META_VERSION.encode(), b"1")
            mv_version = int(mv_version_bytes.decode())
            has_stable_row_ids = mv_version >= 2

            # Get the base version (version when MV was created)
            base_version_str = metadata.get(MATVIEW_META_BASE_VERSION.encode())
            # If no base version metadata, assume it's safe to proceed
            # (for backwards compatibility with MVs created before this feature)
            base_version = int(base_version_str.decode()) if base_version_str else None

            # Resolve src_version to actual version number if None (implicit latest)
            if src_version is None:
                source_table = self._open_mv_source_table()
                if source_table is not None:
                    src_version = source_table.version

            # Validate: if no stable row IDs and src_version differs from base, fail
            if (
                not has_stable_row_ids
                and base_version is not None
                and src_version is not None
                and src_version != base_version
            ):
                raise RuntimeError(
                    f"Cannot refresh materialized view to version {src_version} "
                    "because the source table does not have stable row IDs "
                    f"enabled.\n\n"
                    f"This materialized view was created from source version "
                    f"{base_version}. "
                    "Without stable row IDs, incremental refresh is only supported "
                    "when refreshing to the SAME version it was created from.\n\n"
                    "This limitation exists because compaction operations may have "
                    "changed the physical row IDs between versions, which would "
                    "break the materialized view's ability to track source rows.\n\n"
                    "To enable refresh across all versions, recreate the source "
                    "table with stable row IDs:\n"
                    "  db.create_table(\n"
                    "      name='table_name',\n"
                    "      data=data,\n"
                    "      storage_options={'new_table_enable_stable_row_ids': True}\n"
                    "  )"
                )

            # Note: backwards refresh (point-in-time refresh to older versions) is now
            # supported when stable row IDs are enabled. The actual rollback logic
            # (deleting rows not in the target version) is in run_ray_copy_table.

            # Dispatch via the worker-side remote wrapper; see chunker branch.
            from geneva.runners.ray.pipeline import dispatch_run_ray_refresh

            fut = dispatch_run_ray_refresh(
                self.get_reference(),
                job_id=job_id,
                src_version=src_version,
                max_rows_per_fragment=max_rows_per_fragment,
                concurrency=concurrency,
                intra_applier_concurrency=intra_applier_concurrency,
                output_limit=output_limit,
                _admission_check=_admission_check,
                _admission_strict=_admission_strict,
            )
            _await_job_future(fut, timeout_secs, what="refresh")

            # Update last refreshed version in metadata
            if src_version is not None:
                _set_last_refreshed_version(self, src_version)

            self.checkout_latest()
            return self._build_refresh_result(job_id)

    def _validate_refresh_admission(
        self,
        *,
        mv_version_str: str,
        metadata: dict,
        concurrency: int,
        intra_applier_concurrency: int,
        _admission_check: bool | None,
        _admission_strict: bool | None,
    ) -> None:
        """Driver-side admission control for refresh.

        Pulls the UDF/UDTF/Chunker resource requirements off the MV
        metadata and runs the same checks the inner pipelines used to
        run themselves before the @ray.remote refactor. Must execute on
        the driver: ``validate_admission`` queries the Ray head's
        cluster state and that call is unreliable from inside a Ray
        worker task.
        """
        from geneva.jobs.config import JobConfig
        from geneva.query import (
            MATVIEW_META_QUERY,
            MATVIEW_META_UDTF,
            GenevaQuery,
        )
        from geneva.runners.ray.admission import (
            validate_admission,
            validate_udtf_admission,
        )

        if _admission_check is False:
            return

        if mv_version_str == "udtf":
            from geneva.packager import UDTFSpec, unmarshal_udtf

            spec_json = metadata.get(MATVIEW_META_UDTF.encode())
            if not spec_json:
                return
            udtf_obj = unmarshal_udtf(UDTFSpec.from_json(spec_json.decode()))
            if udtf_obj is None:
                return
            validate_udtf_admission(
                udtf_num_cpus=udtf_obj.num_cpus or 1.0,
                udtf_num_gpus=udtf_obj.num_gpus or 0.0,
                udtf_memory=udtf_obj.memory or 0,
                concurrency=concurrency,
                check=_admission_check,
                strict=_admission_strict,
            )
            return

        if _is_chunker_mv_version(mv_version_str):
            from geneva.packager import ChunkerSpec, unmarshal_chunker

            spec_json = _get_chunker_metadata(metadata)
            if not spec_json:
                return
            chunker_obj = unmarshal_chunker(ChunkerSpec.from_json(spec_json.decode()))
            if chunker_obj is None:
                return
            validate_udtf_admission(
                udtf_num_cpus=chunker_obj.num_cpus or 1.0,
                udtf_num_gpus=chunker_obj.num_gpus or 0.0,
                udtf_memory=chunker_obj.memory or 0,
                concurrency=concurrency,
                check=_admission_check,
                strict=_admission_strict,
            )
            return

        # Plain query MV. Extract column UDFs from the source-query
        # JSON and admit each, matching ``run_ray_copy_table``'s logic.
        query_json = metadata.get(MATVIEW_META_QUERY.encode())
        if not query_json:
            return
        query = GenevaQuery.model_validate_json(query_json.decode())
        column_udfs = query.extract_column_udfs(self._conn._packager)
        if not column_udfs:
            return
        _job_cfg = JobConfig.get()
        for column_udf in column_udfs:
            validate_admission(
                column_udf.udf,
                concurrency=concurrency,
                intra_applier_concurrency=intra_applier_concurrency,
                enable_gpu_pipelining=_job_cfg.enable_gpu_pipelining,
                pipelining_num_readers=_job_cfg.pipelining_num_readers,
                check=_admission_check,
                strict=_admission_strict,
            )

    def _build_refresh_result(self, job_id: str) -> "RefreshJobResult":
        """Build a typed RefreshJobResult for the just-completed refresh.

        ``job_id`` is the real id minted in :meth:`_refresh` and threaded
        through dispatch and ``_geneva_jobs``, so callers can correlate the
        result via ``conn.get_job(result.job_id)``.

        Today's refresh path doesn't surface row-level counters from the
        executor; the result carries identifying metadata so callers can
        chain on it and extend later when counters become available.
        """
        from geneva.jobs.types import DONE, RefreshJobResult

        return RefreshJobResult(
            job_id=job_id,
            status=DONE,
            table_name=self._name,
        )

    def refresh_async(
        self,
        *,
        where: str | None = None,
        src_version: int | None = None,
        max_rows_per_fragment: int | None = None,
        concurrency: int = 8,
        intra_applier_concurrency: int = 1,
        cluster: str | None = None,
        manifest: str | None = None,
        output_limit: int | None = None,
        source_task_size: int | None = None,
        job_id: str | None = None,
        _admission_check: bool | None = None,
        _admission_strict: bool | None = None,
        **kwargs,
    ) -> "Job":
        """Refresh the materialized view asynchronously.

        refresh runs synchronously under the hood; ``refresh_async``
        wraps it in a background thread and returns a
        :class:`~geneva.jobs.types.Job` whose ``.result()`` blocks and
        yields a :class:`~geneva.jobs.types.RefreshJobResult`.

        Threading semantics: the worker is a **non-daemon** thread, so
        Python will wait for an in-flight refresh before exiting the
        process — preventing a partially-applied refresh on abrupt
        shutdown. Callers who do not want to block on completion should
        either invoke [`result`][geneva.jobs.types.Job.result] with a timeout,
        or use the synchronous [`refresh`][geneva.table.Table.refresh] directly.

        ``cluster``, ``manifest``, and ``output_limit`` mirror their
        counterparts on :meth:`refresh` and are only honored for remote
        (``db://``) connections.
        """
        if output_limit is not None:
            self._require_chunker_view("output_limit")

        if self._conn.use_remote_dispatch():
            return self._refresh_async_remote(
                src_version=src_version,
                max_rows_per_fragment=max_rows_per_fragment,
                concurrency=concurrency,
                intra_applier_concurrency=intra_applier_concurrency,
                cluster=cluster,
                manifest=manifest,
                output_limit=output_limit,
                source_task_size=source_task_size,
                **kwargs,
            )

        from geneva.jobs.types import Job, RefreshJobResult

        result_holder: dict[str, Any] = {}
        error_holder: dict[str, BaseException] = {}
        done_event = threading.Event()
        if job_id is None:
            job_id = uuid.uuid4().hex

        def _run() -> None:
            try:
                result_holder["value"] = self.refresh(
                    where=where,
                    src_version=src_version,
                    max_rows_per_fragment=max_rows_per_fragment,
                    concurrency=concurrency,
                    intra_applier_concurrency=intra_applier_concurrency,
                    output_limit=output_limit,
                    source_task_size=source_task_size,
                    job_id=job_id,
                    _admission_check=_admission_check,
                    _admission_strict=_admission_strict,
                    **kwargs,
                )
            except BaseException as e:
                error_holder["error"] = e
            finally:
                done_event.set()

        thread = threading.Thread(
            target=_run,
            name=f"refresh-{job_id}",
            daemon=False,
        )
        thread.start()

        future = _ThreadJobFuture(
            job_id=job_id,
            done_event=done_event,
            result_holder=result_holder,
            error_holder=error_holder,
        )
        return Job(
            future,
            table_name=self._name,
            result_cls=RefreshJobResult,
        )

    def _require_chunker_view(self, kwarg_name: str) -> None:
        """Raise ValueError if this table is not a chunker-backed MV.

        Used to guard chunker-only kwargs (e.g. ``output_limit``) before
        round-tripping the request to phalanx, so the caller gets a fast,
        local error instead of a server-side 400.
        """
        metadata = self.schema.metadata or {}
        mv_version_b = metadata.get(MATVIEW_META_VERSION.encode())
        mv_version_str = mv_version_b.decode() if mv_version_b else None
        if not _is_chunker_mv_version(mv_version_str):
            raise ValueError(
                f"{kwarg_name} is only valid for chunker-backed materialized "
                f"views; this view's kind is {mv_version_str!r}."
            )

    def _open_mv_source_table(self) -> "Table | None":
        """Open the source table for this materialized view.
        Uses namespace-aware connection logic when the view was created from a
        namespace-based source.  Returns ``None`` when source identity is
        missing from the view's serialized source-query JSON.
        """
        from geneva.query import resolve_mv_source_identity

        source_table_name, source_db_uri, namespace_path = resolve_mv_source_identity(
            self.schema.metadata
        )
        if not source_table_name or not source_db_uri:
            return None

        if source_db_uri == self._conn._uri:
            return self._conn.open_table(source_table_name, namespace=namespace_path)

        return connect(
            source_db_uri,
            api_key=_plain_api_key(self._conn._api_key),
            host_override=self._conn._host_override,
            storage_options=self._conn._storage_options,
            namespace_client_pushdown_operations=(
                self._conn.namespace_client_pushdown_operations
            ),
            system_namespace=self._conn.system_namespace,
        ).open_table(source_table_name, namespace=namespace_path)

    def plan_refresh(
        self,
        *,
        src_version: int | None = None,
    ) -> RefreshPlan:
        """Plan a refresh without dispatching: count new source fragments.

        Returns a ``RefreshPlan`` describing what work a ``refresh()`` call
        would perform.  Does not require a Ray cluster.
        """
        import lance as _lance

        from geneva.runners.ray.pipeline import (
            _extract_fragment_ids_from_row_ids,
            _identify_new_source_fragments,
        )

        schema = self.schema
        metadata = schema.metadata or {}

        # Check MV type — UDTF views always have work
        mv_version_bytes = metadata.get(MATVIEW_META_VERSION.encode(), b"1")
        mv_version_str = mv_version_bytes.decode()
        if mv_version_str == "udtf" or _is_chunker_mv_version(mv_version_str):
            return RefreshPlan(
                table_name=self.name,
                version=self.version,
                has_work=True,
                total_tasks=0,
                total_rows_pending=0,
                skipped_fragments=0,
                skipped_rows=0,
                total_fragments=0,
                total_rows=0,
            )

        mv_version = int(mv_version_str)

        source_table = self._open_mv_source_table()
        if source_table is None:
            return RefreshPlan(
                table_name=self.name,
                version=self.version,
                has_work=False,
                total_tasks=0,
                total_rows_pending=0,
                skipped_fragments=0,
                skipped_rows=0,
                total_fragments=0,
                total_rows=0,
            )

        effective_src_version = (
            src_version if src_version is not None else source_table.version
        )
        src_dataset = _lance.dataset(
            source_table.uri,
            version=effective_src_version,
            storage_options=source_table._storage_options,
        )

        # Open destination dataset at current version
        dst_dataset = _lance.dataset(
            self.uri,
            version=self.version,
            storage_options=self._storage_options,
        )

        # Collect all __source_row_id values already present in the MV
        existing_src_row_ids: set[int] = set()
        dst_frags = list(dst_dataset.get_fragments())
        for dst_frag in dst_frags:
            try:
                row_ids = (
                    dst_frag.to_table(columns=["__source_row_id"])
                    .column("__source_row_id")
                    .to_pylist()
                )
                existing_src_row_ids.update(rid for rid in row_ids if rid is not None)
            except Exception:  # noqa: PERF203
                _LOG.debug(
                    "Could not read __source_row_id from dst frag %s",
                    dst_frag.fragment_id,
                )

        has_stable_row_ids = mv_version >= 2
        if has_stable_row_ids:
            # V2: stable row IDs can't be decoded to fragment IDs.
            # Compare source _rowid sets directly to find new rows.
            all_src_frags = list(src_dataset.get_fragments())
            total_src_rows = 0
            new_rows = 0
            new_src_frag_count = 0
            for frag in all_src_frags:
                total_src_rows += frag.count_rows()
                src_rids = set(
                    frag.to_table(columns=[], with_row_id=True)
                    .column("_rowid")
                    .to_pylist()
                )
                missing = src_rids - existing_src_row_ids
                if missing:
                    new_rows += len(missing)
                    new_src_frag_count += 1
        else:
            # V1: fragment+offset encoding — use fragment ID mapping
            dst_to_src_map: dict[int, set[int]] = {}
            for dst_frag in dst_frags:
                dst_frag_id = dst_frag.fragment_id
                try:
                    src_row_ids_list = (
                        dst_frag.to_table(columns=["__source_row_id"])
                        .column("__source_row_id")
                        .to_pylist()
                    )
                    src_frag_ids = _extract_fragment_ids_from_row_ids(
                        [rid for rid in src_row_ids_list if rid is not None],
                        mv_version,
                    )
                    dst_to_src_map[dst_frag_id] = src_frag_ids
                except Exception:
                    dst_to_src_map[dst_frag_id] = set()

            new_src_frag_ids = set(
                _identify_new_source_fragments(src_dataset, dst_to_src_map)
            )

            all_src_frags = list(src_dataset.get_fragments())
            total_src_rows = 0
            new_rows = 0
            for frag in all_src_frags:
                rows = frag.count_rows()
                total_src_rows += rows
                if frag.fragment_id in new_src_frag_ids:
                    new_rows += rows
            new_src_frag_count = len(new_src_frag_ids)

        # Also check for uncomputed UDF columns (NULL values in columns
        # marked as virtual_column).  This detects the case where
        # create_materialized_view populated __source_row_id placeholders
        # but refresh() hasn't run the UDFs yet.
        stale_rows = 0
        dst_schema = dst_dataset.schema
        udf_cols = [
            f.name
            for f in dst_schema
            if f.metadata and f.metadata.get(b"virtual_column") == b"true"
        ]
        if udf_cols and not new_rows:
            # Only check when there are no new source rows — if there are
            # new rows the refresh will reprocess anyway.
            null_filter = " OR ".join(f"{c} IS NULL" for c in udf_cols)
            stale_rows = dst_dataset.count_rows(filter=null_filter)

        has_work = new_rows > 0 or stale_rows > 0

        return RefreshPlan(
            table_name=self.name,
            version=self.version,
            has_work=has_work,
            total_tasks=new_src_frag_count,
            total_rows_pending=new_rows + stale_rows,
            skipped_fragments=len(dst_frags),
            skipped_rows=len(existing_src_row_ids),
            total_fragments=len(all_src_frags),
            total_rows=total_src_rows,
            new_source_fragments=new_src_frag_count,
            stale_rows=stale_rows,
        )

    def _refresh_udtf_matview(
        self,
        src_version: int | None = None,
        concurrency: int = 8,
        _admission_check: bool | None = None,
        _admission_strict: bool | None = None,
        *,
        job_id: str | None = None,
        job_tracker: Any | None = None,
    ) -> None:
        """Refresh a UDTF-backed materialized view (full refresh).

        Re-executes the UDTF against the source table via Ray and overwrites
        the view with the new results.  Uses an ActorPool for fault-tolerant
        parallel execution and a JobTracker for progress metrics.
        Per-batch checkpointing allows failed refreshes to resume from the
        last completed batch.

        Ordering guarantees: within a single partition, batch indices are
        deterministic (0, 1, 2, ...) based on the generator yield order, and
        the source scan order is deterministic for a given pinned version.
        Across partitions, execution and assembly order is not guaranteed.
        """
        import functools
        import uuid

        import ray

        import geneva.cloudpickle as cloudpickle
        from geneva.checkpoint_utils import (
            format_udtf_checkpoint_prefix,
        )
        from geneva.packager import UDTFSpec, unmarshal_udtf
        from geneva.query import open_read_dataset
        from geneva.runners.ray.admission import (
            PipelineResourceConfig,
            validate_udtf_admission,
        )
        from geneva.runners.ray.jobtracker import (
            JobTracker,
            job_tracker_throttle_kwargs,
        )
        from geneva.runners.ray.pipeline import _emit_phase

        schema = open_read_dataset(self).schema
        metadata = schema.metadata or {}
        # Durable phase progression mirrors backfill: planning -> executing.
        _hist = getattr(self._conn, "_history", None)
        _emit_phase(_hist, job_id, "Job planning")

        # Load UDTF from metadata
        udtf_spec_json = metadata.get(MATVIEW_META_UDTF.encode())
        if not udtf_spec_json:
            raise ValueError(
                "Cannot refresh: No UDTF specification found in view metadata."
            )

        udtf_spec = UDTFSpec.from_json(udtf_spec_json.decode())
        udtf_obj = unmarshal_udtf(udtf_spec)
        if udtf_obj is None:
            raise ValueError(
                "Cannot refresh: Failed to deserialize UDTF. "
                "The UDTF module may not be available in this environment."
            )

        # Load source query
        source_query_bytes: bytes | None = metadata.get(MATVIEW_META_QUERY.encode())

        # Get source table info from the embedded source-query identity.
        from geneva.query import resolve_mv_source_identity

        source_name, source_uri, namespace_path = resolve_mv_source_identity(metadata)
        if not source_name or not source_uri:
            raise ValueError(
                "Cannot refresh: Source table information not found in view metadata."
            )

        if source_uri == self._conn._uri or (
            isinstance(source_uri, str)
            and source_uri.startswith("db://")
            and self._conn.namespace_client_impl == "dir"
        ):
            src_tbl = self._conn.open_table(source_name, namespace_path=namespace_path)
        else:
            src_tbl = connect(
                source_uri,
                api_key=_plain_api_key(self._conn._api_key),
                host_override=self._conn._host_override,
                storage_options=self._conn._storage_options,
                namespace_client_pushdown_operations=(
                    self._conn.namespace_client_pushdown_operations
                ),
                system_namespace=self._conn.system_namespace,
            ).open_table(source_name, namespace_path=namespace_path)
        source_api_key = _plain_api_key(src_tbl._conn._api_key)
        source_host_override = src_tbl._conn._host_override

        # Determine actual source version
        if src_version is not None:
            actual_source_version = src_version
        else:
            actual_source_version = src_tbl.version
        src_tbl.checkout(actual_source_version)

        # Version-aware bail-out: skip refresh if source hasn't changed
        # and the view already has data (not the initial empty state after
        # create_udtf_view).
        base_version_str = metadata.get(MATVIEW_META_BASE_VERSION.encode())
        base_version = int(base_version_str.decode()) if base_version_str else None
        if (
            base_version is not None
            and base_version == actual_source_version
            and self.count_rows() > 0
        ):
            _LOG.info(
                "UDTF source unchanged (version %d), skipping refresh",
                base_version,
            )
            return

        # Ensure Ray is initialized
        if get_current_context() is None:
            _LOG.warning(_IMPLICIT_LOCAL_RAY_WARNING, "_refresh_udtf_matview()")
            ray.init(ignore_reinit_error=True)

        # --- Admission control ---
        udtf_num_cpus = udtf_obj.num_cpus or 1.0
        udtf_num_gpus = udtf_obj.num_gpus or 0.0
        udtf_memory = udtf_obj.memory or 0
        validate_udtf_admission(
            udtf_num_cpus=udtf_num_cpus,
            udtf_num_gpus=udtf_num_gpus,
            udtf_memory=udtf_memory,
            concurrency=concurrency,
            check=_admission_check,
            strict=_admission_strict,
        )

        # Open checkpoint store
        table_ref = self.get_reference()
        checkpoint_store = table_ref.open_checkpoint_store()
        top_prefix = format_udtf_checkpoint_prefix(
            udtf_name=udtf_obj.name,
            udtf_version=udtf_obj.version,
            source_version=actual_source_version,
        )

        udtf_pickle = cloudpickle.dumps(udtf_obj)
        error_handling_pickle: bytes | None = (
            cloudpickle.dumps(udtf_obj.error_handling)
            if udtf_obj.error_handling is not None
            else None
        )
        ckp_uri = checkpoint_store.uri()

        if job_id is None:
            job_id = uuid.uuid4().hex
        if job_tracker is None:
            rc = PipelineResourceConfig.get()
            job_tracker = JobTracker.options(
                name=f"jobtracker-udtf-{job_id}",
                num_cpus=rc.jobtracker_num_cpus,
                memory=rc.jobtracker_memory,
                max_restarts=-1,
            ).remote(  # type: ignore[call-arg]
                job_id,
                table_ref,
                enable_saves=True,
                **job_tracker_throttle_kwargs(),
            )

        # Register with cluster exit bookkeeping so the cluster won't be
        # torn down while the UDTF matview refresh is still running.
        from geneva.runners.ray.raycluster import RayCluster

        ctx = get_current_context()
        if isinstance(ctx, RayCluster):
            sentinel_ref = ray.put(True)
            ctx.register_tracked_job(job_id, sentinel_ref, job_tracker)

        # --- Actor resource kwargs ---
        actor_resource_kwargs: dict[str, Any] = {
            "num_cpus": udtf_num_cpus,
            "num_gpus": udtf_num_gpus,
        }
        if udtf_obj.memory is not None:
            actor_resource_kwargs["memory"] = udtf_obj.memory

        # --- Actor factory ---
        # Use self.uri instead of constructing from self._conn._uri directly
        # so that namespace-backed connections resolve the correct table
        # location via the catalog.
        dest_table_uri = self.uri
        try:
            from geneva.query import open_read_dataset

            dest_data_storage_version: str | None = open_read_dataset(
                self
            ).data_storage_version
        except Exception:
            dest_data_storage_version = None
        actor_cls = _get_udtf_processor_actor().options(**actor_resource_kwargs)

        ns_config = src_tbl._conn._ns_config.for_worker()

        actor_factory = functools.partial(
            actor_cls.remote,
            udtf_pickle_bytes=udtf_pickle,
            source_uri=source_uri,
            source_api_key=source_api_key,
            source_host_override=source_host_override,
            source_name=source_name,
            source_query_json_bytes=source_query_bytes,
            ckp_store_uri=ckp_uri,
            error_handling_pickle_bytes=error_handling_pickle,
            job_id=job_id,
            dest_table_uri=dest_table_uri,
            dest_table_name=self.name,
            dest_data_storage_version=dest_data_storage_version,
            source_version=actual_source_version,
            namespace_config=ns_config,
            namespace_path=namespace_path,
        )

        _emit_phase(_hist, job_id, "Executing refresh")
        try:
            self._run_udtf_refresh(
                udtf_obj=udtf_obj,
                job_tracker=job_tracker,
                checkpoint_store=checkpoint_store,
                metadata=metadata,
                actual_source_version=actual_source_version,
                concurrency=concurrency,
                top_prefix=top_prefix,
                src_tbl=src_tbl,
                table_ref=table_ref,
                actor_factory=actor_factory,
                dest_table_uri=dest_table_uri,
                job_id=job_id,
            )
        finally:
            # Signal the JobTracker that this job is finished so that
            # _wait_for_tracked_jobs can detect completion.
            with contextlib.suppress(Exception):
                job_tracker.mark_job_done.remote()

        self.checkout_latest()

    def _run_udtf_refresh(  # noqa: C901
        self,
        *,
        udtf_obj: Any,
        job_tracker: Any,
        checkpoint_store: "CheckpointStore",
        metadata: dict[bytes, bytes],
        actual_source_version: int,
        concurrency: int,
        top_prefix: str,
        src_tbl: Any,
        table_ref: Any,
        actor_factory: Any,
        dest_table_uri: str,
        job_id: str,
    ) -> None:
        """Execute UDTF dispatch + assembly.

        Separated from ``_refresh_udtf_matview`` so the caller can guarantee
        ``mark_job_done`` in a ``finally`` block.

        Actors write data files directly into the destination dataset via
        ``LanceFragment.create()`` and return lightweight ``FragmentMetadata``
        JSON.  The driver collects all fragment metadata (from fresh results
        and from the checkpoint store for resumed partitions) and performs a
        single ``LanceOperation.Overwrite`` + ``LanceDataset.commit()``.
        """
        import lance
        from lance.fragment import FragmentMetadata

        from geneva.checkpoint_utils import (
            format_udtf_fragment_key,
            format_udtf_partition_prefix,
        )
        from geneva.runners.ray.actor_pool import ActorPool
        from geneva.runners.ray.jobtracker import report_plan_progress
        from geneva.runners.ray.pipeline import _emit_otel_metrics
        from geneva.tqdm import Colors, fmt, tqdm

        # --- Build work items ---
        # work_items: list of (partition_filter, partition_prefix, index_info)
        work_items: list[tuple[str | None, str, _IndexPartitionInfo | None]] = []
        completed_fragment_keys: set[str] | None = None

        # Planning sub-step for the live plan line (the partitions bar takes over
        # once work items are known and dispatched below).
        report_plan_progress(job_tracker, desc="discovering partitions")

        if udtf_obj.partition_by_indexed_column:
            completed_fragment_keys = set(checkpoint_store.list_keys(top_prefix))
            work_items, distinct_values = _build_index_partition_work_items(
                src_tbl,
                udtf_obj.partition_by_indexed_column,
                top_prefix,
                checkpoint_store,
                completed_fragment_keys=completed_fragment_keys,
            )
        elif udtf_obj.partition_by:
            work_items, distinct_values = _build_column_partition_work_items(
                src_tbl, udtf_obj.partition_by, top_prefix, checkpoint_store
            )
        else:
            part_prefix = format_udtf_partition_prefix(
                top_prefix, partition_col=None, partition_value=None
            )
            frag_key = format_udtf_fragment_key(part_prefix)
            if frag_key in checkpoint_store:
                _LOG.info(
                    "UDTF (unpartitioned) already completed, loading from checkpoint"
                )
            else:
                work_items.append((None, part_prefix, None))

        report_plan_progress(job_tracker, n=1, total=1)

        # --- ActorPool dispatch ---
        # Collect FragmentMetadata JSON from fresh actor results.
        fresh_fragment_jsons: list[str] = []
        all_error_dicts: list[dict] = []
        if work_items:
            num_actors = min(len(work_items), concurrency)
            # Annotate the active ``geneva.job`` span with the precomputed
            # UDTF dispatch shape.
            telemetry.set_current_span_attrs(
                {
                    "job_type": "refresh",
                    "concurrency": concurrency,
                    "partitions": len(work_items),
                    "actors": num_actors,
                }
            )
            job_tracker.set_total.remote("partitions", len(work_items))
            job_tracker.set_desc.remote("partitions", "Partitions processed")
            job_tracker.set_desc.remote("rows_produced", "Rows produced")

            pool = ActorPool(
                actor_factory,
                num_actors,
                job_tracker=job_tracker,
                worker_metric="workers",
            )
            skipped_count = 0
            empty_count = 0
            total_rows_produced = 0
            bar_partitions = tqdm(
                total=len(work_items),
                desc=fmt("udtf | partitions", Colors.CYAN, bold=True),
                unit="part",
            )
            bar_rows = tqdm(
                total=0,
                bar_format="{desc}: {n_fmt} [{elapsed}]",
                desc=fmt("udtf | rows produced", Colors.CYAN, bold=True),
            )
            # Capture the current (``geneva.job``) trace context so each remote
            # ``process_partition`` span links back into this job's trace.
            trace_carrier = telemetry.inject_context()
            try:
                for result in pool.map_unordered(
                    lambda actor, item: actor.process_partition.remote(
                        item[0],
                        item[1],
                        (
                            (
                                item[2].partition_ordinal,
                                item[2].index_name,
                                item[2].column,
                            )
                            if item[2] is not None
                            else None
                        ),
                        trace_carrier,
                    ),
                    work_items,
                ):
                    fragment_json, error_dicts, stats = result
                    if error_dicts:
                        skipped_count += 1
                    elif fragment_json is None:
                        empty_count += 1
                    else:
                        fresh_fragment_jsons.append(fragment_json)
                    rows_this_partition = stats.get("rows", 0)
                    total_rows_produced += rows_this_partition
                    all_error_dicts.extend(error_dicts)
                    # Per-partition OTel metrics, mirroring the backfill
                    # ``execute`` stage. Times are ms histograms; the rest
                    # are counters (see ``_emit_otel_metrics``).
                    _emit_otel_metrics(
                        {
                            "udtf_execute_time": int(
                                stats.get("execute_time_s", 0.0) * 1000
                            ),
                            "udtf_checkpoint_time": int(
                                stats.get("checkpoint_time_s", 0.0) * 1000
                            ),
                            "udtf_rows_produced": int(rows_this_partition),
                            "udtf_batches": int(stats.get("batches", 0)),
                            "udtf_partitions_completed": 1,
                        },
                        job_type="refresh",
                        stage="execute",
                        job_id=job_id,
                        table=table_ref.table_name,
                    )
                    job_tracker.increment.remote("partitions", 1)
                    if rows_this_partition:
                        job_tracker.increment.remote(
                            "rows_produced", rows_this_partition
                        )
                    bar_partitions.update(1)
                    bar_rows.n = total_rows_produced
                    bar_rows.refresh()
            finally:
                bar_partitions.close()
                bar_rows.close()
                # Flush each worker's buffered spans BEFORE shutdown: shutdown()
                # ray.kills and drops every idle actor, so a broadcast after it
                # reaches zero actors (atexit does not run under ray.kill).
                pool.broadcast("flush_telemetry")
                pool.shutdown()
            if skipped_count:
                _LOG.warning(
                    "UDTF refresh: %d/%d partitions skipped due to errors",
                    skipped_count,
                    len(work_items),
                )
            if empty_count:
                _LOG.info(
                    "UDTF refresh: %d/%d partitions produced no output rows",
                    empty_count,
                    len(work_items),
                )

        # --- ErrorStore bulk logging ---
        if all_error_dicts:
            from geneva.debug.error_store import ErrorRecord, ErrorStore

            error_store = ErrorStore(self._conn, namespace=self._conn.system_namespace)
            errors = [ErrorRecord(**d) for d in all_error_dicts]
            error_store.log_errors(errors)

        # --- Collect FragmentMetadata from checkpoint store (resumed partitions) ---
        # Load completed partitions that were not in this run's work items.
        # Indexed planning already listed their keys in bulk.

        def _load_checkpoint_fragment(pfx: str) -> str | None:
            """Load FragmentMetadata JSON from checkpoint, or None."""
            frag_key = format_udtf_fragment_key(pfx)
            if completed_fragment_keys is not None:
                if frag_key not in completed_fragment_keys:
                    return None
            elif frag_key not in checkpoint_store:
                return None
            batch = checkpoint_store[frag_key]
            return batch.column("fragment_json")[0].as_py()  # type: ignore[return-value]

        fresh_set = set(fresh_fragment_jsons)
        checkpoint_fragment_jsons: list[str] = []

        # Build list of all partition prefixes to scan
        all_prefixes: list[str] = []
        if udtf_obj.partition_by_indexed_column:
            partition_col = _IVF_PARTITION_COL
            all_prefixes.extend(
                format_udtf_partition_prefix(
                    top_prefix, partition_col=partition_col, partition_value=v
                )
                for v in distinct_values
            )
        elif udtf_obj.partition_by:
            partition_col = udtf_obj.partition_by
            all_prefixes.extend(
                format_udtf_partition_prefix(
                    top_prefix, partition_col=partition_col, partition_value=v
                )
                for v in distinct_values
            )
        else:
            all_prefixes.append(
                format_udtf_partition_prefix(
                    top_prefix, partition_col=None, partition_value=None
                )
            )

        for pfx in all_prefixes:
            fj = _load_checkpoint_fragment(pfx)
            if fj is not None and fj not in fresh_set:
                checkpoint_fragment_jsons.append(fj)

        # --- Single Overwrite commit ---
        all_fragment_jsons = fresh_fragment_jsons + checkpoint_fragment_jsons
        all_fragment_metas = [
            FragmentMetadata.from_json(fj) for fj in all_fragment_jsons
        ]

        # Get storage options from namespace if configured
        storage_options = None
        ns_client = table_ref.namespace_config.connect_namespace_client()
        if ns_client is not None and table_ref.table_id:
            from lance_namespace import DescribeTableRequest

            response = ns_client.describe_table(
                DescribeTableRequest(id=table_ref.table_id)
            )
            storage_options = response.storage_options

        new_metadata: dict[str | bytes, str | bytes] = dict(metadata)  # type: ignore[arg-type]
        new_metadata[MATVIEW_META_BASE_VERSION.encode()] = str(
            actual_source_version
        ).encode()
        new_schema = udtf_obj.output_schema.with_metadata(new_metadata)

        if all_fragment_metas:
            operation = lance.LanceOperation.Overwrite(new_schema, all_fragment_metas)
            get_committer().commit(
                dest_table_uri,
                operation,
                storage_options=storage_options,
            )
        else:
            # No partitions produced data -- write empty table with metadata.
            # write-guard-ok: empty-table fallback, no rows to fault
            lance.write_dataset(
                new_schema.empty_table(),
                dest_table_uri,
                mode="overwrite",
                storage_options=storage_options,
            )

    def _validate_update_mode(
        self,
        update_mode: "str | None",
        *,
        num_frags: "int | None" = None,
        skip_frags: int = 0,
        read_version: "int | None" = None,
    ) -> None:
        """Validate an explicit ``update_mode`` before any dispatch -- shared by
        ``backfill`` and ``backfill_async`` so neither path (nor a remote async one)
        can route an unvalidated mode to the Ray remote, which treats any non-None
        value as sparse."""
        if update_mode is None:
            return
        from geneva.runners.sparse_update import SPARSE_UPDATE_MODE

        if update_mode != SPARSE_UPDATE_MODE:
            raise ValueError(
                f"unknown update_mode {update_mode!r}; "
                f"supported: {SPARSE_UPDATE_MODE!r}"
            )
        # Fragment windowing is ill-defined for sparse: it relocates rows
        # (delete+append), so the fragment set is a moving target. Reject rather
        # than silently updating every matching fragment.
        if num_frags is not None or skip_frags:
            raise NotImplementedError(
                f"update_mode={SPARSE_UPDATE_MODE!r} does not support fragment "
                "windowing (num_frags / skip_frags); sparse relocates fragments, so a "
                "window is ill-defined. Omit them, or use the default backfill path."
            )
        # Sparse reads the live dataset (it re-derives work each round to follow
        # compactions), so it cannot honor a historical snapshot. Reject an explicit
        # read_version older than current rather than silently reading live.
        if read_version is not None and read_version != self.version:
            raise NotImplementedError(
                f"update_mode={SPARSE_UPDATE_MODE!r} does not support a historical "
                f"read_version (got {read_version}, current is {self.version}); sparse "
                "reads the live dataset. Omit read_version, or use the default "
                "backfill path for a pinned snapshot."
            )
        # Sparse mode is not yet supported on remote (namespace-dispatched)
        # connections -- the namespace request schema carries no update_mode field.
        # Fail clearly instead of silently falling back to carry-forward.
        if self._conn.use_remote_dispatch():
            raise NotImplementedError(
                f"update_mode={SPARSE_UPDATE_MODE!r} is not yet supported on remote "
                "(namespace-dispatched) connections; it must be piped through the "
                "namespace client. Use a direct connection for now."
            )

    def backfill_async(
        self,
        columns: "str | list[str]",
        *,
        udf: UDF | None = None,
        where: str | None = None,
        concurrency: int = 8,
        intra_applier_concurrency: int = 1,
        _admission_check: bool | None = None,
        _admission_strict: bool | None = None,
        min_checkpoint_size: int | None = None,
        max_checkpoint_size: int | None = None,
        batch_checkpoint_flush_interval_seconds: float | None = None,
        _enable_job_tracker_saves: bool = True,
        job_tracker_min_update_interval_secs: float | None = None,
        job_id: str | None = None,
        _return_future: bool = False,
        _root_span: bool = True,
        **kwargs,
    ) -> "JobFuture | Job":
        """
        Backfills the specified column asynchronously.

        Returns a :class:`~geneva.jobs.types.Job` whose ``.result()`` blocks
        and yields a :class:`~geneva.jobs.types.BackfillJobResult`.

        Parameters
        ----------
        columns: str | list[str]
            Target column name to backfill. A single-element list is
            equivalent to a string. Multi-column backfill is not yet
            supported and raises ``NotImplementedError``.
        udf: UDF | None
            Optionally override the UDF used to backfill the column.
        where: str | None
            SQL expression filter to select rows to backfill. Defaults to
            '<col_name> IS NULL' to skip already-computed rows. Use where="1=1"
            to force reprocessing all rows.
        concurrency: int
            (default = 8) This controls the number of processes that tasks run
            concurrently. For max throughput, ideally this is larger than the number
            of nodes in the k8s cluster.   This is the number of Ray actor processes
            are started.
        intra_applier_concurrency: int
            (default = 1) This controls the number of threads used to execute tasks
            within a process. Multiplying this times `concurrency` roughly corresponds
            to the number of cpu's being used.
        _admission_check: bool | None
            Whether to run admission control to validate cluster resources before
            starting the job. If None, uses GENEVA_ADMISSION__CHECK env var
            (default: true). Set to False to skip the check.
            **Experimental**: Parameters starting with `_` are subject to change.
        _admission_strict: bool | None
            If True, raises ResourcesUnavailableError when resources are
            insufficient. If False, logs a warning but allows the job to proceed.
            If None, uses GENEVA_ADMISSION__STRICT env var (default: false, i.e.
            warn and proceed).
            **Experimental**: Parameters starting with `_` are subject to change.
        commit_granularity: int | None
            (default = 64) Show a partial result everytime this number of fragments
            are completed. If None, the entire result is committed at once.
        read_version: int | None
            (default = None) The version of the table to read from.  If None, the
            latest version is used.
        task_shuffle_diversity: int | None
            (default = 8) ??
        batch_size: int | None (deprecated)
            (default = 10240) Legacy alias for checkpoint_size. Prefer checkpoint_size.
        checkpoint_size: int | None
            The max number of rows per checkpoint.
            This influences how often progress and proof of life is presented.
            When adaptive sizing is enabled, an explicit checkpoint_size seeds the
            initial checkpoint size; otherwise the initial size defaults to
            min_checkpoint_size.
        min_checkpoint_size: int | None
            Minimum adaptive checkpoint size (lower bound).
        max_checkpoint_size: int | None
            Maximum adaptive checkpoint size (upper bound). This also caps the
            largest read batch and thus the maximum memory footprint per batch.
        batch_checkpoint_flush_interval_seconds: float | None
            Controls how frequently in-progress results are persisted as batch
            checkpoints. Larger values usually improve throughput, but if the
            job stops unexpectedly, more recently computed work may need to be
            redone. Smaller values checkpoint progress sooner, which improves
            durability and resume behavior, but can reduce throughput. Set to
            ``0`` to persist every batch as soon as it is produced.
        task_size: int | None
            Controls read-task sizing (rows per worker task). Defaults to
            ``min(table.count_rows() // num_workers // 2,
            max_fragment_size)`` when omitted, where ``max_fragment_size`` is
            the largest fragment in the pinned read snapshot.
        num_frags: int | None
            (default = None) The number of table fragments to process.  If None,
            process all fragments.
        skip_frags: int
            (default = 0) Number of fragments to skip before processing.
            Combined with ``num_frags`` this allows batching through a large
            dataset in manageable chunks. For example, ``skip_frags=100,
            num_frags=50`` processes fragments 100–149.
        _enable_job_tracker_saves: bool
            (default = False) Experimentally enable persistence of job metrics to the
            database. When disabled, metrics are tracked in-memory only.
        job_tracker_min_update_interval_secs: float | None
            (default = None) Per-job override for the *initial* seconds between
            throttled metric saves. Overrides the global
            ``GENEVA_JOB_TRACKER__MIN_UPDATE_INTERVAL_SECS``. The interval still
            grows with job runtime toward the configured ceiling, and
            terminal/forced saves always bypass the throttle. If None, the
            global config is used.
        """
        col_name = _normalize_backfill_columns(columns)
        col_name = self._canonical_backfill_output_column(col_name)
        self._validate_update_mode(
            kwargs.get("update_mode"),
            num_frags=kwargs.get("num_frags"),
            skip_frags=kwargs.get("skip_frags", 0),
            read_version=kwargs.get("read_version"),
        )

        # V2 remote path: route through namespace API
        if self._conn.use_remote_dispatch():
            if udf is not None:
                raise NotImplementedError(
                    "backfill_async(udf=...) is not yet supported for remote "
                    "connections. Call alter_columns() to update the UDF first."
                )
            if _admission_check is not None or _admission_strict is not None:
                raise NotImplementedError(
                    "Admission control is not yet supported for remote connections."
                )
            return self._backfill_async_v2(
                col_name,
                where=where,
                concurrency=concurrency,
                intra_applier_concurrency=intra_applier_concurrency,
                min_checkpoint_size=min_checkpoint_size,
                max_checkpoint_size=max_checkpoint_size,
                batch_checkpoint_flush_interval_seconds=batch_checkpoint_flush_interval_seconds,
                cluster=kwargs.get("cluster"),
                manifest=kwargs.get("manifest"),
                _return_future=_return_future,
                **{k: v for k, v in kwargs.items() if k not in ("cluster", "manifest")},
            )

        from geneva.runners.ray.pipeline import dispatch_run_ray_add_column

        if min_checkpoint_size is not None:
            kwargs["min_checkpoint_size"] = min_checkpoint_size
        if max_checkpoint_size is not None:
            kwargs["max_checkpoint_size"] = max_checkpoint_size
        if batch_checkpoint_flush_interval_seconds is not None:
            kwargs["batch_checkpoint_flush_interval_seconds"] = (
                batch_checkpoint_flush_interval_seconds
            )

        self._normalize_backfill_batch_kwargs(kwargs)

        read_version = kwargs.get("read_version")
        if read_version is None:
            read_version = self.version
            kwargs["read_version"] = read_version

        original_where = where
        unpack_context = self._get_unpack_backfill_context(col_name)
        current_udf, resolved_where, udf_mismatch, srcfiles_mismatch = (
            self._resolve_backfill_context(
                col_name, udf=udf, where=where, read_version=read_version
            )
        )
        expected_default_where = (
            unpack_context.default_where
            if unpack_context is not None
            else f"{col_name} IS NULL"
        )
        default_where_generated = (
            original_where is None and resolved_where == expected_default_where
        )
        where = resolved_where
        if (
            udf_mismatch
            or srcfiles_mismatch
            or _is_intentional_full_reprocess_where(original_where)
        ):
            kwargs.setdefault("_skip_checkpoint_index_scan", True)

        # Admission control: validate cluster has sufficient resources
        # Always call validate_admission when there's a UDF - it handles check=None
        # by reading from config (GENEVA_ADMISSION__CHECK env var, default True)
        from geneva.jobs.config import JobConfig
        from geneva.runners.ray.admission import validate_admission

        if current_udf is not None:
            # Mirror setup_actor's CPU reservation so admission catches
            # the documented pipelining-readers footgun (reserved
            # 1+pipelining_num_readers CPUs but admission saw 1) before
            # the actor wedges Ray's lease queue indefinitely.
            _job_cfg = JobConfig.get()
            validate_admission(
                current_udf,
                concurrency=concurrency,
                intra_applier_concurrency=intra_applier_concurrency,
                enable_gpu_pipelining=_job_cfg.enable_gpu_pipelining,
                pipelining_num_readers=_job_cfg.pipelining_num_readers,
                check=_admission_check,
                strict=_admission_strict,
            )

        # Mint the job_id up front so the root span carries the real id.
        if job_id is None:
            job_id = uuid.uuid4().hex
        # Root job-type span. Opened here — the async entry point that both sync
        # and fire-and-forget callers funnel through — and tied to the future so
        # it closes when the job resolves, covering job execution for both. The
        # sync wrapper owns its own span and passes _root_span=False to avoid a
        # duplicate; attach_span(None) / close_span(None) are then no-ops.
        _ba_ref = self.get_reference()
        _ba_span = (
            telemetry.open_span(
                "backfill",
                {
                    "job_id": job_id,
                    "job_type": "backfill",
                    "table": _ba_ref.table_name,
                    "table_uri": _ba_ref.table_uri or "",
                    "column": col_name,
                },
            )
            if _root_span
            else None
        )
        try:
            with telemetry.attach_span(_ba_span):
                fut = dispatch_run_ray_add_column(
                    self.get_reference(),
                    col_name,
                    udf=udf,
                    where=where,
                    default_where_generated=default_where_generated,
                    unpack_fields=(
                        unpack_context.fields if unpack_context is not None else None
                    ),
                    checkpoint_column=(
                        unpack_context.checkpoint_column
                        if unpack_context is not None
                        else None
                    ),
                    concurrency=concurrency,
                    intra_applier_concurrency=intra_applier_concurrency,
                    enable_job_tracker_saves=_enable_job_tracker_saves,
                    job_tracker_min_update_interval_secs=(
                        job_tracker_min_update_interval_secs
                    ),
                    job_id=job_id,
                    **kwargs,
                )
        except BaseException as e:
            telemetry.close_span(_ba_span, e)
            raise
        if _ba_span is not None:
            fut._otel_span = _ba_span
        if _return_future:
            return fut

        from geneva.jobs.types import BackfillJobResult, Job

        return Job(
            fut,
            table_name=self._name,
            column_names=(
                unpack_context.columns if unpack_context is not None else [col_name]
            ),
            result_cls=BackfillJobResult,
        )

    def backfill(
        self,
        columns: "str | list[str]",
        *,
        udf: UDF | None = None,
        where: str | None = None,
        concurrency: int = 8,
        intra_applier_concurrency: int = 1,
        _admission_check: bool | None = None,
        _admission_strict: bool | None = None,
        refresh_status_secs: float = 2.0,
        min_checkpoint_size: int | None = None,
        max_checkpoint_size: int | None = None,
        batch_checkpoint_flush_interval_seconds: float | None = None,
        _enable_job_tracker_saves: bool = True,
        job_tracker_min_update_interval_secs: float | None = None,
        job_id: str | None = None,
        timeout: timedelta | float | None = None,
        **kwargs,
    ) -> "BackfillJobResult":
        # todo: make native interface consistent with remote interface
        """
        Backfills the specified column synchronously and returns a
        :class:`~geneva.jobs.types.BackfillJobResult` once the job
        reaches a terminal state. Use :meth:`backfill_async` for a
        non-blocking handle.

        Parameters
        ----------
        columns: str | list[str]
            Target column name to backfill. A single-element list is
            equivalent to a string. Multi-column backfill is not yet
            supported and raises ``NotImplementedError``.
        udf: UDF | None
            Optionally override the UDF used to backfill the column.
        where: str | None
            SQL expression filter to select rows to backfill. Defaults to
            '<col_name> IS NULL' to skip already-computed rows. Use where="1=1"
            to force reprocessing all rows.
        concurrency: int
            (default = 8) This controls the number of processes that tasks run
            concurrently. For max throughput, ideally this is larger than the number
            of nodes in the k8s cluster.   This is the number of Ray actor processes
            are started.
        intra_applier_concurrency: int
            (default = 1) This controls the number of threads used to execute tasks
            within a process. Multiplying this times `concurrency` roughly corresponds
            to the number of cpu's being used.
        _admission_check: bool | None
            Whether to run admission control to validate cluster resources before
            starting the job. If None, uses GENEVA_ADMISSION__CHECK env var
            (default: true). Set to False to skip the check.
            **Experimental**: Parameters starting with `_` are subject to change.
        _admission_strict: bool | None
            If True, raises ResourcesUnavailableError when resources are
            insufficient. If False, logs a warning but allows the job to proceed.
            If None, uses GENEVA_ADMISSION__STRICT env var (default: false, i.e.
            warn and proceed).
            **Experimental**: Parameters starting with `_` are subject to change.
        commit_granularity: int | None
            (default = 64) Show a partial result everytime this number of fragments
            are completed. If None, the entire result is committed at once.
        read_version: int | None
            (default = None) The version of the table to read from.  If None, the
            latest version is used.
        task_shuffle_diversity: int | None
            (default = 8) ??
        batch_size: int | None (deprecated)
            (default = 100) Legacy alias for checkpoint_size. Prefer checkpoint_size.
            If 0, the batch will be the total number of rows from a fragment.
        checkpoint_size: int | None
            The max number of rows per checkpoint.
            This influences how often progress and proof of life is presented.
            When adaptive sizing is enabled, an explicit checkpoint_size seeds the
            initial checkpoint size; otherwise the initial size defaults to
            min_checkpoint_size.
        min_checkpoint_size: int | None
            Minimum adaptive checkpoint size (lower bound).
        max_checkpoint_size: int | None
            Maximum adaptive checkpoint size (upper bound). This also caps the
            largest read batch and thus the maximum memory footprint per batch.
        batch_checkpoint_flush_interval_seconds: float | None
            Controls how frequently in-progress results are persisted as batch
            checkpoints. Larger values usually improve throughput, but if the
            job stops unexpectedly, more recently computed work may need to be
            redone. Smaller values checkpoint progress sooner, which improves
            durability and resume behavior, but can reduce throughput. Set to
            ``0`` to persist every batch as soon as it is produced.
        task_size: int | None
            Controls read-task sizing (rows per worker task). Defaults to
            ``min(table.count_rows() // num_workers // 2,
            max_fragment_size)`` when omitted, where ``max_fragment_size`` is
            the largest fragment in the pinned read snapshot.
        num_frags: int | None
            (default = None) The number of table fragments to process.  If None,
            process all fragments.
        skip_frags: int
            (default = 0) Number of fragments to skip before processing.
            Combined with ``num_frags`` this allows batching through a large
            dataset in manageable chunks. For example, ``skip_frags=100,
            num_frags=50`` processes fragments 100–149.
        _enable_job_tracker_saves: bool
            (default = False) Experimentally enable persistence of job metrics to the
            database. When disabled, metrics are tracked in-memory only.
        job_tracker_min_update_interval_secs: float | None
            (default = None) Per-job override for the *initial* seconds between
            throttled metric saves. Overrides the global
            ``GENEVA_JOB_TRACKER__MIN_UPDATE_INTERVAL_SECS``. The interval still
            grows with job runtime toward the configured ceiling, and
            terminal/forced saves always bypass the throttle. If None, the
            global config is used.
        timeout: timedelta | float | None
            Maximum wall-clock time to wait for the backfill job to complete.
        """
        col_name = _normalize_backfill_columns(columns)
        col_name = self._canonical_backfill_output_column(col_name)
        unpack_context = self._get_unpack_backfill_context(col_name)

        # update_mode is validated in backfill_async (the shared sync entry).

        # Input validation
        from geneva.runners.ray.pipeline import validate_backfill_args

        if min_checkpoint_size is not None:
            kwargs["min_checkpoint_size"] = min_checkpoint_size
        if max_checkpoint_size is not None:
            kwargs["max_checkpoint_size"] = max_checkpoint_size
        if batch_checkpoint_flush_interval_seconds is not None:
            kwargs["batch_checkpoint_flush_interval_seconds"] = (
                batch_checkpoint_flush_interval_seconds
            )

        self._normalize_backfill_batch_kwargs(kwargs)

        read_version = kwargs.get("read_version")
        if read_version is None:
            read_version = self.version
            kwargs["read_version"] = read_version

        validate_backfill_args(self, col_name, udf, read_version=read_version)

        # get cluster status
        from geneva.runners.ray.raycluster import ClusterStatus

        cs = ClusterStatus()
        timeout_secs = (
            timeout.total_seconds() if isinstance(timeout, timedelta) else timeout
        )
        deadline = None if timeout_secs is None else time.monotonic() + timeout_secs
        # Root span for the whole backfill: stays open across dispatch + the
        # blocking wait below, so the worker's geneva.job span nests inside it.
        # Mint the job_id up front so the root span carries the real id (the
        # same value threaded through dispatch/hist.launch) instead of "".
        if job_id is None:
            job_id = uuid.uuid4().hex
        _bf_ref = self.get_reference()
        _bf_span = telemetry.open_span(
            "backfill",
            {
                "job_id": job_id,
                "job_type": "backfill",
                "table": _bf_ref.table_name,
                "table_uri": _bf_ref.table_uri or "",
                "column": col_name,
            },
        )
        _bf_exc: BaseException | None = None
        try:
            # Kick off the job; request the underlying future so we can drive
            # the status loop directly. The backfill span is attached here so
            # the worker's geneva.job span nests under it.
            with (
                status_updates(cs.get_status, refresh_status_secs),
                telemetry.attach_span(_bf_span),
            ):
                fut: JobFuture = self.backfill_async(  # type: ignore[assignment]
                    col_name,
                    udf=udf,
                    where=where,
                    concurrency=concurrency,
                    intra_applier_concurrency=intra_applier_concurrency,
                    _admission_check=_admission_check,
                    _admission_strict=_admission_strict,
                    _enable_job_tracker_saves=_enable_job_tracker_saves,
                    job_tracker_min_update_interval_secs=(
                        job_tracker_min_update_interval_secs
                    ),
                    job_id=job_id,
                    _return_future=True,
                    # Sync path owns _bf_span above; async must not double-open.
                    _root_span=False,
                    **kwargs,
                )

            while True:
                wait_secs = refresh_status_secs
                if deadline is not None:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise TimeoutError(
                            f"backfill({col_name}) did not complete within "
                            f"{timeout_secs}s"
                        )
                    wait_secs = min(refresh_status_secs, remaining)
                if fut.done(timeout=wait_secs):
                    break
                # wait for the backfill to complete, updating statuses
                cs.get_status()
                fut.status()

            cs.get_status()
            fut.status()

            # Check for errors - this will raise if the job failed
            payload = fut.result()

            # updates came from an external writer, so get the latest version.
            self.checkout_latest()

            from geneva.jobs.types import DONE, BackfillJobResult, UdfResult

            udf_kwargs: dict[str, Any] = {}
            top_kwargs: dict[str, Any] = {}
            if isinstance(payload, dict):
                for key in (
                    "udf_name",
                    "udf_version",
                    "input_columns",
                    "rows_processed",
                    "rows_skipped",
                ):
                    if key in payload:
                        udf_kwargs[key] = payload[key]
                for key in (
                    "manifest_id",
                    "manifest_source",
                    "cluster_name",
                    "cluster_source",
                ):
                    if key in payload:
                        top_kwargs[key] = payload[key]
            return BackfillJobResult(
                job_id=fut.job_id,
                status=DONE,
                table_name=self._name,
                columns={
                    col: UdfResult(**udf_kwargs)
                    for col in (
                        unpack_context.columns
                        if unpack_context is not None
                        else [col_name]
                    )
                },
                **top_kwargs,
            )
        except BaseException as e:
            _bf_exc = e
            raise
        finally:
            with contextlib.suppress(Exception):
                cs.close()
            telemetry.close_span(_bf_span, _bf_exc)

    # ------------------------------------------------------------------
    # Bulk Load Column
    # ------------------------------------------------------------------

    def load_columns_async(
        self,
        source: str | list[str],
        pk: str,
        columns: list[str],
        *,
        source_format: str | None = None,
        source_storage_options: dict[str, str] | None = None,
        on_missing: str = "carry",
        concurrency: int = 8,
        task_size: int | None = None,
        checkpoint_size: int | None = None,
        min_checkpoint_size: int | None = None,
        max_checkpoint_size: int | None = None,
        checkpoint_interval_seconds: float | None = None,
        _loader_cpus: float | None = None,
        _loader_memory: int | None = None,
        commit_granularity: int | None = None,
        enable_job_tracker_saves: bool = True,
        job_id: str | None = None,
        _root_span: bool = True,
    ) -> JobFuture:
        """Load pre-computed column data from an external source by primary key.

        Joins value columns from an external dataset (Parquet, Lance, or IPC)
        into this table using a primary-key lookup. Returns a ``JobFuture``
        immediately; call ``.result()`` to block until completion.

        Examples
        --------
        Basic single-source load:

        >>> table.load_columns(
        ...     source="s3://bucket/embeddings/",
        ...     pk="document_id",
        ...     columns=["embedding"],
        ... )

        Multi-pass load when the source is too large for a single in-memory
        index. Split the source files into N chunks and run N **sequential**
        calls — each call must finish before the next starts. Carry semantics
        make later passes preserve earlier passes' values, so the end state
        is correct after all passes complete:

        >>> import pyarrow.dataset as pads
        >>> source_files = pads.dataset(
        ...     "s3://bucket/embeddings/", format="parquet"
        ... ).files
        >>> N = 4
        >>> chunk_size = len(source_files) // N
        >>> for i in range(N):
        ...     # blocks until this pass commits before starting the next
        ...     table.load_columns(
        ...         source=source_files[i * chunk_size : (i + 1) * chunk_size],
        ...         pk="document_id",
        ...         columns=["embedding"],
        ...     )

        Each pass reads only its assigned files, so the total source scan I/O
        across all passes stays at 1× full scan. Per-pass memory cost is
        ``source_size / N``.

        .. warning::
            Multi-pass loads must run **sequentially**, not concurrently. Two
            ``load_columns`` calls running at the same time against the same
            column produce an interleaved end state (last-writer-wins per
            fragment). Use a plain ``for`` loop, not ``concurrent.futures``.

        Parameters
        ----------
        source
            URI of the external dataset (local path or cloud storage), or a
            list of file paths.  Passing a list of paths enables file-level
            partitioning for the multi-pass load pattern: each call reads only
            its assigned files.  Lance sources must be a single URI.
        pk
            Primary key column name. Must exist in both source and destination.
        columns
            Value column names to load from the source dataset.
        source_format
            One of ``"parquet"``, ``"lance"``, ``"ipc"``. Auto-detected from
            the URI suffix when omitted.
        source_storage_options
            Storage options used only for opening the external source. These
            are independent from this table's storage options.
        on_missing
            How to handle destination rows with no source match:

            - ``"carry"`` (default): keep existing value (NULL for new columns).
            - ``"null"``: set to NULL.
            - ``"error"``: raise on first unmatched row.
        concurrency
            Number of Ray worker actors (default 8).
        task_size
            Rows per worker task. Auto-sized when omitted.
        checkpoint_size
            Rows per checkpoint batch. When omitted, uses the job config
            default. When ``min_checkpoint_size`` and ``max_checkpoint_size``
            are also set, this becomes the initial size for adaptive sizing.
        min_checkpoint_size
            Minimum checkpoint batch size for adaptive sizing.
        max_checkpoint_size
            Maximum checkpoint batch size for adaptive sizing.
        checkpoint_interval_seconds
            Target seconds per adaptive checkpoint batch.  The adaptive
            sizer grows or shrinks batch sizes to hit this target.
            Defaults to 60 s for bulk_load (longer than the 10 s UDF
            default because bulk_load is I/O-bound and benefits from
            larger batches that amortize GCS write overhead).
        _loader_cpus
            CPU reservation per loader actor (Ray scheduling). Defaults
            to ``None`` (Ray default of 1.0 CPU per actor).
        _loader_memory
            Memory reservation in bytes per loader actor. Defaults to
            ``None`` (no explicit reservation). Set this when loading
            wide columns (large strings, embeddings) to prevent Ray from
            oversubscribing worker nodes.
        commit_granularity
            Number of fragments per intermediate commit.
        enable_job_tracker_saves
            Enable persistence of job metrics to the database.
        job_id
            Reuse an existing job ID instead of generating a new one.
        """
        from geneva.apply.bulk_load import _VALID_ON_MISSING

        if not columns:
            raise ValueError("columns must be non-empty")
        if on_missing not in _VALID_ON_MISSING:
            raise ValueError(
                f"on_missing must be one of {_VALID_ON_MISSING!r}, got {on_missing!r}"
            )

        from geneva.runners.ray.pipeline import dispatch_run_ray_bulk_load

        # Mint the job_id up front so the root span carries the real id.
        if job_id is None:
            job_id = uuid.uuid4().hex
        # Root job-type span tied to the future (see backfill_async). The sync
        # wrapper owns its own span and passes _root_span=False to avoid a
        # duplicate; attach_span(None) / close_span(None) are then no-ops.
        _bl_ref = self.get_reference()
        _bl_span = (
            telemetry.open_span(
                "bulk_load",
                {
                    "job_id": job_id,
                    "job_type": "bulk_load",
                    "table": _bl_ref.table_name,
                    "table_uri": _bl_ref.table_uri or "",
                },
            )
            if _root_span
            else None
        )
        try:
            with telemetry.attach_span(_bl_span):
                fut = dispatch_run_ray_bulk_load(
                    self.get_reference(),
                    source_uri=source,
                    pk_column=pk,
                    value_columns=columns,
                    source_format=source_format,
                    source_storage_options=source_storage_options,
                    on_missing=on_missing,
                    concurrency=concurrency,
                    task_size=task_size,
                    checkpoint_size=checkpoint_size,
                    min_checkpoint_size=min_checkpoint_size,
                    max_checkpoint_size=max_checkpoint_size,
                    checkpoint_interval_seconds=checkpoint_interval_seconds,
                    loader_cpus=_loader_cpus,
                    loader_memory=_loader_memory,
                    commit_granularity=commit_granularity,
                    enable_job_tracker_saves=enable_job_tracker_saves,
                    job_id=job_id,
                )
        except BaseException as e:
            telemetry.close_span(_bl_span, e)
            raise
        if _bl_span is not None:
            fut._otel_span = _bl_span
        return fut

    def load_columns(
        self,
        source: str | list[str],
        pk: str,
        columns: list[str],
        *,
        source_format: str | None = None,
        source_storage_options: dict[str, str] | None = None,
        on_missing: str = "carry",
        concurrency: int = 8,
        task_size: int | None = None,
        checkpoint_size: int | None = None,
        min_checkpoint_size: int | None = None,
        max_checkpoint_size: int | None = None,
        checkpoint_interval_seconds: float | None = None,
        _loader_cpus: float | None = None,
        _loader_memory: int | None = None,
        commit_granularity: int | None = None,
        refresh_status_secs: float = 2.0,
        enable_job_tracker_saves: bool = True,
        job_id: str | None = None,
    ) -> str:
        """Load pre-computed column data from an external source by primary key.

        Synchronous wrapper around :meth:`load_columns_async`. Returns the
        job ID string on success.

        See :meth:`load_columns_async` for parameter documentation.
        """
        from geneva.runners.ray.raycluster import ClusterStatus

        cs = ClusterStatus()
        # Mint the job_id up front so the root span carries the real id.
        if job_id is None:
            job_id = uuid.uuid4().hex
        _bl_ref = self.get_reference()
        _bl_span = telemetry.open_span(
            "bulk_load",
            {
                "job_id": job_id,
                "job_type": "bulk_load",
                "table": _bl_ref.table_name,
                "table_uri": _bl_ref.table_uri or "",
            },
        )
        _bl_exc: BaseException | None = None
        try:
            # Attach the bulk_load span so the worker's geneva.job nests under it.
            with (
                status_updates(cs.get_status, refresh_status_secs),
                telemetry.attach_span(_bl_span),
            ):
                fut = self.load_columns_async(
                    source,
                    pk,
                    columns,
                    source_format=source_format,
                    source_storage_options=source_storage_options,
                    on_missing=on_missing,
                    concurrency=concurrency,
                    task_size=task_size,
                    checkpoint_size=checkpoint_size,
                    min_checkpoint_size=min_checkpoint_size,
                    max_checkpoint_size=max_checkpoint_size,
                    checkpoint_interval_seconds=checkpoint_interval_seconds,
                    _loader_cpus=_loader_cpus,
                    _loader_memory=_loader_memory,
                    commit_granularity=commit_granularity,
                    enable_job_tracker_saves=enable_job_tracker_saves,
                    job_id=job_id,
                    # Sync path owns _bl_span above; async must not double-open.
                    _root_span=False,
                )

            while not fut.done(timeout=refresh_status_secs):
                cs.get_status()
                fut.status()

            cs.get_status()
            fut.status()
            fut.result()

            self._ltbl.checkout_latest()
            return fut.job_id
        except BaseException as e:
            _bl_exc = e
            raise
        finally:
            with contextlib.suppress(Exception):
                cs.close()
            telemetry.close_span(_bl_span, _bl_exc)

    def _resolve_backfill_context(
        self,
        col_name: str,
        *,
        udf: UDF | None,
        where: str | None,
        read_version: int,
    ) -> tuple[UDF | None, str | None, bool, bool]:
        """Shared pre-dispatch logic for backfill and plan_backfill.

        Validates args, resolves the UDF, detects mismatches, and computes the
        effective WHERE filter.

        Returns ``(resolved_udf, resolved_where, udf_mismatch, srcfiles_mismatch)``.
        """
        from geneva.apply.utils import (
            detect_backfill_mismatches,
            resolve_backfill_where,
        )
        from geneva.runners.ray.pipeline import (
            fetch_udf,
            validate_backfill_args,
        )

        validate_backfill_args(self, col_name, udf, read_version=read_version)

        current_udf = udf
        if current_udf is None:
            try:
                udf_spec = fetch_udf(self, col_name)
                current_udf = self._conn._packager.unmarshal(udf_spec)
            except Exception as e:
                _LOG.debug("Could not fetch UDF: %s", e)
                current_udf = None

        col_field = self._ltbl.schema.field(col_name)
        unpack_context = self._get_unpack_backfill_context(col_name)
        if unpack_context is not None and udf is not None and not udf.is_multi_output:
            raise ValueError(
                f"Column {col_name!r} is part of a multi-column UDF group. "
                "backfill(udf=...) overrides for sibling columns must also be "
                "Columns[T] multi-output UDFs."
            )
        checkpoint_col_name = (
            unpack_context.checkpoint_column if unpack_context is not None else col_name
        )
        # An explicit WHERE filter is used verbatim: mismatch detection only ever
        # expands a None filter to all rows (see resolve_backfill_where), and the
        # flags are otherwise discarded by the execution path. So skip the
        # checkpoint scan it performs — which lists the entire checkpoint root and
        # reads per-fragment checkpoints, prohibitively slow on large tables
        # (GEN-606). When where is None the scan is still needed to catch
        # UDF-version / input-data changes and force a full reprocess.
        if where is not None:
            udf_mismatch, srcfiles_mismatch = False, False
            # Detection is skipped, so emit a cheap unconditional advisory in
            # its place: an explicit filter on a UDF-backed column may leave rows
            # computed under a previous UDF version or changed input data
            # unprocessed.
            if current_udf is not None and not _is_intentional_full_reprocess_where(
                where
            ):
                _LOG.warning(
                    "Column %s has an explicit where filter provided. Rows "
                    "already computed with a previous UDF version or changed "
                    "input data will not be reprocessed. Use where='1=1' to "
                    "force reprocessing all rows.",
                    col_name,
                )
        else:
            udf_mismatch, srcfiles_mismatch = detect_backfill_mismatches(
                self, checkpoint_col_name, current_udf, read_version
            )
        where = resolve_backfill_where(
            col_name,
            col_field,
            where,
            udf_mismatch,
            srcfiles_mismatch,
            default_where=(
                unpack_context.default_where if unpack_context is not None else None
            ),
        )
        return current_udf, where, udf_mismatch, srcfiles_mismatch

    def _get_unpack_backfill_context(
        self, col_name: str
    ) -> _UnpackBackfillContext | None:
        try:
            field = self._ltbl.schema.field(col_name)
        except KeyError:
            return None

        metadata = field.metadata or {}
        if metadata.get(_UNPACK_META_FLAG.encode("utf-8")) != b"true":
            return None

        raw_fields = metadata.get(_UNPACK_META_FIELDS.encode("utf-8"))
        if raw_fields is None:
            raise ValueError(
                f"Unpacked computed column {col_name!r} is missing "
                f"{_UNPACK_META_FIELDS} metadata"
            )

        entries = json.loads(raw_fields.decode("utf-8"))
        unpacked_fields: list[UnpackedUDFField] = []
        missing: list[str] = []
        for entry in entries:
            output_column = entry["column"]
            try:
                output_field = self._ltbl.schema.field(output_column)
            except KeyError:
                missing.append(output_column)
                continue
            unpacked_fields.append(
                UnpackedUDFField(
                    struct_field_name=entry["field"],
                    output_column=output_column,
                    field=_without_virtual_column_metadata(output_field),
                )
            )

        if missing:
            raise ValueError(
                f"Unpacked computed column {col_name!r} references missing sibling "
                f"columns {missing}. Drop the remaining sibling columns and add "
                "the Columns[T] UDF again."
            )
        return _UnpackBackfillContext(tuple(unpacked_fields))

    def _unpack_group_columns_for_column(self, col_name: str) -> list[str] | None:
        try:
            field = self._ltbl.schema.field(col_name)
        except KeyError:
            return None

        metadata = field.metadata or {}
        if metadata.get(_UNPACK_META_FLAG.encode("utf-8")) != b"true":
            return None

        raw_fields = metadata.get(_UNPACK_META_FIELDS.encode("utf-8"))
        if raw_fields is None:
            raise ValueError(
                f"Unpacked computed column {col_name!r} is missing "
                f"{_UNPACK_META_FIELDS} metadata"
            )

        return [entry["column"] for entry in json.loads(raw_fields.decode("utf-8"))]

    def plan_backfill(
        self,
        col_name: str,
        *,
        udf: UDF | None = None,
        where: str | None = None,
        read_version: int | None = None,
        num_frags: int | None = None,
        skip_frags: int = 0,
        task_size: int | None = None,
    ) -> BackfillPlan:
        """Plan a backfill without dispatching: count tasks and rows.

        Returns a ``BackfillPlan`` describing what work a ``backfill()`` call
        would perform.  Does not require a Ray cluster.

        .. warning::
            Evaluates ``where`` per fragment via ``count_rows(filter=...)``
            on the driver — serial, can take many minutes for selective
            predicates over wide columns. ``backfill()`` itself avoids
            this cost.
        """
        from geneva.apply import _plan_read

        if read_version is None:
            read_version = self.version

        col_name = self._canonical_backfill_output_column(col_name)
        unpack_context = self._get_unpack_backfill_context(col_name)
        current_udf, where, udf_mismatch, srcfiles_mismatch = (
            self._resolve_backfill_context(
                col_name, udf=udf, where=where, read_version=read_version
            )
        )

        if where:
            _LOG.info(
                "plan_backfill evaluates `%s` per fragment via count_rows; "
                "this may be slow for selective predicates over large or "
                "wide columns. backfill() itself avoids this cost.",
                where,
            )

        table_ref = self.get_reference()

        plan_kwargs: dict = {}
        if num_frags is not None:
            plan_kwargs["num_frags"] = num_frags
        if skip_frags:
            plan_kwargs["skip_frags"] = skip_frags
        if task_size is not None:
            plan_kwargs["task_size"] = task_size

        plan_result = _plan_read(
            self.uri,
            table_ref,
            unpack_context.columns if unpack_context is not None else [col_name],
            read_version=read_version,
            where=where,
            **plan_kwargs,
        )

        total_tasks = plan_result.total_tasks
        total_rows_pending = plan_result.total_rows

        # Get total table stats
        from geneva.db import open_lance_dataset

        dataset = open_lance_dataset(
            self.uri,
            namespace_config=table_ref.namespace_config,
            table_id=table_ref.table_id,
            storage_options=table_ref.storage_options,
        )
        if read_version is not None:
            dataset = dataset.checkout_version(read_version)

        fragments = list(dataset.get_fragments())
        total_fragments = len(fragments)
        total_rows = sum(f.count_rows() for f in fragments)

        return BackfillPlan(
            table_name=self.name,
            version=read_version,
            has_work=total_tasks > 0 or udf_mismatch,
            total_tasks=total_tasks,
            total_rows_pending=total_rows_pending,
            skipped_fragments=plan_result.skipped_stats["fragments"],
            skipped_rows=plan_result.skipped_stats["rows"],
            total_fragments=total_fragments,
            total_rows=total_rows,
            column_name=col_name,
            where=where,
            udf_mismatch=udf_mismatch,
            srcfiles_mismatch=srcfiles_mismatch,
        )

    @staticmethod
    def _normalize_backfill_batch_kwargs(kwargs: dict[str, Any]) -> None:
        """Normalize batch-size kwargs for backfill calls."""

        checkpoint_size = kwargs.pop("checkpoint_size", None)
        batch_size = kwargs.pop("batch_size", None)
        task_size = kwargs.pop("task_size", None)

        resolved = resolve_batch_size(
            batch_size=batch_size,
            checkpoint_size=checkpoint_size,
        )

        if task_size is not None:
            kwargs["task_size"] = task_size

        kwargs["checkpoint_size"] = resolved

    def alter_columns(self, *alterations: dict[str, Any], **kwargs) -> None:
        """
        Alter columns in the table.  This can change the computed columns' udf

        Parameters
        ----------
        alterations:  Iterable[dict[str, Any]]
            This is a list of alterations to apply to the table.

        Examples
        --------

            table.alter_columns(
                { "path": "col1", "udf": col1_udf_v2, },
                { "path": "col2", "udf": col2_udf})

        """
        # Remote (db://) path: route through namespace API.
        if self._conn.use_remote_dispatch():
            return self._alter_columns_remote(*alterations)

        basic_column_alterations = []
        for alter in alterations:
            if "path" not in alter:
                raise ValueError("path is required to alter computed column's udf")

            col_name = alter["path"]
            group_columns = self._unpack_group_columns_for_column(col_name)
            if group_columns is not None:
                raise ValueError(
                    f"Column {col_name!r} is part of a multi-column UDF group. "
                    "alter_columns() is not supported for individual sibling "
                    "columns; drop all sibling columns and add the replacement "
                    f"columns again. Sibling columns: {group_columns}."
                )

            # Reject ambiguous input early: when both the deprecated alias
            # and the new key are present, native and remote paths used to
            # disagree on which one wins. Force the caller to pick one.
            if "virtual_column" in alter and "udf" in alter:
                raise ValueError(
                    "alter_columns: pass either 'udf' (preferred) or "
                    "'virtual_column' (deprecated), not both"
                )

            if "virtual_column" in alter:  # deprecated
                udf = alter.get("virtual_column")
                if not isinstance(udf, UDF):
                    raise ValueError("virtual_column must be a UDF")
                _LOG.warning(
                    "alter_columns 'virtual_column' is deprecated, use 'udf' instead."
                )
            elif "udf" in alter:
                udf = alter.get("udf")
                if not isinstance(udf, UDF):
                    raise ValueError("udf must be a UDF")
            else:
                basic_column_alterations.append(alter)
                continue
            if udf.is_multi_output:
                raise ValueError(
                    "Replacing columns with a Columns[T] multi-column UDF via "
                    "alter_columns() is not supported; drop all sibling columns "
                    "and add the Columns[T] UDF again."
                )

            input_cols = alter.get("input_columns", None)
            if input_cols is None:
                input_cols = udf.input_columns

            self._configure_computed_column(col_name, udf, input_cols)

        if len(basic_column_alterations) > 0:
            self._ltbl.alter_columns(*basic_column_alterations)

    def _upload_udf(
        self,
        udf_payload: bytes,
        udf_location: str,
    ) -> None:
        """
        Upload UDF payload to the dataset storage using Lance file sessions.

        Uses Lance's native object_store layer which handles credential
        management for all storage backends (S3, GCS, Azure, local).

        Parameters
        ----------
        udf_payload : bytes
            The serialized UDF package to upload
        udf_location : str
            Relative path within the dataset (e.g., "_udfs/checksum")
        """
        import os
        import tempfile

        ds = self.to_lance()  # to_lance: fresh — UDF upload writes via new_file_session
        session = ds.new_file_session()

        with tempfile.NamedTemporaryFile(
            mode="wb", delete=False, suffix=".udf"
        ) as tmp_file:
            tmp_file.write(udf_payload)
            tmp_path = tmp_file.name

        try:
            session.upload_file(tmp_path, udf_location)
            _LOG.debug(f"Uploaded UDF to {udf_location} ({len(udf_payload)} bytes)")
        except Exception as e:
            raise RuntimeError(f"Failed to upload UDF at {udf_location}: {e}") from e
        finally:
            os.unlink(tmp_path)

    def _configure_computed_column(
        self,
        col_name: str,
        udf: UDF,
        input_cols: list[str] | None,
    ) -> None:
        """
        Configure a column to be a computed column for the given UDF.

        This procedure includes:
        - Packaging the UDF
        - Uploading the UDF to the dataset
        - Updating the field metadata to include the UDF information

        Note that the column should already exist on the table.
        """
        # record batch udf's don't specify inputs
        if (
            udf.arg_type != UDFArgType.RECORD_BATCH
            and udf.input_columns
            and col_name in udf.input_columns
        ):
            raise ValueError(
                f"UDF output column {col_name} is not allowed to be in"
                f" input {udf.input_columns}"
            )

        udf_spec = self._conn._packager.marshal(udf, table_ref=self.get_reference())
        canonical_input_cols = canonical_field_paths(self._ltbl.schema, input_cols)

        # upload the UDF to the dataset URL
        if not isinstance(self._ltbl, LanceLocalTable):
            raise TypeError(
                "adding udf column is currently only supported for local tables"
            )

        # upload the packaged UDF to some location inside the dataset:
        checksum = hashlib.sha256(udf_spec.udf_payload).hexdigest()
        udf_location = f"_udfs/{checksum}"

        self._upload_udf(udf_spec.udf_payload, udf_location)

        # TODO rename this from virtual_column to computed column
        field_metadata = udf.field_metadata | {
            "virtual_column": "true",
            "virtual_column.udf_backend": udf_spec.backend,
            "virtual_column.udf_name": udf_spec.name,
            "virtual_column.udf": "_udfs/" + checksum,
            "virtual_column.udf_inputs": json.dumps(canonical_input_cols),
            "virtual_column.platform.system": platform.system(),
            "virtual_column.platform.arch": platform.machine(),
            "virtual_column.platform.python_version": platform.python_version(),
            "virtual_column.auto_backfill": "true" if udf.auto_backfill else "false",
        }

        # When the UDF carries an explicit manifest from @udf(manifest=...),
        # snapshot the manifest JSON inline in field metadata so backfill
        # reads it without consulting any other source. Columns without an
        # explicit manifest preserve today's metadata shape exactly.
        # ``virtual_column.manifest_checksum`` is the same value as
        # ``GenevaManifest.checksum`` — same algorithm, same field set
        # — so column-metadata identity matches registry-row identity.
        if udf.manifest is not None:
            field_metadata["virtual_column.manifest"] = udf.manifest.to_json()
            field_metadata["virtual_column.manifest_checksum"] = (
                udf.manifest.compute_checksum()
            )

        # Add the column metadata:
        get_field_metadata_writer().update(
            self._ltbl,
            {"path": col_name, "metadata": field_metadata, "replace": True},
        )

    def create_index(
        self,
        metric: str = "L2",
        num_partitions: int | None = None,
        num_sub_vectors: int | None = None,
        vector_column_name: str = VECTOR_COLUMN_NAME,
        replace: bool = True,
        accelerator=None,
        index_cache_size=None,
        *,
        index_type: Literal[
            "IVF_FLAT",
            "IVF_PQ",
            "IVF_HNSW_SQ",
            "IVF_HNSW_PQ",
        ] = "IVF_PQ",
        num_bits: int = 8,
        max_iterations: int = 50,
        sample_rate: int = 256,
        m: int = 20,
        ef_construction: int = 300,
    ) -> None:
        """Create Vector Index"""
        self._ltbl.create_index(
            cast('Literal["l2", "cosine", "dot", "hamming"]', metric),
            num_partitions or 256,
            num_sub_vectors or 96,
            vector_column_name,
            replace,
            accelerator,
            index_cache_size,
            index_type=index_type,
            num_bits=num_bits,
            max_iterations=max_iterations,
            sample_rate=sample_rate,
            m=m,
            ef_construction=ef_construction,
        )

    @override
    def create_fts_index(
        self,
        field_names: str | list[str],
        *,
        ordering_field_names: str | list[str] | None = None,
        replace: bool = False,
        writer_heap_size: int | None = 1024 * 1024 * 1024,
        tokenizer_name: str | None = None,
        with_position: bool = True,
        base_tokenizer: Literal["simple", "raw", "whitespace"] = "simple",
        language: str = "English",
        max_token_length: int | None = 40,
        lower_case: bool = True,
        stem: bool = False,
        remove_stop_words: bool = False,
        ascii_folding: bool = False,
        **_kwargs,
    ) -> None:
        self._ltbl.create_fts_index(
            field_names,
            ordering_field_names=ordering_field_names,
            replace=replace,
            writer_heap_size=writer_heap_size,
            tokenizer_name=tokenizer_name,
            with_position=with_position,
            base_tokenizer=base_tokenizer,
            language=language,
            max_token_length=max_token_length,
            lower_case=lower_case,
            stem=stem,
            remove_stop_words=remove_stop_words,
            ascii_folding=ascii_folding,
            use_tantivy=False,
        )

    @override
    def create_scalar_index(
        self,
        column: str,
        *,
        replace: bool = True,
        index_type: Literal["BTREE", "BITMAP", "LABEL_LIST"] = "BTREE",
    ) -> None:
        self._ltbl.create_scalar_index(
            column,
            replace=replace,
            index_type=index_type,
        )

    @override
    def _do_merge(
        self,
        merge: LanceMergeInsertBuilder,
        new_data: DATA,
        on_bad_vectors: OnBadVectorsType,
        fill_value: float,
    ) -> MergeResult:
        return self._ltbl._do_merge(merge, new_data, on_bad_vectors, fill_value)

    @override
    def _execute_query(
        self,
        query: LanceQuery,
        batch_size: int | None = None,
    ) -> pa.RecordBatchReader:
        return self._ltbl._execute_query(query, batch_size=batch_size)

    def list_versions(self) -> list[dict[str, Any]]:
        return self._ltbl.list_versions()

    @override
    def cleanup_old_versions(
        self,
        older_than: timedelta | None = None,
        *,
        delete_unverified=False,
    ) -> Any:  # lance.CleanupStats not available in type stubs
        return self._ltbl.cleanup_old_versions(
            older_than,
            delete_unverified=delete_unverified,
        )

    def to_batches(self, batch_size: int | None = None) -> Iterator[pa.RecordBatch]:
        from .query import Query

        if isinstance(self._ltbl, Query):
            return self._ltbl.to_batches(batch_size)  # type: ignore[attr-defined]
        from geneva.query import open_read_dataset

        return open_read_dataset(self).to_batches(batch_size=batch_size)  # type: ignore[arg-type]

    """This is the signature for the standard LanceDB table.search call"""

    def search(  # type: ignore[override]
        self,
        query: list | pa.Array | pa.ChunkedArray | np.ndarray | None = None,
        vector_column_name: str | None = None,
        query_type: Literal["vector", "fts", "hybrid", "auto"] = "auto",
        ordering_field_name: str | None = None,
        fts_columns: str | list[str] | None = None,
    ) -> GenevaQueryBuilder | LanceQueryBuilder:
        if query is None:
            return GenevaQueryBuilder(self)
        else:
            return self._ltbl.search(
                query, vector_column_name, query_type, ordering_field_name, fts_columns
            )

    @override
    def drop_columns(self, columns: Iterable[str]) -> None:
        columns_list = [columns] if isinstance(columns, str) else list(columns)
        drop_set = set(columns_list)

        for col_name in columns_list:
            group_columns = self._unpack_group_columns_for_column(col_name)
            if group_columns is None:
                continue

            missing_from_drop = sorted(set(group_columns) - drop_set)
            if missing_from_drop:
                raise ValueError(
                    f"Column {col_name!r} is part of a multi-column UDF group. "
                    "drop_columns() must drop all sibling columns in the same "
                    "call before any replacement column can be added. "
                    f"Sibling columns: {group_columns}."
                )

        self._ltbl.drop_columns(columns_list)

    @override
    def update_field_metadata(
        self, *updates: dict[str, Any]
    ) -> UpdateFieldMetadataResult:
        """Update per-field (column) metadata on the table.

        Delegates to the underlying Lance table, which handles both native
        (object-storage) and remote (``db://``) backends.
        """
        return get_field_metadata_writer().update(self._ltbl, *updates)

    @override
    def to_arrow(self) -> pa.Table:
        return self._ltbl.to_arrow()

    @override
    def to_pandas(self, blob_mode: BlobMode = "lazy", **kwargs: Any) -> "pd.DataFrame":
        return self._ltbl.to_pandas(blob_mode=blob_mode, **kwargs)

    @override
    def count_rows(self, filter: str | None = None) -> int:
        return self._ltbl.count_rows(filter)

    @override
    def update(
        self,
        where: str | None = None,
        values: dict | None = None,
        *,
        values_sql: dict[str, str] | None = None,
    ) -> None:
        get_table_writer().update(self._ltbl, where, values, values_sql=values_sql)

    @override
    def delete(self, where: str) -> None:
        get_table_writer().delete(self._ltbl, where)

    @override
    def list_indices(self) -> Iterable[IndexConfig]:
        return self._ltbl.list_indices()

    def tokenize(
        self,
        query: str,
        *,
        column: str | None = None,
        index_name: str | None = None,
    ) -> Iterable[Any]:
        return self._ltbl.tokenize(  # type: ignore[attr-defined]
            query,
            column=column,
            index_name=index_name,
        )

    @override
    def index_stats(self, index_name: str) -> IndexStatistics | None:
        return self._ltbl.index_stats(index_name)

    @override
    def optimize(
        self,
        *,
        cleanup_older_than: timedelta | None = None,
        delete_unverified: bool = False,
    ) -> None:
        return self._ltbl.optimize(
            cleanup_older_than=cleanup_older_than,
            delete_unverified=delete_unverified,
        )

    @override
    def compact_files(self) -> None:
        self._ltbl.compact_files()

    def cleanup_checkpoints(
        self,
        *,
        _clean_batches: bool = True,
        _clean_orphan_fragments: bool = True,
        _clean_udtf_batches: bool = True,
    ) -> dict[str, int]:
        """Sweep expired checkpoints from this table's checkpoint store."""
        import re

        empty_counts = {
            "batch_deleted": 0,
            "orphan_frag_deleted": 0,
            "udtf_batch_deleted": 0,
        }

        try:
            store = self.get_reference().open_checkpoint_store()
        except Exception:
            _LOG.warning(
                "cleanup_checkpoints: failed to open checkpoint store",
                exc_info=True,
            )
            return empty_counts

        # Multi-base datasets keep per-fragment checkpoints in each
        # fragment's storage base; sweep those roots too. Includes bases
        # with no current fragment so orphaned checkpoints are reachable.
        try:
            from geneva.utils.multi_base import (
                FragmentBasePlacement,
                maybe_wrap_checkpoint_store_for_bases,
            )

            # to_lance: fresh — the sweep needs the live base set
            placement = FragmentBasePlacement.from_dataset(self.to_lance())
            store = maybe_wrap_checkpoint_store_for_bases(
                store, placement, include_unused_bases=True
            )
        except Exception:
            _LOG.debug(
                "cleanup_checkpoints: failed to resolve multi-base roots",
                exc_info=True,
            )

        current_frag_ids: set[int] = set()
        if _clean_orphan_fragments:
            try:
                # to_lance: fresh — orphan cleanup needs the live fragment set
                ds = self.to_lance()
                current_frag_ids = {f.fragment_id for f in ds.get_fragments()}
            except Exception:
                _LOG.warning(
                    "cleanup_checkpoints: failed to list current fragments",
                    exc_info=True,
                )
                return empty_counts

        all_keys = list(store.list_keys())
        udf_pattern = re.compile(r"^(udf-.+?_frag-(\d+))(_range-.+)?$")
        udtf_batch_pattern = re.compile(r"^(udtf_.+?)_batch-\d+$")

        udf_dedupe_keys: set[str] = set()
        udf_batch_to_dedupe: dict[str, str] = {}
        udf_frag_id_by_key: dict[str, int] = {}
        udtf_batch_to_partition: dict[str, str] = {}
        udtf_partition_complete: set[str] = set()

        for key in all_keys:
            udf_match = udf_pattern.match(key)
            if udf_match:
                dedupe_key = udf_match.group(1)
                frag_id = int(udf_match.group(2))
                range_suffix = udf_match.group(3)
                udf_frag_id_by_key[key] = frag_id
                if range_suffix is not None:
                    udf_batch_to_dedupe[key] = dedupe_key
                else:
                    udf_dedupe_keys.add(key)
                continue
            udtf_match = udtf_batch_pattern.match(key)
            if udtf_match:
                udtf_batch_to_partition[key] = udtf_match.group(1)
                continue
            if key.endswith("_fragment"):
                udtf_partition_complete.add(key[: -len("_fragment")])

        def _safe_delete(key: str) -> bool:
            try:
                store.purge(key)
                return True
            except KeyError:
                return False
            except Exception:
                _LOG.debug(
                    "cleanup_checkpoints: failed to purge %s", key, exc_info=True
                )
                return False

        deleted_keys: set[str] = set()
        batch_deleted = 0
        if _clean_batches:
            for batch_key, dedupe_key in udf_batch_to_dedupe.items():
                if dedupe_key in udf_dedupe_keys and _safe_delete(batch_key):
                    batch_deleted += 1
                    deleted_keys.add(batch_key)

        orphan_frag_deleted = 0
        if _clean_orphan_fragments:
            for key, frag_id in udf_frag_id_by_key.items():
                if key in deleted_keys:
                    continue
                if frag_id not in current_frag_ids and _safe_delete(key):
                    orphan_frag_deleted += 1
                    deleted_keys.add(key)

        udtf_batch_deleted = 0
        if _clean_udtf_batches:
            for batch_key, partition_prefix in udtf_batch_to_partition.items():
                if partition_prefix in udtf_partition_complete and _safe_delete(
                    batch_key
                ):
                    udtf_batch_deleted += 1

        return {
            "batch_deleted": batch_deleted,
            "orphan_frag_deleted": orphan_frag_deleted,
            "udtf_batch_deleted": udtf_batch_deleted,
        }

    @override
    def restore(self, *args, **kwargs) -> None:
        self._ltbl.restore(*args, **kwargs)

    # TODO: This annotation sucks
    # NOTE: When using blob columns with stable row IDs enabled (e.g., for
    # materialized views), pylance >= 1.1.0b2 is required. Earlier versions
    # have a bug where take_blobs fails on fragments created via DataReplacement.
    def take_blobs(self, indices: list[int] | pa.Array, column: str):  # noqa: ANN201
        from geneva.query import open_read_dataset

        return open_read_dataset(self).take_blobs(blob_column=column, indices=indices)

    def to_lance(self) -> lance.LanceDataset:
        # to_lance: fresh — this IS the primitive snapshot open Table.to_lance wraps
        return self._ltbl.to_lance()  # type: ignore[attr-defined]

    def uses_v2_manifest_paths(self) -> bool:
        return self._ltbl.uses_v2_manifest_paths()

    def migrate_v2_manifest_paths(self) -> None:
        return self._ltbl.migrate_v2_manifest_paths()

    def _analyze_plan(self, query: LanceQuery) -> str:
        return self._ltbl._analyze_plan(query)

    def _explain_plan(self, query: LanceQuery, verbose: bool | None = False) -> str:
        return self._ltbl._explain_plan(query, verbose=verbose)

    def stats(self) -> TableStatistics:
        return self._ltbl.stats()

    @property
    def tags(self) -> Tags:
        return self._ltbl.tags

    def take_offsets(self, offsets: list[int]) -> LanceTakeQueryBuilder:
        return self._ltbl.take_offsets(offsets)

    def take_row_ids(self, row_ids: list[int]) -> LanceTakeQueryBuilder:
        return self._ltbl.take_row_ids(row_ids)

    def blob_columns(self) -> list[str]:
        return self._ltbl.blob_columns()  # type: ignore[attr-defined]

    def fetch_blobs(
        self, column: str, row_ids: list[int] | pa.Table
    ) -> pa.LargeBinaryArray:
        return self._ltbl.fetch_blobs(column, row_ids)  # type: ignore[attr-defined]

    def fetch_blob_ranges(
        self,
        column: str,
        requests: Sequence[tuple[int, int, int]],
    ) -> pa.LargeBinaryArray:
        return self._ltbl.fetch_blob_ranges(  # type: ignore[attr-defined]
            column, requests
        )

    def fetch_blob_files(
        self, column: str, row_ids: list[int] | pa.Table
    ) -> list[Any | None]:
        return self._ltbl.fetch_blob_files(  # type: ignore[attr-defined]
            column, row_ids
        )

    def refresh_column(self, column: str) -> Never:
        """Fill the rows of a Lance computed column that hold no value yet.

        Not supported: Geneva does not declare Lance computed columns, so a
        Geneva table never has one to fill. Unrelated to
        [`refresh`][geneva.table.Table.refresh], which rebuilds a materialized
        view, and to [`backfill`][geneva.table.Table.backfill], which runs
        Geneva UDF columns.
        """
        raise _computed_column_unsupported("refresh_column")

    def refresh_column_async(self, column: str) -> Never:
        """Start a Lance computed column refresh and return its job handle.

        Not supported, for the same reason as
        [`refresh_column`][geneva.table.Table.refresh_column].
        """
        raise _computed_column_unsupported("refresh_column_async")

    def get_errors(
        self,
        job_id: str | None = None,
        column_name: str | None = None,
        error_type: str | None = None,
    ) -> list[Any]:
        """Get error records for this table.

        Parameters
        ----------
        job_id : str, optional
            Filter errors by job ID
        column_name : str, optional
            Filter errors by column name
        error_type : str, optional
            Filter errors by exception type

        Returns
        -------
        list[ErrorRecord]
            List of error records matching the filters

        Examples
        --------
        >>> # Get all errors for this table
        >>> errors = table.get_errors()
        >>>
        >>> # Get errors for a specific job
        >>> errors = table.get_errors(job_id="abc123")
        >>>
        >>> # Get errors for a specific column
        >>> errors = table.get_errors(column_name="my_column")
        """
        from geneva.debug.error_store import ErrorStore

        error_store = ErrorStore(self._conn)
        return error_store.get_errors(
            job_id=job_id,
            table_name=self._name,
            column_name=column_name,
            error_type=error_type,
        )

    def get_failed_row_addresses(self, job_id: str, column_name: str) -> list[int]:
        """Get row addresses for all failed rows in a job.

        Parameters
        ----------
        job_id : str
            Job ID to query
        column_name : str
            Column name to filter by

        Returns
        -------
        list[int]
            List of row addresses that failed

        Examples
        --------

            # Get failed row addresses
            failed_rows = table.get_failed_row_addresses(
                job_id="abc123", column_name="my_col"
            )

            # Retry processing only failed rows
            row_ids = ','.join(map(str, failed_rows))
            table.backfill("my_col", where=f"_rowaddr IN ({row_ids})")
        """
        from geneva.debug.error_store import ErrorStore

        error_store = ErrorStore(self._conn)
        return error_store.get_failed_row_addresses(
            job_id=job_id, column_name=column_name
        )

    @override
    def _output_schema(self, query: LanceQuery) -> pa.Schema:
        return self._ltbl._output_schema(query)

    # ------------------------------------------------------------------
    # Remote (db://) routing helpers (namespace API)
    # ------------------------------------------------------------------

    def _min_read_version_namespace_client(self) -> "LanceNamespace":
        """Namespace client that pins min read version to this client's version.

        The server-side handler validates the target column against a *versionless*
        server-side open. Under weak read consistency that open can be served a
        cached snapshot from before the column was added, which surfaces as
        ``Column '<name>' not found``. Attaching ``x-lancedb-min-read-version``
        asserts a monotonic read floor equal to the version this client sees, so
        the query node refreshes its cache to at least that version and the
        just-added column is visible — no server-side change required.
        """
        conn = self._conn
        impl = conn.namespace_client_impl
        props = conn.namespace_client_properties
        if impl != "rest" or props is None:
            return conn.namespace_client()
        from lance_namespace import connect as namespace_connect

        props = dict(props)
        props["header.x-lancedb-min-read-version"] = str(self.version)
        props = with_geneva_user_agent(impl, props)
        return namespace_connect(impl, props)

    def _backfill_async_v2(
        self,
        col_name: str,
        *,
        where: str | None = None,
        concurrency: int | None = None,
        intra_applier_concurrency: int | None = None,
        min_checkpoint_size: int | None = None,
        max_checkpoint_size: int | None = None,
        batch_checkpoint_flush_interval_seconds: float | None = None,
        cluster: str | None = None,
        manifest: str | None = None,
        _return_future: bool = False,
        **kwargs: Any,
    ) -> "JobFuture | Job":
        """Dispatch backfill via the namespace API (remote ``db://`` path)."""
        from lance_namespace import AlterTableBackfillColumnsRequest

        from geneva.jobs.remote import RemoteJob
        from geneva.jobs.types import BackfillJobResult, Job
        from geneva.remote_v2 import RemoteJobFuture

        ns = self._min_read_version_namespace_client()
        output_column = self._canonical_backfill_output_column(col_name)
        explicit_skip_checkpoint_index_scan = kwargs.get("_skip_checkpoint_index_scan")
        if explicit_skip_checkpoint_index_scan is None:
            skip_checkpoint_index_scan = _is_intentional_full_reprocess_where(where)
        else:
            skip_checkpoint_index_scan = bool(explicit_skip_checkpoint_index_scan)

        request_kwargs = {
            "id": self._table_id,
            "column": output_column,
            "where": where,
            "concurrency": concurrency,
            "intra_applier_concurrency": intra_applier_concurrency,
            "min_checkpoint_size": min_checkpoint_size,
            "max_checkpoint_size": max_checkpoint_size,
            "batch_checkpoint_flush_interval_seconds": (
                batch_checkpoint_flush_interval_seconds
            ),
            "read_version": (
                kwargs.get("read_version")
                if kwargs.get("read_version") is not None
                else self.version
            ),
            "task_size": kwargs.get("task_size"),
            "num_frags": kwargs.get("num_frags"),
            "checkpoint_size": kwargs.get("checkpoint_size"),
            "commit_granularity": kwargs.get("commit_granularity"),
            "cluster": cluster,
            "manifest": manifest,
        }
        if skip_checkpoint_index_scan:
            if _request_model_supports_field(
                AlterTableBackfillColumnsRequest, "_skip_checkpoint_index_scan"
            ):
                request_kwargs["_skip_checkpoint_index_scan"] = True
            elif explicit_skip_checkpoint_index_scan:
                raise NotImplementedError(
                    "Remote backfill does not yet support "
                    "_skip_checkpoint_index_scan with this lance_namespace client."
                )

        request = build_remote_request(
            AlterTableBackfillColumnsRequest, request_kwargs, kwargs, op="backfill"
        )
        response = ns.alter_table_backfill_columns(request)

        output_columns = [output_column]
        input_columns = self._virtual_column_input_paths(output_columns[0])
        self._conn._history.launch(
            self._name,
            output_columns[0],
            job_id=response.job_id,
            input_columns=input_columns,
            output_columns=output_columns,
        )

        remote_job = RemoteJob(
            job_id=response.job_id,
            table_name=self._name,
            column_name=output_columns[0],
            job_type="backfill",
            conn=self._conn,
        )
        fut = RemoteJobFuture(remote_job)
        if _return_future:
            return fut
        return Job(
            fut,
            table_name=self._name,
            column_names=output_columns,
            result_cls=BackfillJobResult,
        )

    def _canonical_backfill_output_column(self, col_name: str) -> str:
        """Resolve a backfill target without accepting nested output fields."""

        if col_name in self.schema.names:
            return col_name
        try:
            resolved = resolve_arrow_field_path(self.schema, col_name)
        except (KeyError, ValueError):
            return col_name
        if len(resolved.segments) > 1:
            raise ValueError(
                f"Nested backfill output target {col_name!r} resolves to "
                f"{resolved.canonical_path!r}, but Geneva backfill outputs must "
                "be registered top-level virtual columns. Use nested fields as "
                "UDF inputs or register a top-level output column."
            )
        return resolved.canonical_path

    def _virtual_column_input_paths(self, col_name: str) -> list[str] | None:
        """Return canonical virtual-column inputs from field metadata."""

        try:
            field = self.schema.field(col_name)
        except KeyError:
            return None
        metadata = field.metadata or {}
        raw_inputs = metadata.get(b"virtual_column.udf_inputs")
        if raw_inputs is None:
            return None
        inputs = json.loads(raw_inputs)
        if inputs is None:
            return None
        return canonical_field_paths(self.schema, inputs)

    def _refresh_async_remote(
        self,
        *,
        src_version: int | None = None,
        max_rows_per_fragment: int | None = None,
        concurrency: int | None = None,
        intra_applier_concurrency: int | None = None,
        cluster: str | None = None,
        manifest: str | None = None,
        output_limit: int | None = None,
        source_task_size: int | None = None,
        **kwargs: Any,
    ) -> "Job":
        """Dispatch refresh via the namespace API (remote ``db://`` path).

        Builds a ``RefreshMaterializedViewRequest`` and calls the
        configured namespace client. Returns a :class:`Job` wrapping a
        :class:`RemoteJobFuture` that polls phalanx for completion.
        """
        from lance_namespace import RefreshMaterializedViewRequest

        from geneva.jobs.remote import RemoteJob
        from geneva.jobs.types import Job, RefreshJobResult
        from geneva.remote_v2 import RemoteJobFuture

        ns = self._conn.namespace_client()
        request_kwargs: dict[str, Any] = {
            "id": self._table_id,
            "src_version": src_version,
            "max_rows_per_fragment": max_rows_per_fragment,
            "concurrency": concurrency,
            "intra_applier_concurrency": intra_applier_concurrency,
            "cluster": cluster,
            "manifest": manifest,
            "output_limit": output_limit,
        }
        # source_task_size was added to the namespace API later; only forward it
        # when the installed lance-namespace version carries the field, so an
        # older client degrades gracefully instead of failing.
        #
        # Deliberately not folded into the surplus bag below: the server rejects
        # keys it considers driver-owned, which would turn today's ignored knob
        # into a failed dispatch. Worth revisiting once that list is confirmed.
        if source_task_size is not None:
            if "source_task_size" in RefreshMaterializedViewRequest.model_fields:
                request_kwargs["source_task_size"] = source_task_size
            else:
                _LOG.warning(
                    "source_task_size is not supported by the installed "
                    "lance-namespace version; ignoring it for this remote refresh"
                )

        request = build_remote_request(
            RefreshMaterializedViewRequest, request_kwargs, kwargs, op="refresh"
        )
        response = ns.refresh_materialized_view(request)

        self._conn._history.launch(self._name, "", job_id=response.job_id)

        # See _backfill_async_remote: geneva_driver owns _geneva_jobs writes.
        remote_job = RemoteJob(
            job_id=response.job_id,
            table_name=self._name,
            column_name=None,
            job_type="refresh",
            conn=self._conn,
        )
        fut = RemoteJobFuture(remote_job)
        return Job(
            fut,
            table_name=self._name,
            column_names=[],
            result_cls=RefreshJobResult,
        )

    def _add_columns_remote(
        self,
        transforms: dict[str, "str | UDF | tuple[UDF, list[str]]"],
    ) -> None:
        """Add columns via the namespace API (remote ``db://`` path)."""
        from lance_namespace import AlterTableAddColumnsRequest
        from lance_namespace_urllib3_client.models.add_columns_entry import (
            AddColumnsEntry,
        )
        from lance_namespace_urllib3_client.models.add_virtual_column_entry import (
            AddVirtualColumnEntry,
        )

        from geneva.virtual_column import build_virtual_column_entry

        ns = self._conn.namespace_client()
        new_columns: list[AddColumnsEntry] = []
        for col_name, spec in transforms.items():
            if isinstance(spec, str):
                new_columns.append(AddColumnsEntry(name=col_name, expression=spec))
            else:
                if isinstance(spec, tuple):
                    udf, input_cols = spec
                else:
                    udf = spec
                    input_cols = udf.input_columns or []
                input_cols = canonical_field_paths(self.schema, input_cols) or []
                if udf.is_multi_output:
                    raise NotImplementedError(
                        "RemoteTable.add_columns() does not yet support Columns[T] "
                        "multi-column UDFs."
                    )
                entry_dict = build_virtual_column_entry(
                    col_name,
                    udf,
                    input_cols,
                    self._conn._packager,
                    table_ref=self.get_reference(),
                )
                vc = AddVirtualColumnEntry.model_validate(entry_dict)
                new_columns.append(AddColumnsEntry(name=col_name, virtual_column=vc))

        request = AlterTableAddColumnsRequest(
            id=self._table_id,
            new_columns=new_columns,
        )
        # TODO: Remove retry once phalanx updates its table cache after write
        # operations. Currently the stale cache causes commit conflicts when
        # add_columns runs shortly after create_table.
        max_retries = 3
        for attempt in range(max_retries):
            try:
                ns.alter_table_add_columns(request)
                break
            except Exception as exc:
                if (
                    "Retryable commit conflict" in str(exc)
                    and attempt < max_retries - 1
                ):
                    _LOG.warning(
                        "Retryable commit conflict on add_columns (attempt %d/%d), "
                        "retrying: %s",
                        attempt + 1,
                        max_retries,
                        exc,
                    )
                    self.checkout_latest()
                    continue
                raise

        self.checkout_latest()

    def _alter_columns_remote(self, *alterations: dict[str, Any]) -> None:
        """Alter columns via the namespace API (remote ``db://`` path)."""
        from lance_namespace import AlterTableAlterColumnsRequest
        from lance_namespace_urllib3_client.models.alter_columns_entry import (
            AlterColumnsEntry,
        )
        from lance_namespace_urllib3_client.models.alter_virtual_column_entry import (
            AlterVirtualColumnEntry,
        )

        from geneva.transformer import UDF
        from geneva.virtual_column import build_virtual_column_entry

        ns = self._conn.namespace_client()
        out: list[AlterColumnsEntry] = []
        for alter in alterations:
            if "path" not in alter:
                raise ValueError("path is required to alter computed column's udf")

            if "virtual_column" in alter and "udf" in alter:
                raise ValueError(
                    "alter_columns: pass either 'udf' (preferred) or "
                    "'virtual_column' (deprecated), not both"
                )

            udf_obj = alter.get("udf")
            if "virtual_column" in alter and udf_obj is None:
                udf_obj = alter.get("virtual_column")
                if not isinstance(udf_obj, UDF):
                    raise ValueError("virtual_column must be a UDF")
                _LOG.warning("alter_columns 'virtual_column' is deprecated, use 'udf'.")

            if udf_obj is not None:
                if not isinstance(udf_obj, UDF):
                    raise ValueError("udf must be a UDF")
                if udf_obj.is_multi_output:
                    raise NotImplementedError(
                        "RemoteTable.alter_columns() does not yet support "
                        "Columns[T] multi-column UDFs."
                    )
                input_cols = alter.get("input_columns")
                if input_cols is None:
                    input_cols = udf_obj.input_columns or []
                input_cols = canonical_field_paths(self.schema, input_cols) or []
                entry_dict = build_virtual_column_entry(
                    alter["path"],
                    udf_obj,
                    input_cols,
                    self._conn._packager,
                    table_ref=self.get_reference(),
                )
                vc = AlterVirtualColumnEntry.model_validate(entry_dict)
                out.append(
                    AlterColumnsEntry(
                        path=alter["path"],
                        virtual_column=vc,
                    )
                )
            else:
                out.append(AlterColumnsEntry.model_validate(alter))

        request = AlterTableAlterColumnsRequest(
            id=self._table_id,
            alterations=out,
        )
        ns.alter_table_alter_columns(request)


# Backward-compatible alias (previously a subclass that guarded the
# remote ``db://`` dispatch paths).
NativeTable = Table
