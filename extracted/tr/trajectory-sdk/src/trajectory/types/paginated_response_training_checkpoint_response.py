# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory.types.rl.checkpoints.training_checkpoint_response import TrainingCheckpointResponse


class PaginatedResponseTrainingCheckpointResponse(SyncPage[TrainingCheckpointResponse]):
  items: list[TrainingCheckpointResponse]

  next_cursor: str | None = None

  has_more: bool
