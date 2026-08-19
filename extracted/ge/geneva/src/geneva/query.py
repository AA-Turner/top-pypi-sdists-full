# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging
import os
import threading
from collections import OrderedDict
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, Any, TypeAlias, cast

import pyarrow as pa
from lancedb.query import (
    LanceEmptyQueryBuilder,
    Query,
    _query_is_plain_scan,
    _scanner_kwargs_for_query,
    _scanner_to_pandas,
    _scanner_to_table,
)
from lancedb.rerankers.base import Reranker
from lancedb.types import BlobMode
from lancedb.util import flatten_columns
from numpy.random import default_rng
from pydantic import BaseModel

# Self / override is not available in python 3.10
from typing_extensions import Self, override  # noqa: UP035

from geneva.db import Connection, dataset_uses_stable_row_ids
from geneva.packager import UDFPackager, UDFSpec
from geneva.transformer import BACKFILL_SELECTED, UDF
from geneva.utils.arrow import batch_add_column
from geneva.utils.schema import canonical_field_paths, resolve_arrow_field_path

if TYPE_CHECKING:
    import pandas as pd
    from lancedb.expr import Expr

    # The shapes lancedb accepts for ``Query.columns``.
    QueryColumns: TypeAlias = (
        list[str] | list[tuple[str, str | Expr]] | dict[str, str | Expr] | None
    )

_INTERNAL_ROW_ID_SCAN_BATCH_SIZE = 4096
_VIRTUAL_COLUMN_META_FLAG = "virtual_column"


def _close_iterator(iterator: object) -> None:
    close = getattr(iterator, "close", None)
    if callable(close):
        close()


def _expr_to_str(expr: "str | Expr") -> str:
    """Convert an Expr to its SQL string representation, or pass through strings."""
    # Use duck typing to check for Expr-like objects (has to_sql method)
    if isinstance(expr, str):
        return expr
    return expr.to_sql()


def normalize_query_columns(
    columns: "QueryColumns",
) -> "list[str] | dict[str, str | Expr] | None":
    """Collapse lancedb's ordered ``[(alias, expr)]`` projection into a dict.

    ``Query.columns`` also accepts a list of ``(alias, expr)`` pairs; geneva's
    projection handling only understands the plain-name list and the dict form.
    Dict insertion order preserves the requested projection order.
    """
    if isinstance(columns, list) and columns and not isinstance(columns[0], str):
        pairs = cast("list[tuple[str, str | Expr]]", columns)
        return dict(pairs)
    return cast("list[str] | dict[str, str | Expr] | None", columns)


def _columns_to_str_dict(
    columns: "QueryColumns",
) -> list[str] | dict[str, str] | None:
    """Convert columns dict with Expr values to str values for lance API."""
    columns = normalize_query_columns(columns)
    if columns is None or isinstance(columns, list):
        return columns
    return {k: _expr_to_str(v) for k, v in columns.items()}


def _has_nested_blob(fields: "Iterator[pa.Field] | list[pa.Field]") -> bool:
    """Return True if any field has ``lance-encoding:blob`` metadata below
    the top level (e.g. on a struct child).

    The top-level blob path uses :meth:`LanceDataset.take_blobs`, which only
    accepts top-level column names. Nested blob fields must instead be
    materialized inline by the scanner via ``blob_handling="all_binary"``.
    """

    def walk(field: pa.Field, depth: int) -> bool:
        if (
            depth > 0
            and field.metadata
            and field.metadata.get(b"lance-encoding:blob") == b"true"
        ):
            return True
        if pa.types.is_struct(field.type):
            return any(
                walk(field.type.field(i), depth + 1)
                for i in range(field.type.num_fields)
            )
        return False

    return any(walk(f, 0) for f in fields)


def _resolve_field(schema: pa.Schema, name: str) -> pa.Field:
    """Resolve a possibly nested column path to a PyArrow field.

    For struct paths (e.g., ``info.left`` or ``literal.`a.b```), return a field
    whose name is the canonical path and whose type, nullable flag, and metadata
    come from the leaf field.
    """

    try:
        resolved = resolve_arrow_field_path(schema, name)
    except (KeyError, ValueError) as exc:
        raise KeyError(f"Column {name} does not exist in schema") from exc
    return resolved.as_projected_field()


def _without_virtual_column_metadata(field: pa.Field, *, name: str) -> pa.Field:
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
        name,
        field.type,
        nullable=field.nullable,
        metadata=metadata or None,
    )


if TYPE_CHECKING:
    from lance import LanceDataset

    from geneva.table import Table

_LOG = logging.getLogger(__name__)
_LOG.setLevel(logging.INFO)


# Process-global cache of opened LanceDatasets for read reuse, keyed by the
# immutable snapshot identity ``(uri, version, storage_options)``.
#
# ``Table.to_lance()`` opens a fresh ``LanceDataset`` (re-reading the manifest)
# on every call, so a distributed backfill re-opens the source once per read
# task — thousands of redundant manifest reads on a many-fragment table. A
# pinned dataset version is an immutable snapshot, so sharing the opened dataset
# across read tasks in the same worker process is safe. Tunable via
# ``GENEVA_DATASET_CACHE_SIZE`` (default 64; ``0`` disables and restores
# open-per-read). Used only on read paths, where the dataset is never mutated.
_read_dataset_cache: "OrderedDict[tuple, LanceDataset]" = OrderedDict()
_read_dataset_cache_lock = threading.Lock()


