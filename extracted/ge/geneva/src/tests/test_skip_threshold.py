# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for skip threshold feature (GEN-368)

Tests cover:
- SkipBudgetTracker: count threshold, fraction threshold, both, edge cases
- ErrorHandlingConfig validation with skip thresholds
- skip_on_error() factory with threshold params
- Integration tests with SimpleApplier via Ray backfill
"""

import logging

import lance
import pyarrow as pa
import pytest

import geneva
from geneva import Skip, SkipThresholdExceededError, skip_on_error, udf
from geneva.apply.error_handling import SkipBudgetTracker, make_skip_budget_tracker
from geneva.db import Connection
from geneva.debug.error_store import (
    ErrorHandlingConfig,
    FaultIsolation,
    resolve_on_error,
)

_LOG = logging.getLogger(__name__)
_LOG.setLevel(logging.DEBUG)

SIZE = 20


# =============================================================================
# Unit tests for SkipBudgetTracker
# =============================================================================


class TestSkipBudgetTracker:
    """Tests for the SkipBudgetTracker class"""

    def test_count_threshold_not_exceeded(self) -> None:
        """No exception when skip count is within budget"""
        tracker = SkipBudgetTracker(max_skip_count=5, max_skip_fraction=None)
        tracker.record_batch(10, 2)
        tracker.record_batch(10, 3)
        assert tracker.skipped == 5
        assert tracker.processed == 20

    def test_count_threshold_exceeded(self) -> None:
        """Raises SkipThresholdExceededError when count threshold crossed"""
        tracker = SkipBudgetTracker(max_skip_count=3, max_skip_fraction=None)
        tracker.record_batch(10, 2)  # 2 skipped, ok
        with pytest.raises(SkipThresholdExceededError, match="max_skip_count=3"):
            tracker.record_batch(10, 2)  # 4 skipped total, > 3

    def test_count_threshold_exactly_at_limit(self) -> None:
        """No exception when skip count equals the threshold exactly"""
        tracker = SkipBudgetTracker(max_skip_count=5, max_skip_fraction=None)
        tracker.record_batch(10, 5)  # exactly at limit, not exceeded
        assert tracker.skipped == 5

    def test_fraction_threshold_not_exceeded(self) -> None:
        """No exception when fraction is within budget"""
        tracker = SkipBudgetTracker(max_skip_count=None, max_skip_fraction=0.3)
        tracker.record_batch(10, 2)  # 20% < 30%
        assert tracker.skipped == 2

    def test_fraction_threshold_exceeded(self) -> None:
        """Raises SkipThresholdExceededError when fraction threshold crossed"""
        tracker = SkipBudgetTracker(max_skip_count=None, max_skip_fraction=0.1)
        with pytest.raises(SkipThresholdExceededError, match="max_skip_fraction=0.1"):
            tracker.record_batch(10, 2)  # 20% > 10%

    def test_both_thresholds_count_triggers_first(self) -> None:
        """When both thresholds set, count triggers first"""
        tracker = SkipBudgetTracker(max_skip_count=2, max_skip_fraction=0.5)
        with pytest.raises(SkipThresholdExceededError, match="max_skip_count=2"):
            tracker.record_batch(10, 3)  # 3 > 2 (count), 30% < 50% (fraction)

    def test_both_thresholds_fraction_triggers_first(self) -> None:
        """When both thresholds set, fraction triggers first"""
        tracker = SkipBudgetTracker(max_skip_count=100, max_skip_fraction=0.1)
        with pytest.raises(SkipThresholdExceededError, match="max_skip_fraction=0.1"):
            tracker.record_batch(10, 2)  # 2 < 100 (count), 20% > 10% (fraction)

    def test_no_thresholds(self) -> None:
        """No exception when no thresholds configured"""
        tracker = SkipBudgetTracker(max_skip_count=None, max_skip_fraction=None)
        tracker.record_batch(10, 10)  # 100% skipped, still ok
        assert tracker.skipped == 10

    def test_accumulates_across_batches(self) -> None:
        """Skips accumulate across multiple batches"""
        tracker = SkipBudgetTracker(max_skip_count=5, max_skip_fraction=None)
        tracker.record_batch(10, 1)  # 1 total
        tracker.record_batch(10, 2)  # 3 total
        tracker.record_batch(10, 2)  # 5 total, still at limit
        with pytest.raises(SkipThresholdExceededError):
            tracker.record_batch(10, 1)  # 6 total, exceeds 5

    def test_zero_count_threshold(self) -> None:
        """max_skip_count=0 means any skip triggers failure"""
        tracker = SkipBudgetTracker(max_skip_count=0, max_skip_fraction=None)
        with pytest.raises(SkipThresholdExceededError):
            tracker.record_batch(10, 1)

    def test_zero_skip_count_no_error(self) -> None:
        """No error when no rows are skipped"""
        tracker = SkipBudgetTracker(max_skip_count=0, max_skip_fraction=None)
        tracker.record_batch(10, 0)
        assert tracker.skipped == 0

    def test_zero_batch_size_no_error(self) -> None:
        """record_batch(0, 0) is a no-op — no division-by-zero or false trigger"""
        tracker = SkipBudgetTracker(max_skip_count=1, max_skip_fraction=0.1)
        tracker.record_batch(0, 0)
        assert tracker.processed == 0
        assert tracker.skipped == 0

    def test_zero_fraction_threshold(self) -> None:
        """max_skip_fraction=0.0 means any skip triggers failure"""
        tracker = SkipBudgetTracker(max_skip_count=None, max_skip_fraction=0.0)
        with pytest.raises(SkipThresholdExceededError):
            tracker.record_batch(10, 1)

    def test_zero_fraction_threshold_no_skips(self) -> None:
        """max_skip_fraction=0.0 allows batches with zero skips"""
        tracker = SkipBudgetTracker(max_skip_count=None, max_skip_fraction=0.0)
        tracker.record_batch(10, 0)
        assert tracker.skipped == 0

    def test_exception_message_includes_diagnostics(self) -> None:
        """Exception message includes useful diagnostic info"""
        tracker = SkipBudgetTracker(max_skip_count=2, max_skip_fraction=0.1)
        with pytest.raises(SkipThresholdExceededError) as exc_info:
            tracker.record_batch(10, 5)

        exc = exc_info.value
        assert exc.skipped == 5
        assert exc.processed == 10
        assert exc.max_count == 2
        assert exc.max_fraction == 0.1
        assert "5 rows skipped" in str(exc)
        assert "10 processed" in str(exc)


class TestMakeSkipBudgetTracker:
    """Tests for the make_skip_budget_tracker helper"""

    def test_returns_none_when_no_config(self) -> None:
        assert make_skip_budget_tracker(None) is None

    def test_returns_none_when_fail_batch(self) -> None:
        config = ErrorHandlingConfig(fault_isolation=FaultIsolation.FAIL_BATCH)
        assert make_skip_budget_tracker(config) is None

    def test_returns_none_when_no_thresholds(self) -> None:
        config = ErrorHandlingConfig(fault_isolation=FaultIsolation.SKIP_ROWS)
        assert make_skip_budget_tracker(config) is None

    def test_returns_tracker_with_count(self) -> None:
        config = ErrorHandlingConfig(
            fault_isolation=FaultIsolation.SKIP_ROWS, max_skip_count=10
        )
        tracker = make_skip_budget_tracker(config)
        assert tracker is not None
        assert tracker.max_skip_count == 10
        assert tracker.max_skip_fraction is None

    def test_returns_tracker_with_fraction(self) -> None:
        config = ErrorHandlingConfig(
            fault_isolation=FaultIsolation.SKIP_ROWS, max_skip_fraction=0.05
        )
        tracker = make_skip_budget_tracker(config)
        assert tracker is not None
        assert tracker.max_skip_fraction == 0.05

    def test_returns_tracker_with_both(self) -> None:
        config = ErrorHandlingConfig(
            fault_isolation=FaultIsolation.SKIP_ROWS,
            max_skip_count=100,
            max_skip_fraction=0.05,
        )
        tracker = make_skip_budget_tracker(config)
        assert tracker is not None
        assert tracker.max_skip_count == 100
        assert tracker.max_skip_fraction == 0.05


# =============================================================================
# Unit tests for ErrorHandlingConfig validation
# =============================================================================


class TestErrorHandlingConfigValidation:
    """Tests for skip threshold validation on ErrorHandlingConfig"""

    def test_valid_config_skip_rows_with_count(self) -> None:
        """Valid: SKIP_ROWS with max_skip_count"""
        config = ErrorHandlingConfig(
            fault_isolation=FaultIsolation.SKIP_ROWS, max_skip_count=10
        )
        assert config.max_skip_count == 10

    def test_valid_config_skip_rows_with_fraction(self) -> None:
        """Valid: SKIP_ROWS with max_skip_fraction"""
        config = ErrorHandlingConfig(
            fault_isolation=FaultIsolation.SKIP_ROWS, max_skip_fraction=0.05
        )
        assert config.max_skip_fraction == 0.05

    def test_valid_config_skip_rows_with_both(self) -> None:
        """Valid: SKIP_ROWS with both thresholds"""
        config = ErrorHandlingConfig(
            fault_isolation=FaultIsolation.SKIP_ROWS,
            max_skip_count=100,
            max_skip_fraction=0.1,
        )
        assert config.max_skip_count == 100
        assert config.max_skip_fraction == 0.1

    def test_invalid_negative_count(self) -> None:
        """Invalid: negative max_skip_count"""
        with pytest.raises(ValueError, match="max_skip_count must be >= 0"):
            ErrorHandlingConfig(
                fault_isolation=FaultIsolation.SKIP_ROWS, max_skip_count=-1
            )

    def test_invalid_fraction_too_high(self) -> None:
        """Invalid: max_skip_fraction > 1.0"""
        with pytest.raises(ValueError, match="max_skip_fraction must be between"):
            ErrorHandlingConfig(
                fault_isolation=FaultIsolation.SKIP_ROWS, max_skip_fraction=1.5
            )

    def test_invalid_fraction_negative(self) -> None:
        """Invalid: negative max_skip_fraction"""
        with pytest.raises(ValueError, match="max_skip_fraction must be between"):
            ErrorHandlingConfig(
                fault_isolation=FaultIsolation.SKIP_ROWS, max_skip_fraction=-0.1
            )

    def test_invalid_count_with_fail_batch(self) -> None:
        """Invalid: max_skip_count with FAIL_BATCH"""
        with pytest.raises(ValueError, match="can only be used with.*SKIP_ROWS"):
            ErrorHandlingConfig(
                fault_isolation=FaultIsolation.FAIL_BATCH, max_skip_count=10
            )

    def test_invalid_fraction_with_fail_batch(self) -> None:
        """Invalid: max_skip_fraction with FAIL_BATCH"""
        with pytest.raises(ValueError, match="can only be used with.*SKIP_ROWS"):
            ErrorHandlingConfig(
                fault_isolation=FaultIsolation.FAIL_BATCH, max_skip_fraction=0.1
            )

    def test_none_thresholds_ok_with_any_mode(self) -> None:
        """None thresholds are fine with any fault isolation mode"""
        config = ErrorHandlingConfig(
            fault_isolation=FaultIsolation.FAIL_BATCH,
            max_skip_count=None,
            max_skip_fraction=None,
        )
        assert config.max_skip_count is None
        assert config.max_skip_fraction is None


# =============================================================================
# Unit tests for skip_on_error() factory and resolve_on_error
# =============================================================================


class TestSkipOnErrorFactory:
    """Tests for skip_on_error() with threshold params"""

    def test_skip_on_error_no_thresholds(self) -> None:
        """skip_on_error() without thresholds produces SKIP_ROWS with no limits"""
        config = resolve_on_error(skip_on_error())
        assert config.fault_isolation == FaultIsolation.SKIP_ROWS
        assert config.max_skip_count is None
        assert config.max_skip_fraction is None

    def test_skip_on_error_with_count(self) -> None:
        """skip_on_error(max_skip_count=N) flows through to config"""
        config = resolve_on_error(skip_on_error(max_skip_count=100))
        assert config.fault_isolation == FaultIsolation.SKIP_ROWS
        assert config.max_skip_count == 100
        assert config.max_skip_fraction is None

    def test_skip_on_error_with_fraction(self) -> None:
        """skip_on_error(max_skip_fraction=F) flows through to config"""
        config = resolve_on_error(skip_on_error(max_skip_fraction=0.05))
        assert config.fault_isolation == FaultIsolation.SKIP_ROWS
        assert config.max_skip_count is None
        assert config.max_skip_fraction == 0.05

    def test_skip_on_error_with_both(self) -> None:
        """skip_on_error() with both thresholds flows through correctly"""
        config = resolve_on_error(
            skip_on_error(max_skip_count=100, max_skip_fraction=0.05)
        )
        assert config.fault_isolation == FaultIsolation.SKIP_ROWS
        assert config.max_skip_count == 100
        assert config.max_skip_fraction == 0.05

    def test_skip_matcher_carries_thresholds(self) -> None:
        """Skip matcher object stores threshold values"""
        matchers = skip_on_error(max_skip_count=50, max_skip_fraction=0.1)
        assert len(matchers) == 1
        skip = matchers[0]
        assert isinstance(skip, Skip)
        assert skip.max_skip_count == 50
        assert skip.max_skip_fraction == 0.1

    def test_udf_with_skip_thresholds(self) -> None:
        """@udf decorator correctly propagates skip thresholds"""

        @udf(
            data_type=pa.int32(),
            on_error=skip_on_error(max_skip_count=10, max_skip_fraction=0.2),
        )
        def my_udf(x: int) -> int:
            return x

        assert my_udf.error_handling is not None
        assert my_udf.error_handling.fault_isolation == FaultIsolation.SKIP_ROWS
        assert my_udf.error_handling.max_skip_count == 10
        assert my_udf.error_handling.max_skip_fraction == 0.2


# =============================================================================
# Integration tests (require Ray)
# =============================================================================


@pytest.fixture
def db(tmp_path) -> Connection:
    """Create a test database with a simple table"""
    tbl_path = tmp_path / "test.lance"

    # Create initial dataset with column 'a'
    data = {"a": pa.array(range(SIZE))}
    tbl = pa.Table.from_pydict(data)
    lance.write_dataset(tbl, tbl_path, max_rows_per_file=10)

    db = geneva.connect(str(tmp_path))
    yield db
    db.close()


def test_applier_tracks_skip_counts() -> None:
    """SimpleApplier accumulates skip_count and total_rows as attributes."""
    from geneva.apply.simple import SimpleApplier
    from geneva.apply.task import BackfillUDFTask
    from geneva.debug.logger import NoOpErrorLogger

    @udf(data_type=pa.int32(), on_error=skip_on_error(max_skip_count=100))
    def sometimes_fails(a: int) -> int:
        if a % 5 == 0:
            raise ValueError(f"Bad row {a}")
        return a * 2

    task = BackfillUDFTask(
        udfs={"b": sometimes_fails},
        where="b IS NULL",
        override_batch_size=5,
    )

    class MockReadTask:
        def to_batches(self, *, batch_size=100):  # noqa: ANN202
            for start in range(0, 20, 5):
                batch = pa.record_batch(
                    {
                        "a": pa.array(range(start, start + 5)),
                        "_rowaddr": pa.array(range(start, start + 5), type=pa.uint64()),
                    }
                )
                yield batch

        def table_uri(self) -> str:
            return "test://mock"

    applier = SimpleApplier(job_id="test")
    list(applier.run(MockReadTask(), task, error_logger=NoOpErrorLogger()))

    # 4 batches of 5 rows, 1 failure per batch (rows 0, 5, 10, 15)
    assert applier.total_rows == 20
    assert applier.skip_count == 4


def test_simple_applier_enforces_skip_threshold() -> None:
    """SimpleApplier raises SkipThresholdExceededError when threshold is exceeded."""
    from geneva.apply.simple import SimpleApplier
    from geneva.apply.task import BackfillUDFTask
    from geneva.debug.logger import NoOpErrorLogger

    @udf(data_type=pa.int32(), on_error=skip_on_error(max_skip_count=2))
    def mostly_fails(a: int) -> int:
        if a % 5 == 0:
            raise ValueError(f"Bad row {a}")
        return a * 2

    task = BackfillUDFTask(
        udfs={"b": mostly_fails},
        where="b IS NULL",
        override_batch_size=5,
    )

    class MockReadTask:
        def to_batches(self, *, batch_size=100):  # noqa: ANN202
            for start in range(0, 20, 5):
                batch = pa.record_batch(
                    {
                        "a": pa.array(range(start, start + 5)),
                        "_rowaddr": pa.array(range(start, start + 5), type=pa.uint64()),
                    }
                )
                yield batch

        def table_uri(self) -> str:
            return "test://mock"

    applier = SimpleApplier(job_id="test")
    with pytest.raises(SkipThresholdExceededError):
        list(applier.run(MockReadTask(), task, error_logger=NoOpErrorLogger()))


@pytest.mark.ray
def test_skip_threshold_count_exceeded_ray(db: Connection, local_ray_context) -> None:
    """Job fails when skip count exceeds max_skip_count (per-job via pipeline)."""

    @udf(data_type=pa.int32(), on_error=skip_on_error(max_skip_count=2))
    def failing_udf(a: int) -> int:
        if a % 3 == 0:  # ~33% failure rate → ~7 failures across 20 rows
            raise ValueError(f"Bad row {a}")
        return a * 2

    tbl = db.open_table("test")
    tbl.add_columns({"b": failing_udf})

    # Pipeline-level tracker accumulates across all tasks/fragments
    with pytest.raises(SkipThresholdExceededError) as exc_info:
        tbl.backfill("b")

    exc = exc_info.value
    assert exc.skipped > exc.max_count, "skipped should exceed max_count"
    assert exc.processed > 0, "processed should be positive"


@pytest.mark.ray
def test_skip_threshold_fraction_exceeded_ray(
    db: Connection, local_ray_context
) -> None:
    """Job fails when skip fraction exceeds max_skip_fraction (per-job)."""

    @udf(data_type=pa.int32(), on_error=skip_on_error(max_skip_fraction=0.1))
    def failing_udf(a: int) -> int:
        if a % 3 == 0:  # ~33% failure rate > 10%
            raise ValueError(f"Bad row {a}")
        return a * 2

    tbl = db.open_table("test")
    tbl.add_columns({"b": failing_udf})

    with pytest.raises(SkipThresholdExceededError) as exc_info:
        tbl.backfill("b")

    exc = exc_info.value
    assert exc.processed > 0, "processed should be positive"
    assert exc.skipped / exc.processed > exc.max_fraction, (
        "actual fraction should exceed max_fraction"
    )


@pytest.mark.ray
def test_skip_threshold_under_limit_succeeds(db: Connection, local_ray_context) -> None:
    """Job succeeds when failures are within threshold.

    Uses count-only threshold to avoid fraction issues when Ray splits
    data into small per-task batches (a single failing row in a 1-row
    task would have 100% failure rate).
    """

    @udf(
        data_type=pa.int32(),
        on_error=skip_on_error(max_skip_count=20),
    )
    def mostly_ok_udf(a: int) -> int:
        if a == 5:  # Only 1 row fails out of 20
            raise ValueError(f"Bad row {a}")
        return a * 2

    tbl = db.open_table("test")
    tbl.add_columns({"b": mostly_ok_udf})

    job_id = tbl.backfill("b")
    assert job_id is not None  # backfill completed without SkipThresholdExceededError

    # Verify results — successful completion means job reached DONE status
    result_tbl = db.open_table("test")
    result_data = result_tbl.to_arrow()
    b_values = result_data["b"].to_pylist()

    for i, val in enumerate(b_values):
        if i == 5:
            assert val is None, f"Row {i} should be null (skipped)"
        else:
            assert val == i * 2, f"Row {i} should be {i * 2}"


@pytest.mark.ray
def test_skip_threshold_no_limit_skips_all(db: Connection, local_ray_context) -> None:
    """Job succeeds with unlimited skipping (no threshold)"""

    @udf(data_type=pa.int32(), on_error=skip_on_error())
    def half_failing_udf(a: int) -> int:
        if a % 2 == 0:  # 50% failure rate, but no threshold set
            raise ValueError(f"Bad row {a}")
        return a * 2

    tbl = db.open_table("test")
    tbl.add_columns({"b": half_failing_udf})

    job_id = tbl.backfill("b")
    assert job_id is not None  # backfill completed without error

    result_tbl = db.open_table("test")
    result_data = result_tbl.to_arrow()
    b_values = result_data["b"].to_pylist()

    for i, val in enumerate(b_values):
        if i % 2 == 0:
            assert val is None
        else:
            assert val == i * 2
