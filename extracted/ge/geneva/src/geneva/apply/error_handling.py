# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Error handling for batch processing.

This module provides:
- ErrorHandlingContext: Bundles job/task metadata for error logging
- BatchStrategy: Strategy pattern for different error handling behaviors
  - FailFastStrategy: No error handling, fail immediately
  - BatchRetryStrategy: Retry entire batch with tenacity
  - SkipRowsStrategy: Process rows individually, skip failures

All error handling logic is centralized here to eliminate branching in appliers.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any

import attrs
import pyarrow as pa
from tenacity import Retrying

from geneva.apply.task import BackfillUDFTask, CopyTableTask, MapTask, ReadTask
from geneva.debug.error_store import (
    ErrorHandlingConfig,
    FaultIsolation,
    SkipThresholdExceededError,
    make_error_record_from_exception,
)
from geneva.debug.logger import ErrorLogger
from geneva.transformer import BACKFILL_SELECTED
from geneva.utils import make_null_array

_LOG = logging.getLogger(__name__)


# =============================================================================
# Utility Functions
# =============================================================================


def get_max_attempts(retry_config) -> int:
    """Extract max attempts from retry config"""
    if hasattr(retry_config.stop, "max_attempt_number"):
        return retry_config.stop.max_attempt_number  # type: ignore[attr-defined]
    return 1


def build_retry_kwargs(retry_config, reraise: bool | None = None) -> dict:
    """Build tenacity Retrying kwargs from RetryConfig"""
    kwargs = {
        "retry": retry_config.retry,
        "stop": retry_config.stop,
        "wait": retry_config.wait,
        "reraise": reraise if reraise is not None else retry_config.reraise,
    }
    if retry_config.before_sleep is not None:
        kwargs["before_sleep"] = retry_config.before_sleep
    if retry_config.after_attempt is not None:
        kwargs["after"] = retry_config.after_attempt
    return kwargs


def extract_table_name(table_uri: str) -> str:
    """Extract table name from URI"""
    return table_uri.split("/")[-1].replace(".lance", "")


def get_error_handling_config(map_task: MapTask) -> ErrorHandlingConfig | None:
    """Extract error handling config from map task's UDF"""
    if isinstance(map_task, BackfillUDFTask):
        _, udf = next(iter(map_task.udfs.items()))
        if hasattr(udf, "error_handling"):
            return udf.error_handling
    return None


def _stable_udf_version(map_task: MapTask) -> str:
    """Return a stable identifier for logging (does not vary per batch)."""
    try:
        return map_task.checkpoint_prefix(
            dataset_uri="unknown",
            where=getattr(map_task, "where", None),
        )
    except Exception:
        try:
            return map_task.name()
        except Exception:
            return "unknown"


@attrs.define
class SkipBudgetTracker:
    """Tracks cumulative skip counts across batches for threshold enforcement.

    Lives in the main process (applier's ``run()`` loop), not inside
    per-batch strategies. This naturally handles both single-process and
    multiprocess appliers without shared memory.

    **Fraction is a rolling guardrail:** ``max_skip_fraction`` is evaluated
    incrementally after each batch as ``skipped / processed_so_far``, *not*
    as a final-aggregate check over the entire dataset. A batch with a high
    failure rate early in the job can trigger the threshold before later
    clean batches dilute the running average. This is intentional — it
    provides early termination for runaway failures.

    ``max_skip_count`` is monotonically increasing, so evaluation order does
    not affect its outcome.
    """

    max_skip_count: int | None = attrs.field(default=None)
    max_skip_fraction: float | None = attrs.field(default=None)
    _skipped: int = attrs.field(default=0, init=False)
    _processed: int = attrs.field(default=0, init=False)

    def record_batch(self, processed_count: int, skip_count: int) -> None:
        """Record results from a batch and check thresholds.

        Parameters
        ----------
        processed_count : int
            Total number of rows processed in the batch.
        skip_count : int
            Number of rows that were skipped (failed) in this batch.

        Raises
        ------
        SkipThresholdExceededError
            If cumulative skips exceed the configured threshold.
        """
        self._processed += processed_count
        self._skipped += skip_count
        self._check_threshold()

    def _check_threshold(self) -> None:
        count_exceeded = (
            self.max_skip_count is not None and self._skipped > self.max_skip_count
        )
        fraction_exceeded = (
            self.max_skip_fraction is not None
            and self._processed > 0
            and self._skipped / self._processed > self.max_skip_fraction
        )
        if count_exceeded or fraction_exceeded:
            raise SkipThresholdExceededError(
                skipped=self._skipped,
                processed=self._processed,
                max_count=self.max_skip_count,
                max_fraction=self.max_skip_fraction,
            )

    @property
    def skipped(self) -> int:
        return self._skipped

    @property
    def processed(self) -> int:
        return self._processed


