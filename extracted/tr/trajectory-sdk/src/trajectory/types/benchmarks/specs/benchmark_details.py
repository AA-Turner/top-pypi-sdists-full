# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel
from trajectory.types.benchmark_runtime import BenchmarkRuntime
from trajectory.types.benchmark_spec_tool import BenchmarkSpecTool
from trajectory.types.benchmarks.tasks.benchmark_spec_task import BenchmarkSpecTask


class BenchmarkUploadProgress(BaseModel):
  status: Literal[
    "uploading", "queued", "running", "cancelled", "succeeded", "partial_failure", "failed"
  ]

  stage: Literal["verifying", "registering", "building"]

  registered_tasks: int = 0

  total_tasks: int = 0

  ready_runtimes: int = 0

  total_runtimes: int = 0

  failure_count: int = 0


class BenchmarkDetails(BaseModel):
  ingestion: BenchmarkUploadProgress | None = None

  bench_id: str

  task_count: int

  tasks: list[BenchmarkSpecTask] | None = None

  tools: list[BenchmarkSpecTool] | None = None

  runtimes: list[BenchmarkRuntime] | None = None
