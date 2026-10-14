# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory.types.training.training_run_response import TrainingRunResponse


class PaginatedResponseTrainingRunResponse(SyncPage[TrainingRunResponse]):
  items: list[TrainingRunResponse]

  next_cursor: str | None = None

  has_more: bool
