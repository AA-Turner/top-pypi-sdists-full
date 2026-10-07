# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.eval_task_selection import EvalTaskSelection


class StartEvalResponse(BaseModel):
  task_selection: EvalTaskSelection | None = None
  """Task coverage fixed at launch; null for legacy or diagnostic runs."""

  bench_id: str
  """Benchmark evaluated by this run."""

  eval_run_id: str
  """Evaluation run created for this request."""

  display_name: str | None
  """User-facing name for the evaluation run."""
