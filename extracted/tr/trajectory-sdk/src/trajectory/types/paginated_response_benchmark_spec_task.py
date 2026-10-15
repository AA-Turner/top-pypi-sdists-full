# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory.types.benchmarks.tasks.benchmark_spec_task import BenchmarkSpecTask


class PaginatedResponseBenchmarkSpecTask(SyncPage[BenchmarkSpecTask]):
  items: list[BenchmarkSpecTask]

  next_cursor: str | None = None

  has_more: bool
