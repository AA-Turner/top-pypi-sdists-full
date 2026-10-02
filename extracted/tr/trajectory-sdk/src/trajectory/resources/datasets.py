# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Literal

import httpx

from trajectory._base_client import SyncPage, make_request_options
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.types.datasets.dataset_metadata import DatasetMetadata


class Datasets(APIResource):
  @cached_property
  def with_raw_response(self) -> DatasetsWithRawResponse:
    return DatasetsWithRawResponse(self)

  def list(
    self,
    *,
    cursor: str | None | Omit = omit,
    limit: int | Omit = omit,
    sort: str | None | Omit = omit,
    order: Literal["asc", "desc"] | Omit = omit,
    search: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> SyncPage[DatasetMetadata]:
    """Datasets

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/datasets",
      cast_to=SyncPage[DatasetMetadata],
      options=make_request_options(
        params=maybe_transform(
          {
            "cursor": cursor,
            "limit": limit,
            "sort": sort,
            "order": order,
            "search": search,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class DatasetsWithRawResponse:
  def __init__(self, resource: Datasets) -> None:
    self._resource = resource
    self.list = to_raw_response_wrapper(resource.list)
