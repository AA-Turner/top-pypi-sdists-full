# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class DataQcFindingCount(BaseModel):
  bench_id: str

  task_id: str | None = None

  trajectory_id: str | None = None

  include_descendants: bool = False

  open_count: int

  resolved_count: int


class DataQcFindingCounts(BaseModel):
  data: list[DataQcFindingCount]
