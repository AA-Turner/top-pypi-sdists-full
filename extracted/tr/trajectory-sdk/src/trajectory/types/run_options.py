# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, TypeAlias

from trajectory._models import BaseModel
from trajectory.types.priority_aggregation import PriorityAggregation
from trajectory.types.priority_trait import PriorityTrait

TrainingAlgorithm: TypeAlias = Literal["gspo", "grpo", "importance_sampling", "score_centering"]


class RunOptions(BaseModel):
  load_weights_only: bool | None = None
  """
    Load parent checkpoint weights with fresh training state. Defaults to false, which
    resumes the optimizer, LR schedule, and global step. With validation enabled, evaluate
    the starting policy, run validation when global_step % val_interval_steps == 0, and
    evaluate the final policy on normal completion. Resuming preserves the global step and
    validation cadence.
    """

  density_aware_training: bool | None = None
  """
    Train each task at four output-token budgets, with group_size trajectories per budget.
    Turns on train_on_truncation, which must stay true except when resuming a checkpoint
    with its training state. batch_size sets the total number of task groups per batch; each
    budget counts as a separate group. Learn more:
    https://www.trajectory.ai/field-notes/intelligence-density
    """

  algorithm: TrainingAlgorithm | None = None
  """Training algorithm; omit to preserve the model default."""

  train_on_truncation: bool | None = None
  """
    Include trajectories that hit token or turn limits in training, with reward 0. Defaults
    to false, or true with density_aware_training; set to true to discourage reward hacking
    through truncated submissions.
    """

  train_on_error: bool | None = None
  """
    Train on errored trajectories, including execution errors, grading errors, and missing
    grades, with reward 0.
    """

  train_on_timeout: bool | None = None
  """
    Include timed-out trajectories in training, with reward 0. Defaults to false; set to
    true to discourage reward hacking through timed-out submissions.
    """

  val_enabled: bool | None = None
  """Enable validation during training."""

  val_interval_steps: int | None = None
  """Training steps between validations; 0 disables validation."""

  val_num_tasks: int | None = None
  """
    Maximum distinct tasks per evaluation. Standalone evals run every task in the selected
    scope when omitted.
    """

  val_trajectories_per_task: int | None = None
  """Number of trajectories generated for each task in a validation round."""

  val_max_concurrent_trajectories: int | None = None
  """Maximum number of validation trajectories running concurrently."""

  val_final_wait_timeout_seconds: float | None = None
  """Maximum seconds to wait for outstanding validation rounds at training end."""

  learning_rate: float | None = None
  """Base optimizer learning rate."""

  lr_warmup_steps: int | None = None
  """Reported training steps used for warmup, including skipped optimizer updates."""

  lr_hold_steps: int | None = None
  """
    Training steps to hold the base rate after warmup, including skipped updates, before
    cosine decay.
    """

  lr_min_ratio: float | None = None
  """Cosine decay floor as a fraction of the base learning rate."""

  reasoning_effort: (
    Literal["off", "on", "minimal", "low", "medium", "high", "xhigh", "max"] | None
  ) = None
  """
    Model reasoning effort. null selects the lowest supported thinking level; off disables
    thinking where supported. Levels: minimal, low, medium, high, xhigh, max, depending on
    the model. Qwen3.5-4B, Qwen3.6-35B-A3B, Qwen3.5-397B-A17B, and
    Nemotron-3.5-Lightning-30B-A3B support only on/off; null selects on.
    """

  temperature: float | None = None
  """Sampling temperature; defaults to 1.0."""

  top_p: float | None = None
  """Nucleus sampling probability; null preserves the model default."""

  top_k: int | None = None
  """
    Sample from the top k tokens; -1 disables the limit, and null preserves the model
    default.
    """

  val_reasoning_effort: (
    Literal["off", "on", "minimal", "low", "medium", "high", "xhigh", "max"] | None
  ) = None
  """
    Validation reasoning effort. null inherits training defaults. Supports the same
    model-specific levels and on/off options as reasoning_effort.
    """

  val_temperature: float | None = None
  """Validation sampling temperature. null inherits training defaults."""

  val_top_p: float | None = None
  """Validation nucleus sampling probability. null inherits training defaults."""

  val_top_k: int | None = None
  """Validation top-k token limit. null inherits training defaults; -1 disables it."""

  val_max_output_tokens_per_turn: int | None = None
  """
    Maximum output tokens per turn in each validation trajectory. null inherits training
    defaults.
    """

  val_max_output_tokens_per_trajectory: int | None = None
  """Maximum output tokens across one validation trajectory. null inherits training defaults."""

  val_max_turns_per_trajectory: int | None = None
  """
    Maximum agent and environment turns per validation trajectory. null inherits training
    defaults.
    """

  val_trajectory_timeout_seconds: int | None = None
  """
    Maximum execution seconds per validation trajectory, including grading. null inherits
    training defaults.
    """

  num_steps: int | None = None
  """Number of optimizer steps to run."""

  batch_size: int | None = None
  """Eligible task-instance groups per optimizer update."""

  group_size: int | None = None
  """Trajectories generated for each training instance; GSPO and GRPO require at least 2."""

  shuffle_tasks: bool | None = None
  """
    Shuffle training tasks each epoch. Defaults to true; false starts tasks in upload order,
    with appended tasks after earlier ones, while each batch still takes groups as they
    finish. Benchmarks uploaded before upload order was recorded must be re-uploaded.
    """

  priority_trait: PriorityTrait | None = None
  """Trait used to prioritize completed training groups."""

  priority_aggregation: PriorityAggregation | None = None
  """Aggregation used to score a group for batch-selection priority."""

  min_trajectories_per_group: int | None = None
  """
    Minimum eligible trajectories per training group. null uses half of group_size, rounded
    down.
    """

  max_concurrent_trajectories: int | None = None
  """
    Maximum active training trajectories. null uses batch_size × group_size × 2, allowing 2×
    batch oversampling for throughput and asynchronous RL. Recommended: set above batch_size
    × group_size to keep collection ahead of training.
    """

  max_staleness: int | None = None
  """
    Maximum optimizer steps a training rollout’s starting policy may trail the current
    policy. Older in-flight rollouts are cancelled and older completed rollouts are
    discarded; 0 trains only on rollouts started from the current policy.
    """

  train_on_all_fail: bool | None = None
  """Train on groups whose eligible rewards are all at or below zero; false excludes them."""

  train_on_all_pass: bool | None = None
  """Train on groups whose eligible rewards are all at or above one; false excludes them."""

  train_on_zero_advantage: bool | None = None
  """Train on groups with identical eligible rewards; false excludes them."""

  trajectory_timeout_seconds: int | None = None
  """
    Maximum execution seconds per trajectory, including grading. Excludes queueing and
    sandbox startup. Collection timeouts must cover this budget.
    """

  batch_timeout_seconds: int | None = None
  """
    Wall-clock threshold for logging and reporting slow training batch collection.
    Collection continues after the threshold and reports again after each additional
    interval.
    """

  max_output_tokens_per_turn: int | None = None
  """
    Maximum output tokens per model response. null uses the model’s maximum, bounded by
    remaining context.
    """

  max_output_tokens_per_trajectory: int | None = None
  """
    Maximum output tokens across one trajectory, including after context compaction. null
    uses the model’s maximum supported context length.
    """

  max_turns_per_trajectory: int | None = None
  """Maximum agent and environment turns allowed in each trajectory."""

  image_max_pixels: int | None = None
  """
    Downscale input images above this many pixels, keeping their aspect ratio, before the
    model reads them. Fewer pixels cost fewer image tokens. null uses the model's default; a
    checkpoint evaluation keeps the cap its training run used unless this is set.
    """

  shuffle: bool | None = None
  """Shuffle training tasks each epoch; false follows benchmark upload order."""
