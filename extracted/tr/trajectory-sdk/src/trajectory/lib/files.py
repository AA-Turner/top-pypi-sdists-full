"""Shared primitives for uploading files through signed URLs."""

from __future__ import annotations

import base64
import hashlib
import mimetypes
import re
import time
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from contextlib import nullcontext
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path
from typing import BinaryIO

import httpx

from trajectory.lib._exceptions import FileUploadError
from trajectory.types.benchmark_upload_url import BenchmarkUploadUrl
from trajectory.types.benchmarks.benchmark_upload_file_param import BenchmarkUploadFileParam

_DEFAULT_CONTENT_TYPE = "text/plain"
_DEFAULT_MAX_CONCURRENCY = 8
_SUPPORTED_CONTENT_TYPES = frozenset(
  {"application/gzip", "application/json", "application/x-tar", "text/plain"}
)
_PATH_SEGMENT = re.compile(r"^[A-Za-z0-9._ @+()\[\]-]{1,255}$")
_RETRYABLE_STATUS_CODES = frozenset({408, 409, 429, 500, 502, 503, 504})
_UPLOAD_CHUNK_SIZE = 64 * 1024


@dataclass(frozen=True)
class UploadFile:
  """A local byte source and its path within a signed upload session."""

  path: str
  content: bytes | Path
  content_type: str = _DEFAULT_CONTENT_TYPE
  size_bytes: int = field(init=False)
  expected_md5: str | None = field(default=None, kw_only=True)

  def __post_init__(self) -> None:
    _validate_upload_path(self.path)
    if not isinstance(self.content_type, str) or not self.content_type:
      raise ValueError("content_type must be a non-empty string")
    if isinstance(self.content, Path):
      source = self.content.expanduser().resolve(strict=True)
      if not source.is_file():
        raise ValueError(f"Upload source {source} is not a file")
      object.__setattr__(self, "content", source)
      object.__setattr__(self, "size_bytes", source.stat().st_size)
    elif isinstance(self.content, bytes):
      object.__setattr__(self, "size_bytes", len(self.content))
    else:
      raise TypeError("UploadFile content must be bytes or a pathlib.Path")

  @classmethod
  def from_path(
    cls,
    source: str | Path,
    *,
    path: str | None = None,
    content_type: str | None = None,
  ) -> UploadFile:
    source_path = Path(source)
    return cls(
      path=path or source_path.name,
      content=source_path,
      content_type=content_type or _guess_content_type(source_path),
    )

  def declaration(self) -> BenchmarkUploadFileParam:
    return {
      "path": self.path,
      "content_type": self.content_type,
      "size_bytes": self.size_bytes,
    }

  def open(self) -> BinaryIO:
    if isinstance(self.content, bytes):
      return BytesIO(self.content)
    return self.content.open("rb")

  def _source_changed_error(self, detail: str) -> FileUploadError:
    source = str(self.content) if isinstance(self.content, Path) else "in-memory bytes"
    return FileUploadError(
      f"Upload source {source!r} for {self.path!r} changed {detail} after it was "
      "declared. Keep source files unchanged until submission finishes, then resubmit.",
      path=self.path,
    )


class _ReplayableUploadStream(httpx.SyncByteStream):
  """Reopen an upload source whenever HTTPX replays a request body."""

  def __init__(self, file: UploadFile) -> None:
    self._file = file

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
        yield chunk
    if size != self._file.size_bytes:
      raise self._file._source_changed_error("size")
    if digest is not None:
      actual_md5 = base64.b64encode(digest.digest()).decode()
      if actual_md5 != self._file.expected_md5:
        raise self._file._source_changed_error("content (MD5 checksum mismatch)")


def put_files(
  files: list[UploadFile],
  urls: list[BenchmarkUploadUrl],
  *,
  http_client: httpx.Client | None = None,
  timeout: float = 120.0,
  max_retries: int = 2,
  max_concurrency: int = _DEFAULT_MAX_CONCURRENCY,
) -> None:
  """PUT local files to matching signed URLs."""
  if max_retries < 0:
    raise ValueError("max_retries must be non-negative")
  if max_concurrency <= 0:
    raise ValueError("max_concurrency must be greater than zero")
  files_by_path = _index_files(files)
  urls_by_path = _index_urls(urls)
  if files_by_path.keys() != urls_by_path.keys():
    missing = sorted(files_by_path.keys() - urls_by_path.keys())
    unexpected = sorted(urls_by_path.keys() - files_by_path.keys())
    raise FileUploadError(
      f"Signed upload paths did not match local files; missing={missing!r}, "
      f"unexpected={unexpected!r}"
    )

  client_context = (
    nullcontext(http_client)
    if http_client is not None
    else httpx.Client(timeout=timeout, follow_redirects=True)
  )
  with client_context as client:

    def upload(item: tuple[str, UploadFile]) -> None:
      path, file = item
      _put_file(client, file, urls_by_path[path], timeout=timeout, max_retries=max_retries)

    workers = min(max_concurrency, len(files_by_path))
    if workers:
      with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(upload, files_by_path.items()))


def _put_file(
  client: httpx.Client,
  file: UploadFile,
  upload_url: BenchmarkUploadUrl,
  *,
  timeout: float,
  max_retries: int,
) -> None:
  headers = httpx.Headers(upload_url.headers)
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
      if file.expected_md5 is not None:
        # Validate before every attempt, including servers returning an early 412
        # without consuming the body. The stream also validates bytes actually sent.
        for _ in _ReplayableUploadStream(file):
          pass
      response = client.put(
        upload_url.url,
        content=_ReplayableUploadStream(file),
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
    except httpx.TransportError as error:
      if attempt < max_retries:
        _sleep_before_retry(attempt)
        continue
      raise FileUploadError(f"Upload of {file.path!r} failed: {error}", path=file.path) from error

    if response.is_success or response.status_code == 412:
      return
    if response.status_code in _RETRYABLE_STATUS_CODES and attempt < max_retries:
      response.close()
      _sleep_before_retry(attempt)
      continue
    raise FileUploadError(
      f"Upload of {file.path!r} was rejected with HTTP {response.status_code}",
      path=file.path,
      status_code=response.status_code,
    )


def _index_files(files: list[UploadFile]) -> dict[str, UploadFile]:
  indexed = {file.path: file for file in files}
  if len(indexed) != len(files):
    raise ValueError("Upload file paths must be unique")
  return indexed


def _index_urls(urls: list[BenchmarkUploadUrl]) -> dict[str, BenchmarkUploadUrl]:
  indexed = {url.path: url for url in urls}
  if len(indexed) != len(urls):
    raise FileUploadError("Signed upload URL paths must be unique")
  return indexed


def _validate_upload_path(path: str) -> None:
  if not path or path.startswith("/") or len(path) > 1024:
    raise ValueError("Upload path must be a non-empty relative POSIX path")
  if any(
    segment in {"", ".", ".."} or not _PATH_SEGMENT.fullmatch(segment)
    for segment in path.split("/")
  ):
    raise ValueError(
      f"Upload path {path!r} must contain only relative [A-Za-z0-9._ @+()[]-] segments "
      "(at most 255 characters each)"
    )


def _guess_content_type(path: Path) -> str:
  guessed = mimetypes.guess_type(path.name)[0]
  return guessed if guessed in _SUPPORTED_CONTENT_TYPES else _DEFAULT_CONTENT_TYPE


def _sleep_before_retry(attempt: int) -> None:
  time.sleep(0.5 * 2**attempt)
