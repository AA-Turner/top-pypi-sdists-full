# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Iterable
from typing import Literal, Required, TypedDict


class BenchmarkIngestionUploadObjectParam(TypedDict, total=False):
  path: Required[str]
  content_type: Required[str]
  size_bytes: Required[int]
  md5: Required[str]
  kind: Literal["artifact", "part"]


class IngestionAllocateUploadsParams(TypedDict, total=False):
  files: Required[Iterable[BenchmarkIngestionUploadObjectParam]]
  """
  At most 1000 files and 1024 KiB with `put`, or 5000 files and 4096 KiB with `post`.
  """
  upload_method: Literal["put", "post"]
  """
  `put` returns a signed PUT URL per file. `post` returns one signed form-upload policy for the
  whole batch; uploads are checked against their declarations when the submission is verified.
  """
