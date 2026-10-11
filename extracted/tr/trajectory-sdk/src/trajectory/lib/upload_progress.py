"""Shared no-op handler for file upload progress."""

from __future__ import annotations


class UploadProgress:
  """No-op transfer handler; reporting handlers override these hooks."""

  interval: float | None = None

  def start_file(self, path: str, size: int) -> None:
    pass

  def bytes_sent(self, path: str, size: int) -> None:
    pass

  def retry(self, path: str) -> None:
    pass

  def completed(self, path: str, size: int) -> None:
    pass

  def emit(self, *, force: bool = False) -> None:
    pass


NO_UPLOAD_PROGRESS = UploadProgress()
