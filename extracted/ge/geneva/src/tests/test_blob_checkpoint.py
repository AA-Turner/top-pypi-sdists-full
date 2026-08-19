# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import os
import uuid
from pathlib import Path
from urllib.parse import urlparse

import lance
import pyarrow as pa
import pytest
from lance.file import LanceFileReader

from geneva import udf
from geneva.apply import (
    CheckpointingApplier,
    DirectFragmentWriteConfig,
    blob_v2_checkpoint_data_file_name_for_fragment,
    plan_read,
)
from geneva.apply.blob_checkpoint import (
    blob_v2_checkpoint_data_file_name,
    prepare_blob_v2_checkpoint_batch,
)
from geneva.checkpoint import FlatLanceCheckpointStore
from geneva.checkpoint_utils import (
    format_checkpoint_key,
    format_checkpoint_prefix,
    hash_source_files,
)
from geneva.runners.ray.writer import write_fragment_file
from geneva.utils.parse_rust_debug import extract_field_ids_and_column_indices

_IMAGE_SIZE_BYTES = 64 * 1024


class _MapTask:
    def __init__(self, schema: pa.Schema) -> None:
        self._schema = schema

    def output_schema(self) -> pa.Schema:
        return self._schema

    def input_columns(self) -> list[str] | None:
        return None

    def batch_size(self) -> int:
        return 1024

    def checkpoint_prefix(
        self,
        *,
        dataset_uri: str,
        where: str | None,
        column: str | None = None,
        src_files_hash: str | None = None,
    ) -> str:
        return format_checkpoint_prefix(
            udf_name="make_blob",
            udf_version="v1",
            column=column or "blob",
            where=where,
            dataset_uri=dataset_uri,
            src_files_hash=src_files_hash,
        )

    def checkpoint_key(
        self,
        *,
        dataset_uri: str,
        dataset_version: int | str | None,
        frag_id: int,
        start: int,
        end: int,
        where: str | None,
        src_files_hash: str | None = None,
    ) -> str:
        del dataset_version
        return format_checkpoint_key(
            self.checkpoint_prefix(
                dataset_uri=dataset_uri,
                where=where,
                src_files_hash=src_files_hash,
            ),
            frag_id=frag_id,
            start=start,
            end=end,
        )

    def udf_version(self) -> str:
        return "v1"


class _Task:
    def __init__(self, uri: str) -> None:
        self.uri = uri

    def dest_frag_id(self) -> int:
        return 7

    def dest_offset(self) -> int:
        return 0

    def num_rows(self) -> int:
        return 2

    def table_uri(self) -> str:
        return self.uri


class _NoPayloadReadFlatLanceCheckpointStore(FlatLanceCheckpointStore):
    def __getitem__(self, item: str) -> pa.RecordBatch:
        raise AssertionError(f"checkpoint payload read for {item}")


def _blob_batch() -> pa.RecordBatch:
    return pa.record_batch(
        [
            pa.array([0, 1], type=pa.uint64()),
            lance.blob_array([b"image-a", None]),
        ],
        schema=pa.schema(
            [
                pa.field("_rowaddr", pa.uint64()),
                lance.blob_field("blob"),
            ]
        ),
    )


def _field_names(dtype: pa.StructType) -> set[str]:
    return {dtype.field(idx).name for idx in range(dtype.num_fields)}


def _blob_storage(array: pa.Array) -> pa.StructArray:
    if isinstance(array, pa.ExtensionArray):
        return array.storage
    return array  # type: ignore[return-value]


def _local_path(uri: str) -> Path:
    parsed = urlparse(uri)
    if parsed.scheme == "file":
        return Path(parsed.path)
    return Path(uri)


def _image_payload(image_id: int) -> bytes:
    return bytes((image_id * 37 + idx * 29) % 251 for idx in range(_IMAGE_SIZE_BYTES))


def _lance_file_version(path: Path) -> tuple[int, int]:
    metadata = LanceFileReader(str(path)).metadata()
    return metadata.major_version, metadata.minor_version


def _source_files_hash_for_table(uri: str) -> str:
    ds = lance.dataset(uri)
    fragment = ds.get_fragment(0)
    assert fragment is not None
    return hash_source_files(data_file.path for data_file in fragment.data_files())


