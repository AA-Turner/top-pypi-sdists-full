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
  same_as: str | None
  """
  Path of an artifact declared earlier in this submission, or in this request, with the same
  `md5` and `size_bytes`. Its object is read in place of this path, so this path is not
  uploaded. A runtime's Dockerfile cannot be a `same_as` path.
  """
  reuse: bool
  """
  Let the API reuse an identical artifact this organization uploaded in an earlier submission.
  Reused paths are returned in `reused` and must not be uploaded. This flag is not part of the
  declaration or the upload digest. A runtime's Dockerfile cannot be reused.
  """


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
