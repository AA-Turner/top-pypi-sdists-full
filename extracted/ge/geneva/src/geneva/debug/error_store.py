# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Error storage and retry configuration for UDF execution"""

import enum
import logging
import re
import traceback
import uuid
from collections.abc import Callable
from datetime import datetime
from typing import Any, Optional

import attrs
import pyarrow as pa
from tenacity import (
    RetryCallState,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    wait_fixed,
    wait_random_exponential,
)
from tenacity.retry import retry_base
from tenacity.stop import stop_base
from tenacity.wait import wait_base

from geneva.state.manager import BaseManager
from geneva.utils import dt_now_utc, escape_sql_string, retry_lance

_LOG = logging.getLogger(__name__)

GENEVA_ERRORS_TABLE_NAME = "geneva_errors"


class SkipThresholdExceededError(Exception):
    """Raised when cumulative skipped rows exceed the configured threshold.

    Attributes
    ----------
    skipped : int
        Total number of rows skipped so far
    processed : int
        Total number of rows processed so far
    max_count : int | None
        Configured max skip count threshold (if set)
    max_fraction : float | None
        Configured max skip fraction threshold (if set)
    """

    def __init__(
        self,
        skipped: int,
        processed: int,
        max_count: int | None,
        max_fraction: float | None,
    ) -> None:
        self.skipped = skipped
        self.processed = processed
        self.max_count = max_count
        self.max_fraction = max_fraction
        parts = [
            f"Skip threshold exceeded: {skipped} rows skipped"
            f" out of {processed} processed."
        ]
        if max_count is not None and skipped > max_count:
            parts.append(f"max_skip_count={max_count}")
        if (
            max_fraction is not None
            and processed > 0
            and skipped / processed > max_fraction
        ):
            actual = skipped / processed
            parts.append(f"max_skip_fraction={max_fraction} (actual: {actual:.4f})")
        super().__init__(" ".join(parts))

    def __reduce__(self) -> tuple:
        # Make picklable for Ray serialization across process boundaries.
        return (
            self.__class__,
            (self.skipped, self.processed, self.max_count, self.max_fraction),
        )


class FaultIsolation(enum.Enum):
    """Strategy for isolating UDF failures"""

    FAIL_BATCH = "fail_batch"  # Fail entire batch on any error (default)
    SKIP_ROWS = "skip_rows"  # Isolate failing rows by bisection and skip them


@attrs.define
class UDFRetryConfig:
    """Retry configuration for UDF execution using tenacity semantics"""

    # Tenacity retry condition - which exceptions to retry
    retry: retry_base = attrs.field(
        factory=lambda: retry_if_exception_type(())  # No retries by default
    )

    # Stop condition - when to give up
    stop: stop_base = attrs.field(factory=lambda: stop_after_attempt(1))

    # Wait strategy - how long to wait between retries
    wait: wait_base = attrs.field(
        factory=lambda: wait_exponential(multiplier=1, min=1, max=60)
    )

    # Optional callbacks
    before_sleep: Callable[[RetryCallState], None] | None = attrs.field(default=None)
    after_attempt: Callable[[RetryCallState], None] | None = attrs.field(default=None)

    # Whether to reraise exception after retries exhausted
    reraise: bool = attrs.field(default=True)

    @classmethod
    def no_retry(cls) -> "UDFRetryConfig":
        """No retries - fail immediately (default behavior)"""
        return cls()

    @classmethod
    def retry_transient(cls, max_attempts: int = 3) -> "UDFRetryConfig":
        """Retry common transient errors (network, timeouts)

        Parameters
        ----------
        max_attempts : int
            Maximum number of attempts including the initial try
        """
        return cls(
            retry=retry_if_exception_type((OSError, TimeoutError, ConnectionError)),
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=1, min=1, max=60),
        )


