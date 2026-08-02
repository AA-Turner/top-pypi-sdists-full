# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""End-to-end backfill tests for deferred carry-forward of blob outputs.

A filtered re-backfill of a blob carry-forward column under deferred
carry-forward (``GENEVA_DEFER_CARRY_FORWARD=1``) must materialize the old blob
bytes at write time. Before the writer-side fix, the old-column read fell to the
plain Lance scanner and streamed ``struct<position,size>`` descriptors, which
either crashed the overlay merge (mixed matched/unmatched fragments) or silently
committed a corrupt data file (fragments that matched nothing).

These tests cover both output shapes the fix targets — a top-level blob column
and a struct column with a nested blob leaf — and both the overwrite (mixed) and
zero-match paths.

Deferred carry-forward is decided inside the Ray worker (``run_ray_add_column``
reads ``DEFAULT_DEFER_CARRY_FORWARD`` at import), so the env var must be set
before the local cluster starts for the worker to inherit it — see the
``deferred_cf_cluster`` fixture.

The backfills also pass ``_skip_planner_filter_count=True`` ("leaf mode"): the
planner then skips the per-fragment ``count_rows(filter=where)`` and emits a task
for every fragment instead of pruning zero-match ones. This both matches the
production config that hit the bug (filters that aren't index-served) and is what
makes the zero-match fragment actually reach the writer's carry-forward branch.
"""

import contextlib
import os
from collections.abc import Generator
from pathlib import Path

import lance
import pyarrow as pa
import pytest

import geneva
from geneva import udf
from geneva.db import Connection

NUM_ROWS = 20
MAX_ROWS_PER_FILE = 2  # 10 fragments; each holds one even + one odd row

pytestmark = [pytest.mark.ray, pytest.mark.multibackfill]

_BLOB_ENCODING = {"lance-encoding:blob": "true"}
_IMG_STRUCT = pa.struct(
    [
        pa.field("image_bytes", pa.large_binary(), metadata=_BLOB_ENCODING),
        pa.field("w", pa.int64()),
    ]
)


@udf(
    data_type=pa.large_binary(),
    field_metadata=_BLOB_ENCODING,
    checkpoint_size=8,
    num_cpus=0.1,
)
def blob_enc_v1(a: int) -> bytes:
    return f"v1-{a}".encode()


@udf(
    data_type=pa.large_binary(),
    field_metadata=_BLOB_ENCODING,
    checkpoint_size=8,
    num_cpus=0.1,
)
def blob_enc_v2(a: int) -> bytes:
    return f"v2-{a}".encode()


@udf(data_type=_IMG_STRUCT, checkpoint_size=8, num_cpus=0.1)
def img_v1(a: int) -> dict:
    return {"image_bytes": f"v1-{a}".encode(), "w": a}


@udf(data_type=_IMG_STRUCT, checkpoint_size=8, num_cpus=0.1)
def img_v2(a: int) -> dict:
    return {"image_bytes": f"v2-{a}".encode(), "w": a}


@pytest.fixture(scope="module", autouse=True)
def deferred_cf_cluster() -> Generator[None, None, None]:
    """Start a local Ray cluster with deferred carry-forward forced on.

    The flag is read at module import inside the worker, so it must be set in the
    driver env *before* the cluster (and its workers) start. A fresh cluster is
    used so the workers inherit the env var rather than reusing a stale one.
    """
    import ray

    with contextlib.suppress(Exception):
        ray.shutdown()
    prev = os.environ.get("GENEVA_DEFER_CARRY_FORWARD")
    os.environ["GENEVA_DEFER_CARRY_FORWARD"] = "1"
    try:
        with Connection.local_ray_context():
            _assert_worker_defer_enabled()
            yield
    finally:
        if prev is None:
            os.environ.pop("GENEVA_DEFER_CARRY_FORWARD", None)
        else:
            os.environ["GENEVA_DEFER_CARRY_FORWARD"] = prev


def _assert_worker_defer_enabled() -> None:
    """Fail loudly if deferred carry-forward is not actually engaged in the Ray
    worker.

    The deferral decision (skip scanning the carry-forward column during
    planning, then fill it at write time) is made inside the worker process,
    where ``DEFAULT_DEFER_CARRY_FORWARD`` is read from the env at import. If the
    env var failed to reach the worker, these tests would silently exercise the
    non-deferred path instead of the one under test — so assert the worker sees
    it on.
    """
    import ray

    @ray.remote
    def _worker_flag() -> bool:
        import geneva.runners.ray.pipeline as pipeline

        return pipeline.DEFAULT_DEFER_CARRY_FORWARD

    assert ray.get(_worker_flag.remote()) is True, (
        "deferred carry-forward (GENEVA_DEFER_CARRY_FORWARD) is not enabled in "
        "the Ray worker; these tests must run with the deferred path engaged"
    )


@pytest.fixture
def db(tmp_path: Path) -> Generator[Connection, None, None]:
    """A 10-fragment table (20 rows, 2 rows/fragment) with key column ``a``."""
    lance.write_dataset(
        pa.table({"a": pa.array(range(NUM_ROWS))}),
        str(tmp_path / "foo.lance"),
        max_rows_per_file=MAX_ROWS_PER_FILE,
        data_storage_version="2.0",
    )
    conn = geneva.connect(str(tmp_path))
    yield conn
    conn.close()


def _read_blob_bytes_by_a(tbl, blob_path: str) -> dict[int, bytes]:
    """Read a blob-encoded column back as bytes keyed by each row's ``a``.

    Blob columns read back as ``{position, size}`` descriptors, so the bytes are
    fetched via ``take_blobs`` (which accepts a dotted path for a nested leaf).
    ``a`` and the blobs come from the same dataset handle so row order aligns.
    """
    ds = lance.dataset(tbl.uri)
    a_vals = ds.to_table(columns=["a"])["a"].to_pylist()
    blobs = ds.take_blobs(blob_path, indices=list(range(len(a_vals))))
    return {int(a): bf.read() for a, bf in zip(a_vals, blobs, strict=True)}


def test_output_blob_carryforward_overwrite(db: Connection) -> None:
    """Top-level blob output: a filtered re-backfill recomputes matched rows and
    carries the old blob forward for unmatched rows. Every fragment here is mixed
    (one matched + one unmatched), so each exercises the overlay merge."""
    tbl = db.open_table("foo")
    tbl.add_columns({"b": blob_enc_v1})
    tbl.backfill_async("b", where="1=1", _skip_planner_filter_count=True).result()
    tbl.checkout_latest()
    assert _read_blob_bytes_by_a(tbl, "b") == {
        a: f"v1-{a}".encode() for a in range(NUM_ROWS)
    }

    tbl.alter_columns({"path": "b", "udf": blob_enc_v2})
    tbl.checkout_latest()
    tbl.backfill_async("b", where="a % 2 = 0", _skip_planner_filter_count=True).result()
    tbl.checkout_latest()

    result = _read_blob_bytes_by_a(tbl, "b")
    for a in range(NUM_ROWS):
        want = f"v2-{a}".encode() if a % 2 == 0 else f"v1-{a}".encode()
        assert result[a] == want, f"row a={a}: got {result[a]!r}, want {want!r}"


def test_output_struct_blob_carryforward_overwrite(db: Connection) -> None:
    """Struct output with a nested blob leaf (``img.image_bytes``): the same
    overwrite semantics must hold for the struct-with-nested-blob shape."""
    tbl = db.open_table("foo")
    tbl.add_columns({"img": img_v1})
    tbl.backfill_async("img", where="1=1", _skip_planner_filter_count=True).result()
    tbl.checkout_latest()
    assert _read_blob_bytes_by_a(tbl, "img.image_bytes") == {
        a: f"v1-{a}".encode() for a in range(NUM_ROWS)
    }

    tbl.alter_columns({"path": "img", "udf": img_v2})
    tbl.checkout_latest()
    tbl.backfill_async(
        "img", where="a % 2 = 0", _skip_planner_filter_count=True
    ).result()
    tbl.checkout_latest()

    result = _read_blob_bytes_by_a(tbl, "img.image_bytes")
    for a in range(NUM_ROWS):
        want = f"v2-{a}".encode() if a % 2 == 0 else f"v1-{a}".encode()
        assert result[a] == want, f"row a={a}: got {result[a]!r}, want {want!r}"


def test_output_blob_zero_match_carryforward(db: Connection) -> None:
    """Guard the silent-corruption path: a filter that matches NO rows makes
    every fragment take the zero-match carry-forward branch (no overlay merge).
    The blob column must be rewritten as materialized bytes, never descriptor
    structs, so all rows still read back as their original v1 bytes.

    ``_skip_planner_filter_count=True`` (leaf mode) is required: otherwise the
    planner runs ``count_rows(filter=where)`` per fragment and prunes every
    zero-match fragment before it reaches the writer, so the carry-forward branch
    would never run and this test would pass trivially without exercising it."""
    tbl = db.open_table("foo")
    tbl.add_columns({"b": blob_enc_v1})
    tbl.backfill_async("b", where="1=1", _skip_planner_filter_count=True).result()
    tbl.checkout_latest()

    tbl.alter_columns({"path": "b", "udf": blob_enc_v2})
    tbl.checkout_latest()
    tbl.backfill_async(
        "b", where="a >= 100", _skip_planner_filter_count=True
    ).result()  # matches nothing
    tbl.checkout_latest()

    result = _read_blob_bytes_by_a(tbl, "b")
    for a in range(NUM_ROWS):
        assert result[a] == f"v1-{a}".encode(), (
            f"row a={a} matched no filter; must keep v1 (got {result[a]!r})"
        )
