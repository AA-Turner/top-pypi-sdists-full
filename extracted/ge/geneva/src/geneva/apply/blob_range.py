# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Lance blob materialization helpers."""

from __future__ import annotations

import logging
import os
import re
from array import array
from itertools import pairwise
from typing import TYPE_CHECKING, Any, Literal, cast

import attrs
import pyarrow as pa
import pyarrow.compute as pc
from lance.blob import BlobFile

from geneva.transformer import BACKFILL_SELECTED
from geneva.utils.parse_rust_debug import extract_field_ids
from geneva.utils.schema import (
    canonical_field_path,
    field_path_covers,
    format_field_path,
    parse_field_path,
    resolve_arrow_field,
)

_LOG = logging.getLogger(__name__)
_ROW_ID_COLUMN = "_rowid"
_ROW_ADDRESS_COLUMN = "_rowaddr"
_BLOB_KIND_EXTERNAL = 3

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence

    import lance
    from lance.file import LanceFileSession

BlobReadStrategy = Literal["auto", "legacy", "range"]

BLOB_ENCODING_METADATA_KEY = b"lance-encoding:blob"
BLOB_ENCODING_METADATA_VALUE = b"true"
BLOB_V2_EXTENSION_METADATA_KEY = b"ARROW:extension:name"
BLOB_V2_EXTENSION_METADATA_PAYLOAD_KEY = b"ARROW:extension:metadata"
BLOB_V2_EXTENSION_NAME = b"lance.blob.v2"
DEFAULT_RANGE_BLOB_READ_BUFFER_SIZE = 128 * 1024 * 1024
# Deprecated raw env var. The blob read buffer now reads the JobConfig knob
# applier_blob_buffer_bytes, set via env JOB__APPLIER_BLOB_BUFFER_BYTES -- one
# attribute sizing both this actual read buffer and the memory estimate. This
# env survives only as that JobConfig field's default, whose factory
# (_default_applier_blob_buffer_bytes) warns once when this env is the source.
# TODO: drop this raw env once operators have moved to the JobConfig knob.
RANGE_BLOB_READ_BUFFER_SIZE_ENV = "GENEVA_RANGE_BLOB_READ_BUFFER_SIZE"
_INTERNAL_ROW_ID_SCAN_BATCH_SIZE = 4096


def _close_iterator(iterator: object) -> None:
    close = getattr(iterator, "close", None)
    if callable(close):
        close()


class RangeBlobReadUnsupportedError(RuntimeError):
    """Raised when the range reader cannot preserve existing storage semantics."""


class ExternalBlobUnsupportedError(RuntimeError):
    """Raised when a blob v2 descriptor points at an external URI."""


class UnsupportedBlobLayoutError(ValueError):
    """Blob-in-list or a blob nested deeper than one struct."""


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
        # Default to the JobConfig knob (JOB__APPLIER_BLOB_BUFFER_BYTES), which
        # also sizes the memory estimate -- one attribute for both. Its default
        # still mirrors the deprecated raw env, and the JobConfig factory warns
        # once when that env is the source.
        from geneva.jobs.config import JobConfig

        value = JobConfig.get().applier_blob_buffer_bytes
    value = int(value)
    if value <= 0:
        raise ValueError("blob_read_buffer_size must be positive")
    return value


def is_blob_v2_field(field: pa.Field) -> bool:
    if isinstance(field.type, pa.ExtensionType):
        return field.type.extension_name == BLOB_V2_EXTENSION_NAME.decode("utf-8")
    metadata = field.metadata or {}
    return metadata.get(BLOB_V2_EXTENSION_METADATA_KEY) == BLOB_V2_EXTENSION_NAME


def is_blob_field(field: pa.Field) -> bool:
    if is_blob_v2_field(field):
        return True
    # Newer Lance tables write the namespaced metadata key. Older tables use
    # the generic lance-encoding marker, so range reads accept both forms.
    metadata = field.metadata or {}
    value = metadata.get(BLOB_ENCODING_METADATA_KEY)
    if value is not None:
        return value.lower() == BLOB_ENCODING_METADATA_VALUE
    legacy_value = metadata.get(b"lance-encoding")
    return bool(legacy_value and legacy_value.lower() == b"blob")


def _as_utf8_bytes(value: bytes | str) -> bytes:
    return value if isinstance(value, bytes) else str(value).encode("utf-8")


def _is_legacy_blob_metadata_entry(key: bytes | str, value: bytes | str) -> bool:
    """True only for the v1 blob marker, not the rest of ``lance-encoding:*``."""
    key_bytes = _as_utf8_bytes(key)
    if key_bytes == BLOB_ENCODING_METADATA_KEY:
        return True
    return key_bytes == b"lance-encoding" and _as_utf8_bytes(value).lower() == b"blob"


def without_legacy_blob_metadata(
    metadata: dict[Any, Any] | None,
) -> dict[Any, Any]:
    if not metadata:
        return {}
    return {
        k: v for k, v in metadata.items() if not _is_legacy_blob_metadata_entry(k, v)
    }


