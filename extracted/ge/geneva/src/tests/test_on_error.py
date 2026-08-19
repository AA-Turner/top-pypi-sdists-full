# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for the simplified on_error UDF API"""

import logging
import signal
import uuid
from collections import Counter, deque
from pathlib import Path
from typing import NoReturn

import lance
import pyarrow as pa
import pytest
import ray.exceptions

import geneva
from geneva import (
    Fail,
    FatalWorkerCrashError,
    FatalWorkerExitError,
    FatalWorkerOOMError,
    FatalWorkerTransientError,
    Retry,
    Skip,
    fail_fast,
    retry_all,
    retry_transient,
    skip_on_error,
    udf,
)
from geneva.apply.error_handling import get_max_attempts
from geneva.apply.task import BackfillUDFTask, ScanTask
from geneva.checkpoint import CheckpointStore
from geneva.db import Connection
from geneva.debug.error_store import (
    ErrorHandlingConfig,
    ExceptionMatcher,
    FaultIsolation,
    Outcome,
    get_exception_outcome,
    resolve_on_error,
)
from geneva.errors import (
    CheckpointCoverageError,
    CorruptCheckpointError,
    FatalWorkerError,
    MergeFallbackTargetError,
    ShortFragmentWriteError,
)
from geneva.jobs.config import JobConfig
from geneva.runners.ray.actor_pool import ActorLostError, ActorStateSnapshot
from geneva.runners.ray.pipeline import (
    ColumnAddPipelineJob,
    ScheduledReadTask,
    _config_handles_exception,
    _default_worker_loss_policy,
    _normalize_fatal_worker_error,
)
from geneva.table import TableReference

_LOG = logging.getLogger(__name__)
_LOG.setLevel(logging.DEBUG)

SIZE = 20
HAS_SIGALRM_TIMEOUT = all(
    hasattr(signal, attr)
    for attr in ("SIGALRM", "ITIMER_REAL", "setitimer", "getitimer")
)

pytestmark = pytest.mark.ray


# =============================================================================
# Unit tests for ExceptionMatcher classes
# =============================================================================


class TestExceptionMatcher:
    """Tests for the ExceptionMatcher base class and matching logic"""

    def test_matches_exception_type(self) -> None:
        """Test matching by exception type"""
        matcher = ExceptionMatcher(exceptions=(ValueError,))
        assert matcher.matches(ValueError("test"))
        assert not matcher.matches(TypeError("test"))

    def test_matches_multiple_exception_types(self) -> None:
        """Test matching multiple exception types"""
        matcher = ExceptionMatcher(exceptions=(ValueError, TypeError))
        assert matcher.matches(ValueError("test"))
        assert matcher.matches(TypeError("test"))
        assert not matcher.matches(KeyError("test"))

    def test_matches_exception_subclass(self) -> None:
        """Test that exception inheritance is respected"""
        matcher = ExceptionMatcher(exceptions=(OSError,))
        assert matcher.matches(OSError("test"))
        assert matcher.matches(ConnectionError("test"))  # subclass of OSError
        assert not matcher.matches(ValueError("test"))

    def test_match_substring(self) -> None:
        """Test substring matching (plain string as regex)"""
        matcher = ExceptionMatcher(exceptions=(ValueError,), match="rate limit")
        assert matcher.matches(ValueError("rate limit exceeded"))
        assert matcher.matches(ValueError("hit rate limit"))
        assert not matcher.matches(ValueError("Rate Limit"))  # case-sensitive
        assert not matcher.matches(ValueError("invalid input"))

    def test_match_case_insensitive(self) -> None:
        """Test case-insensitive matching with (?i) flag"""
        matcher = ExceptionMatcher(exceptions=(ValueError,), match=r"(?i)rate limit")
        assert matcher.matches(ValueError("Rate limit exceeded"))
        assert matcher.matches(ValueError("RATE LIMIT hit"))
        assert not matcher.matches(ValueError("invalid input"))

    def test_match_regex(self) -> None:
        """Test regex pattern matching"""
        matcher = ExceptionMatcher(exceptions=(ValueError,), match=r"rate.?limit")
        assert matcher.matches(ValueError("rate limit"))
        assert matcher.matches(ValueError("ratelimit"))
        assert matcher.matches(ValueError("rate_limit"))
        assert not matcher.matches(ValueError("RATE_LIMIT"))  # case-sensitive
        assert not matcher.matches(ValueError("invalid"))

    def test_match_regex_alternation(self) -> None:
        """Test regex with alternation"""
        matcher = ExceptionMatcher(exceptions=(ValueError,), match=r"429|rate.?limit")
        assert matcher.matches(ValueError("Error 429"))
        assert matcher.matches(ValueError("rate limit exceeded"))
        assert not matcher.matches(ValueError("invalid input"))

    def test_invalid_regex_raises_error(self) -> None:
        """Test that invalid regex pattern raises ValueError at construction time"""
        with pytest.raises(ValueError, match="Invalid regex pattern"):
            ExceptionMatcher(exceptions=(ValueError,), match=r"[invalid")

    def test_invalid_regex_in_retry_raises_error(self) -> None:
        """Test that invalid regex in Retry raises ValueError"""
        with pytest.raises(ValueError, match="Invalid regex pattern"):
            Retry(ValueError, match=r"(unclosed group")


class TestRetryClass:
    """Tests for the Retry matcher class"""

    def test_retry_single_exception(self) -> None:
        """Test Retry with a single exception type"""
        retry = Retry(ConnectionError)
        assert retry.exceptions == (ConnectionError,)
        assert retry.max_attempts == 3
        assert retry.backoff == "exponential"

    def test_retry_multiple_exceptions(self) -> None:
        """Test Retry with multiple exception types"""
        retry = Retry(ConnectionError, TimeoutError, max_attempts=5)
        assert retry.exceptions == (ConnectionError, TimeoutError)
        assert retry.max_attempts == 5

    def test_retry_with_match(self) -> None:
        """Test Retry with match pattern"""
        retry = Retry(ValueError, match="rate limit", max_attempts=10)
        assert retry.matches(ValueError("rate limit exceeded"))
        assert not retry.matches(ValueError("invalid input"))
        assert retry.max_attempts == 10

    def test_retry_custom_backoff(self) -> None:
        """Test Retry with custom backoff strategy"""
        retry = Retry(ValueError, backoff="fixed")
        assert retry.backoff == "fixed"

    def test_retry_invalid_backoff_raises_error(self) -> None:
        """Test that invalid backoff strategy raises ValueError"""
        with pytest.raises(ValueError, match="Invalid backoff strategy"):
            Retry(ValueError, backoff="invalid_strategy")

    def test_retry_all_valid_backoff_strategies(self) -> None:
        """Test all valid backoff strategies"""
        for strategy in ["exponential", "fixed", "linear"]:
            retry = Retry(ValueError, backoff=strategy)
            assert retry.backoff == strategy


class TestSkipClass:
    """Tests for the Skip matcher class"""

    def test_skip_single_exception(self) -> None:
        """Test Skip with a single exception type"""
        skip = Skip(ValueError)
        assert skip.exceptions == (ValueError,)
        assert skip.matches(ValueError("test"))

    def test_skip_multiple_exceptions(self) -> None:
        """Test Skip with multiple exception types"""
        skip = Skip(ValueError, KeyError)
        assert skip.exceptions == (ValueError, KeyError)
        assert skip.matches(ValueError("test"))
        assert skip.matches(KeyError("test"))

    def test_skip_with_match(self) -> None:
        """Test Skip with match pattern"""
        skip = Skip(ValueError, match="invalid input")
        assert skip.matches(ValueError("invalid input provided"))
        assert not skip.matches(ValueError("rate limit exceeded"))


class TestFailClass:
    """Tests for the Fail matcher class"""

    def test_fail_single_exception(self) -> None:
        """Test Fail with a single exception type"""
        fail = Fail(RuntimeError)
        assert fail.exceptions == (RuntimeError,)
        assert fail.matches(RuntimeError("fatal error"))

    def test_fail_with_match(self) -> None:
        """Test Fail with match pattern"""
        fail = Fail(ValueError, match="fatal")
        assert fail.matches(ValueError("fatal error occurred"))
        assert not fail.matches(ValueError("minor issue"))


# =============================================================================
# Unit tests for resolve_on_error and presets
# =============================================================================


