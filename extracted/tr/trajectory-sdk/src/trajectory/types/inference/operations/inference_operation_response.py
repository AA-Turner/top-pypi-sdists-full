# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal, TypeAlias

from trajectory._models import BaseModel

InferenceOperationState: TypeAlias = Literal["PENDING", "IN_PROGRESS", "COMPLETED", "FAILED"]


class InferenceOperationResponse(BaseModel):
  id: str

  status: InferenceOperationState

  status_url: str

  deadline_at: datetime

  failure_code: str | None = None

  failure: dict[str, Any] | None = None

  result: dict[str, Any] | None = None
