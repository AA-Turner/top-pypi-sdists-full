# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any

import httpx

from trajectory._base_client import make_request_options, path_template
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, not_given
from trajectory.types.delete_eval_run_response import DeleteEvalRunResponse
from trajectory.types.eval_progress_response import EvalProgressResponse
from trajectory.types.eval_rollout_statistics_response import EvalRolloutStatisticsResponse
from trajectory.types.evals.eval_run import EvalRun


class Runs(APIResource):
  @cached_property
  def with_raw_response(self) -> RunsWithRawResponse:
    return RunsWithRawResponse(self)

  def list(
    self,
    bench_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> list[EvalRun]:
    """List Eval Runs Route

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(bench_id, str) and not bench_id:
      raise ValueError(f"Expected a non-empty value for `bench_id` but received {bench_id!r}")
    return self._get(
      path_template(
        "/api/v1/eval/{bench_id}/runs",
        bench_id=bench_id,
      ),
      cast_to=list[EvalRun],
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
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> EvalRun:
    """Get Eval Run Route

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
        "/api/v1/eval/{run_id}",
        run_id=run_id,
      ),
      cast_to=EvalRun,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def delete(
    self,
    run_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> DeleteEvalRunResponse:
    """Delete Eval Run Route

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(run_id, str) and not run_id:
      raise ValueError(f"Expected a non-empty value for `run_id` but received {run_id!r}")
    return self._delete(
      path_template(
        "/api/v1/eval/{run_id}",
        run_id=run_id,
      ),
      cast_to=DeleteEvalRunResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def cancel(
    self,
    run_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> httpx.Response:
    """Cancel a pending or running evaluation.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(run_id, str) and not run_id:
      raise ValueError(f"Expected a non-empty value for `run_id` but received {run_id!r}")
    return self._post(
      path_template(
        "/api/v1/eval/{run_id}/cancel",
        run_id=run_id,
      ),
      cast_to=None,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def progress(
    self,
    run_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> EvalProgressResponse:
    """Get Eval Progress Route

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
        "/api/v1/eval/{run_id}/progress",
        run_id=run_id,
      ),
      cast_to=EvalProgressResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def retrieve_rollout_statistics(
    self,
    run_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> EvalRolloutStatisticsResponse:
    """Get Eval Rollout Statistics Route

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
        "/api/v1/eval/{run_id}/rollout-statistics",
        run_id=run_id,
      ),
      cast_to=EvalRolloutStatisticsResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class RunsWithRawResponse:
  def __init__(self, resource: Runs) -> None:
    self._resource = resource
    self.list = to_raw_response_wrapper(resource.list)
    self.retrieve = to_raw_response_wrapper(resource.retrieve)
    self.delete = to_raw_response_wrapper(resource.delete)
    self.cancel = to_raw_response_wrapper(resource.cancel)
    self.progress = to_raw_response_wrapper(resource.progress)
    self.retrieve_rollout_statistics = to_raw_response_wrapper(resource.retrieve_rollout_statistics)