class TestFactoryFunctions:
    """Tests for factory function configurations"""

    def test_retry_transient_default(self) -> None:
        """Test retry_transient() with defaults"""
        config = resolve_on_error(retry_transient())
        assert config.fault_isolation == FaultIsolation.FAIL_BATCH
        assert config._matchers is not None
        assert len(config._matchers) == 1
        assert isinstance(config._matchers[0], Retry)
        assert config._matchers[0].max_attempts == 3

    def test_retry_transient_custom_attempts(self) -> None:
        """Test retry_transient() with custom max_attempts"""
        config = resolve_on_error(retry_transient(max_attempts=5))
        assert config._matchers is not None
        assert config._matchers[0].max_attempts == 5
        assert config.retry_config.stop.max_attempt_number == 5

    def test_retry_all_default(self) -> None:
        """Test retry_all() with defaults"""
        config = resolve_on_error(retry_all())
        assert config._matchers is not None
        assert len(config._matchers) == 1
        retry = config._matchers[0]
        assert isinstance(retry, Retry)
        assert Exception in retry.exceptions

    def test_retry_all_custom_attempts(self) -> None:
        """Test retry_all() with custom max_attempts"""
        config = resolve_on_error(retry_all(max_attempts=10))
        assert config._matchers is not None
        assert config._matchers[0].max_attempts == 10

    def test_skip_on_error_factory(self) -> None:
        """Test skip_on_error() factory"""
        config = resolve_on_error(skip_on_error())
        assert config.fault_isolation == FaultIsolation.SKIP_ROWS
        assert config._matchers is not None
        assert isinstance(config._matchers[0], Skip)

    def test_fail_fast_factory(self) -> None:
        """Test fail_fast() factory"""
        config = resolve_on_error(fail_fast())
        # Empty list results in default config with no matchers
        assert config._matchers is None
        assert config.fault_isolation == FaultIsolation.FAIL_BATCH

    def test_none_returns_default_config(self) -> None:
        """Test that None returns default error handling"""
        config = resolve_on_error(None)
        assert config.fault_isolation == FaultIsolation.FAIL_BATCH
        assert config._matchers is None

    def test_custom_backoff(self) -> None:
        """Test factory with custom backoff strategy"""
        config = resolve_on_error(retry_transient(backoff="fixed"))
        assert config._matchers is not None
        assert config._matchers[0].backoff == "fixed"


class TestResolveOnError:
    """Tests for resolve_on_error function"""

    def test_resolve_with_matchers(self) -> None:
        """Test resolve_on_error with matcher list"""
        matchers = [
            Retry(ConnectionError, TimeoutError, max_attempts=3),
            Skip(ValueError),
        ]
        config = resolve_on_error(matchers)
        assert config._matchers == matchers
        assert config.fault_isolation == FaultIsolation.SKIP_ROWS  # Has Skip

    def test_resolve_retry_only(self) -> None:
        """Test resolve_on_error with only Retry matchers"""
        matchers = [Retry(ConnectionError, max_attempts=5)]
        config = resolve_on_error(matchers)
        assert config.fault_isolation == FaultIsolation.FAIL_BATCH  # No Skip
        # With per-exception stop, check the max_attempts dict
        assert config.retry_config.stop._max_attempts[ConnectionError] == 5

    def test_resolve_skip_only(self) -> None:
        """Test resolve_on_error with only Skip matchers"""
        matchers = [Skip(ValueError)]
        config = resolve_on_error(matchers)
        assert config.fault_isolation == FaultIsolation.SKIP_ROWS

    def test_different_backoff_strategies_allowed(self) -> None:
        """Test that multiple Retry matchers with different backoffs are allowed"""
        matchers = [
            Retry(ConnectionError, backoff="exponential"),
            Retry(TimeoutError, backoff="fixed"),
        ]
        config = resolve_on_error(matchers)
        assert config._matchers is not None
        assert len(config._matchers) == 2
        # Verify per-exception retry config is created
        assert config.retry_config is not None

    def test_multiple_retry_same_backoff_ok(self) -> None:
        """Test that multiple Retry matchers with same backoff is allowed"""
        matchers = [
            Retry(ConnectionError, backoff="exponential"),
            Retry(TimeoutError, backoff="exponential"),
        ]
        config = resolve_on_error(matchers)
        assert config._matchers is not None
        assert len(config._matchers) == 2

    def test_per_exception_max_attempts(self) -> None:
        """Test that different max_attempts work per exception type"""
        matchers = [
            Retry(ConnectionError, max_attempts=3),
            Retry(TimeoutError, max_attempts=5),
        ]
        config = resolve_on_error(matchers)
        # Should have per-exception stop strategy
        stop = config.retry_config.stop
        # Verify the stop strategy tracks different max_attempts
        assert hasattr(stop, "_max_attempts")
        assert stop._max_attempts[ConnectionError] == 3
        assert stop._max_attempts[TimeoutError] == 5


class TestPerExceptionStrategies:
    """Tests for per-exception wait and stop strategies"""

    def test_per_exception_wait_uses_correct_strategy(self) -> None:
        """Test that _PerExceptionWait uses the correct backoff per exception"""

        from geneva.debug.error_store import _PerExceptionWait

        matchers = [
            Retry(ConnectionError, backoff="exponential"),
            Retry(TimeoutError, backoff="fixed"),
        ]
        wait_strategy = _PerExceptionWait(matchers)

        # Verify different exception types have different wait strategies
        assert wait_strategy._wait_strategies[ConnectionError] is not None
        assert wait_strategy._wait_strategies[TimeoutError] is not None
        # They should be different strategy objects
        assert (
            wait_strategy._wait_strategies[ConnectionError]
            is not wait_strategy._wait_strategies[TimeoutError]
        )

    def test_per_exception_stop_stops_at_correct_attempt(self) -> None:
        """Test that _PerExceptionStop stops at the correct attempt per exception"""
        from unittest.mock import MagicMock

        from geneva.debug.error_store import _PerExceptionStop

        matchers = [
            Retry(ConnectionError, max_attempts=2),
            Retry(TimeoutError, max_attempts=5),
        ]
        stop_strategy = _PerExceptionStop(matchers)

        # Create mock retry states
        def make_retry_state(exc: Exception, attempt: int) -> MagicMock:
            state = MagicMock()
            outcome = MagicMock()
            outcome.exception.return_value = exc
            state.outcome = outcome
            state.attempt_number = attempt
            return state

        # ConnectionError should stop at attempt 2
        assert stop_strategy(make_retry_state(ConnectionError(), 1)) is False
        assert stop_strategy(make_retry_state(ConnectionError(), 2)) is True
        assert stop_strategy(make_retry_state(ConnectionError(), 3)) is True

        # TimeoutError should stop at attempt 5
        assert stop_strategy(make_retry_state(TimeoutError(), 2)) is False
        assert stop_strategy(make_retry_state(TimeoutError(), 4)) is False
        assert stop_strategy(make_retry_state(TimeoutError(), 5)) is True

    def test_per_exception_max_attempt_number_property(self) -> None:
        """Test that max_attempt_number returns the maximum across all exceptions"""
        from geneva.debug.error_store import _PerExceptionStop

        matchers = [
            Retry(ConnectionError, max_attempts=3),
            Retry(TimeoutError, max_attempts=7),
        ]
        stop_strategy = _PerExceptionStop(matchers)

        # max_attempt_number should return the overall max for compatibility
        assert stop_strategy.max_attempt_number == 7


class TestGetExceptionOutcome:
    """Tests for get_exception_outcome function"""

    def test_outcome_retry(self) -> None:
        """Test that Retry matcher returns RETRY outcome"""
        config = resolve_on_error([Retry(ConnectionError)])
        outcome = get_exception_outcome(ConnectionError("test"), config)
        assert outcome == Outcome.RETRY

    def test_outcome_skip(self) -> None:
        """Test that Skip matcher returns SKIP outcome"""
        config = resolve_on_error([Skip(ValueError)])
        outcome = get_exception_outcome(ValueError("test"), config)
        assert outcome == Outcome.SKIP

    def test_outcome_fail(self) -> None:
        """Test that Fail matcher returns FAIL outcome"""
        config = resolve_on_error([Fail(RuntimeError)])
        outcome = get_exception_outcome(RuntimeError("test"), config)
        assert outcome == Outcome.FAIL

    def test_outcome_default_fail(self) -> None:
        """Test that unmatched exceptions return FAIL"""
        config = resolve_on_error([Retry(ConnectionError)])
        outcome = get_exception_outcome(ValueError("test"), config)
        assert outcome == Outcome.FAIL

    def test_outcome_priority(self) -> None:
        """Test that first matching rule wins"""
        config = resolve_on_error(
            [
                Retry(ValueError, match="rate limit"),
                Skip(ValueError),  # Less specific, matches second
            ]
        )
        # Rate limit message should match Retry
        outcome = get_exception_outcome(ValueError("rate limit exceeded"), config)
        assert outcome == Outcome.RETRY

        # Other ValueError should match Skip
        outcome = get_exception_outcome(ValueError("invalid input"), config)
        assert outcome == Outcome.SKIP

    def test_outcome_no_matchers(self) -> None:
        """Test outcome when config has no matchers"""
        config = ErrorHandlingConfig()  # No _matchers
        outcome = get_exception_outcome(ValueError("test"), config)
        assert outcome == Outcome.FAIL


# =============================================================================
# Unit tests for @udf decorator with on_error
# =============================================================================


