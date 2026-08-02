# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# definition of the read task, which is portion of a fragment

import hashlib
import inspect
import logging
from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any, cast

import attrs
import pyarrow as pa
import pyarrow.compute as pc
from lance.blob import BlobFile
from typing_extensions import override

from geneva.checkpoint_utils import format_checkpoint_key, format_checkpoint_prefix
from geneva.namespace_properties import is_sensitive_namespace_property
from geneva.query import ExtractedTransform
from geneva.table import Table, TableReference
from geneva.transformer import BACKFILL_SELECTED, UDF, UDFArgType, UnpackedUDFField
from geneva.utils import get_null_value_for_type, make_null_array
from geneva.utils.arrow import batch_add_column
from geneva.utils.schema import parse_field_path

_LOG = logging.getLogger(__name__)

DEFAULT_CHECKPOINT_ROWS = 100


_STABLE_REST_NAMESPACE_HEADERS = {"header.x-lancedb-database"}


def _stable_namespace_properties(
    namespace_client_properties: dict[str, str] | None,
) -> tuple[tuple[str, str], ...] | None:
    if not namespace_client_properties:
        return None

    stable_properties: list[tuple[str, str]] = []
    for key, value in namespace_client_properties.items():
        key_lower = key.lower()
        normalized_key = key_lower.replace("-", "_")
        if key_lower.startswith("storage."):
            continue
        if key_lower == "worker_uri":
            continue
        if (
            key_lower.startswith("header.")
            and key_lower not in _STABLE_REST_NAMESPACE_HEADERS
        ):
            continue
        if is_sensitive_namespace_property(normalized_key):
            continue
        stable_properties.append((key, value))

    return tuple(sorted(stable_properties)) or None


def _table_ref_identity(table_ref: TableReference) -> tuple:
    ns = table_ref.namespace_config
    namespace_client_properties = _stable_namespace_properties(
        ns.namespace_client_properties
    )
    return (
        tuple(table_ref.table_id),
        table_ref.version,
        ns.namespace_client_impl,
        namespace_client_properties,
    )


class ReadTask(ABC):
    """
    A task to read data that has a defined output location and unique identifier
    """

    @abstractmethod
    def to_batches(
        self, *, batch_size=DEFAULT_CHECKPOINT_ROWS
    ) -> Iterator[pa.RecordBatch]:
        """Return the data to read"""

    @abstractmethod
    def checkpoint_key(self) -> str:
        """Return a unique key for this task"""

    @abstractmethod
    def dest_frag_id(self) -> int:
        """Return the id of the destination fragment"""

    @abstractmethod
    def dest_offset(self) -> int:
        """Return the offset into the destination fragment"""

    @abstractmethod
    def num_rows(self) -> int:
        """Return the number of rows this task will read"""

    @abstractmethod
    def table_uri(self) -> str:
        """Return the source table URI for this read task"""


