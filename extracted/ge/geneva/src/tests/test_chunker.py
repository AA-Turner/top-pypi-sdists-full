# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging
from collections.abc import Iterator
from typing import NamedTuple

import lance
import pyarrow as pa
import pytest

import geneva
import geneva.cloudpickle as pickle
from geneva import connect
from geneva.db import Connection, dataset_uses_stable_row_ids
from geneva.packager import (
    ChunkerSpec,
    marshal_chunker,
    unmarshal_chunker,
)
from geneva.table import Table
from geneva.transformer import Chunker

pytestmark = pytest.mark.ray


# ---------------------------------------------------------------------------
# Shared types and helpers
# ---------------------------------------------------------------------------


class Clip(NamedTuple):
    clip_start: float
    clip_end: float


class ClipWithPath(NamedTuple):
    video_path: str
    clip_start: float
    clip_end: float


class Chunk(NamedTuple):
    chunk_text: str
    chunk_index: int


CLIP_SCHEMA = pa.schema(
    [
        pa.field("clip_start", pa.float64()),
        pa.field("clip_end", pa.float64()),
    ]
)


def _make_video_table(tmp_path, name: str = "videos") -> tuple[Connection, Table]:
    db = connect(tmp_path)
    data = pa.table(
        {
            "video_path": pa.array(["/v/a.mp4", "/v/b.mp4", "/v/c.mp4"]),
            "duration": pa.array([30.0, 20.0, 10.0]),
        }
    )
    tbl = db.create_table(
        name, data, storage_options={"new_table_enable_stable_row_ids": True}
    )
    return db, tbl


def _make_doc_table(tmp_path, name: str = "docs") -> tuple[Connection, Table]:
    db = connect(tmp_path)
    data = pa.table(
        {
            "doc_id": pa.array([1, 2]),
            "text": pa.array(
                [
                    "Hello world. How are you. Fine thanks.",
                    "One sentence only.",
                ]
            ),
        }
    )
    tbl = db.create_table(
        name, data, storage_options={"new_table_enable_stable_row_ids": True}
    )
    return db, tbl


# ---------------------------------------------------------------------------
# Unit: Chunker decorator and class
# ---------------------------------------------------------------------------


class TestChunkerDecorator:
    def test_basic_decorator_infers_schema(self) -> None:
        @geneva.chunker
        def extract_clips(
            duration: float,
        ) -> Iterator[Clip]:
            for start in range(0, int(duration), 10):
                end = min(start + 10, duration)
                yield Clip(clip_start=start, clip_end=end)

        assert isinstance(extract_clips, Chunker)
        assert extract_clips.output_schema == CLIP_SCHEMA
        assert extract_clips.input_columns == ["duration"]
        assert extract_clips.name == "extract_clips"
        assert extract_clips.batch is False

    def test_decorator_with_explicit_schema(self) -> None:
        @geneva.chunker(output_schema=CLIP_SCHEMA)
        def extract_clips(
            duration: float,
        ) -> Iterator[Clip]:
            for start in range(0, int(duration), 10):
                yield Clip(clip_start=start, clip_end=min(start + 10, duration))

        assert extract_clips.output_schema == CLIP_SCHEMA

    def test_decorator_with_input_columns(self) -> None:
        @geneva.chunker(input_columns=["dur"])
        def extract_clips(
            dur: float,
        ) -> Iterator[Clip]:
            yield Clip(clip_start=0, clip_end=dur)

        assert extract_clips.input_columns == ["dur"]

    def test_decorator_inherit_input_columns_flag(self) -> None:
        @geneva.chunker
        def defaults(duration: float) -> Iterator[Clip]:
            yield Clip(clip_start=0, clip_end=duration)

        assert defaults.inherit_input_columns is False

        @geneva.chunker(inherit_input_columns=True)
        def opted_in(duration: float) -> Iterator[Clip]:
            yield Clip(clip_start=0, clip_end=duration)

        assert opted_in.inherit_input_columns is True

    def test_decorator_batch_mode(self) -> None:
        @geneva.chunker(batch=True, output_schema=CLIP_SCHEMA)
        def batch_extract(
            duration: pa.Array,
            __source_row_id: pa.Array,
        ) -> pa.RecordBatch:
            return pa.RecordBatch.from_pydict(
                {
                    "__source_row_id": __source_row_id,
                    "clip_start": pa.array([0.0]),
                    "clip_end": duration,
                }
            )

        assert isinstance(batch_extract, Chunker)
        assert batch_extract.batch is True


# ---------------------------------------------------------------------------
# Unit: execute_on_record_batch (scalar mode)
# ---------------------------------------------------------------------------


class TestScalarExecution:
    def test_1_to_n_expansion(self) -> None:
        @geneva.chunker
        def extract_clips(
            duration: float,
        ) -> Iterator[Clip]:
            for start in range(0, int(duration), 10):
                end = min(start + 10, duration)
                yield Clip(clip_start=start, clip_end=end)

        batch = pa.RecordBatch.from_pydict(
            {
                "__source_row_id": pa.array([100, 200], type=pa.int64()),
                "duration": pa.array([25.0, 10.0]),
            }
        )

        result = extract_clips.execute_on_record_batch(batch)

        # Row 100 (duration=25): 3 clips [0-10, 10-20, 20-25]
        # Row 200 (duration=10): 1 clip [0-10]
        assert result.num_rows == 4

        src_ids = result["__source_row_id"].to_pylist()
        assert src_ids == [100, 100, 100, 200]

        child_indices = result["__child_index"].to_pylist()
        assert child_indices == [0, 1, 2, 0]

        starts = result["clip_start"].to_pylist()
        assert starts == [0.0, 10.0, 20.0, 0.0]

        ends = result["clip_end"].to_pylist()
        assert ends == [10.0, 20.0, 25.0, 10.0]

    def test_zero_yield_rows(self) -> None:
        """A source row can produce zero output rows."""

        @geneva.chunker
        def maybe_expand(
            value: int,
        ) -> Iterator[Clip]:
            if value > 10:
                yield Clip(clip_start=0, clip_end=float(value))

        batch = pa.RecordBatch.from_pydict(
            {
                "__source_row_id": pa.array([1, 2, 3], type=pa.int64()),
                "value": pa.array([5, 20, 3]),
            }
        )

        result = maybe_expand.execute_on_record_batch(batch)
        # Only row 2 (value=20) yields output
        assert result.num_rows == 1
        assert result["__source_row_id"].to_pylist() == [2]

    def test_dict_yield(self) -> None:
        @geneva.chunker(output_schema=CLIP_SCHEMA)
        def extract_clips(
            duration: float,
        ) -> Iterator[dict]:
            yield {"clip_start": 0.0, "clip_end": duration}

        batch = pa.RecordBatch.from_pydict(
            {
                "__source_row_id": pa.array([1], type=pa.int64()),
                "duration": pa.array([10.0]),
            }
        )

        result = extract_clips.execute_on_record_batch(batch)
        assert result.num_rows == 1
        assert result["clip_end"].to_pylist() == [10.0]