def _without_blob_v2_extension(
    metadata: dict[bytes, bytes] | None,
) -> dict[bytes, bytes] | None:
    if not metadata:
        return None
    cleaned = dict(metadata)
    cleaned.pop(BLOB_V2_EXTENSION_METADATA_KEY, None)
    cleaned.pop(BLOB_V2_EXTENSION_METADATA_PAYLOAD_KEY, None)
    return cleaned or None


def rewrite_blob_fields_for_storage(
    field: pa.Field, *, use_blob_v2: bool, _depth: int = 0
) -> pa.Field:
    """Rewrite legacy blob fields for v2 storage."""
    if not use_blob_v2:
        return field

    from lance.blob import BlobType

    dtype = field.type
    if is_blob_v2_field(field) or (
        is_blob_field(field)
        and (pa.types.is_binary(dtype) or pa.types.is_large_binary(dtype))
    ):
        if _depth > 1:
            raise UnsupportedBlobLayoutError(
                f"Blob field {field.name!r} is nested deeper than one struct. "
                "Geneva supports top-level blobs or one-level leaves such as "
                "image.image_bytes"
            )
        metadata = without_legacy_blob_metadata(field.metadata)
        if is_blob_v2_field(field):
            return pa.field(
                field.name,
                dtype,
                nullable=field.nullable,
                metadata=metadata or None,
            )
        metadata[BLOB_V2_EXTENSION_METADATA_KEY] = BLOB_V2_EXTENSION_NAME
        return pa.field(
            field.name,
            BlobType(),
            nullable=field.nullable,
            metadata=metadata or None,
        )
    if pa.types.is_struct(dtype):
        struct_type = cast("pa.StructType", dtype)
        children = [
            rewrite_blob_fields_for_storage(
                struct_type.field(i), use_blob_v2=True, _depth=_depth + 1
            )
            for i in range(struct_type.num_fields)
        ]
        return pa.field(
            field.name,
            pa.struct(children),
            nullable=field.nullable,
            metadata=field.metadata,
        )
    if (
        pa.types.is_list(dtype)
        or pa.types.is_large_list(dtype)
        or pa.types.is_fixed_size_list(dtype)
    ):
        list_type = cast("pa.ListType", dtype)
        if _field_contains_blob(list_type.value_field):
            raise UnsupportedBlobLayoutError(
                f"Blob-in-list field {field.name!r} is not supported"
            )
        return field
    return field


def resolve_field_path(schema: pa.Schema, name: str) -> pa.Field | None:
    """Resolve a possibly nested column path to a leaf ``pa.Field``.

    Returns ``None`` if the path cannot be resolved (e.g. unknown field or
    walks through a non-struct type).
    """

    return resolve_arrow_field(schema, name)


def blob_v2_field_paths(schema: pa.Schema) -> frozenset[str]:
    paths: list[str] = []

    def walk(field: pa.Field, prefix: list[str], depth: int) -> None:
        segments = [*prefix, field.name]
        name = format_field_path(segments)
        if is_blob_v2_field(field):
            if depth <= 1:
                paths.append(name)
            return
        dtype = field.type
        if pa.types.is_struct(dtype) and depth < 1:
            struct_type = cast("pa.StructType", dtype)
            for idx in range(struct_type.num_fields):
                walk(struct_type.field(idx), segments, depth + 1)

    for field in schema:
        walk(field, [], 0)
    return frozenset(paths)


def blob_v2_paths_for_inputs(
    schema: pa.Schema, input_columns: Sequence[str] | None
) -> frozenset[str]:
    """Select v2 leaves for inputs. None selects all; [] selects none.

    A struct name includes its nested leaves.
    """
    all_v2 = blob_v2_field_paths(schema)
    if not all_v2:
        return frozenset()
    if input_columns is None:
        return all_v2
    input_leaf_paths: set[str] = set()
    for input_column in input_columns:
        if input_column in schema.names:
            canonical = format_field_path([input_column])
        else:
            canonical = canonical_field_path(schema, input_column)
        input_leaf_paths.update(
            path for path in all_v2 if field_path_covers(canonical, path)
        )
    return frozenset(input_leaf_paths)


def referenced_v2_paths(where: str | None, schema: pa.Schema) -> frozenset[str]:
    if not where:
        return frozenset()
    return frozenset(
        path
        for path in blob_v2_field_paths(schema)
        if re.search(
            rf"(?<![\w.]){re.escape(path)}(?![\w])",
            where,
            re.IGNORECASE,
        )
    )


def where_references_blob_v2(where: str | None, schema: pa.Schema) -> bool:
    return bool(referenced_v2_paths(where, schema))


def empty_blob_v2_predicate(path: str) -> str:
    """Match Arrow-null and size-0 v2 descriptors."""
    return f"({path} IS NULL OR {path}.size = 0)"


def expand_exact_blob_v2_null_filter(
    where: str | None, schema: pa.Schema
) -> str | None:
    """Rewrite a whole-filter ``IS NULL`` to the resume empty predicate."""
    if where is None:
        return None
    compact = " ".join(where.split())
    lowered = compact.lower()
    for path in blob_v2_field_paths(schema):
        if lowered == f"{path} is null".lower():
            return empty_blob_v2_predicate(path)
        if lowered == f"{path} is not null".lower():
            return f"{path}.size > 0"
    return where


