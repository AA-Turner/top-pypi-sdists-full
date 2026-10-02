# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class MessageUsage(BaseModel):
  prompt_tokens: int = 0

  completion_tokens: int = 0

  total_tokens: int = 0
