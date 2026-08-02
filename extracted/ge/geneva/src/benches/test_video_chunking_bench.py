# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Throughput + concurrency benchmark for ``chunk_video_udtf``.

Generates synthetic videos of known durations and chunks them into a known
number of fixed-length clips, benchmarking the **real** in-process
decode/cut/re-encode path (``execute_on_record_batch``; nothing is mocked —
only the input videos are synthetic, and an emitted clip is decoded back to
confirm it is a valid mp4).

It sweeps two dimensions:
- **batch size** ``num_videos`` (powers of two in
  ``[GENEVA_BENCH_MIN_VIDEOS, GENEVA_BENCH_MAX_VIDEOS]``, default 2048..8192);
- **concurrency** ``GENEVA_BENCH_CONCURRENCY`` (default ``1,2,4,8``) — the batch
  is split into N contiguous shards each chunked on its own thread, modeling N
  parallel ``num_cpus=1`` chunker tasks (libx264 releases the GIL, so threads
  parallelize the encode).

Doubles as a scale correctness check: each batch must expand to exactly
``sum(ceil(duration / chunk_seconds))`` clips.

**Heavy.** At 640x480, 8192 videos is on the order of ~10 min per
single-threaded pass — this is a stress-scale benchmark. Dial it down locally
with the env vars above (e.g. ``GENEVA_BENCH_MIN_VIDEOS=4
GENEVA_BENCH_MAX_VIDEOS=8 GENEVA_BENCH_CONCURRENCY=1,2``).

Results are persisted two ways:
- pytest-benchmark timing JSON (``--benchmark-json`` / ``make bench``), one entry
  per (videos, concurrency) cell, with metrics in ``benchmark.extra_info``;
- a combined per-cell scores CSV + JSON written to ``GENEVA_BENCH_RESULTS_DIR``.

