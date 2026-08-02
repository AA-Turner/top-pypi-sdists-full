# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for ``chunk_video_udtf`` (video chunking UDTF)."""

import importlib.util
import io
import math
from fractions import Fraction
from pathlib import Path

import pyarrow as pa
import pytest

from geneva import connect
from geneva.chunkers.video import (
    _VIDEO_CLIP_SCHEMA,
    _clip_windows,
    _probe_video,
    chunk_video_udtf,
)
from geneva.packager import marshal_chunker, unmarshal_chunker
from geneva.transformer import Chunker

_FIXTURES = Path(__file__).parent / "fixtures"
_FIXTURE = _FIXTURES / "sample_clip.mp4"
_FIXTURE_AUDIO = _FIXTURES / "sample_clip_with_audio.mp4"

# Per-test gate for the optional PyAV (``av``) dependency. Applied only to the
# tests that decode/encode real video, so the pure-math ``TestClipWindows`` and
# the monkeypatched coverage tests still run without the extra installed.
requires_av = pytest.mark.skipif(
    importlib.util.find_spec("av") is None,
    reason="PyAV (av) is not installed",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_synthetic_mp4(
    seconds: float = 3.0,
    fps: int | Fraction = 10,
    w: int = 64,
    h: int = 48,
) -> bytes:
    """Encode a short H.264 mp4 in-memory with per-frame-varying content.

    Frame ``i`` has a flat red channel of ``(i * 10) % 256`` (so a clip's
    content can be identified by its decoded red value) plus a moving green
    scanline for real inter-frame motion.
    """
    import av
    import numpy as np

    buf = io.BytesIO()
    time_base = Fraction(1, 1) / fps
    with av.open(buf, mode="w", format="mp4") as out:
        stream = out.add_stream("libx264", rate=fps)
        stream.width = w
        stream.height = h
        stream.pix_fmt = "yuv420p"
        stream.codec_context.time_base = time_base
        stream.codec_context.thread_count = 1
        stream.codec_context.thread_type = "NONE"
        for i in range(int(seconds * fps)):
            arr = np.zeros((h, w, 3), dtype=np.uint8)
            arr[:, :, 0] = (i * 10) % 256  # ramp on red
            arr[i % h, :, 1] = 255  # moving green line -> real motion
            frame = av.VideoFrame.from_ndarray(arr, format="rgb24")
            frame.pts = i
            frame.time_base = time_base
            for packet in stream.encode(frame):
                out.mux(packet)
        for packet in stream.encode():
            out.mux(packet)
    return buf.getvalue()


def _batch(
    video_bytes_list: list[bytes | None],
    video_ids: list[str] | None = None,
) -> pa.RecordBatch:
    """Build a source RecordBatch with __source_row_id + video_id + video_bytes."""
    n = len(video_bytes_list)
    if video_ids is None:
        video_ids = [f"vid_{i}" for i in range(n)]
    return pa.RecordBatch.from_pydict(
        {
            "__source_row_id": pa.array(list(range(n)), type=pa.int64()),
            "video_id": pa.array(video_ids, type=pa.string()),
            "video_bytes": pa.array(video_bytes_list, type=pa.large_binary()),
        }
    )


def _clip_duration(clip_bytes: bytes) -> float:
    """Return the duration (seconds) of an encoded clip, and assert it decodes."""
    import av

    with av.open(io.BytesIO(clip_bytes)) as container:
        stream = container.streams.video[0]
        first = next(container.decode(stream))  # must have a decodable frame
        assert first is not None
        return float(stream.duration * stream.time_base)


def _first_frame_mean_red(clip_bytes: bytes) -> float:
    """Decode a clip's first frame and return its mean red-channel value."""
    import av

    with av.open(io.BytesIO(clip_bytes)) as container:
        stream = container.streams.video[0]
        frame = next(container.decode(stream))
        return float(frame.to_ndarray(format="rgb24")[:, :, 0].mean())


def _clip_resolution(clip_bytes: bytes) -> tuple[int, int]:
    """Return (width, height) of an encoded clip."""
    import av

    with av.open(io.BytesIO(clip_bytes)) as container:
        ctx = container.streams.video[0].codec_context
        return ctx.width, ctx.height


# ---------------------------------------------------------------------------
# Pure windowing math — no optional dependencies
# ---------------------------------------------------------------------------


class TestClipWindows:
    def test_exact_division(self) -> None:
        assert _clip_windows(4.0, 1.0) == [
            (0.0, 1.0),
            (1.0, 2.0),
            (2.0, 3.0),
            (3.0, 4.0),
        ]

    def test_partial_trailing_window(self) -> None:
        assert _clip_windows(2.5, 1.0) == [(0.0, 1.0), (1.0, 2.0), (2.0, 2.5)]

    def test_sub_chunk_length_single_window(self) -> None:
        assert _clip_windows(0.4, 1.0) == [(0.0, 0.4)]

    def test_max_clips_cap(self) -> None:
        assert _clip_windows(10.0, 1.0, max_clips=3) == [
            (0.0, 1.0),
            (1.0, 2.0),
            (2.0, 3.0),
        ]

    @pytest.mark.parametrize("duration", [0.0, -1.0])
    def test_non_positive_duration_empty(self, duration: float) -> None:
        assert _clip_windows(duration, 1.0) == []

    def test_non_positive_chunk_empty(self) -> None:
        assert _clip_windows(5.0, 0.0) == []

    @pytest.mark.parametrize("max_clips", [0, -1])
    def test_non_positive_max_clips_empty(self, max_clips: int) -> None:
        assert _clip_windows(5.0, 1.0, max_clips=max_clips) == []


# ---------------------------------------------------------------------------
# Component tests — exercise real demux/decode/re-encode (needs PyAV)
# Each PyAV-dependent test is gated with ``@requires_av``.
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def synthetic_mp4() -> bytes:
    return _make_synthetic_mp4(seconds=3.0, fps=10)


@pytest.fixture(scope="module")
def sample_clip_bytes() -> bytes:
    if not _FIXTURE.exists():  # pragma: no cover - fixture is committed
        pytest.skip(f"missing video fixture: {_FIXTURE}")
    return _FIXTURE.read_bytes()


@pytest.fixture(scope="module")
def sample_clip_with_audio_bytes() -> bytes:
    if not _FIXTURE_AUDIO.exists():  # pragma: no cover - fixture is committed
        pytest.skip(f"missing video fixture: {_FIXTURE_AUDIO}")
    return _FIXTURE_AUDIO.read_bytes()


@pytest.fixture(params=["synthetic_mp4", "sample_clip_bytes"])
def video_bytes(request: pytest.FixtureRequest) -> bytes:
    return request.getfixturevalue(request.param)


def test_factory_chunker_shape() -> None:
    chunker = chunk_video_udtf(chunk_seconds=1.0)
    assert isinstance(chunker, Chunker)
    assert chunker.input_columns == ["video_id", "video_bytes"]
    assert chunker.inherit_input_columns is False
    assert chunker.output_schema == _VIDEO_CLIP_SCHEMA


@requires_av
def test_chunks_full_video(video_bytes: bytes) -> None:
    duration = _probe_video(video_bytes)
    expected = _clip_windows(duration, 1.0)
    assert len(expected) >= 2  # both fixtures are multi-second

    out = chunk_video_udtf(chunk_seconds=1.0).execute_on_record_batch(
        _batch([video_bytes])
    )

    # schema + row count
    assert out.select(_VIDEO_CLIP_SCHEMA.names).schema.equals(_VIDEO_CLIP_SCHEMA)
    assert out.num_rows == len(expected)

    # video_id is echoed onto every clip row for correlation
    assert out.column("video_id").to_pylist() == ["vid_0"] * len(expected)
    # expansion bookkeeping
    assert out.column("__child_index").to_pylist() == list(range(len(expected)))
    assert out.column("chunk_id").to_pylist() == list(range(len(expected)))

    # contiguous, monotonic windows within [0, duration]
    starts = out.column("start_sec").to_pylist()
    ends = out.column("end_sec").to_pylist()
    assert starts == [pytest.approx(s) for s, _ in expected]
    assert ends == [pytest.approx(e) for _, e in expected]
    assert starts[0] == 0.0
    assert ends[-1] == pytest.approx(duration, abs=0.2)

    # each clip is a valid, decodable mp4 of roughly its window length
    clip_durations = [_clip_duration(cb) for cb in out.column("clip_bytes").to_pylist()]
    for (start, end), clip_dur in zip(expected, clip_durations, strict=True):
        assert clip_dur == pytest.approx(end - start, abs=0.25)
    assert sum(clip_durations) == pytest.approx(duration, abs=0.5)


def test_none_input_yields_no_rows() -> None:
    out = chunk_video_udtf(chunk_seconds=1.0).execute_on_record_batch(_batch([None]))
    assert out.num_rows == 0


@requires_av
def test_corrupt_bytes_skipped() -> None:
    out = chunk_video_udtf(chunk_seconds=1.0).execute_on_record_batch(
        _batch([b"not a video"])
    )
    assert out.num_rows == 0


@requires_av
def test_max_video_s_skip_is_opt_in(sample_clip_bytes: bytes) -> None:
    duration = _probe_video(sample_clip_bytes)
    # Default: no skip -> chunks the whole clip.
    default_rows = (
        chunk_video_udtf(chunk_seconds=1.0)
        .execute_on_record_batch(_batch([sample_clip_bytes]))
        .num_rows
    )
    assert default_rows == len(_clip_windows(duration, 1.0))
    # Opt-in: a limit below the clip duration skips it entirely.
    skipped = chunk_video_udtf(
        chunk_seconds=1.0, max_video_s=duration / 2
    ).execute_on_record_batch(_batch([sample_clip_bytes]))
    assert skipped.num_rows == 0


@requires_av
def test_num_clips_cap(sample_clip_bytes: bytes) -> None:
    out = chunk_video_udtf(chunk_seconds=1.0, num_clips=2).execute_on_record_batch(
        _batch([sample_clip_bytes])
    )
    assert out.num_rows == 2


@requires_av
def test_chunk_seconds_controls_count(sample_clip_bytes: bytes) -> None:
    duration = _probe_video(sample_clip_bytes)
    out = chunk_video_udtf(chunk_seconds=2.0).execute_on_record_batch(
        _batch([sample_clip_bytes])
    )
    assert out.num_rows == math.ceil(duration / 2.0)


@requires_av
def test_num_clips_zero_yields_no_rows(sample_clip_bytes: bytes) -> None:
    out = chunk_video_udtf(chunk_seconds=1.0, num_clips=0).execute_on_record_batch(
        _batch([sample_clip_bytes])
    )
    assert out.num_rows == 0


@requires_av
def test_multi_video_batch_expansion() -> None:
    """Multiple source videos expand independently; per-video bookkeeping."""
    vid_a = _make_synthetic_mp4(seconds=3.0, fps=10)  # -> 3 clips
    vid_b = _make_synthetic_mp4(seconds=2.0, fps=10)  # -> 2 clips

    out = chunk_video_udtf(chunk_seconds=1.0).execute_on_record_batch(
        _batch([vid_a, vid_b], ["A", "B"])
    )

    assert out.num_rows == 5
    # video_id maps each clip to its source video
    assert out.column("video_id").to_pylist() == ["A", "A", "A", "B", "B"]
    # __child_index resets to 0 for each source video
    assert out.column("__child_index").to_pylist() == [0, 1, 2, 0, 1]
    assert out.column("chunk_id").to_pylist() == [0, 1, 2, 0, 1]


@requires_av
def test_mixed_batch_skips_bad_rows_without_misaligning() -> None:
    """A bad row yields nothing and does not corrupt good rows' video_id."""
    good = _make_synthetic_mp4(seconds=2.0, fps=10)  # -> 2 clips

    out = chunk_video_udtf(chunk_seconds=1.0).execute_on_record_batch(
        _batch([b"not a video", good], ["bad", "good"])
    )

    assert out.num_rows == 2
    assert out.column("video_id").to_pylist() == ["good", "good"]
    assert out.column("__child_index").to_pylist() == [0, 1]


@requires_av
def test_clip_content_matches_window(synthetic_mp4: bytes) -> None:
    """Each clip contains the frames of its window, not window 0's frames.

    Frame ``i`` has red ``(i*10) % 256``; at 10 fps with 1 s chunks the first
    frame of window ``w`` is frame ``10*w`` -> red ``(100*w) % 256``.
    """
    out = chunk_video_udtf(chunk_seconds=1.0).execute_on_record_batch(
        _batch([synthetic_mp4])
    )
    reds = [_first_frame_mean_red(cb) for cb in out.column("clip_bytes").to_pylist()]
    assert len(reds) == 3
    # distinct, increasing segments (proves seek/window selection works)
    assert reds[0] < reds[1] < reds[2]
    for w, red in enumerate(reds):
        assert red == pytest.approx((100 * w) % 256, abs=40)


@requires_av
def test_chunks_video_with_audio_track(sample_clip_with_audio_bytes: bytes) -> None:
    """A source carrying an audio track is chunked without error (video-only)."""
    duration = _probe_video(sample_clip_with_audio_bytes)
    out = chunk_video_udtf(chunk_seconds=1.0).execute_on_record_batch(
        _batch([sample_clip_with_audio_bytes])
    )
    assert out.num_rows == len(_clip_windows(duration, 1.0))
    for cb in out.column("clip_bytes").to_pylist():
        _clip_duration(cb)  # each clip re-decodes


@requires_av
def test_fractional_fps_source() -> None:
    """Non-integer fps (e.g. 30000/1001) is handled by the CFR timeline math."""
    data = _make_synthetic_mp4(seconds=2.0, fps=Fraction(30000, 1001))
    out = chunk_video_udtf(chunk_seconds=1.0).execute_on_record_batch(_batch([data]))
    assert out.num_rows >= 1
    for cb in out.column("clip_bytes").to_pylist():
        _clip_duration(cb)


@requires_av
def test_video_shorter_than_chunk_yields_single_clip() -> None:
    data = _make_synthetic_mp4(seconds=0.5, fps=10)
    out = chunk_video_udtf(chunk_seconds=5.0).execute_on_record_batch(_batch([data]))
    assert out.num_rows == 1
    assert out.column("start_sec").to_pylist() == [0.0]


@requires_av
def test_clip_resolution_matches_source() -> None:
    data = _make_synthetic_mp4(seconds=2.0, fps=10, w=64, h=48)
    out = chunk_video_udtf(chunk_seconds=1.0).execute_on_record_batch(_batch([data]))
    for cb in out.column("clip_bytes").to_pylist():
        assert _clip_resolution(cb) == (64, 48)


@requires_av
def test_none_video_id_allowed(sample_clip_bytes: bytes) -> None:
    """A null video_id is permitted and echoed as null on each clip row."""
    out = chunk_video_udtf(chunk_seconds=1.0).execute_on_record_batch(
        _batch([sample_clip_bytes], [None])  # type: ignore[list-item]
    )
    assert out.num_rows >= 1
    assert all(v is None for v in out.column("video_id").to_pylist())


def test_version_stable_and_param_sensitive() -> None:
    """Same params -> same version (cache hit); different -> different (re-run)."""
    assert chunk_video_udtf(chunk_seconds=1.0).version == (
        chunk_video_udtf(chunk_seconds=1.0).version
    )
    assert (
        chunk_video_udtf(chunk_seconds=1.0).version
        != chunk_video_udtf(chunk_seconds=2.0).version
    )


def test_serialization_preserves_no_inherit() -> None:
    """marshal/unmarshal round-trips the inherit_input_columns opt-out."""
    restored = unmarshal_chunker(marshal_chunker(chunk_video_udtf(chunk_seconds=2.0)))
    assert restored is not None
    assert restored.inherit_input_columns is False
    assert restored.input_columns == ["video_id", "video_bytes"]
    assert restored.output_schema == _VIDEO_CLIP_SCHEMA


def test_create_udtf_view_requires_video_id(tmp_path) -> None:
    """The view cannot be built if the projection omits the required video_id."""
    db = connect(tmp_path)
    src = db.create_table(
        "videos",
        pa.table({"video_id": pa.array(["a"]), "video_bytes": pa.array([b"x"])}),
    )
    # Project only video_bytes -> video_id is missing from the projection.
    query = src.search(None).select(["video_bytes"])
    with pytest.raises(ValueError, match="not found in query projection"):
        db.create_udtf_view("clips", query, chunk_video_udtf(chunk_seconds=1.0))


# ---------------------------------------------------------------------------
# Loop coverage — exercise the chunking loop without PyAV by stubbing the
# decode/encode helpers, so these run (and are measured) in every CI job.
# ---------------------------------------------------------------------------


def test_chunk_id_dense_when_window_skipped(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A window yielding no clip must not create a chunk_id gap.

    ``chunk_id`` stays dense and equal to ``__child_index`` even when
    ``_encode_clip`` returns ``None`` for a non-trailing window. Runs without
    PyAV by stubbing the decode/encode helpers.
    """
    import geneva.chunkers.video as vid

    monkeypatch.setattr(vid, "_probe_video", lambda _b: 3.0)

    def fake_encode(_b: bytes, start: float, _end: float) -> bytes | None:
        # The middle window (1s-2s) encodes to nothing.
        return None if 1.0 <= start < 2.0 else b"fake-mp4-bytes"

    monkeypatch.setattr(vid, "_encode_clip", fake_encode)

    out = chunk_video_udtf(chunk_seconds=1.0).execute_on_record_batch(
        _batch([b"anything"], ["vid_0"])
    )

    assert out.num_rows == 2
    assert out.column("chunk_id").to_pylist() == [0, 1]
    assert out.column("__child_index").to_pylist() == [0, 1]
    # The surviving clips are windows 0 and 2 (window 1 was skipped).
    assert out.column("start_sec").to_pylist() == [
        pytest.approx(0.0),
        pytest.approx(2.0),
    ]


def test_max_video_s_skips_long_video(monkeypatch: pytest.MonkeyPatch) -> None:
    """A video longer than ``max_video_s`` is skipped entirely (no decode)."""
    import geneva.chunkers.video as vid

    monkeypatch.setattr(vid, "_probe_video", lambda _b: 100.0)

    def _unexpected_encode(*_a: object, **_k: object) -> bytes | None:
        raise AssertionError("_encode_clip must not run for a skipped video")

    monkeypatch.setattr(vid, "_encode_clip", _unexpected_encode)

    out = chunk_video_udtf(chunk_seconds=1.0, max_video_s=10.0).execute_on_record_batch(
        _batch([b"anything"], ["vid_0"])
    )

    assert out.num_rows == 0


# ---------------------------------------------------------------------------
# Ray integration — materialize via create_udtf_view + refresh
# ---------------------------------------------------------------------------


@requires_av
@pytest.mark.ray
def test_create_udtf_view_and_refresh(tmp_path, ray_with_test_path) -> None:
    clip = _FIXTURE.read_bytes()
    duration = _probe_video(clip)
    expected = len(_clip_windows(duration, 1.0))

    db = connect(tmp_path)
    src = db.create_table(
        "videos",
        pa.table(
            {
                "video_id": pa.array(["vid_A"], type=pa.string()),
                "video_bytes": pa.array([clip], type=pa.large_binary()),
            }
        ),
    )

    # The chunker requires video_id; project it alongside the bytes.
    query = src.search(None).select(["video_id", "video_bytes"])
    view = db.create_udtf_view(
        "video_clips", query, chunk_video_udtf(chunk_seconds=1.0)
    )
    view.refresh(_admission_check=False)

    # The single source video expands into one row per clip.
    assert view.count_rows() == expected
    result = view.to_pandas().sort_values("__child_index").reset_index(drop=True)
    for col in ("video_id", "__child_index", "chunk_id", "clip_bytes"):
        assert col in result.columns

    # The input bytes are NOT duplicated onto every clip row...
    assert "video_bytes" not in result.columns
    # ...but video_id is echoed on each clip, so clips correlate back to the
    # source by a stable, caller-controlled key (not __source_row_id).
    assert result["video_id"].tolist() == ["vid_A"] * expected
    assert result["__child_index"].tolist() == list(range(expected))
    assert result["clip_bytes"].notna().all()


@requires_av
@pytest.mark.ray
def test_refresh_multi_video_and_incremental(tmp_path, ray_with_test_path) -> None:
    clip = _FIXTURE.read_bytes()
    per_video = len(_clip_windows(_probe_video(clip), 1.0))

    db = connect(tmp_path)
    src = db.create_table(
        "videos",
        pa.table(
            {
                "video_id": pa.array(["vid_A", "vid_B"], type=pa.string()),
                "video_bytes": pa.array([clip, clip], type=pa.large_binary()),
            }
        ),
        storage_options={"new_table_enable_stable_row_ids": True},
    )
    query = src.search(None).select(["video_id", "video_bytes"])
    view = db.create_udtf_view(
        "video_clips", query, chunk_video_udtf(chunk_seconds=1.0)
    )
    view.refresh(_admission_check=False)

    # Two source videos -> per_video clips each, correlated by video_id.
    assert view.count_rows() == 2 * per_video
    df = view.to_pandas()
    assert "video_bytes" not in df.columns
    assert (df["video_id"] == "vid_A").sum() == per_video
    assert (df["video_id"] == "vid_B").sum() == per_video

    # Incremental: a new source video is picked up; existing clips untouched.
    src.add(
        pa.table(
            {
                "video_id": pa.array(["vid_C"], type=pa.string()),
                "video_bytes": pa.array([clip], type=pa.large_binary()),
            }
        )
    )
    view.refresh(_admission_check=False)
    assert view.count_rows() == 3 * per_video
    df2 = view.to_pandas()
    assert (df2["video_id"] == "vid_C").sum() == per_video
