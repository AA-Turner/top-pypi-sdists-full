# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

import logging
import queue
import random
import threading
import time
from collections.abc import Generator
from concurrent.futures import (
    ALL_COMPLETED,
    FIRST_COMPLETED,
    Future,
    ThreadPoolExecutor,
    wait,
)
from typing import TYPE_CHECKING

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pytest
from pyarrow.fs import S3FileSystem

from geneva.tqdm import tqdm

_LOG = logging.getLogger(__name__)

if TYPE_CHECKING:
    from geneva.db import Connection
    from geneva.table import Table

ImageBatchGenerator = Generator[pa.Table, None, None]

# Keep this in sync with e2e/large_image_embedding/benchmarks/ray_data_main.py
INPUT_PREFIX = "s3://anonymous@ray-example-data/image-datasets/10TiB-b64encoded-images-in-parquet-v3/"
S3_REGION = "us-west-2"
MIN_ROWS_PER_FRAGMENT = 2048
DEFAULT_BATCH_READAHEAD = 16
DEFAULT_FRAGMENT_READAHEAD = 8
DEFAULT_PREFETCH_CHUNKS = 2
MIN_SCANNER_BATCH_SIZE = 512
DEFAULT_WRITE_CONCURRENCY = 16
DEFAULT_WRITE_MAX_RETRIES = 8
_PREFETCH_DONE = object()


def _parse_anonymous_s3_prefix(prefix: str) -> tuple[str, str]:
    if not prefix.startswith("s3://anonymous@"):
        raise ValueError("Expected s3://anonymous@... prefix")
    without_scheme = prefix[len("s3://anonymous@") :]
    bucket, _, key_prefix = without_scheme.partition("/")
    if not bucket or not key_prefix:
        raise ValueError(f"Invalid S3 prefix: {prefix}")
    return bucket, key_prefix


def _coerce_batch_schema(batch: pa.RecordBatch) -> pa.RecordBatch:
    if "url" not in batch.schema.names or "image" not in batch.schema.names:
        raise RuntimeError(f"Expected columns 'url' and 'image', got {batch.schema}")

    url = batch.column(batch.schema.get_field_index("url"))
    image = batch.column(batch.schema.get_field_index("image"))

    if pa.types.is_string(url.type) or pa.types.is_large_string(url.type):
        url = pc.cast(url, pa.large_string())

    if (
        pa.types.is_string(image.type)
        or pa.types.is_large_string(image.type)
        or pa.types.is_binary(image.type)
    ):
        image = pc.cast(image, pa.large_binary())

    return pa.record_batch([url, image], names=["url", "image"])


def _scanner_batch_size(num_images: int, min_rows_per_fragment: int) -> int:
    if num_images <= 0:
        return MIN_SCANNER_BATCH_SIZE
    return max(
        MIN_SCANNER_BATCH_SIZE,
        min(num_images, max(min_rows_per_fragment, MIN_SCANNER_BATCH_SIZE)),
    )


def _coalesce_batches(
    scanner: ds.Scanner,
    *,
    num_images: int,
    min_rows_per_fragment: int,
) -> Generator[pa.Table, None, None]:
    remaining = num_images
    buffered_batches: list[pa.RecordBatch] = []
    buffered_rows = 0

    for batch in tqdm(scanner.to_batches()):
        if remaining <= 0:
            break
        rb = (
            batch
            if isinstance(batch, pa.RecordBatch)
            else batch.to_record_batch()  # pragma: no cover
        )
        if len(rb) > remaining:
            rb = rb.slice(0, remaining)

        coerced = _coerce_batch_schema(rb)
        buffered_batches.append(coerced)
        buffered_rows += len(coerced)
        remaining -= len(coerced)

        if buffered_rows >= min_rows_per_fragment:
            yield pa.Table.from_batches(buffered_batches)
            buffered_batches = []
            buffered_rows = 0

    if buffered_batches:
        yield pa.Table.from_batches(buffered_batches)

    if remaining > 0:
        pytest.skip(
            "Ray example dataset returned fewer rows than requested: "
            f"missing {remaining} rows"
        )


def _prefetch_tables(
    tables: Generator[pa.Table, None, None], *, prefetch_chunks: int
) -> ImageBatchGenerator:
    if prefetch_chunks <= 0:
        yield from tables
        return

    items: queue.Queue[pa.Table | BaseException | object] = queue.Queue(
        maxsize=prefetch_chunks
    )

    def _producer() -> None:
        try:
            for table in tables:
                items.put(table)
        except BaseException as exc:
            items.put(exc)
        finally:
            items.put(_PREFETCH_DONE)

    producer = threading.Thread(
        target=_producer,
        name="large-image-loader-prefetch",
        daemon=True,
    )
    producer.start()

    while True:
        item = items.get()
        if item is _PREFETCH_DONE:
            break
        if isinstance(item, BaseException):
            raise item
        yield item


def _is_retryable_write_error(exc: BaseException) -> bool:
    msg = str(exc)
    return (
        "Too many concurrent writers" in msg
        or "Commit conflict for version" in msg
    )


