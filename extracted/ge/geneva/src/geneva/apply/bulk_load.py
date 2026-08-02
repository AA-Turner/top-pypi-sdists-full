# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Bulk load column: join pre-computed external data into a Lance table by primary key.

This module provides `SourceIndex` (eager pk index with lazy value reads)
and `BulkLoadMapTask` (a `MapTask` that replaces UDF execution with a
pk-based lookup against the external source).
"""

import atexit
import contextlib
import hashlib
import logging
import os
import tempfile
import threading
import time
from collections.abc import Iterator
from datetime import timedelta
from typing import Any
from urllib.parse import unquote, urlparse

import attrs
import lance
import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
from typing_extensions import override

from geneva.apply.task import MapTask
from geneva.checkpoint_utils import (
    format_checkpoint_key,
    format_checkpoint_prefix,
    hash_source_files,
    hash_string,
)
from geneva.namespace_properties import is_sensitive_namespace_property

_LOG = logging.getLogger(__name__)

_VALID_ON_MISSING = {"carry", "null", "error"}
_ENV_LOCK = threading.RLock()


def _uri_scheme(path: str) -> str:
    return urlparse(path).scheme


def _file_uri_to_path(uri: str) -> str:
    parsed = urlparse(uri)
    return unquote(parsed.path)


def _uri_path(uri: str) -> str:
    parsed = urlparse(uri)
    return unquote(f"{parsed.netloc}{parsed.path}")


def _dataset_module() -> Any:
    try:
        import pyarrow.dataset as pads
    except ImportError as exc:
        raise RuntimeError(
            "bulk_load with Parquet/IPC sources requires pyarrow. "
            "Install Geneva with the bulk-load extra."
        ) from exc
    return pads


def _fs_module() -> Any:
    try:
        import pyarrow.fs as pa_fs
    except ImportError as exc:
        raise RuntimeError(
            "bulk_load with Parquet/IPC sources requires pyarrow filesystem support. "
            "Install Geneva with the bulk-load extra."
        ) from exc
    return pa_fs


def _storage_options_for_pyarrow(
    storage_options: dict[str, str] | None,
) -> dict[str, Any]:
    if not storage_options:
        return {}

    opts: dict[str, Any] = {}
    for key, value in storage_options.items():
        normalized_key = key.removeprefix("storage.")
        opts[normalized_key] = value

    aliases = {
        "aws_access_key_id": "access_key",
        "aws_secret_access_key": "secret_key",
        "aws_session_token": "session_token",
        "aws_region": "region",
        "aws_endpoint": "endpoint_override",
        "endpoint": "endpoint_override",
        "azure_storage_account_name": "account_name",
    }
    for src, dst in aliases.items():
        if src in opts and dst not in opts:
            opts[dst] = opts.pop(src)

    for key in (
        "anonymous",
        "background_writes",
        "allow_bucket_creation",
        "allow_bucket_deletion",
        "check_directory_existence_before_creation",
        "force_virtual_addressing",
    ):
        value = opts.get(key)
        if isinstance(value, str):
            lowered = value.lower()
            if lowered in {"true", "false"}:
                opts[key] = lowered == "true"

    for key in ("request_timeout", "connect_timeout"):
        value = opts.get(key)
        if isinstance(value, str):
            with contextlib.suppress(ValueError):
                opts[key] = float(value)

    value = opts.get("retry_time_limit")
    if isinstance(value, str | int | float):
        with contextlib.suppress(ValueError, TypeError):
            opts["retry_time_limit"] = timedelta(seconds=float(value))

    for key in ("load_frequency",):
        value = opts.get(key)
        if isinstance(value, str):
            with contextlib.suppress(ValueError):
                opts[key] = int(value)

    return opts


def _get_azure_storage_account(options: dict[str, Any]) -> str:
    import os

    account_name = (
        options.pop("account_name", None)
        or os.environ.get("AZURE_STORAGE_ACCOUNT_NAME")
        or os.environ.get("AZURE_STORAGE_ACCOUNT")
    )
    if not account_name:
        raise ValueError(
            "source_storage_options['account_name'] or AZURE_STORAGE_ACCOUNT_NAME "
            "must be set for az:// bulk_load sources."
        )
    return str(account_name)


def _filter_options(options: dict[str, Any], allowed: set[str]) -> dict[str, Any]:
    return {key: value for key, value in options.items() if key in allowed}


@contextlib.contextmanager
def _temporary_env(updates: dict[str, str]) -> Iterator[None]:
    with _ENV_LOCK:
        old_values = {key: os.environ.get(key) for key in updates}
        try:
            for key, value in updates.items():
                os.environ[key] = value
            yield
        finally:
            for key, old_value in old_values.items():
                if old_value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = old_value


def _azure_credential_env(options: dict[str, Any]) -> dict[str, str]:
    env_mapping = {
        "tenant_id": "AZURE_TENANT_ID",
        "client_id": "AZURE_CLIENT_ID",
        "client_secret": "AZURE_CLIENT_SECRET",
        "federated_token_file": "AZURE_FEDERATED_TOKEN_FILE",
    }
    env: dict[str, str] = {}
    for option_key, env_key in env_mapping.items():
        value = options.pop(option_key, None)
        if value is not None:
            env[env_key] = str(value)
    return env


def _remove_temp_file(path: str) -> None:
    with contextlib.suppress(OSError):
        os.unlink(path)


def _gcs_credential_env(options: dict[str, Any]) -> dict[str, str]:
    credentials_path = options.pop("json_credentials_path", None)
    credentials_json = options.pop("json_credentials", None)
    if credentials_path:
        return {"GOOGLE_APPLICATION_CREDENTIALS": str(credentials_path)}
    if credentials_json:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            suffix=".json",
            delete=False,
        ) as credentials_file:
            credentials_file.write(str(credentials_json))
            atexit.register(_remove_temp_file, credentials_file.name)
            return {"GOOGLE_APPLICATION_CREDENTIALS": credentials_file.name}
    return {}


def _arrow_filesystem_from_uri(
    uri: str,
    storage_options: dict[str, str] | None,
) -> tuple[Any, str]:
    pa_fs = _fs_module()
    scheme = _uri_scheme(uri)
    options = _storage_options_for_pyarrow(storage_options)

    if storage_options and scheme in {"abfs", "abfss"}:
        raise ValueError(
            "abfs:// and abfss:// bulk_load sources do not support "
            "source_storage_options. Use az:// sources when passing dedicated "
            "Azure storage options."
        )

    if scheme == "az":
        account_name = _get_azure_storage_account(options)
        azure_env = _azure_credential_env(options)
        with _temporary_env(azure_env):
            return (
                pa_fs.AzureFileSystem(
                    account_name,
                    **_filter_options(
                        options,
                        {
                            "account_key",
                            "blob_storage_authority",
                            "dfs_storage_authority",
                            "blob_storage_scheme",
                            "dfs_storage_scheme",
                            "sas_token",
                        },
                    ),
                ),
                _uri_path(uri),
            )

    if storage_options and scheme in {"s3", "s3a"}:
        return (
            pa_fs.S3FileSystem(
                **_filter_options(
                    options,
                    {
                        "access_key",
                        "secret_key",
                        "session_token",
                        "anonymous",
                        "region",
                        "request_timeout",
                        "connect_timeout",
                        "scheme",
                        "endpoint_override",
                        "background_writes",
                        "role_arn",
                        "session_name",
                        "external_id",
                        "load_frequency",
                        "proxy_options",
                        "allow_bucket_creation",
                        "allow_bucket_deletion",
                        "check_directory_existence_before_creation",
                        "force_virtual_addressing",
                    },
                ),
            ),
            _uri_path(uri),
        )

    if storage_options and scheme in {"gs", "gcs"}:
        gcs_env = _gcs_credential_env(options)
        with _temporary_env(gcs_env):
            return (
                pa_fs.GcsFileSystem(
                    **_filter_options(
                        options,
                        {
                            "anonymous",
                            "access_token",
                            "target_service_account",
                            "credential_token_expiration",
                            "default_bucket_location",
                            "scheme",
                            "endpoint_override",
                            "default_metadata",
                            "retry_time_limit",
                            "project_id",
                        },
                    ),
                ),
                _uri_path(uri),
            )

    return pa_fs.FileSystem.from_uri(uri)


def _open_arrow_dataset(
    source_uri: str | list[str],
    source_format: str,
    storage_options: dict[str, str] | None,
) -> Any:
    pads = _dataset_module()

    if isinstance(source_uri, str):
        filesystem, path = _arrow_filesystem_from_uri(source_uri, storage_options)
        return pads.dataset(
            path,
            format=source_format,  # type: ignore[arg-type]
            filesystem=filesystem,  # type: ignore[arg-type]
        )

    schemes = {_uri_scheme(path) for path in source_uri}
    non_empty_schemes = schemes - {""}
    if not non_empty_schemes:
        return pads.dataset(
            source_uri,
            format=source_format,  # type: ignore[arg-type]
        )

    if non_empty_schemes == {"file"} and schemes <= {"", "file"}:
        local_paths = [
            _file_uri_to_path(path) if _uri_scheme(path) == "file" else path
            for path in source_uri
        ]
        return pads.dataset(
            local_paths,
            format=source_format,  # type: ignore[arg-type]
        )

    if "" in schemes:
        raise ValueError(
            "source_uri list cannot mix local paths and remote URIs. "
            "Pass either all local paths or all remote URIs."
        )
    if len(non_empty_schemes) > 1:
        raise ValueError(
            f"source_uri list must use a single URI scheme, got "
            f"{sorted(non_empty_schemes)}"
        )

    filesystem, _ = _arrow_filesystem_from_uri(source_uri[0], storage_options)
    paths = [_uri_path(path) for path in source_uri]
    return pads.dataset(
        paths,
        format=source_format,  # type: ignore[arg-type]
        filesystem=filesystem,  # type: ignore[arg-type]
    )


def _source_storage_options_hash(
    storage_options: dict[str, str] | None,
) -> str | None:
    if not storage_options:
        return None

    stable_options: list[tuple[str, str]] = []
    for key, value in _storage_options_for_pyarrow(storage_options).items():
        if is_sensitive_namespace_property(key):
            continue
        stable_options.append((key, str(value)))

    if not stable_options:
        return None
    return hash_string(str(sorted(stable_options)))


@attrs.define
class SourceIndex:
    """In-memory primary-key index backed by an Arrow array.

    Holds only the pk column in memory; value columns are read lazily from the
    source dataset on each lookup (batched by source file for efficiency).

    The index is built once during planning and broadcast to workers via Ray's
    object store for zero-copy sharing.
    """

    # --- persisted across serialization ---
    pk_column: str
    value_columns: list[str] = attrs.field()
    # Either a single URI/path or a list of file paths.  Lance only accepts
    # a single URI; Parquet/IPC accept either.
    source_uri: str | list[str] = attrs.field()
    source_format: str = attrs.field()  # "parquet", "lance", "ipc"

    # Arrow arrays holding [pk_value, row_index_in_source] for non-null pk rows.
    # Stored as flat pa.Array (not ChunkedArray) to avoid per-batch
    # combine_chunks() overhead in lookup().
    _pk_array: pa.Array = attrs.field(repr=False, alias="pk_array")
    _row_idx_array: pa.Array = attrs.field(repr=False, alias="row_idx_array")

    # Schema of value columns in the source (for null-fill when no match).
    _value_schema: pa.Schema = attrs.field(repr=False, alias="value_schema")

    # Snapshot of source identity so that _open_source() re-opens the exact
    # same data that was scanned during build(), even on a different machine.
    # Lance: pinned dataset version.  Parquet/IPC: explicit file list.
    _source_version: int | None = attrs.field(
        default=None, repr=False, alias="source_version"
    )
    _source_files: list[str] | None = attrs.field(
        default=None, repr=False, alias="source_files"
    )

    # Stable hash of the external source file identity (paths for Parquet/IPC,
    # pinned version for Lance).  Used as src_files_hash in checkpoint keys so
    # that bulk_load checkpoints are keyed by the SOURCE data — not the
    # destination fragment data files (which change on schema evolution and
    # partial commits).  This makes checkpoints reusable across job retries.
    _source_identity_hash: str = attrs.field(
        default="", repr=False, alias="source_identity_hash"
    )
    source_storage_options: dict[str, str] | None = attrs.field(
        default=None, repr=False
    )

    # Number of null pks excluded from the index.
    null_pk_count: int = attrs.field(default=0)

    # Cached dataset handle — avoids re-opening the source on every
    # read_values() call.  The per-batch _open_source() overhead was the
    # primary driver of the adaptive batch-sizing death spiral.
    _cached_source_ds: Any = attrs.field(default=None, init=False, repr=False, eq=False)

    @classmethod
    def build(
        cls,
        source_uri: str | list[str],
        source_format: str,
        pk_column: str,
        value_columns: list[str],
        source_storage_options: dict[str, str] | None = None,
        storage_options: dict[str, str] | None = None,
    ) -> "SourceIndex":
        """Scan the source dataset and build an in-memory pk index.

        Parameters
        ----------
        source_uri
            URI of the source dataset (local path or cloud), or a list of
            file paths.  Passing a list of paths enables file-level
            partitioning for the A-multi pattern: each pass reads only its
            assigned files.  Lance sources must be a single URI.
        source_format
            One of ``"parquet"``, ``"lance"``, ``"ipc"``.
        pk_column
            Name of the primary-key column (must exist in source).
        value_columns
            Names of value columns to load from source.
        source_storage_options
            Storage options used only for opening the external source. These
            are independent from the destination table storage options.
        storage_options
            Backward-compatible alias for ``source_storage_options``.

        Raises
        ------
        ValueError
            If pk_column or value_columns are missing, source contains
            duplicate primary keys, or a list of paths is passed for a
            Lance source.
        """
        if source_storage_options is not None and storage_options is not None:
            raise ValueError(
                "pass either source_storage_options or storage_options, not both"
            )
        if source_storage_options is None:
            source_storage_options = storage_options

        # --- validate source_uri shape ---
        if isinstance(source_uri, list):
            if not source_uri:
                raise ValueError("source_uri list must not be empty")
            if source_format == "lance":
                raise ValueError(
                    "Lance sources do not support a list of paths. "
                    "Pass a single dataset URI instead."
                )

        # --- open source dataset and snapshot its identity ---
        t0 = time.perf_counter()
        _LOG.info(
            "SourceIndex: opening source dataset (format=%s, uri=%s)",
            source_format,
            source_uri if isinstance(source_uri, str) else f"[{len(source_uri)} files]",
        )
        source_version: int | None = None
        source_files: list[str] | None = None
        if source_format == "lance":
            # Validation above guarantees non-list for lance.
            assert isinstance(source_uri, str)
            lance_kwargs: dict[str, Any] = {}
            if source_storage_options is not None:
                lance_kwargs["storage_options"] = source_storage_options
            ds: Any = lance.dataset(source_uri, **lance_kwargs)
            source_version = ds.version
        else:
            ds = _open_arrow_dataset(
                source_uri,
                source_format,
                source_storage_options,
            )
            source_files = ds.files

        src_schema = ds.schema

        # --- validate columns exist ---
        missing = {pk_column} - set(src_schema.names)
        if missing:
            raise ValueError(
                f"Primary key column '{pk_column}' not found in source schema. "
                f"Available columns: {src_schema.names}"
            )
        missing_vals = set(value_columns) - set(src_schema.names)
        if missing_vals:
            raise ValueError(
                f"Value column(s) {sorted(missing_vals)} not found in source "
                f"schema. Available columns: {src_schema.names}"
            )

        # --- scan pk column only (+ row index) ---
        t_open = time.perf_counter()
        n_source_files = len(source_files) if source_files else "unknown"
        _LOG.info(
            "SourceIndex: source opened in %.1fs (%s files), "
            "scanning pk column '%s'...",
            t_open - t0,
            n_source_files,
            pk_column,
        )
        pk_table = ds.to_table(columns=[pk_column])
        pk_col = pk_table.column(pk_column)
        n_total = len(pk_col)

        t_scan = time.perf_counter()
        _LOG.info(
            "SourceIndex: pk scan complete in %.1fs — %d rows",
            t_scan - t_open,
            n_total,
        )

        # row indices [0..n) — use numpy for zero-copy into Arrow
        all_indices = pa.array(np.arange(n_total, dtype=np.int64))

        # filter out null pks
        valid_mask = pc.is_valid(pk_col)
        null_count = pc.sum(pc.invert(valid_mask)).as_py()
        if null_count:
            _LOG.warning(
                "Source dataset has %d rows with NULL primary key '%s'; "
                "these rows will be excluded from the bulk load index.",
                null_count,
                pk_column,
            )
            pk_col = pc.filter(pk_col, valid_mask)
            all_indices = pc.filter(all_indices, valid_mask)

        # Flatten to pa.Array to avoid per-batch combine_chunks() in lookup().
        if isinstance(pk_col, pa.ChunkedArray):
            pk_col = pk_col.combine_chunks()
        if isinstance(all_indices, pa.ChunkedArray):
            all_indices = all_indices.combine_chunks()

        # check for duplicate pks
        _LOG.info(
            "SourceIndex: checking %d pks for duplicates...",
            len(pk_col),
        )
        t_dedup_start = time.perf_counter()
        n_unique = pc.count_distinct(pk_col).as_py()
        if n_unique < len(pk_col):
            n_dupes = len(pk_col) - n_unique
            raise ValueError(
                f"Source dataset contains {n_dupes} duplicate primary key "
                f"values in column '{pk_column}'. Deduplicate the source "
                "before loading."
            )
        t_dedup = time.perf_counter()
        _LOG.info(
            "SourceIndex: duplicate check passed in %.1fs",
            t_dedup - t_dedup_start,
        )

        value_schema = pa.schema([src_schema.field(c) for c in value_columns])

        # Compute a stable identity hash for the source data.  This is used
        # as src_files_hash in checkpoint keys so that bulk_load checkpoints
        # are keyed by the external SOURCE — not the destination fragment
        # files (which change on schema evolution and partial commits).
        storage_hash = _source_storage_options_hash(source_storage_options)
        if source_format == "lance":
            source_identity_hash = hash_string(str(source_version))
        else:
            source_identity_hash = hash_source_files(source_files)
        if storage_hash is not None:
            source_identity_hash = hash_string(f"{source_identity_hash}:{storage_hash}")

        t_total = time.perf_counter() - t0
        _LOG.info(
            "SourceIndex: built in %.1fs — %d pk entries (%d nulls excluded), "
            "%d value columns, source=%s",
            t_total,
            len(pk_col),
            null_count,
            len(value_columns),
            source_uri if isinstance(source_uri, str) else f"[{len(source_uri)} files]",
        )

        return cls(
            pk_column=pk_column,
            value_columns=value_columns,
            source_uri=source_uri,
            source_format=source_format,
            pk_array=pk_col,
            row_idx_array=all_indices,
            value_schema=value_schema,
            source_version=source_version,
            source_files=source_files,
            source_identity_hash=source_identity_hash,
            source_storage_options=source_storage_options,
            null_pk_count=null_count,
        )

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def lookup(self, dest_pks: pa.Array | pa.ChunkedArray) -> tuple[pa.Array, pa.Array]:
        """Find source row indices for the given destination pk values.

        Returns a tuple of ``(source_indices, matched)``:

        - **source_indices**: int64 array aligned with *dest_pks*. Each
          element is the row index in the source dataset if the pk
          matched, or **null** if the pk has no match in the source.
        - **matched**: boolean array aligned with *dest_pks*. ``True``
          where the pk was found in the source, ``False`` otherwise.
          This is needed to distinguish "source value is legitimately
          NULL" from "pk not found" during the carry-semantics merge.
        """
        # pc.index_in returns index into value_set for each element of values,
        # or null if not found.
        idx_in_pk = pc.index_in(dest_pks, self._pk_array)

        # matched mask: True where pk was found (index is non-null)
        matched = pc.is_valid(idx_in_pk)

        # Map from "index in pk_array" → "row index in source dataset"
        return self._row_idx_array.take(idx_in_pk), matched

    def read_values(
        self,
        source_indices: pa.Array,
    ) -> dict[str, pa.Array]:
        """Read value columns from the source dataset for the given row indices.

        *source_indices* is an int64 array (with nulls for unmatched rows)
        as returned by :meth:`lookup`.  Returns a dict mapping column name
        to a pa.Array aligned with *source_indices*.  Unmatched positions
        are null.
        """
        valid_mask = pc.is_valid(source_indices)
        n = len(source_indices)

        if not pc.any(valid_mask).as_py():
            # No matches at all — return all-null arrays.  The caller
            # (BulkLoadMapTask.apply) logs a WARNING with pk-range
            # context, so we just return the nulls here.
            return {
                col: pa.nulls(n, type=self._value_schema.field(col).type)
                for col in self.value_columns
            }

        # Collect the non-null source row indices.
        non_null_indices = pc.filter(source_indices, valid_mask)

        # Read from source dataset (lazy — only these rows).
        # Lance's take() expects a Python list of ints, while PyArrow's
        # Dataset.take() accepts Arrow arrays directly.
        ds = self._open_source()
        if self.source_format == "lance":
            matched_table = ds.take(
                non_null_indices.to_pylist(), columns=self.value_columns
            )
        else:
            matched_table = ds.take(non_null_indices, columns=self.value_columns)

        # Defensive: source take() should return exactly len(non_null_indices)
        # rows. If the source returns a short result (silent read error,
        # eviction mid-read, data corruption), fail loudly here rather than
        # silently checkpointing wrong merged output.  Without this check, a
        # short result propagates to the downstream scatter and may either
        # raise an IndexError deep in pa.compute or — in edge cases —
        # produce silently-wrong committed data files.
        if len(matched_table) != len(non_null_indices):
            raise RuntimeError(
                f"BulkLoad source read returned {len(matched_table)} rows "
                f"for {len(non_null_indices)} requested indices from "
                f"{self.source_uri!r}; source read may have failed silently"
            )

        # Scatter matched values back into full-size arrays.
        # Build an index array: for each position in the output, if the
        # position is valid, point to the next element in the matched result.
        cumsum = pc.cumulative_sum(valid_mask.cast(pa.int64()), skip_nulls=True)
        scatter_idx = pc.if_else(valid_mask, pc.subtract(cumsum, 1), None)

        result: dict[str, pa.Array] = {}
        for col_name in self.value_columns:
            matched_col = matched_table.column(col_name)
            if isinstance(matched_col, pa.ChunkedArray):
                matched_col = matched_col.combine_chunks()
            result[col_name] = matched_col.take(scatter_idx)

        return result

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _open_source(self) -> Any:
        """Open (or return cached) source dataset handle.

        The dataset handle is cached after the first call to avoid
        re-scanning metadata and re-resolving the filesystem on every
        ``read_values()`` invocation.  This eliminates the fixed
        per-batch overhead that was a primary driver of the adaptive
        batch-sizing death spiral.
        """
        if self._cached_source_ds is not None:
            return self._cached_source_ds

        ds = self._open_source_uncached()
        self._cached_source_ds = ds
        return ds

    def _open_source_uncached(self) -> Any:
        if self.source_format == "lance":
            assert isinstance(self.source_uri, str)
            lance_kwargs: dict[str, Any] = {"version": self._source_version}
            if self.source_storage_options is not None:
                lance_kwargs["storage_options"] = self.source_storage_options
            return lance.dataset(self.source_uri, **lance_kwargs)

        if self._source_files is not None:
            if isinstance(self.source_uri, str):
                if _uri_scheme(self.source_uri):
                    filesystem, _ = _arrow_filesystem_from_uri(
                        self.source_uri,
                        self.source_storage_options,
                    )
                    source = (
                        self._source_files[0]
                        if len(self._source_files) == 1
                        else self._source_files
                    )
                    return _dataset_module().dataset(
                        source,
                        format=self.source_format,  # type: ignore[arg-type]
                        filesystem=filesystem,  # type: ignore[arg-type]
                    )
                source = self._source_files
            else:
                source = (
                    self.source_uri
                    if any(_uri_scheme(path) for path in self.source_uri)
                    else self._source_files
                )
            return _open_arrow_dataset(
                source,
                self.source_format,
                self.source_storage_options,
            )
        return _open_arrow_dataset(
            self.source_uri,
            self.source_format,
            self.source_storage_options,
        )


# ======================================================================
# BulkLoadMapTask
# ======================================================================


@attrs.define(order=True)
class BulkLoadMapTask(MapTask):
    """MapTask that performs pk-based lookup from an external source dataset.

    Replaces UDF execution in the backfill pipeline.  The worker reads
    destination rows (pk + _rowaddr + existing value columns), looks up
    matching source values via the ``SourceIndex``, and merges them.
    """

    source_index: SourceIndex = attrs.field(eq=False, order=False)
    pk_column: str = attrs.field()
    value_columns: list[str] = attrs.field()
    _output_schema_val: pa.Schema = attrs.field(
        repr=False, eq=False, order=False, alias="output_schema_val"
    )
    on_missing: str = attrs.field(default="carry")  # "carry" | "null" | "error"
    _batch_size_val: int = attrs.field(default=1000, alias="batch_size_val")
    _min_checkpoint_size: int | None = attrs.field(
        default=None, alias="min_checkpoint_size"
    )
    _max_checkpoint_size: int | None = attrs.field(
        default=None, alias="max_checkpoint_size"
    )
    _checkpoint_interval_seconds: float | None = attrs.field(
        default=None, alias="checkpoint_interval_seconds"
    )
    _loader_cpus: float | None = attrs.field(default=None, alias="loader_cpus")
    _loader_memory: int | None = attrs.field(default=None, alias="loader_memory")

    # Hash of source URI + columns for checkpoint keys.
    _source_hash: str = attrs.field(init=False, repr=False, eq=False, order=False)

    def __attrs_post_init__(self) -> None:
        # The hash drives the checkpoint key prefix, so any input that would
        # change which rows or values a task produces must be folded in here.
        # Otherwise a re-run with a changed argument would silently replay
        # stale checkpoints from the prior run.
        hasher = hashlib.md5()
        src = self.source_index.source_uri
        if isinstance(src, list):
            # Hash sorted list contents so list order doesn't affect identity.
            hasher.update(b"src=")
            hasher.update(str(sorted(src)).encode())
        else:
            hasher.update(b"src=")
            hasher.update(src.encode())
        hasher.update(b"|fmt=")
        hasher.update(self.source_index.source_format.encode())
        source_storage_hash = _source_storage_options_hash(
            self.source_index.source_storage_options
        )
        if source_storage_hash is not None:
            hasher.update(b"|source_storage=")
            hasher.update(source_storage_hash.encode())
        hasher.update(b"|pk=")
        hasher.update(self.pk_column.encode())
        hasher.update(b"|cols=")
        hasher.update(str(sorted(self.value_columns)).encode())
        self._source_hash = hasher.hexdigest()[:12]

    # ------------------------------------------------------------------
    # MapTask interface
    # ------------------------------------------------------------------

    @override
    def name(self) -> str:
        return "bulkload"

    @override
    def input_columns(self) -> list[str] | None:
        return [self.pk_column] + list(self.value_columns)

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
        prefix = self.checkpoint_prefix(
            dataset_uri=dataset_uri,
            where=where,
            src_files_hash=src_files_hash,
        )
        return format_checkpoint_key(
            prefix,
            frag_id=frag_id if frag_id is not None else 0,
            start=start,
            end=end,
        )

    def source_files_hash(self) -> str:
        """Return the source-file-based identity hash.

        Unlike UDF backfill (which hashes destination fragment data files),
        bulk_load hashes the EXTERNAL source file paths.  This makes
        checkpoint keys stable across destination schema evolution and
        partial commits, enabling resume across job retries.
        """
        return self.source_index._source_identity_hash

    @override
    def checkpoint_prefix(
        self,
        *,
        dataset_uri: str,
        where: str | None = None,
        column: str | None = None,
        src_files_hash: str | None = None,
    ) -> str:
        col_label = column or "+".join(sorted(self.value_columns))
        # Always use the source-file-based hash rather than the
        # caller-provided dest-fragment-based hash.  This is the key
        # difference from UDF backfill: bulk_load's inputs come from an
        # external source, so the checkpoint key should track SOURCE
        # identity, not destination state.
        return format_checkpoint_prefix(
            udf_name="bulkload",
            udf_version=self._source_hash,
            column=col_label,
            where=where,
            dataset_uri=dataset_uri,
            src_files_hash=self.source_files_hash(),
        )

    @override
    def legacy_map_task_key(self, *, where: str | None = None) -> str:
        return f"bulkload:{self._source_hash}"

    @override
    def apply(self, batch: pa.RecordBatch) -> pa.RecordBatch:
        """Look up source values by pk and merge with existing destination values."""
        dest_pks = batch.column(self.pk_column)
        row_addr = batch.column("_rowaddr")
        n_rows = len(dest_pks)

        # 1. Lookup: find source row indices + matched mask for each dest pk.
        source_indices, matched = self.source_index.lookup(dest_pks)
        n_matched = pc.sum(matched).as_py() or 0  # type: ignore[union-attr]
        n_unmatched = n_rows - n_matched

        # 2. Read source values (lazy — reads from source files on demand).
        source_values = self.source_index.read_values(source_indices)

        # Log per-batch match stats at DEBUG normally, WARNING when
        # suspiciously few matches (helps diagnose silent data loss).
        if n_matched == 0 and n_rows > 0:
            _LOG.warning(
                "BulkLoad.apply: batch of %d rows had 0 source matches "
                "(pk range %s..%s); all values will be carry/null",
                n_rows,
                dest_pks[0].as_py(),
                dest_pks[-1].as_py(),
            )
        else:
            _LOG.debug(
                "BulkLoad.apply: %d/%d rows matched source (%d unmatched → carry/null)",
                n_matched,
                n_rows,
                n_unmatched,
            )

        # 3. Merge: source wins where present; carry existing where absent.
        merged_arrays: list[pa.Array] = []
        fields: list[pa.Field] = []

        for col_name in self.value_columns:
            source_col = source_values[col_name]
            field = self._output_schema_val.field(col_name)
            fields.append(field)

            if self.on_missing == "null":
                # Source values only — unmatched rows become null.
                merged_arrays.append(source_col)
            elif self.on_missing == "error":
                # Check matched mask, not is_null(source_col) — a matched
                # row with a legitimately NULL source value is NOT a miss.
                n_unmatched_pks = pc.sum(pc.invert(matched)).as_py() or 0  # type: ignore[union-attr]
                if n_unmatched_pks > 0:
                    raise ValueError(
                        f"on_missing='error': {n_unmatched_pks} destination "
                        f"rows have no match in source for column "
                        f"'{col_name}'."
                    )
                merged_arrays.append(source_col)
            else:
                # "carry" (default) — use the matched mask to decide
                # whether to take the source value or carry existing.
                # This correctly handles source NULLs: a matched row with
                # a NULL source value writes NULL (not carry), while an
                # unmatched row carries existing.
                if col_name in batch.schema.names:
                    existing_col = batch.column(col_name)
                    merged = pc.if_else(matched, source_col, existing_col)
                    merged_arrays.append(merged)
                else:
                    # Column not in batch (shouldn't happen since we request it,
                    # but handle gracefully).
                    merged_arrays.append(source_col)

        # Build output: [value_col_1, ..., value_col_n, _rowaddr]
        fields.append(pa.field("_rowaddr", pa.uint64()))
        merged_arrays.append(row_addr)

        schema = pa.schema(fields)
        return pa.record_batch(merged_arrays, schema=schema)

    @override
    def output_schema(self) -> pa.Schema:
        return self._output_schema_val

    @override
    def is_cuda(self) -> bool:
        return False

    @override
    def num_cpus(self) -> float | None:
        return self._loader_cpus

    @override
    def num_gpus(self) -> float | None:
        return None

    @override
    def memory(self) -> int | None:
        return self._loader_memory

    @override
    def batch_size(self) -> int:
        return self._batch_size_val

    @override
    def adaptive_checkpoint_bounds(self) -> tuple[int | None, int | None]:
        return self._min_checkpoint_size, self._max_checkpoint_size

    @override
    def initial_checkpoint_size(self) -> int | None:
        return self._batch_size_val

    @override
    def checkpoint_interval_seconds(self) -> float | None:
        return self._checkpoint_interval_seconds
