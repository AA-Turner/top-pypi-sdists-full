# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, Required, TypedDict


class TelemetryEventIngestParam(TypedDict, total=False):
  event_id: Required[str]
  """
  Caller-provided unique event id used for idempotency and deduplication.
  """
  event_type: Required[str]
  """
  Product-defined telemetry event name, such as 'tool_call' or 'user_accept'.
  """
  timestamp: Required[str]
  """
  ISO 8601 timestamp for when the event occurred.
  """
  session_id: Required[str]
  """
  Grouping key for a broader user session, eval run, or import job.
  """
  source: Required[str]
  """
  Origin of the event, such as 'sdk', 'api', 'training', or 'synthetic'.
  """
  user_id: str | None
  """
  End-user identifier from the caller's system, when available.
  """
  trajectory_id: str | None
  """
  Stored trajectory id returned by trajectory upload, when already known.
  """
  trace_id: str | None
  """
  Caller-owned correlation key shared by telemetry and its trajectory.
  """
  properties: Mapping[str, Any]
  """
  Event-specific JSON properties.
  """
  metadata: Mapping[str, Any] | None
  """
  Additional metadata for debugging, SDK versions, or ingestion context.
  """


class TelemetryIngestEventsParams(TypedDict, total=False):
  events: Required[Iterable[TelemetryEventIngestParam]]
  """
  Telemetry events to ingest.
  """
