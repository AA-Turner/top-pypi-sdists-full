# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime

from trajectory._models import BaseModel


class BenchmarkListItem(BaseModel):
  bench_id: str

  agent_id: str | None = None

  organization_id: str

  name: str

  description: str = ""

  visibility: str = "private"

  family: str | None = None

  created_at: datetime

  updated_at: datetime

  eval_run_count: int = 0
