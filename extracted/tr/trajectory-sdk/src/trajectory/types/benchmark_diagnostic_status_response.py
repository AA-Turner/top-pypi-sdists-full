# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel


class BenchmarkDiagnosticStatusResponse(BaseModel):
  benchmark_diagnostic_id: str

  status: Literal["pending", "running", "completed", "failed", "cancelled"]
