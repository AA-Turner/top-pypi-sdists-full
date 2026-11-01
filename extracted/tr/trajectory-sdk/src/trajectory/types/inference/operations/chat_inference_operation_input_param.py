# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, Required, TypedDict

from trajectory.types.chat_completion_params import ChatCompletionParams


class ChatInferenceOperationInputParam(TypedDict, total=False):
  api: Required[Literal["chat"]]
  input: Required[ChatCompletionParams | Mapping[str, Any]]