def default_resume_predicate(column: str, field: pa.Field) -> str:
    """Filter Geneva generates when the caller did not pass ``where``."""
    if is_blob_v2_field(field):
        return empty_blob_v2_predicate(column)
    return f"{column} IS NULL"


def has_nested_v1_blob(fields: Sequence[pa.Field]) -> bool:
    """Return whether the schema has a nested v1 blob."""

    def walk(field: pa.Field, depth: int) -> bool:
        if is_blob_v2_field(field):
            return False
        if depth > 0 and is_blob_field(field):
            return True
        if pa.types.is_struct(field.type):
            return any(
                walk(field.type.field(i), depth + 1)
                for i in range(field.type.num_fields)
            )
        return False

    return any(walk(field, 0) for field in fields)


def field_with_blob_v2_as_bytes(field: pa.Field, *, _depth: int = 0) -> pa.Field:
    if is_blob_v2_field(field):
        metadata = _without_blob_v2_extension(field.metadata)
        return pa.field(
            field.name,
            pa.large_binary(),
            nullable=True,
            metadata=metadata,
        )
    dtype = field.type
    if pa.types.is_struct(dtype) and _depth < 1:
        struct_type = cast("pa.StructType", dtype)
        children = [
            field_with_blob_v2_as_bytes(struct_type.field(i), _depth=_depth + 1)
            for i in range(struct_type.num_fields)
        ]
        return pa.field(
            field.name,
            pa.struct(children),
            nullable=field.nullable,
            metadata=field.metadata,
        )
    return field


def encode_blob_v2_storage_array(field: pa.Field, array: pa.Array) -> pa.Array:
    if is_blob_v2_field(field):
        if pa.types.is_binary(array.type) or pa.types.is_large_binary(array.type):
            if not isinstance(field.type, pa.ExtensionType):
                raise TypeError(
                    f"Blob v2 field {field.name!r} needs an extension type to encode, "
                    f"got {field.type}"
                )
            return _blob_v2_array_from_payloads(field.type, array)
        if isinstance(field.type, pa.ExtensionType) and isinstance(
            array.type, pa.ExtensionType
        ):
            return pa.ExtensionArray.from_storage(
                field.type, cast("pa.ExtensionArray", array).storage
            )
        if isinstance(field.type, pa.ExtensionType) and _is_v2_blob_descriptor(array):
            return pa.ExtensionArray.from_storage(field.type, array)
        return array

    dtype = field.type
    if pa.types.is_struct(dtype) and pa.types.is_struct(array.type):
        struct_type = cast("pa.StructType", dtype)
        struct_array = cast("pa.StructArray", array)
        child_fields: list[pa.Field] = []
        child_arrays: list[pa.Array] = []
        for idx in range(struct_type.num_fields):
            child_field = struct_type.field(idx)
            child_arrays.append(
                encode_blob_v2_storage_array(child_field, struct_array.field(idx))
            )
            child_fields.append(child_field)
        mask = struct_array.is_null() if struct_array.null_count else None
        return pa.StructArray.from_arrays(
            child_arrays,
            fields=child_fields,
            mask=mask,
        )
    return array


def _blob_v2_array_from_payloads(
    blob_type: pa.ExtensionType, payloads: pa.Array
) -> pa.Array:
    # Keep the Arrow payload buffer. to_pylist copies every byte into Python.
    storage_type = cast("pa.StructType", blob_type.storage_type)
    data_field = storage_type.field(storage_type.get_field_index("data"))
    data = payloads
    if not data.type.equals(data_field.type):
        data = data.cast(data_field.type)
    n = len(data)
    children = [
        data if storage_field.name == "data" else pa.nulls(n, storage_field.type)
        for storage_field in storage_type
    ]
    mask = data.is_null() if data.null_count else None
    storage = pa.StructArray.from_arrays(
        children,
        fields=list(storage_type),
        mask=mask,
    )
    return pa.ExtensionArray.from_storage(blob_type, storage)


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
    data_file_base_id: int | None = None


class _MissingBlobDataFileError(ValueError):
    pass


def _get_blob_data_file_path(
    dataset: lance.LanceDataset,
    fragment: lance.LanceFragment,
    column: str,
) -> tuple[str, int | None]:
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
            base_id = getattr(data_file, "base_id", None)
            return (
                data_file.path,
                int(base_id) if base_id is not None else None,
            )

    raise _MissingBlobDataFileError(
        f"Could not find data file for blob column {column!r} "
        f"in fragment {fragment.fragment_id}"
    )


def _descriptor_struct_storage(array: pa.Array) -> pa.Array:
    if isinstance(array, pa.ChunkedArray):
        array = array.combine_chunks()
    storage = getattr(array, "storage", array)
    return array if storage is None else storage


def _blob_v2_descriptor_storage(array: pa.Array) -> pa.StructArray:
    storage = _descriptor_struct_storage(array)
    if not pa.types.is_struct(storage.type):
        raise RuntimeError(f"Expected a blob v2 descriptor struct, got {array.type}")
    return cast("pa.StructArray", storage)


