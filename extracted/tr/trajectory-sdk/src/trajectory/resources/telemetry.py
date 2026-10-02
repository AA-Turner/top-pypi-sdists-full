# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Iterable

import httpx

from trajectory._base_client import make_request_options
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, not_given
from trajectory._utils import maybe_transform
from trajectory.types.telemetry.telemetry_ingest_events_params import (
  TelemetryEventIngestParam,
  TelemetryIngestEventsParams,
)
from trajectory.types.telemetry_events_ingest_response import TelemetryEventsIngestResponse


class Telemetry(APIResource):
  @cached_property
  def with_raw_response(self) -> TelemetryWithRawResponse:
    return TelemetryWithRawResponse(self)

  def ingest_events(
    self,
    *,
    events: Iterable[TelemetryEventIngestParam],
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> TelemetryEventsIngestResponse:
    """Ingest Events

    Args:
      events: Telemetry events to ingest.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/telemetry/events",
      cast_to=TelemetryEventsIngestResponse,
      body=maybe_transform(
        {
          "events": events,
        },
        TelemetryIngestEventsParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class TelemetryWithRawResponse:
  def __init__(self, resource: Telemetry) -> None:
    self._resource = resource
    self.ingest_events = to_raw_response_wrapper(resource.ingest_events)
