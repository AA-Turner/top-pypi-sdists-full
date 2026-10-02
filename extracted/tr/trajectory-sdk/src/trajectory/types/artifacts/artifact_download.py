# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime

from trajectory._models import BaseModel


class ArtifactDownload(BaseModel):
  artifact_id: str
  """Stable file ID, resolved within the owning organization."""

  media_type: str
  """MIME type of the stored file."""

  size_bytes: int
  """Size of the original file in bytes."""

  md5: str
  """GCS-verified, base64-encoded MD5 checksum of the file."""

  created_at: datetime
  """Time the file metadata was first published."""

  download_url: str
  """Signed file download URL, valid for five minutes."""
