# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory._models import BaseModel


class BenchmarkImage(BaseModel):
  task_id: str

  provider: str

  provider_ref: str | None = None

  dockerfile_uri: str | None = None

  build_status: str | None = None


class BenchmarkImagesPage(SyncPage[BenchmarkImage]):
  items: list[BenchmarkImage]

  next_cursor: str | None = None

  has_more: bool

  bench_id: str
  """Benchmark whose task images are returned."""
