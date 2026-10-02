# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime

from trajectory._models import BaseModel


class ModelSlug(BaseModel):
  model_slug_id: str

  organization_id: str

  name: str

  created_at: datetime | None = None
