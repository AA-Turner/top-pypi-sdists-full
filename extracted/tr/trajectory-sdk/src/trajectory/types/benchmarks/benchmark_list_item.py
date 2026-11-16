# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime

from trajectory._models import BaseModel
from trajectory.types.benchmark_type import BenchmarkType


class BenchmarkListItem(BaseModel):
  bench_id: str

  benchmark_type: BenchmarkType = "generative"

  agent_id: str | None = None

  organization_id: str

  name: str

  description: str = ""

  visibility: str = "private"

  created_at: datetime

  updated_at: datetime

  eval_run_count: int = 0
