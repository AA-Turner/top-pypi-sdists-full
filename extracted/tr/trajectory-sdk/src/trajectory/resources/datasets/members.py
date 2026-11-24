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
from trajectory.types.datasets.members.dataset_member import DatasetMember


class Members(APIResource):
  @cached_property
  def with_raw_response(self) -> MembersWithRawResponse:
    return MembersWithRawResponse(self)

  def list(
    self,
    dataset_id: str,
    *,
    cursor: str | None | Omit = omit,
    limit: int | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> SyncPage[DatasetMember]:
    """List a dataset's members in trajectory ID order, with their train or heldout split.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(dataset_id, str) and not dataset_id:
      raise ValueError(f"Expected a non-empty value for `dataset_id` but received {dataset_id!r}")
    return self._get(
      path_template(
        "/api/v1/datasets/{dataset_id}/members",
        dataset_id=dataset_id,
      ),
      cast_to=SyncPage[DatasetMember],
      options=make_request_options(
        params=maybe_transform(
          {
            "cursor": omit if cursor is None else cursor,
            "limit": limit,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class MembersWithRawResponse:
  def __init__(self, resource: Members) -> None:
    self._resource = resource
    self.list = to_raw_response_wrapper(resource.list)
