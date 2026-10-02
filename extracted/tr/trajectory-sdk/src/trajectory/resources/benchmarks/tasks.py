# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Iterable, Mapping

import httpx

from trajectory._base_client import make_request_options, path_template, serialize_header
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.types.benchmark_task_append_result import BenchmarkTaskAppendResult
from trajectory.types.benchmark_task_count_response import BenchmarkTaskCountResponse
from trajectory.types.benchmark_task_diff_response import BenchmarkTaskDiffResponse
from trajectory.types.benchmarks.benchmark_spec import BenchmarkSpec
from trajectory.types.benchmarks.benchmark_spec_params import BenchmarkSpecParams
from trajectory.types.benchmarks.benchmark_upload_file_param import BenchmarkUploadFileParam
from trajectory.types.benchmarks.tasks.tasks_append_params import TasksAppendParams
from trajectory.types.benchmarks.tasks.tasks_diff_params import TasksDiffParams
from trajectory.types.create_benchmark_task_append_response import CreateBenchmarkTaskAppendResponse
from trajectory.types.delete_benchmark_task_response import DeleteBenchmarkTaskResponse


class Tasks(APIResource):
  @cached_property
  def with_raw_response(self) -> TasksWithRawResponse:
    return TasksWithRawResponse(self)

  def count(
    self,
    bench_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkTaskCountResponse:
    """Benchmark Task Count

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
        "/api/v1/benchmarks/{bench_id}/task-count",
        bench_id=bench_id,
      ),
      cast_to=BenchmarkTaskCountResponse,
      options=make_request_options(
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
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
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
        "/api/v1/benchmarks/{bench_id}/tasks:diff",
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

  def append(
    self,
    bench_id: str,
    *,
    idempotency_key: str,
    files: Iterable[BenchmarkUploadFileParam],
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> CreateBenchmarkTaskAppendResponse:
    """Return signed artifact URLs for one append batch, staged under a prefix derived from the
    Idempotency-Key. Commit the returned batch_id to publish the batch's tasks.

    Args:
      files: Files to sign upload URLs for, one URL returned per declared path.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(bench_id, str) and not bench_id:
      raise ValueError(f"Expected a non-empty value for `bench_id` but received {bench_id!r}")
    return self._post(
      path_template(
        "/api/v1/benchmarks/{bench_id}/tasks:append",
        bench_id=bench_id,
      ),
      cast_to=CreateBenchmarkTaskAppendResponse,
      body=maybe_transform(
        {
          "files": files,
        },
        TasksAppendParams,
      ),
      options=make_request_options(
        headers={
          "Idempotency-Key": serialize_header(idempotency_key),
        },
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def commit(
    self,
    bench_id: str,
    batch_id: str,
    *,
    manifest: BenchmarkSpec,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkTaskAppendResult:
    """Persist and validate the request manifest, publish new tasks, and replace live tasks
    whose names are stored with different content in one transaction. Task names already
    stored with identical content are skipped, so committing the same batch twice is a
    no-op.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(bench_id, str) and not bench_id:
      raise ValueError(f"Expected a non-empty value for `bench_id` but received {bench_id!r}")
    if isinstance(batch_id, str) and not batch_id:
      raise ValueError(f"Expected a non-empty value for `batch_id` but received {batch_id!r}")
    return self._post(
      path_template(
        "/api/v1/benchmarks/{bench_id}/tasks:append/{batch_id}/commit",
        bench_id=bench_id,
        batch_id=batch_id,
      ),
      cast_to=BenchmarkTaskAppendResult,
      body=maybe_transform(manifest, BenchmarkSpecParams),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def delete(
    self,
    bench_id: str,
    task_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> DeleteBenchmarkTaskResponse:
    """Delete one benchmark task and its cascading task metadata. GCS artifacts are preserved
    because re-ingested benchmark snapshots may still reference them.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(bench_id, str) and not bench_id:
      raise ValueError(f"Expected a non-empty value for `bench_id` but received {bench_id!r}")
    if isinstance(task_id, str) and not task_id:
      raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
    return self._delete(
      path_template(
        "/api/v1/benchmarks/{bench_id}/tasks/{task_id}",
        bench_id=bench_id,
        task_id=task_id,
      ),
      cast_to=DeleteBenchmarkTaskResponse,
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
    self.count = to_raw_response_wrapper(resource.count)
    self.diff = to_raw_response_wrapper(resource.diff)
    self.append = to_raw_response_wrapper(resource.append)
    self.commit = to_raw_response_wrapper(resource.commit)
    self.delete = to_raw_response_wrapper(resource.delete)
