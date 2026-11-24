# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, TypeAlias

from trajectory._models import BaseModel

ArtemisDecision: TypeAlias = Literal["approved", "rejected"]


class DecideArtemisResponse(BaseModel):
  session_id: str

  request_id: str

  decision: ArtemisDecision
