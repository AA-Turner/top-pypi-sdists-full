# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any

import httpx2

from trajectory._base_client import make_request_options, path_template, serialize_header
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.types.inference.operations.chat_inference_operation_input_param import (
  ChatInferenceOperationInputParam,
)
from trajectory.types.inference.operations.inference_operation_response import (
  InferenceOperationResponse,
)
from trajectory.types.inference.operations.responses_inference_operation_input_param import (
  ResponsesInferenceOperationInputParam,
)


class Operations(APIResource):
  @cached_property
  def with_raw_response(self) -> OperationsWithRawResponse:
    return OperationsWithRawResponse(self)

  def create(
    self,
    *,
    x_trajectory_id: str,
    idempotency_key: str,
    body: ChatInferenceOperationInputParam | ResponsesInferenceOperationInputParam,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> InferenceOperationResponse:
    """Submit Inference Operation

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/inference/operations",
      cast_to=InferenceOperationResponse,
      body=maybe_transform(
        body, ChatInferenceOperationInputParam | ResponsesInferenceOperationInputParam
      ),
      options=make_request_options(
        headers={
          "X-Trajectory-Id": serialize_header(x_trajectory_id),
          "Idempotency-Key": serialize_header(idempotency_key),
        },
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def retrieve(
    self,
    inference_operation_id: str,
    *,
    wait_seconds: float | Omit = omit,
    x_trajectory_id: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> InferenceOperationResponse:
    """Get By Inference Operation

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(inference_operation_id, str) and not inference_operation_id:
      raise ValueError(
        f"Expected a non-empty value for `inference_operation_id` but received {inference_operation_id!r}"
      )
    return self._get(
      path_template(
        "/api/v1/inference/operations/{inference_operation_id}",
        inference_operation_id=inference_operation_id,
      ),
      cast_to=InferenceOperationResponse,
      options=make_request_options(
        params=maybe_transform(
          {
            "wait_seconds": wait_seconds,
          }
        ),
        headers={
          "X-Trajectory-Id": serialize_header(x_trajectory_id),
        },
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class OperationsWithRawResponse:
  def __init__(self, resource: Operations) -> None:
    self._resource = resource
    self.create = to_raw_response_wrapper(resource.create)
    self.retrieve = to_raw_response_wrapper(resource.retrieve)
