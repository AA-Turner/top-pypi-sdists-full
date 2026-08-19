# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests for shared startup memory sampling."""

from typing import Any

import pyarrow as pa
import pytest

import geneva.query
from geneva.runners.ray.pipeline import _estimate_avg_row_bytes, _max_fragment_size


def test_max_fragment_size_uses_pinned_read_version(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeFragment:
        def __init__(self, physical_rows: int) -> None:
            self.physical_rows = physical_rows

    class FakeDataset:
        def get_fragments(self) -> list[FakeFragment]:
            return [FakeFragment(20), FakeFragment(75), FakeFragment(30)]

    calls: list[tuple[object, int | None]] = []

    def open_dataset(table: object, version: int | None = None) -> FakeDataset:
        calls.append((table, version))
        return FakeDataset()

    monkeypatch.setattr(geneva.query, "open_read_dataset", open_dataset)
    table = object()

    assert _max_fragment_size(table, read_version=42) == 75  # type: ignore[arg-type]
    assert calls == [(table, 42)]


def test_estimate_avg_row_bytes_samples_all_groups_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pa.table(
        {
            "input": pa.array([1, 2, 3], type=pa.int32()),
            "metadata": pa.array(
                [
                    {"left": 10, "right": 20},
                    {"left": 30, "right": 40},
                    {"left": 50, "right": 60},
                ]
            ),
            "output": pa.array(["a", "longer", "value"]),
        }
    )
    scanner_calls: list[tuple[list[str], int]] = []
    open_calls = 0

    class FakeScanner:
        def __init__(self, sample: pa.Table) -> None:
            self._sample = sample

        def to_table(self) -> pa.Table:
            return self._sample

    class FakeDataset:
        schema = source.schema

        def scanner(self, *, columns: list[str], limit: int) -> FakeScanner:
            scanner_calls.append((columns, limit))
            return FakeScanner(source.select(columns).slice(0, limit))

    versions: list[int | None] = []

    def open_dataset(_table: Any, version: int | None = None) -> FakeDataset:
        nonlocal open_calls
        open_calls += 1
        versions.append(version)
        return FakeDataset()

    monkeypatch.setattr(geneva.query, "open_read_dataset", open_dataset)

    estimates = _estimate_avg_row_bytes(
        object(),  # type: ignore[arg-type]
        {
            "input": ["input", "metadata.left"],
            "output": ["output", "metadata.right"],
        },
        read_version=7,
    )

    assert open_calls == 1
    # The sample must open the pinned snapshot, not the live table.
    assert versions == [7]
    assert scanner_calls == [(["input", "metadata", "output"], 128)]
    assert estimates == {
        "input": source.select(["input", "metadata"]).nbytes // source.num_rows,
        "output": source.select(["output", "metadata"]).nbytes // source.num_rows,
    }


def test_estimate_avg_row_bytes_applies_hint_to_each_group(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GENEVA_AVG_ROW_BYTES_HINT", "4096")

    def unexpected_open(_table: Any) -> None:
        raise AssertionError("dataset should not be opened when the hint is set")

    monkeypatch.setattr(geneva.query, "open_read_dataset", unexpected_open)

    assert _estimate_avg_row_bytes(
        object(),  # type: ignore[arg-type]
        {"input": ["a"], "output": ["b"]},
    ) == {"input": 4096, "output": 4096}


def test_estimate_avg_row_bytes_sees_through_blob_descriptors(tmp_path) -> None:  # noqa: ANN001
    """A blob column must be priced by its payload, not its descriptor.

    A plain scan of a ``lance-encoding:blob`` column yields
    ``struct<position, size>`` descriptors, so ``nbytes`` reports ~16 B/row
    however large the payload is. That number feeds ``resolve_read_task_rows``
    and the per-actor reservation, so a blob backfill -- the workload the memory
    model exists for -- would plan and reserve as if its rows were 16 bytes
    wide. Measured before the fix: 153,608 B/row unencoded versus 16 B/row for
    byte-identical blob-encoded values.
    """
    import geneva

    width = 150 * 1024
    payload = pa.table(
        {"payload": [b"x" * width, b"y" * width]},
        schema=pa.schema([pa.field("payload", pa.large_binary())]),
    )
    blob_payload = pa.table(
        {"payload": [b"x" * width, b"y" * width]},
        schema=pa.schema(
            [
                pa.field(
                    "payload",
                    pa.large_binary(),
                    metadata={"lance-encoding:blob": "true"},
                )
            ]
        ),
    )

    db = geneva.connect(str(tmp_path))
    plain = db.create_table("plain", payload)
    blob = db.create_table(
        "blob",
        blob_payload,
        storage_options={"new_table_data_storage_version": "2.0"},
    )

    plain_width = _estimate_avg_row_bytes(plain, {"x": ["payload"]})["x"]
    blob_width = _estimate_avg_row_bytes(blob, {"x": ["payload"]})["x"]

    assert plain_width is not None
    assert blob_width is not None
    # The two tables hold byte-identical values, so the widths must agree to
    # within the descriptor overhead the blob column additionally carries.
    assert blob_width >= width, (
        f"blob column priced at {blob_width} B/row, i.e. still the descriptor "
        "rather than the payload"
    )
    assert abs(blob_width - plain_width) <= 64, (
        f"blob {blob_width} vs plain {plain_width} B/row for identical values"
    )


def test_estimate_avg_row_bytes_follows_pinned_read_version(tmp_path) -> None:  # noqa: ANN001
    """The sample must read the snapshot the job reads, not the live table.

    A historical backfill pins ``read_version``. Sampling the live table sizes
    read tasks and the actor reservation from rows the job will never touch:
    with a 1 MiB payload at the pinned version and a narrow value written
    afterwards, the live sample reports single-digit bytes per row.
    """
    import geneva

    width = 1024 * 1024
    db = geneva.connect(str(tmp_path))
    tbl = db.create_table("t", pa.table({"payload": [b"a" * width, b"b" * width]}))
    pinned = tbl.version
    tbl.update(values={"payload": "z"})

    live = _estimate_avg_row_bytes(tbl, {"input": ["payload"]})["input"]
    at_pinned = _estimate_avg_row_bytes(
        tbl, {"input": ["payload"]}, read_version=pinned
    )["input"]

    assert live is not None
    assert at_pinned is not None
    assert live < 1_000, f"expected the live table to be narrow, got {live}"
    assert at_pinned > width * 0.9, (
        f"pinned sample read {at_pinned} B/row; it is still reading the live "
        "table rather than the pinned snapshot"
    )


def test_estimate_avg_row_bytes_sees_through_a_nested_blob_leaf(tmp_path) -> None:  # noqa: ANN001
    """The descriptor shape hides a blob one struct level down too.

    A scanned blob leaf arrives as a bare ``struct<position, size>`` with the
    ``lance-encoding:blob`` metadata stripped, so walking the *scanned* type to
    decide whether a struct holds a blob answers no, and the whole column falls
    through to descriptor bytes. Geneva supports these explicitly -- see
    ``nested_blob_paths`` and ``plan_struct_blob_decomposition`` -- so pricing
    them at ~16 B/row is the same bug as the top-level case, one level down.
    """
    import geneva

    width = 100 * 1024
    blob_leaf = pa.field(
        "image_bytes",
        pa.large_binary(),
        metadata={"lance-encoding:blob": "true"},
    )
    schema = pa.schema(
        [pa.field("image", pa.struct([pa.field("url", pa.string()), blob_leaf]))]
    )
    data = pa.table(
        {
            "image": [
                {"url": "a", "image_bytes": b"x" * width},
                {"url": "b", "image_bytes": b"y" * width},
            ]
        },
        schema=schema,
    )

    db = geneva.connect(str(tmp_path))
    tbl = db.create_table(
        "nested_blob",
        data,
        storage_options={"new_table_data_storage_version": "2.0"},
    )

    measured = _estimate_avg_row_bytes(tbl, {"input": ["image"]})["input"]

    assert measured is not None
    assert measured > width * 0.9, (
        f"nested blob leaf priced at {measured} B/row against a {width} B "
        "payload; it is still being counted as its descriptor"
    )
