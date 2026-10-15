# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory.types.benchmark_runtime import BenchmarkRuntime


class BenchmarkRuntimesPage(SyncPage[BenchmarkRuntime]):
  items: list[BenchmarkRuntime]

  next_cursor: str | None = None

  has_more: bool

  bench_id: str
  """Benchmark whose task runtimes are returned."""
