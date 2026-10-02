# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class ArtifactUpload(BaseModel):
  artifact_id: str
  """Reserved file ID; complete the upload before using it."""

  upload_url: str
  """Signed PUT URL valid for ten minutes; send the file here."""

  headers: dict[str, str]
  """Required headers for the PUT request."""
