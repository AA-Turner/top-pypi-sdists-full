# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any

import httpx2

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
    start_step_index: int | None | Omit = omit,
    cursor: str | None | Omit = omit,
    limit: int | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> SyncPage[Step]:
    """Steps

    Args:
      start_step_index: Begin the page at this step index. Cannot be combined with cursor.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(trajectory_id, str) and not trajectory_id:
      raise ValueError(
        f"Expected a non-empty value for `trajectory_id` but received {trajectory_id!r}"
      )
    page = self._get(
      path_template(
        "/api/v1/trajectories/{trajectory_id}/steps",
        trajectory_id=trajectory_id,
      ),
      cast_to=SyncPage[Step],
      options=make_request_options(
        params=maybe_transform(
          {
            "start_step_index": start_step_index,
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
    # The cursor carries the position, and the API rejects it combined with start_step_index.
    page._options = page._options.model_copy(
      update={
        "params": {
          key: value for key, value in page._options.params.items() if key != "start_step_index"
        }
      }
    )
    return page


class StepsWithRawResponse:
  def __init__(self, resource: Steps) -> None:
    self._resource = resource
    self.list = to_raw_response_wrapper(resource.list)