class TestUdfOnErrorParameter:
    """Tests for the on_error parameter on @udf decorator"""

    def test_udf_with_on_error_factory(self) -> None:
        """Test @udf with on_error factory function"""

        @udf(data_type=pa.int32(), on_error=retry_transient())
        def my_udf(x: int) -> int:
            return x

        assert my_udf.error_handling is not None
        assert my_udf.error_handling._matchers is not None

    def test_udf_with_on_error_factory_custom(self) -> None:
        """Test @udf with customized factory function"""

        @udf(data_type=pa.int32(), on_error=retry_transient(max_attempts=7))
        def my_udf(x: int) -> int:
            return x

        assert my_udf.error_handling is not None
        assert my_udf.error_handling.retry_config.stop.max_attempt_number == 7

    def test_udf_with_on_error_matchers(self) -> None:
        """Test @udf with on_error matcher list"""

        @udf(
            data_type=pa.int32(),
            on_error=[
                Retry(ConnectionError, max_attempts=5),
                Skip(ValueError),
            ],
        )
        def my_udf(x: int) -> int:
            return x

        assert my_udf.error_handling is not None
        assert my_udf.error_handling.fault_isolation == FaultIsolation.SKIP_ROWS
        assert my_udf.error_handling.retry_config.stop.max_attempt_number == 5

    def test_udf_on_error_and_error_handling_conflict(self) -> None:
        """Test that specifying both on_error and error_handling raises error"""
        with pytest.raises(ValueError, match="Cannot specify both"):

            @udf(
                data_type=pa.int32(),
                on_error=retry_transient(),
                error_handling=ErrorHandlingConfig(),
            )
            def my_udf(x: int) -> int:
                return x

    def test_udf_without_on_error(self) -> None:
        """Test that @udf without on_error has no error_handling"""

        @udf(data_type=pa.int32())
        def my_udf(x: int) -> int:
            return x

        assert my_udf.error_handling is None


# =============================================================================
# Fixture for integration tests
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


# =============================================================================
# Integration tests
# =============================================================================


def test_on_error_retry_transient_integration(
    db: Connection, local_ray_context
) -> None:
    """Integration test: on_error=retry_transient() retries network errors"""
    import fcntl
    import tempfile

    # Create unique temp file for atomic counter
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("0")
        counter_file = Path(f.name)

    def atomic_increment(filepath: Path) -> int:
        """Atomically increment counter in file and return new value"""
        with open(filepath, "r+") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                count = int(f.read() or "0")
                count += 1
                f.seek(0)
                f.write(str(count))
                f.truncate()
                return count
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    @udf(data_type=pa.int32(), on_error=retry_transient())
    def flaky_udf(a: int) -> int:
        count = atomic_increment(counter_file)
        if count < 3:
            raise ConnectionError(f"Temporary failure (attempt {count})")
        return a * 2

    # Add column with UDF
    tbl = db.open_table("test")
    tbl.add_columns({"b": flaky_udf})

    # Backfill should succeed after retries
    job_id = tbl.backfill("b")
    assert job_id is not None

    # Verify results
    result_tbl = db.open_table("test")
    result_data = result_tbl.to_arrow()
    expected = [x * 2 for x in range(SIZE)]
    assert result_data["b"].to_pylist() == expected

    # Cleanup
    counter_file.unlink(missing_ok=True)


def test_on_error_skip_integration(db: Connection, local_ray_context) -> None:
    """Integration test: on_error=skip_on_error() skips failing rows"""

    @udf(data_type=pa.int32(), on_error=skip_on_error())
    def selective_udf(a: int) -> int:
        if a % 3 == 0:  # Skip every 3rd row
            raise ValueError(f"Skipping row {a}")
        return a * 2

    # Add column with UDF
    tbl = db.open_table("test")
    tbl.add_columns({"b": selective_udf})

    # Backfill should succeed (skipping some rows)
    job_id = tbl.backfill("b")
    assert job_id is not None

    # Verify results - rows divisible by 3 should be null
    result_tbl = db.open_table("test")
    result_data = result_tbl.to_arrow()
    b_values = result_data["b"].to_pylist()

    for i, val in enumerate(b_values):
        if i % 3 == 0:
            assert val is None, f"Row {i} should be null"
        else:
            assert val == i * 2, f"Row {i} should be {i * 2}"


def test_on_error_skip_memory_error_integration(
    db: Connection, local_ray_context
) -> None:
    """Per-row Python ``MemoryError`` raised inside a UDF is caught at
    the batch applier and recorded with ``error_type='MemoryError'``
    -- it does NOT crash the actor or go through the bisect path. This
    is the failure mode the cgroup stress test runs into when Python's
    allocator returns a clean ``MemoryError`` before the kernel kills
    the process."""

    @udf(data_type=pa.int32(), on_error=skip_on_error(), version=uuid.uuid4().hex)
    def memory_error_udf(a: int) -> int:
        if a == 5:
            raise MemoryError("simulated allocator failure")
        return a * 2

    tbl = db.open_table("test")
    tbl.add_columns({"b": memory_error_udf})

    result = tbl.backfill("b")
    assert result is not None
    assert result.job_id

    result_tbl = db.open_table("test")
    b_values = result_tbl.to_arrow().sort_by("a")["b"].to_pylist()
    assert b_values[5] is None, f"row 5 should be null, got {b_values[5]!r}"
    populated = sum(1 for v in b_values if v is not None)
    assert populated == SIZE - 1, f"expected {SIZE - 1} populated rows, got {populated}"

    errors = result_tbl.get_errors(job_id=result.job_id, column_name="b")
    mem_errors = [e for e in errors if e.error_type == "MemoryError"]
    types_seen = sorted({e.error_type for e in errors})
    assert mem_errors, f"expected MemoryError record; got types: {types_seen}"
    # Per-row catches do NOT go through _handle_fatal_task_failure, so
    # bisect_depth stays at its default (None). This is the distinguishing
    # signal between the per-row path and the actor-death/bisect path.
    depths = [getattr(e, "bisect_depth", None) for e in mem_errors]
    assert all(d is None for d in depths), (
        f"per-row MemoryError should not set bisect_depth; got {depths}"
    )


@pytest.mark.skipif(
    not HAS_SIGALRM_TIMEOUT, reason="signal.setitimer(SIGALRM) not available"
)
def test_on_error_skip_timeout_integration(db: Connection, local_ray_context) -> None:
    """Integration test: timeout + skip_on_error() nulls timed-out rows."""
    import time

    @udf(data_type=pa.int32(), timeout=0.01, on_error=skip_on_error())
    def selective_timeout_udf(a: int) -> int:
        if a % 3 == 0:
            time.sleep(0.05)
        return a * 2

    tbl = db.open_table("test")
    tbl.add_columns({"b": selective_timeout_udf})

    job_id = tbl.backfill("b")
    assert job_id is not None

    result_tbl = db.open_table("test")
    b_values = result_tbl.to_arrow()["b"].to_pylist()

    for i, val in enumerate(b_values):
        if i % 3 == 0:
            assert val is None, f"Row {i} should be null"
        else:
            assert val == i * 2, f"Row {i} should be {i * 2}"


@pytest.mark.skipif(
    not HAS_SIGALRM_TIMEOUT, reason="signal.setitimer(SIGALRM) not available"
)
def test_on_error_skip_timeout_integration_multiprocess(
    db: Connection, local_ray_context
) -> None:
    """Integration test: timeout works inside MultiProcessBatchApplier workers."""
    import time

    @udf(data_type=pa.int32(), timeout=0.01, on_error=skip_on_error())
    def selective_timeout_udf_mp(a: int) -> int:
        if a % 3 == 0:
            time.sleep(0.05)
        return a * 2

    tbl = db.open_table("test")
    tbl.add_columns(
        {"b": selective_timeout_udf_mp},
        batch_size=2,
        intra_applier_concurrency=2,
    )

    job_id = tbl.backfill("b")
    assert job_id is not None

    result_tbl = db.open_table("test")
    b_values = result_tbl.to_arrow()["b"].to_pylist()

    for i, val in enumerate(b_values):
        if i % 3 == 0:
            assert val is None, f"Row {i} should be null"
        else:
            assert val == i * 2, f"Row {i} should be {i * 2}"


@pytest.mark.skipif(
    not HAS_SIGALRM_TIMEOUT, reason="signal.setitimer(SIGALRM) not available"
)
def test_on_error_retry_timeout_integration(db: Connection, local_ray_context) -> None:
    """Integration test: timeout + retry_transient() retries the batch."""
    import fcntl
    import tempfile
    import time

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("0")
        counter_file = Path(f.name)

    def atomic_increment(filepath: Path) -> int:
        with open(filepath, "r+") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                count = int(f.read() or "0")
                count += 1
                f.seek(0)
                f.write(str(count))
                f.truncate()
                return count
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    @udf(data_type=pa.int32(), timeout=0.01, on_error=retry_transient(max_attempts=2))
    def flaky_timeout_udf(a: int) -> int:
        if atomic_increment(counter_file) == 1:
            time.sleep(0.05)
        return a * 2

    tbl = db.open_table("test")
    tbl.add_columns({"b": flaky_timeout_udf})

    job_id = tbl.backfill("b")
    assert job_id is not None

    result_tbl = db.open_table("test")
    assert result_tbl.to_arrow()["b"].to_pylist() == [x * 2 for x in range(SIZE)]

    counter_file.unlink(missing_ok=True)


