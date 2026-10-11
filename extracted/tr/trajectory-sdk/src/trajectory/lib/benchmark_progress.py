"""Caller-thread progress snapshots for benchmark preparation and upload."""

from __future__ import annotations

import sys
import time
from collections.abc import Callable
from threading import Lock, get_ident
from typing import TypedDict

from tqdm import tqdm

from trajectory.lib.upload_progress import UploadProgress

_TERMINAL_STAGES = ("completed", "accepted", "error", "cancelled")


class BenchmarkProgress(TypedDict):
  """Benchmark upload progress. Totals are provisional until totals_final is true.

  uploaded_* counts completed files.
  Inflight bytes track active transfers and reset when a file is retried.
  """

  stage: str
  terminal: bool
  error: str | None
  uploaded_files: int
  uploaded_bytes: int
  total_files: int
  total_bytes: int
  totals_final: bool
  hashed_files: int
  hashed_bytes: int
  inflight_bytes: int
  retry_count: int


class _ProgressStream:
  def write(self, text: str) -> int:
    if sys.stderr is None:
      return 0
    try:
      return sys.stderr.write(text)
    except (OSError, ValueError):
      return 0  # Progress output must not hide a successful submission.

  def flush(self) -> None:
    if sys.stderr is None:
      return
    try:
      sys.stderr.flush()
    except (OSError, ValueError):
      pass


class _BenchmarkProgressDisplay:
  """Render benchmark progress and close the display when submission ends."""

  def __init__(self, *, disabled: bool = False) -> None:
    self.bar = tqdm(
      desc="Preparing benchmark",
      unit="B",
      unit_scale=True,
      file=_ProgressStream(),
      disable=disabled,
    )
    self.upload_started = False

  def __enter__(self) -> _BenchmarkProgressDisplay:
    return self

  def __exit__(self, *args: object) -> None:
    self.bar.close()

  def update(self, event: BenchmarkProgress) -> None:
    bar = self.bar
    stage = event["stage"]
    description = {
      "preparing": "Preparing benchmark",
      "hashing": "Hashing benchmark",
      "uploading": "Uploading benchmark",
      "finalizing": "Finalizing benchmark",
      "completed": "Submitted benchmark",
      "accepted": "Submitted benchmark",
      "error": "Benchmark failed",
      "cancelled": "Benchmark cancelled",
    }[stage]
    preparing = stage in {"preparing", "hashing"} or (
      stage in {"error", "cancelled"} and not self.upload_started
    )
    if preparing:
      value = event["hashed_bytes"]
      total = None
      bar.bar_format = "{desc}: {n_fmt}{unit} processed [{elapsed}{postfix}]"
    else:
      value = (
        event["total_bytes"]
        if stage == "accepted"
        else event["uploaded_bytes"] + event["inflight_bytes"]
      )
      total = event["total_bytes"]
      bar.bar_format = "{desc} [{elapsed}{postfix}]" if stage == "finalizing" else None
    bar.set_description_str(description, refresh=False)
    bar.set_postfix_str(
      f"retries={event['retry_count']}" if event["retry_count"] else "", refresh=False
    )
    if stage == "uploading" and not self.upload_started:
      bar.reset(total=total)
      self.upload_started = True
    bar.total = total
    if not bar.update(value - bar.n):
      bar.refresh()


class _SubmissionProgress(UploadProgress):
  """Keep worker updates small and deliver callbacks only on the creating thread."""

  def __init__(
    self,
    callback: Callable[[BenchmarkProgress], None] | None = None,
  ) -> None:
    self.callback = callback
    self.interval = 0.1 if callback is not None else None
    self.owner = get_ident()
    self.lock = Lock()
    self.stage = "preparing"
    self.error: str | None = None
    self.total_files = 0
    self.total_bytes = 0
    self.totals_final = False
    self.hashed_files = 0
    self.hashed_bytes = 0
    self.uploaded_files = 0
    self.uploaded_bytes = 0
    self.retry_count = 0
    self.active: dict[str, tuple[int, int]] = {}
    self.dirty = True
    self.last_emit = 0.0

  def discover(self, size: int) -> None:
    if self.callback is None:
      return
    with self.lock:
      self.total_files += 1
      self.total_bytes += size
      self.dirty = True
    self.emit()

  def hashed(self, size: int) -> None:
    if self.callback is None:
      return
    with self.lock:
      self.hashed_bytes += size
      self.dirty = True
    if get_ident() == self.owner:
      self.emit()

  def hashed_file(self) -> None:
    if self.callback is None:
      return
    with self.lock:
      self.hashed_files += 1
      self.dirty = True
    self.emit()

  def final_totals(self, files: int, size: int) -> None:
    if self.callback is None:
      return
    with self.lock:
      self.total_files = files
      self.total_bytes = size
      self.totals_final = True
      self.dirty = True
    self.emit(force=True)

  def set_stage(self, stage: str, *, error: str | None = None) -> None:
    if self.callback is None:
      return
    with self.lock:
      self.stage = stage
      self.error = error
      if stage in _TERMINAL_STAGES:
        self.active.clear()
      self.dirty = True
    self.emit(force=True)

  def start_file(self, path: str, size: int) -> None:
    if self.callback is None:
      return
    with self.lock:
      self.active[path] = (size, 0)
      self.dirty = True

  def bytes_sent(self, path: str, size: int) -> None:
    if self.callback is None:
      return
    with self.lock:
      if path in self.active:
        total, current = self.active[path]
        self.active[path] = total, min(total, current + size)
      self.dirty = True

  def retry(self, path: str) -> None:
    if self.callback is None:
      return
    with self.lock:
      self.retry_count += 1
      if path in self.active:
        total, _ = self.active[path]
        self.active[path] = total, 0
      self.dirty = True

  def completed(self, path: str, size: int) -> None:
    if self.callback is None:
      return
    with self.lock:
      self.active.pop(path, None)
      self.uploaded_files += 1
      self.uploaded_bytes += size
      self.dirty = True
    self.emit()

  def emit(self, *, force: bool = False) -> None:
    if self.callback is None:
      return
    if get_ident() != self.owner:
      raise RuntimeError("Progress callbacks must run on the submission thread")
    now = time.monotonic()
    with self.lock:
      if not self.dirty or (not force and now - self.last_emit < 0.1):
        return
      snapshot: BenchmarkProgress = {
        "stage": self.stage,
        "terminal": self.stage in _TERMINAL_STAGES,
        "error": self.error,
        "uploaded_files": self.uploaded_files,
        "uploaded_bytes": self.uploaded_bytes,
        "total_files": self.total_files,
        "total_bytes": self.total_bytes,
        "totals_final": self.totals_final,
        "hashed_files": self.hashed_files,
        "hashed_bytes": self.hashed_bytes,
        "inflight_bytes": sum(current for _, current in self.active.values()),
        "retry_count": self.retry_count,
      }
      self.dirty = False
      self.last_emit = now
    self.callback(snapshot)
