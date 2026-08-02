# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests for UDTF checkpoint key helpers and store operations."""

import gc
from typing import ClassVar, cast

import pyarrow as pa
import pytest

import geneva.checkpoint_utils as checkpoint_utils
from geneva.checkpoint import InMemoryCheckpointStore
from geneva.checkpoint_utils import (
    format_chunker_checkpoint_prefix,
    format_chunker_fragment_key,
    format_chunker_work_item_key,
    format_udtf_batch_key,
    format_udtf_checkpoint_prefix,
    format_udtf_fragment_key,
    format_udtf_partition_prefix,
)

# ---------------------------------------------------------------------------
# Key helper tests
# ---------------------------------------------------------------------------


class TestUDTFCheckpointKeyHelpers:
    def test_format_checkpoint_prefix(self) -> None:
        prefix = format_udtf_checkpoint_prefix(
            udtf_name="dedup",
            udtf_version="abc123",
            source_version=42,
        )
        assert prefix == "udtf_dedup_abc123_src-42"

    def test_format_partition_prefix_unpartitioned(self) -> None:
        top = "udtf_dedup_abc123_src-42"
        result = format_udtf_partition_prefix(
            top, partition_col=None, partition_value=None
        )
        assert result == "udtf_dedup_abc123_src-42___all__"

    def test_format_partition_prefix_partitioned(self) -> None:
        top = "udtf_dedup_abc123_src-42"
        result = format_udtf_partition_prefix(
            top, partition_col="group", partition_value="a"
        )
        assert result == "udtf_dedup_abc123_src-42_group=a"

    def test_format_partition_prefix_sanitizes_underscores(self) -> None:
        top = "udtf_dedup_abc123_src-42"
        result = format_udtf_partition_prefix(
            top, partition_col="category", partition_value="foo_bar"
        )
        assert result == "udtf_dedup_abc123_src-42_category=foo-bar"

    def test_format_batch_key_zero_padded(self) -> None:
        part = "udtf_dedup_abc123_src-42_group=a"
        key = format_udtf_batch_key(part, 5)
        assert key == "udtf_dedup_abc123_src-42_group=a_batch-0005"

    def test_format_batch_key_zero(self) -> None:
        part = "udtf_dedup_abc123_src-42___all__"
        key = format_udtf_batch_key(part, 0)
        assert key == "udtf_dedup_abc123_src-42___all___batch-0000"

    def test_format_fragment_key(self) -> None:
        part = "udtf_dedup_abc123_src-42_group=a"
        key = format_udtf_fragment_key(part)
        assert key == "udtf_dedup_abc123_src-42_group=a_fragment"

    def test_sorted_batch_keys_numeric_order(self) -> None:
        part = "udtf_x_v1_src-1_group=a"
        keys = [format_udtf_batch_key(part, i) for i in [9, 0, 100, 3]]
        assert sorted(keys) == [
            format_udtf_batch_key(part, 0),
            format_udtf_batch_key(part, 3),
            format_udtf_batch_key(part, 9),
            format_udtf_batch_key(part, 100),
        ]


