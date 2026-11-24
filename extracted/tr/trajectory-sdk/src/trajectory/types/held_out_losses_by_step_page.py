# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory._models import BaseModel


class HeldOutLoss(BaseModel):
  step: int
  """Training step whose weights were scored; 0 is before training."""

  held_out_loss: float
  """Mean loss over the supervised tokens of the heldout trajectories; lower is better."""

  held_out_loss_per_trajectory: float | None = None
  """
    Mean over the heldout trajectories of each one's mean loss per supervised token, so
    every trajectory counts equally; null for passes scored before it was recorded.
    """

  expected_samples: int | None = None
  """Heldout trajectories selected for the pass."""

  completed_samples: int | None = None
  """Heldout trajectories that were scored."""

  failed_samples: int | None = None
  """Heldout trajectories left out because they could not be read."""


class HeldOutLossesByStepPage(SyncPage[HeldOutLoss]):
  items: list[HeldOutLoss]

  next_cursor: str | None = None

  has_more: bool

  training_run_id: str
  """Training run whose held-out losses are returned."""
