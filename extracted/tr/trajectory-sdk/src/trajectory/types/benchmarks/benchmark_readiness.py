# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class BenchmarkReadiness(BaseModel):
  ready: bool
  """Whether the benchmark is fully ingested and ready to launch."""

  missing_secret_names: list[str]
  """Required organization secrets that are not available."""

  unready_task_image_counts: dict[str, int]
  """
    Task environments that are not ready, grouped by preparation status. Empty when all task
    environments are built.
    """
