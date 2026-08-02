# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Render the video-chunking benchmark scores into a Wiki markdown page.

Reads ``video_chunking_scores.csv`` (produced by
``src/benches/test_video_chunking_bench.py`` and uploaded as the
``video-chunking-bench-<run>`` CI artifact) and writes a Wiki page. Invoked by
``weekly-wiki-update.yml``. Stdlib only.

Usage: render_video_chunking_wiki.py <scores.csv> <out.md>
"""

import csv
import datetime
import sys
from pathlib import Path

_COLUMNS = [
    ("num_videos", "Videos"),
    ("concurrency", "Concurrency"),
    ("total_clips", "Clips"),
    ("batch_median_s", "Batch median (s)"),
    ("clips_per_sec", "Clips/sec"),
    ("video_secs_per_sec", "Video-s/sec"),
]

_LEGEND = """## Column reference

- **Videos** — number of videos chunked in the batch (swept by powers of two).
- **Concurrency** — parallel shards the batch is split into (each a num_cpus=1
  chunker task running on its own thread).
- **Clips** — total clips produced = sum of `ceil(duration / chunk_seconds)`.
- **Batch median (s)** — median wall-clock to chunk the whole batch once.
- **Clips/sec** — `Clips / Batch median` (output throughput).
- **Video-s/sec** — input footage seconds / `Batch median` (ingest throughput)."""


def _table(rows: list[dict[str, str]]) -> str:
    header = "| " + " | ".join(label for _, label in _COLUMNS) + " |"
    sep = "|" + "|".join(["---:"] * len(_COLUMNS)) + "|"
    body = [
        "| " + " | ".join(str(row[key]) for key, _ in _COLUMNS) + " |"
        for row in sorted(
            rows, key=lambda r: (int(r["num_videos"]), int(r["concurrency"]))
        )
    ]
    return "\n".join([header, sep, *body])


def main(scores_csv: str, out_md: str) -> int:
    csv_path = Path(scores_csv)
    if not csv_path.exists():
        print(f"No scores file at {csv_path}; skipping wiki page.")
        return 0

    with csv_path.open() as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        print("Scores file is empty; skipping wiki page.")
        return 0

    today = datetime.date.today().strftime("%B %d, %Y")
    page = f"""# Geneva Benchmarks — Video Chunking

> **Automated benchmark.** Generated from the latest `video-chunking-bench`
> GitHub Actions run, refreshed weekly. Last updated: {today}. Absolute numbers
> are runner-dependent — watch the trend, not the point values.

`chunk_video_udtf` splits a video into fixed-length clips (one output row per
clip, each a standalone re-encoded H.264 mp4). This benchmark times the **real**
in-process decode → cut → re-encode path (`execute_on_record_batch`, no Ray;
nothing is mocked — only the input videos are synthetic) and sweeps the batch
size by powers of two and the **concurrency** (parallel `num_cpus=1` chunker
tasks). Each cell also asserts correctness: every video yields exactly
`ceil(duration / chunk_seconds)` clips, and an emitted clip is decoded back to
confirm it is a valid mp4.

## Throughput by batch size and concurrency

{_table(rows)}

{_LEGEND}

## Methodology

- Synthetic 640×480 @ 10 fps clips (1–5 s each), generated once at the largest
  scale and sliced for smaller scales; expected clip counts derived from each
  clip's probed duration.
- Chunker runs with `num_cpus=1`; concurrency splits the batch into N thread
  shards. `libx264`, single-threaded encode; `benchmark.pedantic(rounds=1)`.
- Source: `src/benches/test_video_chunking_bench.py`. Raw `benchmark.json` and
  `video_chunking_scores.csv` are attached to each CI run as the
  `video-chunking-bench-<run>` artifact.
"""

    out_path = Path(out_md)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page)
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