@geneva.chunker(batch=True, output_schema=CLIP_SCHEMA)
def _batch_three_clips(
    duration: pa.Array,
    __source_row_id: pa.Array,
) -> pa.RecordBatch:
    """Batch chunker emitting 3 clips per source row (module-level to avoid
    name-mangling of ``__source_row_id``)."""
    src = __source_row_id.to_pylist()
    ids, starts, ends = [], [], []
    for sid in src:
        for _ in range(3):
            ids.append(sid)
            starts.append(0.0)
            ends.append(10.0)
    return pa.RecordBatch.from_pydict(
        {
            "__source_row_id": pa.array(ids, type=pa.int64()),
            "clip_start": pa.array(starts, type=pa.float64()),
            "clip_end": pa.array(ends, type=pa.float64()),
        }
    )


def _make_counting_batch_chunker() -> tuple["geneva.transformer.Chunker", list]:
    """A batch chunker (3 clips/source row) that records the input row count of
    every ``func`` invocation (module-level to avoid ``__source_row_id``
    name-mangling inside a class body)."""
    calls: list[int] = []

    @geneva.chunker(batch=True, output_schema=CLIP_SCHEMA)
    def counting(
        duration: pa.Array,
        __source_row_id: pa.Array,
    ) -> pa.RecordBatch:
        calls.append(len(__source_row_id))
        src = __source_row_id.to_pylist()
        ids, starts, ends = [], [], []
        for sid in src:
            for i in range(3):
                ids.append(sid)
                starts.append(float(i))
                ends.append(float(i + 1))
        return pa.RecordBatch.from_pydict(
            {
                "__source_row_id": pa.array(ids, type=pa.int64()),
                "clip_start": pa.array(starts, type=pa.float64()),
                "clip_end": pa.array(ends, type=pa.float64()),
            }
        )

    return counting, calls