def test_default_worker_loss_isolates_row_and_preserves_where_values(
    db: Connection,
    local_ray_context,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The default retries, isolates one row, and preserves WHERE siblings."""

    import geneva.runners.ray.pipeline as pipeline_module

    monkeypatch.setattr(pipeline_module, "DEFAULT_DEFER_CARRY_FORWARD", False)

    @udf(data_type=pa.int32(), version=uuid.uuid4().hex)
    def times_ten(a: int) -> int:
        return a * 10

    @udf(data_type=pa.int32(), version=uuid.uuid4().hex)
    def fatal_exit_udf(a: int) -> int:
        import os

        if a == 0:
            os._exit(137)
        return a * 100

    tbl = db.open_table("test")
    tbl.add_columns({"b": times_ten})
    tbl.backfill("b", where="1=1", concurrency=1, checkpoint_size=4)
    tbl.checkout_latest()
    tbl.alter_columns({"path": "b", "udf": fatal_exit_udf})
    tbl.checkout_latest()

    result = tbl.backfill(
        "b",
        where="a < 2",
        concurrency=1,
        checkpoint_size=64,
        min_checkpoint_size=1,
        max_checkpoint_size=4,
        task_size=SIZE,
    )
    assert result.job_id

    result_tbl = db.open_table("test")
    values = result_tbl.to_arrow().sort_by("a")["b"].to_pylist()
    assert values[:4] == [None, 100, 20, 30]
    assert values[4:] == [a * 10 for a in range(4, SIZE)]
    assert result_tbl.get_failed_row_addresses(result.job_id, "b") == [0]

    errors = result_tbl.get_errors(job_id=result.job_id, column_name="b")
    fatal_errors = [e for e in errors if e.error_type == "FatalWorkerExitError"]
    assert len(fatal_errors) == 1
    assert fatal_errors[0].attempt == 3
    assert fatal_errors[0].max_attempts == 3
    assert fatal_errors[0].bisect_depth > 0

    metrics = {m.name: m for m in db.get_job(result.job_id).metrics or []}
    assert metrics["rows_skipped_on_error"].n == 1
    assert metrics["tasks_completed"].n == metrics["tasks_completed"].total


def test_on_error_skip_fatal_worker_exit_integration(
    db: Connection, local_ray_context
) -> None:
    """skip_on_error should isolate fatal worker exits down to a single row."""

    @udf(
        data_type=pa.int32(),
        on_error=skip_on_error(),
        version=uuid.uuid4().hex,
    )
    def fatal_skip_udf(a: int) -> int:
        import os

        if a == 0:
            os._exit(137)
        return a * 2

    tbl = db.open_table("test")
    tbl.add_columns({"b": fatal_skip_udf}, batch_size=4, concurrency=1)

    result = tbl.backfill("b")
    assert result is not None
    assert result.job_id

    result_tbl = db.open_table("test")
    b_values = result_tbl.to_arrow()["b"].to_pylist()
    assert b_values[0] is None
    assert b_values[1:] == [x * 2 for x in range(1, SIZE)]

    errors = result_tbl.get_errors(job_id=result.job_id, column_name="b")
    assert errors
    assert any(err.error_type == "FatalWorkerExitError" for err in errors)


def test_on_error_retry_all_fatal_worker_exit_integration(
    db: Connection, local_ray_context
) -> None:
    """retry_all should retry fatal worker exits and then succeed."""
    import fcntl
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("0")
        counter_file = Path(f.name)

    def atomic_increment(filepath: Path) -> int:
        with open(filepath, "r+") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                count = int(f.read() or "0")
                count += 1
                f.seek(0)
                f.write(str(count))
                f.truncate()
                return count
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    @udf(
        data_type=pa.int32(),
        on_error=retry_all(max_attempts=2),
        version=uuid.uuid4().hex,
    )
    def fatal_retry_udf(a: int) -> int:
        import os

        if atomic_increment(counter_file) == 1:
            os._exit(137)
        return a * 2

    tbl = db.open_table("test")
    tbl.add_columns({"b": fatal_retry_udf}, batch_size=1, concurrency=1)

    job_id = tbl.backfill("b")
    assert job_id is not None

    result_tbl = db.open_table("test")
    assert result_tbl.to_arrow()["b"].to_pylist() == [x * 2 for x in range(SIZE)]

    counter_file.unlink(missing_ok=True)


def _make_poison_udf(kind: str, on_error, version: str):  # noqa: ANN001, ANN202
    """Build a poison UDF of the given arg type that SIGSEGVs the worker on the
    input containing ``a == 0``.

    One per UDF arg type -- ``scalar`` (``a: int``), ``array`` (``a: pa.Array``),
    ``batch`` (``batch: pa.RecordBatch``). The crash is inlined (not a shared
    helper) so the UDF ships cleanly to the Ray worker; the ``faulthandler`` /
    core-dump suppression keeps this intentional crash out of CI's crash output.
    """
    if kind == "scalar":

        @udf(data_type=pa.int32(), on_error=on_error, version=version)
        def crash_udf(a: int) -> int:
            if a == 0:
                import faulthandler
                import os
                import resource
                import signal

                faulthandler.disable()
                resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
                os.kill(os.getpid(), signal.SIGSEGV)
            return a * 2

        return crash_udf

    if kind == "array":

        @udf(data_type=pa.int32(), on_error=on_error, version=version)
        def crash_udf(a: pa.Array) -> pa.Array:
            import pyarrow.compute as pc

            if pc.any(pc.equal(a, 0)).as_py():
                import faulthandler
                import os
                import resource
                import signal

                faulthandler.disable()
                resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
                os.kill(os.getpid(), signal.SIGSEGV)
            return pc.multiply(a, 2).cast(pa.int32())

        return crash_udf

    @udf(data_type=pa.int32(), on_error=on_error, version=version)
    def crash_udf(batch: pa.RecordBatch) -> pa.Array:
        import pyarrow.compute as pc

        a = batch.column("a")
        if pc.any(pc.equal(a, 0)).as_py():
            import faulthandler
            import os
            import resource
            import signal

            faulthandler.disable()
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
            os.kill(os.getpid(), signal.SIGSEGV)
        return pc.multiply(a, 2).cast(pa.int32())

    return crash_udf


@pytest.mark.parametrize("kind", ["scalar", "array", "batch"])
def test_on_error_retry_then_skip_isolates_fatal_crash_integration(
    db: Connection, local_ray_context, kind: str
) -> None:
    """End-to-end proof, for all three UDF arg types: a real SIGSEGV on the poison
    row is retried at the whole-task level, then bisected to isolate the row --
    nulled and recorded (``bisect_depth > 0``) -- while every other row computes.

    Runs for scalar, array, and RecordBatch (``batch``) UDFs; the customer's case
    is the RecordBatch one (enabled by #1060). ``task_size`` forces multi-row scan
    tasks so isolation requires real splitting, not just retry of a width-1 task.

    Classification note: on the Ray actor path a worker SIGSEGV surfaces as
    ``ActorLostError(WORKER_DIED)`` and normalizes to ``FatalWorkerExitError`` --
    NOT ``FatalWorkerCrashError`` (Ray's ``WorkerCrashedError``, the multiprocess
    path). The policy covers both.
    """
    death = [
        Retry(FatalWorkerCrashError, FatalWorkerExitError, max_attempts=2),
        Skip(FatalWorkerCrashError, FatalWorkerExitError, max_skip_count=SIZE),
    ]
    crash_udf = _make_poison_udf(kind, death, uuid.uuid4().hex)

    tbl = db.open_table("test")
    tbl.add_columns({"b": crash_udf}, concurrency=1)

    # task_size > 1 -> the poison row co-batches with healthy rows, so the driver
    # must bisect (not just retry a width-1 task) to isolate it.
    result = tbl.backfill("b", task_size=10)
    assert result is not None
    assert result.job_id

    result_tbl = db.open_table("test")
    b_values = result_tbl.to_arrow()["b"].to_pylist()
    assert b_values[0] is None  # poison row isolated + nulled
    assert b_values[1:] == [x * 2 for x in range(1, SIZE)]  # every other row computed

    errors = result_tbl.get_errors(job_id=result.job_id, column_name="b")
    exit_errs = [e for e in errors if e.error_type == "FatalWorkerExitError"]
    assert exit_errs
    assert any(e.row_address == 0 for e in exit_errs)
    # Proof the whole task was split to isolate the poison row (job metric).
    assert any((e.bisect_depth or 0) > 0 for e in exit_errs)


def test_on_error_retry_recovers_intermittent_fatal_crash_integration(
    db: Connection, local_ray_context
) -> None:
    """End-to-end proof of the retry leg: a row that SIGSEGVs on its first
    execution succeeds on the whole-task retry, so no row is nulled.

    A cross-process counter file makes the crash fire exactly once (the
    intermittent / mi_malloc failure mode), so the retry recovers it rather than
    the skip path isolating it. Scoped to ``FatalWorkerExitError`` because a Ray
    worker SIGSEGV normalizes to that (see the sibling isolate test).
    """
    import fcntl
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("0")
        counter_file = Path(f.name)

    def atomic_increment(filepath: Path) -> int:
        with open(filepath, "r+") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                count = int(f.read() or "0") + 1
                f.seek(0)
                f.write(str(count))
                f.truncate()
                return count
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    @udf(
        data_type=pa.int32(),
        on_error=[
            Retry(FatalWorkerCrashError, FatalWorkerExitError, max_attempts=3),
            Skip(FatalWorkerCrashError, FatalWorkerExitError, max_skip_count=SIZE),
        ],
        version=uuid.uuid4().hex,
    )
    def intermittent_crash_udf(a: int) -> int:
        # Only row 0's first execution crashes; the whole-task retry then passes.
        if a == 0 and atomic_increment(counter_file) == 1:
            import faulthandler
            import os
            import resource
            import signal

            faulthandler.disable()
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
            os.kill(os.getpid(), signal.SIGSEGV)
        return a * 2

    tbl = db.open_table("test")
    tbl.add_columns({"b": intermittent_crash_udf}, batch_size=4, concurrency=1)

    result = tbl.backfill("b")
    assert result is not None
    assert result.job_id

    result_tbl = db.open_table("test")
    b_values = result_tbl.to_arrow()["b"].to_pylist()
    # Retry recovered the intermittent crash: every row computed, nothing nulled.
    assert b_values == [x * 2 for x in range(SIZE)]

    # The values above are also what a run with no crash at all would produce,
    # so assert row 0 actually executed twice: once crashing, once on retry.
    executions = int(counter_file.read_text() or "0")
    counter_file.unlink(missing_ok=True)
    assert executions >= 2, (
        f"row 0 executed {executions} time(s); the SIGSEGV never fired, "
        "so the retry leg was not exercised"
    )


def test_on_error_retry_then_skip_fatal_worker_exit_preserves_attempts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Split skip subtasks should inherit the parent attempt count."""

    @udf(
        data_type=pa.int32(),
        on_error=[
            Retry(FatalWorkerExitError, max_attempts=2),
            Skip(FatalWorkerExitError),
        ],
        version=uuid.uuid4().hex,
    )
    def fatal_retry_then_skip_udf(a: int) -> int:
        return a

    tbl_ref = TableReference(table_id=["tbl"], version=None, db_uri="db://example")
    task = ScanTask(
        uri="db://example/tbl",
        table_ref=tbl_ref,
        columns=["a", "b"],
        frag_id=0,
        offset=0,
        limit=4,
    )
    replacements = [
        ScanTask(
            uri=task.uri,
            table_ref=task.table_ref,
            columns=task.columns,
            frag_id=task.frag_id,
            offset=0,
            limit=2,
        ),
        ScanTask(
            uri=task.uri,
            table_ref=task.table_ref,
            columns=task.columns,
            frag_id=task.frag_id,
            offset=2,
            limit=2,
        ),
    ]

    job = ColumnAddPipelineJob(
        map_task=BackfillUDFTask(udfs={"b": fatal_retry_then_skip_udf}),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=tbl_ref,
        input_plan=iter(()),
        job_id="job-fatal-retry-then-skip",
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_load_existing_checkpoints_for_task",
        lambda self, task, **kwargs: None,
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_replacement_scan_tasks",
        lambda self, task, split_limit, **kwargs: replacements,
    )

    class _FakeFwm:
        def __init__(self) -> None:
            self.replaced: list[ScanTask] | None = None

        def replace_task(
            self, task: ScanTask, replacement_tasks: list[ScanTask]
        ) -> None:
            self.replaced = replacement_tasks

    fwm = _FakeFwm()
    pending_tasks: deque[ScheduledReadTask] = deque()

    handled = job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=2),
        FatalWorkerExitError("boom"),
        pending_tasks,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )

    assert handled is True
    assert fwm.replaced == replacements
    # Bisect propagates ``bisect_depth = parent.bisect_depth + 1`` so children
    # of the depth=0 root land at depth=1. The attempt counter is preserved
    # (bisect uses ``scheduled.attempt``, not ``attempt + 1``).
    assert list(pending_tasks) == [
        ScheduledReadTask(replacements[0], attempt=2, bisect_depth=1),
        ScheduledReadTask(replacements[1], attempt=2, bisect_depth=1),
    ]