def _is_v2_blob_descriptor(array: pa.Array) -> bool:
    storage = _descriptor_struct_storage(array)
    if not pa.types.is_struct(storage.type):
        return False
    names = {field.name for field in storage.type}
    if "kind" in names:
        return True
    return "data" in names and "uri" in names


def _blob_descriptor_arrays(array: pa.Array) -> tuple[pa.Array, pa.Array]:
    if _is_v2_blob_descriptor(array):
        raise RuntimeError(
            "Blob v2 descriptors cannot be range-read from the fragment data "
            "file; packed and dedicated payloads live in sidecars"
        )
    storage = _descriptor_struct_storage(array)
    if not pa.types.is_struct(storage.type):
        raise RangeBlobReadUnsupportedError(
            f"Expected Lance blob descriptor struct, got {array.type}"
        )
    struct_arr = cast("pa.StructArray", storage)
    field_names = {field.name for field in storage.type}
    if "position" not in field_names or "size" not in field_names:
        raise RangeBlobReadUnsupportedError(
            "Expected Lance blob descriptor struct with position and size fields, "
            f"got {array.type}"
        )
    return struct_arr.field("position"), struct_arr.field("size")


def _reject_null_required_v2_fields(column: str, struct_arr: pa.StructArray) -> None:
    names = {field.name for field in struct_arr.type}
    valid = struct_arr.is_valid()
    for name in ("kind", "size"):
        if name not in names:
            raise RuntimeError(f"Blob column {column!r} descriptor is missing {name}")
        values = struct_arr.field(name)
        for idx in range(len(struct_arr)):
            if not valid[idx].as_py():
                continue
            if not values[idx].is_valid:
                raise RuntimeError(
                    f"Blob column {column!r} has a descriptor with a null {name}"
                )


def _reject_external_blob_v2(column: str, descriptors: pa.Array) -> None:
    if not _is_v2_blob_descriptor(descriptors):
        return
    struct_arr = _blob_v2_descriptor_storage(descriptors)
    names = {field.name for field in struct_arr.type}
    if "kind" in names:
        _reject_null_required_v2_fields(column, struct_arr)
        kinds = struct_arr.field("kind")
        for idx in range(len(struct_arr)):
            if not struct_arr[idx].is_valid:
                continue
            if int(kinds[idx].as_py()) == _BLOB_KIND_EXTERNAL:
                raise ExternalBlobUnsupportedError(
                    f"Blob column {column!r} contains an external blob. "
                    "Geneva does not support external blob v2 payloads"
                )
        return
    if "uri" not in names:
        return
    uris = struct_arr.field("uri")
    for idx in range(len(struct_arr)):
        if not struct_arr[idx].is_valid or not uris[idx].is_valid:
            continue
        uri = uris[idx].as_py()
        if uri:
            raise ExternalBlobUnsupportedError(
                f"Blob column {column!r} contains an external blob. "
                "Geneva does not support external blob v2 payloads"
            )


def _materialize_v2_blob_columns(
    dataset: lance.LanceDataset,
    batch: pa.RecordBatch,
    v2_fields: dict[str, pa.Field],
    *,
    selected_only_blob_columns: frozenset[str] | None,
    io_buffer_size: int | None,
) -> pa.RecordBatch:
    if _ROW_ADDRESS_COLUMN not in batch.schema.names:
        raise RuntimeError(
            "Blob v2 materialization requires _rowaddr on the scanned batch"
        )
    addresses = batch[_ROW_ADDRESS_COLUMN]
    selected_mask = (
        batch[BACKFILL_SELECTED] if BACKFILL_SELECTED in batch.schema.names else None
    )
    columns = list(batch.columns)
    fields = list(batch.schema)
    index_by_name = {name: idx for idx, name in enumerate(batch.schema.names)}

    for column, field in v2_fields.items():
        idx = index_by_name[column]
        _reject_external_blob_v2(column, columns[idx])
        is_selected_only = (
            selected_only_blob_columns is not None
            and column in selected_only_blob_columns
        )
        columns[idx] = _read_v2_blob_values(
            dataset,
            column,
            addresses,
            columns[idx],
            selected_only=is_selected_only,
            selected_mask=selected_mask,
            io_buffer_size=io_buffer_size,
        )
        metadata = dict(field.metadata or {})
        metadata[BLOB_V2_EXTENSION_METADATA_KEY] = BLOB_V2_EXTENSION_NAME
        fields[idx] = pa.field(
            column,
            pa.large_binary(),
            nullable=field.nullable or (is_selected_only and selected_mask is not None),
            metadata=metadata,
        )

    return pa.RecordBatch.from_arrays(columns, schema=pa.schema(fields))


@attrs.define(frozen=True)
class BlobV2Materialization:
    """Map a projected blob path to its physical Lance path."""

    batch_path: str
    dataset_path: str


def _descriptor_array_at_path(batch: pa.RecordBatch, path: str) -> pa.Array | None:
    if path in batch.schema.names:
        return batch[path]
    try:
        parts = parse_field_path(path)
    except ValueError:
        return None
    if len(parts) != 2 or parts[0] not in batch.schema.names:
        return None
    root = batch[parts[0]]
    if not pa.types.is_struct(root.type):
        return None
    struct_array = cast("pa.StructArray", root)
    child_names = [root.type.field(i).name for i in range(root.type.num_fields)]
    if parts[1] not in child_names:
        return None
    return struct_array.field(parts[1])


