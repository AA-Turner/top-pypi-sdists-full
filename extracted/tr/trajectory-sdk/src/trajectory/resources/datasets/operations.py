# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any

import httpx2

from trajectory._base_client import make_request_options, path_template
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, not_given
from trajectory.types.datasets.operations.dataset_operation import DatasetOperation


class Operations(APIResource):
  @cached_property
  def with_raw_response(self) -> OperationsWithRawResponse:
    return OperationsWithRawResponse(self)

  def retrieve(
    self,
    operation_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> DatasetOperation:
    """Retrieve the status of an add of trajectories to a draft dataset.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(operation_id, str) and not operation_id:
      raise ValueError(
        f"Expected a non-empty value for `operation_id` but received {operation_id!r}"
      )
    return self._get(
      path_template(
        "/api/v1/datasets/operations/{operation_id}",
        operation_id=operation_id,
      ),
      cast_to=DatasetOperation,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class OperationsWithRawResponse:
  def __init__(self, resource: Operations) -> None:
    self._resource = resource
    self.retrieve = to_raw_response_wrapper(resource.retrieve)