@attrs.define
class ErrorHandlingConfig:
    """Configuration for UDF error handling behavior"""

    # Retry policy using tenacity
    retry_config: UDFRetryConfig = attrs.field(factory=UDFRetryConfig.no_retry)

    # How to isolate failures
    fault_isolation: FaultIsolation = attrs.field(default=FaultIsolation.FAIL_BATCH)

    # Whether to log errors to the error table
    log_errors: bool = attrs.field(default=True)

    # Whether to log all retry attempts (not just final failures)
    log_retry_attempts: bool = attrs.field(default=False)

    # Skip threshold: fail job if too many rows are skipped (SKIP_ROWS only)
    max_skip_count: int | None = attrs.field(default=None)
    max_skip_fraction: float | None = attrs.field(default=None)

    # Internal: Store matchers for runtime exception matching (set by resolve_on_error)
    _matchers: Optional[list["ExceptionMatcher"]] = attrs.field(
        default=None, repr=False, alias="_matchers"
    )

    def __attrs_post_init__(self) -> None:
        """Validate skip threshold configuration"""
        if self.max_skip_count is not None:
            if self.max_skip_count < 0:
                raise ValueError(
                    f"max_skip_count must be >= 0, got {self.max_skip_count}"
                )
            if self.fault_isolation != FaultIsolation.SKIP_ROWS:
                raise ValueError(
                    "max_skip_count can only be used with fault_isolation=SKIP_ROWS"
                )
        if self.max_skip_fraction is not None:
            if not (0.0 <= self.max_skip_fraction <= 1.0):
                raise ValueError(
                    f"max_skip_fraction must be between 0.0 and 1.0, "
                    f"got {self.max_skip_fraction}"
                )
            if self.fault_isolation != FaultIsolation.SKIP_ROWS:
                raise ValueError(
                    "max_skip_fraction can only be used with fault_isolation=SKIP_ROWS"
                )

    def validate_compatibility(self, map_task) -> None:
        """Validate that this error config is compatible with the given task

        Parameters
        ----------

        map_task
            The MapTask to validate against

        Raises
        ------

        ValueError
            If the config is incompatible with the task
        """
        # SKIP_ROWS supports every UDF arg type: SkipRowsStrategy applies
        # batches whole and bisects on failure.
        return


# =============================================================================
# Simplified on_error API
# =============================================================================


class Outcome(enum.Enum):
    """Outcome for exception handling"""

    RETRY = "retry"
    SKIP = "skip"
    FAIL = "fail"


def _normalize_exceptions(
    exceptions: type[Exception] | tuple[type[Exception], ...] | list[type[Exception]],
) -> tuple[type[Exception], ...]:
    """Convert exception input to a tuple of exception types"""
    if isinstance(exceptions, type) and issubclass(exceptions, BaseException):
        return (exceptions,)
    return tuple(exceptions)


@attrs.define
class ExceptionMatcher:
    """Base class for exception matchers"""

    exceptions: tuple[type[Exception], ...] = attrs.field(
        converter=_normalize_exceptions
    )
    match: Optional[str] = attrs.field(default=None)
    _compiled_pattern: Optional[re.Pattern[str]] = attrs.field(
        default=None, init=False, repr=False
    )

    def __attrs_post_init__(self) -> None:
        """Pre-compile regex pattern for validation and performance"""
        if self.match is not None:
            try:
                object.__setattr__(self, "_compiled_pattern", re.compile(self.match))
            except re.error as e:
                raise ValueError(
                    f"Invalid regex pattern in match parameter: '{self.match}'. "
                    f"Error: {e}"
                ) from e

    def matches(self, exc: Exception) -> bool:
        """Check if this matcher matches the given exception"""
        if not isinstance(exc, self.exceptions):
            return False
        if self._compiled_pattern is None:
            return True
        return bool(self._compiled_pattern.search(str(exc)))


_VALID_BACKOFF_STRATEGIES = ("exponential", "fixed", "linear")