def make_skip_budget_tracker(
    error_config: ErrorHandlingConfig | None,
) -> SkipBudgetTracker | None:
    """Create a SkipBudgetTracker if the config has skip thresholds.

    Returns None if no thresholds are configured (i.e. unlimited skipping).
    """
    if error_config is None:
        return None
    if error_config.fault_isolation != FaultIsolation.SKIP_ROWS:
        return None
    if error_config.max_skip_count is None and error_config.max_skip_fraction is None:
        return None
    return SkipBudgetTracker(
        max_skip_count=error_config.max_skip_count,
        max_skip_fraction=error_config.max_skip_fraction,
    )


def extract_context_from_task(read_task: ReadTask) -> dict:
    """Extract table context from read task for error logging"""
    context: dict = {}
    try:
        context["table_uri"] = read_task.table_uri()
    except Exception:
        if hasattr(read_task, "uri"):
            context["table_uri"] = read_task.uri  # type: ignore[attr-defined]
    if hasattr(read_task, "version"):
        context["table_version"] = read_task.version  # type: ignore[attr-defined]
    if hasattr(read_task, "frag_id"):
        context["fragment_id"] = read_task.frag_id  # type: ignore[attr-defined]
    return context


def _audit_output_columns(map_task: MapTask) -> list[str] | None:
    """Return user-visible output columns for error audit records."""

    if isinstance(map_task, BackfillUDFTask):
        try:
            col_name = next(iter(map_task.udfs))
            return map_task._output_column_names(col_name)
        except Exception:
            return None
    if isinstance(map_task, CopyTableTask):
        outputs = [transform.output_name for transform in map_task.column_udfs]
        return outputs or None

    try:
        output_columns = list(map_task.output_schema().names)
    except Exception:
        return None
    output_columns = [name for name in output_columns if name != "_rowaddr"]
    return output_columns or None


# =============================================================================
# Error Handling Context
# =============================================================================


@attrs.define
class ErrorHandlingContext:
    """Bundles common error handling parameters to reduce repetition"""

    job_id: str
    task_context: dict  # table_uri, version, fragment_id
    seq: int
    udf_name: str
    udf_version: str
    input_columns: list[str] | None = None
    output_columns: list[str] | None = None
    error_config: ErrorHandlingConfig | None = None

    @classmethod
    def create(
        cls,
        map_task: MapTask,
        read_task: ReadTask,
        job_id: str,
        seq: int,
    ) -> "ErrorHandlingContext":
        """Create error handling context from tasks

        Parameters
        ----------
            map_task
                The map task being executed
            read_task
                The read task providing data
            job_id
                Job identifier
            seq
                Batch sequence number

        Returns
        -------
            ErrorHandlingContext configured for the given tasks
        """
        error_config = get_error_handling_config(map_task)

        if error_config:
            error_config.validate_compatibility(map_task)

        task_context = extract_context_from_task(read_task)

        # Extract UDF info directly from map_task methods
        udf_name = map_task.name() if hasattr(map_task, "name") else "unknown"
        dataset_uri = task_context.get("table_uri", "unknown")
        where = getattr(map_task, "where", None)
        try:
            udf_version = map_task.checkpoint_prefix(
                dataset_uri=dataset_uri,
                where=where,
            )
        except Exception:
            udf_version = _stable_udf_version(map_task)
        try:
            input_columns = map_task.input_columns()
        except Exception:
            input_columns = None
        output_columns = _audit_output_columns(map_task)

        return cls(
            job_id=job_id,
            task_context=task_context,
            seq=seq,
            udf_name=udf_name,
            udf_version=udf_version,
            input_columns=input_columns,
            output_columns=output_columns,
            error_config=error_config,
        )

    def create_error_record(
        self,
        exception: Exception,
        row_address: int | None,
        attempt: int,
        max_attempts: int,
        bisect_depth: int | None = None,
    ) -> Any:
        """Create error record with this context"""
        table_uri = self.task_context.get("table_uri", "unknown")
        return make_error_record_from_exception(
            exception=exception,
            job_id=self.job_id,
            table_uri=table_uri,
            table_name=extract_table_name(table_uri),
            table_version=self.task_context.get("table_version"),
            column_name=self.udf_name,
            udf_name=self.udf_name,
            udf_version=self.udf_version,
            input_columns=self.input_columns,
            output_columns=self.output_columns,
            batch_index=self.seq,
            fragment_id=self.task_context.get("fragment_id"),
            row_address=row_address,
            attempt=attempt,
            max_attempts=max_attempts,
            bisect_depth=bisect_depth,
        )


