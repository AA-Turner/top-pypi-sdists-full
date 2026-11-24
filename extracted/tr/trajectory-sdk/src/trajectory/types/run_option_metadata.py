# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel


class RunOptionMetadata(BaseModel):
  type: Literal["integer", "number", "boolean", "string"]

  min: float | None = None

  max: float | None = None

  default: bool | int | float | str | None

  choices: list[str] | None = None

  default_kind: Literal["fixed", "computed"]

  description: str
