# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime

from trajectory._models import BaseModel
from trajectory.types.benchmark_upload_url import BenchmarkUploadUrl


class BenchmarkIngestionUploadPolicy(BaseModel):
  url: str
  """Form upload endpoint (POST) for every file in the batch."""

  fields: dict[str, str]
  """
    Signed form fields; send them with `key`, `Content-Type`, and the file as the last
    field, `file`.
    """

  artifact_prefix: str
  """An artifact's `key` is this prefix plus its path."""

  part_prefix: str
  """A task part's `key` is this prefix plus its path."""

  expires_at: datetime
  """Uploads must start before this time."""


class BenchmarkIngestionUploadUrls(BaseModel):
  urls: list[BenchmarkUploadUrl]

  policy: BenchmarkIngestionUploadPolicy | None = None
  """Set instead of `urls` when the allocation requested `post`."""
