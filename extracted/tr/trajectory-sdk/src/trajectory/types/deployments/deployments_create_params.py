# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, Required, TypedDict


class ModelEndpointConfigParam(TypedDict, total=False):
  model_path: Required[str]
  max_output_tokens_per_step: Required[int]
  max_response_chars_per_tool_call: Required[int]
  max_output_tokens: int | None
  max_turns_per_trajectory: int
  temperature_override: float | None
  disable_thinking: bool
  reasoning_effort: Literal["none", "minimal", "low", "medium", "high", "xhigh"] | None


class DeploymentsCreateParams(TypedDict, total=False):
  checkpoint_id: Required[str]
  model_slug: Required[str]
  agent_id: str | None
  """
  Owning agent; inferred from the checkpoint or serving name when omitted.
  """
  role: Literal["production", "test"]
  model_endpoint_config: ModelEndpointConfigParam | None
  """
  Model Endpoint configuration for the deployment. Defaults to the exact configuration persisted
  for the originating Training Service run.
  """