def test_user_policy_retry_preserves_bisect_depth_on_child(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A bisect child (``bisect_depth>0``) hitting a retry-eligible
    error should keep its parent's depth across the retry. Retry does
    not split the task, so the child's depth is the parent's depth.
    Regresses against the pre-fix bug where the retry sites in
    ``_handle_fatal_task_failure`` constructed ``ScheduledReadTask``
    without ``bisect_depth=``, silently resetting depth to 0."""

    @udf(
        data_type=pa.int32(),
        on_error=[Retry(FatalWorkerExitError, max_attempts=3)],
        version=uuid.uuid4().hex,
    )
    def retry_only_udf(a: int) -> int:
        return a

    tbl_ref = TableReference(table_id=["tbl"], version=None, db_uri="db://example")
    task = ScanTask(
        uri="db://example/tbl",
        table_ref=tbl_ref,
        columns=["a", "b"],
        frag_id=0,
        offset=0,
        limit=2,
    )
    # RETRY does not split: ``_replacement_scan_tasks`` is called with
    # ``split_limit=task.limit`` so the single replacement spans the
    # same window as the failing task.
    replacement = ScanTask(
        uri=task.uri,
        table_ref=task.table_ref,
        columns=task.columns,
        frag_id=task.frag_id,
        offset=0,
        limit=2,
    )

    job = ColumnAddPipelineJob(
        map_task=BackfillUDFTask(udfs={"b": retry_only_udf}),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=tbl_ref,
        input_plan=iter(()),
        job_id="job-retry-preserves-depth",
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_load_existing_checkpoints_for_task",
        lambda self, task, **kwargs: None,
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_replacement_scan_tasks",
        lambda self, task, split_limit, **kwargs: [replacement],
    )

    class _FakeFwm:
        def __init__(self) -> None:
            self.replaced: list[ScanTask] | None = None

        def replace_task(
            self, task: ScanTask, replacement_tasks: list[ScanTask]
        ) -> None:
            self.replaced = replacement_tasks

    fwm = _FakeFwm()
    pending_tasks: deque[ScheduledReadTask] = deque()

    # Bisect child at depth=1, attempt=1 (below max_attempts=3 so retry
    # is in budget), hits a retry-eligible error.
    handled = job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=1, bisect_depth=1),
        FatalWorkerExitError("boom"),
        pending_tasks,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )

    assert handled is True
    assert fwm.replaced == [replacement]
    # Retry increments ``attempt`` (1 -> 2) but preserves
    # ``bisect_depth`` (stays at 1). Pre-fix, this would have been 0.
    assert list(pending_tasks) == [
        ScheduledReadTask(replacement, attempt=2, bisect_depth=1),
    ]


def test_transient_fatal_retry_preserves_bisect_depth_on_child(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The default worker-loss retry preserves a child's bisect depth."""

    @udf(
        data_type=pa.int32(),
        # No matcher for transient errors -> the driver fallback engages.
        version=uuid.uuid4().hex,
    )
    def passthrough_udf(a: int) -> int:
        return a

    tbl_ref = TableReference(table_id=["tbl"], version=None, db_uri="db://example")
    task = ScanTask(
        uri="db://example/tbl",
        table_ref=tbl_ref,
        columns=["a", "b"],
        frag_id=0,
        offset=0,
        limit=2,
    )
    replacement = ScanTask(
        uri=task.uri,
        table_ref=task.table_ref,
        columns=task.columns,
        frag_id=task.frag_id,
        offset=0,
        limit=2,
    )

    job = ColumnAddPipelineJob(
        map_task=BackfillUDFTask(udfs={"b": passthrough_udf}),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=tbl_ref,
        input_plan=iter(()),
        job_id="job-transient-preserves-depth",
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_load_existing_checkpoints_for_task",
        lambda self, task, **kwargs: None,
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_replacement_scan_tasks",
        lambda self, task, split_limit, **kwargs: [replacement],
    )

    class _FakeFwm:
        def __init__(self) -> None:
            self.replaced: list[ScanTask] | None = None

        def replace_task(
            self, task: ScanTask, replacement_tasks: list[ScanTask]
        ) -> None:
            self.replaced = replacement_tasks

    fwm = _FakeFwm()
    pending_tasks: deque[ScheduledReadTask] = deque()

    # ``_handle_fatal_task_failure`` runs the raw exception through
    # ``_normalize_fatal_worker_error`` which classifies
    # ``ActorUnavailableError`` -> ``FatalWorkerTransientError``,
    # triggering the transient-retry path.
    transient_exc = ray.exceptions.ActorUnavailableError(
        "actor temporarily unavailable", None
    )
    handled = job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=1, bisect_depth=1),
        transient_exc,
        pending_tasks,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )

    assert handled is True
    assert fwm.replaced == [replacement]
    assert list(pending_tasks) == [
        ScheduledReadTask(replacement, attempt=2, bisect_depth=1),
    ]