# =============================================================================
# Batch Processing Strategies
# =============================================================================


class BatchStrategy(ABC):
    """Base class for batch processing strategies with error handling"""

    def __init__(
        self,
        ctx: ErrorHandlingContext,
        map_task: MapTask,
        error_logger: ErrorLogger | None = None,
    ) -> None:
        """
        Parameters
        ----------
            ctx
                Error handling context with job/task metadata
            map_task
                The task to apply to batches
            error_logger
                Optional logger for errors (None in worker processes)
        """
        self.ctx = ctx
        self.map_task = map_task
        self.error_logger = error_logger

    @classmethod
    def from_context(
        cls,
        ctx: ErrorHandlingContext,
        map_task: MapTask,
        error_logger: ErrorLogger | None = None,
    ) -> "BatchStrategy":
        """Factory method to create appropriate strategy based on context

        Parameters
        ----------
            ctx
                Error handling context
            map_task
                The task to apply
            error_logger
                Optional error logger

        Returns
        -------
            Appropriate strategy instance
        """
        if not ctx.error_config:
            return FailFastStrategy(ctx, map_task, error_logger)

        if ctx.error_config.fault_isolation == FaultIsolation.SKIP_ROWS:
            return SkipRowsStrategy(ctx, map_task, error_logger)

        if ctx.error_config.retry_config:
            return BatchRetryStrategy(ctx, map_task, error_logger)

        return FailFastStrategy(ctx, map_task, error_logger)

    @abstractmethod
    def apply(self, batch: pa.RecordBatch) -> tuple[pa.RecordBatch, list[Any], int]:
        """Apply the strategy to a batch

        Returns
        -------
            (result_batch, error_records, skip_count) - error_records may be
            empty, skip_count tracks actual skips independently of log_errors.
        """


class FailFastStrategy(BatchStrategy):
    """No error handling - fail immediately on any error"""

    def apply(self, batch: pa.RecordBatch) -> tuple[pa.RecordBatch, list[Any], int]:
        """Apply without error handling, fail on first error"""
        try:
            result = self.map_task.apply(batch)
            return (result, [], 0)
        except Exception as e:
            # Log error if error_logger is provided (either explicitly configured
            # via error_config.log_errors or just passed in)
            if self.error_logger and (
                not self.ctx.error_config or self.ctx.error_config.log_errors
            ):
                error_record = self.ctx.create_error_record(
                    exception=e,
                    row_address=None,
                    attempt=1,
                    max_attempts=1,
                )
                self.error_logger.log_error(error_record)
            raise


class BatchRetryStrategy(BatchStrategy):
    """Retry entire batch on failure, eventually fail the batch"""

    def apply(self, batch: pa.RecordBatch) -> tuple[pa.RecordBatch, list[Any], int]:
        """Apply with retry logic, fail batch if retries exhausted"""
        if not self.ctx.error_config or not self.ctx.error_config.retry_config:
            raise ValueError("BatchRetryStrategy requires retry_config")

        retry_config = self.ctx.error_config.retry_config
        retry_kwargs = build_retry_kwargs(retry_config)
        max_attempts = get_max_attempts(retry_config)

        for attempt in Retrying(**retry_kwargs):
            with attempt:
                try:
                    result = self.map_task.apply(batch)

                    # Log successful retry if configured
                    if (
                        self.ctx.error_config.log_retry_attempts
                        and attempt.retry_state.attempt_number > 1
                    ):
                        _LOG.info(
                            f"UDF {self.ctx.udf_name} succeeded on attempt "
                            f"{attempt.retry_state.attempt_number} "
                            f"for batch {self.ctx.seq}"
                        )

                    return (result, [], 0)

                except Exception as e:
                    self._log_retry_failure(
                        e, attempt.retry_state.attempt_number, max_attempts
                    )
                    raise

        raise RuntimeError("Retry loop exited unexpectedly")

    def _log_retry_failure(
        self, exception: Exception, current_attempt: int, max_attempts: int
    ) -> None:
        """Log retry failure with appropriate detail level"""
        should_log_to_store = (
            self.error_logger
            and self.ctx.error_config
            and self.ctx.error_config.log_errors
            and (
                self.ctx.error_config.log_retry_attempts
                or current_attempt >= max_attempts
            )
        )

        if should_log_to_store:
            error_record = self.ctx.create_error_record(
                exception=exception,
                row_address=None,
                attempt=current_attempt,
                max_attempts=max_attempts,
            )
            self.error_logger.log_error(error_record)  # type: ignore[union-attr]
        elif current_attempt > 1:
            # In worker process without logger, or not logging to store
            _LOG.warning(
                f"Retry attempt {current_attempt} failed "
                f"for batch {self.ctx.seq}: {exception}"
            )


