# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class BenchmarkUploadUrl(BaseModel):
  path: str

  url: str

  headers: dict[str, str]