def _validate_backoff(
    instance: "Retry", attribute: attrs.Attribute, value: str
) -> None:
    """Validate that backoff is a valid strategy"""
    if value not in _VALID_BACKOFF_STRATEGIES:
        raise ValueError(
            f"Invalid backoff strategy: '{value}'. "
            f"Must be one of: {', '.join(_VALID_BACKOFF_STRATEGIES)}"
        )


@attrs.define
class Retry(ExceptionMatcher):
    """Retry on matching exceptions with backoff

    Parameters
    ----------
    *exceptions : type[Exception]
        Exception types to match
    match : str, optional
        Regex pattern to match in exception message.
        Simple strings work as substring matches (e.g., "rate limit").
        Use (?i) for case-insensitive matching.
    max_attempts : int
        Maximum number of attempts (default: 3)
    backoff : str
        Backoff strategy: "exponential" (default), "fixed", or "linear"

    Examples
    --------

        Retry(ConnectionError, TimeoutError, max_attempts=3)
        Retry(ValueError, match="rate limit", max_attempts=5)
        Retry(APIError, match=r"429|rate.?limit")
        Retry(APIError, match=r"(?i)rate limit")  # case-insensitive
    """

    max_attempts: int = attrs.field(default=3)
    backoff: str = attrs.field(default="exponential", validator=_validate_backoff)

    def __init__(
        self,
        *exceptions: type[Exception],
        match: Optional[str] = None,
        max_attempts: int = 3,
        backoff: str = "exponential",
    ) -> None:
        # Handle both Retry(E1, E2) and Retry((E1, E2)) syntax
        if len(exceptions) == 1 and isinstance(exceptions[0], (tuple, list)):
            exceptions = tuple(exceptions[0])
        self.__attrs_init__(  # pyright: ignore[reportAttributeAccessIssue]
            exceptions=exceptions,
            match=match,
            max_attempts=max_attempts,
            backoff=backoff,
        )


@attrs.define
class Skip(ExceptionMatcher):
    """Skip row (return None) on matching exceptions

    Parameters
    ----------
    *exceptions : type[Exception]
        Exception types to match
    match : str, optional
        Regex pattern to match in exception message
    max_skip_count : int, optional
        Maximum number of rows that can be skipped before failing the job.
        Only used when passed via ``skip_on_error()``.
    max_skip_fraction : float, optional
        Maximum fraction of rows (0.0-1.0) that can be skipped before
        failing the job. Only used when passed via ``skip_on_error()``.

    Examples
    --------

        Skip(ValueError, KeyError)
        Skip(ValueError, match="invalid input")
    """

    max_skip_count: int | None = attrs.field(default=None)
    max_skip_fraction: float | None = attrs.field(default=None)

    def __init__(
        self,
        *exceptions: type[Exception],
        match: Optional[str] = None,
        max_skip_count: int | None = None,
        max_skip_fraction: float | None = None,
    ) -> None:
        if len(exceptions) == 1 and isinstance(exceptions[0], (tuple, list)):
            exceptions = tuple(exceptions[0])
        self.__attrs_init__(  # pyright: ignore[reportAttributeAccessIssue]
            exceptions=exceptions,
            match=match,
            max_skip_count=max_skip_count,
            max_skip_fraction=max_skip_fraction,
        )


@attrs.define
class Fail(ExceptionMatcher):
    """Fail job immediately on matching exceptions

    Parameters
    ----------
    *exceptions : type[Exception]
        Exception types to match
    match : str, optional
        Regex pattern to match in exception message

    Examples
    --------

        Fail(AuthError)
        Fail(ValueError, match="fatal")
    """

    def __init__(
        self,
        *exceptions: type[Exception],
        match: Optional[str] = None,
    ) -> None:
        if len(exceptions) == 1 and isinstance(exceptions[0], (tuple, list)):
            exceptions = tuple(exceptions[0])
        self.__attrs_init__(  # pyright: ignore[reportAttributeAccessIssue]
            exceptions=exceptions, match=match
        )