class TestStreamingIteration:
    """Unit tests for ``execute_on_record_batch_iter`` (memory-bounding)."""

    @staticmethod
    def _clips_chunker() -> "geneva.transformer.Chunker":
        @geneva.chunker
        def extract_clips(duration: float) -> Iterator[Clip]:
            for start in range(0, int(duration), 10):
                yield Clip(clip_start=start, clip_end=min(start + 10, duration))

        return extract_clips

    def _batch(self) -> pa.RecordBatch:
        # 3 + 2 + 1 = 6 output rows.
        return pa.RecordBatch.from_pydict(
            {
                "__source_row_id": pa.array([100, 200, 300], type=pa.int64()),
                "duration": pa.array([30.0, 20.0, 10.0]),
            }
        )

    @pytest.mark.parametrize("max_rows", [None, 1, 2, 3, 5, 100])
    def test_parity_with_single_shot(self, max_rows) -> None:
        """Concatenating the stream equals the single-shot expansion."""
        chunker = self._clips_chunker()
        batch = self._batch()
        full = chunker.execute_on_record_batch(batch)

        subs = list(chunker.execute_on_record_batch_iter(batch, max_rows=max_rows))
        cat = pa.Table.from_batches(subs).combine_chunks().to_batches()[0]

        assert cat.num_rows == full.num_rows
        for col in full.schema.names:
            assert cat[col].to_pylist() == full[col].to_pylist()

    def test_none_yields_single_batch(self) -> None:
        chunker = self._clips_chunker()
        subs = list(chunker.execute_on_record_batch_iter(self._batch(), max_rows=None))
        assert len(subs) == 1
        assert subs[0].num_rows == 6

    def test_bounded_sub_batches(self) -> None:
        """With fanout==1, each sub-batch holds exactly ``max_rows`` (last is
        the remainder), and the count is ``ceil(total / max_rows)``."""

        @geneva.chunker
        def one_each(duration: float) -> Iterator[Clip]:
            yield Clip(clip_start=0.0, clip_end=duration)

        batch = pa.RecordBatch.from_pydict(
            {
                "__source_row_id": pa.array(list(range(20)), type=pa.int64()),
                "duration": pa.array([10.0] * 20),
            }
        )
        subs = list(one_each.execute_on_record_batch_iter(batch, max_rows=7))
        assert [s.num_rows for s in subs] == [7, 7, 6]

    def test_source_row_not_split(self) -> None:
        """A single source row's children are never split across sub-batches,
        even when its fanout exceeds ``max_rows``."""
        chunker = self._clips_chunker()
        # One source row with fanout 5 (> max_rows=2).
        batch = pa.RecordBatch.from_pydict(
            {
                "__source_row_id": pa.array([7], type=pa.int64()),
                "duration": pa.array([50.0]),
            }
        )
        subs = list(chunker.execute_on_record_batch_iter(batch, max_rows=2))
        assert len(subs) == 1
        assert subs[0].num_rows == 5
        assert subs[0]["__child_index"].to_pylist() == [0, 1, 2, 3, 4]

    def test_zero_yield_emits_no_empty_sub_batches(self) -> None:
        """Source rows yielding nothing produce no empty streamed sub-batches."""

        @geneva.chunker
        def maybe(value: int) -> Iterator[Clip]:
            if value > 10:
                yield Clip(clip_start=0.0, clip_end=float(value))

        batch = pa.RecordBatch.from_pydict(
            {
                "__source_row_id": pa.array([1, 2, 3], type=pa.int64()),
                "value": pa.array([5, 20, 3]),
            }
        )
        subs = list(maybe.execute_on_record_batch_iter(batch, max_rows=2))
        assert sum(s.num_rows for s in subs) == 1
        assert all(s.num_rows > 0 for s in subs)

    def test_batch_mode_slicing(self) -> None:
        """Batch-mode chunkers slice their single result into bounded pieces."""
        batch = pa.RecordBatch.from_pydict(
            {
                "__source_row_id": pa.array([1, 2], type=pa.int64()),
                "duration": pa.array([10.0, 10.0]),
            }
        )
        # 2 source rows x 3 = 6 output rows; max_rows=4 -> [4, 2].
        subs = list(_batch_three_clips.execute_on_record_batch_iter(batch, max_rows=4))
        assert [s.num_rows for s in subs] == [4, 2]

    @staticmethod
    def _counting_batch_chunker() -> tuple["geneva.transformer.Chunker", list]:
        return _make_counting_batch_chunker()

    def _batch_input(self, n: int) -> pa.RecordBatch:
        return pa.RecordBatch.from_pydict(
            {
                "__source_row_id": pa.array(list(range(n)), type=pa.int64()),
                "duration": pa.array([10.0] * n),
            }
        )

    @pytest.mark.parametrize("max_rows", [1, 2, 3, 4, 5])
    def test_batch_mode_chunks_input(self, max_rows) -> None:
        """The batch func is invoked once per ``<= max_rows`` source-row chunk,
        each call receiving at most ``max_rows`` input rows — proving peak memory
        is bounded by the chunk size, not the full input."""
        chunker, calls = self._counting_batch_chunker()
        n = 5
        list(chunker.execute_on_record_batch_iter(self._batch_input(n), max_rows))

        import math

        assert len(calls) == math.ceil(n / max_rows)
        assert all(c <= max_rows for c in calls)
        assert sum(calls) == n  # every source row processed exactly once

    @pytest.mark.parametrize("max_rows", [None, 0, 1, 2, 3, 4, 7, 100])
    def test_batch_mode_parity_with_single_shot(self, max_rows) -> None:
        """Concatenating the chunked stream equals the single-shot expansion,
        including ``__child_index``, regardless of input chunking."""
        chunker, _ = self._counting_batch_chunker()
        batch = self._batch_input(5)
        full = chunker.execute_on_record_batch(batch)

        subs = list(chunker.execute_on_record_batch_iter(batch, max_rows=max_rows))
        cat = pa.Table.from_batches(subs).combine_chunks().to_batches()[0]

        assert cat.num_rows == full.num_rows
        for col in full.schema.names:
            assert cat[col].to_pylist() == full[col].to_pylist()

    def test_batch_mode_none_single_call(self) -> None:
        """``max_rows=None`` expands the whole input in a single func call."""
        chunker, calls = self._counting_batch_chunker()
        subs = list(
            chunker.execute_on_record_batch_iter(self._batch_input(5), max_rows=None)
        )
        assert calls == [5]
        assert len(subs) == 1
        assert subs[0].num_rows == 15

    def test_batch_mode_output_sub_batches_bounded(self) -> None:
        """Each yielded sub-batch holds ``<= max_rows`` rows even when one chunk's
        expansion exceeds ``max_rows`` (fanout 3, chunk of 2 -> 6 output rows)."""
        chunker, _ = self._counting_batch_chunker()
        subs = list(
            chunker.execute_on_record_batch_iter(self._batch_input(4), max_rows=2)
        )
        assert all(s.num_rows <= 2 for s in subs)
        assert sum(s.num_rows for s in subs) == 12

    def test_batch_mode_empty_input(self) -> None:
        """Empty input yields a single empty batch with the right schema."""
        chunker, calls = self._counting_batch_chunker()
        subs = list(
            chunker.execute_on_record_batch_iter(self._batch_input(0), max_rows=2)
        )
        assert len(subs) == 1
        assert subs[0].num_rows == 0
        assert set(subs[0].schema.names) == set(chunker.expanded_output_schema.names)


class TestSerialization:
    def test_marshal_unmarshal_round_trip(self) -> None:
        @geneva.chunker
        def extract_clips(
            duration: float,
        ) -> Iterator[Clip]:
            for start in range(0, int(duration), 10):
                yield Clip(
                    clip_start=start,
                    clip_end=min(start + 10, duration),
                )

        spec = marshal_chunker(extract_clips)
        assert isinstance(spec, ChunkerSpec)
        assert spec.name == "extract_clips"

        # Round-trip via JSON
        json_str = spec.to_json()
        spec2 = ChunkerSpec.from_json(json_str)
        assert spec2.name == spec.name
        assert spec2.version == spec.version

        # Unmarshal
        restored = unmarshal_chunker(spec2)
        assert isinstance(restored, Chunker)
        assert restored.name == "extract_clips"
        assert restored.output_schema == CLIP_SCHEMA

    def test_round_trip_preserves_inherit_input_columns(self) -> None:
        @geneva.chunker(inherit_input_columns=False)
        def extract_clips(
            duration: float,
        ) -> Iterator[Clip]:
            yield Clip(clip_start=0, clip_end=duration)

        restored = unmarshal_chunker(marshal_chunker(extract_clips))
        assert isinstance(restored, Chunker)
        assert restored.inherit_input_columns is False

    def test_unpickle_old_payload_missing_field(self) -> None:
        """A Chunker pickled before inherit_input_columns existed still loads.

        Chunker MVs store the chunker as a whole cloudpickle (see
        marshal_chunker). A view created before the field was added unpickles
        into the current slotted class with that slot unset; without the
        backward-compat shim the next __getstate__ (triggered when Ray
        re-pickles the chunker into the actor on refresh) raises AttributeError.
        """

        @geneva.chunker
        def extract_clips(duration: float) -> Iterator[Clip]:
            yield Clip(clip_start=0, clip_end=duration)

        # Simulate an old payload: state without the newer field.
        old_state = extract_clips.__getstate__()
        del old_state["inherit_input_columns"]

        # Unpickle path: __new__ + __setstate__ backfills the missing field.
        restored = Chunker.__new__(Chunker)
        restored.__setstate__(old_state)
        assert restored.inherit_input_columns is False

        # Ray re-pickle path: __getstate__ must not raise on the (now filled)
        # slot, and a full round-trip preserves the default.
        round_tripped = pickle.loads(pickle.dumps(restored))
        assert isinstance(round_tripped, Chunker)
        assert round_tripped.inherit_input_columns is False


