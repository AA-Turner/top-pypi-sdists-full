# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class DeleteBenchmarkResponse(BaseModel):
  bench_id: str
  """ID of the deleted benchmark."""