@pytest.mark.parametrize(
    "exc",
    [
        ActorLostError(
            ActorStateSnapshot(
                actor_id="actor-dead",
                state="DEAD",
                death_cause={
                    "actorDiedErrorContext": {
                        "reason": "NODE_DIED",
                    }
                },
                death_reason="NODE_DIED",
                node_id="node-dead",
            ),
            "task-1",
        ),
        ray.exceptions.ActorUnavailableError("actor temporarily unavailable", None),
        ray.exceptions.RayActorError(
            actor_id="actor-preempted",
            error_msg="actor died because the node was preempted",
            preempted=True,
        ),
        ray.exceptions.NodeDiedError("node hosting the actor died"),
    ],
    ids=[
        "actor_lost_node_died_without_optional_details",
        "actor_unavailable",
        "preempted_ray_actor_error",
        "node_died",
    ],
)
def test_normalize_fatal_worker_error_classifies_actor_or_node_loss_as_transient(
    exc: Exception,
) -> None:
    """Ray actor/node loss should be treated as transient worker loss."""

    normalized = _normalize_fatal_worker_error(exc)

    assert isinstance(normalized, FatalWorkerTransientError)


def test_normalize_fatal_worker_error_ignores_worker_without_oom_evidence() -> None:
    exc = ray.exceptions.ActorUnavailableError("actor temporarily unavailable", None)
    pod_statuses = [
        {
            "name": "ray-worker",
            "phase": "Failed",
            "ready": False,
            "node_type": "worker",
            "node_name": "node-1",
            "waiting_reasons": Counter(),
            "init_waiting_reasons": Counter(),
            "pulling_count": 0,
            "gpu_requested": False,
            "node_is_gpu": False,
            "oom_evidence": Counter(),
        }
    ]

    normalized = _normalize_fatal_worker_error(exc, pod_statuses=pod_statuses)

    assert isinstance(normalized, FatalWorkerTransientError)


def test_normalize_fatal_worker_error_classifies_actor_unavailable_with_pod_oom() -> (
    None
):
    exc = ray.exceptions.ActorUnavailableError("actor temporarily unavailable", None)
    pod_statuses = [
        {
            "name": "ray-head",
            "phase": "Running",
            "ready": True,
            "node_type": "head",
            "node_name": "node-0",
            "waiting_reasons": Counter(),
            "init_waiting_reasons": Counter(),
            "pulling_count": 0,
            "gpu_requested": False,
            "node_is_gpu": False,
            "oom_evidence": Counter({"state.reason=OOMKilled": 1}),
        },
        {
            "name": "ray-worker",
            "phase": "Failed",
            "ready": False,
            "node_type": "worker",
            "node_name": "node-1",
            "waiting_reasons": Counter(),
            "init_waiting_reasons": Counter(),
            "pulling_count": 0,
            "gpu_requested": False,
            "node_is_gpu": False,
            "oom_evidence": Counter(
                {"last_state.message=memory cgroup out of memory": 1}
            ),
        },
    ]

    normalized = _normalize_fatal_worker_error(exc, pod_statuses=pod_statuses)

    assert isinstance(normalized, FatalWorkerOOMError)


def test_normalize_fatal_worker_error_ignores_ready_worker_last_state_oom() -> None:
    exc = ray.exceptions.ActorUnavailableError("actor temporarily unavailable", None)
    pod_statuses = [
        {
            "name": "ray-worker",
            "phase": "Running",
            "ready": True,
            "node_type": "worker",
            "node_name": "node-1",
            "waiting_reasons": Counter(),
            "init_waiting_reasons": Counter(),
            "pulling_count": 0,
            "gpu_requested": False,
            "node_is_gpu": False,
            "oom_evidence": Counter({"last_state.reason=OOMKilled": 1}),
        }
    ]

    normalized = _normalize_fatal_worker_error(exc, pod_statuses=pod_statuses)

    assert isinstance(normalized, FatalWorkerTransientError)


def test_normalize_fatal_worker_error_classifies_not_ready_worker_last_state_oom() -> (
    None
):
    exc = ray.exceptions.ActorUnavailableError("actor temporarily unavailable", None)
    pod_statuses = [
        {
            "name": "ray-worker",
            "phase": "Running",
            "ready": False,
            "node_type": "worker",
            "node_name": "node-1",
            "waiting_reasons": Counter(),
            "init_waiting_reasons": Counter(),
            "pulling_count": 0,
            "gpu_requested": False,
            "node_is_gpu": False,
            "oom_evidence": Counter(
                {"last_state.message=memory cgroup out of memory": 1}
            ),
        }
    ]

    normalized = _normalize_fatal_worker_error(exc, pod_statuses=pod_statuses)

    assert isinstance(normalized, FatalWorkerOOMError)


def test_normalize_fatal_worker_error_classifies_ready_worker_current_oom() -> None:
    exc = ray.exceptions.ActorUnavailableError("actor temporarily unavailable", None)
    pod_statuses = [
        {
            "name": "ray-worker",
            "phase": "Running",
            "ready": True,
            "node_type": "worker",
            "node_name": "node-1",
            "waiting_reasons": Counter(),
            "init_waiting_reasons": Counter(),
            "pulling_count": 0,
            "gpu_requested": False,
            "node_is_gpu": False,
            "oom_evidence": Counter({"state.reason=OOMKilled": 1}),
        }
    ]

    normalized = _normalize_fatal_worker_error(exc, pod_statuses=pod_statuses)

    assert isinstance(normalized, FatalWorkerOOMError)


def test_normalize_fatal_worker_error_classifies_actor_died_with_pod_oom() -> None:
    exc = ray.exceptions.ActorDiedError(None)
    pod_statuses = [
        {
            "name": "ray-worker",
            "phase": "Failed",
            "ready": False,
            "node_type": "worker",
            "node_name": "node-1",
            "waiting_reasons": Counter(),
            "init_waiting_reasons": Counter(),
            "pulling_count": 0,
            "gpu_requested": False,
            "node_is_gpu": False,
            "oom_evidence": Counter({"last_state.reason=OOMKilled": 1}),
        }
    ]

    normalized = _normalize_fatal_worker_error(exc, pod_statuses=pod_statuses)

    assert isinstance(normalized, FatalWorkerOOMError)


@pytest.mark.parametrize(
    "exc",
    [
        ray.exceptions.NodeDiedError("node hosting the actor died"),
        ActorLostError(
            ActorStateSnapshot(
                actor_id="actor-dead",
                state="DEAD",
                death_cause={
                    "actorDiedErrorContext": {
                        "reason": "NODE_DIED",
                        "nodeDeathInfo": {"reason": "NODE_DIED"},
                    }
                },
                death_reason="NODE_DIED",
                node_id="node-dead",
            ),
            "task-1",
        ),
    ],
    ids=["node_died", "actor_lost_node_died"],
)
def test_normalize_fatal_worker_error_classifies_actor_or_node_loss_with_pod_oom(
    exc: Exception,
) -> None:
    pod_statuses = [
        {
            "name": "ray-worker",
            "phase": "Running",
            "ready": True,
            "node_type": "worker",
            "node_name": "node-1",
            "waiting_reasons": Counter(),
            "init_waiting_reasons": Counter(),
            "pulling_count": 0,
            "gpu_requested": False,
            "node_is_gpu": False,
            "oom_evidence": Counter({"state.reason=OOMKilled": 1}),
        }
    ]

    normalized = _normalize_fatal_worker_error(exc, pod_statuses=pod_statuses)

    assert isinstance(normalized, FatalWorkerOOMError)


@pytest.mark.parametrize(
    "exc",
    [
        ActorLostError(
            ActorStateSnapshot(
                actor_id="actor-dead",
                state="DEAD",
                death_cause=None,
                death_reason=None,
                node_id="node-live",
            ),
            "task-1",
        ),
        ActorLostError(
            ActorStateSnapshot(
                actor_id="actor-dead",
                state="DEAD",
                death_cause={"actorDiedErrorContext": {"reason": "WORKER_DIED"}},
                death_reason="WORKER_DIED",
                node_id="node-live",
            ),
            "task-1",
        ),
        ray.exceptions.ActorDiedError(None),
        ray.exceptions.RayActorError(
            actor_id="actor-abc", error_msg="actor died before task finished"
        ),
    ],
    ids=[
        "actor_lost_no_death_cause",
        "actor_lost_worker_died",
        "actor_died",
        "ray_actor_error",
    ],
)
def test_normalize_fatal_worker_error_keeps_generic_actor_errors_as_exit(
    exc: Exception,
) -> None:
    """Generic actor process exits are not retried as infrastructure loss."""

    normalized = _normalize_fatal_worker_error(exc)

    assert isinstance(normalized, FatalWorkerExitError)


@pytest.mark.parametrize("oom_context_key", ["oomContext", "oom_context"])
def test_normalize_fatal_worker_error_classifies_actor_lost_oom_context(
    oom_context_key: str,
) -> None:
    exc = ActorLostError(
        ActorStateSnapshot(
            actor_id="actor-oom",
            state="DEAD",
            death_cause={oom_context_key: {}},
            death_reason=None,
            node_id="node-live",
        ),
        "task-1",
    )

    normalized = _normalize_fatal_worker_error(exc)

    assert isinstance(normalized, FatalWorkerOOMError)


def test_normalize_fatal_worker_error_classifies_oom() -> None:
    """Ray's preemptive memory-monitor kill surfaces as OutOfMemoryError;
    Geneva should classify it as FatalWorkerOOMError."""
    exc = ray.exceptions.OutOfMemoryError("worker killed by memory monitor")

    normalized = _normalize_fatal_worker_error(exc)

    assert isinstance(normalized, FatalWorkerOOMError)