class TestCreateAndRefresh:
    def test_empty_source_stable_row_id_detection(self, tmp_path) -> None:
        db = connect(tmp_path)
        stable = db.create_table(
            "stable_empty",
            pa.table({"duration": pa.array([], type=pa.float64())}),
            storage_options={"new_table_enable_stable_row_ids": True},
        )
        unstable = db.create_table(
            "unstable_empty",
            pa.table({"duration": pa.array([], type=pa.float64())}),
        )

        assert dataset_uses_stable_row_ids(stable.to_lance()) is True
        assert dataset_uses_stable_row_ids(unstable.to_lance()) is False

    def test_create_view_empty(self, tmp_path) -> None:
        db, videos = _make_video_table(tmp_path)

        @geneva.chunker(inherit_input_columns=True)
        def extract_clips(
            duration: float,
        ) -> Iterator[Clip]:
            for start in range(0, int(duration), 10):
                yield Clip(
                    clip_start=start,
                    clip_end=min(start + 10, duration),
                )

        query = videos.search(None).select(["video_path", "duration"])
        view = db.create_udtf_view("clips", query, extract_clips)

        assert view.count_rows() == 0
        schema = view.schema
        assert "__source_row_id" in schema.names
        assert "__child_index" in schema.names
        assert "video_path" in schema.names
        assert "duration" in schema.names
        assert "clip_start" in schema.names
        assert "clip_end" in schema.names

    def test_refresh_warns_when_manifest_not_applied(
        self, tmp_path, ray_with_test_path, caplog
    ) -> None:
        """A chunker manifest cannot shape workers on a local refresh."""
        from geneva.manifest import GenevaManifest

        db, videos = _make_video_table(tmp_path)

        @geneva.chunker(
            inherit_input_columns=True,
            manifest=GenevaManifest.create_pip("chunker-env").pip(["numpy"]).build(),
        )
        def extract_clips(duration: float) -> Iterator[Clip]:
            for start in range(0, int(duration), 10):
                yield Clip(clip_start=start, clip_end=min(start + 10, duration))

        query = videos.search(None).select(["video_path", "duration"])
        view = db.create_udtf_view("warn_clips", query, extract_clips)

        with caplog.at_level(logging.WARNING):
            view.refresh(_admission_check=False)

        assert "is not applied to this refresh" in caplog.text
        assert "extract_clips" in caplog.text
        assert view.count_rows() == 6

    def test_refresh_expands_rows(self, tmp_path, ray_with_test_path) -> None:
        db, videos = _make_video_table(tmp_path)

        @geneva.chunker(inherit_input_columns=True)
        def extract_clips(
            duration: float,
        ) -> Iterator[Clip]:
            for start in range(0, int(duration), 10):
                yield Clip(
                    clip_start=start,
                    clip_end=min(start + 10, duration),
                )

        query = videos.search(None).select(["video_path", "duration"])
        view = db.create_udtf_view("clips", query, extract_clips)

        view.refresh(_admission_check=False)

        # video a: duration=30 -> 3 clips
        # video b: duration=20 -> 2 clips
        # video c: duration=10 -> 1 clip
        # Total: 6 clips
        assert view.count_rows() == 6

        result = view.to_pandas()
        # Check inherited columns are present
        assert "video_path" in result.columns
        assert "duration" in result.columns
        # Check UDTF output columns
        assert "clip_start" in result.columns
        assert "clip_end" in result.columns
        # Check internal columns
        assert "__source_row_id" in result.columns
        assert "__child_index" in result.columns

    def test_create_warns_without_stable_row_ids(self, tmp_path) -> None:
        db = connect(tmp_path)
        videos = db.create_table(
            "videos_no_stable",
            pa.table(
                {
                    "video_path": ["/v/a.mp4"],
                    "duration": [30.0],
                }
            ),
        )

        @geneva.chunker
        def extract_clips(
            duration: float,
        ) -> Iterator[Clip]:
            yield Clip(clip_start=0, clip_end=duration)

        query = videos.search(None).select(["video_path", "duration"])
        with pytest.warns(UserWarning, match="same source version"):
            db.create_udtf_view("clips_warn", query, extract_clips)

    def test_inherited_columns_correct(self, tmp_path, ray_with_test_path) -> None:
        db, videos = _make_video_table(tmp_path)

        @geneva.chunker(inherit_input_columns=True)
        def extract_clips(
            duration: float,
        ) -> Iterator[Clip]:
            for start in range(0, int(duration), 10):
                yield Clip(
                    clip_start=start,
                    clip_end=min(start + 10, duration),
                )

        query = videos.search(None).select(["video_path", "duration"])
        view = db.create_udtf_view("clips", query, extract_clips)
        view.refresh(_admission_check=False)

        result = view.to_pandas()
        # All clips from video a should inherit video_path="/v/a.mp4"
        a_clips = result[result["video_path"] == "/v/a.mp4"]
        assert len(a_clips) == 3
        assert all(a_clips["duration"] == 30.0)

        # All clips from video c should have video_path="/v/c.mp4"
        c_clips = result[result["video_path"] == "/v/c.mp4"]
        assert len(c_clips) == 1
        assert c_clips.iloc[0]["clip_start"] == 0.0
        assert c_clips.iloc[0]["clip_end"] == 10.0

    def test_inherit_input_columns_false_excludes_input(
        self, tmp_path, ray_with_test_path
    ) -> None:
        db, videos = _make_video_table(tmp_path)

        @geneva.chunker(inherit_input_columns=False)
        def extract_clips(
            duration: float,
        ) -> Iterator[Clip]:
            for start in range(0, int(duration), 10):
                yield Clip(clip_start=start, clip_end=min(start + 10, duration))

        query = videos.search(None).select(["video_path", "duration"])
        view = db.create_udtf_view("clips", query, extract_clips)
        view.refresh(_admission_check=False)

        result = view.to_pandas()
        # The input column (duration) is not copied into the view...
        assert "duration" not in result.columns
        # ...but other projected source columns still are, and expansion still
        # works (the chunker read `duration` to produce clips).
        assert "video_path" in result.columns
        assert set(result["video_path"]) == {"/v/a.mp4", "/v/b.mp4", "/v/c.mp4"}
        assert len(result) == 6  # 30/10 + 20/10 + 10/10

    def test_inherit_input_columns_false_output_recaptures_input(
        self, tmp_path, ray_with_test_path
    ) -> None:
        # A chunker can opt out of inheriting its (large) input columns yet
        # still bring select parent columns into the child MV by emitting them
        # in its output. Here both input columns are excluded from the
        # inherited schema, but video_path is re-captured via the Clip output.
        db, videos = _make_video_table(tmp_path)

        @geneva.chunker(inherit_input_columns=False)
        def extract_clips(
            video_path: str,
            duration: float,
        ) -> Iterator[ClipWithPath]:
            for start in range(0, int(duration), 10):
                yield ClipWithPath(
                    video_path=video_path,
                    clip_start=start,
                    clip_end=min(start + 10, duration),
                )

        assert set(extract_clips.input_columns) == {"video_path", "duration"}

        query = videos.search(None).select(["video_path", "duration"])
        view = db.create_udtf_view("clips", query, extract_clips)
        view.refresh(_admission_check=False)

        result = view.to_pandas()
        # duration is an input column and is excluded from the view...
        assert "duration" not in result.columns
        # ...while video_path, also an input column, is brought back into the
        # view because the chunker emits it in its output.
        assert "video_path" in result.columns
        assert set(result["video_path"]) == {"/v/a.mp4", "/v/b.mp4", "/v/c.mp4"}
        assert len(result) == 6  # 30/10 + 20/10 + 10/10

    def test_zero_yield_source_row(self, tmp_path, ray_with_test_path) -> None:
        """Source rows that yield zero output are valid."""
        db, docs = _make_doc_table(tmp_path)

        @geneva.chunker
        def split_long_text(
            text: str,
        ) -> Iterator[Chunk]:
            sentences = text.split(". ")
            if len(sentences) > 1:
                for i, s in enumerate(sentences):
                    yield Chunk(chunk_text=s, chunk_index=i)
            # Single-sentence docs yield nothing

        query = docs.search(None).select(["doc_id", "text"])
        view = db.create_udtf_view("chunks", query, split_long_text)
        view.refresh(_admission_check=False)

        # Doc 1 has 3 sentences -> 3 chunks
        # Doc 2 has 1 sentence -> 0 chunks
        assert view.count_rows() == 3

    def test_empty_source_table(self, tmp_path, ray_with_test_path) -> None:
        """Refresh with no source rows produces empty view."""
        db = connect(tmp_path)
        empty_data = pa.table(
            {
                "duration": pa.array([], type=pa.float64()),
            }
        )
        src = db.create_table(
            "empty_src",
            empty_data,
            storage_options={"new_table_enable_stable_row_ids": True},
        )

        @geneva.chunker
        def extract_clips(
            duration: float,
        ) -> Iterator[Clip]:
            yield Clip(clip_start=0, clip_end=duration)

        query = src.search(None)
        view = db.create_udtf_view("clips", query, extract_clips)
        view.refresh(_admission_check=False)
        assert view.count_rows() == 0

    def test_double_refresh(self, tmp_path, ray_with_test_path) -> None:
        """Refreshing twice overwrites with same results."""
        db, videos = _make_video_table(tmp_path)

        @geneva.chunker
        def extract_clips(
            duration: float,
        ) -> Iterator[Clip]:
            for start in range(0, int(duration), 10):
                yield Clip(
                    clip_start=start,
                    clip_end=min(start + 10, duration),
                )

        query = videos.search(None).select(["video_path", "duration"])
        view = db.create_udtf_view("clips", query, extract_clips)

        view.refresh(_admission_check=False)
        assert view.count_rows() == 6

        # Second refresh should produce the same result (no new source rows)
        view.refresh(_admission_check=False)
        assert view.count_rows() == 6

    def test_incremental_refresh(self, tmp_path, ray_with_test_path) -> None:
        """Adding source rows and refreshing appends only the new expansions."""
        db, videos = _make_video_table(tmp_path)

        @geneva.chunker
        def extract_clips(
            duration: float,
        ) -> Iterator[Clip]:
            for start in range(0, int(duration), 10):
                yield Clip(
                    clip_start=start,
                    clip_end=min(start + 10, duration),
                )

        query = videos.search(None).select(["video_path", "duration"])
        view = db.create_udtf_view("clips", query, extract_clips)

        view.refresh(_admission_check=False)
        initial_rows = view.count_rows()
        assert initial_rows == 6

        # Add a new source row (duration=5 → 1 clip)
        videos.add(
            pa.table(
                {
                    "video_path": ["new.mp4"],
                    "duration": [5.0],
                }
            )
        )

        # Refresh should pick up only the new row
        view.refresh(_admission_check=False)
        assert view.count_rows() == initial_rows + 1

    def test_cross_version_refresh_without_stable_row_ids_fails_before_delete(
        self, tmp_path, monkeypatch
    ) -> None:
        db = connect(tmp_path)
        videos = db.create_table(
            "videos_no_stable_refresh",
            pa.table(
                {
                    "video_path": ["/v/a.mp4"],
                    "duration": [30.0],
                }
            ),
        )

        @geneva.chunker
        def extract_clips(
            duration: float,
        ) -> Iterator[Clip]:
            yield Clip(clip_start=0, clip_end=duration)

        query = videos.search(None).select(["video_path", "duration"])
        with pytest.warns(UserWarning, match="same source version"):
            view = db.create_udtf_view("clips_guard", query, extract_clips)

        base_version = videos.version
        videos.add(
            pa.table(
                {
                    "video_path": ["new.mp4"],
                    "duration": [5.0],
                }
            )
        )
        cross_version = videos.version
        assert cross_version > base_version

        from geneva.runners.ray import pipeline as ray_pipeline

        def fail_delete(*_args, **_kwargs) -> None:
            raise AssertionError("_delete_stale_mv_rows should not be called")

        monkeypatch.setattr(ray_pipeline, "_delete_stale_mv_rows", fail_delete)

        with pytest.raises(ValueError, match="stable row IDs"):
            ray_pipeline.run_ray_copy_table(
                view.get_reference(),
                db._packager,
                view.get_reference().open_checkpoint_store(),
                src_version=cross_version,
            )

        assert view.count_rows() == 0

    def test_input_columns_validation_against_projection(self, tmp_path) -> None:
        """input_columns should be validated against query projection."""
        db, videos = _make_video_table(tmp_path)

        @geneva.chunker(input_columns=["duration"])
        def extract_clips(
            duration: float,
        ) -> Iterator[Clip]:
            yield Clip(clip_start=0, clip_end=duration)

        # Select only video_path — duration is NOT in the projection
        query = videos.search(None).select(["video_path"])

        with pytest.raises(ValueError, match="not found in query projection"):
            db.create_udtf_view("clips", query, extract_clips)


