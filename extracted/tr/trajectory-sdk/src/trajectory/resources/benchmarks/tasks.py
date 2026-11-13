# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Literal, Mapping

import httpx2

from trajectory._base_client import SyncPage, make_request_options, path_template
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, SequenceNotStr, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.types.benchmark_task_count_response import BenchmarkTaskCountResponse
from trajectory.types.benchmark_task_diff_response import BenchmarkTaskDiffResponse
from trajectory.types.benchmarks.benchmark_spec_params import BenchmarkSpecParams
from trajectory.types.benchmarks.tasks.benchmark_spec_task import BenchmarkSpecTask
from trajectory.types.benchmarks.tasks.tasks_diff_params import TasksDiffParams


class Tasks(APIResource):
  @cached_property
  def with_raw_response(self) -> TasksWithRawResponse:
    return TasksWithRawResponse(self)

  def list(
    self,
    bench_id: str,
    *,
    task_id: SequenceNotStr[str] | None | Omit = omit,
    split: Literal["train", "test", "unassigned"] | None | Omit = omit,
    environment: Literal["setup_needed", "building", "failed", "ready"] | None | Omit = omit,
    run_id: SequenceNotStr[str] | None | Omit = omit,
    cursor: str | None | Omit = omit,
    limit: int | Omit = omit,
    sort: str | None | Omit = omit,
    order: Literal["asc", "desc"] | Omit = omit,
    search: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> SyncPage[BenchmarkSpecTask]:
    """Lists the benchmark's tasks in upload order, with appended tasks after earlier ones.
    Tasks uploaded before upload order was recorded come first, in creation order.
    `order=desc` reverses the list.

    Args:
      task_id: Return only these tasks; repeat the parameter for each task ID.

      split: Return only tasks in this split; `unassigned` selects tasks without one.

      environment: Return only tasks whose environment needs setup (missing run command or runtime
        not ready), is building, failed to build, or is ready to run.

      run_id: Return only tasks with a trajectory in one of these training or evaluation runs;
        repeat the parameter for each run ID.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(bench_id, str) and not bench_id:
      raise ValueError(f"Expected a non-empty value for `bench_id` but received {bench_id!r}")
    return self._get(
      path_template(
        "/api/v1/benchmarks/{bench_id}/tasks",
        bench_id=bench_id,
      ),
      cast_to=SyncPage[BenchmarkSpecTask],
      options=make_request_options(
        params=maybe_transform(
          {
            "task_id": task_id,
            "split": split,
            "environment": environment,
            "run_id": run_id,
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

  def count(
    self,
    bench_id: str,
    *,
    search: str | None | Omit = omit,
    split: Literal["train", "test", "unassigned"] | None | Omit = omit,
    environment: Literal["setup_needed", "building", "failed", "ready"] | None | Omit = omit,
    run_id: SequenceNotStr[str] | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkTaskCountResponse:
    """Benchmark Task Count

    Args:
      search: Count only tasks whose label, ID, user message, or category contains this text.

      split: Return only tasks in this split; `unassigned` selects tasks without one.

      environment: Return only tasks whose environment needs setup (missing run command or runtime
        not ready), is building, failed to build, or is ready to run.

      run_id: Return only tasks with a trajectory in one of these training or evaluation runs;
        repeat the parameter for each run ID.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(bench_id, str) and not bench_id:
      raise ValueError(f"Expected a non-empty value for `bench_id` but received {bench_id!r}")
    return self._get(
      path_template(
        "/api/v1/benchmarks/{bench_id}/task-count",
        bench_id=bench_id,
      ),
      cast_to=BenchmarkTaskCountResponse,
      options=make_request_options(
        params=maybe_transform(
          {
            "search": search,
            "split": split,
            "environment": environment,
            "run_id": run_id,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def diff(
    self,
    bench_id: str,
    *,
    manifest: BenchmarkSpecParams,
    artifacts: Mapping[str, str] | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkTaskDiffResponse:
    """Split submitted tasks into new tasks, tasks already stored with identical content, and
    updates whose names are stored with different content. Lets a client upload only what is
    missing or changed.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(bench_id, str) and not bench_id:
      raise ValueError(f"Expected a non-empty value for `bench_id` but received {bench_id!r}")
    return self._post(
      path_template(
        "/api/v1/benchmarks/{bench_id}/tasks/diff",
        bench_id=bench_id,
      ),
      cast_to=BenchmarkTaskDiffResponse,
      body=maybe_transform(
        {
          "manifest": manifest,
          "artifacts": artifacts,
        },
        TasksDiffParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class TasksWithRawResponse:
  def __init__(self, resource: Tasks) -> None:
    self._resource = resource
    self.list = to_raw_response_wrapper(resource.list)
    self.count = to_raw_response_wrapper(resource.count)
    self.diff = to_raw_response_wrapper(resource.diff)
