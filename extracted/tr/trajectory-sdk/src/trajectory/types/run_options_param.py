# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, TypedDict


class RunOptionsParam(TypedDict, total=False):
  retries: int | None
  """
  Fresh attempts after failure; defaults to 0. Set 3 to retry three times.
  """
  intelligent_density_training: bool | None
  """
  Enable intelligent density training.
  """
  algorithm: Literal["gspo", "grpo", "reinforce_plus_plus"] | None
  """
  Training algorithm; omit to preserve the model default.
  """
  train_on_truncation: bool | None
  """
  Include truncated trajectories in training.
  """
  train_on_ungraded: bool | None
  """
  Include otherwise eligible trajectories without a recorded reward.
  """
  evaluation_max_samples: int | None
  """
  Maximum distinct tasks per evaluation. Standalone evals run every task in the selected scope
  when omitted.
  """
  evaluation_samples_per_task: int | None
  evaluation_max_active_rollouts: int | None
  evaluation_collection_timeout_seconds: float | None
  """
  Total wait for outstanding evaluation rollouts; zero stops waiting immediately.
  """
  learning_rate: float | None
  """
  Base optimizer learning rate.
  """
  lr_warmup_steps: int | None
  """
  Reported training steps used for warmup, including skipped optimizer updates.
  """
  lr_hold_steps: int | None
  """
  Training steps to hold the base rate after warmup, including skipped updates, before cosine
  decay.
  """
  min_lr_ratio: float | None
  """
  Cosine decay floor as a fraction of the base learning rate.
  """
  disable_thinking: bool | None
  """
  Disable model thinking during training or evaluation.
  """
  num_steps: int | None
  """
  Total optimizer step target, including steps restored from a checkpoint.
  """
  train_batch_size: int | None
  """
  Eligible task-instance groups per optimizer update.
  """
  samples_per_instance: int | None
  """
  Rollout samples generated for each training instance; GSPO and GRPO require at least 2, while
  Reinforce++ requires 1.
  """
  n_parallel_agents: int | None
  """
  Maximum active training rollouts (per worker for legacy runs).
  """
  execution_timeout_seconds: int | None
  """
  Maximum execution time per training or evaluation rollout, including policy and grading.
  Collection timeouts must cover this budget and are not adjusted automatically.
  """
  batch_collection_idle_timeout_seconds: int | None
  """
  Maximum wall-clock time to assemble one training batch. The clock starts when collection
  begins and does not reset as groups or in-flight rollouts arrive. The legacy field name is
  retained for API compatibility. Must cover rollout execution and is not adjusted
  automatically.
  """
  max_output_tokens_per_step: int | None
  """
  Maximum assistant output tokens allowed in one model step.
  """
  max_total_tokens_per_trajectory: int | None
  """
  Maximum total tokens available across one trajectory.
  """
  max_turns_per_trajectory: int | None
  """
  Maximum agent and environment turns allowed in each trajectory.
  """
  max_tool_calls_per_step: int | None
  """
  Maximum tool calls executed from one assistant step (0 rejects all).
  """
  max_response_chars_per_tool_call: int | None
  """
  Maximum tool-response characters retained before truncation; at most 65,536 for training or
  10,000,000 for standalone evaluation.
  """
