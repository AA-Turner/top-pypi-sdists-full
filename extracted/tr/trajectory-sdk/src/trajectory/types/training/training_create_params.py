# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, Required, TypedDict

from trajectory.types.run_options_param import RunOptionsParam


class TrainingCreateParams(TypedDict, total=False):
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
      "Qwen/Qwen3.6-35B-A3B",
      "Qwen/Qwen3.8-27B",
      "qwen/qwen3-235b-a22b",
      "nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16",
      "nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16",
      "nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16",
      "nvidia/NVIDIA-Nemotron-3.5-Super-120B-A12B-BF16",
      "openai/gpt-6.1-sol",
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
