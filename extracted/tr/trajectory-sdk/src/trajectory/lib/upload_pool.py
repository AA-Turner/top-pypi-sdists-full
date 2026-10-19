"""Bounded workers shared by signed file upload workflows."""

from __future__ import annotations

import base64
import hashlib
import random
import threading
import time
from collections.abc import Callable, Iterator
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from uuid import uuid4

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
# Total waiting between attempts of one allocation or upload, so throttling costs minutes.
RETRY_WAIT_BUDGET_SECONDS = 4.5 * 60
# Matches the generated client's backoff: capped, jittered, and honoring Retry-After up to 2 min.
_INITIAL_RETRY_DELAY = 0.5
_MAX_RETRY_DELAY = 8.0
_MAX_RETRY_AFTER = 120.0
# Client clocks can run behind GCS, so stop starting form uploads this long before expiry.
_POLICY_EXPIRY_MARGIN = timedelta(seconds=60)

# Seconds a response asks the client to wait, such as the generated client's Retry-After parser.
RetryAfterParser = Callable[[httpx2.Response], float | None]


class RetryBudget:
  """Jittered, capped backoff that honors Retry-After, bounded by retries and total waiting."""

  def __init__(
    self,
    max_retries: int,
    parse_retry_after: RetryAfterParser | None = None,
    wait_seconds: float = RETRY_WAIT_BUDGET_SECONDS,
  ) -> None:
    self.retries_left = max_retries
    self.parse_retry_after = parse_retry_after
    self.wait_left = wait_seconds
    self.attempt = 0

  def take_retry_delay(self, response: httpx2.Response | None = None) -> float | None:
    """Seconds to wait before the next attempt, or None when the budget is spent."""
    if self.retries_left <= 0 or self.wait_left <= 0:
      return None
    delay = min(self._get_delay(response), self.wait_left)
    self.retries_left -= 1
    self.wait_left -= delay
    self.attempt += 1
    return delay

  def _get_delay(self, response: httpx2.Response | None) -> float:
    if response is not None and self.parse_retry_after is not None:
      retry_after = self.parse_retry_after(response)
      if retry_after is not None and 0 < retry_after <= _MAX_RETRY_AFTER:
        return retry_after
    delay = min(_INITIAL_RETRY_DELAY * 2**self.attempt, _MAX_RETRY_DELAY)
    return delay * (1 - 0.25 * random.random())


@dataclass(frozen=True)
class _FormUpload:
  """One file's signed form POST: endpoint, policy expiry, and the fields sent before the file."""

  url: str
  fields: dict[str, str]
  expires_at: datetime


