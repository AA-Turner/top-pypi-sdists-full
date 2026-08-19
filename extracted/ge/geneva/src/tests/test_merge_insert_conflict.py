# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Test for GEN-248: merge_insert and Geneva commits create conflicts.

Tests scenarios where merge_insert operations conflict with Geneva backfills.
"""

import logging
import threading
import time
from collections.abc import Callable, Generator
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import timedelta
from pathlib import Path

import pyarrow as pa
import pytest

import geneva
from conftest import make_lance_dataset
from geneva import udf
from geneva.db import Connection
from geneva.table import Table

_LOG = logging.getLogger(__name__)

SIZE = 20
MAX_ROWS_PER_FILE = 5
MAX_MERGE_ROWS = (
    50  # Cap merges so test runtime is bounded regardless of backfill speed
)

pytestmark = [
    pytest.mark.ray,
    pytest.mark.multibackfill,
    pytest.mark.usefixtures("ray_with_test_path"),
]


@pytest.fixture(autouse=True)
def db(tmp_path: Path, tbl_path: Path) -> Generator[Connection, None, None]:
    make_lance_dataset(tbl_path, size=SIZE, max_rows_per_file=MAX_ROWS_PER_FILE)
    db = geneva.connect(str(tmp_path), read_consistency_interval=timedelta(0))
    yield db
    db.close()


@udf(data_type=pa.int32(), checkpoint_size=8, num_cpus=1)
def slow_times_ten(a) -> int:
    time.sleep(0.05)
    return a * 10


SHUFFLE_CONFIG = {
    "batch_size": 1,
    "shuffle_buffer_size": 3,
    "task_shuffle_diversity": None,
}


# --- Helper Classes ---


@dataclass
class OpResults:
    """Track results from background operations."""

    succeeded: list = field(default_factory=list)
    failed: list = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.succeeded) + len(self.failed)


@contextmanager
def background_worker(
    func: Callable[[threading.Event, OpResults], None],
) -> Generator[OpResults, None, None]:
    """Context manager for running background operations during backfill."""
    results = OpResults()
    stop_event = threading.Event()
    thread = threading.Thread(target=func, args=(stop_event, results), daemon=True)
    thread.start()
    try:
        yield results
    finally:
        stop_event.set()
        thread.join(timeout=5.0)


def wait_for_backfill(fut) -> None:
    """Wait for backfill to complete."""
    while not fut.done():
        time.sleep(0.1)


def verify_column_b(tbl: Table, expected_rows: int | None = None) -> pa.Table:
    """Verify column 'b' has no NULLs and return final data."""
    tbl.checkout_latest()
    data = tbl.to_arrow()

    if expected_rows is not None:
        assert data.num_rows == expected_rows, (
            f"Expected {expected_rows} rows, got {data.num_rows}"
        )

    null_count = data["b"].null_count
    assert null_count == 0, f"Found {null_count} NULL values in column 'b'"

    return data


def verify_udf_values(data: pa.Table, size: int = SIZE) -> None:
    """Verify b = a * 10 for original rows."""
    d = data.to_pydict()
    issues = [
        (d["a"][i], d["b"][i])
        for i in range(len(d["a"]))
        if d["a"][i] < size and d["b"][i] != d["a"][i] * 10
    ]
    assert not issues, f"Original rows with wrong 'b' values: {issues[:5]}"


def _is_gen248_conflict(e: BaseException) -> bool:
    """True when the exception chain carries a GEN-248 conflict shape.
    Anything else (setup errors, unrelated crashes) must fail loudly.

    Two shapes qualify: a Lance "commit conflict" (untyped OSError whose
    wording has varied, per geneva.utils.commit_conflict) and fragment
    invalidation -- concurrent compaction removes the fragments a backfill
    is writing, surfacing as "Fragment N not found" (FragmentWriter) inside
    a FragmentWriteFailedError. Checked on every link of the cause/context
    chain; Ray task errors embed the remote message in str(), so they match
    at the top level too."""
    seen: set[int] = set()
    cur: BaseException | None = e
    while cur is not None and id(cur) not in seen:
        seen.add(id(cur))
        msg = str(cur).lower()
        if "commit conflict" in msg or (
            "fragment" in msg and ("invalidat" in msg or "not found" in msg)
        ):
            return True
        cur = cur.__cause__ or cur.__context__
    return False


# --- Tests ---


def test_merge_insert_during_backfill(db: Connection, local_ray_context) -> None:
    """Test merge_insert (new rows) during backfill."""
    tbl = db.open_table("foo")
    tbl.add_columns({"b": slow_times_ten}, **SHUFFLE_CONFIG)

    def merge_new_rows(stop: threading.Event, results: OpResults) -> None:
        next_id = SIZE
        while not stop.is_set() and len(results.succeeded) < MAX_MERGE_ROWS:
            try:
                data = pa.Table.from_pydict({"a": [next_id]})
                tbl.merge_insert("a").when_not_matched_insert_all().execute(data)
                results.succeeded.append(next_id)
                next_id += 1
            except Exception as e:
                results.failed.append((next_id, e))
                next_id += 1
            time.sleep(0.02)

    # Run background_worker while the backfill is going - so we'll get some number of
    # merges, maybe 30, maybe 50, etc.
    with background_worker(merge_new_rows) as merge_results:
        time.sleep(0.1)
        fut = tbl.backfill_async("b", where=None)
        wait_for_backfill(fut)

    # Verify first backfill - original rows should have 'b' computed
    tbl.checkout_latest()
    data = tbl.to_arrow()
    expected_total = SIZE + len(merge_results.succeeded)
    assert data.num_rows == expected_total

    # Original rows should have 'b' computed
    # so {a: [0, 1, 2, 3,... 49], b: [0, 10, 20, 30,... 190, null, null, null, ...]}
    d = data.to_pydict()
    # Nothing in the 'a' column should be NULL.
    original_nulls = [
        d["a"][i] for i in range(len(d["b"])) if d["a"][i] < SIZE and d["b"][i] is None
    ]
    assert not original_nulls, f"Original rows with NULL: {original_nulls}"

    # Second backfill to fill merged rows
    fut2 = tbl.backfill_async("b", where=None)
    wait_for_backfill(fut2)

    final_data = verify_column_b(tbl, expected_total)
    # {a: [0, 1, 2, 3,... 49], b: [0, 10, 20, 30,... 490]}
    verify_udf_values(final_data)


def test_merge_insert_update_during_backfill(db: Connection, local_ray_context) -> None:
    """Test merge_insert updates (no-op on same data) during backfill."""
    tbl = db.open_table("foo")
    tbl.add_columns({"b": slow_times_ten}, **SHUFFLE_CONFIG)

    fut = tbl.backfill_async("b", where=None)

    results = OpResults()
    target = 0
    while not fut.done():
        try:
            row = target % SIZE
            data = pa.Table.from_pydict({"a": [row]})
            tbl.merge_insert(
                "a"
            ).when_matched_update_all().when_not_matched_insert_all().execute(data)
            results.succeeded.append(row)
            target += 1
        except Exception as e:
            results.failed.append((target, e))
            target += 1
        time.sleep(0.05)

    _LOG.info(f"Updates: {results.total} attempted, {len(results.succeeded)} succeeded")
    verify_column_b(tbl, SIZE)


@pytest.mark.xfail(
    reason="GEN-248: merge_insert to same column causes conflict", strict=False
)
def test_merge_insert_same_column_conflict(db: Connection, local_ray_context) -> None:
    """Test merge_insert writing to column 'b' while backfill computes it."""
    tbl = db.open_table("foo")
    tbl.add_columns({"b": slow_times_ten}, **SHUFFLE_CONFIG)

    def merge_with_b_values(stop: threading.Event, results: OpResults) -> None:
        next_id = SIZE
        while not stop.is_set():
            try:
                data = pa.Table.from_pydict({"a": [next_id], "b": [next_id * 100]})
                tbl.merge_insert("a").when_not_matched_insert_all().execute(data)
                results.succeeded.append(next_id)
                next_id += 1
            except Exception as e:
                results.failed.append((next_id, e))
                next_id += 1
            time.sleep(0.02)

    with background_worker(merge_with_b_values):
        time.sleep(0.1)
        fut = tbl.backfill_async("b", where=None)
        wait_for_backfill(fut)

    data = verify_column_b(tbl)
    verify_udf_values(data)


@pytest.mark.xfail(
    reason="GEN-248: merge_insert updates cause fragment invalidation", strict=False
)
def test_merge_insert_update_same_rows(db: Connection, local_ray_context) -> None:
    """Test merge_insert updating column 'b' on same rows backfill is computing."""
    tbl = db.open_table("foo")
    tbl.add_columns({"b": slow_times_ten}, **SHUFFLE_CONFIG)

    def update_existing_rows(stop: threading.Event, results: OpResults) -> None:
        iteration = 0
        while not stop.is_set():
            iteration += 1
            row = iteration % SIZE
            try:
                data = pa.Table.from_pydict({"a": [row], "b": [row * 1000]})
                tbl.merge_insert(
                    "a"
                ).when_matched_update_all().when_not_matched_insert_all().execute(data)
                results.succeeded.append(row)
            except Exception as e:
                results.failed.append((row, e))
            time.sleep(0.02)

    with background_worker(update_existing_rows) as results:
        time.sleep(0.1)
        fut = tbl.backfill_async("b", where=None)
        wait_for_backfill(fut)

    _LOG.info(f"Updates: {results.total} attempted, {len(results.succeeded)} succeeded")

    tbl.checkout_latest()
    data = tbl.to_arrow()
    assert data.num_rows == SIZE

    # Analyze who won
    d = data.to_pydict()
    udf_wins = sum(
        1
        for i in range(len(d["a"]))
        if d["a"][i] < SIZE and d["b"][i] == d["a"][i] * 10
    )
    _LOG.info(f"UDF wins: {udf_wins}/{SIZE}")

    verify_column_b(tbl, SIZE)
    assert udf_wins == SIZE, f"Expected UDF to win all {SIZE} rows, got {udf_wins}"


@pytest.mark.xfail(
    reason="GEN-248: compaction causes fragment invalidation", strict=False
)
def test_compaction_during_backfill(db: Connection, local_ray_context) -> None:
    """Test compaction during backfill."""
    tbl = db.open_table("foo")
    tbl.add_columns({"b": slow_times_ten}, **SHUFFLE_CONFIG)

    def merge_and_compact(stop: threading.Event, results: OpResults) -> None:
        iteration = 0
        while not stop.is_set():
            iteration += 1
            try:
                row = iteration % SIZE
                data = pa.Table.from_pydict({"a": [row], "c": [row * 100]})
                tbl.merge_insert(
                    "a"
                ).when_matched_update_all().when_not_matched_insert_all().execute(data)
                results.succeeded.append(("merge", row))
            except Exception as e:
                results.failed.append(("merge", e))

            if iteration % 5 == 0:
                try:
                    tbl.compact_files()
                    results.succeeded.append(("compact", iteration))
                except Exception as e:
                    results.failed.append(("compact", e))
            time.sleep(0.02)

    with background_worker(merge_and_compact):
        fut = tbl.backfill_async("b", where=None)
        wait_for_backfill(fut)

    verify_column_b(tbl, SIZE)


def test_compaction_during_backfill_srid(
    db: Connection, tmp_path: Path, local_ray_context
) -> None:
    """Compaction during backfill on a stable-row-id table.

    Mirrors test_compaction_during_backfill with stable row ids enabled and a
    merge source the target schema accepts. The tolerated GEN-248 outcomes --
    a backfill commit conflict or NULL gaps in 'b' -- exit via dynamic
    pytest.xfail, and only after two hard gates that run first:

    * the race was actually exercised -- at least one background compaction
      committed while the backfill was in flight, so neither a pass nor an
      xfail can come from merge conflicts alone;
    * no silent corruption -- a non-null 'b' that is not a*10 always fails,
      as does any background or backfill failure that is not a recognized
      GEN-248 conflict (setup errors, unrelated crashes).

    A function-level xfail marker would swallow exactly those signals, so
    this test must not carry one.
    """
    make_lance_dataset(
        tmp_path / "foo_srid.lance",
        size=SIZE,
        max_rows_per_file=MAX_ROWS_PER_FILE,
        stable_row_ids=True,
    )
    tbl = db.open_table("foo_srid")
    tbl.add_columns({"b": slow_times_ten}, **SHUFFLE_CONFIG)

    # Ops carry a completion timestamp so the overlap gate below can tell a
    # compaction that raced the backfill from one that merely bracketed it.
    # The merge source holds only 'a': merge_insert cannot create columns, so
    # naming one outside the target schema would fail every merge and leave
    # compaction racing nothing but the backfill's own commits.
    def merge_and_compact(stop: threading.Event, results: OpResults) -> None:
        iteration = 0
        while not stop.is_set():
            iteration += 1
            try:
                row = iteration % SIZE
                data = pa.Table.from_pydict({"a": [row]})
                tbl.merge_insert(
                    "a"
                ).when_matched_update_all().when_not_matched_insert_all().execute(data)
                results.succeeded.append(("merge", row, time.monotonic()))
            except Exception as e:
                results.failed.append(("merge", e, time.monotonic()))

            if iteration % 5 == 0:
                try:
                    tbl.compact_files()
                    results.succeeded.append(("compact", iteration, time.monotonic()))
                except Exception as e:
                    results.failed.append(("compact", e, time.monotonic()))
            time.sleep(0.02)

    backfill_error: Exception | None = None
    with background_worker(merge_and_compact) as bg:
        backfill_start = time.monotonic()
        fut = tbl.backfill_async("b", where=None)
        wait_for_backfill(fut)
        backfill_end = time.monotonic()
        try:
            fut.result()
        except Exception as e:  # classified below, after the corruption gate
            backfill_error = e

    # Non-vacuity first: without a compaction committed inside the backfill
    # window, whatever this test reports came from merge conflicts or plain
    # NULLs and says nothing about the compaction race it exists to cover.
    compactions = [(tag, ts) for kind, tag, ts in bg.succeeded if kind == "compact"]
    overlapping = [
        ts for _tag, ts in compactions if backfill_start <= ts <= backfill_end
    ]
    assert overlapping, (
        f"compaction race not exercised: {len(compactions)} compaction(s) "
        f"succeeded, none within the backfill window "
        f"({backfill_end - backfill_start:.1f}s); "
        f"failures={[(k, type(e).__name__) for k, e, _ in bg.failed]}"
    )

    # Background failures are tolerated only in the GEN-248 shape; an
    # unrelated crash in the merge/compact thread would otherwise be recorded
    # and silently discarded.
    unexpected = [
        (kind, repr(e)) for kind, e, _ts in bg.failed if not _is_gen248_conflict(e)
    ]
    assert not unexpected, (
        f"unexpected background failure(s), not a GEN-248 conflict: {unexpected[:3]}"
    )

    # Value correctness next: rows that DID get a non-null 'b' must carry the
    # right value. A mismatch here is silent corruption, never a tolerated
    # GEN-248 outcome, so it is asserted before any xfail exit below.
    tbl.checkout_latest()
    d = tbl.to_arrow().to_pydict()
    misaligned = sorted(
        (a, b)
        for a, b in zip(d["a"], d["b"], strict=True)
        if a < SIZE and b is not None and b != a * 10
    )
    assert not misaligned, (
        f"SILENT VALUE MISALIGNMENT on stable-row-id table: non-null b != a*10 "
        f"for {misaligned[:5]} (of {len(misaligned)})"
    )

    if backfill_error is not None:
        if _is_gen248_conflict(backfill_error):
            pytest.xfail(f"GEN-248 conflict: {backfill_error}")
        raise backfill_error

    nulls = sorted(
        a for a, b in zip(d["a"], d["b"], strict=True) if a < SIZE and b is None
    )
    if nulls:
        pytest.xfail(f"GEN-248: NULL gaps in 'b' ({len(nulls)} rows: {nulls[:5]})")

    verify_column_b(tbl, SIZE)
    verify_udf_values(tbl.to_arrow())


@pytest.mark.xfail(reason="GEN-248: deletes cause issues during backfill", strict=False)
def test_delete_during_backfill(db: Connection, local_ray_context) -> None:
    """Test delete during backfill."""
    tbl = db.open_table("foo")
    tbl.add_columns({"b": slow_times_ten}, **SHUFFLE_CONFIG)

    def delete_rows(stop: threading.Event, results: OpResults) -> None:
        count = 0
        while not stop.is_set():
            count += 1
            row = SIZE - 1 - (count % 10)
            try:
                tbl.delete(f"a = {row}")
                results.succeeded.append(row)
            except Exception as e:
                results.failed.append((row, e))
            time.sleep(0.05)

    with background_worker(delete_rows):
        fut = tbl.backfill_async("b", where=None)
        wait_for_backfill(fut)

    tbl.checkout_latest()
    data = tbl.to_arrow()
    null_count = data["b"].null_count
    assert null_count == 0, (
        f"Found {null_count} NULLs after backfill with concurrent deletes"
    )
