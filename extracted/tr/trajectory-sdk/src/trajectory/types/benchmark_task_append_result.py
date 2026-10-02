# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.benchmark_task_write_failure import BenchmarkTaskWriteFailure


class BenchmarkTaskAppendResult(BaseModel):
  bench_id: str

  batch_id: str

  added_count: int

  updated_count: int

  skipped_count: int

  task_count: int

  failed_tasks: list[BenchmarkTaskWriteFailure] | None = None