# Type alias for on_error parameter
OnErrorSpec = list[ExceptionMatcher] | ErrorHandlingConfig | None


# =============================================================================
# Factory functions for common retry policies
# =============================================================================


def retry_transient(
    max_attempts: int = 3,
    backoff: str = "exponential",
) -> list[ExceptionMatcher]:
    """Retry transient network errors (ConnectionError, TimeoutError, OSError).

    Parameters
    ----------
    max_attempts : int
        Maximum number of attempts (default: 3)
    backoff : str
        Backoff strategy: "exponential" (default), "fixed", or "linear"

    Returns
    -------
    list[ExceptionMatcher]
        Matcher list for use with on_error parameter

    Examples
    --------

        @udf(data_type=pa.int32(), on_error=retry_transient())
        @udf(data_type=pa.int32(), on_error=retry_transient(max_attempts=5))
    """
    return [
        Retry(
            ConnectionError,
            TimeoutError,
            OSError,
            max_attempts=max_attempts,
            backoff=backoff,
        )
    ]


def retry_all(
    max_attempts: int = 3,
    backoff: str = "exponential",
) -> list[ExceptionMatcher]:
    """Retry any exception.

    Parameters
    ----------
    max_attempts : int
        Maximum number of attempts (default: 3)
    backoff : str
        Backoff strategy: "exponential" (default), "fixed", or "linear"

    Returns
    -------
    list[ExceptionMatcher]
        Matcher list for use with on_error parameter

    Examples
    --------

        @udf(data_type=pa.int32(), on_error=retry_all())
        @udf(data_type=pa.int32(), on_error=retry_all(max_attempts=5))
    """
    return [Retry(Exception, max_attempts=max_attempts, backoff=backoff)]


def skip_on_error(
    max_skip_count: int | None = None,
    max_skip_fraction: float | None = None,
) -> list[ExceptionMatcher]:
    """Skip (return None) for any exception.

    Parameters
    ----------
    max_skip_count : int, optional
        Maximum number of rows that can be skipped before the job fails.
        If both ``max_skip_count`` and ``max_skip_fraction`` are set,
        whichever threshold is hit first triggers failure.
    max_skip_fraction : float, optional
        Maximum fraction of rows (0.0-1.0) that can be skipped before the
        job fails. The fraction is computed as
        ``skipped / total_processed_so_far``.

    Returns
    -------
    list[ExceptionMatcher]
        Matcher list for use with on_error parameter

    Examples
    --------

        @udf(data_type=pa.int32(), on_error=skip_on_error())
        @udf(data_type=pa.int32(), on_error=skip_on_error(max_skip_count=100))
        @udf(data_type=pa.int32(), on_error=skip_on_error(max_skip_fraction=0.05))
        @udf(
            data_type=pa.int32(),
            on_error=skip_on_error(max_skip_count=100, max_skip_fraction=0.05),
        )
    """
    return [
        Skip(
            Exception,
            max_skip_count=max_skip_count,
            max_skip_fraction=max_skip_fraction,
        )
    ]


def fail_fast() -> list[ExceptionMatcher]:
    """Fail immediately on any exception (default behavior).

    Returns
    -------
    list[ExceptionMatcher]
        Empty matcher list (no special handling)

    Examples
    --------

        @udf(data_type=pa.int32(), on_error=fail_fast())
    """
    return []


