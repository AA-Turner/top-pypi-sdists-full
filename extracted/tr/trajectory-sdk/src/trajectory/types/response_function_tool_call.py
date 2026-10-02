# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel


class ResponseFunctionToolCall(BaseModel):
  arguments: str

  call_id: str

  name: str

  type: Literal["function_call"]

  id: str | None = None

  status: Literal["in_progress", "completed", "incomplete"] | None = None
