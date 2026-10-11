"""Local byte sources for signed file uploads."""

from __future__ import annotations

import mimetypes
import re
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path
from typing import BinaryIO

from trajectory.lib._exceptions import FileUploadError
from trajectory.types.benchmarks.benchmark_upload_file_param import BenchmarkUploadFileParam

_DEFAULT_CONTENT_TYPE = "text/plain"
_SUPPORTED_CONTENT_TYPES = frozenset(
  {"application/gzip", "application/json", "application/x-tar", "text/plain"}
)
_UNSAFE_PATH_CHARACTER = re.compile(r"[\\\x00-\x1f\x7f-\x9f\ud800-\udfff]")


@dataclass(frozen=True)
class UploadFile:
  """A local byte source and its path within a signed upload session."""

  path: str
  content: bytes | Path
  content_type: str = _DEFAULT_CONTENT_TYPE
  size_bytes: int = field(init=False)
  expected_md5: str | None = field(default=None, kw_only=True)

  def __post_init__(self) -> None:
    self._validate_path(self.path)
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
      content_type=content_type or cls._guess_content_type(source_path),
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

  @staticmethod
  def _validate_path(path: str) -> None:
    if (
      not path
      or _UNSAFE_PATH_CHARACTER.search(path)
      or path.startswith("/")
      or re.match(r"^[A-Za-z]:", path)
      or len(path.encode("utf-8")) > 1024
    ):
      raise ValueError(
        "Upload path must be a non-empty relative POSIX path without control characters"
      )
    if any(
      segment in {"", ".", ".."} or len(segment.encode("utf-8")) > 255
      for segment in path.split("/")
    ):
      raise ValueError(
        "Upload path segments must be non-empty, not '.' or '..', and at most 255 UTF-8 bytes"
      )

  @staticmethod
  def _guess_content_type(path: Path) -> str:
    guessed = mimetypes.guess_type(path.name)[0]
    return guessed if guessed in _SUPPORTED_CONTENT_TYPES else _DEFAULT_CONTENT_TYPE
