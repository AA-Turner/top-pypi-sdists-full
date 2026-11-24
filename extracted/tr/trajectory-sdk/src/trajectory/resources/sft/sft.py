# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Literal

import httpx2

from trajectory._base_client import make_request_options, serialize_header
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.resources.sft.losses import Losses, LossesWithRawResponse
from trajectory.resources.sft.runs import Runs, RunsWithRawResponse
from trajectory.types.create_training_run_response import CreateTrainingRunResponse
from trajectory.types.sft.sft_train_params import SftTrainingOptionsParam, SftTrainParams
from trajectory.types.sft_run_options_response import SftRunOptionsResponse


class Sft(APIResource):
  @cached_property
  def with_raw_response(self) -> SftWithRawResponse:
    return SftWithRawResponse(self)

  @cached_property
  def runs(self) -> Runs:
    return Runs(self._client)

  @cached_property
  def losses(self) -> Losses:
    return Losses(self._client)

  def train(
    self,
    *,
    base_model_slug: Literal[
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
    ],
    dataset_id: str,
    idempotency_key: str | Omit = omit,
    options: SftTrainingOptionsParam | None | Omit = omit,
    parent_checkpoint_id: str | None | Omit = omit,
    display_name: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> CreateTrainingRunResponse:
    """Create and launch a supervised fine-tuning run on a finalized dataset version: it trains
    on the version's train trajectories and reports held-out loss on its heldout
    trajectories.

    Args:
      base_model_slug: Registered base model to fine-tune.

      dataset_id: Saved dataset version (`dset_...`) whose trajectories are the training examples.

      idempotency_key: Optional. Without a key, repeated submissions are treated as separate actions. A
        blank or over-long key is rejected. Reuse this key when retrying a submission; the
        SDK generates one per call and reuses it across automatic retries.

      options: SFT settings; omission, null, and an empty object preserve defaults.

      parent_checkpoint_id: Checkpoint to fine-tune from instead of the base weights; must match
        base_model_slug.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/train_sft",
      cast_to=CreateTrainingRunResponse,
      body=maybe_transform(
        {
          "base_model_slug": base_model_slug,
          "dataset_id": dataset_id,
          "options": options,
          "parent_checkpoint_id": parent_checkpoint_id,
          "display_name": display_name,
        },
        SftTrainParams,
      ),
      options=make_request_options(
        headers={
          "Idempotency-Key": serialize_header(idempotency_key),
        },
        extra_headers=(
          {"Idempotency-Key": omit, **(extra_headers or {})}
          if idempotency_key is None
          else extra_headers
        ),
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
        idempotency_header=("Idempotency-Key" if isinstance(idempotency_key, Omit) else None),
      ),
    )

  def list_options(
    self,
    *,
    base_model_slug: Literal[
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
    | None
    | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> SftRunOptionsResponse:
    """Return the models SFT can fine-tune and each SFT option's limits and default.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/train_sft/options",
      cast_to=SftRunOptionsResponse,
      options=make_request_options(
        params=maybe_transform(
          {
            "base_model_slug": base_model_slug,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class SftWithRawResponse:
  def __init__(self, resource: Sft) -> None:
    self._resource = resource
    self.train = to_raw_response_wrapper(resource.train)
    self.list_options = to_raw_response_wrapper(resource.list_options)

  @cached_property
  def runs(self) -> RunsWithRawResponse:
    return RunsWithRawResponse(self._resource.runs)

  @cached_property
  def losses(self) -> LossesWithRawResponse:
    return LossesWithRawResponse(self._resource.losses)
