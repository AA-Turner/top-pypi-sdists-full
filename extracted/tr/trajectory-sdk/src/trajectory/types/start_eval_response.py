# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class StartEvalResponse(BaseModel):
  bench_id: str
  """Benchmark evaluated by this run."""

  eval_run_id: str
  """Evaluation run created for this request."""

  display_name: str | None
  """User-facing name for the evaluation run."""
