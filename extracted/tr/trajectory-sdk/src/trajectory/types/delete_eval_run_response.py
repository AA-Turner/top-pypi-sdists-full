# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class DeleteEvalRunResponse(BaseModel):
  bench_id: str
  """ID of the benchmark that owned the deleted evaluation run."""

  eval_run_id: str
  """ID of the deleted evaluation run."""
