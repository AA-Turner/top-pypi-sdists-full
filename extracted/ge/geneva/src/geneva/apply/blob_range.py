# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Range-based materialization for Lance blob columns.

The legacy Lance path materializes blobs one logical value at a time. This
module scans Lance blob descriptors, groups the underlying data-file byte
ranges by batch, and opens PyArrow ``NativeFile`` handles to fetch those ranges
directly.

The storage-option helpers are a translation layer between Lance/object_store
``storage_options`` accepted by Geneva and the PyArrow filesystem constructor
arguments needed for direct byte-range reads. When that translation cannot
preserve existing storage semantics, ``auto`` mode falls back to the legacy
blob path.
"""

from __future__ import annotations

import logging
import os
from array import array
from datetime import datetime, timezone
from itertools import pairwise
from typing import TYPE_CHECKING, Any, Literal, cast
from urllib.parse import ParseResult, urlparse, urlunparse

import attrs
import pyarrow as pa
from lance.blob import BlobFile

from geneva.transformer import BACKFILL_SELECTED
from geneva.utils.parse_rust_debug import extract_field_ids
from geneva.utils.schema import format_field_path, resolve_arrow_field
from geneva.utils.storage import (
    azure_credential_env,
    get_azure_storage_account,
    temporary_env,
)

_LOG = logging.getLogger(__name__)
_ROW_ID_COLUMN = "_rowid"

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence

    import lance
    import pyarrow.fs as pafs

BlobReadStrategy = Literal["auto", "legacy", "range"]

BLOB_ENCODING_METADATA_KEY = b"lance-encoding:blob"
BLOB_ENCODING_METADATA_VALUE = b"true"
BLOB_V2_EXTENSION_METADATA_KEY = b"ARROW:extension:name"
BLOB_V2_EXTENSION_NAME = b"lance.blob.v2"
DEFAULT_RANGE_BLOB_READ_BUFFER_SIZE = 128 * 1024 * 1024
RANGE_BLOB_READ_BUFFER_SIZE_ENV = "GENEVA_RANGE_BLOB_READ_BUFFER_SIZE"
_INTERNAL_ROW_ID_SCAN_BATCH_SIZE = 4096


def _close_iterator(iterator: object) -> None:
    close = getattr(iterator, "close", None)
    if callable(close):
        close()


class RangeBlobReadUnsupportedError(RuntimeError):
    """Raised when the range reader cannot preserve existing storage semantics."""


def normalize_blob_read_strategy(value: str | None) -> BlobReadStrategy:
    if value is None:
        return "auto"
    normalized = value.lower()
    if normalized not in ("auto", "legacy", "range"):
        raise ValueError(
            "blob_read_strategy must be one of 'auto', 'legacy', or 'range', "
            f"got {value!r}"
        )
    return cast("BlobReadStrategy", normalized)


def resolve_blob_read_buffer_size(value: int | None) -> int:
    if value is None:
        raw = os.environ.get(RANGE_BLOB_READ_BUFFER_SIZE_ENV)
        value = int(raw) if raw else DEFAULT_RANGE_BLOB_READ_BUFFER_SIZE
    value = int(value)
    if value <= 0:
        raise ValueError("blob_read_buffer_size must be positive")
    return value


def is_blob_field(field: pa.Field) -> bool:
    if isinstance(field.type, pa.ExtensionType):
        return field.type.extension_name == BLOB_V2_EXTENSION_NAME.decode("utf-8")
    metadata = field.metadata or {}
    if metadata.get(BLOB_V2_EXTENSION_METADATA_KEY) == BLOB_V2_EXTENSION_NAME:
        return True
    # Newer Lance tables write the namespaced metadata key. Older tables use
    # the generic lance-encoding marker, so range reads accept both forms.
    value = metadata.get(BLOB_ENCODING_METADATA_KEY)
    if value is not None:
        return value.lower() == BLOB_ENCODING_METADATA_VALUE
    legacy_value = metadata.get(b"lance-encoding")
    return bool(legacy_value and legacy_value.lower() == b"blob")


def resolve_field_path(schema: pa.Schema, name: str) -> pa.Field | None:
    """Resolve a possibly nested column path to a leaf ``pa.Field``.

    Returns ``None`` if the path cannot be resolved (e.g. unknown field or
    walks through a non-struct type).
    """

    return resolve_arrow_field(schema, name)


def blob_columns_in_schema(schema: pa.Schema, columns: Sequence[str]) -> frozenset[str]:
    """Return columns whose resolved field is a blob and can be range-read.

    Supports dotted struct paths (e.g. ``"image.image_bytes"``): when a UDF
    projects a nested blob via a dotted column reference, the Lance scanner
    returns it as a top-level descriptor column, so the range path can
    materialize it the same way as a top-level blob.
    """

    blob_columns: set[str] = set()
    for col in columns:
        field = resolve_field_path(schema, col)
        if field is not None and is_blob_field(field):
            blob_columns.add(col)
    return frozenset(blob_columns)


def nested_blob_paths(schema: pa.Schema, column: str) -> list[str]:
    """Return dotted paths of blob-marked leaf children under a struct column.

    When a UDF projects a whole struct (e.g. ``image``) that contains a nested
    blob leaf (``image.image_bytes [lance-encoding:blob]``), the top-level path
    does not resolve to a blob field, so the column would bypass the coalesced
    range reader. This returns the dotted leaf paths (``["image.image_bytes"]``)
    so the planner can route them through the range path and reassemble the
    struct afterward.

    Only one level of nesting is supported for v1: if ``column`` does not
    resolve to a struct, or any blob leaf is itself nested under a deeper
    struct, an empty list is returned so callers fall back to the legacy path.
    """

    field = resolve_field_path(schema, column)
    if field is None or not pa.types.is_struct(field.type):
        return []

    struct_type = cast("pa.StructType", field.type)
    blob_leaves: list[str] = []
    for i in range(struct_type.num_fields):
        child = struct_type.field(i)
        if pa.types.is_struct(child.type):
            # Deeper nesting is unsupported for v1; bail so the caller falls
            # back to the legacy blob path rather than risk a partial read.
            if _struct_contains_blob(child.type):
                return []
            continue
        if is_blob_field(child):
            blob_leaves.append(format_field_path([column, child.name]))
    return blob_leaves


def _struct_contains_blob(struct_type: pa.DataType) -> bool:
    """Return whether a struct (any depth) contains a blob-marked leaf."""
    if not pa.types.is_struct(struct_type):
        return False
    typed = cast("pa.StructType", struct_type)
    for i in range(typed.num_fields):
        child = typed.field(i)
        if pa.types.is_struct(child.type):
            if _struct_contains_blob(child.type):
                return True
        elif is_blob_field(child):
            return True
    return False


def _field_contains_blob(field: pa.Field) -> bool:
    """Recursively whether ``field`` or any nested child is a blob-marked leaf.

    Covers the field itself, struct children at any depth, and list/large-list/
    fixed-size-list element fields. Used to detect blob shapes the range reader
    cannot decompose (e.g. ``list<blob>``, structs nested 2+ levels deep) so the
    caller can fail loudly rather than fall back to the descriptor-yielding
    scanner.
    """
    if is_blob_field(field):
        return True
    dtype = field.type
    if pa.types.is_struct(dtype):
        return _struct_contains_blob(dtype)
    if (
        pa.types.is_list(dtype)
        or pa.types.is_large_list(dtype)
        or pa.types.is_fixed_size_list(dtype)
    ):
        return _field_contains_blob(cast("pa.ListType", dtype).value_field)
    return False


def column_has_blob_leaf(schema: pa.Schema, column: str) -> bool:
    """Return whether ``column`` resolves to a field containing any blob leaf.

    Unlike :func:`blob_columns_in_schema` (top-level / dotted-struct blobs that
    the range reader can materialize), this reports blob leaves at *any* depth or
    nesting, including shapes the range path does not support.
    """
    field = resolve_field_path(schema, column)
    return field is not None and _field_contains_blob(field)


@attrs.define(frozen=True)
class StructLeaf:
    """One leaf child of a decomposed struct column.

    ``dotted_path`` is the Lance projection name for the leaf; ``name`` is the
    child field name used when reassembling the struct; ``is_blob`` marks the
    blob leaf that the range reader materializes to ``large_binary``.
    """

    name: str
    dotted_path: str
    field: pa.Field
    is_blob: bool


@attrs.define(frozen=True)
class StructBlobDecomposition:
    """Plan to decompose a struct column into dotted leaves and reassemble it.

    The range reader scans the dotted leaf paths (Lance returns them as
    top-level columns), materializes the blob leaf, and this plan reassembles
    the original struct field at its source position for the carry-forward
    merge/write.
    """

    column: str
    field: pa.Field
    leaves: tuple[StructLeaf, ...]

    def leaf_paths(self) -> list[str]:
        return [leaf.dotted_path for leaf in self.leaves]

    def blob_paths(self) -> list[str]:
        return [leaf.dotted_path for leaf in self.leaves if leaf.is_blob]


def plan_struct_blob_decomposition(
    schema: pa.Schema, column: str
) -> StructBlobDecomposition | None:
    """Build a decomposition plan for a struct column with a nested blob leaf.

    Returns ``None`` when ``column`` is not a one-level struct containing a
    blob leaf, so the caller leaves the column on its existing read path.
    """

    blob_leaves = nested_blob_paths(schema, column)
    if not blob_leaves:
        return None

    field = resolve_field_path(schema, column)
    if field is None or not pa.types.is_struct(field.type):
        return None

    struct_type = cast("pa.StructType", field.type)
    blob_path_set = set(blob_leaves)
    leaves: list[StructLeaf] = []
    for i in range(struct_type.num_fields):
        child = struct_type.field(i)
        # Deeper nesting is rejected by nested_blob_paths; guard here too.
        if pa.types.is_struct(child.type):
            return None
        dotted = format_field_path([column, child.name])
        leaves.append(
            StructLeaf(
                name=child.name,
                dotted_path=dotted,
                field=child,
                is_blob=dotted in blob_path_set,
            )
        )
    return StructBlobDecomposition(column=column, field=field, leaves=tuple(leaves))


class InMemoryBlobFile(BlobFile):
    """A ``BlobFile`` backed by bytes already fetched by Geneva."""

    def __init__(self, data: bytes | bytearray | memoryview | None) -> None:
        self._data = bytes(data or b"")
        self._pos = 0
        self._closed = False

    def close(self) -> None:
        self._closed = True

    @property
    def closed(self) -> bool:
        return self._closed

    def read(self, size: int | None = -1) -> bytes:
        self._checkClosed()
        if size is None or size < 0:
            size = len(self._data) - self._pos
        end = min(len(self._data), self._pos + int(size))
        out = self._data[self._pos : end]
        self._pos = end
        return out

    def readall(self) -> bytes:
        return self.read(-1)

    def readinto(self, b: Any) -> int:
        data = self.read(len(b))
        b[: len(data)] = data
        return len(data)

    def seek(self, offset: int, whence: int = os.SEEK_SET) -> int:
        self._checkClosed()
        if whence == os.SEEK_SET:
            new_pos = int(offset)
        elif whence == os.SEEK_CUR:
            new_pos = self._pos + int(offset)
        elif whence == os.SEEK_END:
            new_pos = len(self._data) + int(offset)
        else:
            raise ValueError(f"invalid whence: {whence}")
        if new_pos < 0:
            raise ValueError(f"negative seek value {new_pos}")
        self._pos = new_pos
        return self._pos

    def tell(self) -> int:
        self._checkClosed()
        return self._pos

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return True

    def writable(self) -> bool:
        return False

    def size(self) -> int:
        return len(self._data)


class BufferBackedBlobFile(InMemoryBlobFile):
    """A ``BlobFile`` view over an existing buffer.

    The view avoids copying blob bytes when Geneva wraps Arrow-backed binary
    values for scalar ``BlobFile`` UDFs. ``read()`` still returns Python bytes,
    matching the ``BlobFile`` contract, but the allocation is delayed until the
    UDF actually reads the payload.

    Instances are file-like cursors and are not synchronized. Geneva creates a
    fresh view for each scalar UDF argument, so ``_pos`` is not shared across
    rows or workers; callers that share one instance across threads would need
    their own locking.
    """

    def __init__(
        self,
        data: bytes | bytearray | memoryview | pa.Buffer,
        *,
        offset: int = 0,
        size: int | None = None,
    ) -> None:
        view = memoryview(data)
        start = int(offset)
        if start < 0:
            raise ValueError(f"negative offset {start}")
        end = len(view) if size is None else start + int(size)
        if end < start:
            raise ValueError(f"negative size {size}")
        if end > len(view):
            raise ValueError(
                f"buffer view [{start}, {end}) is outside buffer of size {len(view)}"
            )
        self._view = view[start:end]
        self._pos = 0
        self._closed = False

    def read(self, size: int | None = -1) -> bytes:
        self._checkClosed()
        if size is None or size < 0:
            size = len(self._view) - self._pos
        end = min(len(self._view), self._pos + int(size))
        out = self._view[self._pos : end].tobytes()
        self._pos = end
        return out

    def readinto(self, b: Any) -> int:
        self._checkClosed()
        end = min(len(self._view), self._pos + len(b))
        chunk = self._view[self._pos : end]
        b[: len(chunk)] = chunk
        self._pos = end
        return len(chunk)

    def seek(self, offset: int, whence: int = os.SEEK_SET) -> int:
        self._checkClosed()
        if whence == os.SEEK_SET:
            new_pos = int(offset)
        elif whence == os.SEEK_CUR:
            new_pos = self._pos + int(offset)
        elif whence == os.SEEK_END:
            new_pos = len(self._view) + int(offset)
        else:
            raise ValueError(f"invalid whence: {whence}")
        if new_pos < 0:
            raise ValueError(f"negative seek value {new_pos}")
        self._pos = new_pos
        return self._pos

    def size(self) -> int:
        return len(self._view)


@attrs.define(frozen=True)
class _BlobColumnPlan:
    name: str
    field: pa.Field
    data_file_path: str


class _MissingBlobDataFileError(ValueError):
    pass


def _full_data_file_uri(dataset_uri: str, data_file_path: str) -> str:
    parsed = urlparse(dataset_uri)
    path = f"{parsed.path.rstrip('/')}/data/{data_file_path.lstrip('/')}"
    return urlunparse(parsed._replace(path=path))


def _uri_filesystem_path(parsed: ParseResult) -> str:
    if parsed.netloc:
        return f"{parsed.netloc}{parsed.path}"
    return parsed.path


def _storage_option(options: dict[str, Any], *keys: str) -> Any | None:
    for key in keys:
        value = options.get(key)
        if value is not None:
            return value
    return None


def _storage_bool(options: dict[str, Any], *keys: str) -> bool | None:
    value = _storage_option(options, *keys)
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _storage_float(options: dict[str, Any], *keys: str) -> float | None:
    value = _storage_option(options, *keys)
    if value is None:
        return None
    return float(value)


def _storage_datetime(options: dict[str, Any], *keys: str) -> datetime | None:
    value = _storage_option(options, *keys)
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, int | float):
        return datetime.fromtimestamp(value, tz=timezone.utc)
    text = str(value)
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def _with_storage_value(
    kwargs: dict[str, Any],
    arg_name: str,
    options: dict[str, Any],
    *keys: str,
) -> None:
    value = _storage_option(options, *keys)
    if value is not None:
        kwargs[arg_name] = value


def _with_storage_bool(
    kwargs: dict[str, Any],
    arg_name: str,
    options: dict[str, Any],
    *keys: str,
) -> None:
    value = _storage_bool(options, *keys)
    if value is not None:
        kwargs[arg_name] = value


def _with_storage_float(
    kwargs: dict[str, Any],
    arg_name: str,
    options: dict[str, Any],
    *keys: str,
) -> None:
    value = _storage_float(options, *keys)
    if value is not None:
        kwargs[arg_name] = value


def _s3_filesystem_from_uri(
    parsed: ParseResult, options: dict[str, Any]
) -> tuple[pafs.FileSystem, str]:
    import pyarrow.fs as fs

    kwargs: dict[str, Any] = {}
    _with_storage_value(
        kwargs,
        "access_key",
        options,
        "access_key",
        "aws_access_key_id",
        "aws_access_key",
    )
    _with_storage_value(
        kwargs,
        "secret_key",
        options,
        "secret_key",
        "aws_secret_access_key",
        "aws_secret_key",
    )
    _with_storage_value(
        kwargs, "session_token", options, "session_token", "aws_session_token"
    )
    _with_storage_value(kwargs, "region", options, "region", "aws_region")
    _with_storage_value(
        kwargs,
        "endpoint_override",
        options,
        "endpoint_override",
        "endpoint_url",
        "aws_endpoint",
        "aws_endpoint_url",
        "s3_endpoint",
    )
    _with_storage_value(kwargs, "role_arn", options, "role_arn", "aws_role_arn")
    _with_storage_value(kwargs, "session_name", options, "session_name")
    _with_storage_value(kwargs, "external_id", options, "external_id")
    _with_storage_value(kwargs, "scheme", options, "scheme")
    _with_storage_bool(kwargs, "anonymous", options, "anonymous")
    _with_storage_bool(
        kwargs, "force_virtual_addressing", options, "force_virtual_addressing"
    )
    _with_storage_float(kwargs, "request_timeout", options, "request_timeout")
    _with_storage_float(kwargs, "connect_timeout", options, "connect_timeout")

    return fs.S3FileSystem(**kwargs), _uri_filesystem_path(parsed)


def _gcs_filesystem_from_uri(
    parsed: ParseResult, options: dict[str, Any]
) -> tuple[pafs.FileSystem, str]:
    import pyarrow.fs as fs

    if _storage_option(options, "google_service_account_key", "service_account_key"):
        raise RangeBlobReadUnsupportedError(
            "GCS service-account-key storage_options cannot be represented in "
            "pyarrow.fs.GcsFileSystem; use blob_read_strategy='legacy' or "
            "ambient credentials"
        )

    kwargs: dict[str, Any] = {}
    _with_storage_bool(kwargs, "anonymous", options, "anonymous")
    _with_storage_value(
        kwargs, "project_id", options, "project_id", "google_project_id"
    )
    _with_storage_value(
        kwargs, "target_service_account", options, "target_service_account"
    )
    _with_storage_value(
        kwargs, "endpoint_override", options, "endpoint_override", "endpoint_url"
    )

    access_token = _storage_option(options, "access_token", "google_access_token")
    if access_token is not None:
        expiration = _storage_datetime(
            options,
            "credential_token_expiration",
            "google_credential_token_expiration",
        )
        if expiration is None:
            raise RangeBlobReadUnsupportedError(
                "GCS access_token storage_options require "
                "credential_token_expiration for pyarrow.fs.GcsFileSystem; "
                "use blob_read_strategy='legacy' or provide a token expiration"
            )
        kwargs["access_token"] = access_token
        kwargs["credential_token_expiration"] = expiration

    return fs.GcsFileSystem(**kwargs), _uri_filesystem_path(parsed)


def _azure_filesystem_from_uri(
    parsed: ParseResult, options: dict[str, Any]
) -> tuple[pafs.FileSystem, str]:
    import pyarrow.fs as fs

    try:
        account_name = (
            _storage_option(options, "account_name", "azure_storage_account_name")
            or get_azure_storage_account()
        )
    except ValueError as exc:
        raise RangeBlobReadUnsupportedError(
            "Azure account_name is required for pyarrow.fs.AzureFileSystem; "
            "use blob_read_strategy='legacy' or set account_name/"
            "AZURE_STORAGE_ACCOUNT_NAME"
        ) from exc
    kwargs: dict[str, Any] = {"account_name": account_name}
    account_key = _storage_option(options, "account_key", "azure_storage_account_key")
    if account_key is not None:
        kwargs["account_key"] = account_key
    _with_storage_value(
        kwargs, "blob_storage_authority", options, "blob_storage_authority"
    )
    _with_storage_value(
        kwargs, "dfs_storage_authority", options, "dfs_storage_authority"
    )
    _with_storage_value(kwargs, "blob_storage_scheme", options, "blob_storage_scheme")
    _with_storage_value(kwargs, "dfs_storage_scheme", options, "dfs_storage_scheme")
    sas_token = _storage_option(options, "sas_token", "azure_storage_sas_token")
    if sas_token is None and account_key is None:
        sas_token = parsed.query
    if sas_token:
        kwargs["sas_token"] = sas_token

    with temporary_env(azure_credential_env(options)):
        azure_fs = fs.AzureFileSystem(**kwargs)
    return azure_fs, _uri_filesystem_path(parsed)


def _filesystem_from_uri(
    uri: str, storage_options: dict[str, Any] | None
) -> tuple[pafs.FileSystem, str]:
    import pyarrow.fs as fs

    parsed = urlparse(uri)
    scheme = parsed.scheme.lower()
    options = storage_options or {}

    try:
        if not scheme:
            return fs.LocalFileSystem(), uri
        if scheme == "az":
            return _azure_filesystem_from_uri(parsed, options)
        if scheme in {"s3", "s3+ddb"}:
            return _s3_filesystem_from_uri(parsed, options)
        if scheme in {"gs", "gcs"}:
            return _gcs_filesystem_from_uri(parsed, options)

        if parsed.query and parsed.scheme:
            uri = urlunparse(parsed._replace(query="", fragment=""))
        return fs.FileSystem.from_uri(uri)
    except RangeBlobReadUnsupportedError:
        raise
    except Exception as exc:
        raise RangeBlobReadUnsupportedError(
            f"pyarrow cannot construct a filesystem for {parsed.scheme!r} URIs"
        ) from exc


def _get_blob_data_file_path(
    dataset: lance.LanceDataset,
    fragment: lance.LanceFragment,
    column: str,
) -> str:
    # Field ids come from Lance's internal schema representation. If parsing or
    # lookup fails, mark range reads unsupported so `auto` can fall back.
    try:
        field_ids = set(extract_field_ids(dataset.lance_schema, column))
    except ValueError as exc:
        raise RangeBlobReadUnsupportedError(
            f"Could not resolve field ids for blob column {column!r}"
        ) from exc
    if not field_ids:
        raise RangeBlobReadUnsupportedError(
            f"Could not resolve field ids for blob column {column!r}"
        )

    for data_file in fragment.data_files():
        if field_ids & set(data_file.fields):
            return data_file.path

    raise _MissingBlobDataFileError(
        f"Could not find data file for blob column {column!r} "
        f"in fragment {fragment.fragment_id}"
    )


def _blob_descriptor_arrays(array: pa.Array) -> tuple[pa.Array, pa.Array]:
    if not pa.types.is_struct(array.type):
        raise RangeBlobReadUnsupportedError(
            f"Expected Lance blob descriptor struct, got {array.type}"
        )
    struct_arr = cast("pa.StructArray", array)
    field_names = {field.name for field in array.type}
    if "position" not in field_names or "size" not in field_names:
        raise RangeBlobReadUnsupportedError(
            "Expected Lance blob descriptor struct with position and size fields, "
            f"got {array.type}"
        )
    return struct_arr.field("position"), struct_arr.field("size")


def _row_blob_ranges(
    batch: pa.RecordBatch,
    plans: Sequence[_BlobColumnPlan],
    *,
    selected_only_blob_columns: frozenset[str] | None = None,
) -> list[list[tuple[str, int, int]]]:
    selected_mask = (
        batch[BACKFILL_SELECTED] if BACKFILL_SELECTED in batch.schema.names else None
    )
    row_ranges: list[list[tuple[str, int, int]]] = [[] for _ in range(batch.num_rows)]
    for plan in plans:
        descriptors = batch.column(plan.name)
        positions, sizes = _blob_descriptor_arrays(descriptors)
        for idx, (descriptor_scalar, position_scalar, size_scalar) in enumerate(
            zip(descriptors, positions, sizes, strict=True)
        ):
            # Selected-only blob columns are UDF inputs that are not output
            # carry-forward columns. Rows filtered out by BACKFILL_SELECTED will
            # not call the UDF, so we can avoid fetching their input blobs.
            if (
                selected_mask is not None
                and selected_only_blob_columns is not None
                and plan.name in selected_only_blob_columns
                and not selected_mask[idx].as_py()
            ):
                continue
            if (
                not descriptor_scalar.is_valid
                or not position_scalar.is_valid
                or not size_scalar.is_valid
            ):
                continue
            size = int(size_scalar.as_py())
            if size <= 0:
                continue
            position = int(position_scalar.as_py())
            row_ranges[idx].append((plan.data_file_path, position, position + size))
    return row_ranges


def _coalesce_blob_ranges(
    ranges: Sequence[tuple[str, int, int]],
    byte_budget: int,
) -> dict[str, list[tuple[int, int]]]:
    """Group blob byte ranges by file and coalesce each file independently."""
    ranges_by_file: dict[str, list[tuple[int, int]]] = {}
    for data_file_path, start, end in ranges:
        if end <= start:
            continue
        ranges_by_file.setdefault(data_file_path, []).append((start, end))

    return {
        data_file_path: _coalesce_file_ranges(file_ranges, byte_budget)
        for data_file_path, file_ranges in ranges_by_file.items()
    }


def _coalesce_file_ranges(
    file_ranges: Sequence[tuple[int, int]],
    byte_budget: int,
) -> list[tuple[int, int]]:
    """Merge sorted ranges while each merged span stays within ``byte_budget``.

    Overlapping ranges are always merged. Non-overlapping ranges are merged only
    when the full span from the first start to the latest end fits the read
    budget, which avoids many small reads without creating oversized blob reads.
    """
    current_start: int | None = None
    current_end: int | None = None
    coalesced: list[tuple[int, int]] = []
    for start, end in sorted(file_ranges):
        if current_start is None or current_end is None:
            current_start, current_end = start, end
            continue

        merged_span = max(current_end, end) - current_start
        if start <= current_end or merged_span <= byte_budget:
            current_end = max(current_end, end)
        else:
            coalesced.append((current_start, current_end))
            current_start, current_end = start, end

    if current_start is not None and current_end is not None:
        coalesced.append((current_start, current_end))
    return coalesced


class _CoalescedRangeBudget:
    """Track coalesced read size incrementally for row-budget slicing.

    The common path receives ranges in file-offset order, so adding a range only
    touches the last coalesced range for that file. If a range arrives before the
    current tail, the file is rebuilt with the same sorting/coalescing algorithm
    as ``_coalesce_file_ranges`` while keeping the aggregate size up to date.
    """

    def __init__(self, byte_budget: int) -> None:
        self._byte_budget = byte_budget
        self._raw_ranges_by_file: dict[str, list[tuple[int, int]]] = {}
        self._coalesced_ranges_by_file: dict[str, list[tuple[int, int]]] = {}
        self._size_by_file: dict[str, int] = {}
        self.size = 0

    def add_ranges(self, ranges: Sequence[tuple[str, int, int]]) -> None:
        """Add one row's blob ranges to the tracked coalesced budget."""
        for data_file_path, start, end in ranges:
            self._add_range(data_file_path, start, end)

    def _add_range(self, data_file_path: str, start: int, end: int) -> None:
        """Add a range for one file using the fast ordered-append path when safe."""
        if end <= start:
            return

        raw_ranges = self._raw_ranges_by_file.setdefault(data_file_path, [])
        coalesced_ranges = self._coalesced_ranges_by_file.setdefault(data_file_path, [])
        ordered_append = not coalesced_ranges or start >= coalesced_ranges[-1][0]
        raw_ranges.append((start, end))
        if not ordered_append:
            self._rebuild_file_ranges(data_file_path, raw_ranges)
            return

        old_file_size = self._size_by_file.get(data_file_path, 0)
        if not coalesced_ranges:
            coalesced_ranges.append((start, end))
            delta = end - start
        else:
            current_start, current_end = coalesced_ranges[-1]
            merged_end = max(current_end, end)
            merged_span = merged_end - current_start
            if start <= current_end or merged_span <= self._byte_budget:
                coalesced_ranges[-1] = (current_start, merged_end)
                delta = (merged_end - current_start) - (current_end - current_start)
            else:
                coalesced_ranges.append((start, end))
                delta = end - start
        self._size_by_file[data_file_path] = old_file_size + delta
        self.size += delta

    def _rebuild_file_ranges(
        self,
        data_file_path: str,
        raw_ranges: Sequence[tuple[int, int]],
    ) -> None:
        """Recompute one file after an out-of-order range invalidates the tail."""
        old_file_size = self._size_by_file.get(data_file_path, 0)
        coalesced_ranges = _coalesce_file_ranges(raw_ranges, self._byte_budget)
        new_file_size = sum(end - start for start, end in coalesced_ranges)
        self._coalesced_ranges_by_file[data_file_path] = coalesced_ranges
        self._size_by_file[data_file_path] = new_file_size
        self.size += new_file_size - old_file_size


