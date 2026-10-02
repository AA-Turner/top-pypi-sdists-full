# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime

from trajectory._models import BaseModel


class Secret(BaseModel):
  secret_id: str
  """Opaque identifier used to reference the secret."""

  name: str
  """Name the secret is referenced by (e.g. in ${secret:NAME})."""

  description: str | None = None
  """Optional human-readable description."""

  byte_length: int
  """Length of the secret value in UTF-8 bytes."""

  created_at: str | datetime | None = None
  """UTC timestamp the secret was created."""

  updated_at: str | datetime | None = None
  """UTC timestamp the secret was last updated."""