def test_prepare_blob_v2_checkpoint_batch_replaces_nested_blob_with_descriptors(
    tmp_path,
) -> None:
    payload_field = lance.blob_field(
        "payload",
        inline_size_threshold=1024,
        pack_file_size_threshold=1024 * 1024,
    )
    asset_fields = [pa.field("mime", pa.string()), payload_field]
    batch = pa.record_batch(
        [
            pa.array([0, 1], type=pa.uint64()),
            pa.StructArray.from_arrays(
                [
                    pa.array(["image/png", "image/jpeg"]),
                    lance.blob_array([b"png-bytes", b"jpeg-bytes"]),
                ],
                fields=asset_fields,
            ),
        ],
        schema=pa.schema(
            [
                pa.field("_rowaddr", pa.uint64()),
                pa.field("asset", pa.struct(asset_fields)),
            ]
        ),
    )

    prepared = prepare_blob_v2_checkpoint_batch(
        batch,
        data_dir=str(tmp_path / "data"),
        data_file_name="fixed.lance",
        range_start=0,
    )

    prepared_payload = prepared.schema.field("asset").type.field("payload")
    assert pa.types.is_struct(prepared_payload.type)
    assert prepared_payload.metadata[b"ARROW:extension:name"] == b"lance.blob.v2"
    assert b"lance-encoding:blob" not in prepared_payload.metadata
    assert b"lance-encoding:blob-inline-size-threshold" not in (
        prepared_payload.metadata or {}
    )
    assert b"lance-encoding:blob-pack-file-size-threshold" not in (
        prepared_payload.metadata or {}
    )

    payload = prepared.column("asset").field("payload")
    assert payload.field("kind").to_pylist() == [1, 1]
    assert payload.field("data").to_pylist() == [None, None]


def test_checkpointing_applier_writes_descriptor_checkpoint_with_normal_key(
    tmp_path,
) -> None:
    ds_uri = str(tmp_path / "dataset")
    schema = _blob_batch().schema
    map_task = _MapTask(schema)
    applier = CheckpointingApplier(
        checkpoint_uri=str(tmp_path / "checkpoints"),
        map_task=map_task,  # type: ignore[arg-type]
        direct_fragment_write=DirectFragmentWriteConfig(
            ds_uri=ds_uri,
            column_names=["blob"],
            field_ids=[1],
            column_indices=[0],
            data_storage_version="2.2",
        ),
    )

    result = applier._checkpoint_single_batch(
        _Task(ds_uri),  # type: ignore[arg-type]
        _blob_batch(),
        dataset_uri=ds_uri,
        dataset_version=1,
        where=None,
        udf_rows=2,
        start=0,
        checkpoint_size=2,
    )

    assert result.checkpoint_key == map_task.checkpoint_key(
        dataset_uri=ds_uri,
        dataset_version=1,
        frag_id=7,
        start=0,
        end=2,
        where=None,
    )
    checkpoint_file = (
        Path(applier.checkpoint_store.uri()) / f"{result.checkpoint_key}.lance"
    )
    assert checkpoint_file.exists()

    stored = applier.checkpoint_store[result.checkpoint_key]
    stored_blob = stored.schema.field("blob")
    assert pa.types.is_struct(stored_blob.type)
    assert stored_blob.metadata[b"ARROW:extension:name"] == b"lance.blob.v2"
    stored_payload = stored.column("blob")
    assert stored_payload.field("kind").to_pylist() == [1, None]
    assert stored_payload.field("data").to_pylist() == [None, None]
    assert stored_payload.field("uri").to_pylist() == [None, None]
    assert stored_payload.field("blob_id").to_pylist() == [(1 << 32) - 1, None]
    assert stored_payload.field("blob_size").to_pylist() == [len(b"image-a"), None]
    assert stored_payload.field("position").to_pylist() == [0, None]


def test_checkpointing_applier_keeps_inline_checkpoint_before_blob_v2_storage_version(
    tmp_path,
) -> None:
    ds_uri = str(tmp_path / "dataset")
    schema = _blob_batch().schema
    map_task = _MapTask(schema)
    applier = CheckpointingApplier(
        checkpoint_uri=str(tmp_path / "checkpoints"),
        map_task=map_task,  # type: ignore[arg-type]
        direct_fragment_write=DirectFragmentWriteConfig(
            ds_uri=ds_uri,
            column_names=["blob"],
            field_ids=[1],
            column_indices=[0],
            data_storage_version="2.1",
        ),
    )

    result = applier._checkpoint_single_batch(
        _Task(ds_uri),  # type: ignore[arg-type]
        _blob_batch(),
        dataset_uri=ds_uri,
        dataset_version=1,
        where=None,
        udf_rows=2,
        start=0,
        checkpoint_size=2,
    )

    stored = applier.checkpoint_store[result.checkpoint_key]
    storage = _blob_storage(stored.column("blob"))
    assert _field_names(storage.type) == {"data", "uri", "position", "size"}
    assert storage.field("data").to_pylist() == [b"image-a", None]
    assert storage.field("uri").to_pylist() == [None, None]


