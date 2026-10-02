# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Literal

from trajectory._models import BaseModel
from trajectory.types.message_usage import MessageUsage
from trajectory.types.tool_call import ToolCall
from trajectory.types.tool_definition import ToolDefinition


class BenchmarkMessage(BaseModel):
  role: str

  content: str | None = None

  tool_calls: list[ToolCall] | None = None

  tool_response: ToolResponse | None = None

  tool_definitions: list[ToolDefinition] | None = None

  usage: MessageUsage | None = None

  finish_reason: str | None = None

  metadata: dict[str, Any] | None = None

  reasoning: str | None = None

  reasoning_details: Any | None = None

  tokens: list[int] | None = None

  token_masks: list[int] | None = None

  logprobs: list[float] | None = None

  trainable_status: Literal[
    "trainable", "not_trainable", "superseded", "summarization_boundary"
  ] = "not_trainable"


class GeneratedToolInfo(BaseModel):
  provider: str

  model: str

  messages: list[BenchmarkMessage]


class ToolResponseMetadata(BaseModel):
  generated_tool_info: GeneratedToolInfo | None = None


class ToolResponse(BaseModel):
  id: str

  name: str

  arguments: dict[str, Any]

  response: Any | None = None

  error: str | None = None

  raw_name_args: str | None = None

  metadata: ToolResponseMetadata | None = None

  duration_seconds: float | None = None

  is_env_done: bool = False
