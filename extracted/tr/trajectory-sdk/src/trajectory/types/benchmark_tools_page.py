# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory.types.benchmark_spec_tool import BenchmarkSpecTool


class BenchmarkToolsPage(SyncPage[BenchmarkSpecTool]):
  items: list[BenchmarkSpecTool]

  next_cursor: str | None = None

  has_more: bool

  bench_id: str
  """Benchmark whose bound tools are returned."""