@attrs.define(order=True)
class ScanTask(ReadTask):
    uri: str
    table_ref: TableReference
    columns: list[str]
    frag_id: int
    offset: int
    limit: int

    version: int | None = None
    where: str | None = None

    with_row_address: bool = False
    range_blob_columns: frozenset[str] | None = None
    selected_only_blob_columns: frozenset[str] | None = None
    # Plan for decomposing whole-struct columns whose nested blob leaf must be
    # read via the coalesced range path, then reassembled for the carry-forward
    # merge/write. None when no projected struct contains a nested blob.
    struct_blob_decomp: tuple[Any, ...] | None = None
    blob_read_strategy: str | None = None
    blob_read_buffer_size: int | None = None
    # Hash of source data files for input columns in this fragment.
    # Used in checkpoint keys.
    src_files_hash: str | None = None
    src_data_files: frozenset[str] | None = None
    fragment_physical_rows: int | None = None
    fragment_logical_rows: int | None = None
    _table: Table | None = attrs.field(
        default=None, init=False, repr=False, eq=False, order=False
    )

    def bind_table(self, table: Table | None) -> None:
        self._table = table

    def clear_table(self) -> None:
        self._table = None

    def table_ref_for_read(self) -> TableReference:
        if self.version is not None and self.table_ref.version != self.version:
            return attrs.evolve(self.table_ref, version=self.version)
        return self.table_ref

    def _get_table(self) -> Table:
        if self._table is not None:
            return self._table
        # Use the task's version (set during planning) to ensure we read from
        # the correct point-in-time snapshot, not the latest version
        return self.table_ref_for_read().open()

    @override
    def to_batches(
        self, *, batch_size=DEFAULT_CHECKPOINT_ROWS
    ) -> Iterator[pa.RecordBatch]:
        _LOG.debug(
            f"Reading {self.uri} with version {self.version} for cols {self.columns}"
            f" offset {self.offset} limit {self.limit} where='{self.where}'"
        )
        tbl = self._get_table()
        if self.range_blob_columns:
            from geneva.apply.blob_range import (
                RangeBlobReadUnsupportedError,
                normalize_blob_read_strategy,
                range_blob_batches,
            )

            try:
                yield from range_blob_batches(
                    table=tbl,
                    dataset_uri=self.uri,
                    columns=self.columns,
                    frag_id=self.frag_id,
                    offset=self.offset,
                    limit=self.limit,
                    version=self.version,
                    where=self.where,
                    with_row_address=self.with_row_address,
                    range_blob_columns=self.range_blob_columns,
                    selected_only_blob_columns=self.selected_only_blob_columns,
                    blob_read_buffer_size=self.blob_read_buffer_size,
                    storage_options=self.table_ref.storage_options,
                    batch_size=batch_size,
                    struct_blob_decomp=self.struct_blob_decomp,
                )
                return
            except RangeBlobReadUnsupportedError:
                if normalize_blob_read_strategy(self.blob_read_strategy) == "range":
                    raise
                _LOG.warning(
                    "Range blob read is unsupported for %s; falling back to legacy "
                    "blob reads",
                    self.uri,
                    exc_info=True,
                )

        query = tbl.search().enable_internal_api()  # type: ignore[attr-defined]

        if self.with_row_address:
            query = query.with_row_address()

        # Scoping to a single fragment id lets ``GenevaQueryBuilder`` push
        # ``offset``/``limit`` down to the Lance scanner instead of slicing
        # in Python. This avoids per-checkpoint whole-fragment re-reads on
        # the ``blob_handling="all_binary"`` (nested-blob) path.
        query = query.with_fragments(self.frag_id).offset(self.offset).limit(self.limit)
        query = query.with_where_as_bool_column()
        # Pin the read cache to this task's snapshot so commit cascades that
        # advance the table's current version don't invalidate it (GEN-574).
        query = query.with_read_version(self.version)

        # works with blobs but not filters
        if self.columns is not None:
            query = query.select(self.columns)
        if self.where is not None:
            query = query.where(self.where)

        # Currently lancedb reports the wrong type for the return value
        # of the to_batches method.  Remove pyright ignore when fixed.
        batches: pa.RecordBatchReader = query.to_batches(batch_size)  # pyright: ignore[reportAssignmentType]

        yield from batches

    @override
    def checkpoint_key(self) -> str:
        hasher = hashlib.md5()
        hasher.update(
            f"{self.uri}:{self.version}:{self.columns}:{self.frag_id}:{self.offset}:{self.limit}:{self.where}".encode(),
        )
        return hasher.hexdigest()

    @override
    def dest_frag_id(self) -> int:
        return self.frag_id

    @override
    def dest_offset(self) -> int:
        return self.offset

    @override
    def num_rows(self) -> int:
        if self.limit > 0:
            return self.limit
        if self.fragment_logical_rows is not None:
            return max(0, int(self.fragment_logical_rows) - int(self.offset))
        return self.limit

    @override
    def table_uri(self) -> str:
        return self.uri