def _read_dataset_cache_capacity() -> int:
    try:
        return int(os.environ.get("GENEVA_DATASET_CACHE_SIZE", "64"))
    except ValueError:
        return 64


def clear_read_dataset_cache() -> None:
    """Drop all cached read datasets (test/maintenance helper)."""
    with _read_dataset_cache_lock:
        _read_dataset_cache.clear()


def _direct_open_uri(table: "Table") -> str | None:
    """Physical URI when ``table`` is eligible for a direct (non-namespace) open.

    Namespace-backed datasets re-resolve the table through the namespace during
    scan IO; on a plain dir namespace that round-trip vends nothing and its
    transient failures kill scans (GEN-758). Only plain ``dir`` namespaces with
    no credential vending and no branch checkout qualify; anything else,
    including any error while checking, returns ``None``.
    """
    try:
        ns_config = getattr(getattr(table, "_conn", None), "_ns_config", None)
        if ns_config is None or ns_config.namespace_client_impl != "dir":
            return None
        props = ns_config.namespace_client_properties or {}
        for key in props:
            key_lower = key.lower()
            if key_lower.startswith("credential_vendor.") or (
                key_lower == "vend_input_storage_options"
            ):
                return None
        ltbl = getattr(table, "_ltbl", None)
        current_branch = getattr(ltbl, "current_branch", None)
        if callable(current_branch) and current_branch() is not None:
            return None
        return table.uri
    except Exception:
        return None


def _open_dataset_for_read(table: "Table", version: int | None) -> "LanceDataset":
    """Open ``table`` for reading, preferring a direct physical-URI open.

    Direct opens install no dynamic storage-options provider, so scan IO never
    re-resolves the table through the namespace (GEN-758). Ineligible tables
    and failed direct opens use the namespace-backed ``to_lance()`` open.
    """
    uri = _direct_open_uri(table)
    if uri is not None:
        import lance

        try:
            pinned = version if version is not None else table.version
            storage_options = {
                **(getattr(table._conn, "_storage_options", None) or {}),
                **(getattr(table, "_storage_options", None) or {}),
            } or None
            return lance.dataset(uri, version=pinned, storage_options=storage_options)
        except Exception:
            _LOG.warning(
                "Direct read open failed for %s (version=%s); falling back to "
                "the namespace-backed open",
                uri,
                version,
                exc_info=True,
            )
    # to_lance: fresh — namespace-backed open for ineligible tables / fallback
    dataset = table.to_lance()
    if version is not None and getattr(dataset, "version", None) != version:
        dataset = dataset.checkout_version(version)
    return dataset


def open_read_dataset(table: "Table", version: int | None = None) -> "LanceDataset":
    """Return a process-cached read-only ``LanceDataset`` for ``table``.

    Caches by ``(uri, version, storage_options)`` so repeated read tasks against
    the same pinned snapshot reuse one open instead of re-reading the manifest
    each time. Returns a fresh open when caching is disabled (capacity ``0``).

    When ``version`` is given, the cache key and the opened dataset are pinned to
    that explicit snapshot version instead of ``table.version``. A backfill reads
    a *pinned* source snapshot, but the table's *current* version advances on
    every commit cascade; keying on ``table.version`` therefore invalidated the
    cache on each commit (~one reopen per fragment at scale). Pinning to the
    snapshot version the caller already knows keeps the entry valid for the whole
    backfill window (GEN-574).

    Eligible dir-namespace tables are opened directly by physical URI
    (GEN-758); see ``_direct_open_uri``.
    """
    capacity = _read_dataset_cache_capacity()
    if capacity <= 0:
        return _open_dataset_for_read(table, version)

    key = (
        table.uri,
        version if version is not None else table.version,
        tuple(sorted((getattr(table, "_storage_options", None) or {}).items())),
    )
    # Lock-free hit path (GEN-574). A dict lookup is atomic under the GIL, so a
    # cache hit needs no lock — taking ``_read_dataset_cache_lock`` on every hit
    # serialized hundreds of read tasks per worker and regressed the wall at
    # high actor/fragment counts. We deliberately skip the LRU ``move_to_end``
    # bookkeeping here (it is the only reason a hit would need the lock); for the
    # handful of hot snapshots this cache holds, strict-LRU recency buys nothing
    # and eviction below simply degrades to insertion order.
    dataset = _read_dataset_cache.get(key)
    if dataset is not None:
        return dataset

    # Miss: open outside the lock; a rare concurrent miss just opens twice
    # (harmless). Publish and evict to capacity under the lock.
    dataset = _open_dataset_for_read(table, version)
    with _read_dataset_cache_lock:
        _read_dataset_cache[key] = dataset
        _read_dataset_cache.move_to_end(key)
        while len(_read_dataset_cache) > capacity:
            _read_dataset_cache.popitem(last=False)
    return dataset


