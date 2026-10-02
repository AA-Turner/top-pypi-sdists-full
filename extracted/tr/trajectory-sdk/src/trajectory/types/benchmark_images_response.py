# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class BenchmarkImage(BaseModel):
  task_id: str

  provider: str

  provider_ref: str | None = None

  dockerfile_uri: str | None = None

  build_status: str | None = None

  failure_message: str | None = None
  """Bounded public-safe diagnostic for the failed runtime build."""


class BenchmarkImagesResponse(BaseModel):
  bench_id: str

  images: list[BenchmarkImage]