@attrs.define(order=True)
class CopyTask(ReadTask):
    src: TableReference
    dst: TableReference
    # columns: list of names or dict mapping output names to expressions
    # e.g., ["id", "value"] or {"id": "id", "doubled": "value * 2"}
    columns: list[str] | dict[str, str]
    frag_id: int
    offset: int
    limit: int
    # Hash of source data files for input columns in this fragment.
    # Used in checkpoint keys.
    src_files_hash: str | None = None
    src_data_files: frozenset[str] | None = None
    fragment_physical_rows: int | None = None
    fragment_logical_rows: int | None = None
    _src_table: Table | None = attrs.field(
        default=None, init=False, repr=False, eq=False, order=False
    )
    _dst_table: Table | None = attrs.field(
        default=None, init=False, repr=False, eq=False, order=False
    )

    def bind_tables(
        self, *, src: Table | None = None, dst: Table | None = None
    ) -> None:
        if src is not None:
            self._src_table = src
        if dst is not None:
            self._dst_table = dst

    def clear_tables(self) -> None:
        self._src_table = None
        self._dst_table = None

    @property
    def version(self) -> int | None:
        """Return source version for checkpoint key generation."""
        return self.src.version

    @override
    def to_batches(
        self, *, batch_size=DEFAULT_CHECKPOINT_ROWS
    ) -> Iterator[pa.RecordBatch]:
        from geneva.query import open_read_dataset

        dst_tbl = self._dst_table if self._dst_table is not None else self.dst.open()

        # Read __source_row_id from the specific destination fragment using Lance API
        # This ensures we read from the correct fragment, not from the entire table
        dst_lance = open_read_dataset(dst_tbl)
        dst_fragment = dst_lance.get_fragment(self.frag_id)

        # Use dataset scanner with fragment restriction for efficient offset/limit
        # This only reads the requested slice, avoiding loading the entire fragment.
        # with_row_address yields each row's PHYSICAL destination address (_rowaddr);
        # we must write the projected values back at those physical slots, see below.
        scanner_kwargs: dict[str, Any] = {
            "columns": ["__source_row_id"],
            "offset": self.offset,
            "fragments": [dst_fragment],
            "with_row_address": True,
        }
        if self.limit > 0:
            scanner_kwargs["limit"] = self.limit
        scanner = dst_lance.scanner(**scanner_kwargs)
        row_ids_batch = scanner.to_table()
        row_ids = cast("list[int]", row_ids_batch["__source_row_id"].to_pylist())
        # Physical destination row addresses for the rows being reprojected. These
        # MUST come from the destination scan (which is deletion-vector aware), not
        # be synthesized from self.offset. When the dst fragment carries a deletion
        # vector -- an incremental refresh that just forward-deleted a stale row --
        # the logical scan offset no longer equals the physical slot. Synthesizing
        # `frag_id<<32 | (offset+i)` then writes each projected value into the wrong
        # physical slot and gap-fills the survivor's real slot with NULL (GEN-619).
        dst_row_addrs = row_ids_batch["_rowaddr"]

        # TODO: Add streaming take to lance
        src_tbl = self._src_table if self._src_table is not None else self.src.open()
        src_table_lance = open_read_dataset(src_tbl)
        _LOG.info(
            f"CopyTask: frag_id={self.frag_id}, offset={self.offset}, "
            f"limit={self.limit}, row_ids={row_ids}"
        )
        table = src_table_lance._take_rows(row_ids, columns=self.columns)
        _LOG.info(f"CopyTask: Fetched {table.num_rows} rows from source")

        # _take_rows preserves row_ids order, so dst_row_addrs[i] is the physical
        # address of table row i. Slice defensively if fewer rows came back.
        if table.num_rows != len(dst_row_addrs):
            dst_row_addrs = dst_row_addrs.slice(0, table.num_rows)
        table = table.add_column(table.num_columns, "_rowaddr", dst_row_addrs)

        max_chunksize = (
            int(batch_size)
            if batch_size and int(batch_size) > 0
            else max(1, int(table.num_rows))
        )
        batches = table.to_batches(max_chunksize=max_chunksize)

        yield from batches

    @override
    def checkpoint_key(self) -> str:
        hasher = hashlib.md5()
        hasher.update(
            f"CopyTask:{_table_ref_identity(self.src)}:{self.columns}:"
            f"{_table_ref_identity(self.dst)}:{self.frag_id}:"
            f"{self.offset}:{self.limit}".encode(),
        )
        return hasher.hexdigest()

    @override
    def dest_frag_id(self) -> int:
        return self.frag_id

    @override
    def dest_offset(self) -> int:
        return self.offset

    @override
    def num_rows(self) -> int:
        if self.limit > 0:
            return self.limit
        if self.fragment_logical_rows is not None:
            return max(0, int(self.fragment_logical_rows) - int(self.offset))
        return self.limit

    @override
    def table_uri(self) -> str:
        return self.src.table_uri or "$".join(self.src.table_id)


@attrs.define(order=True)
class SparseRangeTask(ReadTask):
    """A RANGE of fragments' worth of sparse row update work.

    The dispatchable unit for the distributed sparse path. The actor calls
    ``execute(udf)``, which runs ONE scan over the range (discovering its own
    matches -- so the driver runs no planning scan), applies the UDF, writes the
    range's replacement fragments in one ``write_fragments``, and builds a
    deletion vector per matched fragment, returning ``RangeSparseResult`` for the
    driver's ``SparseCommitManager`` to assemble into a ``LanceOperation.Update``.
    ``to_batches`` is intentionally unsupported.
    """

    uri: str
    table_ref: TableReference
    frag_ids: list[int]
    where: str
    output_column: str
    version: int | None = None
    batch_rows: int = 1024
    _table: Table | None = attrs.field(
        default=None, init=False, repr=False, eq=False, order=False
    )

    def bind_table(self, table: Table | None) -> None:
        self._table = table

    def clear_table(self) -> None:
        self._table = None

    def table_ref_for_read(self) -> TableReference:
        if self.version is not None and self.table_ref.version != self.version:
            return attrs.evolve(self.table_ref, version=self.version)
        return self.table_ref

    def _get_table(self) -> Table:
        if self._table is not None:
            return self._table
        return self.table_ref_for_read().open()

    @override
    def to_batches(
        self, *, batch_size=DEFAULT_CHECKPOINT_ROWS
    ) -> Iterator[pa.RecordBatch]:
        raise NotImplementedError(
            "SparseRangeTask runs via execute(); it does not stream batches "
            "through the read pipeline"
        )

    @override
    def checkpoint_key(self) -> str:
        hasher = hashlib.md5()
        hasher.update(
            f"sparse_rows_range:{self.uri}:{self.version}:{self.where}"
            f":{self.output_column}:{self.frag_ids[0] if self.frag_ids else -1}"
            f":{len(self.frag_ids)}".encode(),
        )
        return hasher.hexdigest()

    @override
    def dest_frag_id(self) -> int:
        return self.frag_ids[0] if self.frag_ids else 0

    @override
    def dest_offset(self) -> int:
        return 0

    @override
    def num_rows(self) -> int:
        return 0  # unknown until executed

    @override
    def table_uri(self) -> str:
        return self.uri


