# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class DatasetMetadata(BaseModel):
  dataset_id: str

  organization_id: str

  dataset_name: str

  display_name: str | None = None

  source: str | None = None

  gcs_prefix: str | None = None

  created_at: str

  updated_at: str | None = None
