# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Blob-v2 checkpoint assembly helpers.

These helpers write blob payload bytes directly into the final fragment's packed
blob sidecars and replace checkpoint batch payload arrays with prepared Lance
blob-v2 descriptor arrays.
"""

from __future__ import annotations

import uuid
from typing import Any, cast

import lance
import pyarrow as pa
from lance.file import LanceFileSession
from yarl import URL

from geneva.apply.blob_range import is_blob_field
from geneva.utils import parse_data_storage_version

_BLOB_V2_DATA_FILE_NAMESPACE = uuid.uuid5(
    uuid.NAMESPACE_URL,
    "geneva:blob-v2-checkpoint-data-file",
)
_BLOB_V2_METADATA_KEY = b"ARROW:extension:name"
_BLOB_V2_METADATA_VALUE = b"lance.blob.v2"
_MAX_BLOB_ID = (1 << 32) - 1


class BlobCheckpointOptimizationUnsupportedError(RuntimeError):
    """Raised when a batch or schema cannot use blob-v2 checkpoint assembly."""


def blob_v2_checkpoint_data_file_name(fragment_dedupe_key: str) -> str:
    """Stable final data-file name used by descriptor checkpoints."""

    return f"{uuid.uuid5(_BLOB_V2_DATA_FILE_NAMESPACE, fragment_dedupe_key)}.lance"


def default_fragment_data_dir(ds_uri: str, data_dir: str | None = None) -> str:
    """Resolve the fragment data directory used by Lance file APIs."""

    if data_dir:
        return data_dir
    return str(URL(ds_uri) / "data")


def storage_version_supports_blob_v2_checkpoints(version: str | None) -> bool:
    if not isinstance(version, str):
        return False
    try:
        major, minor = parse_data_storage_version(version)
    except ValueError:
        return False
    return (major, minor) >= (2, 2)


def schema_supports_blob_v2_checkpoints(schema: pa.Schema) -> bool:
    """Return whether ``schema`` has only supported blob checkpoint shapes."""

    return bool(_collect_blob_paths(schema))


def _collect_blob_paths(schema: pa.Schema) -> tuple[tuple[str, ...], ...]:
    paths: list[tuple[str, ...]] = []
    for field in schema:
        _collect_blob_field_paths(field, (field.name,), paths)
    return tuple(paths)


def _collect_blob_field_paths(
    field: pa.Field,
    path: tuple[str, ...],
    paths: list[tuple[str, ...]],
) -> None:
    if _is_binary_blob_field(field):
        paths.append(path)
        return

    dtype = field.type
    if pa.types.is_struct(dtype):
        struct_type = cast("pa.StructType", dtype)
        for idx in range(struct_type.num_fields):
            child = struct_type.field(idx)
            _collect_blob_field_paths(child, (*path, child.name), paths)
        return

    if _field_or_children_have_blob_marker(field):
        raise BlobCheckpointOptimizationUnsupportedError(
            f"blob checkpoint optimization does not support field {'.'.join(path)!r} "
            f"with type {field.type}"
        )


def _field_or_children_have_blob_marker(field: pa.Field) -> bool:
    if is_blob_field(field):
        return True
    dtype = field.type
    if pa.types.is_struct(dtype):
        struct_type = cast("pa.StructType", dtype)
        return any(
            _field_or_children_have_blob_marker(struct_type.field(idx))
            for idx in range(struct_type.num_fields)
        )
    if (
        pa.types.is_list(dtype)
        or pa.types.is_large_list(dtype)
        or pa.types.is_fixed_size_list(dtype)
    ):
        return _field_or_children_have_blob_marker(
            cast("pa.ListType", dtype).value_field
        )
    return False


def _is_binary_blob_field(field: pa.Field) -> bool:
    if _is_blob_v2_extension_type(field.type):
        return True
    metadata = field.metadata or {}
    return metadata.get(_BLOB_V2_METADATA_KEY) == _BLOB_V2_METADATA_VALUE and (
        pa.types.is_binary(field.type) or pa.types.is_large_binary(field.type)
    )


def _is_blob_v2_extension_type(dtype: pa.DataType) -> bool:
    return isinstance(
        dtype, pa.ExtensionType
    ) and dtype.extension_name == _BLOB_V2_METADATA_VALUE.decode("utf-8")


def _blob_id_for_checkpoint(
    *,
    range_start: int,
    blob_field_count: int,
    blob_field_ordinal: int,
) -> int:
    slot = int(range_start) * int(blob_field_count) + int(blob_field_ordinal)
    if slot >= _MAX_BLOB_ID:
        raise BlobCheckpointOptimizationUnsupportedError(
            "blob checkpoint optimization cannot assign a unique blob id for "
            f"range_start={range_start}, blob_field_count={blob_field_count}, "
            f"blob_field_ordinal={blob_field_ordinal}"
        )
    # Use high descending IDs so prepared descriptors do not collide with
    # Lance's normal writer-side allocator, which starts at 1.
    return _MAX_BLOB_ID - slot


def prepare_blob_v2_checkpoint_batch(
    batch: pa.RecordBatch,
    *,
    data_dir: str,
    data_file_name: str,
    range_start: int,
    storage_options: dict[str, str] | None = None,
    namespace_client: Any | None = None,
    table_id: list[str] | None = None,
) -> pa.RecordBatch:
    """Write blob bytes to final sidecars and return a descriptor-only batch."""

    blob_paths = _collect_blob_paths(batch.schema)
    if not blob_paths:
        return batch

    path_to_ordinal = {path: idx for idx, path in enumerate(blob_paths)}
    session = LanceFileSession(
        data_dir,
        storage_options=storage_options,
        namespace_client=namespace_client,
        table_id=table_id,
    )

    new_fields: list[pa.Field] = []
    new_arrays: list[pa.Array] = []
    for field, array in zip(batch.schema, batch.columns, strict=True):
        new_field, new_array = _prepare_field_array(
            field,
            array,
            path=(field.name,),
            path_to_ordinal=path_to_ordinal,
            blob_field_count=len(blob_paths),
            range_start=range_start,
            session=session,
            data_file_name=data_file_name,
        )
        new_fields.append(new_field)
        new_arrays.append(new_array)

    return pa.record_batch(
        new_arrays,
        schema=pa.schema(
            new_fields,
            metadata=cast(
                "dict[bytes | str, bytes | str] | None", batch.schema.metadata
            ),
        ),
    )


def _prepare_field_array(
    field: pa.Field,
    array: pa.Array,
    *,
    path: tuple[str, ...],
    path_to_ordinal: dict[tuple[str, ...], int],
    blob_field_count: int,
    range_start: int,
    session: LanceFileSession,
    data_file_name: str,
) -> tuple[pa.Field, pa.Array]:
    if _is_binary_blob_field(field):
        ordinal = path_to_ordinal[path]
        blob_id = _blob_id_for_checkpoint(
            range_start=range_start,
            blob_field_count=blob_field_count,
            blob_field_ordinal=ordinal,
        )
        return _prepare_blob_array(
            field,
            array,
            session=session,
            data_file_name=data_file_name,
            blob_id=blob_id,
        )

    dtype = field.type
    if pa.types.is_struct(dtype):
        struct_type = cast("pa.StructType", dtype)
        struct_array = cast("pa.StructArray", array)
        child_fields: list[pa.Field] = []
        child_arrays: list[pa.Array] = []
        for idx in range(struct_type.num_fields):
            child_field = struct_type.field(idx)
            new_child_field, new_child_array = _prepare_field_array(
                child_field,
                struct_array.field(idx),
                path=(*path, child_field.name),
                path_to_ordinal=path_to_ordinal,
                blob_field_count=blob_field_count,
                range_start=range_start,
                session=session,
                data_file_name=data_file_name,
            )
            child_fields.append(new_child_field)
            child_arrays.append(new_child_array)

        mask = struct_array.is_null() if struct_array.null_count else None
        new_array = pa.StructArray.from_arrays(
            child_arrays,
            fields=child_fields,
            mask=mask,
        )
        return (
            pa.field(
                field.name,
                pa.struct(child_fields),
                nullable=field.nullable,
                metadata=field.metadata,
            ),
            new_array,
        )

    return field, array


def _prepare_blob_array(
    field: pa.Field,
    array: pa.Array,
    *,
    session: LanceFileSession,
    data_file_name: str,
    blob_id: int,
) -> tuple[pa.Field, pa.Array]:
    builder = lance.BlobDescriptorArrayBuilder(field.name)

    valid_rows: list[bool] = []
    payloads: list[bytes] = []
    for idx in range(len(array)):
        value = array[idx]
        valid_rows.append(value.is_valid)
        if value.is_valid:
            payloads.append(_blob_payload_bytes(array, idx))

    packed = None
    if payloads:
        packed = session.open_packed_blob_writer(data_file_name, blob_id)
        for payload in payloads:
            packed.write_blob(payload)
    descriptors = list(packed.finish()) if packed is not None else []
    if len(descriptors) != len(payloads):
        raise RuntimeError(
            "packed blob writer returned a different number of descriptors "
            f"than payloads: descriptors={len(descriptors)}, "
            f"payloads={len(payloads)}"
        )

    descriptor_idx = 0
    for is_valid in valid_rows:
        if not is_valid:
            builder.append_null()
        else:
            builder.append(descriptors[descriptor_idx])
            descriptor_idx += 1

    descriptor_array = builder.finish()
    descriptor_field = builder.field.with_nullable(field.nullable)
    return descriptor_field, descriptor_array


def _blob_payload_bytes(array: pa.Array, idx: int) -> bytes:
    if _is_blob_v2_extension_type(array.type):
        storage = cast("pa.ExtensionArray", array).storage
        data = storage.field("data")[idx]
        if data.is_valid:
            return bytes(data.as_py())
        uri = storage.field("uri")[idx]
        if uri.is_valid:
            raise BlobCheckpointOptimizationUnsupportedError(
                "blob-v2 checkpoint optimization only supports inline blob "
                "values produced by the UDF"
            )
        return b""
    return bytes(array[idx].as_py())
