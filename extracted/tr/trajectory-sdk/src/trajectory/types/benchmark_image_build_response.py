# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class BenchmarkImageBuildResponse(BaseModel):
  """Acknowledges a build request; it does not report whether builds are pending."""

  bench_id: str
  """
    Benchmark whose image builds were requested. Builds finish asynchronously; always poll
    listBenchmarkImages, reading every page, until no image is building.
    """