_BATCH_EXTRACT_SCHEMA = pa.schema(
    [
        pa.field("clip_start", pa.float64()),
        pa.field("clip_end", pa.float64()),
    ]
)


# Defined at module level to avoid Python name mangling of __source_row_id
@geneva.chunker(batch=True, output_schema=_BATCH_EXTRACT_SCHEMA)
def _batch_extract(
    duration: pa.Array,
    __source_row_id: pa.Array,
) -> pa.RecordBatch:
    starts = []
    ends = []
    src_ids = []
    for i in range(len(duration)):
        dur = duration[i].as_py()
        sid = __source_row_id[i].as_py()
        for s in range(0, int(dur), 10):
            starts.append(float(s))
            ends.append(min(float(s + 10), dur))
            src_ids.append(sid)
    return pa.RecordBatch.from_pydict(
        {
            "__source_row_id": pa.array(src_ids, type=pa.int64()),
            "clip_start": pa.array(starts),
            "clip_end": pa.array(ends),
        }
    )


@geneva.chunker(batch=True, output_schema=CLIP_SCHEMA)
def _batch_fn(
    duration: pa.Array,
    __source_row_id: pa.Array,
) -> pa.RecordBatch:
    return pa.RecordBatch.from_pydict(
        {
            "__source_row_id": __source_row_id,
            "clip_start": pa.array([0.0]),
            "clip_end": pa.array([1.0]),
        }
    )