class _PerExceptionWait(wait_base):
    """Custom wait strategy that uses different backoff per exception type.

    This allows different Retry matchers to have different backoff strategies.
    For example:
        Retry(ConnectionError, backoff="exponential")
        Retry(RateLimitError, backoff="fixed")

    The wait strategy looks up which Retry matcher matches the exception and
    uses that matcher's backoff strategy.
    """

    def __init__(self, retry_matchers: list["Retry"]) -> None:
        self.retry_matchers = retry_matchers
        # Build per-exception wait strategies
        self._wait_strategies: dict[type[Exception], wait_base] = {}
        for matcher in retry_matchers:
            wait_strategy = _build_wait_strategy_for_backoff(matcher.backoff)
            for exc_type in matcher.exceptions:
                self._wait_strategies[exc_type] = wait_strategy
        # Default fallback
        self._default_wait = wait_random_exponential(min=1, max=60)

    def __call__(self, retry_state: RetryCallState) -> float:
        """Return wait time based on the exception that was raised."""
        exc = retry_state.outcome.exception() if retry_state.outcome else None
        if exc is not None:
            # Find the matching wait strategy for this exception
            for exc_type, wait_strategy in self._wait_strategies.items():
                if isinstance(exc, exc_type):
                    return wait_strategy(retry_state)
        return self._default_wait(retry_state)


class _PerExceptionStop(stop_base):
    """Custom stop strategy that uses different max_attempts per exception type.

    This allows different Retry matchers to have different retry limits.
    For example:
        Retry(ConnectionError, max_attempts=3)
        Retry(RateLimitError, max_attempts=10)

    The stop strategy looks up which Retry matcher matches the exception and
    checks against that matcher's max_attempts.
    """

    def __init__(self, retry_matchers: list["Retry"]) -> None:
        self.retry_matchers = retry_matchers
        # Build per-exception max attempts
        self._max_attempts: dict[type[Exception], int] = {}
        for matcher in retry_matchers:
            for exc_type in matcher.exceptions:
                # If same exception in multiple matchers, use the max
                existing = self._max_attempts.get(exc_type, 0)
                self._max_attempts[exc_type] = max(existing, matcher.max_attempts)
        # Default fallback (overall max)
        self._default_max = max(m.max_attempts for m in retry_matchers)
        # Track attempts per exception type
        self._attempt_counts: dict[type[Exception], int] = {}

    @property
    def max_attempt_number(self) -> int:
        """Return the maximum attempts across all exception types.

        This property maintains backwards compatibility with code that
        expects stop_after_attempt semantics.
        """
        return self._default_max

    def __call__(self, retry_state: RetryCallState) -> bool:
        """Return True if we should stop retrying."""
        exc = retry_state.outcome.exception() if retry_state.outcome else None
        current_attempt = retry_state.attempt_number

        if exc is not None:
            # Find the max_attempts for this specific exception
            for exc_type, max_attempts in self._max_attempts.items():
                if isinstance(exc, exc_type):
                    return current_attempt >= max_attempts

        # Fallback to overall max
        return current_attempt >= self._default_max


def _build_wait_strategy_for_backoff(backoff: str) -> wait_base:
    """Build tenacity wait strategy from backoff string (internal helper)."""
    if backoff == "exponential":
        return wait_random_exponential(min=1, max=60)
    elif backoff == "fixed":
        return wait_fixed(1)
    elif backoff == "linear":
        return wait_exponential(multiplier=1, min=1, max=60, exp_base=1)
    else:
        raise ValueError(
            f"Unknown backoff strategy: {backoff}. "
            "Use 'exponential', 'fixed', or 'linear'"
        )


def _build_per_exception_retry_config(
    retry_matchers: list["Retry"],
) -> "UDFRetryConfig":
    """Build retry config with per-exception wait and stop strategies.

    This creates a UDFRetryConfig that supports different backoff strategies
    and max_attempts for different exception types by using custom tenacity
    strategies that dispatch based on the exception.
    """
    # Collect all exception types
    all_exceptions: set[type[Exception]] = set()
    for matcher in retry_matchers:
        all_exceptions.update(matcher.exceptions)

    return UDFRetryConfig(
        retry=retry_if_exception_type(tuple(all_exceptions)),
        stop=_PerExceptionStop(retry_matchers),
        wait=_PerExceptionWait(retry_matchers),
    )


