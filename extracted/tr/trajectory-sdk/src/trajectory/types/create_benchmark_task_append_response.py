# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime

from trajectory._models import BaseModel
from trajectory.types.benchmark_upload_url import BenchmarkUploadUrl


class CreateBenchmarkTaskAppendResponse(BaseModel):
  bench_id: str

  batch_id: str

  urls: list[BenchmarkUploadUrl]

  expires_at: datetime