def test_normalize_fatal_worker_error_classifies_worker_crashed() -> None:
    """Native crash (SIGSEGV/SIGABRT) surfaces as WorkerCrashedError;
    Geneva should classify it as FatalWorkerCrashError."""
    exc = ray.exceptions.WorkerCrashedError()

    normalized = _normalize_fatal_worker_error(exc)

    assert isinstance(normalized, FatalWorkerCrashError)


def test_normalize_fatal_worker_error_classifies_segfault_text_as_crash() -> None:
    """A plain Exception whose message mentions ``segfault`` /
    ``segmentation fault`` should also classify as FatalWorkerCrashError.
    This covers the case where the native crash signal is encoded in the
    error text rather than as a typed WorkerCrashedError."""
    exc = RuntimeError("worker died: segmentation fault at 0xdeadbeef")

    normalized = _normalize_fatal_worker_error(exc)

    assert isinstance(normalized, FatalWorkerCrashError)


def test_normalize_fatal_worker_error_defaults_to_exit() -> None:
    """A non-Ray actor/node-loss exception falls through to exit."""
    exc = RuntimeError("worker exited unexpectedly")

    normalized = _normalize_fatal_worker_error(exc)

    assert isinstance(normalized, FatalWorkerExitError)


class _FutureFatalWorkerError(FatalWorkerError):
    pass


@pytest.mark.parametrize(
    ("error", "outcome", "max_attempts"),
    [
        (FatalWorkerExitError("exit"), Outcome.RETRY, 3),
        (FatalWorkerTransientError("transient"), Outcome.RETRY, 3),
        (_FutureFatalWorkerError("future"), Outcome.RETRY, 3),
        (FatalWorkerCrashError("crash"), Outcome.SKIP, 1),
        (FatalWorkerOOMError("oom"), None, None),
        (ShortFragmentWriteError("short write"), None, None),
        (CorruptCheckpointError("key"), None, None),
        (CheckpointCoverageError(0), None, None),
        (MergeFallbackTargetError("missing target"), None, None),
    ],
)
def test_default_worker_loss_policy(
    error: FatalWorkerError,
    outcome: Outcome | None,
    max_attempts: int | None,
) -> None:
    config = _default_worker_loss_policy(error)
    if outcome is None:
        assert config is None
        return
    assert get_exception_outcome(error, config) == outcome
    assert config.fault_isolation == FaultIsolation.SKIP_ROWS
    assert get_max_attempts(config.retry_config) == max_attempts


@pytest.mark.parametrize(
    "config",
    [resolve_on_error(fail_fast()), ErrorHandlingConfig()],
)
def test_explicit_empty_policy_handles_worker_loss(config: ErrorHandlingConfig) -> None:
    assert _config_handles_exception(config, FatalWorkerExitError("worker exited"))


def test_default_transient_fatal_retry_budget(monkeypatch: pytest.MonkeyPatch) -> None:
    @udf(data_type=pa.int32(), version=uuid.uuid4().hex)
    def transient_udf(a: int) -> int:
        return a

    tbl_ref = TableReference(table_id=["tbl"], version=None, db_uri="db://example")
    task = ScanTask(
        uri="db://example/tbl",
        table_ref=tbl_ref,
        columns=["a", "b"],
        frag_id=0,
        offset=0,
        limit=4,
    )

    job = ColumnAddPipelineJob(
        map_task=BackfillUDFTask(udfs={"b": transient_udf}),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=tbl_ref,
        input_plan=iter(()),
        job_id="job-default-transient-retry",
    )
    invalid_key = "short-checkpoint"

    def _no_checkpoint(self, task, *, invalid_checkpoint_keys=None) -> None:
        invalid_checkpoint_keys.add(invalid_key)
        return None

    original_replacements = ColumnAddPipelineJob._replacement_scan_tasks
    seen_exclusions: list[set[str]] = []

    def _capture_replacements(self, task, **kwargs) -> list[ScanTask]:
        seen_exclusions.append(set(kwargs["excluded_checkpoint_keys"]))
        return original_replacements(self, task, **kwargs)

    monkeypatch.setattr(
        ColumnAddPipelineJob, "_load_existing_checkpoints_for_task", _no_checkpoint
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob, "_replacement_scan_tasks", _capture_replacements
    )

    class _FakeFwm:
        def replace_task(
            self, task: ScanTask, replacement_tasks: list[ScanTask]
        ) -> None:
            return None

    transient_exc = ray.exceptions.ActorUnavailableError(
        "actor temporarily unavailable", None
    )

    pending_tasks: deque[ScheduledReadTask] = deque()
    handled = job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=1),
        transient_exc,
        pending_tasks,
        _FakeFwm(),  # type: ignore[arg-type]
        pod_statuses=None,
    )
    assert handled is True
    assert list(pending_tasks) == [ScheduledReadTask(task, attempt=2)]

    pending_tasks.clear()
    handled = job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=2),
        transient_exc,
        pending_tasks,
        _FakeFwm(),  # type: ignore[arg-type]
        pod_statuses=None,
    )
    assert handled is True
    assert list(pending_tasks) == [ScheduledReadTask(task, attempt=3)]

    pending_tasks.clear()
    assert job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=3),
        transient_exc,
        pending_tasks,
        _FakeFwm(),  # type: ignore[arg-type]
        pod_statuses=None,
    )
    assert [
        (item.task.offset, item.task.limit, item.attempt, item.bisect_depth)
        for item in pending_tasks
    ] == [(0, 2, 3, 1), (2, 2, 3, 1)]
    assert seen_exclusions == [{invalid_key}] * 3


def test_default_transient_fatal_retry_applies_when_on_error_omits_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    @udf(
        data_type=pa.int32(),
        on_error=[Skip(ValueError)],
        version=uuid.uuid4().hex,
    )
    def transient_udf(a: int) -> int:
        return a

    tbl_ref = TableReference(table_id=["tbl"], version=None, db_uri="db://example")
    task = ScanTask(
        uri="db://example/tbl",
        table_ref=tbl_ref,
        columns=["a", "b"],
        frag_id=0,
        offset=0,
        limit=4,
    )

    job = ColumnAddPipelineJob(
        map_task=BackfillUDFTask(udfs={"b": transient_udf}),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=tbl_ref,
        input_plan=iter(()),
        job_id="job-transient-default-with-user-config",
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_load_existing_checkpoints_for_task",
        lambda self, task, **kwargs: None,
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_replacement_scan_tasks",
        lambda self, task, split_limit, **kwargs: [task],
    )

    class _FakeFwm:
        def replace_task(
            self, task: ScanTask, replacement_tasks: list[ScanTask]
        ) -> None:
            return None

    transient_exc = ray.exceptions.ActorUnavailableError(
        "actor temporarily unavailable", None
    )
    pending_tasks: deque[ScheduledReadTask] = deque()

    handled = job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=1),
        transient_exc,
        pending_tasks,
        _FakeFwm(),  # type: ignore[arg-type]
        pod_statuses=None,
    )

    assert handled is True
    assert list(pending_tasks) == [ScheduledReadTask(task, attempt=2)]


def test_explicit_fail_transient_overrides_default_retry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    @udf(
        data_type=pa.int32(),
        on_error=[Fail(FatalWorkerTransientError)],
        version=uuid.uuid4().hex,
    )
    def transient_udf(a: int) -> int:
        return a

    tbl_ref = TableReference(table_id=["tbl"], version=None, db_uri="db://example")
    task = ScanTask(
        uri="db://example/tbl",
        table_ref=tbl_ref,
        columns=["a", "b"],
        frag_id=0,
        offset=0,
        limit=4,
    )

    job = ColumnAddPipelineJob(
        map_task=BackfillUDFTask(udfs={"b": transient_udf}),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=tbl_ref,
        input_plan=iter(()),
        job_id="job-transient-explicit-fail",
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_load_existing_checkpoints_for_task",
        lambda self, task, **kwargs: None,
    )

    class _FakeFwm:
        def replace_task(
            self, task: ScanTask, replacement_tasks: list[ScanTask]
        ) -> None:
            raise AssertionError("replace_task should not be called")

    transient_exc = ray.exceptions.ActorUnavailableError(
        "actor temporarily unavailable", None
    )

    with pytest.raises(FatalWorkerTransientError):
        job._handle_fatal_task_failure(
            ScheduledReadTask(task, attempt=1),
            transient_exc,
            deque(),
            _FakeFwm(),  # type: ignore[arg-type]
            pod_statuses=None,
        )


