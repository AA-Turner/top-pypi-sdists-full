# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, Required, TypedDict


class RunOptionsParam(TypedDict, total=False):
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
  Number of optimizer steps to run.
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


class CreateRunParams(TypedDict, total=False):
  """
  Launch a benchmark ID, or resolve the latest version by agent and benchmark names.
  """

  bench_id: str | None
  agent_name: str | None
  benchmark_name: str | None
  """
  Resolve the latest version and run its benchmark ID.
  """
  bypass_ownership: bool
  """
  Allow a supplied agent to differ from the benchmark owner within the same organization; run
  attribution uses the benchmark owner.
  """
  agent_id: str | None
  base_model_slug: Required[
    Literal[
      "thinkingmachines/Inkling-Small",
      "Qwen/Qwen3.5-4B",
      "Qwen/Qwen3.5-397B-A17B",
      "Qwen/Qwen3.6-27B",
      "Qwen/Qwen3.6-35B-A3B",
      "Qwen/Qwen3.8-27B",
      "qwen/qwen3-235b-a22b",
      "nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16",
      "nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16",
      "nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16",
      "nvidia/NVIDIA-Nemotron-3.5-Super-120B-A12B-BF16",
      "openai/gpt-5.6-sol",
      "openai/gpt-5.6-luna",
      "anthropic/claude-opus-5.5",
      "anthropic/claude-sonnet-5.5",
      "openai/gpt-5-mini",
      "openai/gpt-5.4-mini",
      "openai/gpt-5.5",
      "anthropic/claude-sonnet-4.6",
      "google/gemini-3.1-pro-preview",
      "z-ai/glm-5.3",
      "moonshotai/kimi-k3",
    ]
  ]
  """
  Registered base model for the run, distinct from a deployment model slug.
  """
  options: RunOptionsParam | None
  """
  Run settings; omission, null, and an empty object preserve defaults.
  """
  parent_checkpoint_id: str | None
  """
  Checkpoint to resume training from or evaluate; must match the selected base model.
  """
  display_name: str | None