def materialize_blob_v2_paths(
    dataset: lance.LanceDataset,
    batch: pa.RecordBatch,
    materializations: Sequence[BlobV2Materialization],
    *,
    io_buffer_size: int | None = None,
) -> pa.RecordBatch:
    if not materializations:
        return batch
    if _ROW_ADDRESS_COLUMN not in batch.schema.names:
        raise RuntimeError(
            "Blob v2 materialization requires _rowaddr on the scanned batch"
        )
    addresses = batch[_ROW_ADDRESS_COLUMN]
    columns = list(batch.columns)
    fields = list(batch.schema)
    index_by_name = {name: idx for idx, name in enumerate(batch.schema.names)}
    for materialization in materializations:
        batch_path = materialization.batch_path
        descriptors = _descriptor_array_at_path(batch, batch_path)
        if descriptors is None:
            raise RuntimeError(
                f"Cannot materialize blob v2 path {batch_path!r} without "
                f"descriptors on the batch"
            )
        _reject_external_blob_v2(materialization.dataset_path, descriptors)
        payloads = _read_v2_blob_values(
            dataset,
            materialization.dataset_path,
            addresses,
            descriptors,
            selected_only=False,
            selected_mask=None,
            io_buffer_size=io_buffer_size,
        )
        if batch_path in index_by_name:
            idx = index_by_name[batch_path]
            columns[idx] = payloads
            fields[idx] = pa.field(
                batch_path,
                pa.large_binary(),
                nullable=True,
                metadata=_without_blob_v2_extension(fields[idx].metadata),
            )
            continue
        try:
            parts = parse_field_path(batch_path)
        except ValueError as exc:
            raise RuntimeError(
                f"Cannot materialize blob v2 path {batch_path!r} from batch "
                f"columns {list(index_by_name)}"
            ) from exc
        if len(parts) != 2 or parts[0] not in index_by_name:
            raise RuntimeError(
                f"Cannot materialize blob v2 path {batch_path!r} from batch "
                f"columns {list(index_by_name)}"
            )
        root, child = parts
        idx = index_by_name[root]
        struct_array = cast("pa.StructArray", columns[idx])
        struct_type = fields[idx].type
        child_fields: list[pa.Field] = []
        child_arrays: list[pa.Array] = []
        for child_idx in range(struct_type.num_fields):
            child_field = struct_type.field(child_idx)
            if child_field.name == child:
                child_fields.append(
                    pa.field(
                        child,
                        pa.large_binary(),
                        nullable=True,
                        metadata=_without_blob_v2_extension(child_field.metadata),
                    )
                )
                child_arrays.append(payloads)
            else:
                child_fields.append(child_field)
                child_arrays.append(struct_array.field(child_idx))
        mask = struct_array.is_null() if struct_array.null_count else None
        columns[idx] = pa.StructArray.from_arrays(
            child_arrays,
            fields=child_fields,
            mask=mask,
        )
        fields[idx] = pa.field(
            fields[idx].name,
            pa.struct(child_fields),
            nullable=fields[idx].nullable,
            metadata=fields[idx].metadata,
        )
    return pa.RecordBatch.from_arrays(columns, schema=pa.schema(fields))


def iter_blob_v2_payload_batches(
    dataset: lance.LanceDataset,
    batch: pa.RecordBatch,
    materializations: Sequence[BlobV2Materialization],
    *,
    byte_budget: int | None = None,
    io_buffer_size: int | None = None,
) -> Iterator[pa.RecordBatch]:
    if not materializations:
        yield batch
        return
    budget = resolve_blob_read_buffer_size(byte_budget)
    extra_row_bytes = _v2_row_payload_bytes(
        batch,
        [materialization.batch_path for materialization in materializations],
        selected_only_blob_columns=None,
    )
    row_ranges: list[list[tuple[str, int, int]]] = [[] for _ in range(batch.num_rows)]
    for row_slice in _iter_row_budget_slices(
        row_ranges, budget, extra_row_bytes=extra_row_bytes
    ):
        start = int(row_slice.start or 0)
        stop = int(row_slice.stop or start)
        yield materialize_blob_v2_paths(
            dataset,
            batch.slice(start, stop - start),
            materializations,
            io_buffer_size=io_buffer_size,
        )