class TestChunkerCheckpointKeyHelpers:
    def test_format_chunker_checkpoint_prefix(self) -> None:
        prefix = format_chunker_checkpoint_prefix(
            chunker_name="clips",
            chunker_version="abc123",
            source_version=42,
        )
        assert prefix == "chunker_clips_abc123_src-42"
        assert "udtf" not in prefix

    def test_chunker_source_version_isolates_prefixes(self) -> None:
        prefix_v1 = format_chunker_checkpoint_prefix(
            chunker_name="clips",
            chunker_version="abc123",
            source_version=42,
        )
        prefix_v2 = format_chunker_checkpoint_prefix(
            chunker_name="clips",
            chunker_version="abc123",
            source_version=43,
        )
        assert prefix_v1 != prefix_v2
        assert prefix_v1.endswith("_src-42")
        assert prefix_v2.endswith("_src-43")

    def test_chunker_work_item_key_uses_rowid_range(self) -> None:
        prefix = "chunker_clips_abc123_src-42"
        key = format_chunker_work_item_key(prefix, [100, 101, 102])
        assert key == "chunker_clips_abc123_src-42_rowids-100-102"
        assert "srcfiles" not in key

    def test_chunker_work_item_key_is_deterministic_for_rowids(self) -> None:
        prefix = "chunker_clips_abc123_src-42"
        row_ids = [100, 101, 102]
        assert format_chunker_work_item_key(prefix, row_ids) == (
            format_chunker_work_item_key(prefix, tuple(row_ids))
        )

    @pytest.mark.slow
    def test_chunker_work_item_key_streams_normalized_rowids(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        class TrackedRowId(int):
            live: ClassVar[int] = 0
            peak: ClassVar[int] = 0

            def __new__(cls, value: int) -> "TrackedRowId":
                obj = int.__new__(cls, value)
                cls.live += 1
                cls.peak = max(cls.peak, cls.live)
                return cast("TrackedRowId", obj)

            def __del__(self) -> None:
                type(self).live -= 1

        def track_normalize(row_id: object) -> int:
            gc.collect()
            return TrackedRowId(int(cast("object", row_id)))

        monkeypatch.setattr(checkpoint_utils, "_normalize_row_id", track_normalize)

        key = format_chunker_work_item_key(
            "chunker_clips_abc123_src-42", range(100, 108)
        )

        gc.collect()
        assert key == "chunker_clips_abc123_src-42_rowids-100-107"
        assert TrackedRowId.peak <= 3
        assert TrackedRowId.live == 0

    @pytest.mark.parametrize("row_ids", [[100, 102], [102, 101, 100]])
    def test_chunker_work_item_key_rejects_non_contiguous_rowids(
        self, row_ids: list[int]
    ) -> None:
        prefix = "chunker_clips_abc123_src-42"

        with pytest.raises(ValueError, match="strictly ordered and contiguous"):
            format_chunker_work_item_key(prefix, row_ids)

    def test_chunker_fragment_key_uses_work_item_fragment_metadata_key(self) -> None:
        work_item_key = "chunker_clips_abc123_src-42_rowids-100-102"
        assert (
            format_chunker_fragment_key(work_item_key)
            == "chunker_clips_abc123_src-42_rowids-100-102_fragment"
        )


# ---------------------------------------------------------------------------
# Checkpoint store write/read tests
# ---------------------------------------------------------------------------


class TestUDTFCheckpointWriteRead:
    def test_write_read_roundtrip(self) -> None:
        store = InMemoryCheckpointStore()
        batch = pa.RecordBatch.from_pydict({"id": [1, 2], "val": [10.0, 20.0]})
        key = format_udtf_batch_key("udtf_x_v1_src-1___all__", 0)

        store[key] = batch
        assert key in store
        result = store[key]
        assert result.equals(batch)

    def test_list_partition_batches(self) -> None:
        store = InMemoryCheckpointStore()
        prefix_a = "udtf_x_v1_src-1_group=a"
        prefix_b = "udtf_x_v1_src-1_group=b"

        for i in range(3):
            batch = pa.RecordBatch.from_pydict({"id": [i]})
            store[format_udtf_batch_key(prefix_a, i)] = batch

        store[format_udtf_batch_key(prefix_b, 0)] = pa.RecordBatch.from_pydict(
            {"id": [99]}
        )

        a_keys = sorted(store.list_keys(prefix_a))
        assert len(a_keys) == 3
        # Ensure no prefix_b keys snuck in
        for k in a_keys:
            assert k.startswith(prefix_a)

    def test_fragment_key_signals_completion(self) -> None:
        store = InMemoryCheckpointStore()
        prefix = "udtf_x_v1_src-1___all__"
        frag_key = format_udtf_fragment_key(prefix)

        assert frag_key not in store

        store[frag_key] = pa.RecordBatch.from_pydict({"fragment_json": ["{}"]})
        assert frag_key in store
