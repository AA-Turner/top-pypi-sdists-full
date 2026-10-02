# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.benchmark_runtime import BenchmarkRuntime
from trajectory.types.benchmarks.tasks.benchmark_spec_task import BenchmarkSpecTask


class BenchmarkSpecTool(BaseModel):
  tool_id: str

  name: str


class BenchmarkDetails(BaseModel):
  bench_id: str

  task_count: int

  tasks: list[BenchmarkSpecTask] | None = None

  tools: list[BenchmarkSpecTool] | None = None

  runtimes: list[BenchmarkRuntime] | None = None
