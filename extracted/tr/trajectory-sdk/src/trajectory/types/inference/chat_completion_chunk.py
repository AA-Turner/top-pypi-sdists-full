# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel
from trajectory.types.chat_completion_choice_logprobs import ChatCompletionChoiceLogprobs
from trajectory.types.chat_completion_chunk_function import ChatCompletionChunkFunction
from trajectory.types.usage import Usage


class ChoiceDeltaToolCall(BaseModel):
  index: int

  id: str | None = None

  function: ChatCompletionChunkFunction | None = None

  type: Literal["function"] | None = None


class ChoiceDelta(BaseModel):
  role: str | None = None

  content: str | None = None

  refusal: str | None = None

  function_call: ChatCompletionChunkFunction | None = None

  tool_calls: list[ChoiceDeltaToolCall] | None = None


class Choice(BaseModel):
  index: int

  delta: ChoiceDelta

  finish_reason: str | None = None

  logprobs: ChatCompletionChoiceLogprobs | None = None


class ChatCompletionChunk(BaseModel):
  id: str

  object: str

  created: int

  model: str

  choices: list[Choice]

  usage: Usage | None = None

  service_tier: str | None = None

  system_fingerprint: str | None = None