def materialize_top_level_v1_blob_bytes(
    dataset: lance.LanceDataset,
    batch: pa.RecordBatch,
    columns: Sequence[str],
) -> pa.RecordBatch:
    if not columns:
        return batch
    if _ROW_ID_COLUMN not in batch.schema.names:
        raise RuntimeError("v1 blob take_blobs requires _rowid on the scanned batch")
    row_ids = [
        None if value is None else int(value)
        for value in batch[_ROW_ID_COLUMN].to_pylist()
    ]
    out_columns = list(batch.columns)
    out_fields = list(batch.schema)
    index_by_name = {name: idx for idx, name in enumerate(batch.schema.names)}
    for column in columns:
        idx = index_by_name[column]
        array = out_columns[idx]
        if pa.types.is_binary(array.type) or pa.types.is_large_binary(array.type):
            continue
        if _is_v2_blob_descriptor(array):
            continue
        ids: list[int] = []
        slots: list[int] = []
        for row_idx, row_id in enumerate(row_ids):
            if row_id is None:
                continue
            if array[row_idx].is_valid:
                ids.append(row_id)
                slots.append(row_idx)
        fetched: list[bytes | None] = [None] * len(array)
        if ids:
            blobs = dataset.take_blobs(column, ids=ids)
            for slot, blob in zip(slots, blobs, strict=True):
                if blob is None:
                    continue
                read = getattr(blob, "readall", None) or getattr(blob, "read", None)
                raw = read() if callable(read) else None
                if isinstance(raw, (bytes, bytearray, memoryview)):
                    fetched[slot] = bytes(raw)
        field = out_fields[idx]
        out_columns[idx] = pa.array(fetched, type=pa.large_binary())
        out_fields[idx] = pa.field(
            column,
            pa.large_binary(),
            nullable=True,
            metadata=field.metadata,
        )
    return pa.RecordBatch.from_arrays(out_columns, schema=pa.schema(out_fields))


def _v2_descriptor_payload_sizes(
    column: str, descriptors: pa.Array
) -> list[int | None]:
    struct_arr = _blob_v2_descriptor_storage(descriptors)
    names = {field.name for field in struct_arr.type}
    if "kind" in names:
        _reject_null_required_v2_fields(column, struct_arr)
    elif "size" not in names:
        raise RuntimeError(f"Blob column {column!r} descriptor is missing size")
    sizes = struct_arr.field("size").to_pylist()
    valid = struct_arr.is_valid().to_pylist()
    payload_sizes: list[int | None] = []
    for is_valid, size in zip(valid, sizes, strict=True):
        if not is_valid or size is None:
            payload_sizes.append(None)
            continue
        payload_sizes.append(int(size))
    return payload_sizes


def _v2_row_payload_bytes(
    batch: pa.RecordBatch,
    columns: Sequence[str],
    *,
    selected_only_blob_columns: frozenset[str] | None,
) -> list[int]:
    totals = [0] * batch.num_rows
    selected_mask = (
        batch[BACKFILL_SELECTED] if BACKFILL_SELECTED in batch.schema.names else None
    )
    for column in columns:
        descriptors = _descriptor_array_at_path(batch, column)
        if descriptors is None:
            continue
        is_selected_only = (
            selected_only_blob_columns is not None
            and column in selected_only_blob_columns
        )
        sizes = _v2_descriptor_payload_sizes(column, descriptors)
        for idx, size in enumerate(sizes):
            if (
                is_selected_only
                and selected_mask is not None
                and not selected_mask[idx].as_py()
            ):
                continue
            if size is not None and size > 0:
                totals[idx] += size
    return totals


def _read_v2_blob_values(
    dataset: lance.LanceDataset,
    column: str,
    addresses: pa.Array,
    descriptors: pa.Array,
    *,
    selected_only: bool,
    selected_mask: pa.Array | None,
    io_buffer_size: int | None,
) -> pa.Array:
    address_list = addresses.to_pylist()
    sizes = _v2_descriptor_payload_sizes(column, descriptors)
    if len(sizes) != len(address_list):
        raise RuntimeError(
            f"Blob column {column!r} descriptor count {len(sizes)} does not "
            f"match row address count {len(address_list)}"
        )

    requested: list[int] = []
    seen: set[int] = set()
    for idx, address in enumerate(address_list):
        if address is None:
            continue
        if (
            selected_only
            and selected_mask is not None
            and not selected_mask[idx].as_py()
        ):
            continue
        size = sizes[idx]
        if size is None or size <= 0:
            continue
        row_addr = int(address)
        if row_addr in seen:
            continue
        seen.add(row_addr)
        requested.append(row_addr)

    fetched: dict[int, bytes] = {}
    if requested:
        kwargs: dict[str, Any] = {"preserve_order": False}
        if io_buffer_size is not None:
            kwargs["io_buffer_size"] = io_buffer_size
        for row_addr, payload in dataset.read_blobs(
            column, addresses=requested, **kwargs
        ):
            if payload is None:
                continue
            fetched[int(row_addr)] = payload
    for row_addr in requested:
        payload = fetched.get(row_addr)
        if payload is None:
            raise RuntimeError(
                f"Blob column {column!r} is missing a payload for row "
                f"address {row_addr}"
            )

    values: list[bytes | None] = []
    for idx, address in enumerate(address_list):
        if (
            selected_only
            and selected_mask is not None
            and not selected_mask[idx].as_py()
        ):
            values.append(None)
            continue
        if address is None or sizes[idx] is None:
            values.append(None)
            continue
        if sizes[idx] == 0:
            values.append(b"")
            continue
        values.append(fetched[int(address)])
    return pa.array(values, type=pa.large_binary())


