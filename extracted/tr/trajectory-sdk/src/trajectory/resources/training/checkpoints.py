# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any

import httpx

from trajectory._base_client import make_request_options, path_template
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, not_given
from trajectory.types.training.checkpoints.training_checkpoint_response import (
  TrainingCheckpointResponse,
)
from trajectory.types.training_checkpoints_response import TrainingCheckpointsResponse


class Checkpoints(APIResource):
  @cached_property
  def with_raw_response(self) -> CheckpointsWithRawResponse:
    return CheckpointsWithRawResponse(self)

  def list(
    self,
    run_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> TrainingCheckpointsResponse:
    """List every committed checkpoint produced by a training run.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(run_id, str) and not run_id:
      raise ValueError(f"Expected a non-empty value for `run_id` but received {run_id!r}")
    return self._get(
      path_template(
        "/api/v1/train/{run_id}/checkpoints",
        run_id=run_id,
      ),
      cast_to=TrainingCheckpointsResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def retrieve(
    self,
    run_id: str,
    step_index: int,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> TrainingCheckpointResponse:
    """Resolve a committed checkpoint produced by a training run.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(run_id, str) and not run_id:
      raise ValueError(f"Expected a non-empty value for `run_id` but received {run_id!r}")
    if isinstance(step_index, str) and not step_index:
      raise ValueError(f"Expected a non-empty value for `step_index` but received {step_index!r}")
    return self._get(
      path_template(
        "/api/v1/train/{run_id}/checkpoints/{step_index}",
        run_id=run_id,
        step_index=step_index,
      ),
      cast_to=TrainingCheckpointResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class CheckpointsWithRawResponse:
  def __init__(self, resource: Checkpoints) -> None:
    self._resource = resource
    self.list = to_raw_response_wrapper(resource.list)
    self.retrieve = to_raw_response_wrapper(resource.retrieve)