class MapTask(ABC):
    @abstractmethod
    def checkpoint_key(
        self,
        *,
        dataset_uri: str,
        start: int,
        end: int,
        dataset_version: int | str | None = None,
        frag_id: int | None = None,
        where: str | None = None,
        src_files_hash: str | None = None,
    ) -> str:
        """Return a unique key for the task"""

    @abstractmethod
    def checkpoint_prefix(
        self,
        *,
        dataset_uri: str,
        where: str | None = None,
        column: str | None = None,
        src_files_hash: str | None = None,
    ) -> str:
        """Return a stable prefix (no fragment/range) for logging/aggregation."""

    @abstractmethod
    def legacy_map_task_key(self, *, where: str | None = None) -> str:
        """Return legacy map task key (pre-range) for backwards compat."""

    @abstractmethod
    def input_columns(self) -> list[str] | None:
        """Return source columns used by this map task (if known)."""

    @abstractmethod
    def name(self) -> str:
        """Return a name to use for progress strings"""

    @abstractmethod
    def apply(self, batch: pa.RecordBatch) -> pa.RecordBatch:
        """Apply the map function to the input batch, returning the output batch"""

    @abstractmethod
    def output_schema(self) -> pa.Schema:
        """Return the output schema"""

    @abstractmethod
    def is_cuda(self) -> bool:
        """Return true if the task requires CUDA

        !!! warning "Deprecated"
            Use [`num_gpus`][num_gpus] instead to get the actual GPU requirement.
        """

    @abstractmethod
    def num_cpus(self) -> float | None:
        """Return the number of CPUs the task should use (None for default)"""

    @abstractmethod
    def num_gpus(self) -> float | None:
        """Return the number of GPUs the task should use (None for default)"""

    @abstractmethod
    def memory(self) -> int | None:
        """Return the amount of RAM the task should use (None for default)"""

    @abstractmethod
    def batch_size(self) -> int:
        """Return the batch size the task should use"""

    def has_preprocess(self) -> bool:
        """True if the UDF declares an optional CPU-side ``preprocess()`` step.

        Default: False. ``BackfillUDFTask`` overrides to inspect the
        wrapped UDF.
        """
        return False

    def preprocess_batch(self, batch: pa.RecordBatch) -> pa.RecordBatch:
        """Invoke the UDF's ``preprocess(batch) -> batch`` on a record batch.

        Default: raises ``NotImplementedError``. Callers should guard
        with ``has_preprocess()`` first.
        """
        raise NotImplementedError(
            f"{type(self).__name__} does not declare a preprocess() step"
        )

    def adaptive_checkpoint_bounds(self) -> tuple[int | None, int | None]:
        """Return adaptive checkpoint (min, max) bounds when supported."""
        return None, None

    def initial_checkpoint_size(self) -> int | None:
        """Return an explicit initial checkpoint size for adaptive sizing."""
        return None

    def checkpoint_interval_seconds(self) -> float | None:
        """Target seconds per adaptive checkpoint batch.

        When ``None``, the applier uses its built-in default (10 s).
        """
        return None

    def udf_version(self) -> str | None:
        """Return the UDF version hash for checkpoint comparison (optional)."""
        return None