class TestBatchExecution:
    def test_batch_mode_execution(self) -> None:
        """batch=True variant processes Arrow Arrays."""
        batch = pa.RecordBatch.from_pydict(
            {
                "__source_row_id": pa.array([100, 200], type=pa.int64()),
                "duration": pa.array([25.0, 10.0]),
            }
        )

        result = _batch_extract.execute_on_record_batch(batch)
        assert result.num_rows == 4
        assert result["__source_row_id"].to_pylist() == [
            100,
            100,
            100,
            200,
        ]
        assert "__child_index" in result.schema.names

    def test_batch_mode_infers_input_columns(self) -> None:
        """batch=True infers input_columns, excluding __source_row_id."""
        assert _batch_fn.input_columns == ["duration"]


class TestErrorHandling:
    def test_skip_on_error(self) -> None:
        """on_error with Skip skips failing rows."""
        from geneva.debug.error_store import Skip

        @geneva.chunker(on_error=[Skip(ValueError)])
        def flaky_expand(
            value: int,
        ) -> Iterator[Clip]:
            if value == 2:
                raise ValueError("bad row")
            yield Clip(clip_start=0, clip_end=float(value))

        batch = pa.RecordBatch.from_pydict(
            {
                "__source_row_id": pa.array([1, 2, 3], type=pa.int64()),
                "value": pa.array([10, 2, 30]),
            }
        )

        result = flaky_expand.execute_on_record_batch(batch)
        # Row 2 (value=2) raises ValueError -> skipped
        assert result.num_rows == 2
        assert result["__source_row_id"].to_pylist() == [1, 3]

    def test_fail_on_error_default(self) -> None:
        """Without on_error, exceptions propagate."""

        @geneva.chunker
        def always_fail(
            value: int,
        ) -> Iterator[Clip]:
            raise ValueError("boom")
            yield  # noqa: RET503

        batch = pa.RecordBatch.from_pydict(
            {
                "__source_row_id": pa.array([1], type=pa.int64()),
                "value": pa.array([10]),
            }
        )

        with pytest.raises(ValueError, match="boom"):
            always_fail.execute_on_record_batch(batch)


