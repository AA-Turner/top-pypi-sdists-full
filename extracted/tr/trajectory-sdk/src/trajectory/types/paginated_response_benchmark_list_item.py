# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory.types.benchmarks.benchmark_list_item import BenchmarkListItem


class PaginatedResponseBenchmarkListItem(SyncPage[BenchmarkListItem]):
  items: list[BenchmarkListItem]

  next_cursor: str | None = None

  has_more: bool
