# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class SendArtemisMessageResponse(BaseModel):
  session_id: str
  """The session the message joined; read it to get the answer."""
