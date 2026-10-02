# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class BenchmarkIngestionSession(BaseModel):
  session_id: str

  bench_id: str

  accepted: bool
