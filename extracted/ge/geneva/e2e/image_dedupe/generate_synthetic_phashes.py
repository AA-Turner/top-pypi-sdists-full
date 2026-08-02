#!/usr/bin/env python
# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Generate synthetic perceptual hash (phash) values and write them to a Lance dataset.

This script produces a Lance table with a ``phash`` column
(fixed-size list of 8 uint8 values) suitable for IVF_FLAT indexing
with hamming distance.  It can inject near-duplicate rows (with controlled
bit-flip distance) and is designed to scale to billions of rows by streaming
fragments to disk.

Fragments are generated in parallel using multiple worker processes.
Each fragment is self-contained: duplicates are near-copies of originals
within the same fragment, so no shared state is needed between workers.
"""

from __future__ import annotations

import argparse
import logging
import multiprocessing
import os
import time
from collections import deque
from concurrent.futures import Future, ProcessPoolExecutor
import numpy as np
import pyarrow as pa

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

_LOG = logging.getLogger(__name__)

PHASH_TYPE = pa.list_(pa.uint8(), 8)

SCHEMA = pa.schema(
    [
        pa.field("phash", PHASH_TYPE),
    ]
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _flip_bits(
    phashes: np.ndarray,
    max_bit_flips: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Flip 1..max_bit_flips random bits in each 8-byte phash.

    Parameters
    ----------
    phashes:
        Array of shape ``(n, 8)`` with dtype ``uint8``.
    max_bit_flips:
        Upper bound (inclusive) on the number of bits to flip per row.
    rng:
        Numpy random generator.

    Returns
    -------
    A **copy** of *phashes* with bits flipped.
    """
    bits = np.unpackbits(phashes, axis=1)  # (n, 64) binary
    n = len(bits)
    num_flips = rng.integers(1, max_bit_flips + 1, size=n)
    for i, k in enumerate(num_flips):
        positions = rng.choice(64, size=k, replace=False)
        bits[i, positions] ^= 1
    return np.packbits(bits, axis=1)


def _generate_fragment_data(
    fragment_size: int,
    duplicate_pct: float,
    max_bit_flips: int,
    seed: int,
) -> np.ndarray:
    """Generate one fragment of phash data.

    Each fragment is self-contained: duplicates are near-copies of originals
    within the same fragment.  This makes fragments independent so they can
    be generated in parallel across worker processes.

    Parameters
    ----------
    fragment_size:
        Total rows to generate.
    duplicate_pct:
        Fraction of rows that should be near-duplicates.
    max_bit_flips:
        Max bits flipped when creating a near-duplicate.
    seed:
        Random seed for this fragment.

    Returns
    -------
    An ``(n, 8)`` uint8 numpy array of phash values.
    """
    rng = np.random.default_rng(seed)
    num_duplicates = int(fragment_size * duplicate_pct)
    num_originals = fragment_size - num_duplicates

    originals = rng.integers(0, 256, size=(num_originals, 8), dtype=np.uint8)

    if num_duplicates > 0 and num_originals > 0:
        source_indices = rng.integers(0, num_originals, size=num_duplicates)
        sources = originals[source_indices]
        duplicates = _flip_bits(sources, max_bit_flips, rng)
    elif num_duplicates > 0:
        duplicates = rng.integers(0, 256, size=(num_duplicates, 8), dtype=np.uint8)
    else:
        duplicates = np.empty((0, 8), dtype=np.uint8)

    return np.concatenate([originals, duplicates], axis=0)


def _generate_fragment_data_star(
    args: tuple[int, float, int, int],
) -> np.ndarray:
    """Wrapper for ``pool.map`` which passes a single argument per call."""
    return _generate_fragment_data(*args)


