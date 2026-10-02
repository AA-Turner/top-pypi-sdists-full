# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class BenchmarkTaskDiffResponse(BaseModel):
  bench_id: str

  new: list[str]

  present: list[str]

  updated: list[str]

  task_count: int