def _build_wait_strategy(backoff: str) -> wait_base:
    """Build tenacity wait strategy from backoff string"""
    if backoff == "exponential":
        # Use random exponential for jitter to avoid thundering herd
        return wait_random_exponential(min=1, max=60)
    elif backoff == "fixed":
        return wait_fixed(1)
    elif backoff == "linear":
        # Linear backoff: 1s, 2s, 3s, 4s... capped at 60s
        return wait_exponential(multiplier=1, min=1, max=60, exp_base=1)
    else:
        raise ValueError(
            f"Unknown backoff strategy: {backoff}. "
            "Use 'exponential', 'fixed', or 'linear'"
        )


def resolve_on_error(on_error: OnErrorSpec) -> ErrorHandlingConfig:
    """Convert on_error spec to ErrorHandlingConfig

    Parameters
    ----------
    on_error : list[ExceptionMatcher] | ErrorHandlingConfig | None
        - None: Default fail-fast behavior
        - list: List of Retry, Skip, Fail matchers (or from factory functions)
        - ErrorHandlingConfig: Already resolved config (passed through)

    Returns
    -------
    ErrorHandlingConfig
        Configured error handling
    """
    if on_error is None:
        return ErrorHandlingConfig()  # Default: fail fast

    # If already an ErrorHandlingConfig, pass through
    if isinstance(on_error, ErrorHandlingConfig):
        return on_error

    # Otherwise it's a list of matchers
    return _build_error_config(on_error)


def _build_error_config(matchers: list[ExceptionMatcher]) -> ErrorHandlingConfig:
    """Convert matcher list to ErrorHandlingConfig

    This function translates the high-level on_error matchers into the
    lower-level tenacity-based ErrorHandlingConfig.
    """
    if not matchers:
        return ErrorHandlingConfig()  # No matchers = fail fast

    # Collect retry matchers and check for Skip matchers
    retry_matchers = [m for m in matchers if isinstance(m, Retry)]
    skip_matchers = [m for m in matchers if isinstance(m, Skip)]
    has_skip = len(skip_matchers) > 0

    # Build retry config
    if retry_matchers:
        # Use per-exception retry logic
        retry_config = _build_per_exception_retry_config(retry_matchers)
    else:
        retry_config = UDFRetryConfig.no_retry()

    # Determine fault isolation
    fault_isolation = (
        FaultIsolation.SKIP_ROWS if has_skip else FaultIsolation.FAIL_BATCH
    )

    # Extract skip thresholds from Skip matchers (use first one with values)
    max_skip_count = None
    max_skip_fraction = None
    for skip_matcher in skip_matchers:
        if skip_matcher.max_skip_count is not None and max_skip_count is None:
            max_skip_count = skip_matcher.max_skip_count
        if skip_matcher.max_skip_fraction is not None and max_skip_fraction is None:
            max_skip_fraction = skip_matcher.max_skip_fraction

    return ErrorHandlingConfig(
        retry_config=retry_config,
        fault_isolation=fault_isolation,
        log_errors=True,
        max_skip_count=max_skip_count,
        max_skip_fraction=max_skip_fraction,
        _matchers=matchers,
    )


def get_exception_outcome(exc: Exception, config: ErrorHandlingConfig) -> Outcome:
    """Determine the outcome for an exception based on matchers

    Parameters
    ----------
    exc : Exception
        The exception that occurred
    config : ErrorHandlingConfig
        The error handling configuration (may have _matchers attached)

    Returns
    -------
    Outcome
        RETRY, SKIP, or FAIL
    """
    matchers = getattr(config, "_matchers", None)
    if not matchers:
        return Outcome.FAIL  # Default: fail

    for matcher in matchers:
        if matcher.matches(exc):
            if isinstance(matcher, Retry):
                return Outcome.RETRY
            elif isinstance(matcher, Skip):
                return Outcome.SKIP
            elif isinstance(matcher, Fail):
                return Outcome.FAIL

    # No match = fail job (default)
    return Outcome.FAIL