def _numpy_to_table(data: np.ndarray) -> pa.Table:
    """Convert an ``(n, 8)`` uint8 array to a ``pa.Table`` with a ``phash`` column."""
    # pyright ignores: pyarrow type stubs are incomplete for FixedSizeListArray
    # and pa.table() with dict input.
    flat_values: pa.Array = pa.array(data.ravel(), type=pa.uint8())  # pyright: ignore[reportAssignmentType]
    phash_array = pa.FixedSizeListArray.from_arrays(  # pyright: ignore[reportCallIssue]
        flat_values, list_size=8
    )
    return pa.table(  # pyright: ignore[reportCallIssue]
        {"phash": phash_array},
        schema=SCHEMA,
    )


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------


class _LanceLocalWriter:
    """Write fragments directly via pylance (local / object-store paths)."""

    def __init__(self, path: str, storage_options: dict[str, str] | None = None) -> None:
        self._path = path
        self._storage_options = storage_options

    def write(
        self,
        table: pa.Table,
        *,
        first: bool,
        overwrite: bool,
        max_retries: int = 5,
    ) -> None:
        from lance.dataset import write_dataset

        if first:
            mode = "overwrite" if overwrite else "create"
        else:
            mode = "append"

        for attempt in range(1, max_retries + 1):
            try:
                write_dataset(
                    table, self._path, mode=mode, storage_options=self._storage_options
                )
                return
            except OSError as e:
                if attempt == max_retries:
                    raise
                wait = min(2**attempt, 60)
                _LOG.warning(
                    "Write failed (attempt %d/%d), retrying in %ds: %s",
                    attempt,
                    max_retries,
                    wait,
                    e,
                )
                time.sleep(wait)


class _LanceDBWriter:
    """Write via lancedb client (db:// URIs)."""

    def __init__(self, uri: str) -> None:
        import lancedb

        # Split db://host:port/table_name into connection URI and table name.
        # Everything up to the last '/' is the DB URI; the last segment is the
        # table name.
        last_slash = uri.rfind("/")
        self._db_uri = uri[:last_slash]
        self._table_name = uri[last_slash + 1 :]
        self._db = lancedb.connect(self._db_uri)
        self._tbl = None

    def write(self, table: pa.Table, *, first: bool, overwrite: bool) -> None:
        if first:
            if overwrite:
                try:
                    self._db.drop_table(self._table_name)
                except Exception:
                    pass  # table may not exist yet
            self._tbl = self._db.create_table(self._table_name, table)
        else:
            assert self._tbl is not None
            self._tbl.add(table)


