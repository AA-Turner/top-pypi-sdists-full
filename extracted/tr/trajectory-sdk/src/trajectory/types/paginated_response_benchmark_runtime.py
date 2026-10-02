# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.benchmark_runtime import BenchmarkRuntime


class PaginatedResponseBenchmarkRuntime(BaseModel):
  items: list[BenchmarkRuntime]

  next_cursor: str | None = None

  has_more: bool