def _iter_row_budget_slices(
    row_ranges: Sequence[Sequence[tuple[str, int, int]]], byte_budget: int
) -> Iterator[slice]:
    """Yield row slices whose coalesced blob reads stay near ``byte_budget``.

    A single row can exceed the budget, but rows are never split because UDF
    inputs must stay row-complete.
    """

    if not row_ranges:
        return

    start = 0
    current_budget = _CoalescedRangeBudget(byte_budget)
    for idx, ranges in enumerate(row_ranges):
        current_budget.add_ranges(ranges)
        if idx > start and current_budget.size > byte_budget:
            yield slice(start, idx)
            start = idx
            current_budget = _CoalescedRangeBudget(byte_budget)
            current_budget.add_ranges(ranges)

    if start < len(row_ranges):
        yield slice(start, len(row_ranges))


def _read_data_file_ranges(
    files: dict[str, pa.NativeFile],
    ranges: dict[str, list[tuple[int, int]]],
) -> dict[str, list[tuple[int, pa.Buffer]]]:
    buffers: dict[str, list[tuple[int, pa.Buffer]]] = {}
    for data_file_path, file_ranges in ranges.items():
        file = files[data_file_path]
        for range_start, range_end in file_ranges:
            file.seek(range_start)
            buffers.setdefault(data_file_path, []).append(
                (range_start, file.read_buffer(range_end - range_start))
            )
    return buffers


