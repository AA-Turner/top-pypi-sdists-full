# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Checkpoints store blob columns without blob encoding (GEN-580).

A nullable blob column written with ``lance-encoding:blob`` lands on Lance's
``BlobLayout`` decode path, which panics the reader on read (GEN-578). The
checkpoint store strips that metadata on write so the column is stored with
ordinary (``FullZip``) encoding, and restores it on read so the committed table —
whose fragment schema the writer derives from the checkpoint batch — stays
blob-encoded.
"""

import glob
import os

import pyarrow as pa
from blob_test_utils import bytes_blob_field, nullable_blob_batch
from lance.file import LanceFileReader

from geneva.checkpoint import (
    _BLOB_ENCODING_KEY,
    _WAS_BLOB_KEY,
    FlatLanceCheckpointStore,
    _swap_batch_blob_marker,
)


def _on_disk_layout(root: str, key: str) -> str:
    path = next(
        p
        for p in glob.glob(os.path.join(root, "**", "*.lance"), recursive=True)
        if os.path.isfile(p) and key in p
    )
    enc = str(LanceFileReader(path).metadata().columns[0].pages[0].encoding)
    for kind in ("BlobLayout", "FullZip", "MiniBlock"):
        if kind in enc:
            return kind
    return "other"


def test_blob_checkpoint_stored_as_fullzip_and_restored(tmp_path) -> None:
    store = FlatLanceCheckpointStore(str(tmp_path))
    key = "udf-x_ver-1_col-image_range-0-4000"
    batch = nullable_blob_batch()
    store[key] = batch
    got = store[key]

    # Stored off the buggy BlobLayout path.
    assert _on_disk_layout(str(tmp_path), key) == "FullZip"

    # Blob encoding restored on read, so the committed fragment stays blob-encoded.
    restored_md = got.schema.field("image").type.field(0).metadata or {}
    assert restored_md.get(_BLOB_ENCODING_KEY) == b"true"
    assert _WAS_BLOB_KEY not in restored_md

    # Data is byte-for-byte identical (nulls preserved).
    orig_bytes = batch.column("image").field("image_bytes")
    got_bytes = got.column("image").field("image_bytes")
    assert got.num_rows == batch.num_rows
    assert got_bytes.null_count > 0
    assert got_bytes.equals(orig_bytes)


def test_non_blob_checkpoint_unchanged(tmp_path) -> None:
    store = FlatLanceCheckpointStore(str(tmp_path))
    key = "udf-x_ver-1_col-c_range-0-3"
    batch = pa.record_batch(
        [pa.array([1, 2, 3], type=pa.int64())],
        schema=pa.schema([pa.field("x", pa.int64())]),
    )
    store[key] = batch
    got = store[key]
    assert got.num_rows == 3
    # No marker introduced on a batch that never carried blob encoding.
    assert got.schema.field("x").metadata is None


def test_swap_marker_roundtrip_preserves_nested_and_data() -> None:
    # Blob field nested in a struct inside a list exercises recursion.
    inner = pa.struct([bytes_blob_field(), pa.field("n", pa.int32())])
    schema = pa.schema(
        [
            bytes_blob_field(),
            pa.field("nested", pa.large_list(inner)),
            pa.field("plain", pa.string()),
        ]
    )
    batch = pa.record_batch(
        [
            pa.array([None, b"x"], type=pa.large_binary()),
            pa.array([[], [{"image_bytes": b"y", "n": 1}]], type=pa.large_list(inner)),
            pa.array(["a", "b"], type=pa.string()),
        ],
        schema=schema,
    )

    stripped = _swap_batch_blob_marker(batch, _BLOB_ENCODING_KEY, _WAS_BLOB_KEY)
    # No blob-encoding metadata remains anywhere after stripping.
    assert stripped.schema.field("image_bytes").metadata == {_WAS_BLOB_KEY: b"true"}
    list_item = stripped.schema.field("nested").type.value_field.type
    assert list_item.field("image_bytes").metadata == {_WAS_BLOB_KEY: b"true"}

    restored = _swap_batch_blob_marker(stripped, _WAS_BLOB_KEY, _BLOB_ENCODING_KEY)
    assert restored.schema.equals(batch.schema, check_metadata=True)
    assert restored.equals(batch)


def test_swap_marker_noop_without_blob_fields() -> None:
    batch = pa.record_batch(
        [pa.array([1, 2], type=pa.int64())],
        schema=pa.schema([pa.field("x", pa.int64())]),
    )
    # Unchanged object returned (no rebuild) when there is nothing to rename.
    assert _swap_batch_blob_marker(batch, _BLOB_ENCODING_KEY, _WAS_BLOB_KEY) is batch