def materialized_column_bytes(
    array: pa.Array | pa.ChunkedArray, field: pa.Field
) -> int:
    """Bytes this column occupies once its blob leaves are materialized.

    A plain scan of a blob column returns ``struct<position, size>``
    *descriptors*, so ``nbytes`` reports ~16 B/row no matter how large the
    payload is. Sizing a read task or an actor reservation from that number is
    blind to the payload the applier will actually hold: measured on identical
    150 KiB values, ``nbytes`` gives 153,608 B/row unencoded and 16 B/row with
    ``lance-encoding:blob=true``.

    The descriptor carries the payload length in its ``size`` field, so the
    real width is available without fetching a single blob byte. Struct columns
    are walked so a nested blob leaf counts too; anything else falls back to
    ``nbytes``.
    """
    if isinstance(array, pa.ChunkedArray):
        return sum(materialized_column_bytes(chunk, field) for chunk in array.chunks)

    if is_blob_field(field) and pa.types.is_struct(array.type):
        names = {f.name for f in array.type}
        if {"position", "size"} <= names:
            sizes = cast("pa.StructArray", array).field("size")
            total = pc.sum(sizes).as_py()
            # Descriptors themselves stay resident alongside the payload.
            return int(total or 0) + array.nbytes

    # Recurse on the *schema* type, not the scanned one. A scanned blob leaf
    # arrives as a bare ``struct<position, size>`` with the
    # ``lance-encoding:blob`` metadata stripped, so asking ``array.type``
    # whether it holds a blob answers no and the whole struct falls through to
    # descriptor bytes -- the exact bug this function exists to fix, one level
    # down. ``field.type`` came from the dataset schema and still knows.
    #
    # Children are paired by name because a projection can drop or reorder
    # them: a positional walk would misattribute one child's payload to
    # another's field, and silently price both wrong.
    if _struct_contains_blob(field.type) and pa.types.is_struct(array.type):
        struct_arr = cast("pa.StructArray", array)
        scanned = {f.name: i for i, f in enumerate(array.type)}
        schema_type = cast("pa.StructType", field.type)
        total = 0
        for i in range(schema_type.num_fields):
            child_field = schema_type.field(i)
            scanned_index = scanned.get(child_field.name)
            if scanned_index is None:
                continue
            total += materialized_column_bytes(
                struct_arr.field(scanned_index), child_field
            )
        return total

    return array.nbytes


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
    row_ranges: Sequence[Sequence[tuple[str, int, int]]],
    byte_budget: int,
    extra_row_bytes: Sequence[int] | None = None,
) -> Iterator[slice]:
    """Yield row slices whose coalesced blob reads stay near ``byte_budget``.

    A single row can exceed the budget, but rows are never split because UDF
    inputs must stay row-complete. ``extra_row_bytes`` charges payload sizes
    that are not data-file ranges.
    """

    if not row_ranges:
        return

    start = 0
    current_budget = _CoalescedRangeBudget(byte_budget)
    extra_acc = 0
    for idx, ranges in enumerate(row_ranges):
        extra = extra_row_bytes[idx] if extra_row_bytes is not None else 0
        current_budget.add_ranges(ranges)
        extra_acc += extra
        if idx > start and current_budget.size + extra_acc > byte_budget:
            yield slice(start, idx)
            start = idx
            current_budget = _CoalescedRangeBudget(byte_budget)
            current_budget.add_ranges(ranges)
            extra_acc = extra

    if start < len(row_ranges):
        yield slice(start, len(row_ranges))


