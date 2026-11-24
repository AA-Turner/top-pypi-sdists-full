# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory._models import BaseModel


class StalenessKlPart(BaseModel):
  staleness: int
  """Policy steps between the policy that sampled these sequences and the update."""

  kl_estimate_k3: float
  """
    These sequences' k3 sum over their action tokens with a nonzero advantage, divided by
    all such tokens in the batch.
    """


class TrainingStepMetrics(BaseModel):
  step: int
  """Training step produced by this update; its checkpoint has the same step index."""

  rollout_wait_seconds: float | None
  """
    Seconds the trainer waited to collect this update's batch: rollouts for reinforcement
    learning, dataset reads for supervised fine-tuning. Rollouts run alongside training, so
    this is time the trainer was blocked, not total generation time.
    """

  training_seconds: float
  """
    Seconds the trainer spent on the update: forward/backward, the optimizer step, and any
    extra passes the algorithm needs, such as reference log-probabilities.
    """

  forward_backward_seconds: float | None
  """Seconds until the forward/backward result arrived, including any provider queueing."""

  optimizer_seconds: float | None
  """
    Seconds the optimizer step added after the forward/backward result. Providers that run
    both in one batch can report close to zero.
    """

  weight_sync_seconds: float | None
  """
    Seconds to export the updated weights for sampling. Near zero when the provider exports
    them in the same batch as the update.
    """

  checkpoint_seconds: float | None
  """Seconds to save the step's training state."""

  trainer_tokens_per_second: float | None
  """Trained input tokens divided by training_seconds."""

  generated_tokens_per_second: float | None
  """
    Generated tokens in the batch divided by the wall time since the previous batch. Null on
    the first step after training starts or resumes.
    """

  learning_rate: float | None
  """
    Learning rate the update applied, after warmup and decay. Null for steps recorded before
    the trainer persisted it.
    """

  brier_loss: float | None = None
  """
    Half the sum of squared differences between RLCD choice probabilities and targets,
    averaged across decisions. Lower is better.
    """

  training_loss: float | None = None
  """
    Mean loss over the update's supervised tokens; lower is better. Recorded by supervised
    fine-tuning and null otherwise.
    """

  kl_estimate_k3: float | None
  """
    Mean k3 estimate of KL(sampler || learner) over the batch's action tokens with a nonzero
    advantage. Null for algorithms that do not estimate it.
    """

  kl_estimate_k3_min: float | None
  """
    Lowest of the batch's per-sequence k3 estimates, each the mean over that sequence's
    action tokens with a nonzero advantage.
    """

  kl_estimate_k3_max: float | None
  """Highest of the batch's per-sequence k3 estimates."""

  kl_estimate_k3_p25: float | None
  """25th percentile of the batch's per-sequence k3 estimates."""

  kl_estimate_k3_p50: float | None
  """Median of the batch's per-sequence k3 estimates."""

  kl_estimate_k3_p75: float | None
  """75th percentile of the batch's per-sequence k3 estimates."""

  kl_estimate_k3_by_staleness: list[StalenessKlPart]
  """
    kl_estimate_k3's part from each sample staleness in the batch, by ascending staleness.
    The parts add up to the estimate, less any hindsight copies, which no policy sampled.
    Empty when the batch's sample staleness is unknown.
    """

  sequences_per_trajectory_mean: float | None
  """
    Mean trained sequences per trajectory in the batch. A trajectory starts another sequence
    whenever a turn does not extend the previous turn's context.
    """

  sequences_per_trajectory_min: int | None
  """Fewest trained sequences of one trajectory in the batch."""

  sequences_per_trajectory_max: int | None
  """Most trained sequences of one trajectory in the batch."""

  sequences_per_trajectory_p25: float | None
  """25th percentile of trained sequences per trajectory in the batch."""

  sequences_per_trajectory_p50: float | None
  """Median trained sequences per trajectory in the batch."""

  sequences_per_trajectory_p75: float | None
  """75th percentile of trained sequences per trajectory in the batch."""


class TrainingStepMetricsPage(SyncPage[TrainingStepMetrics]):
  items: list[TrainingStepMetrics]

  next_cursor: str | None = None

  has_more: bool

  training_run_id: str
  """Training run whose step metrics are returned."""
