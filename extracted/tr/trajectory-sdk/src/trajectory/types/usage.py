# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class CompletionTokensDetails(BaseModel):
  accepted_prediction_tokens: int | None = None

  audio_tokens: int | None = None

  reasoning_tokens: int | None = None

  rejected_prediction_tokens: int | None = None


class PromptTokensDetails(BaseModel):
  audio_tokens: int | None = None

  cached_tokens: int | None = None


class Usage(BaseModel):
  prompt_tokens: int

  completion_tokens: int

  total_tokens: int

  completion_tokens_details: CompletionTokensDetails | None = None

  prompt_tokens_details: PromptTokensDetails | None = None
