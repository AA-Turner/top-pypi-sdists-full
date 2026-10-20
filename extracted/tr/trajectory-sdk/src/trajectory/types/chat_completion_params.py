# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, Required, TypedDict


class ChatMessageParam(TypedDict, total=False):
  role: Required[str]
  content: str | Iterable[Mapping[str, Any]] | None


class ChatCompletionParams(TypedDict, total=False):
  model: Required[str]
  messages: Required[Iterable[ChatMessageParam | Mapping[str, Any]]]
  stream: bool | None
  temperature: float | None
  max_tokens: int | None
  """
  Maximum generated tokens, including reasoning tokens when emitted.
  """
  top_p: float | None
