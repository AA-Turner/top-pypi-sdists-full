# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel
from trajectory.types.chat_completion_choice_logprobs import ChatCompletionChoiceLogprobs
from trajectory.types.usage import Usage


class ChatCompletionResponseFunction(BaseModel):
  name: str

  arguments: str


class ChatCompletionResponseToolCall(BaseModel):
  id: str

  type: Literal["function"]

  function: ChatCompletionResponseFunction


class ChatCompletionResponseMessage(BaseModel):
  role: str

  content: str | None

  tool_calls: list[ChatCompletionResponseToolCall] | None = None


class ChatCompletionChoice(BaseModel):
  index: int

  message: ChatCompletionResponseMessage

  finish_reason: str | None = None

  logprobs: ChatCompletionChoiceLogprobs | None = None


class ChatCompletionResponse(BaseModel):
  id: str

  object: str

  created: int

  model: str

  choices: list[ChatCompletionChoice]

  usage: Usage | None = None
