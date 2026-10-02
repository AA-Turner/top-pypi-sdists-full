# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel
from trajectory.types.benchmarks.ingestion.benchmark_ingestion_failure import (
  BenchmarkIngestionFailure,
)


class BenchmarkIngestionOperationStatus(BaseModel):
  operation_id: str

  bench_id: str

  status: Literal[
    "uploading", "queued", "running", "cancelled", "succeeded", "partial_failure", "failed"
  ]

  stage: Literal["verifying", "registering", "building"]

  attempt: int

  max_attempts: int

  last_error: BenchmarkIngestionFailure | None = None

  task_count: int = 0

  added_count: int = 0

  updated_count: int = 0

  skipped_count: int = 0

  registered_tasks: int = 0

  total_tasks: int = 0

  ready_runtimes: int = 0

  total_runtimes: int = 0

  failure_count: int = 0

  build_images: bool

  ready: bool = False