class UploadPool:
  """Bounded, shared PUT workers for successive signed URL allocations."""

  def __init__(
    self,
    client: httpx2.Client,
    timeout: float | None,
    max_retries: int,
    max_concurrency: int,
    progress: UploadProgress = NO_UPLOAD_PROGRESS,
    parse_retry_after: RetryAfterParser | None = None,
  ) -> None:
    if max_retries < 0:
      raise ValueError("max_retries must be non-negative")
    if max_concurrency <= 0:
      raise ValueError("max_concurrency must be greater than zero")
    self.client = client
    self.timeout = timeout
    self.max_retries = max_retries
    self.progress = progress
    self.parse_retry_after = parse_retry_after
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
    self._submit({path: (file, urls_by_path[path]) for path, file in files_by_path.items()})

  def add_with_policy(self, files: list[UploadFile], policy: dict[str, Any]) -> None:
    """Upload every file as a form POST under one signed benchmark ingestion policy."""
    uploads = {}
    for path, file in self._index_files(files).items():
      # Task parts live at the operation root; artifacts live under the artifact directory.
      prefix = policy["part_prefix"] if path.startswith("parts/") else policy["artifact_prefix"]
      fields = {**policy["fields"], "key": prefix + path, "Content-Type": file.content_type}
      expires_at = datetime.fromisoformat(policy["expires_at"])
      uploads[path] = (file, _FormUpload(policy["url"], fields, expires_at))
    self._submit(uploads)

  def _submit(
    self, uploads: dict[str, tuple[UploadFile, BenchmarkUploadUrl | _FormUpload]]
  ) -> None:
    for path, (file, target) in uploads.items():
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
      future = self.pool.submit(self._start_put, file, target)
      self.pending[future] = file
    # Report successful files and surface failures between allocations without waiting.
    self._drain_completed(timeout=0)

  def _over_byte_budget(self, file: UploadFile) -> bool:
    return self.waiting_bytes > 0 and self.waiting_bytes + file.size_bytes > MAX_WAITING_BYTES

  def _start_put(self, file: UploadFile, target: BenchmarkUploadUrl | _FormUpload) -> None:
    # Only bytes still waiting for a worker count against the budget; running uploads do not.
    with self.upload_started:
      self.waiting_bytes -= file.size_bytes
      self.upload_started.notify_all()
    if isinstance(target, _FormUpload):
      self._post_file(
        self.client,
        file,
        target,
        timeout=self.timeout,
        max_retries=self.max_retries,
        progress=self.progress,
        parse_retry_after=self.parse_retry_after,
      )
      return
    self._put_file(
      self.client,
      file,
      target,
      timeout=self.timeout,
      max_retries=self.max_retries,
      progress=self.progress,
      parse_retry_after=self.parse_retry_after,
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
    parse_retry_after: RetryAfterParser | None = None,
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
    UploadPool._send_with_retries(
      file,
      lambda: client.put(
        upload_url.url,
        content=_ReplayableUploadStream(file, progress),
        headers=headers,
        follow_redirects=True,
        timeout=timeout,
      ),
      RetryBudget(max_retries, parse_retry_after),
      progress,
      # Signed PUT URLs create only new objects, so a failed precondition means it already exists.
      precondition_failed_is_success=True,
    )

  @staticmethod
  def _post_file(
    client: httpx2.Client,
    file: UploadFile,
    upload: _FormUpload,
    timeout: float | None,
    max_retries: int,
    progress: UploadProgress = NO_UPLOAD_PROGRESS,
    parse_retry_after: RetryAfterParser | None = None,
  ) -> None:
    # The policy cannot pin Content-MD5; the stream checks it and the server verifies uploads.
    def send() -> httpx2.Response:
      if datetime.now(UTC) >= upload.expires_at - _POLICY_EXPIRY_MARGIN:
        raise FileUploadError(
          f"The signed upload policy for {file.path!r} expired before its upload could start. "
          "Resubmit the benchmark.",
          path=file.path,
        )
      body = _FormUploadStream(upload.fields, file, progress)
      return client.post(
        upload.url,
        content=body,
        headers={"Content-Type": body.content_type, "Content-Length": str(body.size_bytes)},
        follow_redirects=True,
        timeout=timeout,
      )

    UploadPool._send_with_retries(file, send, RetryBudget(max_retries, parse_retry_after), progress)

  @staticmethod
  def _send_with_retries(
    file: UploadFile,
    send: Callable[[], httpx2.Response],
    budget: RetryBudget,
    progress: UploadProgress,
    precondition_failed_is_success: bool = False,
  ) -> None:
    while True:
      try:
        if isinstance(file.content, Path) and file.content.stat().st_size != file.size_bytes:
          raise file._source_changed_error("size")
        response = send()
      except OSError as error:
        raise FileUploadError(
          f"Upload source for {file.path!r} could not be read: {error}. "
          "Keep source files present and unchanged until submission finishes, then resubmit.",
          path=file.path,
        ) from error
      except httpx2.TransportError as error:
        delay = budget.take_retry_delay()
        if delay is not None:
          progress.retry(file.path)
          time.sleep(delay)
          continue
        raise FileUploadError(f"Upload of {file.path!r} failed: {error}", path=file.path) from error

      if response.is_success or (precondition_failed_is_success and response.status_code == 412):
        return
      response.close()
      retryable = response.status_code in _RETRYABLE_STATUS_CODES
      delay = budget.take_retry_delay(response) if retryable else None
      if delay is not None:
        progress.retry(file.path)
        time.sleep(delay)
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


class _FormUploadStream(httpx2.SyncByteStream):
  """A multipart/form-data body: the signed fields, then the file as the last field."""

  def __init__(
    self, fields: dict[str, str], file: UploadFile, progress: UploadProgress = NO_UPLOAD_PROGRESS
  ) -> None:
    boundary = uuid4().hex
    self.content_type = f"multipart/form-data; boundary={boundary}"
    parts = [
      f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'
      for name, value in fields.items()
    ]
    # GCS names the object by `key`, so the filename is only a multipart formality.
    parts.append(
      f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="file"\r\n'
      f"Content-Type: {file.content_type}\r\n\r\n"
    )
    self._head = "".join(parts).encode()
    self._tail = f"\r\n--{boundary}--\r\n".encode()
    self._file = _ReplayableUploadStream(file, progress)
    self.size_bytes = len(self._head) + file.size_bytes + len(self._tail)

  def __iter__(self) -> Iterator[bytes]:
    yield self._head
    yield from self._file
    yield self._tail
