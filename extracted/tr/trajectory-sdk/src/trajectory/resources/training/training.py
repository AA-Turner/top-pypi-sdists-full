# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Literal

import httpx

from trajectory._base_client import make_request_options, serialize_header
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.resources.training.checkpoints import Checkpoints, CheckpointsWithRawResponse
from trajectory.resources.training.rewards import Rewards, RewardsWithRawResponse
from trajectory.resources.training.runs import Runs, RunsWithRawResponse
from trajectory.types.create_run_params import CreateRunParams, RunOptionsParam
from trajectory.types.create_training_run_response import CreateTrainingRunResponse
from trajectory.types.list_supported_models_response import ListSupportedModelsResponse
from trajectory.types.run_options_response import RunOptionsResponse


class Training(APIResource):
  @cached_property
  def with_raw_response(self) -> TrainingWithRawResponse:
    return TrainingWithRawResponse(self)

  @cached_property
  def runs(self) -> Runs:
    return Runs(self._client)

  @cached_property
  def checkpoints(self) -> Checkpoints:
    return Checkpoints(self._client)

  @cached_property
  def rewards(self) -> Rewards:
    return Rewards(self._client)

  def create(
    self,
    *,
    base_model_slug: Literal[
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
    ],
    idempotency_key: str | None | Omit = omit,
    bench_id: str | None | Omit = omit,
    agent_name: str | None | Omit = omit,
    benchmark_name: str | None | Omit = omit,
    bypass_ownership: bool | Omit = omit,
    agent_id: str | None | Omit = omit,
    options: RunOptionsParam | None | Omit = omit,
    parent_checkpoint_id: str | None | Omit = omit,
    display_name: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> CreateTrainingRunResponse:
    """Create and launch a training run.

    Args:
      base_model_slug: Registered base model for the run, distinct from a deployment model slug.

      idempotency_key: Optional; reuse this key when retrying a submission. The API generates one when
        omitted.

      benchmark_name: Resolve the latest version and run its benchmark ID.

      bypass_ownership: Allow a supplied agent to differ from the benchmark owner within the same
        organization; run attribution uses the benchmark owner.

      options: Run settings; omission, null, and an empty object preserve defaults.

      parent_checkpoint_id: Checkpoint to resume training from or evaluate; must match the selected base
        model.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/train",
      cast_to=CreateTrainingRunResponse,
      body=maybe_transform(
        {
          "base_model_slug": base_model_slug,
          "bench_id": bench_id,
          "agent_name": agent_name,
          "benchmark_name": benchmark_name,
          "bypass_ownership": bypass_ownership,
          "agent_id": agent_id,
          "options": options,
          "parent_checkpoint_id": parent_checkpoint_id,
          "display_name": display_name,
        },
        CreateRunParams,
      ),
      options=make_request_options(
        headers={
          "Idempotency-Key": serialize_header(idempotency_key),
        },
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def list_options(
    self,
    *,
    bench_id: str,
    base_model_slug: Literal[
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
    | None
    | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> RunOptionsResponse:
    """Return supported training models and their authored option ranges.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/train/options",
      cast_to=RunOptionsResponse,
      options=make_request_options(
        params=maybe_transform(
          {
            "bench_id": bench_id,
            "base_model_slug": base_model_slug,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def list_models(
    self,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> ListSupportedModelsResponse:
    """List Supported Training Models

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/models/supported-training-models",
      cast_to=ListSupportedModelsResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class TrainingWithRawResponse:
  def __init__(self, resource: Training) -> None:
    self._resource = resource
    self.create = to_raw_response_wrapper(resource.create)
    self.list_options = to_raw_response_wrapper(resource.list_options)
    self.list_models = to_raw_response_wrapper(resource.list_models)

  @cached_property
  def runs(self) -> RunsWithRawResponse:
    return RunsWithRawResponse(self._resource.runs)

  @cached_property
  def checkpoints(self) -> CheckpointsWithRawResponse:
    return CheckpointsWithRawResponse(self._resource.checkpoints)

  @cached_property
  def rewards(self) -> RewardsWithRawResponse:
    return RewardsWithRawResponse(self._resource.rewards)
