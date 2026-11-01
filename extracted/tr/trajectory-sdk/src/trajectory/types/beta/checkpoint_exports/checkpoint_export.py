# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime
from typing import Literal, TypeAlias

from trajectory._models import BaseModel


class Download(BaseModel):
  filename: str

  size_bytes: int

  md5: str
  """GCS-verified, base64-encoded MD5 checksum of the complete ZIP."""

  url: str
  """Signed HTTPS link; request a fresh one after it expires."""

  url_expires_at: datetime


State: TypeAlias = Literal["queued", "preparing", "ready", "failed"]


class CheckpointExport(BaseModel):
  export_id: str

  checkpoint_id: str

  export_type: str

  state: State

  download: Download | None = None
  """Present only on retrieval of a ready export."""
