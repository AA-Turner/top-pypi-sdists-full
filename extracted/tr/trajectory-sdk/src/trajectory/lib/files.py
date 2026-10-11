"""Shared primitives for uploading files through signed URLs."""

from __future__ import annotations

from contextlib import nullcontext

import httpx2

from trajectory.lib.upload_file import UploadFile as UploadFile
from trajectory.lib.upload_pool import DEFAULT_UPLOAD_CONCURRENCY, UploadPool
from trajectory.lib.upload_pool import DEFAULT_UPLOAD_TIMEOUT as DEFAULT_UPLOAD_TIMEOUT
from trajectory.lib.upload_pool import UPLOAD_BATCH_FILES as UPLOAD_BATCH_FILES
from trajectory.lib.upload_progress import NO_UPLOAD_PROGRESS, UploadProgress
from trajectory.types.benchmark_upload_url import BenchmarkUploadUrl


def put_files(
  files: list[UploadFile],
  urls: list[BenchmarkUploadUrl],
  *,
  http_client: httpx2.Client | None = None,
  timeout: float | None = DEFAULT_UPLOAD_TIMEOUT,
  max_retries: int = 2,
  max_concurrency: int = DEFAULT_UPLOAD_CONCURRENCY,
  progress: UploadProgress = NO_UPLOAD_PROGRESS,
) -> None:
  """PUT local files to signed URLs; timeout is in seconds, or None to disable it."""
  if max_retries < 0:
    raise ValueError("max_retries must be non-negative")
  if max_concurrency <= 0:
    raise ValueError("max_concurrency must be greater than zero")
  client_context = (
    nullcontext(http_client)
    if http_client is not None
    else httpx2.Client(timeout=timeout, follow_redirects=True)
  )
  with client_context as client:
    with UploadPool(
      client,
      timeout=timeout,
      max_retries=max_retries,
      max_concurrency=max_concurrency,
      progress=progress,
    ) as pool:
      pool.add(files, urls)
      pool.finish()