@pytest.mark.parametrize(
    "data_storage_version",
    ["2.1", "2.2"],
)
def test_plan_read_uses_indexed_ranges_without_blob_checkpoint_payload_reads(
    db,
    tmp_path,
    data_storage_version: str,
) -> None:
    table = db.create_table(
        f"plan_blob_checkpoint_{data_storage_version.replace('.', '_')}",
        pa.table({"image_id": [1, 2, 3, 4]}),
        storage_options={"new_table_data_storage_version": data_storage_version},
    )
    assert lance.dataset(table.uri).data_storage_version == data_storage_version
    map_task = _MapTask(_blob_batch().schema)
    checkpoint_store = _NoPayloadReadFlatLanceCheckpointStore(
        str(tmp_path / f"checkpoints-{data_storage_version}")
    )
    src_files_hash = _source_files_hash_for_table(table.uri)
    base_prefix = map_task.checkpoint_prefix(
        dataset_uri=table.uri,
        where=None,
        column=None,
        src_files_hash=src_files_hash,
    )
    checkpoint_store[format_checkpoint_key(base_prefix, frag_id=0, start=0, end=2)] = (
        _blob_batch()
    )

    tasks, pipeline_args = plan_read(
        table.uri,
        table.get_reference(),
        ["image_id"],
        batch_size=2,
        task_size=2,
        map_task=map_task,  # type: ignore[arg-type]
        checkpoint_store=checkpoint_store,
    )

    task_list = list(tasks)
    # The covered run [0, 2) is planned too (reused from checkpoints, no
    # payload read at planning time); [2, 4) is recomputed.
    assert [(task.dest_offset(), task.num_rows()) for task in task_list] == [
        (0, 2),
        (2, 2),
    ]
    assert pipeline_args["skipped_stats"] == {"fragments": 0, "rows": 0}


def test_blob_v2_field_id_mapping_omits_descriptor_children(tmp_path) -> None:
    asset_type = pa.struct(
        [
            pa.field("mime_type", pa.string()),
            lance.blob_field("payload"),
        ]
    )
    asset = pa.StructArray.from_arrays(
        [
            pa.array(["image/png"]),
            lance.blob_array([b"png-bytes"]),
        ],
        fields=list(asset_type),
    )
    ds = lance.write_dataset(
        pa.table({"image_id": [1], "asset": asset}),
        str(tmp_path / "dataset"),
        data_storage_version="2.2",
    )

    default_ids, default_column_indices = extract_field_ids_and_column_indices(
        ds.lance_schema,
        ["asset"],
        ds.data_storage_version,
    )
    optimized_ids, optimized_column_indices = extract_field_ids_and_column_indices(
        ds.lance_schema,
        ["asset"],
        ds.data_storage_version,
        omit_special_leaf_children=True,
    )

    assert len(default_ids) > len(optimized_ids)
    assert len(optimized_ids) == len(optimized_column_indices)
    assert optimized_ids == [1, 2, 3]
    assert optimized_column_indices == [-1, 0, 1]
    assert default_column_indices[:3] == [-1, 0, 1]


def test_write_fragment_file_uses_supplied_data_file_name(tmp_path) -> None:
    ds_uri = str(tmp_path / "dataset")
    batch = pa.record_batch(
        [pa.array([1, 2], type=pa.int64())],
        schema=pa.schema([pa.field("value", pa.int64())]),
    )
    data_file_name = blob_v2_checkpoint_data_file_name("fragment-key")
    assert data_file_name == blob_v2_checkpoint_data_file_name("fragment-key")
    assert data_file_name != blob_v2_checkpoint_data_file_name("other-fragment-key")
    uuid.UUID(data_file_name.removesuffix(".lance"))

    data_file, rows, _elapsed = write_fragment_file(
        ds_uri,
        iter([batch]),
        column_names=["value"],
        field_ids=[1],
        column_indices=[0],
        data_storage_version="2.1",
        data_file_name=data_file_name,
    )

    assert rows == 2
    assert data_file.path == data_file_name
    assert (tmp_path / "dataset" / "data" / data_file_name).exists()


def test_blob_v2_checkpoint_data_file_name_helper_matches_dedupe_key(tmp_path) -> None:
    ds_uri = str(tmp_path / "dataset")
    map_task = _MapTask(_blob_batch().schema)
    src_files_hash = "src-hash"
    data_file_name = blob_v2_checkpoint_data_file_name_for_fragment(
        ds_uri,
        7,
        map_task,  # type: ignore[arg-type]
        dataset_version=12,
        src_files_hash=src_files_hash,
    )
    dedupe_key = map_task.checkpoint_prefix(
        dataset_uri=ds_uri,
        where=None,
        src_files_hash=src_files_hash,
    )

    assert data_file_name == blob_v2_checkpoint_data_file_name(f"{dedupe_key}_frag-7")


