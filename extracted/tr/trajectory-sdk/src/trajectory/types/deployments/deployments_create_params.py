# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, Required, TypedDict


class ModelEndpointConfigParam(TypedDict, total=False):
  model_path: Required[str]
  max_output_tokens_per_step: int | None
  max_response_chars_per_tool_call: int | None
  max_context_tokens: int | None
  max_output_tokens: int | None
  max_turns_per_trajectory: int | None
  temperature_override: float | None
  disable_thinking: bool | None
  reasoning_effort: Literal["none", "minimal", "low", "medium", "high", "xhigh", "max"] | None
  tokenizer_path: str | None
  top_p_override: float | None
  top_k_override: int | None


class DeploymentsCreateParams(TypedDict, total=False):
  checkpoint_id: Required[str]
  test_model_slug: Required[str]
  agent_id: str | None
  """
  Owning agent; inferred from the checkpoint when omitted.
  """
  model_endpoint_config: ModelEndpointConfigParam | None
  """
  Model and tokenizer identity for the deployment; defaults to the originating Training Service
  run. Sampling overrides and training limits are cleared.
  """