@attrs.define(order=True)
class BackfillUDFTask(MapTask):
    udfs: dict[str, UDF] = (
        attrs.field()
    )  # TODO: use attrs to enforce stateful udfs are handled here

    # this is needed to differentiate a filtered task's checkpont keys
    # for backfill jobs
    where: str | None = attrs.field(default=None)

    # If set, this overrides the UDF-declared batch size. Used to respect
    # the backfill(batch_size=...) parameter from the job config.
    override_batch_size: int | None = attrs.field(default=None)
    explicit_checkpoint_size: bool = attrs.field(default=False)
    min_checkpoint_size: int | None = attrs.field(default=None)
    max_checkpoint_size: int | None = attrs.field(default=None)
    unpack_fields: tuple[UnpackedUDFField, ...] | None = attrs.field(default=None)
    checkpoint_column: str | None = attrs.field(default=None)
    # GEN-624: when True, a filtered task emits only the WHERE-matched rows
    # (sparse output) instead of carrying old values forward in-memory. The old
    # column is never read on the applier; the FragmentWriter fills the
    # unmatched gaps by streaming the old column at write time. This keeps
    # carry-forward blob backfills from materializing every unmatched row's old
    # blob on the applier.
    defer_carry_forward: bool = attrs.field(default=False)

    def __get_udf(self) -> tuple[str, UDF]:
        # TODO: Add support for multiple columns to add_columns operation
        if len(self.udfs) != 1:
            raise NotImplementedError("Add columns does not support multiple UDFs")
        col, udf = next(iter(self.udfs.items()))
        if not isinstance(udf, UDF):
            # stateful udf are Callable classes that need to be instantiated.
            udf = udf()
        return col, udf

    def _user_callable(self) -> Any:
        """Return the user's callable (class instance or function).

        For stateful UDFs wrapped via ``@udf`` on a class, ``udf.func``
        is an instance of the user's class — that's where custom
        methods like ``preprocess`` live. For function UDFs,
        ``udf.func`` is the function; attributes attached to the
        function itself are returned.
        """
        _, udf = self.__get_udf()
        return udf.func if getattr(udf, "func", None) is not None else udf

    def has_preprocess(self) -> bool:
        """True if the UDF declares an optional CPU-side ``preprocess()`` step.

        Used by the GPU pipelining BatchAppliers (collocated and
        distributed) to fan CPU decode / tokenization out to reader
        workers so the GPU actor stays on pure inference.

        Detection looks at the *class*, not the instance: stateful UDFs
        commonly assign callables to ``self.preprocess`` (e.g. an
        OpenCLIP image transform) and an instance-attribute check would
        misroute record batches through that callable.
        """
        try:
            user = self._user_callable()
        except Exception:
            return False
        cls = user if inspect.isclass(user) else type(user)
        return inspect.isfunction(getattr(cls, "preprocess", None))

    def preprocess_batch(self, batch: pa.RecordBatch) -> pa.RecordBatch:
        """Invoke the UDF's ``preprocess(batch) -> batch`` on a record batch.

        Raises AttributeError if the UDF has no preprocess step — callers
        should guard with ``has_preprocess()`` first.
        """
        user = self._user_callable()
        return user.preprocess(batch)

    def adaptive_checkpoint_bounds(self) -> tuple[int | None, int | None]:
        min_size = self.min_checkpoint_size
        max_size = self.max_checkpoint_size
        if min_size is None or max_size is None:
            _, udf = self.__get_udf()
            if min_size is None:
                min_size = getattr(udf, "min_checkpoint_size", None)
            if max_size is None:
                max_size = getattr(udf, "max_checkpoint_size", None)
        return min_size, max_size

    def initial_checkpoint_size(self) -> int | None:
        if self.override_batch_size is not None and self.explicit_checkpoint_size:
            return self.override_batch_size
        _, udf = self.__get_udf()
        if udf.checkpoint_size is not None:
            return udf.checkpoint_size
        if udf.batch_size is not None:
            return udf.batch_size
        return None

    def _output_fields(self, udf_col_name: str, udf: UDF) -> list[pa.Field]:
        if self.unpack_fields is None:
            return [pa.field(udf_col_name, udf.data_type, metadata=udf.field_metadata)]
        return [
            pa.field(
                field.output_column,
                field.field.type,
                nullable=field.field.nullable,
                metadata=field.field.metadata,
            )
            for field in self.unpack_fields
        ]

    def _output_column_names(self, udf_col_name: str) -> list[str]:
        if self.unpack_fields is None:
            return [udf_col_name]
        return [field.output_column for field in self.unpack_fields]

    def _checkpoint_column_label(self, udf_col_name: str) -> str:
        return self.checkpoint_column or udf_col_name

    def _split_result_arrays(
        self, udf_col_name: str, new_arr: pa.Array
    ) -> dict[str, pa.Array]:
        if self.unpack_fields is None:
            return {udf_col_name: new_arr}
        if not pa.types.is_struct(new_arr.type):
            raise TypeError(
                "Columns[T] multi-column UDF expected result to be a struct array, "
                f"got {new_arr.type}"
            )
        struct_arr = cast("pa.StructArray", new_arr)
        return {
            field.output_column: struct_arr.field(field.struct_field_name)
            for field in self.unpack_fields
        }

    @override
    def name(self) -> str:
        name, _ = self.__get_udf()
        return name

    @override
    def input_columns(self) -> list[str] | None:
        input_cols: set[str] = set()
        for udf in self.udfs.values():
            if not isinstance(udf, UDF):
                try:
                    udf = udf()
                except Exception:
                    return None
            cols = udf.input_columns
            if cols is None:
                return None
            input_cols.update(cols)
        if not input_cols:
            return None
        return list(input_cols)

    @override
    def checkpoint_key(
        self,
        *,
        dataset_uri: str,
        start: int,
        end: int,
        dataset_version: int | str | None = None,
        frag_id: int | None = None,
        where: str | None = None,
        src_files_hash: str | None = None,
    ) -> str:
        # 'where' is required in key to distinguish different partial backfills jobs
        # hashing it so that it cannot be used as a directory path attack vector
        col, udf = self.__get_udf()
        prefix = udf.checkpoint_prefix(
            column=self._checkpoint_column_label(col),
            dataset_uri=dataset_uri,
            where=where if where is not None else self.where,
            src_files_hash=src_files_hash,
        )
        return format_checkpoint_key(
            prefix,
            frag_id=frag_id if frag_id is not None else 0,
            start=start,
            end=end,
        )

    @override
    def checkpoint_prefix(
        self,
        *,
        dataset_uri: str,
        where: str | None = None,
        column: str | None = None,
        src_files_hash: str | None = None,
    ) -> str:
        col, udf = self.__get_udf()
        return udf.checkpoint_prefix(
            column=column or self._checkpoint_column_label(col),
            dataset_uri=dataset_uri,
            where=where if where is not None else self.where,
            src_files_hash=src_files_hash,
        )

    @override
    def legacy_map_task_key(self, *, where: str | None = None) -> str:
        col, udf = self.__get_udf()
        where_val = where if where is not None else self.where
        if where_val:
            hasher = hashlib.md5()
            hasher.update(where_val.encode())
            return f"{udf.checkpoint_key}:where={hasher.hexdigest()}"
        return udf.checkpoint_key

    @override
    def apply(self, batch: pa.RecordBatch | list[dict[str, Any]]) -> pa.RecordBatch:
        udf_col_name, udf = self.__get_udf()
        output_columns = self._output_column_names(udf_col_name)
        input_columns = udf.input_columns or []
        input_column_roots = {parse_field_path(col)[0] for col in input_columns}
        # Keep this in sync with _plan_read's selected_only_blob_columns.
        # The planner decides which input-only blob columns may be skipped on
        # filtered rows; this worker-side set removes carry-forward output
        # columns before invoking the UDF.
        carry_forward_set = set(output_columns) - input_column_roots

        if isinstance(batch, pa.RecordBatch):
            row_addr = batch["_rowaddr"]
            has_carry_forward_col = any(
                col in batch.schema.names for col in output_columns
            )
            has_backfill_selected = BACKFILL_SELECTED in batch.schema.names
        else:
            # might have blob_columns which needs _rowaddr
            row_addr = pa.array([x["_rowaddr"] for x in batch], type=pa.uint64())
            has_carry_forward_col = bool(batch) and any(
                col in batch[0] for col in output_columns
            )
            has_backfill_selected = bool(batch) and (BACKFILL_SELECTED in batch[0])

        # Drop carry-forward cols from what will be UDF arguments.
        if isinstance(batch, pa.RecordBatch):
            if carry_forward_set & set(batch.schema.names):
                # select all the other columns
                col_val_arrays = [
                    batch[col]
                    for col in batch.schema.names
                    if col not in carry_forward_set
                ]
                col_fields = [
                    batch.schema.field(col)
                    for col in batch.schema.names
                    if col not in carry_forward_set
                ]
                batch_for_udf = pa.RecordBatch.from_arrays(
                    col_val_arrays,
                    schema=pa.schema(col_fields),
                )
            else:
                batch_for_udf = batch
        else:
            # list-of-dicts case: just filter out the key
            batch_for_udf = [
                {k: v for k, v in row.items() if k not in carry_forward_set}
                for row in batch
            ]

        # execute the udf
        # Optimization: For RecordBatch and Array UDFs with filtering, only process
        # selected rows
        try:
            if (
                has_backfill_selected
                and isinstance(batch, pa.RecordBatch)
                and udf.arg_type in (UDFArgType.RECORD_BATCH, UDFArgType.ARRAY)
            ):
                # Get the selection mask
                mask = batch[BACKFILL_SELECTED]

                # Will be set to array data or None if no rows processed
                new_arr = None

                # Check if any rows are selected
                if any(mask.to_pylist()):
                    # Filter batch_for_udf to only include selected rows
                    filtered_batch_for_udf = pc.filter(batch_for_udf, mask)  # type: ignore[call-overload,arg-type]
                    _LOG.debug(
                        f"{udf.arg_type.name} UDF optimization: processing "
                        f"{filtered_batch_for_udf.num_rows} rows instead of "  # type: ignore[attr-defined]
                        f"{batch_for_udf.num_rows}"  # type: ignore[attr-defined]
                    )

                    # Execute UDF on filtered batch
                    filtered_new_arr = udf(filtered_batch_for_udf, use_applier=True)

                    # Expand results back to full batch size.
                    # Get indices of rows that passed the filter
                    indices_array = pa.array(range(batch.num_rows))
                    selected_indices = pc.filter(indices_array, mask)

                    if len(filtered_new_arr) > 0:
                        # Build complete list with values at correct positions.
                        # Use get_null_value_for_type to create structs with null
                        # fields instead of null structs for Lance 2.1 compatibility.
                        null_value = get_null_value_for_type(udf.data_type)  # type: ignore[arg-type]
                        result_pylist = [null_value] * batch.num_rows
                        for i, filtered_val in enumerate(filtered_new_arr):
                            original_idx = selected_indices[i].as_py()  # type: ignore[attr-defined]
                            result_pylist[original_idx] = filtered_val.as_py()

                        # Create array using pa.table() to ensure proper buffer
                        # structure for variable-width types (strings, binary,
                        # lists). pa.table() guarantees correct buffer allocation.
                        # See writer.py:_make_filler_batch() for details.
                        temp_table = pa.table(
                            {"_temp": result_pylist},
                            schema=pa.schema([("_temp", udf.data_type)]),
                        )  # type: ignore[arg-type,list-item]
                        new_arr = temp_table.column("_temp").combine_chunks()

                # If no rows were processed, return array of nulls
                if new_arr is None:
                    # Use make_null_array() for proper struct null handling in
                    # Lance 2.1 and proper buffer structure for variable-width types.
                    new_arr = make_null_array(batch.num_rows, udf.data_type)  # type: ignore[arg-type]
            else:
                # Original behavior for non-RecordBatch UDFs or when no filtering
                new_arr = udf(batch_for_udf, use_applier=True)
        except KeyError as e:
            # Column not found in batch
            if isinstance(batch_for_udf, pa.RecordBatch):
                available_cols = batch_for_udf.schema.names
            elif batch_for_udf and len(batch_for_udf) > 0:  # list[dict] with elements
                available_cols = list(batch_for_udf[0].keys())
            else:  # empty list
                available_cols = []
            raise KeyError(
                f"UDF '{udf.name}' failed: column {e} not found in batch. "
                f"Available columns: {available_cols}. "
                f"UDF expects input_columns: {udf.input_columns}. "
                f"This typically means the UDF's input_columns don't match "
                f"the table schema."
            ) from e
        except (pa.ArrowInvalid, pa.ArrowTypeError) as e:
            # Type mismatch or serialization error
            batch_schema = (
                batch_for_udf.schema
                if isinstance(batch_for_udf, pa.RecordBatch)
                else None
            )
            raise TypeError(
                f"UDF '{udf.name}' failed with type error: {e}. "
                f"Input batch schema: {batch_schema}. "
                f"UDF expects input_columns: {udf.input_columns}. "
                f"UDF output type: {udf.data_type}. "
                f"This often indicates a type mismatch (e.g., float32 vs float64) "
                f"between the table schema and UDF expectations."
            ) from e

        # now finalize the result.
        output_fields = self._output_fields(udf_col_name, udf)
        new_arrays = self._split_result_arrays(udf_col_name, new_arr)
        schema = pa.schema([*output_fields, pa.field("_rowaddr", pa.uint64())])

        if self.defer_carry_forward and has_backfill_selected:
            # GEN-624: emit only the WHERE-matched rows (sparse). The old column
            # was never read here, so unmatched rows carry no value; the
            # FragmentWriter fills those gaps by streaming the old column at
            # write time. Filtering to matched keeps the matched output (incl.
            # any blob bytes) and their _rowaddr.
            dense = pa.record_batch(
                [*[new_arrays[field.name] for field in output_fields], row_addr],
                schema=schema,
            )
            if isinstance(batch, pa.RecordBatch):
                mask = batch[BACKFILL_SELECTED]
            else:
                mask = pa.array(
                    [x.get(BACKFILL_SELECTED) for x in batch], type=pa.bool_()
                )
            return dense.filter(mask)

        if not has_carry_forward_col or not has_backfill_selected:
            schema = pa.schema([*output_fields, pa.field("_rowaddr", pa.uint64())])

            # no carry forward col? return the new
            return pa.record_batch(
                [*[new_arrays[field.name] for field in output_fields], row_addr],
                schema=schema,
            )

        # handle carry forward of old values
        merged_arrays = []
        if isinstance(batch, pa.RecordBatch):
            mask = batch[BACKFILL_SELECTED]
            for field in output_fields:
                if field.name in batch.schema.names:
                    orig_arr = batch[field.name]
                else:
                    orig_arr = make_null_array(batch.num_rows, field.type)
                merged_arrays.append(pc.if_else(mask, new_arrays[field.name], orig_arr))
        else:
            mask_vals = [x.get(BACKFILL_SELECTED) for x in batch]
            mask = pa.array(mask_vals, type=pa.bool_())
            for field in output_fields:
                # pa.array needs bytes, but blob cells are lazy BlobFile handles.
                orig_vals = [
                    v.readall() if isinstance(v, BlobFile) else v
                    for v in (x.get(field.name) for x in batch)
                ]
                orig_arr = pa.array(orig_vals, type=field.type)
                merged_arrays.append(pc.if_else(mask, new_arrays[field.name], orig_arr))

        schema = pa.schema([*output_fields, pa.field("_rowaddr", pa.uint64())])
        return pa.record_batch([*merged_arrays, row_addr], schema=schema)

    @override
    def output_schema(self) -> pa.Schema:
        name, udf = self.__get_udf()
        return pa.schema(
            [*self._output_fields(name, udf), pa.field("_rowaddr", pa.uint64())]
        )

    @override
    def is_cuda(self) -> bool:
        """Deprecated: Use num_gpus() instead."""
        _, udf = self.__get_udf()
        return bool(udf.num_gpus and udf.num_gpus > 0)

    @override
    def num_cpus(self) -> float | None:
        _, udf = self.__get_udf()
        return udf.num_cpus

    @override
    def num_gpus(self) -> float | None:
        _, udf = self.__get_udf()
        return udf.num_gpus

    @override
    def memory(self) -> int | None:
        _, udf = self.__get_udf()
        return udf.memory

    @override
    def batch_size(self) -> int:
        if self.override_batch_size is not None:
            return self.override_batch_size
        _, udf = self.__get_udf()
        return udf.batch_size or DEFAULT_CHECKPOINT_ROWS

    @override
    def udf_version(self) -> str | None:
        """Return the UDF version hash for checkpoint comparison."""
        _, udf = self.__get_udf()
        return udf.version


