# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.benchmark_task_write_failure import BenchmarkTaskWriteFailure


class IngestBenchmarkResponse(BaseModel):
  bench_id: str

  name: str

  family: str | None = None

  task_count: int

  failed_tasks: list[BenchmarkTaskWriteFailure] | None = None

  warnings: list[str] | None = None
  """Provider resource adjustments made before ingestion."""