MATVIEW_META = "geneva::view::"
# Serialized ``GenevaQuery`` JSON describing the MV's source query.
# Used uniformly across plain query, UDTF, and chunker MVs.
MATVIEW_META_QUERY = f"{MATVIEW_META}query"
# Source-table identity. ``resolve_mv_source_identity`` reads these as
# the canonical location for "which table does this MV refresh from"; the
# ``GenevaQuery`` JSON also carries them as a fallback for create paths
# (currently phalanx) that don't know the source up front.
MATVIEW_META_BASE_TABLE = f"{MATVIEW_META}base_table"
MATVIEW_META_BASE_DBURI = f"{MATVIEW_META}base_table_db_uri"
MATVIEW_META_BASE_VERSION = f"{MATVIEW_META}base_table_version"
MATVIEW_META_VERSION = f"{MATVIEW_META}version"
# UDTF / chunker spec stored alongside the query.
MATVIEW_META_UDTF = f"{MATVIEW_META}udtf"
MATVIEW_META_CHUNKER = f"{MATVIEW_META}chunker"
MATVIEW_VERSION_CHUNKER = "chunker"
MATVIEW_META_SCALAR_UDTF = f"{MATVIEW_META}scalar_udtf"
MATVIEW_VERSION_SCALAR_UDTF = "scalar_udtf"
# Manifest snapshotted into the view at create time (revamped-api-mv-udtf.md §3)
MATVIEW_META_MANIFEST = f"{MATVIEW_META}manifest"
MATVIEW_META_MANIFEST_CHECKSUM = f"{MATVIEW_META}manifest_checksum"
# Namespace path for materialized views (source table's namespace path)
MATVIEW_META_NAMESPACE_PATH = f"{MATVIEW_META}namespace_path"


class PydanticUDFSpec(BaseModel):
    name: str
    backend: str
    udf_payload: bytes
    runner_payload: bytes | None

    @classmethod
    def from_attrs(cls, spec: UDFSpec) -> "PydanticUDFSpec":
        return PydanticUDFSpec(
            name=spec.name,
            backend=spec.backend,
            udf_payload=spec.udf_payload,
            runner_payload=spec.runner_payload,
        )

    def to_attrs(self) -> UDFSpec:
        return UDFSpec(
            name=self.name,
            backend=self.backend,
            udf_payload=self.udf_payload,
            runner_payload=self.runner_payload,
        )


class ColumnUDF(BaseModel):
    output_index: int
    output_name: str
    udf: PydanticUDFSpec
    input_columns: list[str] | None = None


@dataclass
class ExtractedTransform:
    output_index: int
    output_name: str
    udf: UDF
    input_columns: list[str] | None = None


class GenevaQuery(BaseModel):
    base: Query
    shuffle: bool | None = None
    shuffle_seed: int | None = None
    fragment_ids: list[int] | None = None
    with_row_address: bool | None = None
    column_udfs: list[ColumnUDF] | None = None
    # Source-table identity carried inside the serialized query. This is
    # the **authoritative** source for "which table does this MV refresh
    # from" — see :func:`resolve_mv_source_identity`. Carried alongside
    # the query because phalanx treats ``source_query`` as opaque, so the
    # client gets to define what goes inside it.
    source_table: str | None = None
    source_db_uri: str | None = None

    def extract_column_udfs(self, packager: UDFPackager) -> list[ExtractedTransform]:
        """
        Loads a set of transforms that reflect the column_udfs and map_batches_udfs
        of the query.
        """
        transforms = []
        if self.column_udfs is not None:
            for column_udf in self.column_udfs:
                udf = packager.unmarshal(column_udf.udf.to_attrs())
                if udf is not None and column_udf.input_columns is not None:
                    udf.input_columns = list(column_udf.input_columns)
                transforms.append(
                    ExtractedTransform(
                        output_index=column_udf.output_index,
                        output_name=column_udf.output_name,
                        udf=udf,
                        input_columns=column_udf.input_columns,
                    )
                )
        return transforms


def resolve_mv_source_identity(
    schema_metadata: dict[bytes, bytes] | None,
) -> tuple[str | None, str | None, list[str] | None]:
    """Return ``(source_table, source_db_uri, namespace_path)`` for a
    materialized view.

    Source identity is stored in ``MATVIEW_META_BASE_TABLE`` /
    ``MATVIEW_META_BASE_DBURI`` — the canonical location, written by
    both the native ``create_materialized_view`` path and phalanx
    """
    if not schema_metadata:
        return (None, None, None)

    def _get(key: str) -> str | None:
        v = schema_metadata.get(key.encode())
        return v.decode() if isinstance(v, bytes) else v

    src_table = _get(MATVIEW_META_BASE_TABLE)
    src_db_uri = _get(MATVIEW_META_BASE_DBURI)

    if src_table is None or src_db_uri is None:
        raw_query = _get(MATVIEW_META_QUERY)
        if raw_query is not None:
            try:
                q = GenevaQuery.model_validate_json(raw_query)
            except Exception:
                q = None
            if q is not None:
                src_table = src_table or q.source_table
                src_db_uri = src_db_uri or q.source_db_uri

    ns_path_str = _get(MATVIEW_META_NAMESPACE_PATH)
    ns_path = ns_path_str.split("$") if ns_path_str else None

    return (src_table, src_db_uri, ns_path)