Marked ``slow``; lives under ``src/benches`` so it stays out of the fast suite.
"""

import csv
import io
import json
import math
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path

import pyarrow as pa
import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from geneva.chunkers.video import (
    _clip_windows,
    _probe_video,
    chunk_video_udtf,
)

MIN_VIDEOS = int(os.getenv("GENEVA_BENCH_MIN_VIDEOS", "2048"))
MAX_VIDEOS = int(os.getenv("GENEVA_BENCH_MAX_VIDEOS", "8192"))
CONCURRENCY = [
    int(x) for x in os.getenv("GENEVA_BENCH_CONCURRENCY", "1,2,4,8").split(",")
]
ROUNDS = int(os.getenv("GENEVA_BENCH_ROUNDS", "1"))
CHUNK_SECONDS = 1.0
FPS = 10
_DEFAULT_RESULTS_DIR = (
    Path(tempfile.gettempdir()) / "test-results" / "video-chunking-bench"
)
_RESULTS_DIR = Path(
    os.environ.get("GENEVA_BENCH_RESULTS_DIR", str(_DEFAULT_RESULTS_DIR))
)
# Column meanings (see the doc/Wiki legend):
#   num_videos          videos chunked in the batch
#   concurrency         number of parallel shards (threads) the batch is split into
#   total_clips         clips produced (sum of ceil(duration/chunk_seconds))
#   input_video_seconds total source footage fed in (sum of probed durations)
#   batch_median_s      median wall-clock to chunk the whole batch once
#   batch_total_s       total wall-clock across all timed rounds
#   clips_per_sec       total_clips / batch_median_s (output throughput)
#   video_secs_per_sec  input_video_seconds / batch_median_s (ingest throughput)
_SCORE_FIELDS = [
    "num_videos",
    "concurrency",
    "total_clips",
    "input_video_seconds",
    "batch_median_s",
    "batch_total_s",
    "clips_per_sec",
    "video_secs_per_sec",
]
# Accumulates one row per (videos, concurrency) cell; flushed by the finalizer.
_SCORES: list[dict[str, object]] = []


def _power_of_two_scales(min_n: int, max_n: int) -> list[int]:
    """Return powers of two in ``[min_n, max_n]`` inclusive."""
    scales: list[int] = []
    n = 1
    while n <= max_n:
        if n >= min_n:
            scales.append(n)
        n *= 2
    return scales or [max(1, max_n)]


SCALES = _power_of_two_scales(MIN_VIDEOS, MAX_VIDEOS)


def _make_synthetic_mp4(
    seconds: float,
    fps: int | Fraction = FPS,
    w: int = 640,
    h: int = 480,
) -> bytes:
    """Encode a tiny H.264 mp4 in-memory with per-frame-varying content."""
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
            arr[:, :, 0] = (i * 10) % 256
            arr[i % h, :, 1] = 255
            frame = av.VideoFrame.from_ndarray(arr, format="rgb24")
            frame.pts = i
            frame.time_base = time_base
            for packet in stream.encode(frame):
                out.mux(packet)
        for packet in stream.encode():
            out.mux(packet)
    return buf.getvalue()


def _assert_clip_is_real_mp4(clip_bytes: bytes) -> None:
    """Decode an emitted clip to confirm it is a genuine mp4 (not a mock)."""
    import av

    assert clip_bytes, "clip_bytes is empty"
    with av.open(io.BytesIO(clip_bytes)) as container:
        stream = container.streams.video[0]
        assert next(container.decode(stream)) is not None


def _chunk_concurrently(
    chunker: object, batch: pa.RecordBatch, concurrency: int
) -> list[pa.RecordBatch]:
    """Split ``batch`` into ``concurrency`` shards, chunk each on its own thread.

    Models ``concurrency`` parallel ``num_cpus=1`` chunker tasks.
    """
    run = chunker.execute_on_record_batch  # type: ignore[attr-defined]
    if concurrency <= 1:
        return [run(batch)]
    n = batch.num_rows
    shard = math.ceil(n / concurrency)
    shards = [batch.slice(i, min(shard, n - i)) for i in range(0, n, shard)]
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        return list(ex.map(run, shards))


class _Workload:
    """Synthetic videos with known clip expectations, built once at max scale.

    ``slice(k)`` returns the first ``k`` videos so each scale reuses the same
    generated data. Generation is parallelized across threads (encode releases
    the GIL) to keep fixture setup tractable at 16k videos.
    """

    def __init__(self, n: int) -> None:
        requested = [1.0 + (i % 5) for i in range(n)]  # 1..5 s -> 1..5 clips
        with ThreadPoolExecutor() as ex:
            video_bytes = list(ex.map(_make_synthetic_mp4, requested))

        self.video_ids = [f"vid_{i:06d}" for i in range(n)]
        self.probed_seconds = [_probe_video(b) for b in video_bytes]
        self.expected_counts = [
            len(_clip_windows(s, CHUNK_SECONDS)) for s in self.probed_seconds
        ]
        self.batch = pa.RecordBatch.from_pydict(
            {
                "__source_row_id": pa.array(range(n), type=pa.int64()),
                "video_id": pa.array(self.video_ids, type=pa.string()),
                "video_bytes": pa.array(video_bytes, type=pa.large_binary()),
            }
        )

    def slice(self, k: int) -> tuple[pa.RecordBatch, int, float]:
        """Return (first-k batch, expected total clips, total input seconds)."""
        return (
            self.batch.slice(0, k),
            sum(self.expected_counts[:k]),
            sum(self.probed_seconds[:k]),
        )


@pytest.fixture(scope="module")
def full_workload() -> _Workload:
    return _Workload(max(SCALES))


@pytest.fixture(scope="module", autouse=True)
def _persist_scores() -> object:
    yield
    if not _SCORES:
        return
    _RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    rows = sorted(_SCORES, key=lambda r: (r["num_videos"], r["concurrency"]))
    with (_RESULTS_DIR / "video_chunking_scores.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=_SCORE_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    with (_RESULTS_DIR / "video_chunking_scores.json").open("w") as fh:
        json.dump(rows, fh, indent=2)


@pytest.mark.slow
@pytest.mark.parametrize("concurrency", CONCURRENCY, ids=lambda c: f"conc={c}")
@pytest.mark.parametrize("num_videos", SCALES, ids=lambda n: f"videos={n}")
def test_chunk_video_throughput(
    benchmark: BenchmarkFixture,
    full_workload: _Workload,
    num_videos: int,
    concurrency: int,
) -> None:
    """Benchmark chunking ``num_videos`` videos at ``concurrency`` shards."""
    chunker = chunk_video_udtf(chunk_seconds=CHUNK_SECONDS)
    batch, expected_total, total_video_seconds = full_workload.slice(num_videos)

    results = benchmark.pedantic(
        _chunk_concurrently,
        args=(chunker, batch, concurrency),
        rounds=ROUNDS,
        iterations=1,
    )

    # Correctness: shards together expand to the known clip count.
    assert sum(r.num_rows for r in results) == expected_total
    # Proof this is real chunking (not a mock): an emitted clip is a valid mp4.
    first = next((r for r in results if r.num_rows), None)
    if first is not None:
        _assert_clip_is_real_mp4(first.column("clip_bytes")[0].as_py())

    stats = benchmark.stats.stats
    median_s = float(stats.median)
    total_s = float(sum(stats.data))
    row: dict[str, object] = {
        "num_videos": num_videos,
        "concurrency": concurrency,
        "total_clips": expected_total,
        "input_video_seconds": round(total_video_seconds, 3),
        "batch_median_s": round(median_s, 6),
        "batch_total_s": round(total_s, 6),
        "clips_per_sec": round(expected_total / median_s, 2) if median_s else math.inf,
        "video_secs_per_sec": (
            round(total_video_seconds / median_s, 2) if median_s else math.inf
        ),
    }
    benchmark.extra_info.update(row)
    _SCORES.append(row)