def _make_writer(output_path: str) -> _LanceLocalWriter | _LanceDBWriter:
    if output_path.startswith("db://"):
        return _LanceDBWriter(output_path)

    # Build storage_options from environment for cloud URIs.
    storage_options: dict[str, str] | None = None
    if output_path.startswith("az://"):
        storage_options = {}
        account = os.environ.get("AZURE_STORAGE_ACCOUNT")
        if account:
            storage_options["account_name"] = account
        key = os.environ.get("AZURE_STORAGE_KEY")
        if key:
            storage_options["account_key"] = key

    return _LanceLocalWriter(output_path, storage_options=storage_options)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate synthetic phash values and write to a Lance dataset."
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to the output Lance dataset.",
    )
    parser.add_argument(
        "--num-rows",
        type=int,
        required=True,
        help="Total number of rows to generate.",
    )
    parser.add_argument(
        "--duplicate-pct",
        type=float,
        default=0.0,
        help="Fraction of rows that are near-duplicates (0.0-1.0). Default: 0.0",
    )
    parser.add_argument(
        "--max-bit-flips",
        type=int,
        default=3,
        help="Max bits to flip when creating duplicates. Default: 3",
    )
    parser.add_argument(
        "--fragment-size",
        type=int,
        default=1_000_000,
        help="Rows per Lance fragment/batch. Default: 1,000,000",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility. Default: None",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the output dataset if it already exists.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Number of parallel workers for fragment generation. Default: number of CPUs",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    parser = _build_parser()
    args = parser.parse_args(argv)

    num_rows: int = args.num_rows
    fragment_size: int = args.fragment_size
    duplicate_pct: float = args.duplicate_pct
    max_bit_flips: int = args.max_bit_flips
    output_path: str = args.output
    seed: int | None = args.seed
    overwrite: bool = args.overwrite
    workers: int = args.workers or os.cpu_count() or 1

    if not 0.0 <= duplicate_pct <= 1.0:
        parser.error("--duplicate-pct must be between 0.0 and 1.0")
    if num_rows <= 0:
        parser.error("--num-rows must be positive")
    if fragment_size <= 0:
        parser.error("--fragment-size must be positive")
    if max_bit_flips < 1:
        parser.error("--max-bit-flips must be >= 1")
    if max_bit_flips > 64:
        parser.error("--max-bit-flips cannot exceed 64 (phash is 8 bytes = 64 bits)")

    rng = np.random.default_rng(seed)

    # Pre-compute per-fragment parameters.  Each fragment gets its own seed
    # derived from the main RNG so results are reproducible regardless of
    # the number of workers.
    fragment_params: list[tuple[int, float, int, int]] = []
    remaining = num_rows
    while remaining > 0:
        frag_size = min(fragment_size, remaining)
        frag_seed = int(rng.integers(0, 2**63))
        fragment_params.append((frag_size, duplicate_pct, max_bit_flips, frag_seed))
        remaining -= frag_size

    total_fragments = len(fragment_params)
    _LOG.info(
        "Generating %s rows across %d fragments with %d worker(s)",
        f"{num_rows:,}",
        total_fragments,
        workers,
    )

    writer = _make_writer(output_path)

    t0 = time.monotonic()
    rows_written = 0

    def _write_and_log(data: np.ndarray, idx: int) -> None:
        nonlocal rows_written
        table = _numpy_to_table(data)
        writer.write(table, first=(idx == 0), overwrite=overwrite)
        rows_written += len(data)
        elapsed = time.monotonic() - t0
        rows_per_sec = rows_written / elapsed if elapsed > 0 else 0
        pct = rows_written / num_rows * 100
        _LOG.info(
            "Written %s / %s rows (%.1f%%) – %.0f rows/s",
            f"{rows_written:,}",
            f"{num_rows:,}",
            pct,
            rows_per_sec,
        )

    if workers <= 1:
        for i, params in enumerate(fragment_params):
            data = _generate_fragment_data(*params)
            _write_and_log(data, i)
    else:
        # Bounded submission: keep at most `workers * 2` fragments in flight
        # to prevent unbounded memory growth when generation outpaces writes.
        max_in_flight = workers * 2
        pool = ProcessPoolExecutor(
            max_workers=workers,
            mp_context=multiprocessing.get_context("spawn"),
        )
        try:
            pending: deque[tuple[int, Future[np.ndarray]]] = deque()
            param_iter = iter(enumerate(fragment_params))

            # Seed the pipeline
            for _ in range(min(max_in_flight, total_fragments)):
                idx, params = next(param_iter)
                fut = pool.submit(_generate_fragment_data_star, params)
                pending.append((idx, fut))

            while pending:
                # Wait for the oldest result (preserves fragment order)
                idx, fut = pending.popleft()
                _write_and_log(fut.result(), idx)

                # Submit the next fragment if any remain
                try:
                    next_idx, next_params = next(param_iter)
                    next_fut = pool.submit(
                        _generate_fragment_data_star, next_params
                    )
                    pending.append((next_idx, next_fut))
                except StopIteration:
                    pass
        finally:
            pool.shutdown(wait=False)

    elapsed = time.monotonic() - t0
    _LOG.info(
        "Done. Wrote %s rows to %s in %.1fs (%.0f rows/s)",
        f"{rows_written:,}",
        output_path,
        elapsed,
        rows_written / elapsed if elapsed > 0 else 0,
    )


if __name__ == "__main__":
    main()