@attrs.define(kw_only=True)
class ErrorRecord:
    """UDF execution error record, stored in geneva_errors table"""

    # Unique error ID
    error_id: str = attrs.field(factory=lambda: str(uuid.uuid4()))

    # Error details
    error_type: str = attrs.field()  # Exception.__class__.__name__
    error_message: str = attrs.field()
    error_trace: str = attrs.field()  # Full traceback

    # Job/Table context
    job_id: str = attrs.field()
    table_uri: str = attrs.field()  # Full URI to the table
    table_name: str = attrs.field()
    table_version: Optional[int] = attrs.field(default=None)  # Read version
    column_name: str = attrs.field()

    # UDF context
    udf_name: str = attrs.field()
    udf_version: str = attrs.field()
    input_columns: Optional[list[str]] = attrs.field(
        default=None,
        metadata={"pa_type": pa.list_(pa.string())},
    )
    output_columns: Optional[list[str]] = attrs.field(
        default=None,
        metadata={"pa_type": pa.list_(pa.string())},
    )

    # Execution context (Ray/distributed)
    actor_id: Optional[str] = attrs.field(default=None)
    fragment_id: Optional[int] = attrs.field(default=None)
    batch_index: int = attrs.field()  # Sequence number within fragment

    # Row-level granularity (for scalar UDFs)
    row_address: Optional[int] = attrs.field(default=None)

    # Retry context
    attempt: int = attrs.field(default=1)
    max_attempts: int = attrs.field(default=1)
    # Bisect depth at the point this row was finally isolated and null-checkpointed
    # by FaultIsolation.SKIP_ROWS. ``None`` for errors that did not go through the
    # task-bisect path (e.g. per-row scalar UDF exceptions caught inside the
    # applier).
    bisect_depth: Optional[int] = attrs.field(default=None)

    # Timestamp
    timestamp: datetime = attrs.field(
        factory=dt_now_utc, metadata={"pa_type": pa.timestamp("us", tz="UTC")}
    )


class ErrorStore(BaseManager):
    """Store and query error records in a Lance table"""

    def get_model(self) -> Any:
        return ErrorRecord(
            error_type="InitError",
            error_message="init",
            error_trace="",
            job_id="init",
            table_uri="init",
            table_name="init",
            column_name="init",
            udf_name="init",
            udf_version="init",
            batch_index=0,
            table_version=0,
        )

    def get_table_name(self) -> str:
        return GENEVA_ERRORS_TABLE_NAME

    @retry_lance
    def log_error(self, error: ErrorRecord) -> None:
        """Log an error record to the error table

        Parameters
        ----------
        error : ErrorRecord
            The error record to log
        """
        self.get_table().add([attrs.asdict(error)])
        _LOG.info(
            f"Logged error {error.error_id}: {error.error_type} in "
            f"{error.table_name}.{error.column_name} (attempt {error.attempt})"
        )

    @retry_lance
    def log_errors(self, errors: list[ErrorRecord]) -> None:
        """Log multiple error records to the error table in a single operation

        Parameters
        ----------
        errors : list[ErrorRecord]
            The error records to log
        """
        if not errors:
            return

        self.get_table().add([attrs.asdict(error) for error in errors])
        _LOG.info(f"Logged {len(errors)} errors in bulk")

    def get_errors(
        self,
        job_id: str | None = None,
        table_name: str | None = None,
        column_name: str | None = None,
        error_type: str | None = None,
    ) -> list[ErrorRecord]:
        """Query error records with optional filters

        Parameters
        ----------
        job_id : str, optional
            Filter by job ID
        table_name : str, optional
            Filter by table name
        column_name : str, optional
            Filter by column name
        error_type : str, optional
            Filter by error type (exception class name)

        Returns
        -------
        list[ErrorRecord]
            List of matching error records
        """
        wheres = []
        if job_id:
            wheres.append(f"job_id = '{escape_sql_string(job_id)}'")
        if table_name:
            wheres.append(f"table_name = '{escape_sql_string(table_name)}'")
        if column_name:
            wheres.append(f"column_name = '{escape_sql_string(column_name)}'")
        if error_type:
            wheres.append(f"error_type = '{escape_sql_string(error_type)}'")

        query = self.get_table(True).search()
        if wheres:
            query = query.where(" and ".join(wheres))

        # Only select known fields for forward compatibility
        known_fields = [f.name for f in attrs.fields(ErrorRecord)]
        results = query.select(known_fields).to_arrow().to_pylist()

        return [self._safe_error_record(rec) for rec in results]

    def _safe_error_record(self, rec_dict: dict) -> ErrorRecord:
        """Create ErrorRecord from dict, ignoring unknown fields"""
        known_fields = {f.name for f in attrs.fields(ErrorRecord)}
        filtered = {k: v for k, v in rec_dict.items() if k in known_fields}
        return ErrorRecord(**filtered)

    def get_failed_row_addresses(self, job_id: str, column_name: str) -> list[int]:
        """Get row addresses for all failed rows in a job

        Parameters
        ----------
        job_id : str
            Job ID to query
        column_name : str
            Column name to filter by

        Returns
        -------
        list[int]
            List of row addresses that failed
        """
        errors = self.get_errors(job_id=job_id, column_name=column_name)
        row_addresses = [
            err.row_address for err in errors if err.row_address is not None
        ]
        return row_addresses


