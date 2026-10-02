# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel


class ResponseReasoningSummary(BaseModel):
  text: str

  type: Literal["summary_text"]


class ResponseReasoningText(BaseModel):
  text: str

  type: Literal["reasoning_text"]


class ResponseReasoningItem(BaseModel):
  id: str

  summary: list[ResponseReasoningSummary]

  type: Literal["reasoning"]

  content: list[ResponseReasoningText] | None = None

  encrypted_content: str | None = None

  status: Literal["in_progress", "completed", "incomplete"] | None = None
