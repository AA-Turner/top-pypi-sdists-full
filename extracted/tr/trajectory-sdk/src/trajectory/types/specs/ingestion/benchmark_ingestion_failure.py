# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel


class BenchmarkIngestionFailure(BaseModel):
  stage: Literal["verifying", "registering", "building"]

  resource_type: Literal["submission", "upload", "task", "runtime"]

  resource_id: str

  code: str

  message: str

  retryable: bool

  provider_status_code: int | None = None

  affected_tasks_cursor: str | None = None

  resolved: bool = False
