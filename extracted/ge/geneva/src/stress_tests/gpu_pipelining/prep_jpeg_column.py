#!/usr/bin/env python3
# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""One-shot helper: write a sister Lance dataset with ``image_jpeg``.

NVIDIA's nvJPEG (the GPU JPEG decoder behind
``torchvision.io.decode_jpeg(..., device='cuda')``) accepts JPEG only.
The bench's existing dataset is PNG. To benchmark GPU decode we need
the same rows re-encoded as JPEG.

Bypasses Geneva — even with the per-ScanTask scanner-state-leak fix
in this branch, 40k rows would drag this out via the public-API
backfill path. Read
PNG bytes via Lance directly, re-encode as JPEG with a process pool
(PIL releases the GIL), and write a new Lance dataset
(``./db/images_jpeg.lance``). The fused-NVJPEG bench reads from
there.

Usage:

    python src/stress_tests/gpu_pipelining/prep_jpeg_column.py
"""

from __future__ import annotations

import io
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import lance
import pyarrow as pa


def _png_to_jpeg(png_bytes: bytes) -> bytes:
    from PIL import Image  # imported in worker to avoid fork issues

    pil = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    buf = io.BytesIO()
    pil.save(buf, format="JPEG", quality=95)
    return buf.getvalue()


def _convert_chunk(png_chunk: list[bytes]) -> list[bytes]:
    """Worker entry point: re-encode a chunk of PNGs as JPEGs."""
    return [_png_to_jpeg(b) for b in png_chunk]


def main() -> int:
    src_uri = "./db/images.lance"
    dst_uri = "./db/images_jpeg.lance"

    if os.path.isdir(dst_uri):
        ds = lance.dataset(dst_uri)
        n = ds.count_rows()
        cols = [f.name for f in ds.schema]
        print(f"{dst_uri} already exists ({n} rows, columns={cols}).")
        return 0

    print(f"reading source from {src_uri} …")
    src = lance.dataset(src_uri)
    n_total = src.count_rows()
    print(f"  {n_total} rows; columns={[f.name for f in src.schema]}")

    # Stream rows in batches so we don't materialise the entire
    # source dataset in memory.
    batch_size = 1000
    n_workers = 24

    def _row_batches():
        for batch in src.to_batches(
            columns=["image", "label", "image_id", "label_cat_dog"],
            batch_size=batch_size,
        ):
            png_list: list[bytes] = batch["image"].to_pylist()
            with ProcessPoolExecutor(max_workers=n_workers) as ex:
                # Split the row batch across workers so each one
                # decodes ~batch_size/n_workers rows in C while
                # holding its own GIL.
                shard = max(1, len(png_list) // n_workers)
                futures = [
                    ex.submit(_convert_chunk, png_list[i : i + shard])
                    for i in range(0, len(png_list), shard)
                ]
                jpeg_list: list[bytes] = []
                for fut in futures:
                    jpeg_list.extend(fut.result())
            assert len(jpeg_list) == batch.num_rows
            yield pa.RecordBatch.from_arrays(
                [
                    pa.array(jpeg_list, type=pa.binary()),
                    batch["label"],
                    batch["image_id"],
                    batch["label_cat_dog"],
                ],
                names=["image_jpeg", "label", "image_id", "label_cat_dog"],
            )

    schema = pa.schema(
        [
            pa.field("image_jpeg", pa.binary()),
            pa.field("label", pa.int16()),
            pa.field("image_id", pa.string()),
            pa.field("label_cat_dog", pa.int16()),
        ]
    )

    print(f"writing {dst_uri} (24 worker processes, batch_size={batch_size}) …")
    t0 = time.time()
    lance.write_dataset(
        _row_batches(),
        dst_uri,
        mode="overwrite",
        schema=schema,
    )
    elapsed = time.time() - t0

    out = lance.dataset(dst_uri)
    print(f"done in {elapsed:.1f}s ({out.count_rows() / elapsed:.1f} rows/s)")
    print(f"  output columns: {[f.name for f in out.schema]}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
