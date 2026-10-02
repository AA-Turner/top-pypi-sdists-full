# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any

import httpx

from trajectory._base_client import make_request_options
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, not_given


class Organizations(APIResource):
  @cached_property
  def with_raw_response(self) -> OrganizationsWithRawResponse:
    return OrganizationsWithRawResponse(self)

  def retrieve_current(
    self,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> dict[str, str]:
    """The caller's resolved tenant; lets API-key clients assert their org cheaply.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/organizations/current",
      cast_to=dict[str, str],
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class OrganizationsWithRawResponse:
  def __init__(self, resource: Organizations) -> None:
    self._resource = resource
    self.retrieve_current = to_raw_response_wrapper(resource.retrieve_current)