def _assert_nested_image_blob_backfill_uses_descriptor_checkpoints(
    db,
    monkeypatch: pytest.MonkeyPatch,
    table_name: str,
) -> None:
    asset_type = pa.struct(
        [
            pa.field("mime_type", pa.string()),
            lance.blob_field("payload"),
        ]
    )
    table = db.create_table(
        table_name,
        pa.table({"image_id": [1, 2, 3, 4], "text": ["cat", "dog", "owl", "fox"]}),
        storage_options={"new_table_data_storage_version": "2.2"},
    )
    ds = lance.dataset(table.uri)
    assert ds.data_storage_version == "2.2"

    @udf(data_type=asset_type, checkpoint_size=2, batch_size=2, num_cpus=0.1)
    def enrich(batch: pa.RecordBatch) -> pa.Array:
        image_ids = batch["image_id"].to_pylist()
        return pa.StructArray.from_arrays(
            [
                pa.array(["image/png"] * len(image_ids)),
                lance.blob_array([_image_payload(image_id) for image_id in image_ids]),
            ],
            fields=list(asset_type),
        )

    table.add_columns({"asset": enrich})
    test_path = os.path.abspath("src/tests")
    existing_pythonpath = os.environ.get("PYTHONPATH", "")
    monkeypatch.setenv(
        "PYTHONPATH",
        (
            f"{test_path}{os.pathsep}{existing_pythonpath}"
            if existing_pythonpath
            else test_path
        ),
    )
    with db.local_ray_context():
        table.backfill(
            "asset",
            concurrency=1,
            intra_applier_concurrency=1,
            batch_checkpoint_flush_interval_seconds=0,
            checkpoint_size=2,
            task_size=2,
            commit_granularity=1,
        )
    table = db.open_table(table_name)

    ds = lance.dataset(table.uri)
    assert ds.data_storage_version == "2.2"
    assets = ds.to_table(columns=["asset"]).column("asset").to_pylist()
    assert [asset["mime_type"] for asset in assets] == ["image/png"] * 4
    expected_payloads = [_image_payload(image_id) for image_id in [1, 2, 3, 4]]

    blob_files = ds.take_blobs("asset.payload", indices=[0, 1, 2, 3])
    assert [blob.read() for blob in blob_files] == expected_payloads

    output_field_ids, _ = extract_field_ids_and_column_indices(
        ds.lance_schema,
        ["asset"],
        ds.data_storage_version,
        omit_special_leaf_children=True,
    )
    output_files = [
        data_file.path
        for fragment in ds.get_fragments()
        for data_file in fragment.data_files()
        if list(data_file.fields) == output_field_ids
    ]
    assert len(output_files) == 1
    data_root = _local_path(table.uri) / "data"
    assert _lance_file_version(data_root / output_files[0]) == (2, 2)

    checkpoint_store = table.get_reference().open_checkpoint_store()
    checkpoint_keys = sorted(
        key
        for key in checkpoint_store.list_keys("udf-")
        if "_frag-" in key and "_range-" not in key
    )
    assert len(checkpoint_keys) == 1
    checkpoint_file = (
        _local_path(checkpoint_store.uri()) / f"{checkpoint_keys[0]}.lance"
    )
    assert checkpoint_file.exists()
    assert checkpoint_file.stat().st_size < sum(
        len(payload) for payload in expected_payloads
    )
    fragment_checkpoint = checkpoint_store[checkpoint_keys[0]].to_pydict()
    assert fragment_checkpoint == {
        "file": output_files,
        "output_field_ids": [str(output_field_ids)],
        "udf_version": [enrich.version],
    }

    main_file = data_root / output_files[0]
    sidecar_dir = data_root / output_files[0].removesuffix(".lance")
    sidecar_files = list(sidecar_dir.rglob("*.blob"))
    payload_bytes = sum(len(payload) for payload in expected_payloads)

    assert main_file.exists()
    assert sidecar_files
    assert sum(path.stat().st_size for path in sidecar_files) >= payload_bytes
    assert main_file.stat().st_size < payload_bytes // 2


@pytest.mark.ray
def test_backfill_nested_image_blob_uses_descriptor_checkpoints(
    db,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _assert_nested_image_blob_backfill_uses_descriptor_checkpoints(
        db,
        monkeypatch,
        table_name="nested_image_blob_v2",
    )
