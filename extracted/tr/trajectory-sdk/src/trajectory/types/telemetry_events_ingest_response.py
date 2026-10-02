# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.batch_item_failure import BatchItemFailure


class TelemetryEventsIngestResponse(BaseModel):
  ingested: int
  """Number of telemetry events accepted for ingestion."""

  skipped: int = 0
  """Number of telemetry events skipped by validation."""

  failures: list[BatchItemFailure] | None = None
  """Structured batch-level ingestion failures, if any."""
