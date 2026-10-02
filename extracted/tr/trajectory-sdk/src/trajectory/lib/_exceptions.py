from __future__ import annotations

from trajectory._exceptions import TrajectoryError
from trajectory._models import BaseModel
from trajectory.types.batch_item_failure import BatchItemFailure


class WorkflowError(TrajectoryError):
  """A lib workflow could not safely continue after a completed API call."""

  def __init__(
    self,
    message: str,
    *,
    failures: list[BatchItemFailure],
    partial_result: BaseModel | None = None,
  ) -> None:
    super().__init__(message)
    self.message = message
    self.failures = failures
    self.partial_result = partial_result


class BenchmarkImageBuildError(WorkflowError):
  """A benchmark image-build workflow failed."""


class BenchmarkImageBuildTimeoutError(BenchmarkImageBuildError):
  """Benchmark image builds did not reach a terminal state before the deadline."""


class FileUploadError(TrajectoryError):
  """A signed file upload could not be completed."""

  def __init__(
    self,
    message: str,
    *,
    path: str | None = None,
    status_code: int | None = None,
  ) -> None:
    super().__init__(message)
    self.message = message
    self.path = path
    self.status_code = status_code
