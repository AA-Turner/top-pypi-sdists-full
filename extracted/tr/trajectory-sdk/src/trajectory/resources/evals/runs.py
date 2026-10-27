# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Iterable, Literal

import httpx2

from trajectory._base_client import SyncPage, make_request_options, path_template, serialize_header
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
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
    status: Iterable[
      Literal["pending", "registered", "running", "completed", "failed", "cancelled"]
    ]
    | None
    | Omit = omit,
    training_run_id: str | None | Omit = omit,
    base_model_slug: str | None | Omit = omit,
    cursor: str | None | Omit = omit,
    limit: int | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> SyncPage[EvalRun]:
    """List evaluation runs by creation time and ID, newest first. Cursors do not hold a
    snapshot.

    Args:
      status: Return only runs in these statuses; repeat for each status.

      training_run_id: Return only evaluations of this training run's checkpoints.

      base_model_slug: Return only runs of this base model.

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
      cast_to=SyncPage[EvalRun],
      options=make_request_options(
        params=maybe_transform(
          {
            "status": status,
            "training_run_id": training_run_id,
            "base_model_slug": base_model_slug,
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

  def retrieve(
    self,
    run_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
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
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
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
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> httpx2.Response:
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

  def resume(
    self,
    run_id: str,
    *,
    idempotency_key: str,
    retry_policy: str | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> EvalRun:
    """Resume a failed or cancelled evaluation, preserving its scored results and evaluation
    ID.

    Args:
      idempotency_key: Required. Reuse the same key when retrying this recovery request.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(run_id, str) and not run_id:
      raise ValueError(f"Expected a non-empty value for `run_id` but received {run_id!r}")
    return self._post(
      path_template(
        "/api/v1/eval/{run_id}/resume",
        run_id=run_id,
      ),
      cast_to=EvalRun,
      options=make_request_options(
        params=maybe_transform(
          {
            "retry_policy": retry_policy,
          }
        ),
        headers={
          "Idempotency-Key": serialize_header(idempotency_key),
        },
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
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
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
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
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
    self.resume = to_raw_response_wrapper(resource.resume)
    self.progress = to_raw_response_wrapper(resource.progress)
    self.retrieve_rollout_statistics = to_raw_response_wrapper(resource.retrieve_rollout_statistics)
