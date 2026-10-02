# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel
from trajectory.types.batch_item_failure import BatchItemFailure


class TrajectoryUploadItem(BaseModel):
  request_index: int
  """Zero-based index of this trajectory in the request."""

  conversation_id: str | None = None
  """Caller-provided conversation id from task.conversation_id."""

  trace_id: str | None = None
  """Caller-owned correlation key shared by telemetry and this trajectory."""

  trajectory_id: str | None = None
  """Stored trajectory id assigned by the backend."""

  model_id: str | None = None
  """Internal model id associated with this trajectory, when known."""

  model_association_source: str | None = None
  """How the trajectory was associated with a model."""

  status: Literal["uploaded", "skipped", "error"]
  """Upload status for this trajectory: uploaded, skipped, or error."""

  failure: BatchItemFailure | None = None
  """Structured trajectory-specific failure, if any."""


class TrajectoryUploadResponse(BaseModel):
  uploaded: int
  """Number of trajectories accepted for storage."""

  skipped: int
  """Number of trajectories skipped by validation or deduplication."""

  failures: list[BatchItemFailure] | None = None
  """Structured batch-level upload failures, if any."""

  message: str | None = None
  """Human-readable upload summary."""

  partial_success: bool = False
  """True when some trajectories uploaded but one or more errors occurred."""

  trajectories: list[TrajectoryUploadItem] | None = None
  """Per-trajectory upload mapping for correlating caller ids to trajectory ids."""
