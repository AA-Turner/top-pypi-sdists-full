# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.secrets.secret import Secret


class SecretListResponse(BaseModel):
  items: list[Secret]
  """Page of the organization's live secrets."""

  next_cursor: str | None = None
  """Cursor for the next page, or null if none."""

  has_more: bool
  """True if more secrets remain beyond this page."""
