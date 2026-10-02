# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.training.checkpoints.training_checkpoint_response import (
  TrainingCheckpointResponse,
)


class TrainingCheckpointsResponse(BaseModel):
  items: list[TrainingCheckpointResponse]
