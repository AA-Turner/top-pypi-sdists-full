# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Literal

import httpx2

from trajectory._base_client import make_request_options
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.types.billing_run_costs_response import BillingRunCostsResponse


class Billing(APIResource):
  @cached_property
  def with_raw_response(self) -> BillingWithRawResponse:
    return BillingWithRawResponse(self)

  def list_run_costs(
    self,
    *,
    offset: int | Omit = omit,
    limit: int | Omit = omit,
    sort: Literal["cents", "launch_at"] | Omit = omit,
    order: Literal["asc", "desc"] | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> BillingRunCostsResponse:
    """List this organization's cached run costs in USD cents over the last 30 calendar days.
    Includes training, inference, grading, and sandbox costs; older runs show only costs
    incurred within that window. Free organizations show usage at list price, not charges.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/billing/usage/runs",
      cast_to=BillingRunCostsResponse,
      options=make_request_options(
        params=maybe_transform(
          {
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "order": order,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class BillingWithRawResponse:
  def __init__(self, resource: Billing) -> None:
    self._resource = resource
    self.list_run_costs = to_raw_response_wrapper(resource.list_run_costs)
