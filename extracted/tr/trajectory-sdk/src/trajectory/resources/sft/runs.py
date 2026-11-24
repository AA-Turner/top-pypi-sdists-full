# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any

import httpx2

from trajectory._base_client import make_request_options, path_template
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.types.training_step_metrics_page import TrainingStepMetricsPage


class Runs(APIResource):
  @cached_property
  def with_raw_response(self) -> RunsWithRawResponse:
    return RunsWithRawResponse(self)

  def list_step_metrics(
    self,
    run_id: str,
    *,
    cursor: str | None | Omit = omit,
    limit: int | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> TrainingStepMetricsPage:
    """Trainer timing, throughput, learning rate and training loss for each committed SFT
    update.

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
        "/api/v1/train_sft/{run_id}/step-metrics",
        run_id=run_id,
      ),
      cast_to=TrainingStepMetricsPage,
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


class RunsWithRawResponse:
  def __init__(self, resource: Runs) -> None:
    self._resource = resource
    self.list_step_metrics = to_raw_response_wrapper(resource.list_step_metrics)
