# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime

from trajectory._models import BaseModel


class CheckpointExportFile(BaseModel):
  path: str
  """The file's path inside the model folder."""

  size_bytes: int

  md5: str
  """GCS-verified, base64-encoded MD5 checksum of the file."""

  url: str
  """Signed HTTPS link; list the files again for a fresh one."""

  url_expires_at: datetime
