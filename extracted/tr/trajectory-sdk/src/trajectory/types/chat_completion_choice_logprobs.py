# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class ChatCompletionTokenTopLogprob(BaseModel):
  token: str

  logprob: float

  bytes: list[int] | None = None


class ChatCompletionTokenLogprob(BaseModel):
  token: str

  logprob: float

  bytes: list[int] | None = None

  top_logprobs: list[ChatCompletionTokenTopLogprob]


class ChatCompletionChoiceLogprobs(BaseModel):
  content: list[ChatCompletionTokenLogprob] | None = None

  refusal: list[ChatCompletionTokenLogprob] | None = None
