# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any

import httpx

from trajectory._base_client import SyncPage, make_request_options, path_template
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.types.trajectories.steps.step import Step


class Steps(APIResource):
  @cached_property
  def with_raw_response(self) -> StepsWithRawResponse:
    return StepsWithRawResponse(self)

  def list(
    self,
    trajectory_id: str,
    *,
    cursor: str | None | Omit = omit,
    limit: int | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> SyncPage[Step]:
    """Steps

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(trajectory_id, str) and not trajectory_id:
      raise ValueError(
        f"Expected a non-empty value for `trajectory_id` but received {trajectory_id!r}"
      )
    return self._get(
      path_template(
        "/api/v1/trajectories/{trajectory_id}/steps",
        trajectory_id=trajectory_id,
      ),
      cast_to=SyncPage[Step],
      options=make_request_options(
        params=maybe_transform(
          {
            "cursor": cursor,
            "limit": limit,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class StepsWithRawResponse:
  def __init__(self, resource: Steps) -> None:
    self._resource = resource
    self.list = to_raw_response_wrapper(resource.list)
