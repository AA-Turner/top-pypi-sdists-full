# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel
from trajectory.types.benchmarks.ingestion.benchmark_ingestion_failure import (
  BenchmarkIngestionFailure,
)


class BenchmarkIngestionRuntimeResult(BaseModel):
  runtime_id: str

  status: Literal["pending", "building", "ready", "failed"]

  provider_ref: str | None = None


class BenchmarkIngestionTaskResult(BaseModel):
  task_id: str

  name: str

  runtime_id: str

  action: Literal["added", "updated", "skipped"]


class BenchmarkIngestionOperationPage(BaseModel):
  items: list[
    BenchmarkIngestionTaskResult | BenchmarkIngestionRuntimeResult | BenchmarkIngestionFailure
  ]

  next_cursor: str | None
