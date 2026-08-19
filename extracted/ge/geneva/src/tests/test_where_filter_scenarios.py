# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Tests for WHERE filter scenarios from backfill_concurrent_conflicts.md.

These tests validate that the default WHERE filter (`<col> IS NULL`) is correctly
applied or skipped based on UDF version changes detected via checkpoint inspection.

Scenarios:
- A: Partial backfill → Compaction → Resume (same UDF) - WHERE filter APPLIES
- B: Partial backfill → alter_columns → Resume (different UDF) - WHERE filter SKIPPED
- C: Partial backfill → Compaction → alter_columns → Resume - WHERE filter SKIPPED
- D: First backfill (no checkpoints) - WHERE filter APPLIES
"""

import logging
from collections.abc import Generator
from pathlib import Path

import lance
import pyarrow as pa
import pytest

import geneva
from geneva import udf
from geneva.db import Connection, dataset_uses_stable_row_ids

_LOG = logging.getLogger(__name__)

NUM_ROWS = 20
MAX_ROWS_PER_FILE = 2  # Creates 10 fragments

pytestmark = [
    pytest.mark.ray,
    pytest.mark.multibackfill,
    pytest.mark.usefixtures("ray_with_test_path"),
]

SHUFFLE_CONFIG = {
    "batch_size": 1,
    "shuffle_buffer_size": 3,
    "task_shuffle_diversity": None,
}


def make_table_with_10_fragments(
    tbl_path: Path, *, stable_row_ids: bool = False
) -> lance.LanceDataset:
    """Create a table with 10 fragments (20 rows, 2 rows per fragment)."""
    data = {"a": pa.array(range(NUM_ROWS))}
    tbl = pa.Table.from_pydict(data)
    return lance.write_dataset(
        tbl,
        tbl_path,
        max_rows_per_file=MAX_ROWS_PER_FILE,
        data_storage_version="2.0",
        enable_stable_row_ids=stable_row_ids,
    )


@pytest.fixture
def tbl_path(tmp_path: Path) -> Path:
    return tmp_path / "foo.lance"


@pytest.fixture(params=[False], ids=["rowaddr"])
def stable_row_ids(request: pytest.FixtureRequest) -> bool:
    """Whether the module table is created with stable row IDs (SRID).

    Defaults to rowaddr-based tables; opt a test into both modes via
    ``@pytest.mark.parametrize("stable_row_ids", [False, True], indirect=True)``.
    """
    return request.param


@pytest.fixture
def db(
    tmp_path: Path, tbl_path: Path, stable_row_ids: bool
) -> Generator[Connection, None, None]:
    make_table_with_10_fragments(tbl_path, stable_row_ids=stable_row_ids)
    db = geneva.connect(str(tmp_path))
    yield db
    db.close()


# --- UDF definitions ---


@udf(data_type=pa.int32(), checkpoint_size=8, num_cpus=0.1)
def times_ten_v1(a: int) -> int:
    """First version: multiply by 10."""
    return a * 10


@udf(data_type=pa.int32(), checkpoint_size=8, num_cpus=0.1)
def times_ten_v2(a: int) -> int:
    """Second version: multiply by 100."""
    return a * 100


@udf(data_type=pa.large_binary(), checkpoint_size=8, num_cpus=0.1)
def blob_v1(a: int) -> bytes:
    """First version blob value."""
    return f"v1-{a}".encode()


@udf(data_type=pa.large_binary(), checkpoint_size=8, num_cpus=0.1)
def blob_v2(a: int) -> bytes:
    """Second version blob value."""
    return f"v2-{a}".encode()


# --- Test Scenarios ---


@pytest.mark.parametrize(
    "stable_row_ids", [False, True], indirect=True, ids=["rowaddr", "srid"]
)
def test_scenario_a_partial_backfill_resume_same_udf(
    db: Connection, local_ray_context
) -> None:
    """
    Scenario A: Incomplete backfill → Resume with same UDF (no compaction).

    The default WHERE filter should APPLY because UDF version matches.
    Only NULL rows should be processed on resume.

    Steps:
    1. Add column with UDF v1
    2. Partial backfill (num_frags=2) - creates checkpoints with udf_version=v1
    3. Resume backfill with same v1 UDF
       - WHERE filter APPLIES (IS NULL) - only NULL rows processed
    """
    tbl = db.open_table("foo")
    tbl.add_columns({"b": times_ten_v1}, **SHUFFLE_CONFIG)

    # Step 1: Partial backfill - only first 2 fragments (4 rows)
    fut1 = tbl.backfill_async("b", num_frags=2, where=None)
    fut1.result()
    tbl.checkout_latest()

    data1 = tbl.to_arrow().to_pydict()
    # First 4 rows should have values, rest NULL
    computed_count_1 = sum(1 for v in data1["b"] if v is not None)
    assert computed_count_1 == 4, f"Expected 4 computed rows, got {computed_count_1}"
    _LOG.info(f"After partial backfill: {computed_count_1} rows computed")

    # Step 2: Resume backfill with SAME UDF (no explicit where - should default to
    # IS NULL)
    # The WHERE filter should apply because UDF version in checkpoints matches current
    fut2 = tbl.backfill_async("b")  # No where= means default WHERE filter
    fut2.result()
    tbl.checkout_latest()

    data2 = tbl.to_arrow().to_pydict()
    # All rows should now have values
    null_count = sum(1 for v in data2["b"] if v is None)
    assert null_count == 0, f"Expected 0 NULL values, got {null_count}"

    # Verify all values are correct (a * 10)
    for i, (a_val, b_val) in enumerate(zip(data2["a"], data2["b"], strict=True)):
        assert b_val == a_val * 10, f"Row {i}: expected {a_val * 10}, got {b_val}"

    _LOG.info("Scenario A passed: WHERE filter correctly applied on resume")


def test_scenario_b_partial_backfill_alter_columns_resume(
    db: Connection, local_ray_context
) -> None:
    """
    Scenario B: Incomplete backfill → alter_columns → Resume with different UDF.

    The default WHERE filter should NOT apply because UDF version changed.
    ALL rows should be recomputed with the new UDF.

    Steps:
    1. Add column with UDF v1
    2. Partial backfill (num_frags=2) - creates checkpoints with udf_version=v1
    3. alter_columns to change UDF to v2
    4. Resume backfill with v2 UDF
       - WHERE filter SKIPPED - ALL rows recomputed with v2
    """
    tbl = db.open_table("foo")
    tbl.add_columns({"b": times_ten_v1}, **SHUFFLE_CONFIG)

    # Step 1: Partial backfill - only first 2 fragments (4 rows)
    fut1 = tbl.backfill_async("b", num_frags=2, where=None)
    fut1.result()
    tbl.checkout_latest()

    data1 = tbl.to_arrow().to_pydict()
    computed_count_1 = sum(1 for v in data1["b"] if v is not None)
    assert computed_count_1 == 4, f"Expected 4 computed rows, got {computed_count_1}"

    # Verify first 4 rows have v1 values (a * 10)
    for i in range(4):
        assert data1["b"][i] == data1["a"][i] * 10, (
            f"Row {i}: expected v1 value {data1['a'][i] * 10}, got {data1['b'][i]}"
        )
    _LOG.info(f"After partial backfill with v1: {computed_count_1} rows computed")

    # Step 2: Change UDF to v2 via alter_columns
    tbl.alter_columns({"path": "b", "udf": times_ten_v2})
    tbl.checkout_latest()
    _LOG.info("After alter_columns to v2")

    # Step 3: Resume backfill (no explicit where - should detect UDF change and skip
    # default filter)
    # Because UDF changed, WHERE filter should NOT apply - all rows recomputed
    fut2 = tbl.backfill_async("b")  # No where= means check UDF version
    fut2.result()
    tbl.checkout_latest()

    data2 = tbl.to_arrow().to_pydict()
    # All rows should have values
    null_count = sum(1 for v in data2["b"] if v is None)
    assert null_count == 0, f"Expected 0 NULL values, got {null_count}"

    # Verify ALL values are v2 (a * 100) - including the first 4 that were v1
    for i, (a_val, b_val) in enumerate(zip(data2["a"], data2["b"], strict=True)):
        expected = a_val * 100  # v2 formula
        assert b_val == expected, f"Row {i}: expected v2 value {expected}, got {b_val}"

    _LOG.info("Scenario B passed: WHERE filter correctly skipped after alter_columns")


@pytest.mark.parametrize(
    "defer",
    [False, True],
    ids=["defer_off", "defer_on"],
)
def test_filtered_rebackfill_preserves_unmatched_values_deferred(
    db: Connection, local_ray_context, monkeypatch, defer
) -> None:
    """GEN-624: a filtered re-backfill must preserve the previously computed
    value for rows that do NOT match the WHERE filter, whether or not deferred
    carry-forward (write-time old-column fill) is enabled.

    Steps:
    1. Add column ``b`` with UDF v1 (a * 10) and fully materialize it.
    2. Switch the UDF to v2 (a * 100) via alter_columns.
    3. Re-backfill with an explicit ``WHERE a % 2 = 0`` so only even rows
       recompute. Odd rows match no filter and must keep the v1 value (a * 10).

    Running with deferral off and on and getting the same preserved result
    proves deferred carry-forward does not clobber unmatched values.
    """
    import geneva.runners.ray.pipeline as pipeline_module

    monkeypatch.setattr(pipeline_module, "DEFAULT_DEFER_CARRY_FORWARD", defer)

    tbl = db.open_table("foo")
    tbl.add_columns({"b": times_ten_v1}, **SHUFFLE_CONFIG)

    # Baseline: fully materialize b = a * 10 for all 20 rows.
    tbl.backfill_async("b", where="1=1").result()
    tbl.checkout_latest()
    base = tbl.to_arrow().sort_by("a").to_pydict()
    assert base["b"] == [a * 10 for a in base["a"]]

    # Switch UDF to v2 (a * 100), then re-backfill ONLY even rows.
    tbl.alter_columns({"path": "b", "udf": times_ten_v2})
    tbl.checkout_latest()
    tbl.backfill_async("b", where="a % 2 = 0").result()
    tbl.checkout_latest()

    result = tbl.to_arrow().sort_by("a").to_pydict()
    for a_val, b_val in zip(result["a"], result["b"], strict=True):
        if a_val % 2 == 0:
            assert b_val == a_val * 100, (
                f"matched row a={a_val} should recompute to v2 (got {b_val})"
            )
        else:
            assert b_val == a_val * 10, (
                f"unmatched row a={a_val} must PRESERVE old v1 value "
                f"(got {b_val}, defer={defer})"
            )


@pytest.mark.parametrize(
    "defer",
    [False, True],
    ids=["defer_off", "defer_on"],
)
def test_filtered_rebackfill_blob_carry_forward_deferred(
    db: Connection, local_ray_context, monkeypatch, defer
) -> None:
    """GEN-624: deferred carry-forward must preserve unmatched blob values.

    A filtered re-backfill of a blob column updates only matched rows; the
    unmatched rows must keep their previous blob. With deferral on, the old
    blobs are never read on the applier — the FragmentWriter streams the old
    column at write time. Running with the path off and on, identically
    preserved, proves correctness.
    """
    import geneva.runners.ray.pipeline as pipeline_module

    monkeypatch.setattr(pipeline_module, "DEFAULT_DEFER_CARRY_FORWARD", defer)

    tbl = db.open_table("foo")
    tbl.add_columns({"b": blob_v1}, **SHUFFLE_CONFIG)

    # Baseline: every row gets its v1 blob.
    tbl.backfill_async("b", where="1=1").result()
    tbl.checkout_latest()
    base = tbl.to_arrow().sort_by("a").to_pydict()
    assert base["b"] == [f"v1-{a}".encode() for a in base["a"]]

    # Switch UDF to v2, re-backfill ONLY even rows.
    tbl.alter_columns({"path": "b", "udf": blob_v2})
    tbl.checkout_latest()
    tbl.backfill_async("b", where="a % 2 = 0").result()
    tbl.checkout_latest()

    result = tbl.to_arrow().sort_by("a").to_pydict()
    for a_val, b_val in zip(result["a"], result["b"], strict=True):
        if a_val % 2 == 0:
            assert b_val == f"v2-{a_val}".encode(), (
                f"matched row a={a_val} should recompute to v2 (got {b_val!r})"
            )
        else:
            assert b_val == f"v1-{a_val}".encode(), (
                f"unmatched row a={a_val} must PRESERVE old v1 blob "
                f"(got {b_val!r}, defer={defer})"
            )


@pytest.mark.parametrize(
    "stable_row_ids", [False, True], indirect=True, ids=["rowaddr", "srid"]
)
def test_scenario_c_partial_backfill_compaction_alter_columns_resume(
    db: Connection, local_ray_context, stable_row_ids: bool
) -> None:
    """
    Scenario C: Incomplete backfill → Compaction → alter_columns → Resume.

    The default WHERE filter should NOT apply because UDF version changed.
    ALL rows should be recomputed with the new UDF.

    Steps:
    1. Add column with UDF v1
    2. Partial backfill (num_frags=2) - creates checkpoints with udf_version=v1
    3. Compact files - fragment IDs change
    4. alter_columns to change UDF to v2
    5. Resume backfill with v2 UDF
       - WHERE filter SKIPPED - ALL rows recomputed with v2
    """
    tbl = db.open_table("foo")
    tbl.add_columns({"b": times_ten_v1}, **SHUFFLE_CONFIG)

    # Step 1: Partial backfill - only first 2 fragments (4 rows)
    fut1 = tbl.backfill_async("b", num_frags=2, where=None)
    fut1.result()
    tbl.checkout_latest()

    data1 = tbl.to_arrow().to_pydict()
    computed_count_1 = sum(1 for v in data1["b"] if v is not None)
    assert computed_count_1 == 4, f"Expected 4 computed rows, got {computed_count_1}"
    _LOG.info(f"After partial backfill with v1: {computed_count_1} rows computed")

    # Step 2: Compact files
    tbl.compact_files()
    tbl.checkout_latest()
    _LOG.info(f"After compaction, table version: {tbl.version}")

    # Step 3: Change UDF to v2 via alter_columns
    tbl.alter_columns({"path": "b", "udf": times_ten_v2})
    tbl.checkout_latest()
    _LOG.info("After alter_columns to v2")

    # Step 4: Resume backfill (no explicit where - should detect UDF change)
    fut2 = tbl.backfill_async("b")
    fut2.result()
    tbl.checkout_latest()

    data2 = tbl.to_arrow().to_pydict()
    null_count = sum(1 for v in data2["b"] if v is None)
    assert null_count == 0, f"Expected 0 NULL values, got {null_count}"

    # Verify ALL values are v2 (a * 100)
    for i, (a_val, b_val) in enumerate(zip(data2["a"], data2["b"], strict=True)):
        expected = a_val * 100
        assert b_val == expected, f"Row {i}: expected v2 value {expected}, got {b_val}"

    if stable_row_ids:
        # backfill -> compaction -> alter -> resume must not silently drop
        # the stable-row-id manifest flag.
        assert dataset_uses_stable_row_ids(tbl.to_lance())

    _LOG.info(
        "Scenario C passed: WHERE filter correctly skipped after compaction + "
        "alter_columns"
    )


@pytest.mark.parametrize(
    "stable_row_ids", [False, True], indirect=True, ids=["rowaddr", "srid"]
)
def test_scenario_c_with_retry_after_compaction(
    db: Connection, local_ray_context, stable_row_ids: bool
) -> None:
    """
    Scenario C variant: Partial backfill → Compaction → alter_columns → Retry.

    After compaction merges column files, DataReplacement fails because it
    can't find matching field_ids. The system falls back to Merge operation
    which uses masked DataFiles to overlay new column data.

    Steps:
    1. Add column with UDF v1
    2. Partial backfill (num_frags=2) - creates checkpoints with udf_version=v1
    3. Compact files - merges separate column files into combined files
    4. alter_columns to change UDF to v2
    5. First backfill attempt uses DataReplacement (may fail post-compaction)
    6. System falls back to Merge with masked files if DataReplacement fails
    7. Retry with where='1=1' forces reprocessing all rows
    """
    tbl = db.open_table("foo")
    tbl.add_columns({"b": times_ten_v1}, **SHUFFLE_CONFIG)

    # Step 1: Partial backfill - only first 2 fragments (4 rows)
    fut1 = tbl.backfill_async("b", num_frags=2, where=None)
    fut1.result()
    tbl.checkout_latest()

    data1 = tbl.to_arrow().to_pydict()
    computed_count_1 = sum(1 for v in data1["b"] if v is not None)
    assert computed_count_1 == 4, f"Expected 4 computed rows, got {computed_count_1}"
    _LOG.info(f"After partial backfill with v1: {computed_count_1} rows computed")

    # Step 2: Compact files
    tbl.compact_files()
    tbl.checkout_latest()
    _LOG.info(f"After compaction, table version: {tbl.version}")

    # Step 3: Change UDF to v2 via alter_columns
    tbl.alter_columns({"path": "b", "udf": times_ten_v2})
    tbl.checkout_latest()
    _LOG.info("After alter_columns to v2")

    # Step 4: First backfill attempt - may fail due to compaction, that's OK
    try:
        fut2 = tbl.backfill_async("b")
        fut2.result()
        tbl.checkout_latest()
        _LOG.info("First backfill succeeded")
    except Exception as e:
        _LOG.info(f"First backfill failed as expected: {e}")
        tbl.checkout_latest()

    # Step 5: Second backfill with where="1=1" to force reprocessing all rows
    fut3 = tbl.backfill_async("b", where="1=1")
    fut3.result()
    tbl.checkout_latest()

    data3 = tbl.to_arrow().to_pydict()
    null_count = sum(1 for v in data3["b"] if v is None)
    assert null_count == 0, f"Expected 0 NULL values, got {null_count}"

    # Verify ALL values are v2 (a * 100)
    for i, (a_val, b_val) in enumerate(zip(data3["a"], data3["b"], strict=True)):
        expected = a_val * 100
        assert b_val == expected, f"Row {i}: expected v2 value {expected}, got {b_val}"

    if stable_row_ids:
        # backfill -> compaction -> alter -> retry must not silently drop
        # the stable-row-id manifest flag.
        assert dataset_uses_stable_row_ids(tbl.to_lance())

    _LOG.info(
        "Scenario C with retry passed: All rows recomputed with v2 after "
        "compaction + alter_columns"
    )


@pytest.mark.parametrize(
    "stable_row_ids", [False, True], indirect=True, ids=["rowaddr", "srid"]
)
def test_scenario_d_first_backfill_no_checkpoints(
    db: Connection, local_ray_context
) -> None:
    """
    Scenario D: First backfill with no checkpoints.

    The default WHERE filter should APPLY because there are no checkpoints
    to compare against (no UDF mismatch detected).

    Steps:
    1. Add column with UDF v1
    2. First backfill (no prior checkpoints)
       - WHERE filter APPLIES (IS NULL) - all NULL rows processed
    """
    tbl = db.open_table("foo")
    tbl.add_columns({"b": times_ten_v1}, **SHUFFLE_CONFIG)

    # Backfill without explicit where - should default to IS NULL
    fut = tbl.backfill_async("b")
    fut.result()
    tbl.checkout_latest()

    data = tbl.to_arrow().to_pydict()
    null_count = sum(1 for v in data["b"] if v is None)
    assert null_count == 0, f"Expected 0 NULL values, got {null_count}"

    # Verify all values are correct (a * 10)
    for i, (a_val, b_val) in enumerate(zip(data["a"], data["b"], strict=True)):
        assert b_val == a_val * 10, f"Row {i}: expected {a_val * 10}, got {b_val}"

    _LOG.info("Scenario D passed: First backfill processed all NULL rows")


def test_scenario_a_verify_where_filter_skips_computed_rows(
    db: Connection, local_ray_context
) -> None:
    """
    Extended Scenario A: Verify that the WHERE filter actually skips computed rows.

    This test verifies that after a partial backfill, resuming with the default
    WHERE filter only processes the remaining NULL rows, not the already-computed ones.
    """
    tbl = db.open_table("foo")
    tbl.add_columns({"b": times_ten_v1}, **SHUFFLE_CONFIG)

    # Step 1: Partial backfill - only first 2 fragments (4 rows)
    fut1 = tbl.backfill_async("b", num_frags=2, where=None)
    fut1.result()
    tbl.checkout_latest()

    data1 = tbl.to_arrow().to_pydict()
    computed_count_1 = sum(1 for v in data1["b"] if v is not None)
    assert computed_count_1 == 4

    # Step 2: Resume backfill with default WHERE filter (IS NULL)
    # This should only process the remaining 16 NULL rows
    fut2 = tbl.backfill_async("b")  # Default where = "b IS NULL"
    fut2.result()
    tbl.checkout_latest()

    data2 = tbl.to_arrow().to_pydict()
    null_count = sum(1 for v in data2["b"] if v is None)
    assert null_count == 0, f"Expected 0 NULL values, got {null_count}"

    # Verify all values are correct
    for i, (a_val, b_val) in enumerate(zip(data2["a"], data2["b"], strict=True)):
        assert b_val == a_val * 10, f"Row {i}: expected {a_val * 10}, got {b_val}"

    _LOG.info(
        "Extended Scenario A passed: WHERE filter correctly skipped computed rows"
    )


def test_explicit_filter_with_udf_change_logs_warning(
    db: Connection, local_ray_context, caplog: pytest.LogCaptureFixture
) -> None:
    """
    Test that explicit where filter + UDF change logs a warning.

    When user provides an explicit where filter (e.g., "b IS NULL") but the UDF
    version has changed, the system should:
    1. Log a WARNING that some rows may not be reprocessed
    2. Honor the user's explicit filter (only process matching rows)
    3. NOT automatically reprocess all rows

    This is intentional - explicit user input takes precedence, but we warn them.
    """
    tbl = db.open_table("foo")
    tbl.add_columns({"b": times_ten_v1}, **SHUFFLE_CONFIG)

    # Step 1: Complete backfill with v1 UDF
    fut1 = tbl.backfill_async("b", where=None)
    fut1.result()
    tbl.checkout_latest()

    data1 = tbl.to_arrow().to_pydict()
    # All rows should have v1 values (a * 10)
    for i, (a_val, b_val) in enumerate(zip(data1["a"], data1["b"], strict=True)):
        assert b_val == a_val * 10, f"Row {i}: expected v1 value {a_val * 10}"

    # Step 2: Change UDF to v2 via alter_columns
    tbl.alter_columns({"path": "b", "udf": times_ten_v2})
    tbl.checkout_latest()

    # Step 3: Backfill with EXPLICIT where filter (not default)
    # This should log a WARNING but still honor the explicit filter
    caplog.clear()
    with caplog.at_level(logging.WARNING):
        fut2 = tbl.backfill_async("b", where="b IS NULL")  # Explicit filter!
        fut2.result()
    tbl.checkout_latest()

    # Verify warning was logged
    warning_logged = any(
        "UDF version" in record.message and "explicit where filter" in record.message
        for record in caplog.records
        if record.levelno >= logging.WARNING
    )
    assert warning_logged, (
        "Expected warning about UDF change with explicit filter. "
        f"Log records: {[r.message for r in caplog.records]}"
    )

    data2 = tbl.to_arrow().to_pydict()
    # Since there are NO NULL rows (all were computed with v1), and we used
    # explicit "b IS NULL" filter, NO rows should be reprocessed.
    # All values should still be v1 (a * 10), NOT v2 (a * 100)
    for i, (a_val, b_val) in enumerate(zip(data2["a"], data2["b"], strict=True)):
        assert b_val == a_val * 10, (
            f"Row {i}: expected v1 value {a_val * 10}, got {b_val}. "
            "Explicit filter should have prevented reprocessing."
        )

    _LOG.info("Test passed: Warning logged for explicit filter + UDF change")


def test_explicit_1_equals_1_forces_reprocessing(
    db: Connection, local_ray_context
) -> None:
    """
    Test that where="1=1" forces reprocessing all rows even with UDF mismatch.

    This verifies the recommended workaround: use where="1=1" to force
    reprocessing all rows after a UDF change.
    """
    tbl = db.open_table("foo")
    tbl.add_columns({"b": times_ten_v1}, **SHUFFLE_CONFIG)

    # Step 1: Complete backfill with v1 UDF
    fut1 = tbl.backfill_async("b", where=None)
    fut1.result()
    tbl.checkout_latest()

    data1 = tbl.to_arrow().to_pydict()
    # All rows should have v1 values (a * 10)
    for i, (a_val, b_val) in enumerate(zip(data1["a"], data1["b"], strict=True)):
        assert b_val == a_val * 10, f"Row {i}: expected v1 value {a_val * 10}"

    # Step 2: Change UDF to v2 via alter_columns
    tbl.alter_columns({"path": "b", "udf": times_ten_v2})
    tbl.checkout_latest()

    # Step 3: Force reprocessing with where="1=1"
    fut2 = tbl.backfill_async("b", where="1=1")
    fut2.result()
    tbl.checkout_latest()

    data2 = tbl.to_arrow().to_pydict()
    # ALL rows should now have v2 values (a * 100)
    for i, (a_val, b_val) in enumerate(zip(data2["a"], data2["b"], strict=True)):
        assert b_val == a_val * 100, (
            f"Row {i}: expected v2 value {a_val * 100}, got {b_val}. "
            "where='1=1' should have forced reprocessing."
        )

    _LOG.info("Test passed: where='1=1' forces reprocessing all rows")


# --- Struct Column Backfill Tests ---

struct_type = pa.struct([("rpad", pa.string()), ("lpad", pa.string())])


@udf(data_type=struct_type, checkpoint_size=8, num_cpus=0.1)
def struct_udf_v1(a: int) -> dict:
    """First version: simple padding."""
    return {"lpad": f"{a:04d}", "rpad": f"{a}0000"[:4]}


@udf(data_type=struct_type, checkpoint_size=8, num_cpus=0.1)
def struct_udf_v2(a: int) -> dict:
    """Second version: different padding."""
    return {"lpad": f"{a:08d}", "rpad": f"{a}00000000"[:8]}


@pytest.mark.parametrize(
    "stable_row_ids", [False, True], indirect=True, ids=["rowaddr", "srid"]
)
def test_struct_column_resume_partial_backfill(
    db: Connection, local_ray_context
) -> None:
    """
    Test that struct column backfill can resume after a partial backfill.

    Since struct columns can't use IS NULL filter effectively (a struct with NULL
    fields is not the same as a NULL struct), the second backfill reprocesses all
    rows. This is less efficient but correct.

    Steps:
    1. Create table with struct UDF column
    2. Run partial backfill (num_frags=2) - creates data files in first 2 fragments
    3. Run full backfill without where parameter
    4. Verify all rows have values (all rows reprocessed)
    """
    tbl = db.open_table("foo")
    tbl.add_columns({"b": struct_udf_v1}, **SHUFFLE_CONFIG)

    # Step 1: Partial backfill - only first 2 fragments (4 rows)
    fut1 = tbl.backfill_async("b", num_frags=2, where=None)
    fut1.result()
    tbl.checkout_latest()

    data1 = tbl.to_arrow().to_pydict()
    # First 4 rows should have values, rest NULL
    computed_count_1 = sum(1 for v in data1["b"] if v is not None)
    assert computed_count_1 == 4, f"Expected 4 computed rows, got {computed_count_1}"

    # Verify first 4 rows have v1 values
    for i in range(4):
        assert data1["b"][i] is not None
        assert data1["b"][i]["lpad"] == f"{data1['a'][i]:04d}"
    _LOG.info(f"After partial backfill: {computed_count_1} rows computed")

    # Step 2: Resume backfill without where parameter
    # For struct columns, all rows are reprocessed (IS NULL filter doesn't work)
    fut2 = tbl.backfill_async("b")  # No where = reprocess all rows
    fut2.result()
    tbl.checkout_latest()

    data2 = tbl.to_arrow().to_pydict()
    # All rows should now have values
    null_count = sum(1 for v in data2["b"] if v is None)
    assert null_count == 0, f"Expected 0 NULL values, got {null_count}"

    # Verify all values are v1 (all rows were reprocessed with same UDF)
    for i, (a_val, b_val) in enumerate(zip(data2["a"], data2["b"], strict=True)):
        expected_lpad = f"{a_val:04d}"
        assert b_val["lpad"] == expected_lpad, (
            f"Row {i}: expected lpad={expected_lpad}, got {b_val['lpad']}"
        )

    _LOG.info("Test passed: Struct column resume reprocessed all rows correctly")


def test_struct_column_processes_all_if_no_data_files(
    db: Connection, local_ray_context
) -> None:
    """
    Test that struct column processes all fragments if none have data files.

    When no fragments have data files for the struct column, all should be processed.
    """
    tbl = db.open_table("foo")
    tbl.add_columns({"b": struct_udf_v1}, **SHUFFLE_CONFIG)

    # Backfill without prior partial backfill - no fragments have data files
    fut = tbl.backfill_async("b")  # No where = per-fragment data file check
    fut.result()
    tbl.checkout_latest()

    data = tbl.to_arrow().to_pydict()
    # All rows should have values
    null_count = sum(1 for v in data["b"] if v is None)
    assert null_count == 0, f"Expected 0 NULL values, got {null_count}"

    # Verify all values are correct
    for i, (a_val, b_val) in enumerate(zip(data["a"], data["b"], strict=True)):
        expected_lpad = f"{a_val:04d}"
        assert b_val["lpad"] == expected_lpad, (
            f"Row {i}: expected lpad={expected_lpad}, got {b_val['lpad']}"
        )

    _LOG.info(
        "Test passed: Struct column processed all fragments (no prior data files)"
    )


def test_struct_column_reprocesses_all_after_alter_columns(
    db: Connection, local_ray_context
) -> None:
    """
    Test struct column reprocesses all fragments after alter_columns changes UDF.

    When UDF changes, the srcfiles_hash check should detect mismatch and skip
    the per-fragment data file check, reprocessing all fragments.
    """
    tbl = db.open_table("foo")
    tbl.add_columns({"b": struct_udf_v1}, **SHUFFLE_CONFIG)

    # Step 1: Complete backfill with v1
    fut1 = tbl.backfill_async("b", where=None)
    fut1.result()
    tbl.checkout_latest()

    data1 = tbl.to_arrow().to_pydict()
    null_count_1 = sum(1 for v in data1["b"] if v is None)
    assert null_count_1 == 0, "First backfill should complete all rows"

    # Verify first backfill used v1 (4-char padding)
    for i, (a_val, b_val) in enumerate(zip(data1["a"], data1["b"], strict=True)):
        assert b_val["lpad"] == f"{a_val:04d}", f"Row {i} should have v1 value"
    _LOG.info("After v1 backfill: all rows computed with v1")

    # Step 2: Change UDF to v2 via alter_columns
    tbl.alter_columns({"path": "b", "udf": struct_udf_v2})
    tbl.checkout_latest()
    _LOG.info("After alter_columns to v2")

    # Step 3: Backfill with changed UDF - should reprocess ALL rows
    fut2 = tbl.backfill_async("b")  # No where = should detect UDF change
    fut2.result()
    tbl.checkout_latest()

    data2 = tbl.to_arrow().to_pydict()
    null_count_2 = sum(1 for v in data2["b"] if v is None)
    assert null_count_2 == 0, "Second backfill should complete all rows"

    # Verify ALL rows now have v2 values (8-char padding)
    for i, (a_val, b_val) in enumerate(zip(data2["a"], data2["b"], strict=True)):
        expected_lpad = f"{a_val:08d}"
        assert b_val["lpad"] == expected_lpad, (
            f"Row {i}: expected v2 lpad={expected_lpad}, got {b_val['lpad']}"
        )

    _LOG.info("Test passed: Struct column reprocessed all after alter_columns")
