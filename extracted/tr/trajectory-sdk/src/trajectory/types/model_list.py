# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.inference.model import Model


class ModelList(BaseModel):
  object: str = "list"

  data: list[Model]