class SkipRowsStrategy(BatchStrategy):
    """Apply the batch whole; on failure, bisect to isolate and skip the
    failing rows.

    A healthy batch is one vectorized ``map_task.apply``; one bad row costs
    O(log batch_size) re-executions. Rows co-batched with a failure re-execute
    on the successful halves -- UDFs are assumed idempotent, as with
    checkpoint resume.
    """

    def apply(self, batch: pa.RecordBatch) -> tuple[pa.RecordBatch, list[Any], int]:
        """Apply the batch whole; bisect only on failure."""
        if not isinstance(self.map_task, BackfillUDFTask):
            # Fall back to normal apply for non-UDF tasks
            return (self.map_task.apply(batch), [], 0)

        # Blob-encoded columns yield list[dict] instead of RecordBatch.
        # Delegate to the map_task which already handles both shapes.
        # TODO(#782): implement bisection for list[dict] to preserve
        #  SKIP_ROWS isolation semantics (whole-batch fallback).
        if isinstance(batch, list):
            return (self.map_task.apply(batch), [], 0)

        try:
            return (self.map_task.apply(batch), [], 0)
        except Exception as e:
            _LOG.warning(
                f"Batch {self.ctx.seq} ({len(batch)} rows) failed: {e}; "
                "bisecting to isolate the failing rows"
            )
            return self._apply_bisect(batch)

    def _apply_bisect(
        self, batch: pa.RecordBatch
    ) -> tuple[pa.RecordBatch, list[Any], int]:
        """Resolve segments left-to-right off a stack, seeded with the failed
        batch's halves: failing multi-row segments split in half; a failing
        single row becomes an all-null row (retry + error record first).

        Segment results are concatenated as-is, so multi-column (unpacked)
        outputs and sparse results (``defer_carry_forward`` emits only
        WHERE-matched rows) pass through unchanged.
        """
        assert isinstance(self.map_task, BackfillUDFTask)  # guaranteed by apply()
        col_name, udf = next(iter(self.map_task.udfs.items()))
        output_schema = pa.schema(
            [
                *self.map_task._output_fields(col_name, udf),
                pa.field("_rowaddr", pa.uint64()),
            ]
        )

        # Unmatched rows are absent from sparse output; skip their leaves.
        sparse_mask = None
        if (
            self.map_task.defer_carry_forward
            and BACKFILL_SELECTED in batch.schema.names
        ):
            sparse_mask = batch[BACKFILL_SELECTED].to_pylist()

        pieces: list[pa.RecordBatch] = []
        error_records: list[Any] = []
        skip_count = 0

        # Seed with the halves: apply() already saw the full batch fail.
        n = len(batch)
        half = n // 2
        if n > 1:
            # (offset, length); right pushed first so left resolves first
            stack: list[tuple[int, int]] = [(half, n - half), (0, half)]
        else:
            stack = [(0, 1)] if n == 1 else []
        while stack:
            offset, length = stack.pop()
            segment = batch.slice(offset, length)

            if length > 1:
                try:
                    pieces.append(self.map_task.apply(segment))
                except Exception:
                    half = length // 2
                    stack.append((offset + half, length - half))
                    stack.append((offset, half))
                continue

            row_address_value = batch["_rowaddr"][offset].as_py()
            if row_address_value is None:
                _LOG.warning(f"Row {offset} has null _rowaddr, skipping")
                pieces.append(self._null_row(output_schema, None))
                skip_count += 1
                continue
            if sparse_mask is not None and not sparse_mask[offset]:
                continue

            piece, error_record, failed = self._process_row(
                segment, int(row_address_value), output_schema
            )
            pieces.append(piece)
            if error_record is not None:
                error_records.append(error_record)
            if failed:
                skip_count += 1

        table = (
            pa.Table.from_batches(pieces, schema=output_schema)
            if pieces
            else output_schema.empty_table()
        )
        batches = table.combine_chunks().to_batches()
        result_batch = (
            batches[0]
            if batches
            else pa.RecordBatch.from_pylist([], schema=output_schema)
        )

        return (result_batch, error_records, skip_count)

    @staticmethod
    def _null_row(output_schema: pa.Schema, row_address: int | None) -> pa.RecordBatch:
        """A one-row batch with every output column null (skipped row)."""
        arrays = [make_null_array(1, field.type) for field in list(output_schema)[:-1]]
        arrays.append(pa.array([row_address], type=pa.uint64()))
        return pa.record_batch(arrays, schema=output_schema)

    def _process_row(
        self,
        row_batch: pa.RecordBatch,
        row_address: int,
        output_schema: pa.Schema,
    ) -> tuple[pa.RecordBatch, Any, bool]:
        """Process a single row, with retry if configured; a row that still
        fails comes back as (all-null row, error record, failed=True)."""
        if self._should_retry():
            return self._process_row_with_retry(row_batch, row_address, output_schema)
        else:
            return self._process_row_once(row_batch, row_address, output_schema)

    def _should_retry(self) -> bool:
        """Check if row-level retry is configured"""
        if not self.ctx.error_config or not self.ctx.error_config.retry_config:
            return False
        max_attempts = get_max_attempts(self.ctx.error_config.retry_config)
        return max_attempts > 1

    def _process_row_once(
        self,
        row_batch: pa.RecordBatch,
        row_address: int,
        output_schema: pa.Schema,
    ) -> tuple[pa.RecordBatch, Any, bool]:
        """Process row without retry"""
        try:
            return (self.map_task.apply(row_batch), None, False)
        except Exception as e:
            error_record = None
            if self.ctx.error_config and self.ctx.error_config.log_errors:
                error_record = self.ctx.create_error_record(
                    exception=e,
                    row_address=row_address,
                    attempt=1,
                    max_attempts=1,
                )

            _LOG.warning(
                f"Skipping row {row_address} in batch {self.ctx.seq} due to error: {e}"
            )
            return (self._null_row(output_schema, row_address), error_record, True)

    def _process_row_with_retry(
        self,
        row_batch: pa.RecordBatch,
        row_address: int,
        output_schema: pa.Schema,
    ) -> tuple[pa.RecordBatch, Any, bool]:
        """Process row with retry logic"""
        if not self.ctx.error_config or not self.ctx.error_config.retry_config:
            raise ValueError("_process_row_with_retry requires retry_config")

        retry_config = self.ctx.error_config.retry_config
        max_attempts = get_max_attempts(retry_config)
        retry_kwargs = build_retry_kwargs(retry_config, reraise=True)

        last_exception = None
        try:
            for attempt in Retrying(**retry_kwargs):
                with attempt:
                    try:
                        result_batch = self.map_task.apply(row_batch)

                        # Log successful retry if configured
                        if (
                            self.ctx.error_config.log_retry_attempts
                            and attempt.retry_state.attempt_number > 1
                        ):
                            _LOG.info(
                                f"UDF {self.ctx.udf_name} succeeded on attempt "
                                f"{attempt.retry_state.attempt_number} "
                                f"for row {row_address}"
                            )

                        return (result_batch, None, False)

                    except Exception as e:
                        last_exception = e
                        if attempt.retry_state.attempt_number > 1:
                            _LOG.warning(
                                f"Retry attempt {attempt.retry_state.attempt_number} "
                                f"failed for row {row_address}: {e}"
                            )
                        raise

        except Exception:
            # Retries exhausted - skip this row
            _LOG.warning(
                f"Skipping row {row_address} in batch {self.ctx.seq} after "
                f"{max_attempts} attempts due to error: {last_exception}"
            )

            error_record = None
            if self.ctx.error_config.log_errors and last_exception:
                error_record = self.ctx.create_error_record(
                    exception=last_exception,
                    row_address=row_address,
                    attempt=max_attempts,
                    max_attempts=max_attempts,
                )

            return (self._null_row(output_schema, row_address), error_record, True)

        # Unreachable with reraise=True; keep the schema-shaped fallback.
        return (self._null_row(output_schema, row_address), None, True)