class TestWideTableUDTF:
    """Verify UDTF works correctly with wide tables (many columns)."""

    def test_wide_table_with_1_to_n_expansion(
        self, tmp_path, ray_with_test_path
    ) -> None:
        """UDTF on a wide table with 1-to-N expansion.

        Ensures correctness when the source table has many columns but
        the query selects only a few, and each row can produce multiple
        output rows.
        """
        db = connect(tmp_path)
        # Create a wide table with 50 columns
        durations = [25.0, 10.0, 35.0, 5.0, 20.0, 15.0, 40.0, 30.0, 10.0, 50.0]
        data = {"key": list(range(10)), "duration": durations}
        for i in range(48):
            data[f"extra_{i}"] = list(range(10))
        source = db.create_table("wide_videos", pa.table(data))

        @geneva.chunker(inherit_input_columns=True)
        def extract_clips(
            duration: float,
        ) -> Iterator[Clip]:
            for start in range(0, int(duration), 10):
                end = min(start + 10, duration)
                yield Clip(clip_start=float(start), clip_end=end)

        query = source.search(None).select(["key", "duration"])
        view = db.create_udtf_view("wide_clips", query, extract_clips)
        view.refresh(_admission_check=False)

        # Expected clips per row: 3,1,4,1,2,2,4,3,1,5 = 26 total
        assert view.count_rows() == 26
        result = view.to_pandas()
        assert "key" in result.columns
        assert "duration" in result.columns
        assert "clip_start" in result.columns
        assert "clip_end" in result.columns
        # Verify no extra columns leaked into the view
        for i in range(48):
            assert f"extra_{i}" not in result.columns


class TestLimitHandling:
    """Verify .limit(N) is enforced globally for scalar UDTF views."""

    def test_chunker_limit_across_fragments(self, tmp_path, ray_with_test_path) -> None:
        db = connect(tmp_path)
        # Create source with many rows across multiple fragments
        data0 = pa.table(
            {
                "video_path": [f"/v/{i}.mp4" for i in range(10)],
                "duration": [10.0] * 10,
            }
        )
        source = db.create_table("videos_limit", data0)
        # Add more fragments
        for batch_start in range(10, 40, 10):
            source.add(
                pa.table(
                    {
                        "video_path": [
                            f"/v/{i}.mp4" for i in range(batch_start, batch_start + 10)
                        ],
                        "duration": [10.0] * 10,
                    }
                )
            )
        assert source.count_rows() == 40

        @geneva.chunker
        def extract_clips(
            duration: float,
        ) -> Iterator[Clip]:
            # Each row yields 2 clips to test one-to-many limit enforcement
            yield Clip(clip_start=0.0, clip_end=duration / 2)
            yield Clip(clip_start=duration / 2, clip_end=duration)

        limit = 8
        query = source.search(None).select(["video_path", "duration"]).limit(limit)
        view = db.create_udtf_view("clips_limited", query, extract_clips)
        view.refresh(_admission_check=False)

        assert view.count_rows() == limit, (
            f"Expected {limit} rows but got {view.count_rows()}"
        )


class TestStreamingFragments:
    """End-to-end: actor streams bounded sub-batches into Lance fragments."""

    @staticmethod
    def _one_each(duration: float) -> Iterator[Clip]:
        # Fanout == 1 so output-row count equals source-row count, making
        # fragment sizes exactly predictable.
        yield Clip(clip_start=0.0, clip_end=duration)

    def _source(self, db, n: int = 20) -> Table:
        data = pa.table(
            {
                "video_path": [f"/v/{i}.mp4" for i in range(n)],
                "duration": [float(i) for i in range(n)],
            }
        )
        return db.create_table("vids", data)

    def test_fragment_count_bounded_by_max_rows(
        self, tmp_path, ray_with_test_path
    ) -> None:
        """Each produced fragment holds <= max_rows_per_fragment rows, and the
        number of non-empty fragments is ceil(total / max_rows)."""
        import math

        db = connect(tmp_path)
        source = self._source(db, n=20)

        chunker = geneva.chunker(self._one_each, output_schema=CLIP_SCHEMA)
        query = source.search(None).select(["video_path", "duration"])
        view = db.create_udtf_view("clips_frag", query, chunker)

        view.refresh(max_rows_per_fragment=7, _admission_check=False)

        assert view.count_rows() == 20
        frags = view.to_lance().get_fragments()
        non_empty = [f for f in frags if f.count_rows() > 0]
        assert len(non_empty) == math.ceil(20 / 7)  # 3
        for f in non_empty:
            assert f.count_rows() <= 7

    def test_content_parity(self, tmp_path, ray_with_test_path) -> None:
        """Streaming fragment writes produce the same rows/columns as a
        baseline expansion."""
        db = connect(tmp_path)
        source = self._source(db, n=12)

        chunker = geneva.chunker(self._one_each, output_schema=CLIP_SCHEMA)
        query = source.search(None).select(["video_path", "duration"])
        view = db.create_udtf_view("clips_parity", query, chunker)
        view.refresh(max_rows_per_fragment=5, _admission_check=False)

        df = view.to_pandas().sort_values("__source_row_id").reset_index(drop=True)
        assert len(df) == 12
        # Every source row contributes exactly one child at index 0.
        assert df["__child_index"].tolist() == [0] * 12
        assert sorted(df["clip_end"].tolist()) == [float(i) for i in range(12)]
        # Inherited (non-input) column aligns with the output's source row.
        # `duration` is a chunker input, so with the default
        # inherit_input_columns=False it is not carried onto the view; the
        # non-input `video_path` is. Source row i has "/v/{i}.mp4" and yields
        # clip_end == i.
        for _, row in df.iterrows():
            vid_idx = int(row["video_path"].rsplit("/", 1)[1].split(".", 1)[0])
            assert row["clip_end"] == float(vid_idx)

    def test_source_task_size_param(self, tmp_path, ray_with_test_path) -> None:
        """A small source_task_size changes work-item granularity but not the
        expansion result."""
        db = connect(tmp_path)
        source = self._source(db, n=20)

        chunker = geneva.chunker(self._one_each, output_schema=CLIP_SCHEMA)
        query = source.search(None).select(["video_path", "duration"])
        view = db.create_udtf_view("clips_rib", query, chunker)

        view.refresh(source_task_size=4, _admission_check=False)
        assert view.count_rows() == 20
        assert sorted(view.to_pandas()["clip_end"].tolist()) == [
            float(i) for i in range(20)
        ]

    def test_worker_oom_splits_source_work_without_duplicates(
        self, tmp_path, ray_with_test_path
    ) -> None:
        """A worker OOM retries only smaller source-row-id work items."""
        import ray

        db = connect(tmp_path)
        source = self._source(db, n=6)

        @geneva.chunker(
            batch=True,
            output_schema=CLIP_SCHEMA,
            input_columns=["duration"],
        )
        def oom_above_one_row(
            duration: pa.Array,
            **kwargs,
        ) -> pa.RecordBatch:
            if len(duration) > 1:
                raise ray.exceptions.OutOfMemoryError("synthetic worker OOM")
            return pa.RecordBatch.from_pydict(
                {
                    "__source_row_id": kwargs["__source_row_id"],
                    "clip_start": pa.array([0.0] * len(duration)),
                    "clip_end": duration,
                }
            )

        query = source.search(None).select(["video_path", "duration"])
        view = db.create_udtf_view("clips_oom_recovery", query, oom_above_one_row)

        view.refresh(
            concurrency=2,
            source_task_size=4,
            _admission_check=False,
        )

        result = view.to_arrow()
        source_row_ids = result["__source_row_id"].to_pylist()
        assert result.num_rows == 6
        assert len(source_row_ids) == len(set(source_row_ids))
        assert sorted(result["clip_end"].to_pylist()) == [float(i) for i in range(6)]

    def test_output_limit_exact_mid_fragment(
        self, tmp_path, ray_with_test_path
    ) -> None:
        """output_limit is enforced exactly even when it lands mid-fragment
        (boundary tail-trim)."""
        db = connect(tmp_path)
        source = self._source(db, n=20)

        chunker = geneva.chunker(self._one_each, output_schema=CLIP_SCHEMA)
        query = source.search(None).select(["video_path", "duration"])
        view = db.create_udtf_view("clips_lim", query, chunker)

        # flush_rows == max_rows_per_fragment == 7; limit 10 lands inside the
        # second fragment, exercising the surplus trim.
        view.refresh(max_rows_per_fragment=7, output_limit=10, _admission_check=False)
        assert view.count_rows() == 10

    def test_output_limit_on_fragment_boundary(
        self, tmp_path, ray_with_test_path
    ) -> None:
        """When output_limit lands exactly on a fragment boundary, surplus is
        zero and no trim happens (count is still exact)."""
        db = connect(tmp_path)
        source = self._source(db, n=20)

        chunker = geneva.chunker(self._one_each, output_schema=CLIP_SCHEMA)
        query = source.search(None).select(["video_path", "duration"])
        view = db.create_udtf_view("clips_boundary", query, chunker)

        # flush_rows == 7; limit 14 == two full fragments, no surplus.
        view.refresh(max_rows_per_fragment=7, output_limit=14, _admission_check=False)
        assert view.count_rows() == 14

    def test_output_limit_larger_than_total(self, tmp_path, ray_with_test_path) -> None:
        """output_limit above the total expansion is a no-op (no trim)."""
        db = connect(tmp_path)
        source = self._source(db, n=12)

        chunker = geneva.chunker(self._one_each, output_schema=CLIP_SCHEMA)
        query = source.search(None).select(["video_path", "duration"])
        view = db.create_udtf_view("clips_over", query, chunker)

        view.refresh(max_rows_per_fragment=5, output_limit=1000, _admission_check=False)
        assert view.count_rows() == 12


