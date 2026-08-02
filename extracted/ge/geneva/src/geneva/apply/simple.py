# ruff: noqa: PERF203

# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# super simple applier

import logging
import time
from collections.abc import Iterator

import attrs
import pyarrow as pa

from geneva.apply.applier import BatchApplier
from geneva.apply.error_handling import (
    BatchStrategy,
    ErrorHandlingContext,
    get_error_handling_config,
    make_skip_budget_tracker,
)
from geneva.apply.memory import (
    get_applier_memory_trim_interval,
    release_unused_process_memory,
)
from geneva.apply.task import MapTask, ReadTask
from geneva.apply.utils import _iter_with_next_duration
from geneva.debug.logger import ErrorLogger

_LOG = logging.getLogger(__name__)


@attrs.define
class SimpleApplier(BatchApplier):
    """
    A simple applier that applies a function to each element in the batch.
    """

    job_id: str = attrs.field(default="unknown")
    enforce_skip_threshold: bool = attrs.field(default=True)
    udf_processing_time_ms: int = attrs.field(default=0, init=False)
    read_io_time_ms: int = attrs.field(default=0, init=False)
    skip_count: int = attrs.field(default=0, init=False)
    total_rows: int = attrs.field(default=0, init=False)

    def reset_run_state(self) -> None:
        self.udf_processing_time_ms = 0
        self.read_io_time_ms = 0
        self.skip_count = 0
        self.total_rows = 0

    def run(
        self,
        read_task: ReadTask,
        map_task: MapTask,
        error_logger: ErrorLogger,
    ) -> Iterator[pa.RecordBatch]:
        self.reset_run_state()
        error_config = get_error_handling_config(map_task)
        skip_tracker = (
            make_skip_budget_tracker(error_config)
            if self.enforce_skip_threshold
            else None
        )
        batch_iter = read_task.to_batches(batch_size=map_task.batch_size())
        memory_trim_interval = get_applier_memory_trim_interval()
        for completed_batches, (read_ms, batch) in enumerate(
            _iter_with_next_duration(iter(batch_iter)),
            start=1,
        ):
            seq = completed_batches - 1
            self.read_io_time_ms += read_ms
            # Create error context and strategy for this batch
            ctx = ErrorHandlingContext.create(map_task, read_task, self.job_id, seq)
            strategy = BatchStrategy.from_context(ctx, map_task, error_logger)

            # Apply strategy - no branching needed!
            start = time.perf_counter()
            result_batch, error_records, skip_count = strategy.apply(batch)
            self.udf_processing_time_ms += int((time.perf_counter() - start) * 1000)

            # Log errors if any were collected
            if error_records:
                error_logger.log_errors(error_records)

            # Track skip counts
            batch_rows = (
                batch.num_rows if isinstance(batch, pa.RecordBatch) else len(batch)
            )
            self.total_rows += batch_rows
            self.skip_count += skip_count

            # Enforce per-job skip threshold
            if skip_tracker is not None and batch_rows > 0:
                skip_tracker.record_batch(batch_rows, skip_count)

            yield result_batch
            if (
                memory_trim_interval > 0
                and completed_batches % memory_trim_interval == 0
            ):
                release_unused_process_memory()
