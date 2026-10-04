# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TypedDict


class MessageUsageParam(TypedDict, total=False):
  prompt_tokens: int
  completion_tokens: int
  total_tokens: int
