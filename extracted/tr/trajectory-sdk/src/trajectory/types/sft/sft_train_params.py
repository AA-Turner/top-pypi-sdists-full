# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, Required, TypedDict


class SftTrainingOptionsParam(TypedDict, total=False):
  """
  SFT settings; RL options such as samplers, group_size and rollout limits are rejected.
  """

  val_enabled: bool | None
  """
  Enable validation during training.
  """
  val_interval_steps: int | None
  """
  Training steps between validations; 0 disables validation.
  """
  learning_rate: float | None
  """
  Base optimizer learning rate.
  """
  num_steps: int | None
  """
  Number of optimizer steps to run. Training cycles through the dataset, reshuffling it after
  each full pass. 0 only scores the held-out split at the starting weights.
  """
  batch_size: int | None
  """
  Max Context window x Batch size tokens are used per optimizer update
  """
  max_tokens_per_turn: int | None
  """
  Maximum prompt and completion tokens in each trained turn; a trajectory with a longer turn is
  dropped. Defaults to the model's context length.
  """


class SftTrainParams(TypedDict, total=False):
  """
  Fine-tune a base model on a saved dataset.
  """

  base_model_slug: Required[
    Literal[
      "typesafe/jev-1.14",
      "thinkingmachines/Inkling-2-Small",
      "thinkingmachines/Inkling-2-Mini",
      "deepseek-ai/DeepSeek-V4.1-Flash",
      "thinkingmachines/Inkling-Small",
      "Qwen/Qwen3.5-4B",
      "Qwen/Qwen3.5-397B-A17B",
      "Qwen/Qwen3.6-35B-A3B",
      "Qwen/Qwen3.8-27B",
      "nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16",
      "nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16",
      "nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16",
      "nvidia/NVIDIA-Nemotron-3.5-Super-120B-A12B-BF16",
      "openai/gpt-6.1-sol",
      "openai/gpt-6-luna",
      "openai/gpt-6-sol",
      "openai/gpt-6-astra",
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
      "z-ai/glm-5.3-flash",
      "moonshotai/kimi-k3",
    ]
  ]
  """
  Registered base model to fine-tune.
  """
  dataset_id: Required[str]
  """
  Saved dataset version (`dset_...`) whose trajectories are the training examples.
  """
  options: SftTrainingOptionsParam | None
  """
  SFT settings; omission, null, and an empty object preserve defaults.
  """
  parent_checkpoint_id: str | None
  """
  Checkpoint to fine-tune from instead of the base weights; must match base_model_slug.
  """
  display_name: str | None
