# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime

from trajectory._models import BaseModel


class BenchmarkRuntime(BaseModel):
  organization_id: str

  runtime_id: str

  image_ref: str | None = None

  dockerfile_uri: str | None = None

  content_hash: str

  provider: str

  blueprint_id: str | None = None
  """Image ID of the resulting build."""

  build_status: str

  created_at: datetime
