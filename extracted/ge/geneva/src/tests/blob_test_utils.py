# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Focused helpers for blob schema and writer checkpoint tests."""

import os
from collections.abc import Iterator
from typing import Any

import pyarrow as pa

STRING_BLOB_METADATA: dict[str, str] = {"lance-encoding:blob": "true"}
BYTES_BLOB_METADATA: dict[bytes, bytes] = {b"lance-encoding:blob": b"true"}


def blob_field(
    name: str = "image_bytes",
    metadata: dict | None = None,
) -> pa.Field:
    """A large-binary leaf field marked with Lance's blob-encoding metadata."""
    return pa.field(
        name,
        pa.large_binary(),
        metadata=dict(STRING_BLOB_METADATA) if metadata is None else metadata,
    )


def bytes_blob_field(name: str = "image_bytes") -> pa.Field:
    return blob_field(name, metadata=dict(BYTES_BLOB_METADATA))


def blob_schema(name: str = "blob") -> pa.Schema:
    return pa.schema([blob_field(name), pa.field("_rowaddr", pa.uint64())])


def struct_blob_schema(root: str = "image") -> pa.Schema:
    """A whole-struct column whose nested leaf is blob-encoded."""
    struct_type = pa.struct([blob_field("image_bytes"), pa.field("w", pa.int64())])
    return pa.schema([pa.field(root, struct_type), pa.field("_rowaddr", pa.uint64())])


def list_blob_schema(name: str = "imgs") -> pa.Schema:
    """A list column whose elements are blob-encoded."""
    return pa.schema(
        [
            pa.field(name, pa.list_(blob_field("item"))),
            pa.field("_rowaddr", pa.uint64()),
        ]
    )


def deep_struct_blob_schema(root: str = "outer") -> pa.Schema:
    """A struct column whose blob leaf is nested two levels deep."""
    inner = pa.struct([blob_field("image_bytes"), pa.field("w", pa.int64())])
    return pa.schema(
        [
            pa.field(root, pa.struct([pa.field("inner", inner)])),
            pa.field("_rowaddr", pa.uint64()),
        ]
    )


def nullable_blob_batch(nrows: int = 4000) -> pa.RecordBatch:
    st = pa.struct(
        [
            bytes_blob_field(),
            pa.field("error_code", pa.string()),
        ]
    )
    rows = [
        {
            "image_bytes": None if i % 3 == 0 else os.urandom(256),
            "error_code": "ERR" if i % 3 == 0 else None,
        }
        for i in range(nrows)
    ]
    return pa.record_batch(
        [pa.array(rows, type=st), pa.array(range(nrows), type=pa.uint64())],
        schema=pa.schema([pa.field("image", st), pa.field("_rowaddr", pa.uint64())]),
    )


def one_blob_batch(value: int) -> pa.RecordBatch:
    return pa.RecordBatch.from_arrays([pa.array([value])], names=["blob"])


class FakeScanner:
    def __init__(self, value: int, scanned: dict) -> None:
        self._value = value
        self._scanned = scanned

    def to_batches(self) -> Iterator[pa.RecordBatch]:
        yield one_blob_batch(self._value)


class FakeFragment:
    def __init__(self, value: int, scanned: dict) -> None:
        self._value = value
        self._scanned = scanned

    def scanner(self, **kwargs: Any) -> FakeScanner:
        self._scanned.update(kwargs)
        return FakeScanner(self._value, self._scanned)


class FakeDataset:
    """Minimal stand-in for the scanner fallback path.

    ``schema`` drives blob detection; defaults to a non-blob column so the
    scanner path is exercised.
    """

    def __init__(self, value: int = 9, schema: pa.Schema | None = None) -> None:
        self._value = value
        self.scanned: dict = {}
        self.schema = (
            schema
            if schema is not None
            else pa.schema(
                [pa.field("blob", pa.int64()), pa.field("_rowaddr", pa.uint64())]
            )
        )

    def get_fragment(self, frag_id: int) -> FakeFragment:
        self.scanned["frag_id"] = frag_id
        return FakeFragment(self._value, self.scanned)


def bare_fragment_writer(**fields: Any) -> Any:
    """Construct a FragmentWriter without invoking Ray.

    The actor's user class lives behind the ``@ray.remote`` wrapper; build a
    bare instance and set only the attrs the targeted writer helpers read.
    """
    import geneva.runners.ray.writer as writer_module

    cls = writer_module.FragmentWriter.__ray_metadata__.modified_class
    inst = cls.__new__(cls)
    defaults: dict[str, Any] = {
        "uri": "mem://x",
        "fragment_id": 7,
        "read_version": 3,
        "storage_options": None,
        "range_blob_columns": None,
        "selected_only_blob_columns": None,
        "struct_blob_decomp": None,
        "blob_read_strategy": None,
        "blob_read_buffer_size": None,
    }
    defaults.update(fields)
    for k, v in defaults.items():
        object.__setattr__(inst, k, v)
    return inst


def blob_encoded_table(root: str | os.PathLike[str], values: list[bytes]) -> Any:
    """Create an on-disk Geneva table with a blob-encoded ``b`` column."""
    from geneva import connect

    schema = pa.schema(
        [
            pa.field("a", pa.int64()),
            blob_field("b"),
        ]
    )
    table = pa.table({"a": list(range(len(values))), "b": values}, schema=schema)
    db = connect(str(root))
    return db.create_table(
        "cf", table, storage_options={"new_table_data_storage_version": "2.0"}
    )


def struct_blob_encoded_table(
    root: str | os.PathLike[str],
    image_bytes: list[bytes],
) -> Any:
    """Create an on-disk table with an ``image.image_bytes`` blob leaf."""
    from geneva import connect

    struct_type = pa.struct([blob_field("image_bytes"), pa.field("w", pa.int64())])
    schema = pa.schema([pa.field("a", pa.int64()), pa.field("image", struct_type)])
    table = pa.table(
        {
            "a": list(range(len(image_bytes))),
            "image": [{"image_bytes": v, "w": i} for i, v in enumerate(image_bytes)],
        },
        schema=schema,
    )
    db = connect(str(root))
    return db.create_table(
        "cf_struct", table, storage_options={"new_table_data_storage_version": "2.0"}
    )


class FakeQueue:
    """Minimal Ray checkpoint queue stand-in for deferred carry-forward tests.

    Items are ``(offset, key, num_rows)`` payloads, followed by a seal sentinel.
    """

    def __init__(self, items: list[tuple[int, str, int]]) -> None:
        self._items = list(items) + [(-1, "", 0)]  # in-band seal sentinel

    def get(self) -> tuple[int, str, int]:
        return self._items.pop(0)


def deferred_cf_writer(tbl: Any, ds: Any, frag_id: int, store: Any, queue: Any) -> Any:
    inst = bare_fragment_writer(
        uri=tbl.uri,
        fragment_id=frag_id,
        read_version=ds.version,
        namespace_config=None,
        table_id=None,
        column_names=["b"],
    )
    object.__setattr__(inst, "checkpoint_keys", queue)
    object.__setattr__(inst, "_store", store)
    return inst