class GenevaQueryBuilder(LanceEmptyQueryBuilder):
    """A proxy that wraps LanceQueryBuilder and adds geneva-specific functionality."""

    def __init__(self, table: "Table") -> None:
        super().__init__(table)
        self._table = table
        self._shuffle = None
        self._shuffle_seed = None
        self._fragment_ids = None
        self._with_row_address = None
        self._internal_api_enabled = False
        self._column_udfs = None
        self._with_where_as_bool_column = False
        self._read_version: int | None = None

    def _internal_api_only(self) -> None:
        if not self._internal_api_enabled:
            raise ValueError(
                "This method is for internal use only and subject to change. "
                "Call enable_internal_api() first to enable."
            )

    @override
    def select(self, columns: "list[str] | Mapping[str, str | UDF | Expr]") -> Self:
        """
        Select the output columns of the query.

        Parameters
        ----------
        columns: list[str] | dict[str, str | Expr] | dict[str, UDF]
            The columns to select.

            If a list of strings, each string is the name of a column to select.

            If a dictionary of strings then the key is the output name of the column
            and the value is either an SQL expression (str), an Expr, or a UDF.
        """
        if isinstance(columns, dict):
            self._column_udfs = {
                key: (value, index)
                for (index, (key, value)) in enumerate(columns.items())
                if isinstance(value, UDF)
            }
            # Filter out UDFs and convert Expr to str for super().select()
            filtered_columns: dict[str, str | Expr] = {
                key: value
                for key, value in columns.items()
                if not isinstance(value, UDF)
            }
            super().select(filtered_columns)
        else:
            super().select(columns)  # type: ignore[arg-type]
        return self

    def shuffle(self, seed: int | None = None) -> Self:
        """Shuffle the rows of the table"""
        self._shuffle = True
        self._shuffle_seed = seed
        return self

    def enable_internal_api(self) -> Self:
        """
        Enable internal APIs
        WARNING: Internal APIs are subject to change
        """
        self._internal_api_enabled = True
        return self

    def with_fragments(self, fragments: list[int] | int) -> Self:
        """
        Filter the rows of the table to only include the specified fragments.
        """
        self._internal_api_only()
        self._fragment_ids = [fragments] if isinstance(fragments, int) else fragments
        return self

    def with_row_address(self) -> Self:
        """
        Include the physical row address in the result
        WARNING: INTERNAL API DETAIL
        """
        self._internal_api_only()
        self._with_row_address = True
        return self

    def with_read_version(self, version: int | None) -> Self:
        """Pin reads to a snapshot version so the read-dataset cache stays valid
        across commits that advance the table's current version (GEN-574).
        WARNING: INTERNAL API DETAIL
        """
        self._internal_api_only()
        self._read_version = version
        return self

    def with_where_as_bool_column(self) -> Self:
        """
        Include the filter selected column in the result instead of just selected rows
        """
        self._internal_api_only()
        self._with_where_as_bool_column = True
        return self

    @override
    def to_query_object(self) -> GenevaQuery:  # type: ignore
        query = super().to_query_object()
        result = GenevaQuery(
            base=query,
            shuffle=self._shuffle,
            shuffle_seed=self._shuffle_seed,
            fragment_ids=self._fragment_ids,
            with_row_address=self._with_row_address,
        )
        if self._column_udfs:
            result.column_udfs = [
                ColumnUDF(
                    output_index=index,
                    output_name=name,
                    udf=PydanticUDFSpec.from_attrs(
                        self._table._conn._packager.marshal(
                            udf,
                            table_ref=self._table.get_reference(),
                        )
                    ),
                    input_columns=canonical_field_paths(
                        self._table.schema,
                        udf.input_columns,
                    ),
                )
                for (name, (udf, index)) in self._column_udfs.items()
            ]
        return result

    @classmethod
    def from_query_object(
        cls, table: "Table", query: GenevaQuery
    ) -> "GenevaQueryBuilder":
        result = GenevaQueryBuilder(table)

        # TODO: Add from_query_object to lancedb.  For now, this will work
        # for simple (non-vector, non-fts) queries.
        base_columns = normalize_query_columns(query.base.columns)
        if base_columns is not None:
            result.select(base_columns)
        if query.base.filter:
            result.where(query.base.filter)
        if query.base.limit:
            result.limit(query.base.limit)
        if query.base.offset:
            result.offset(query.base.offset)
        if query.base.with_row_id:
            result.with_row_id(True)

        result._shuffle = query.shuffle
        result._shuffle_seed = query.shuffle_seed
        if query.column_udfs:
            result._column_udfs = {}
            for column_udf in query.column_udfs:
                udf = table._conn._packager.unmarshal(column_udf.udf.to_attrs())
                if udf is not None and column_udf.input_columns is not None:
                    udf.input_columns = list(column_udf.input_columns)
                result._column_udfs[column_udf.output_name] = (
                    udf,
                    column_udf.output_index,
                )
        result._fragment_ids = query.fragment_ids
        result._with_row_address = query.with_row_address
        result._internal_api_enabled = True
        return result

    def take_rows(self, rows: list[int]) -> pa.Table:
        query = self.to_query_object()
        return open_read_dataset(self._table)._take_rows(
            rows, _columns_to_str_dict(query.base.columns)
        )

    @override
    def _plain_scan_to_pandas(
        self, blob_mode: BlobMode, flatten: int | bool | None = None, **kwargs: Any
    ) -> "pd.DataFrame | None":
        base_query = super().to_query_object()
        if (
            self._column_udfs
            or self._with_where_as_bool_column
            or self._shuffle
            or not _query_is_plain_scan(base_query)
        ):
            return None

        dataset: LanceDataset = open_read_dataset(self._table)
        scanner = dataset.scanner(
            **_scanner_kwargs_for_query(base_query, blob_mode, dataset)
        )
        if flatten is not None:
            # LanceDB owns the public `flatten` option. For blob descriptions it
            # calls this plain-scan hook instead of Geneva's `to_arrow()`; flatten
            # the scanner table here to preserve LanceDB's `to_pandas` semantics.
            tbl = flatten_columns(_scanner_to_table(scanner), flatten)
            return tbl.to_pandas(**kwargs)
        return _scanner_to_pandas(scanner, blob_mode, **kwargs)

    def _infer_sql_expression_type(self, expr: str, dest_name: str) -> pa.DataType:
        """Infer output type of SQL expression by evaluating on source table."""
        dataset = open_read_dataset(self._table)
        scanner = dataset.scanner(columns={dest_name: expr}, limit=1)
        return scanner.projected_schema.field(dest_name).type

    def _schema_for_query(self, include_metacols: bool = True) -> pa.Schema:
        schema = self._table._ltbl.schema

        base_query = super().to_query_object()
        base_query.columns = normalize_query_columns(base_query.columns)

        if base_query.columns is not None:
            if isinstance(base_query.columns, list):
                fields = [_resolve_field(schema, col) for col in base_query.columns]
            else:
                fields = []
                for dest_name, expr in base_query.columns.items():
                    expr_str = _expr_to_str(expr)
                    try:
                        field = _resolve_field(schema, expr_str)
                    except KeyError:
                        if dest_name == BACKFILL_SELECTED:
                            # HACK special case for BACKFILL_SELECTED
                            field = pa.field(dest_name, pa.bool_(), True)
                        else:
                            # SQL expression - infer type by executing on sample data
                            inferred_type = self._infer_sql_expression_type(
                                expr_str, dest_name
                            )
                            field = pa.field(dest_name, inferred_type, nullable=True)

                    fields.append(
                        _without_virtual_column_metadata(field, name=dest_name)
                    )

        else:
            fields = list(schema)

        if self._column_udfs is not None:
            for output_name, (udf, output_index) in self._column_udfs.items():
                fields.insert(
                    output_index,
                    pa.field(output_name, udf.data_type, metadata=udf.field_metadata),
                )

        if include_metacols and base_query.with_row_id:
            fields += [pa.field("_rowid", pa.uint64())]

        if include_metacols and self._with_row_address:
            # uint64 to match what Lance emits, and every other declaration of
            # this metacolumn in Geneva (apply/task.py, runners/ray/writer.py,
            # apply/error_handling.py).
            fields += [pa.field("_rowaddr", pa.uint64())]

        return pa.schema(fields)

    @property
    def schema(self) -> pa.Schema:
        return self._schema_for_query()

    @override
    def output_schema(self) -> pa.Schema:
        # lancedb's base ``output_schema`` re-derives the schema by passing
        # ``to_query_object()`` into lancedb internals, but Geneva's
        # ``to_query_object`` returns a ``GenevaQuery`` wrapper that those
        # internals don't understand. Compute the schema directly instead.
        return self._schema_for_query()

    @override
    def to_batches(
        self, /, batch_size: int | None = None, *, timeout: timedelta | None = None
    ) -> pa.RecordBatchReader:
        schema_no_meta = self._schema_for_query(include_metacols=False)

        # Collect top-level blob columns. These are materialized via
        # ``dataset.take_blobs`` so UDFs receive ``BlobFile`` objects.
        blob_columns: dict[str, int] = {
            f.name: idx
            for idx, f in enumerate(schema_no_meta)
            if f.metadata and f.metadata.get(b"lance-encoding:blob") == b"true"
        }
        # Nested blob fields (e.g. ``image.image_bytes``) are not addressable
        # by ``take_blobs`` in current Lance. Ask the scanner to inline them
        # as ``large_binary`` so the in-memory schema matches the declared
        # schema and downstream carry-forward merges succeed.
        nested_blob = _has_nested_blob(list(schema_no_meta))

        base_query = super().to_query_object()
        base_query.columns = normalize_query_columns(base_query.columns)
        orig_filter = base_query.filter

        # Enforce row_id if we need blobs or where-as-column
        if blob_columns or (self._with_where_as_bool_column and orig_filter):
            base_query.with_row_id = True

        # UDF extra-column bookkeeping
        extra_columns: list[str] = []
        if self._column_udfs and base_query.columns is not None:
            # collect all needed inputs
            current_cols = (
                set(base_query.columns)
                if isinstance(base_query.columns, list)
                else set(base_query.columns.keys())
            )
            for udf, _ in self._column_udfs.values():
                for inp in udf.input_columns or []:
                    if inp not in current_cols:
                        extra_columns.append(inp)
                        current_cols.add(inp)

        # append extra_columns into the query, track their positions
        added_columns: list[int] = []
        if base_query.columns is not None and extra_columns:
            if isinstance(base_query.columns, list):
                pos = len(base_query.columns)
                for col in extra_columns:
                    added_columns.append(pos)
                    base_query.columns.append(col)
                    pos += 1
            else:
                pos = len(base_query.columns)
                for col in extra_columns:
                    added_columns.append(pos)
                    base_query.columns[col] = col
                    pos += 1

        # sanity‐check unsupported features
        if self._shuffle:
            raise NotImplementedError("Shuffle is not yet implemented")
        if base_query.vector:
            raise NotImplementedError("Vector search not yet implemented")
        if base_query.full_text_query:
            raise NotImplementedError("FTS search not yet implemented")

        dataset: LanceDataset = open_read_dataset(
            self._table, version=self._read_version
        )
        fragments = (
            [dataset.get_fragment(fid) for fid in self._fragment_ids]
            if self._fragment_ids
            else list(dataset.get_fragments())
        )

        schema_with_meta = self._schema_for_query(include_metacols=True)

        # Extract offset/limit for global application across fragments
        global_offset = base_query.offset or 0
        global_limit = base_query.limit

        # When the query is scoped to a single fragment we can push
        # ``offset``/``limit`` directly to the Lance scanner. This is the
        # common geneva backfill case (each checkpoint task issues a
        # ``with_fragments(frag).offset(o).limit(l)`` query).
        #
        # Without pushdown the ``blob_handling="all_binary"`` (nested-blob)
        # path scans the whole fragment per task and then slices in Python,
        # causing every checkpoint task on a fragment to re-read all of its
        # blob bytes -- amplification ≈ rows_per_fragment / checkpoint_size.
        # Multi-fragment queries continue to use the Python-side global
        # offset/limit tracking below.
        push_offset_limit_to_scanner = len(fragments) == 1

        # Fragment‐by‐fragment generator with global offset/limit tracking
        def gen() -> Iterator[pa.RecordBatch]:
            # When pushing to the scanner, offset is satisfied by Lance itself
            # so the post-loop offset logic must short-circuit.
            rows_skipped = global_offset if push_offset_limit_to_scanner else 0
            rows_emitted = 0

            for frag in fragments:
                # Check if we've already emitted enough rows
                if global_limit is not None and rows_emitted >= global_limit:
                    break

                # build per‐fragment matching_ids if we're doing where-as-column
                frag_ids: set[int] | None = None
                if self._with_where_as_bool_column and orig_filter:
                    frag_ids = set()
                    id_scan = dataset.scanner(
                        columns=["_rowid"],
                        with_row_id=True,
                        filter=orig_filter,
                        fragments=[frag],
                        # This scan only builds the membership set for
                        # BACKFILL_SELECTED; it does not shape emitted batches,
                        # and it projects a single 8-byte column, so a whole
                        # batch is ~32 KB regardless. Keep it coarse so a
                        # caller asking for tiny output batches doesn't turn a
                        # trivial id scan into thousands of scanner round
                        # trips.
                        batch_size=max(
                            batch_size or 0,
                            _INTERNAL_ROW_ID_SCAN_BATCH_SIZE,
                        ),
                    )
                    id_batches = id_scan.to_batches()
                    try:
                        for id_batch in id_batches:
                            rowid_list = id_batch["_rowid"].to_pylist()
                            valid_ids = [
                                int(rid) for rid in rowid_list if rid is not None
                            ]
                            frag_ids.update(valid_ids)
                    finally:
                        _close_iterator(id_batches)

                # choose filter for main scan
                scan_filter = None if frag_ids is not None else orig_filter

                # run the main scan over this fragment.
                # ``blob_handling="all_binary"`` is required when the
                # projection contains a nested blob field: without it, Lance
                # returns ``struct<position: uint64, size: uint64>`` for the
                # nested column, which crashes the carry-forward merge in
                # ``apply/task.py`` with an ``ArrowTypeError``. We don't set
                # it unconditionally because the top-level blob path relies
                # on ``take_blobs`` returning lazy ``BlobFile`` handles.
                #
                # offset/limit are pushed to the scanner only when the query
                # is single-fragment (see ``push_offset_limit_to_scanner``
                # above for the rationale). Multi-fragment queries leave
                # them off and apply offset/limit below.
                scanner_kwargs: dict[str, Any] = {
                    "columns": _columns_to_str_dict(base_query.columns),
                    "with_row_id": base_query.with_row_id,
                    "with_row_address": self._with_row_address,
                    "filter": scan_filter,
                    "batch_size": batch_size,
                    "fragments": [frag],
                    "blob_handling": "all_binary" if nested_blob else None,
                }
                if push_offset_limit_to_scanner:
                    if global_offset:
                        scanner_kwargs["offset"] = global_offset
                    if global_limit is not None:
                        scanner_kwargs["limit"] = global_limit
                main_scan = dataset.scanner(**scanner_kwargs)
                main_batches = main_scan.to_batches()
                try:
                    for batch in main_batches:
                        # blob injection. Skipped when ``blob_handling="all_binary"``
                        # is active: Lance has already materialized every blob in
                        # the projection inline as ``large_binary``, so calling
                        # ``take_blobs`` would overwrite real bytes with
                        # ``BlobFile`` handles.
                        if blob_columns and not nested_blob:
                            rowid_list = batch["_rowid"].to_pylist()  # type: ignore[index]
                            ids = [int(rid) for rid in rowid_list if rid is not None]
                            for col_name in blob_columns:
                                if hasattr(batch, "to_pylist"):
                                    rows = cast(
                                        "list[dict[str, Any]]",
                                        batch.to_pylist(),  # type: ignore[attr-defined]
                                    )
                                else:
                                    rows = cast("list[dict[str, Any]]", batch)
                                try:
                                    blob_files = dataset.take_blobs(col_name, ids=ids)
                                    for elem, blob in zip(
                                        rows, blob_files, strict=True
                                    ):
                                        elem[col_name] = blob  # type: ignore[index]
                                except ValueError:
                                    # not blobfile? (maybe because null?) return Null.
                                    for elem in rows:
                                        elem[col_name] = None  # type: ignore[index]
                                batch = rows
                        # UDFs and drop UDF-only columns
                        if self._column_udfs:
                            for col_name, (
                                udf,
                                insert_idx,
                            ) in self._column_udfs.items():
                                arr = udf(batch)
                                if isinstance(batch, pa.RecordBatch):
                                    batch = batch_add_column(
                                        batch,
                                        insert_idx,
                                        pa.field(col_name, arr.type),
                                        arr,
                                    )
                                # else: batch is a list (blob case) - UDFs not supported
                            # remove the extra_columns we only pulled for UDF inputs
                            for drop_idx in reversed(added_columns):
                                if hasattr(batch, "remove_column"):
                                    batch = batch.remove_column(  # type: ignore[attr-defined]
                                        drop_idx + len(self._column_udfs)
                                    )
                                else:
                                    # Handle case where batch is a list
                                    pass

                        # where-as-column mask
                        if frag_ids is not None:
                            if isinstance(batch, list):
                                # blob case -- a list of dicts
                                ids = [row["_rowid"] for row in batch]
                                mask = pa.array(
                                    [rid in frag_ids for rid in ids], pa.bool_()
                                )
                                for i, _row in enumerate(batch):
                                    batch[i][BACKFILL_SELECTED] = mask[i]

                            else:
                                # normal case - pa.RecordBatch
                                ids = batch["_rowid"].to_pylist()
                                mask = pa.array(
                                    [rid in frag_ids for rid in ids], pa.bool_()
                                )
                                field = pa.field(BACKFILL_SELECTED, pa.bool_())
                                batch = batch_add_column(
                                    batch, batch.num_columns, field, mask
                                )

                        # Apply global offset/limit
                        batch_len = (
                            len(batch) if isinstance(batch, list) else batch.num_rows
                        )

                        # Handle offset until we've skipped global_offset rows.
                        if rows_skipped < global_offset:
                            skip_in_batch = min(batch_len, global_offset - rows_skipped)
                            rows_skipped += skip_in_batch
                            if skip_in_batch >= batch_len:
                                # Skip entire batch
                                continue
                            # Slice batch to skip the first skip_in_batch rows
                            if isinstance(batch, list):
                                batch = batch[skip_in_batch:]
                            else:
                                batch = batch.slice(skip_in_batch)
                            batch_len = (
                                len(batch)
                                if isinstance(batch, list)
                                else batch.num_rows
                            )

                        # Skip empty batches (can happen after offset slicing)
                        if batch_len == 0:
                            continue

                        # Handle limit: only emit up to global_limit rows total
                        if global_limit is not None:
                            remaining = global_limit - rows_emitted
                            if remaining <= 0:
                                break
                            if batch_len > remaining:
                                # Slice batch to only emit remaining rows
                                if isinstance(batch, list):
                                    batch = batch[:remaining]
                                else:
                                    batch = batch.slice(0, remaining)
                                batch_len = remaining

                        rows_emitted += batch_len
                        yield batch  # type: ignore[misc]
                        if global_limit is not None and rows_emitted >= global_limit:
                            break
                finally:
                    _close_iterator(main_batches)

        if blob_columns:
            return gen()  # type: ignore[return-value]
        return pa.RecordBatchReader.from_batches(schema_with_meta, gen())  # type: ignore[arg-type]

    @override
    def to_arrow(self, *args, timeout: timedelta | None = None) -> pa.Table:
        return pa.Table.from_batches(
            self.to_batches(*args, timeout=timeout), schema=self.schema
        )

    @override
    def rerank(self, reranker: Reranker) -> Self:
        raise NotImplementedError("rerank is not yet implemented")

    def create_materialized_view(
        self,
        conn: Connection,
        view_name: str,
    ) -> "Table":
        """
        Creates a materialized view of the table.

        The materialized view will be a table that contains the result of the query.
        The view will be populated via a pipeline job.

        Parameters
        ----------
        conn: Connection
            A connection to the database to create the view in.
        view_name: str
            The name of the view to create.

        Raises
        ------
        UserWarning
            If the source table does not have stable row IDs enabled. Without stable
            row IDs, incremental refresh is only supported when refreshing to the
            same source version. Attempting to refresh to a different version will fail.
        """
        import warnings

        # Check if source table has stable row IDs enabled
        source_tbl = self._table

        source_lance_ds = open_read_dataset(source_tbl)
        fragments = list(source_lance_ds.get_fragments())

        # Validate that source table is not empty
        if not fragments:
            raise ValueError(
                f"Cannot create materialized view from empty table "
                f"'{source_tbl.name}'.\n\n"
                "Materialized views require at least one row in the source "
                "table to determine storage characteristics (such as whether "
                "stable row IDs are enabled).\n\n"
                "Please add data to the source table before creating a "
                "materialized view."
            )

        # Read the manifest, not the fragments. On the zero-fragment tables
        # where the two disagree this line is unreachable (rejected above), so
        # it is consistency with the exist_ok validator rather than a behaviour
        # change; the SRID-G06/G07 checks deliberately pin only the validator.
        source_has_stable_row_ids = dataset_uses_stable_row_ids(source_lance_ds)

        if not source_has_stable_row_ids:
            warnings.warn(
                f"Creating materialized view from table '{source_tbl.name}' "
                "without stable row IDs enabled.\n\n"
                "Without stable row IDs, you can only refresh the materialized view "
                "to the SAME source version it was created from. Attempting to refresh "
                "to a different version will fail because compaction operations may "
                "have changed row IDs.\n\n"
                "For full incremental refresh support across all versions, create the "
                "source table with stable row IDs enabled:\n"
                "  db.create_table(\n"
                "      name='table_name',\n"
                "      data=data,\n"
                "      storage_options={'new_table_enable_stable_row_ids': 'true'}\n"
                "  )\n\n"
                "Note: Both 'true' (string) and True (boolean) are accepted.\n\n"
                "Stable row IDs is a Lance feature (added in 0.21.0) exposed via "
                "lancedb's new_table_enable_stable_row_ids option (added in 0.25.4b3).",
                UserWarning,
                stacklevel=2,
            )

        view_schema = self._schema_for_query(include_metacols=True)
        view_schema = view_schema.insert(0, pa.field("__is_set", pa.bool_()))
        view_schema = view_schema.insert(0, pa.field("__source_row_id", pa.int64()))

        query = self.to_query_object()

        # Capture source columns at creation time if no explicit select was used.
        # This ensures that when new columns are added to the source table,
        # the MV refresh only reads the columns that existed at creation time.
        if query.base.columns is None:
            query.base.columns = [
                n
                for n in self._table.schema.names
                if n not in ["__is_set", "__source_row_id"]
            ]

        db_uri = self._table._conn_uri

        query.source_table = source_tbl.name
        query.source_db_uri = db_uri

        # Build metadata including namespace info.
        metadata_dict = {
            MATVIEW_META_QUERY: query.model_dump_json(),
            MATVIEW_META_BASE_TABLE: source_tbl.name,
            MATVIEW_META_BASE_DBURI: db_uri,
            MATVIEW_META_BASE_VERSION: str(source_tbl.version),
            # Store materialized view format version.
            # Version 1: fragment+offset encoding (fragment_id << 32 | offset)
            #   - Used for v0.7.x and earlier (always)
            #   - Used for v0.8.x+ without stable row IDs
            #   - Source table does NOT have stable row IDs
            #   - Refresh only supported to same source version
            # Version 2: stable row IDs (v0.8.x+ with stable row IDs enabled)
            #   - Source table HAS stable row IDs
            #   - Refresh supported across source versions
            MATVIEW_META_VERSION: "2" if source_has_stable_row_ids else "1",
        }

        # Store namespace path as $-delimited string (if source is in a child namespace)
        if self._table._namespace:
            metadata_dict[MATVIEW_META_NAMESPACE_PATH] = "$".join(
                self._table._namespace
            )

        view_schema = view_schema.with_metadata(metadata_dict)

        row_ids_query = GenevaQuery(
            fragment_ids=query.fragment_ids,
            base=query.base,
        )
        row_ids_query.base.with_row_id = True
        row_ids_query.base.columns = []
        row_ids_query.column_udfs = None
        row_ids_query.with_row_address = None

        row_ids_query_builder = GenevaQueryBuilder.from_query_object(
            self._table, row_ids_query
        )

        row_ids_table = row_ids_query_builder.to_arrow()
        row_ids_table = row_ids_table.combine_chunks()
        # Copy is needed so that the array is not read-only
        row_ids = row_ids_table["_rowid"].to_numpy().copy()

        if query.shuffle:
            rng = default_rng(query.shuffle_seed)
            rng.shuffle(row_ids)

        initial_view_table_data = pa.table(
            [
                pa.array(row_ids, type=pa.int64()),
                pa.array([False] * len(row_ids), type=pa.bool_()),
            ],
            names=["__source_row_id", "__is_set"],
        )

        # Create the MV table with system-backed schema. Every backend honours
        # the stable-row-ID create option today (GEN-839); see
        # _supports_stable_row_ids_on_create for how each one gets there.
        storage_options: dict[str, str] = {}
        if conn._supports_stable_row_ids_on_create():
            storage_options["new_table_enable_stable_row_ids"] = "true"

        view_table = conn.create_table(
            view_name,
            data=None,
            schema=view_schema,
            mode="create",
            storage_options=storage_options,
        )
        view_table.add(initial_view_table_data)

        for udf_col, (udf, _output_index) in (self._column_udfs or {}).items():
            input_cols = udf.input_columns
            view_table._configure_computed_column(udf_col, udf, input_cols)

        return view_table


class Column:
    """Present a Column in the Table."""

    def __init__(self, name: str) -> None:
        """Define a column."""
        self.name = name

    def alias(self, alias: str) -> "Column":
        return AliasColumn(self, alias)

    def blob(self) -> "Column":
        return BlobColumn(self)

    def apply(self, batch: pa.RecordBatch) -> tuple[str, pa.Array]:
        return (self.name, batch[self.name])


class BlobColumn(Column):
    def __init__(self, col: Column) -> None:
        self.inner = col


class AliasColumn(Column):
    def __init__(self, col: Column, alias: str) -> None:
        self.col = col
        self._alias = alias

    def apply(self, batch: pa.RecordBatch) -> tuple[str, pa.Array]:
        _, arr = self.col.apply(batch)
        return (self._alias, arr)
