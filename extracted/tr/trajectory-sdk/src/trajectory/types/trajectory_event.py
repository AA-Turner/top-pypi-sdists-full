# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any

from trajectory._models import BaseModel


class TrajectoryEvent(BaseModel):
  event_id: str
  """Caller-owned event id, without the trajectory prefix."""

  timestamp: str
  """When the event was stored, retaining nanosecond precision."""

  step_index: int | None
  """Recorded step count when the event was stored."""

  event: Any
  """Customer-submitted event JSON, excluding telemetry metadata."""