class TestTailRowidTrim:
    """Unit tests for ``_tail_rowids_for_trim`` (tail-fragment-scoped trim)."""

    @staticmethod
    def _dataset(tmp_path, sizes) -> "lance.LanceDataset":
        """Build a Lance dataset with one fragment per entry in *sizes*."""
        uri = str(tmp_path / "trim.lance")
        offset = 0
        for i, sz in enumerate(sizes):
            tbl = pa.table({"x": list(range(offset, offset + sz))})
            lance.write_dataset(
                tbl,
                uri,
                mode="create" if i == 0 else "append",
                max_rows_per_file=10_000,
            )
            offset += sz
        return lance.dataset(uri)

    @staticmethod
    def _all_rowids(ds) -> list[int]:
        return sorted(
            ds.scanner(columns=[], with_row_id=True)
            .to_table()
            .column("_rowid")
            .to_pylist()
        )

    def test_returns_highest_rowids_single_fragment(self, tmp_path) -> None:
        from geneva.runners.ray.pipeline import _tail_rowids_for_trim

        ds = self._dataset(tmp_path, [5, 5, 5])
        out = _tail_rowids_for_trim(ds, 3)
        assert sorted(out) == self._all_rowids(ds)[-3:]

    def test_returns_highest_rowids_spanning_fragments(self, tmp_path) -> None:
        """Surplus larger than the newest fragment spills into the next-newest;
        the returned ids are still the globally highest ``surplus`` row-ids."""
        from geneva.runners.ray.pipeline import _tail_rowids_for_trim

        ds = self._dataset(tmp_path, [5, 5, 3])  # newest fragment holds 3 rows
        out = _tail_rowids_for_trim(ds, 5)  # needs 3 + 2 from prior fragment
        assert sorted(out) == self._all_rowids(ds)[-5:]

    def test_scans_only_tail_fragments(self, tmp_path, monkeypatch) -> None:
        """Only the newest fragment(s) needed to cover the surplus are scanned —
        never the whole table."""
        ds = self._dataset(tmp_path, [5, 5, 3])
        scanned: list[int] = []
        orig = lance.fragment.LanceFragment.scanner

        def spy(self, *args, **kwargs) -> object:
            scanned.append(self.fragment_id)
            return orig(self, *args, **kwargs)

        monkeypatch.setattr(lance.fragment.LanceFragment, "scanner", spy)

        from geneva.runners.ray.pipeline import _tail_rowids_for_trim

        # surplus 2 < newest fragment (3 rows) -> only the newest fragment.
        _tail_rowids_for_trim(ds, 2)
        assert scanned == [2]

        scanned.clear()
        # surplus 5 spans the two newest fragments, but never the oldest (id 0).
        _tail_rowids_for_trim(ds, 5)
        assert scanned == [2, 1]
        assert 0 not in scanned