def make_error_record_from_exception(
    exception: Exception,
    *,
    job_id: str,
    table_uri: str,
    table_name: str,
    table_version: int | None,
    column_name: str,
    udf_name: str,
    udf_version: str,
    batch_index: int,
    input_columns: list[str] | None = None,
    output_columns: list[str] | None = None,
    fragment_id: int | None = None,
    actor_id: str | None = None,
    row_address: int | None = None,
    attempt: int = 1,
    max_attempts: int = 1,
    bisect_depth: int | None = None,
) -> ErrorRecord:
    """Factory function to create an ErrorRecord from an exception

    Parameters
    ----------
    exception : Exception
        The exception that occurred
    job_id : str
        Job ID
    table_uri : str
        URI of the table being processed
    table_name : str
        Name of the table
    table_version : int | None
        Version of the table being read
    column_name : str
        Column being computed
    udf_name : str
        Name of the UDF
    udf_version : str
        Version of the UDF
    input_columns : list[str] | None, optional
        Canonical source field paths used by the UDF
    output_columns : list[str] | None, optional
        Output field paths produced by the UDF
    batch_index : int
        Batch sequence number
    fragment_id : int | None, optional
        Fragment ID if applicable
    actor_id : str | None, optional
        Ray actor ID if applicable
    row_address : int | None, optional
        Row address for row-level errors
    attempt : int, optional
        Current retry attempt number
    max_attempts : int, optional
        Maximum retry attempts
    bisect_depth : int | None, optional
        Bisect depth at which the error was recorded (0 = original
        task, >0 = nested split from the bisect-and-skip path);
        ``None`` if bisect did not engage.

    Returns
    -------
    ErrorRecord
        The constructed error record
    """
    return ErrorRecord(
        error_type=type(exception).__name__,
        error_message=str(exception),
        error_trace=traceback.format_exc(),
        job_id=job_id,
        table_uri=table_uri,
        table_name=table_name,
        table_version=table_version,
        column_name=column_name,
        udf_name=udf_name,
        udf_version=udf_version,
        input_columns=input_columns,
        output_columns=output_columns,
        actor_id=actor_id,
        fragment_id=fragment_id,
        batch_index=batch_index,
        row_address=row_address,
        attempt=attempt,
        max_attempts=max_attempts,
        bisect_depth=bisect_depth,
    )
