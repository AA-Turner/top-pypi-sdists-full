# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class BenchmarkTaskCountResponse(BaseModel):
  bench_id: str

  task_count: int
  """
    Tasks matching the filters. With `search`, counting stops at 1000; a smaller value is
    exact.
    """
