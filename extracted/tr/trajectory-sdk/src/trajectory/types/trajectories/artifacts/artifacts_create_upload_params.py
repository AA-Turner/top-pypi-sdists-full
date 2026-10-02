# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Required, TypedDict


class ArtifactsCreateUploadParams(TypedDict, total=False):
  media_type: Required[str]
  """
  MIME type of the file, such as image/png.
  """
  size_bytes: Required[int]
  """
  Exact file size in bytes, at most 16 MiB.
  """
  md5: Required[str]
  """
  Base64-encoded MD5 of the file; GCS rejects bytes that do not match.
  """
