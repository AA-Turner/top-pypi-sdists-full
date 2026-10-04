# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, Literal, Required, TypedDict

from trajectory.types.message_usage_param import MessageUsageParam
from trajectory.types.tool_call_param import ToolCallParam
from trajectory.types.tool_definition_param import ToolDefinitionParam


class BenchmarkMessageParam(TypedDict, total=False):
  role: Required[str]
  content: str | None
  tool_calls: Iterable[ToolCallParam]
  tool_response: ToolResponseParam | None
  tool_definitions: Iterable[ToolDefinitionParam]
  usage: MessageUsageParam | None
  finish_reason: str | None
  metadata: Mapping[str, Any] | None
  reasoning: str | None
  reasoning_details: Any
  tokens: Iterable[int] | None
  token_masks: Iterable[int] | None
  logprobs: Iterable[float] | None
  trainable_status: Literal["trainable", "not_trainable", "superseded", "summarization_boundary"]


class GeneratedToolInfoParam(TypedDict, total=False):
  provider: Required[str]
  model: Required[str]
  messages: Required[Iterable[BenchmarkMessageParam]]


class ToolResponseParam(TypedDict, total=False):
  id: Required[str]
  name: Required[str]
  arguments: Required[Mapping[str, Any]]
  response: Any
  error: str | None
  raw_name_args: str | None
  metadata: ToolResponseMetadataParam | None
  duration_seconds: float | None
  is_env_done: bool


class ToolResponseMetadataParam(TypedDict, total=False):
  generated_tool_info: GeneratedToolInfoParam | None
