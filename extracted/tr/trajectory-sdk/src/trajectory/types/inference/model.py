# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class Model(BaseModel):
  id: str

  object: str = "model"

  created: int | None = None

  owned_by: str | None = None
