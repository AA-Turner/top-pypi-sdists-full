# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from trajectory._models import BaseModel


class BenchmarkDiagnosticTask(BaseModel):
  task_id: str

  runtime_id: str | None

  status: Literal["pending", "running", "completed", "failed", "cancelled"]

  failure: dict[str, Any] | None
  """Failure for this task, including rollout details when available."""

  created_at: datetime

  updated_at: datetime

  started_at: datetime | None

  completed_at: datetime | None


class BenchmarkDiagnosticTaskCounts(BaseModel):
  completed: int

  failed: int

  cancelled: int


class BenchmarkDiagnosticsResponse(BaseModel):
  benchmark_diagnostic_id: str

  bench_id: str

  eval_run_id: str

  base_model_slug: str
  """Model used for the diagnostic run."""

  status: Literal["completed", "failed", "cancelled"]

  created_at: datetime

  updated_at: datetime

  started_at: datetime | None

  completed_at: datetime | None

  failure: dict[str, Any] | None
  """Run-wide failure summary; task errors appear on tasks."""

  task_counts: BenchmarkDiagnosticTaskCounts
  """Number of tasks by final status."""

  tasks: list[BenchmarkDiagnosticTask]