def _find_blob_range_buffer(
    range_buffers: Sequence[tuple[int, pa.Buffer]],
    position: int,
    size: int,
) -> pa.Buffer:
    end = position + size
    for range_start, buffer in range_buffers:
        range_end = range_start + buffer.size
        if position >= range_start and end <= range_end:
            return buffer.slice(position - range_start, size)
    fetched = ", ".join(
        f"[{range_start}, {range_start + buffer.size})"
        for range_start, buffer in range_buffers
    )
    raise ValueError(
        f"blob descriptor range [{position}, {end}) is outside fetched ranges "
        f"{fetched or '<none>'}"
    )


def _read_blob_values(
    range_buffers: Sequence[tuple[int, pa.Buffer]],
    descriptors: pa.Array,
    *,
    selected_only: bool = False,
    selected_mask: pa.Array | None = None,
) -> pa.Array:
    """Materialize descriptor rows from range buffers and preserve row nulls."""

    positions, sizes = _blob_descriptor_arrays(descriptors)
    offsets = array("q", [0])
    validity = bytearray((len(descriptors) + 7) // 8)
    valid_count = 0
    value_sink = pa.BufferOutputStream()
    for descriptor_scalar, position_scalar, size_scalar in zip(
        descriptors, positions, sizes, strict=True
    ):
        idx = len(offsets) - 1
        # Keep selected-only input blobs null on rows the UDF will not process.
        # Output carry-forward columns are excluded from selected-only planning,
        # so this cannot erase the original output value for unselected rows.
        if (
            selected_only
            and selected_mask is not None
            and not selected_mask[idx].as_py()
        ):
            offsets.append(offsets[-1])
            continue
        is_null = (
            not descriptor_scalar.is_valid
            or not position_scalar.is_valid
            or not size_scalar.is_valid
        )
        if is_null:
            offsets.append(offsets[-1])
            continue
        position = int(position_scalar.as_py())
        size = int(size_scalar.as_py())
        if size < 0:
            raise ValueError(f"negative blob size {size}")
        if size:
            value_sink.write(_find_blob_range_buffer(range_buffers, position, size))
        offsets.append(offsets[-1] + size)
        # Arrow validity bitmaps use 1 for valid and 0 for null.
        validity[idx // 8] |= 1 << (idx % 8)
        valid_count += 1

    values_buffer = value_sink.getvalue()
    null_count = len(descriptors) - valid_count
    null_bitmap = None if null_count == 0 else pa.py_buffer(validity)
    return pa.Array.from_buffers(
        pa.large_binary(),
        len(descriptors),
        cast("list[pa.Buffer]", [null_bitmap, pa.py_buffer(offsets), values_buffer]),
        null_count=null_count,
    )


def _materialize_blob_slice(
    batch: pa.RecordBatch,
    plans: Sequence[_BlobColumnPlan],
    files: dict[str, pa.NativeFile],
    row_ranges: Sequence[Sequence[tuple[str, int, int]]],
    byte_budget: int,
    selected_only_blob_columns: frozenset[str] | None,
) -> pa.RecordBatch:
    flat_ranges = [r for ranges in row_ranges for r in ranges]
    data_file_ranges = _coalesce_blob_ranges(flat_ranges, byte_budget)
    data_file_buffers = _read_data_file_ranges(files, data_file_ranges)
    columns = list(batch.columns)
    fields = list(batch.schema)
    index_by_name = {name: idx for idx, name in enumerate(batch.schema.names)}
    selected_mask = (
        batch[BACKFILL_SELECTED] if BACKFILL_SELECTED in batch.schema.names else None
    )

    for plan in plans:
        idx = index_by_name[plan.name]
        is_selected_only = (
            selected_only_blob_columns is not None
            and plan.name in selected_only_blob_columns
        )
        columns[idx] = _read_blob_values(
            data_file_buffers.get(plan.data_file_path, []),
            columns[idx],
            selected_only=is_selected_only,
            selected_mask=selected_mask,
        )
        fields[idx] = pa.field(
            plan.name,
            pa.large_binary(),
            nullable=plan.field.nullable
            or (is_selected_only and selected_mask is not None),
            metadata=plan.field.metadata,
        )

    return pa.RecordBatch.from_arrays(columns, schema=pa.schema(fields))


def _expand_struct_decomp_columns(
    columns: Sequence[str],
    decomps: Sequence[StructBlobDecomposition],
) -> list[str]:
    """Replace each decomposed struct column with its dotted leaf paths.

    Non-decomposed columns (and metacols such as ``_rowaddr``) pass through
    unchanged and in place, so the scanner projection order is preserved.
    """

    decomp_by_column = {decomp.column: decomp for decomp in decomps}
    expanded: list[str] = []
    for col in columns:
        decomp = decomp_by_column.get(col)
        if decomp is None:
            expanded.append(col)
            continue
        expanded.extend(decomp.leaf_paths())
    return expanded


def _reassemble_struct_columns(
    batch: pa.RecordBatch,
    decomps: Sequence[StructBlobDecomposition],
    original_columns: Sequence[str],
) -> pa.RecordBatch:
    """Reassemble decomposed struct columns from their materialized leaves.

    Leaf columns (dotted paths) produced by the range reader are folded back
    into a single struct array placed at the struct column's original position.
    The blob leaf's field metadata (``lance-encoding:blob``) is preserved so the
    fragment writer re-blob-encodes it and the output schema matches the table.
    """

    if not decomps:
        return batch

    decomp_by_column = {decomp.column: decomp for decomp in decomps}
    name_to_idx = {name: idx for idx, name in enumerate(batch.schema.names)}

    out_columns: list[pa.Array] = []
    out_fields: list[pa.Field] = []
    consumed: set[str] = set()

    # Walk the pre-expansion column order so the struct lands at its original
    # position; leaf columns are consumed in place of their parent struct.
    for col in original_columns:
        decomp = decomp_by_column.get(col)
        if decomp is None:
            if col in consumed or col not in name_to_idx:
                continue
            idx = name_to_idx[col]
            out_columns.append(batch.column(idx))
            out_fields.append(batch.schema.field(idx))
            consumed.add(col)
            continue

        leaf_arrays: list[pa.Array] = []
        leaf_fields: list[pa.Field] = []
        for leaf in decomp.leaves:
            if leaf.dotted_path not in name_to_idx:
                raise RangeBlobReadUnsupportedError(
                    f"Decomposed leaf {leaf.dotted_path!r} missing from scan output"
                )
            leaf_idx = name_to_idx[leaf.dotted_path]
            leaf_arrays.append(batch.column(leaf_idx))
            # Preserve the original child field (including the blob marker) so
            # the writer re-blob-encodes the reassembled struct.
            leaf_fields.append(
                pa.field(
                    leaf.name,
                    batch.schema.field(leaf_idx).type,
                    nullable=leaf.field.nullable,
                    metadata=leaf.field.metadata,
                )
            )
            consumed.add(leaf.dotted_path)

        # Derive struct validity from the leaves: a row is null only when every
        # leaf is null (matches Lance's all_binary struct materialization).
        struct_validity = _struct_validity_from_leaves(leaf_arrays, batch.num_rows)
        struct_array = pa.StructArray.from_arrays(
            leaf_arrays,
            fields=leaf_fields,
            mask=struct_validity,
        )
        out_columns.append(struct_array)
        out_fields.append(
            pa.field(
                decomp.column,
                struct_array.type,
                nullable=decomp.field.nullable,
                metadata=decomp.field.metadata,
            )
        )

    # Append any leftover scan columns (e.g. metacols added after planning).
    for idx, name in enumerate(batch.schema.names):
        if name in consumed:
            continue
        out_columns.append(batch.column(idx))
        out_fields.append(batch.schema.field(idx))

    return pa.RecordBatch.from_arrays(out_columns, schema=pa.schema(out_fields))


def _struct_validity_from_leaves(
    leaf_arrays: Sequence[pa.Array],
    num_rows: int,
) -> pa.Array | None:
    """Return a boolean mask (True == null) where every leaf is null.

    Returns ``None`` when no row is fully null, leaving the struct non-null.

    Note: the dotted-leaf projection discards the original struct-level
    validity, so it is inferred from the leaves here. A valid struct whose
    leaves all happen to be null is therefore reassembled as a null struct.
    This matches Lance's ``all_binary`` materialization (the carry-forward
    equality baseline) and is safe for schemas where an all-null-leaf row never
    coincides with a valid struct (e.g. a present image always has bytes).
    """

    if not leaf_arrays:
        return None
    all_null = pa.array([True] * num_rows, type=pa.bool_())
    import pyarrow.compute as pc

    for leaf in leaf_arrays:
        all_null = pc.and_(all_null, pc.is_null(leaf))
    if pc.sum(pc.cast(all_null, pa.int64())).as_py() == 0:
        return None
    return all_null


def _materialize_missing_blob_columns(
    batch: pa.RecordBatch,
    missing_fields: dict[str, pa.Field],
) -> pa.RecordBatch:
    if not missing_fields:
        return batch

    columns = list(batch.columns)
    fields = list(batch.schema)
    index_by_name = {name: idx for idx, name in enumerate(batch.schema.names)}

    for name, field in missing_fields.items():
        if name not in index_by_name:
            continue
        idx = index_by_name[name]
        columns[idx] = pa.nulls(batch.num_rows, type=pa.large_binary())
        fields[idx] = pa.field(
            name,
            pa.large_binary(),
            nullable=field.nullable,
            metadata=field.metadata,
        )

    return pa.RecordBatch.from_arrays(columns, schema=pa.schema(fields))


def _row_id_filter(row_ids: Sequence[int]) -> str | None:
    if not row_ids:
        return None
    if len(row_ids) == 1:
        return f"{_ROW_ID_COLUMN} = {row_ids[0]}"
    if all(prev + 1 == curr for prev, curr in pairwise(row_ids)):
        return f"{_ROW_ID_COLUMN} >= {row_ids[0]} AND {_ROW_ID_COLUMN} <= {row_ids[-1]}"
    return f"{_ROW_ID_COLUMN} IN ({', '.join(str(row_id) for row_id in row_ids)})"


def _matching_row_ids_for_where(
    dataset: Any,
    fragment: Any,
    where: str,
    row_ids: Sequence[int],
) -> set[int]:
    row_id_filter = _row_id_filter(row_ids)
    if row_id_filter is None:
        return set()

    id_scan = dataset.scanner(
        columns=[_ROW_ID_COLUMN],
        with_row_id=True,
        filter=f"({where}) AND ({row_id_filter})",
        fragments=[fragment],
        batch_size=max(_INTERNAL_ROW_ID_SCAN_BATCH_SIZE, len(row_ids)),
    )
    matching: set[int] = set()
    id_batches = id_scan.to_batches()
    try:
        for id_batch in id_batches:
            matching.update(
                int(row_id)
                for row_id in id_batch[_ROW_ID_COLUMN].to_pylist()
                if row_id is not None
            )
    finally:
        _close_iterator(id_batches)
    return matching


def _add_backfill_selected_mask(
    batch: pa.RecordBatch,
    matching_row_ids: set[int],
) -> pa.RecordBatch:
    row_ids = batch[_ROW_ID_COLUMN].to_pylist()
    mask = pa.array(
        [row_id is not None and int(row_id) in matching_row_ids for row_id in row_ids],
        type=pa.bool_(),
    )
    field = pa.field(BACKFILL_SELECTED, pa.bool_())
    columns = list(batch.columns)
    fields = list(batch.schema)
    if BACKFILL_SELECTED in batch.schema.names:
        idx = batch.schema.get_field_index(BACKFILL_SELECTED)
        columns[idx] = mask
        fields[idx] = field
    else:
        columns.append(mask)
        fields.append(field)
    return pa.RecordBatch.from_arrays(columns, schema=pa.schema(fields))


def _drop_internal_row_id(
    batch: pa.RecordBatch,
    requested_columns: set[str],
) -> pa.RecordBatch:
    if _ROW_ID_COLUMN in requested_columns or _ROW_ID_COLUMN not in batch.schema.names:
        return batch
    return batch.remove_column(batch.schema.get_field_index(_ROW_ID_COLUMN))


def range_blob_batches(
    *,
    table: Any = None,
    dataset_uri: str,
    columns: Sequence[str],
    frag_id: int,
    offset: int,
    limit: int,
    version: int | None,
    where: str | None,
    with_row_address: bool,
    range_blob_columns: frozenset[str],
    selected_only_blob_columns: frozenset[str] | None,
    blob_read_buffer_size: int | None,
    storage_options: dict[str, str] | None,
    batch_size: int,
    struct_blob_decomp: Sequence[StructBlobDecomposition] | None = None,
    dataset: lance.LanceDataset | None = None,
) -> Iterator[pa.RecordBatch]:
    """Yield record batches with top-level blob columns materialized as bytes.

    This is the engine behind ``blob_read_strategy="range"``. It keeps one
    open file handle per Lance data file, batches blob byte ranges by the
    configured buffer budget, and returns batches ready for UDF argument
    conversion.

    When ``struct_blob_decomp`` is provided, each named struct column is read as
    its dotted leaf paths (so the nested blob comes back as a descriptor the
    range path materializes), then the struct is reassembled in-place so the
    UDF/merge/write see the original struct column.
    """

    # Expand decomposed struct columns to their dotted leaves for the scan and
    # blob-resolution loops; reassembly folds them back at the end.
    decomps = list(struct_blob_decomp or [])
    requested_struct_columns = list(columns)
    if decomps:
        columns = _expand_struct_decomp_columns(columns, decomps)

    # Callers may pass an already-open ``dataset`` (e.g. the deferred carry-
    # forward writer, which holds the fragment's source open at ``read_version``)
    # to reuse that handle. Otherwise route through the process-global read cache
    # (GEN-571) so a many-fragment backfill opens the source once per worker
    # instead of once per ScanTask. Pin the cache entry to the task's snapshot
    # ``version`` (not the table's current version) so commit cascades that
    # advance the table don't invalidate it (GEN-574). Imported lazily to avoid
    # an import cycle (geneva.query pulls in geneva.db).
    if dataset is None:
        if table is None:
            raise ValueError("range_blob_batches requires either table or dataset")
        from geneva.query import open_read_dataset

        dataset = open_read_dataset(table, version=version)
    resolved_dataset_uri = str(getattr(dataset, "uri", dataset_uri))

    fragment = dataset.get_fragment(frag_id)
    if fragment is None:
        return

    blob_plans = []
    missing_blob_fields: dict[str, pa.Field] = {}
    # Resolve the Lance data file that stores each requested blob column before
    # scanning row batches. Missing files are handled per-column below.
    for col in columns:
        if col not in range_blob_columns:
            continue
        field = resolve_field_path(dataset.schema, col)
        if field is None:
            raise RangeBlobReadUnsupportedError(
                f"Could not resolve blob column path {col!r} in schema"
            )
        try:
            data_file_path = _get_blob_data_file_path(dataset, fragment, col)
        except _MissingBlobDataFileError:
            _LOG.debug(
                "Blob column %s in fragment %s has no backing data file; "
                "leaving scanner output unmaterialized",
                col,
                frag_id,
            )
            missing_blob_fields[col] = field
            continue
        blob_plans.append(
            _BlobColumnPlan(
                name=col,
                field=field,
                data_file_path=data_file_path,
            )
        )

    byte_budget = resolve_blob_read_buffer_size(blob_read_buffer_size)
    needs_filter_mask = where is not None
    requested_columns = set(columns)

    scanner_kwargs: dict[str, Any] = {
        "columns": list(columns),
        "with_row_address": with_row_address,
        "fragments": [fragment],
        "offset": int(offset),
        "batch_size": int(batch_size) if batch_size and batch_size > 0 else None,
    }
    if needs_filter_mask:
        scanner_kwargs["with_row_id"] = True
    if limit > 0:
        scanner_kwargs["limit"] = int(limit)
    scanner_kwargs = {k: v for k, v in scanner_kwargs.items() if v is not None}

    data_files = {plan.data_file_path for plan in blob_plans}
    open_files = {}
    try:
        # Keep one input file open per data file instead of reopening per row.
        for data_file in data_files:
            full_uri = _full_data_file_uri(resolved_dataset_uri, data_file)
            file_system, path = _filesystem_from_uri(full_uri, storage_options)
            # Read-only blob fetch; no DataLake create/dir semantics.
            # hns-ok: open_input_file does not trigger the Azure dfs/HNS probe.
            open_files[data_file] = file_system.open_input_file(path)

        scanner = dataset.scanner(**scanner_kwargs)
        main_batches = scanner.to_batches()
        try:
            for batch in main_batches:
                batch = _materialize_missing_blob_columns(batch, missing_blob_fields)
                if needs_filter_mask:
                    assert where is not None
                    row_ids = [
                        int(row_id)
                        for row_id in batch[_ROW_ID_COLUMN].to_pylist()
                        if row_id is not None
                    ]
                    matching_row_ids = _matching_row_ids_for_where(
                        dataset,
                        fragment,
                        where,
                        row_ids,
                    )
                    batch = _add_backfill_selected_mask(batch, matching_row_ids)
                    batch = _drop_internal_row_id(batch, requested_columns)
                # Blob descriptor structs provide the byte spans each row needs.
                row_ranges = _row_blob_ranges(
                    batch,
                    blob_plans,
                    selected_only_blob_columns=selected_only_blob_columns,
                )
                for row_slice in _iter_row_budget_slices(row_ranges, byte_budget):
                    start = int(row_slice.start or 0)
                    stop = int(row_slice.stop or start)
                    sliced = batch.slice(start, stop - start)
                    materialized = _materialize_blob_slice(
                        sliced,
                        blob_plans,
                        open_files,
                        row_ranges[start:stop],
                        byte_budget,
                        selected_only_blob_columns,
                    )
                    if decomps:
                        materialized = _reassemble_struct_columns(
                            materialized, decomps, requested_struct_columns
                        )
                    yield materialized
        finally:
            _close_iterator(main_batches)
    finally:
        for file in open_files.values():
            file.close()
