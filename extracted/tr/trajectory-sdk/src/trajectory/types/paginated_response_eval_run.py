# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory.types.evals.eval_run import EvalRun


class PaginatedResponseEvalRun(SyncPage[EvalRun]):
  items: list[EvalRun]

  next_cursor: str | None = None

  has_more: bool