def _read_data_file_ranges(
    file_reads: dict[str, tuple[LanceFileSession, str]],
    ranges: dict[str, list[tuple[int, int]]],
) -> dict[str, list[tuple[int, pa.Buffer]]]:
    """Fetch coalesced byte ranges through per-base Lance file sessions.

    ``file_reads`` maps each data file to its session and session-relative
    path (dataset-root files read via the dataset session, multi-base files
    via a session rooted at their base). Each range is a single ranged GET
    against the owning object store; token acquisition happens in Rust with
    cached credentials, so a failure surfaces as a catchable ``OSError``
    instead of an unhandled C++ exception aborting the process.
    """
    buffers: dict[str, list[tuple[int, pa.Buffer]]] = {}
    for data_file_path, file_ranges in ranges.items():
        session, rel_path = file_reads[data_file_path]
        for range_start, range_end in file_ranges:
            data = session.read_range(rel_path, range_start, range_end - range_start)
            buffers.setdefault(data_file_path, []).append(
                (range_start, pa.py_buffer(data))
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
    file_reads: dict[str, tuple[LanceFileSession, str]],
    row_ranges: Sequence[Sequence[tuple[str, int, int]]],
    byte_budget: int,
    selected_only_blob_columns: frozenset[str] | None,
) -> pa.RecordBatch:
    if not plans:
        return batch
    flat_ranges = [r for ranges in row_ranges for r in ranges]
    data_file_ranges = _coalesce_blob_ranges(flat_ranges, byte_budget)
    data_file_buffers = _read_data_file_ranges(file_reads, data_file_ranges)
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

    schema = dataset.schema
    scan_columns = [_ROW_ID_COLUMN]
    # Lance needs v2 descriptor fields projected when filtering on them.
    scan_columns.extend(sorted(referenced_v2_paths(where, schema)))

    id_scan = dataset.scanner(
        columns=scan_columns,
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

    This is the engine behind ``blob_read_strategy="range"``. It reads blob
    payloads as coalesced ranged reads through the dataset's file session
    (per-base sessions for multi-base datasets), batches the byte ranges by
    the configured buffer budget, and returns batches ready for UDF argument
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
    from geneva.utils.multi_base import resolve_dataset_bases

    base_data_dirs: dict[int, str] | None = {
        base_id: base.data_dir
        for base_id, base in resolve_dataset_bases(dataset).items()
    }
    if not base_data_dirs:
        base_data_dirs = None

    fragment = dataset.get_fragment(frag_id)
    if fragment is None:
        return

    blob_plans = []
    v2_fields: dict[str, pa.Field] = {}
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
        if is_blob_v2_field(field):
            v2_fields[col] = field
            continue
        try:
            data_file_path, data_file_base_id = _get_blob_data_file_path(
                dataset, fragment, col
            )
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
                data_file_base_id=data_file_base_id,
            )
        )

    byte_budget = resolve_blob_read_buffer_size(blob_read_buffer_size)
    needs_filter_mask = where is not None
    requested_columns = set(columns)

    scanner_kwargs: dict[str, Any] = {
        "columns": list(columns),
        # Needed if a planned v1 column is actually v2.
        "with_row_address": True,
        "fragments": [fragment],
        "offset": int(offset),
        "batch_size": int(batch_size) if batch_size and batch_size > 0 else None,
    }
    if needs_filter_mask:
        scanner_kwargs["with_row_id"] = True
    if limit > 0:
        scanner_kwargs["limit"] = int(limit)
    scanner_kwargs = {k: v for k, v in scanner_kwargs.items() if v is not None}

    # One file session per task for dataset-root data files, plus one plain-
    # rooted session per storage base for multi-base data files (a dataset
    # session resolves paths relative to the table root and cannot address a
    # base outside it -- same routing as MultiBaseCheckpointStore). Tokens are
    # acquired, cached, and refreshed in Rust, ranged reads go straight to the
    # store with no per-file open/stat round trip, and an auth failure is a
    # catchable Python error.
    from lance.file import LanceFileSession

    root_session = dataset.new_file_session()
    base_sessions: dict[int, LanceFileSession] = {}
    session_options = (
        {k: str(v) for k, v in storage_options.items()} if storage_options else None
    )
    file_reads: dict[str, tuple[LanceFileSession, str]] = {}
    for plan in blob_plans:
        base_id = plan.data_file_base_id
        base_dir = (
            base_data_dirs.get(base_id)
            if base_data_dirs and base_id is not None
            else None
        )
        if base_id is None or base_dir is None:
            file_reads[plan.data_file_path] = (
                root_session,
                f"data/{plan.data_file_path.lstrip('/')}",
            )
            continue
        session = base_sessions.get(base_id)
        if session is None:
            session = LanceFileSession(base_dir, storage_options=session_options)
            base_sessions[base_id] = session
        file_reads[plan.data_file_path] = (session, plan.data_file_path.lstrip("/"))

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
            # V2 position/size are not necessarily data-file offsets.
            remaining_v1: list[_BlobColumnPlan] = []
            for plan in blob_plans:
                descriptors = batch.column(plan.name)
                if _is_v2_blob_descriptor(descriptors):
                    v2_fields[plan.name] = plan.field
                    _reject_external_blob_v2(plan.name, descriptors)
                else:
                    remaining_v1.append(plan)
            blob_plans = remaining_v1
            if v2_fields:
                for column in v2_fields:
                    if column in batch.schema.names:
                        _reject_external_blob_v2(column, batch[column])
            row_ranges = _row_blob_ranges(
                batch,
                blob_plans,
                selected_only_blob_columns=selected_only_blob_columns,
            )
            extra_row_bytes = (
                _v2_row_payload_bytes(
                    batch,
                    list(v2_fields),
                    selected_only_blob_columns=selected_only_blob_columns,
                )
                if v2_fields
                else None
            )
            for row_slice in _iter_row_budget_slices(
                row_ranges, byte_budget, extra_row_bytes=extra_row_bytes
            ):
                start = int(row_slice.start or 0)
                stop = int(row_slice.stop or start)
                sliced = batch.slice(start, stop - start)
                materialized = _materialize_blob_slice(
                    sliced,
                    blob_plans,
                    file_reads,
                    row_ranges[start:stop],
                    byte_budget,
                    selected_only_blob_columns,
                )
                if v2_fields:
                    materialized = _materialize_v2_blob_columns(
                        dataset,
                        materialized,
                        v2_fields,
                        selected_only_blob_columns=selected_only_blob_columns,
                        io_buffer_size=blob_read_buffer_size,
                    )
                if (
                    not with_row_address
                    and _ROW_ADDRESS_COLUMN in materialized.schema.names
                ):
                    materialized = materialized.drop_columns([_ROW_ADDRESS_COLUMN])
                if decomps:
                    materialized = _reassemble_struct_columns(
                        materialized, decomps, requested_struct_columns
                    )
                yield materialized
    finally:
        _close_iterator(main_batches)
