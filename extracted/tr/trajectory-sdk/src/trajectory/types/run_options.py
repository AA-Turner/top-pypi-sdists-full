# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel
from trajectory.types.training_algorithm import TrainingAlgorithm


class RunOptions(BaseModel):
  intelligent_density_training: bool | None = None
  """Enable intelligent density training."""

  algorithm: TrainingAlgorithm | None = None
  """Training algorithm; omit to preserve the model default."""

  train_on_truncation: bool | None = None
  """Include truncated trajectories in training."""

  train_on_error: bool | None = None
  """Train on error-terminated trajectories, using zero when no reward is recorded."""

  train_on_timeout: bool | None = None
  """Train on execution and sandbox timeouts, using zero when no reward is recorded."""

  evaluation_enabled: bool | None = None
  """Enable evaluations during training."""

  evaluation_frequency: int | None = None
  """
    Optimizer steps between evaluations during training: 0 disables evaluation, 1 evaluates
    after every step, and 2 after every other step. When enabled, the initial policy and
    final step are always evaluated.
    """

  evaluation_max_samples: int | None = None
  """
    Maximum distinct tasks per evaluation. Standalone evals run every task in the selected
    scope when omitted.
    """

  evaluation_samples_per_task: int | None = None

  evaluation_max_active_rollouts: int | None = None

  evaluation_collection_timeout_seconds: float | None = None
  """Total wait for outstanding evaluation rollouts; zero stops waiting immediately."""

  learning_rate: float | None = None
  """Base optimizer learning rate."""

  lr_warmup_steps: int | None = None
  """Reported training steps used for warmup, including skipped optimizer updates."""

  lr_hold_steps: int | None = None
  """
    Training steps to hold the base rate after warmup, including skipped updates, before
    cosine decay.
    """

  min_lr_ratio: float | None = None
  """Cosine decay floor as a fraction of the base learning rate."""

  reasoning_effort: (
    Literal["off", "on", "minimal", "low", "medium", "high", "xhigh", "max"] | None
  ) = None
  """
    Reasoning effort supported by the model; off disables thinking, on enables models
    without effort levels, and null preserves the model default.
    """

  temperature: float | None = None
  """Sampling temperature; null preserves the model default."""

  top_p: float | None = None
  """Nucleus sampling probability; null preserves the model default."""

  top_k: int | None = None
  """
    Sample from the top k tokens; -1 disables the limit, and null preserves the model
    default.
    """

  evaluation_reasoning_effort: (
    Literal["off", "on", "minimal", "low", "medium", "high", "xhigh", "max"] | None
  ) = None
  """Evaluation reasoning effort; null preserves the evaluation default."""

  evaluation_temperature: float | None = None
  """Evaluation sampling temperature; null preserves the evaluation default."""

  evaluation_top_p: float | None = None
  """Evaluation nucleus sampling probability; null preserves the evaluation default."""

  evaluation_top_k: int | None = None
  """
    Evaluation top-k token limit; -1 disables the limit, and null preserves the evaluation
    default.
    """

  num_steps: int | None = None
  """Number of optimizer steps to run."""

  train_batch_size: int | None = None
  """Eligible task-instance groups per optimizer update."""

  group_size: int | None = None
  """
    Rollout samples generated for each training instance; GSPO and GRPO require at least 2,
    while Reinforce++ requires 1.
    """

  samples_per_instance: int | None = None
  """Deprecated alias for group_size; use group_size for new requests."""

  min_samples_per_group: int | None = None
  """
    Minimum valid samples required for a training group; must not exceed group_size. Omit to
    preserve the model default, capped at the group size.
    """

  max_active_rollouts: int | None = None
  """Maximum active training rollouts per run."""

  max_steps_off_policy: int | None = None
  """
    Maximum optimizer steps a training rollout's starting policy may trail the current
    policy. Older in-flight rollouts are cancelled and older completed rollouts are
    discarded; 0 trains only on rollouts started from the current policy.
    """

  execution_timeout_seconds: int | None = None
  """
    Maximum execution time per training or evaluation rollout, including policy and grading.
    The clock starts when the harness runs, after queueing and sandbox startup. Collection
    timeouts must cover this budget and are not adjusted automatically.
    """

  batch_collection_idle_timeout_seconds: int | None = None
  """
    Maximum wall-clock time to assemble one training batch. The clock starts when collection
    begins and does not reset as groups or in-flight rollouts arrive. The legacy field name
    is retained for API compatibility. Must cover rollout execution and is not adjusted
    automatically.
    """

  max_output_tokens_per_step: int | None = None
  """
    On an endpoint created for the run, maximum assistant output tokens per model step;
    replaces the harness request's max_tokens.
    """

  max_total_tokens_per_trajectory: int | None = None
  """
    On an endpoint created for the run, maximum assistant output tokens across all steps of
    one trajectory, including steps after context compaction, so it can exceed the model's
    context window. Reaching this cap during a reply can end the trajectory as LIMIT_REACHED
    before the harness logs reward.
    """

  max_turns_per_trajectory: int | None = None
  """Maximum agent and environment turns allowed in each trajectory."""
