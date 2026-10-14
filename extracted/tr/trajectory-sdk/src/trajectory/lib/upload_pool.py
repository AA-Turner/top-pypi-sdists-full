"""Bounded workers shared by signed file upload workflows."""

from __future__ import annotations

import base64
import hashlib
import threading
import time
from collections.abc import Iterator
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from pathlib import Path

import httpx2

from trajectory.lib._exceptions import FileUploadError
from trajectory.lib.upload_file import UploadFile
from trajectory.lib.upload_progress import NO_UPLOAD_PROGRESS, UploadProgress
from trajectory.types.benchmark_upload_url import BenchmarkUploadUrl

UPLOAD_BATCH_FILES = 64
DEFAULT_UPLOAD_TIMEOUT = 60 * 60.0
DEFAULT_UPLOAD_CONCURRENCY = 8
BENCHMARK_UPLOAD_CONCURRENCY = 64
# Room for two 1,000-file allocation batches ahead of completed PUTs.
MAX_PENDING_FILES = 2 * 1000
# Signed URLs expire after 60 minutes, so bytes waiting for a worker are bounded too.
MAX_WAITING_BYTES = 4 * 1024 * 1024 * 1024

_RETRYABLE_STATUS_CODES = frozenset({408, 409, 429, 500, 502, 503, 504})
_UPLOAD_CHUNK_SIZE = 64 * 1024