def test_actor_unavailable_oom_classification_is_wired_into_handler_and_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    @udf(data_type=pa.int32(), version=uuid.uuid4().hex)
    def passthrough_udf(a: int) -> int:
        return a

    tbl_ref = TableReference(table_id=["tbl"], version=None, db_uri="db://example")

    def _new_job(job_id: str) -> ColumnAddPipelineJob:
        return ColumnAddPipelineJob(
            map_task=BackfillUDFTask(udfs={"b": passthrough_udf}),
            checkpoint_store=CheckpointStore.from_uri("memory"),
            error_store=None,
            config=JobConfig(),
            dst=tbl_ref,
            input_plan=iter(()),
            job_id=job_id,
        )

    pod_statuses = [
        {
            "name": "ray-worker",
            "phase": "Failed",
            "ready": False,
            "node_type": "worker",
            "node_name": "node-1",
            "waiting_reasons": Counter(),
            "init_waiting_reasons": Counter(),
            "pulling_count": 0,
            "gpu_requested": False,
            "node_is_gpu": False,
            "oom_evidence": Counter({"state.reason=OOMKilled": 1}),
        }
    ]
    actor_exc = ray.exceptions.ActorUnavailableError(
        "actor temporarily unavailable", None
    )

    task = ScanTask(
        uri="db://example/tbl",
        table_ref=tbl_ref,
        columns=["a", "b"],
        frag_id=0,
        offset=0,
        limit=4,
    )

    class _FakeFwm:
        def __init__(self) -> None:
            self.replaced: list[ScanTask] | None = None

        def replace_task(
            self, task: ScanTask, replacement_tasks: list[ScanTask]
        ) -> None:
            self.replaced = replacement_tasks

    handler_job = _new_job("job-handler-k8s-oom")
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_load_existing_checkpoints_for_task",
        lambda self, task, **kwargs: None,
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_get_k8s_pod_statuses",
        lambda self: pod_statuses,
    )

    # Actor loss with pod OOM evidence classifies as FatalWorkerOOMError and
    # takes the default bounded OOM recovery: the task is split in half and
    # resubmitted (not the transient path, which would keep the task size).
    fwm = _FakeFwm()
    pending: deque[ScheduledReadTask] = deque()
    handled = handler_job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=3),
        actor_exc,
        pending,
        fwm,  # type: ignore[arg-type]
        pod_statuses=pod_statuses,
    )
    assert handled is True
    assert fwm.replaced is not None
    assert [t.limit for t in fwm.replaced] == [2, 2]
    # Splitting preserves the attempt counter (matching the SKIP-bisect
    # path); OOM recovery is bounded by its own budget, not by attempts.
    assert [(s.attempt, s.bisect_depth) for s in pending] == [(3, 1), (3, 1)]
    assert handler_job.skipped_stats.get("oom_recoveries") == 1

    from geneva.runners.ray import pipeline as ray_pipeline
    from geneva.runners.ray.actor_pool import ActorPoolTaskError

    class _FakeDataset:
        uri = "memory://dataset"
        version = 1

    class _FakePool:
        _num_actors = 0

        def __init__(self) -> None:
            self.shutdown_called = False

        def submission_capacity(self) -> int:
            return 1

        def submit(self, _fn, _value) -> None:  # noqa: ANN001
            return None

        def has_next(self) -> bool:
            return True

        def drain_ready(self, timeout: float) -> NoReturn:
            raise ActorPoolTaskError(ScheduledReadTask(object()), actor_exc)

        def shutdown(self) -> None:
            self.shutdown_called = True

    class _FakeFragmentWriterManager:
        def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
            return None

    fallback_job = _new_job("job-fallback-k8s-oom")
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "setup_inputplans",
        lambda self: (iter([object()]), Counter(), 1),
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "setup_writertracker",
        lambda self, planned_frag_count: (_FakeDataset(), 1),
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_ensure_driver_checkpoint_identity_sidecar",
        lambda self, dataset_uri: None,
    )
    fake_pool = _FakePool()
    monkeypatch.setattr(ColumnAddPipelineJob, "setup_actorpool", lambda self: fake_pool)
    monkeypatch.setattr(
        ColumnAddPipelineJob, "_refresh_cluster_status", lambda self: None
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob, "_fetch_cluster_status", lambda self: None
    )
    monkeypatch.setattr(
        ray_pipeline,
        "FragmentWriterManager",
        _FakeFragmentWriterManager,
    )

    with pytest.raises(FatalWorkerOOMError):
        fallback_job.run()
    assert fake_pool.shutdown_called


def test_on_error_custom_matchers_integration(
    db: Connection, local_ray_context
) -> None:
    """Integration test: on_error with custom matcher list"""
    import fcntl
    import tempfile

    # Create unique temp file for atomic counter
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("0")
        counter_file = Path(f.name)

    def atomic_increment(filepath: Path) -> int:
        with open(filepath, "r+") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                count = int(f.read() or "0")
                count += 1
                f.seek(0)
                f.write(str(count))
                f.truncate()
                return count
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    @udf(
        data_type=pa.int32(),
        on_error=[
            Retry(ConnectionError, max_attempts=3),
            Skip(ValueError),
        ],
    )
    def mixed_udf(a: int) -> int:
        count = atomic_increment(counter_file)

        # First two calls fail with connection error (will retry)
        if count < 3:
            raise ConnectionError(f"Network issue (attempt {count})")

        # Skip every 5th row with ValueError
        if a % 5 == 0:
            raise ValueError(f"Skipping row {a}")

        return a * 2

    # Add column with UDF
    tbl = db.open_table("test")
    tbl.add_columns({"b": mixed_udf})

    # Backfill should succeed
    job_id = tbl.backfill("b")
    assert job_id is not None

    # Verify results
    result_tbl = db.open_table("test")
    result_data = result_tbl.to_arrow()
    b_values = result_data["b"].to_pylist()

    for i, val in enumerate(b_values):
        if i % 5 == 0:
            assert val is None, f"Row {i} should be null (skipped)"
        else:
            assert val == i * 2, f"Row {i} should be {i * 2}"

    # Cleanup
    counter_file.unlink(missing_ok=True)


def test_normalize_preserves_preclassified_fatal_worker_error() -> None:
    """Re-normalizing an already-classified fatal worker error keeps its type
    (no downgrade to FatalWorkerExitError) without aliasing the instance."""
    oom = FatalWorkerOOMError("worker OOMKilled")

    direct = _normalize_fatal_worker_error(oom)
    assert type(direct) is FatalWorkerOOMError
    assert direct is not oom

    outer = RuntimeError("wrapper")
    outer.__cause__ = oom
    nested = _normalize_fatal_worker_error(outer)
    assert type(nested) is FatalWorkerOOMError
    assert "worker OOMKilled" in str(nested)
    assert nested is not oom


def test_partial_checkpoints_reingested_when_task_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A task that dies after flushing some checkpoints must re-ingest the
    flushed coverage into the writer; replacements cover only the gaps.

    Without the re-ingest, the flushed rows never reach the writer and are
    null-filled at seal (the orphan-null bug: completed full-table backfills
    with millions of silently null output rows).
    """

    @udf(data_type=pa.int32(), version=uuid.uuid4().hex)
    def plain_udf(a: int) -> int:
        return a

    tbl_ref = TableReference(table_id=["tbl"], version=None, db_uri="db://example")
    task = ScanTask(
        uri="db://example/tbl",
        table_ref=tbl_ref,
        columns=["a", "b"],
        frag_id=0,
        offset=0,
        limit=4,
    )

    store = CheckpointStore.from_uri("memory")
    map_task = BackfillUDFTask(udfs={"b": plain_udf})
    job = ColumnAddPipelineJob(
        map_task=map_task,
        checkpoint_store=store,
        error_store=None,
        config=JobConfig(),
        dst=tbl_ref,
        input_plan=iter(()),
        job_id="job-partial-reingest",
    )

    # The task flushed a checkpoint for [0, 2) before dying; [2, 4) is missing.
    flushed_key = map_task.checkpoint_key(
        dataset_uri=task.table_uri(),
        dataset_version=getattr(task, "version", None),
        frag_id=task.dest_frag_id(),
        start=0,
        end=2,
        where=None,
        src_files_hash=job._src_files_hash_for_task(task),
    )
    store[flushed_key] = pa.record_batch([], names=[])

    class _FakeFwm:
        def __init__(self) -> None:
            self.recovered: list[tuple[ScanTask, list]] = []
            self.replaced: list[ScanTask] | None = None

        def ingest_recovered_checkpoints(
            self, task: ScanTask, checkpoints: list
        ) -> None:
            self.recovered.append((task, checkpoints))

        def replace_task(
            self, task: ScanTask, replacement_tasks: list[ScanTask]
        ) -> None:
            self.replaced = list(replacement_tasks)

    fwm = _FakeFwm()
    pending_tasks: deque[ScheduledReadTask] = deque()

    handled = job._handle_fatal_task_failure(
        ScheduledReadTask(task, attempt=0),
        FatalWorkerTransientError("worker lost"),
        pending_tasks,
        fwm,  # type: ignore[arg-type]
        pod_statuses=None,
    )

    assert handled is True
    # The flushed [0, 2) coverage was re-ingested for the writer.
    assert len(fwm.recovered) == 1
    _, checkpoints = fwm.recovered[0]
    assert [(c.offset, c.span, c.checkpoint_key) for c in checkpoints] == [
        (0, 2, flushed_key)
    ]
    # Replacements cover only the missing [2, 4) range.
    assert fwm.replaced is not None
    assert [(t.offset, t.limit) for t in fwm.replaced] == [(2, 2)]
    assert [(s.task.offset, s.task.limit) for s in pending_tasks] == [(2, 2)]
