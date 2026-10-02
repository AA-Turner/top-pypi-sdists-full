# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.benchmarks.image_spec import ImageSpec


class RuntimeSpec(BaseModel):
  runtime_id: str | None = None

  source: ImageSpec | None = None