def _append_table_chunk(
    tbl: Table,
    chunk: pa.Table,
    *,
    max_retries: int,
) -> int:
    attempt = 0
    while True:
        try:
            tbl.add(chunk)
            return len(chunk)
        except (OSError, RuntimeError) as exc:  # noqa: PERF203
            if attempt >= max_retries or not _is_retryable_write_error(exc):
                raise
            attempt += 1
            backoff = min(10.0, 0.25 * (2 ** min(attempt, 5)))
            backoff += random.uniform(0.0, backoff * 0.1)
            _LOG.warning(
                "Concurrent add failed for chunk with %s rows (attempt %s/%s): %s",
                len(chunk),
                attempt,
                max_retries,
                exc,
            )
            time.sleep(backoff)


def _await_completed_writes(
    inflight: set[Future[int]],
    *,
    require_all: bool,
) -> int:
    if not inflight:
        return 0

    done, pending = wait(
        inflight,
        return_when=ALL_COMPLETED if require_all else FIRST_COMPLETED,
    )
    inflight.clear()
    inflight.update(pending)

    rows_written = 0
    for future in done:
        rows_written += future.result()
    return rows_written


def write_large_image_table(
    db_uri: str,
    table_name: str,
    *,
    num_images: int,
    min_rows_per_fragment: int = MIN_ROWS_PER_FRAGMENT,
    batch_readahead: int = DEFAULT_BATCH_READAHEAD,
    fragment_readahead: int = DEFAULT_FRAGMENT_READAHEAD,
    prefetch_chunks: int = DEFAULT_PREFETCH_CHUNKS,
    write_concurrency: int = DEFAULT_WRITE_CONCURRENCY,
    max_write_retries: int = DEFAULT_WRITE_MAX_RETRIES,
) -> tuple[Connection, Table, int]:
    import geneva

    conn = geneva.connect(db_uri)
    batches = load_large_image_rows(
        num_images=num_images,
        min_rows_per_fragment=min_rows_per_fragment,
        batch_readahead=batch_readahead,
        fragment_readahead=fragment_readahead,
        prefetch_chunks=prefetch_chunks,
    )
    first_batch = next(batches, None)
    if first_batch is None:
        conn.close()
        raise RuntimeError("No image rows produced; cannot create table")

    tbl = conn.create_table(table_name, first_batch, mode="overwrite")
    chunk_count = 1

    if write_concurrency <= 1:
        for batch in batches:
            tbl.add(batch)
            chunk_count += 1
        return conn, tbl, chunk_count

    max_inflight_writes = max(1, write_concurrency * 2)
    inflight: set[Future[int]] = set()

    _LOG.info(
        "Writing large image table %s with write_concurrency=%s, "
        "max_inflight_writes=%s, min_rows_per_fragment=%s",
        table_name,
        write_concurrency,
        max_inflight_writes,
        min_rows_per_fragment,
    )

    with ThreadPoolExecutor(max_workers=write_concurrency) as executor:
        for batch in batches:
            inflight.add(
                executor.submit(
                    _append_table_chunk,
                    tbl,
                    batch,
                    max_retries=max_write_retries,
                )
            )
            chunk_count += 1
            if len(inflight) >= max_inflight_writes:
                _await_completed_writes(inflight, require_all=False)

        _await_completed_writes(inflight, require_all=True)

    _LOG.info(
        "Finished writing large image table %s with %s rows across %s chunks",
        table_name,
        len(tbl),
        chunk_count,
    )
    return conn, tbl, chunk_count


def load_large_image_rows(
    num_images: int = 20,
    *,
    min_rows_per_fragment: int = MIN_ROWS_PER_FRAGMENT,
    batch_readahead: int = DEFAULT_BATCH_READAHEAD,
    fragment_readahead: int = DEFAULT_FRAGMENT_READAHEAD,
    prefetch_chunks: int = DEFAULT_PREFETCH_CHUNKS,
) -> ImageBatchGenerator:
    """
    Yield base64-encoded images from the same dataset used by the Ray benchmark.

    Output tables are coalesced so each `create_table` / `add` call writes a
    large fragment instead of one tiny fragment per scanner batch. A background
    prefetch thread overlaps S3 reads and Arrow decoding with Lance writes.

    Columns:
      - url: string
      - image: bytes (base64-encoded bytes)
    """
    if num_images <= 0:
        return
    if min_rows_per_fragment < 1:
        raise ValueError("min_rows_per_fragment must be at least 1")

    bucket, key_prefix = _parse_anonymous_s3_prefix(INPUT_PREFIX)
    filesystem = S3FileSystem(anonymous=True, region=S3_REGION)
    base_dir = f"{bucket}/{key_prefix}"
    dataset = ds.dataset(base_dir, filesystem=filesystem, format="parquet")
    batch_size = _scanner_batch_size(num_images, min_rows_per_fragment)

    scanner = dataset.scanner(
        columns=["url", "image"],
        batch_size=batch_size,
        batch_readahead=batch_readahead,
        fragment_readahead=fragment_readahead,
        use_threads=True,
    )
    coalesced = _coalesce_batches(
        scanner,
        num_images=num_images,
        min_rows_per_fragment=min_rows_per_fragment,
    )
    yield from _prefetch_tables(coalesced, prefetch_chunks=prefetch_chunks)
