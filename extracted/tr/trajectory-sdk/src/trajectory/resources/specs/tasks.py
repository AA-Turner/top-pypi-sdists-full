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
from trajectory.types.benchmark_task_env_resources import BenchmarkTaskEnvResources
from trajectory.types.specs.benchmark_spec_params import BenchmarkSpecParams
from trajectory.types.specs.tasks.benchmark_spec_task import BenchmarkSpecTask
from trajectory.types.specs.tasks.tasks_diff_params import TasksDiffParams
from trajectory.types.specs.tasks.tasks_update_env_resources_params import (
  TasksUpdateEnvResourcesParams,
)


class Tasks(APIResource):
  @cached_property
  def with_raw_response(self) -> TasksWithRawResponse:
    return TasksWithRawResponse(self)

  def list(
    self,
    spec_id: str,
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
    """Lists the spec's tasks in upload order, with appended tasks after earlier ones. Tasks
    uploaded before upload order was recorded come first, in creation order. `order=desc`
    reverses the list.

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
    if isinstance(spec_id, str) and not spec_id:
      raise ValueError(f"Expected a non-empty value for `spec_id` but received {spec_id!r}")
    return self._get(
      path_template(
        "/api/v1/specs/{spec_id}/tasks",
        spec_id=spec_id,
      ),
      cast_to=SyncPage[BenchmarkSpecTask],
      options=make_request_options(
        params=maybe_transform(
          {
            "task_id": task_id,
            "split": split,
            "environment": environment,
            "run_id": run_id,
            "cursor": omit if cursor is None else cursor,
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
    spec_id: str,
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
    """Get Spec Task Count

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
    if isinstance(spec_id, str) and not spec_id:
      raise ValueError(f"Expected a non-empty value for `spec_id` but received {spec_id!r}")
    return self._get(
      path_template(
        "/api/v1/specs/{spec_id}/task-count",
        spec_id=spec_id,
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
    spec_id: str,
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
    if isinstance(spec_id, str) and not spec_id:
      raise ValueError(f"Expected a non-empty value for `spec_id` but received {spec_id!r}")
    return self._post(
      path_template(
        "/api/v1/specs/{spec_id}/tasks/diff",
        spec_id=spec_id,
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

  def get_env_resources(
    self,
    spec_id: str,
    task_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkTaskEnvResources:
    """Return the CPU, memory, GPU and network settings of one spec task's sandbox.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(spec_id, str) and not spec_id:
      raise ValueError(f"Expected a non-empty value for `spec_id` but received {spec_id!r}")
    if isinstance(task_id, str) and not task_id:
      raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
    return self._get(
      path_template(
        "/api/v1/specs/{spec_id}/tasks/{task_id}/env_resources",
        spec_id=spec_id,
        task_id=task_id,
      ),
      cast_to=BenchmarkTaskEnvResources,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def update_env_resources(
    self,
    spec_id: str,
    task_id: str,
    *,
    cpus: float | None | Omit = omit,
    memory_mb: int | None | Omit = omit,
    gpus: int | Omit = omit,
    network_mode: Literal["no-network", "public", "allowlist"] | Omit = omit,
    allowed_hosts: SequenceNotStr[str] | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkTaskEnvResources:
    """Change the CPU, memory, GPU or network settings of one spec task's sandbox without
    uploading the task again. Only the fields in the request change. Rollouts that start
    after the change use it; sandboxes already running keep the settings they started with.

    Args:
      cpus: CPU cores to request. Set `cpus` and `memory_mb` both to null for the default.

      memory_mb: Memory to request in MiB.

      gpus: GPUs to request.

      network_mode: `public`, `allowlist` or `no-network`. Leaving `allowlist` clears `allowed_hosts`
        unless the request also sets it.

      allowed_hosts: Domain names the sandbox may reach, such as `pypi.org` or `*.example.com` for
        every subdomain; no scheme, port, path or IP address. Only valid with `allowlist`.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(spec_id, str) and not spec_id:
      raise ValueError(f"Expected a non-empty value for `spec_id` but received {spec_id!r}")
    if isinstance(task_id, str) and not task_id:
      raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
    return self._patch(
      path_template(
        "/api/v1/specs/{spec_id}/tasks/{task_id}/env_resources",
        spec_id=spec_id,
        task_id=task_id,
      ),
      cast_to=BenchmarkTaskEnvResources,
      body=maybe_transform(
        {
          "cpus": cpus,
          "memory_mb": memory_mb,
          "gpus": gpus,
          "network_mode": network_mode,
          "allowed_hosts": allowed_hosts,
        },
        TasksUpdateEnvResourcesParams,
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
    self.get_env_resources = to_raw_response_wrapper(resource.get_env_resources)
    self.update_env_resources = to_raw_response_wrapper(resource.update_env_resources)
