# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class ImageSpec(BaseModel):
  dockerfile_path: str | None = None

  image_ref: str | None = None