class UploadPool:
  """Bounded, shared PUT workers for successive signed URL allocations."""

  def __init__(
    self,
    client: httpx2.Client,
    timeout: float | None,
    max_retries: int,
    max_concurrency: int,
    progress: UploadProgress = NO_UPLOAD_PROGRESS,
  ) -> None:
    if max_retries < 0:
      raise ValueError("max_retries must be non-negative")
    if max_concurrency <= 0:
      raise ValueError("max_concurrency must be greater than zero")
    self.client = client
    self.timeout = timeout
    self.max_retries = max_retries
    self.progress = progress
    self.pool = ThreadPoolExecutor(max_workers=max_concurrency)
    self.pending: dict[Future[None], UploadFile] = {}
    self.max_pending = max(MAX_PENDING_FILES, max_concurrency)
    self.waiting_bytes = 0
    self.upload_started = threading.Condition()

  def __enter__(self) -> UploadPool:
    return self

  def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
    if exc_type is not None:
      for future in self.pending:
        future.cancel()
    self.pool.shutdown(wait=True, cancel_futures=exc_type is not None)

  def add(self, files: list[UploadFile], urls: list[BenchmarkUploadUrl]) -> None:
    files_by_path = self._index_files(files)
    urls_by_path = self._index_urls(urls)
    if files_by_path.keys() != urls_by_path.keys():
      missing = sorted(files_by_path.keys() - urls_by_path.keys())
      unexpected = sorted(urls_by_path.keys() - files_by_path.keys())
      raise FileUploadError(
        f"Signed upload paths did not match local files; missing={missing!r}, "
        f"unexpected={unexpected!r}"
      )
    for path, file in files_by_path.items():
      while len(self.pending) >= self.max_pending or self._over_byte_budget(file):
        if len(self.pending) >= self.max_pending:
          self._drain_completed()
          continue
        # Starting an upload frees byte budget, so wait for a start rather than a completion.
        with self.upload_started:
          self.upload_started.wait_for(
            lambda: not self._over_byte_budget(file), self.progress.interval
          )
        self._drain_completed(timeout=0)
      self.progress.start_file(path, file.size_bytes)
      with self.upload_started:
        self.waiting_bytes += file.size_bytes
      future = self.pool.submit(self._start_put, file, urls_by_path[path])
      self.pending[future] = file
    # Report successful files and surface failures between allocations without waiting.
    self._drain_completed(timeout=0)

  def _over_byte_budget(self, file: UploadFile) -> bool:
    return self.waiting_bytes > 0 and self.waiting_bytes + file.size_bytes > MAX_WAITING_BYTES

  def _start_put(self, file: UploadFile, upload_url: BenchmarkUploadUrl) -> None:
    # Only bytes still waiting for a worker count against the budget; running uploads do not.
    with self.upload_started:
      self.waiting_bytes -= file.size_bytes
      self.upload_started.notify_all()
    self._put_file(
      self.client,
      file,
      upload_url,
      timeout=self.timeout,
      max_retries=self.max_retries,
      progress=self.progress,
    )

  def finish(self) -> None:
    while self.pending:
      self._drain_completed()

  def _drain_completed(self, timeout: float | None = None) -> None:
    if not self.pending:
      return
    if timeout is None:
      timeout = self.progress.interval
    done, _ = wait(self.pending, timeout=timeout, return_when=FIRST_COMPLETED)
    for future in done:
      file = self.pending.pop(future)
      future.result()
      self.progress.completed(file.path, file.size_bytes)
    self.progress.emit()

  @staticmethod
  def _put_file(
    client: httpx2.Client,
    file: UploadFile,
    upload_url: BenchmarkUploadUrl,
    timeout: float | None,
    max_retries: int,
    progress: UploadProgress = NO_UPLOAD_PROGRESS,
  ) -> None:
    headers = httpx2.Headers(upload_url.headers)
    if "Content-Type" not in headers:
      headers["Content-Type"] = file.content_type
    if "Content-Length" not in headers:
      headers["Content-Length"] = str(file.size_bytes)
    if file.expected_md5 is not None:
      if headers.get("Content-MD5", file.expected_md5) != file.expected_md5:
        raise FileUploadError(
          f"Signed Content-MD5 for {file.path!r} does not match its declared checksum",
          path=file.path,
        )
      headers["Content-MD5"] = file.expected_md5
    for attempt in range(max_retries + 1):
      try:
        if isinstance(file.content, Path) and file.content.stat().st_size != file.size_bytes:
          raise file._source_changed_error("size")
        response = client.put(
          upload_url.url,
          content=_ReplayableUploadStream(file, progress),
          headers=headers,
          follow_redirects=True,
          timeout=timeout,
        )
      except OSError as error:
        raise FileUploadError(
          f"Upload source for {file.path!r} could not be read: {error}. "
          "Keep source files present and unchanged until submission finishes, then resubmit.",
          path=file.path,
        ) from error
      except httpx2.TransportError as error:
        if attempt < max_retries:
          progress.retry(file.path)
          UploadPool._sleep_before_retry(attempt)
          continue
        raise FileUploadError(f"Upload of {file.path!r} failed: {error}", path=file.path) from error

      if response.is_success or response.status_code == 412:
        return
      if response.status_code in _RETRYABLE_STATUS_CODES and attempt < max_retries:
        response.close()
        progress.retry(file.path)
        UploadPool._sleep_before_retry(attempt)
        continue
      raise FileUploadError(
        f"Upload of {file.path!r} was rejected with HTTP {response.status_code}",
        path=file.path,
        status_code=response.status_code,
      )

  @staticmethod
  def _index_files(files: list[UploadFile]) -> dict[str, UploadFile]:
    indexed = {file.path: file for file in files}
    if len(indexed) != len(files):
      raise ValueError("Upload file paths must be unique")
    return indexed

  @staticmethod
  def _index_urls(urls: list[BenchmarkUploadUrl]) -> dict[str, BenchmarkUploadUrl]:
    indexed = {url.path: url for url in urls}
    if len(indexed) != len(urls):
      raise FileUploadError("Signed upload URL paths must be unique")
    return indexed

  @staticmethod
  def _sleep_before_retry(attempt: int) -> None:
    time.sleep(0.5 * 2**attempt)


class _ReplayableUploadStream(httpx2.SyncByteStream):
  """Reopen an upload source whenever HTTPX replays a request body."""

  def __init__(self, file: UploadFile, progress: UploadProgress = NO_UPLOAD_PROGRESS) -> None:
    self._file = file
    self.progress = progress

  def __iter__(self) -> Iterator[bytes]:
    digest = hashlib.md5(usedforsecurity=False) if self._file.expected_md5 is not None else None
    size = 0
    with self._file.open() as content:
      while chunk := content.read(_UPLOAD_CHUNK_SIZE):
        size += len(chunk)
        if size > self._file.size_bytes:
          raise self._file._source_changed_error("size")
        if digest is not None:
          digest.update(chunk)
        self.progress.bytes_sent(self._file.path, len(chunk))
        yield chunk
    if size != self._file.size_bytes:
      raise self._file._source_changed_error("size")
    if digest is not None:
      actual_md5 = base64.b64encode(digest.digest()).decode()
      if actual_md5 != self._file.expected_md5:
        raise self._file._source_changed_error("content (MD5 checksum mismatch)")
