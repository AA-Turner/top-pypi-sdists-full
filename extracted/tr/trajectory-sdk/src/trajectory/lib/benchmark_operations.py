"""Reconnectable benchmark operations with bounded polling and lazy result pages."""

from __future__ import annotations

import math
import time
from collections.abc import Iterator
from typing import Any, Literal

from trajectory import BenchmarkIngestionFailure, BenchmarkIngestionOperationStatus, Client
from trajectory._exceptions import APITimeoutError

_TERMINAL = {"succeeded", "partial_failure", "failed", "cancelled"}


class BenchmarkOperationResult:
  def __init__(
    self, operation: BenchmarkOperation, status: BenchmarkIngestionOperationStatus
  ) -> None:
    self.operation = operation
    self.status = status

  def tasks(self) -> Iterator[dict[str, Any]]:
    return self.operation.pages("result")

  def failures(self) -> Iterator[BenchmarkIngestionFailure]:
    for item in self.operation.pages("failure"):
      failure = BenchmarkIngestionFailure.model_validate(item)
      if not failure.resolved:
        yield failure

  def runtimes(self) -> Iterator[dict[str, Any]]:
    return self.operation.pages("runtime")

  def affected_tasks(
    self, runtime_id: str, *, cursor: str | None = None
  ) -> Iterator[dict[str, Any]]:
    for item in self.operation.pages("runtime_task", after=cursor or f"{runtime_id}."):
      if item["runtime_id"] != runtime_id:
        return
      yield item


class BenchmarkOperationError(RuntimeError):
  def __init__(self, result: BenchmarkOperationResult) -> None:
    super().__init__(f"Benchmark operation {result.status.operation_id}: {result.status.status}")
    self.partial_result = result

  @property
  def failures(self) -> Iterator[BenchmarkIngestionFailure]:
    return self.partial_result.failures()


class BenchmarkPartialFailureError(BenchmarkOperationError):
  """Registration or runtime building completed with structured, paginated failures."""


class BenchmarkOperation:
  def __init__(
    self, client: Client, operation_id: str, status: BenchmarkIngestionOperationStatus | None = None
  ) -> None:
    if not isinstance(operation_id, str) or not operation_id:
      raise ValueError("operation_id must be a non-empty string")
    self.client = client
    self.id = operation_id
    self.status = status

  def refresh(self) -> BenchmarkIngestionOperationStatus:
    self.status = self.client.benchmarks.ingestion.retrieve(self.id)
    return self.status

  def result(
    self, timeout: float | None = 1800, poll_interval: float = 2
  ) -> BenchmarkOperationResult:
    if timeout is not None and (timeout < 0 or not math.isfinite(timeout)):
      raise ValueError("timeout must be finite and non-negative, or None")
    if poll_interval <= 0 or not math.isfinite(poll_interval):
      raise ValueError("poll_interval must be positive and finite")
    deadline = None if timeout is None else time.monotonic() + timeout
    while self.status is None or self.status.status not in _TERMINAL:
      remaining = None if deadline is None else deadline - time.monotonic()
      if remaining is not None and remaining <= 0:
        raise TimeoutError(f"Timed out waiting for {self.id}; server processing continues")
      client = (
        self.client
        if remaining is None
        else self.client.with_options(timeout=remaining, max_retries=0)
      )
      try:
        self.status = client.benchmarks.ingestion.retrieve(self.id)
      except APITimeoutError as error:
        if deadline is None:
          time.sleep(poll_interval)
          continue
        raise TimeoutError(
          f"Timed out waiting for {self.id}; server processing continues"
        ) from error
      if self.status.status not in _TERMINAL:
        remaining = poll_interval if deadline is None else max(0, deadline - time.monotonic())
        time.sleep(min(poll_interval, remaining))
    result = BenchmarkOperationResult(self, self.status)
    if self.status.status == "partial_failure":
      raise BenchmarkPartialFailureError(result)
    if self.status.status in {"failed", "cancelled"}:
      raise BenchmarkOperationError(result)
    return result

  def pages(
    self, kind: Literal["result", "failure", "runtime", "runtime_task"], *, after: str = ""
  ) -> Iterator[dict[str, Any]]:
    while True:
      page = self.client.benchmarks.ingestion.list_items(self.id, kind, after=after, limit=100)
      for item in page.items:
        yield item.model_dump(exclude_unset=True)
      cursor = page.next_cursor
      if cursor is None:
        return
      if cursor == after:
        raise RuntimeError("Operation result pagination did not advance")
      after = cursor