@attrs.define(order=True)
class CopyTableTask(MapTask):
    column_udfs: list[ExtractedTransform] = attrs.field()
    view_name: str = attrs.field()
    schema: pa.Schema = attrs.field()
    override_batch_size: int | None = attrs.field(default=None)

    @override
    def name(self) -> str:
        return self.view_name

    @override
    def input_columns(self) -> list[str] | None:
        if not self.column_udfs:
            return None
        input_cols: set[str] = set()
        for transform in self.column_udfs:
            cols = transform.udf.input_columns
            if cols is None:
                return None
            input_cols.update(cols)
        if not input_cols:
            return None
        return list(input_cols)

    @override
    def has_preprocess(self) -> bool:
        """True if any column UDF declares ``preprocess()``. Mirrors
        ``BackfillUDFTask`` so admission and ``setup_actor`` agree.
        ``run_ray_copy_table`` raises early on the
        pipelining=True + preprocess combo since the matview applier
        doesn't actually invoke preprocess() yet (GEN-472)."""
        return any(t.udf.has_preprocess() for t in self.column_udfs)

    @override
    def checkpoint_key(
        self,
        *,
        dataset_uri: str,
        start: int,
        end: int,
        dataset_version: int | str | None = None,
        frag_id: int | None = None,
        where: str | None = None,
        src_files_hash: str | None = None,
    ) -> str:
        column_label = (
            "+".join(sorted(transform.output_name for transform in self.column_udfs))
            if self.column_udfs
            else self.view_name
        )
        prefix = format_checkpoint_prefix(
            udf_name=self.view_name,
            udf_version="copy",
            column=column_label,
            where=where,
            dataset_uri=dataset_uri,
            src_files_hash=src_files_hash,
        )
        return format_checkpoint_key(
            prefix,
            frag_id=frag_id if frag_id is not None else 0,
            start=start,
            end=end,
        )

    @override
    def checkpoint_prefix(
        self,
        *,
        dataset_uri: str,
        where: str | None = None,
        column: str | None = None,
        src_files_hash: str | None = None,
    ) -> str:
        column_label = column
        if column_label is None:
            column_label = (
                "+".join(
                    sorted(transform.output_name for transform in self.column_udfs)
                )
                if self.column_udfs
                else self.view_name
            )
        return format_checkpoint_prefix(
            udf_name=self.view_name,
            udf_version="copy",
            column=column_label,
            where=where,
            dataset_uri=dataset_uri,
            src_files_hash=src_files_hash,
        )

    @override
    def legacy_map_task_key(self, *, where: str | None = None) -> str:
        return self.view_name

    @override
    def apply(self, batch: pa.RecordBatch) -> pa.RecordBatch:
        for transform in self.column_udfs:
            new_arr = transform.udf(batch)
            # Create field with metadata (e.g., lance-encoding:blob) to ensure
            # proper encoding when written to Lance files
            field = pa.field(
                transform.output_name,
                transform.udf.data_type,
                metadata=transform.udf.field_metadata,
            )
            batch = batch_add_column(batch, transform.output_index, field, new_arr)

        return batch

    @override
    def output_schema(self) -> pa.Schema:
        return self.schema

    @override
    def is_cuda(self) -> bool:
        """Deprecated: Use num_gpus() instead."""
        return any(
            column_udf.udf.num_gpus and column_udf.udf.num_gpus > 0
            for column_udf in self.column_udfs
        )

    @override
    def num_cpus(self) -> float | None:
        return max(
            (
                column_udf.udf.num_cpus
                for column_udf in self.column_udfs
                if column_udf.udf.num_cpus is not None
            ),
            default=None,
        )

    @override
    def num_gpus(self) -> float | None:
        return max(
            (
                column_udf.udf.num_gpus
                for column_udf in self.column_udfs
                if column_udf.udf.num_gpus is not None
            ),
            default=None,
        )

    @override
    def memory(self) -> int | None:
        return max(
            (
                column_udf.udf.memory
                for column_udf in self.column_udfs
                if column_udf.udf.memory is not None
            ),
            default=None,
        )

    @override
    def batch_size(self) -> int:
        if self.override_batch_size is not None:
            return self.override_batch_size
        if not self.column_udfs:
            return DEFAULT_CHECKPOINT_ROWS
        return min(
            column_udf.udf.batch_size or DEFAULT_CHECKPOINT_ROWS
            for column_udf in self.column_udfs
        )

    @override
    def initial_checkpoint_size(self) -> int | None:
        if self.override_batch_size is not None:
            if self.override_batch_size <= 0:
                return DEFAULT_CHECKPOINT_ROWS
            return self.override_batch_size
        return None
