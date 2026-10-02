# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Iterable, Literal

import httpx

from trajectory._base_client import SyncPage, make_request_options, path_template
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.resources.benchmarks.images import Images, ImagesWithRawResponse
from trajectory.resources.benchmarks.ingestion import Ingestion, IngestionWithRawResponse
from trajectory.resources.benchmarks.specs import Specs, SpecsWithRawResponse
from trajectory.resources.benchmarks.tasks import Tasks, TasksWithRawResponse
from trajectory.types.benchmark_runtime import BenchmarkRuntime
from trajectory.types.benchmarks.benchmark_list_item import BenchmarkListItem
from trajectory.types.benchmarks.benchmark_readiness import BenchmarkReadiness
from trajectory.types.benchmarks.benchmark_spec import BenchmarkSpec
from trajectory.types.benchmarks.benchmark_spec_params import BenchmarkSpecParams
from trajectory.types.benchmarks.benchmark_upload_file_param import BenchmarkUploadFileParam
from trajectory.types.benchmarks.benchmarks_create_upload_params import BenchmarksCreateUploadParams
from trajectory.types.benchmarks.benchmarks_update_params import BenchmarksUpdateParams
from trajectory.types.create_benchmark_upload_response import CreateBenchmarkUploadResponse
from trajectory.types.delete_benchmark_response import DeleteBenchmarkResponse
from trajectory.types.ingest_benchmark_response import IngestBenchmarkResponse


class Benchmarks(APIResource):
  @cached_property
  def with_raw_response(self) -> BenchmarksWithRawResponse:
    return BenchmarksWithRawResponse(self)

  @cached_property
  def ingestion(self) -> Ingestion:
    return Ingestion(self._client)

  @cached_property
  def specs(self) -> Specs:
    return Specs(self._client)

  @cached_property
  def tasks(self) -> Tasks:
    return Tasks(self._client)

  @cached_property
  def images(self) -> Images:
    return Images(self._client)

  def list(
    self,
    *,
    include_holodeck: bool | Omit = omit,
    cursor: str | None | Omit = omit,
    limit: int | Omit = omit,
    sort: str | None | Omit = omit,
    order: Literal["asc", "desc"] | Omit = omit,
    search: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> SyncPage[BenchmarkListItem]:
    """List Benchmarks

    Args:
      include_holodeck: Include Holodeck benchmarks in the library.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/benchmarks",
      cast_to=SyncPage[BenchmarkListItem],
      options=make_request_options(
        params=maybe_transform(
          {
            "include_holodeck": include_holodeck,
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

  def retrieve(
    self,
    bench_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkListItem:
    """Get Benchmark

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
        "/api/v1/benchmarks/{bench_id}",
        bench_id=bench_id,
      ),
      cast_to=BenchmarkListItem,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def update(
    self,
    bench_id: str,
    *,
    name: str | None | Omit = omit,
    description: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> dict[str, str]:
    """Update Benchmark

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(bench_id, str) and not bench_id:
      raise ValueError(f"Expected a non-empty value for `bench_id` but received {bench_id!r}")
    return self._patch(
      path_template(
        "/api/v1/benchmarks/{bench_id}",
        bench_id=bench_id,
      ),
      cast_to=dict[str, str],
      body=maybe_transform(
        {
          "name": name,
          "description": description,
        },
        BenchmarksUpdateParams,
      ),
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
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> DeleteBenchmarkResponse:
    """Delete a benchmark, all of its tasks and cascading task metadata, its benchmark and
    env-eval result rows, and runtimes not referenced by another benchmark's tasks. Shared
    runtimes, other registry metadata, pipeline execution metadata, and GCS artifacts are
    preserved.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(bench_id, str) and not bench_id:
      raise ValueError(f"Expected a non-empty value for `bench_id` but received {bench_id!r}")
    return self._delete(
      path_template(
        "/api/v1/benchmarks/{bench_id}",
        bench_id=bench_id,
      ),
      cast_to=DeleteBenchmarkResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def create_upload(
    self,
    *,
    files: Iterable[BenchmarkUploadFileParam],
    bench_id: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> CreateBenchmarkUploadResponse:
    """Allocate signed GCS PUT URLs for one batch of benchmark artifacts. Omit bench_id to mint
    a new benchmark; pass the returned bench_id on later calls to add more files to the same
    benchmark, which is how a file set over the per-request limit is uploaded. No rows are
    written until the ingest call.

    Args:
      files: Files to sign upload URLs for, one URL returned per declared path.

      bench_id: Omit to mint a new benchmark. Pass a bench_id returned by an earlier batch to add
        these files to that benchmark's upload prefix, which is how a file set larger than
        the per-request limit is uploaded. An already-ingested bench_id is rejected.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/benchmarks/uploads",
      cast_to=CreateBenchmarkUploadResponse,
      body=maybe_transform(
        {
          "files": files,
          "bench_id": bench_id,
        },
        BenchmarksCreateUploadParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def register(
    self,
    bench_id: str,
    *,
    manifest: BenchmarkSpec,
    agent_id: str | None | Omit = omit,
    agent_name: str | None | Omit = omit,
    bench_type: Literal["benchmark", "holodeck_benchmark"] | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> IngestBenchmarkResponse:
    """Validate a benchmark manifest for a bench_id allocated by createBenchmarkUpload, persist
    it canonically, and write the bench, task, and runtime rows.

    Args:
      agent_id: The benchmark's agent ID. Provide agent_id or agent_name for both new benchmarks
        and appends.

      agent_name: The benchmark's agent name. Provide agent_id or agent_name for both new benchmarks
        and appends.

      bench_type: The kind of benchmark push: a real benchmark or a holodeck draft.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(bench_id, str) and not bench_id:
      raise ValueError(f"Expected a non-empty value for `bench_id` but received {bench_id!r}")
    return self._post(
      path_template(
        "/api/v1/benchmarks/{bench_id}/ingest",
        bench_id=bench_id,
      ),
      cast_to=IngestBenchmarkResponse,
      body=maybe_transform(manifest, BenchmarkSpecParams),
      options=make_request_options(
        params=maybe_transform(
          {
            "agent_id": agent_id,
            "agent_name": agent_name,
            "bench_type": bench_type,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def list_runtimes(
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
  ) -> SyncPage[BenchmarkRuntime]:
    """List the caller's organization-scoped benchmark runtimes.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/benchmarks/runtimes",
      cast_to=SyncPage[BenchmarkRuntime],
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

  def retrieve_readiness(
    self,
    bench_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkReadiness:
    """Return whether a benchmark is ready to launch. A benchmark is ready when it is fully
    ingested, all required organization secrets are available, and all task environments are
    built. When it is not ready, the response identifies the remaining blockers.

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
        "/api/v1/benchmarks/{bench_id}/readiness",
        bench_id=bench_id,
      ),
      cast_to=BenchmarkReadiness,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class BenchmarksWithRawResponse:
  def __init__(self, resource: Benchmarks) -> None:
    self._resource = resource
    self.list = to_raw_response_wrapper(resource.list)
    self.retrieve = to_raw_response_wrapper(resource.retrieve)
    self.update = to_raw_response_wrapper(resource.update)
    self.delete = to_raw_response_wrapper(resource.delete)
    self.create_upload = to_raw_response_wrapper(resource.create_upload)
    self.register = to_raw_response_wrapper(resource.register)
    self.list_runtimes = to_raw_response_wrapper(resource.list_runtimes)
    self.retrieve_readiness = to_raw_response_wrapper(resource.retrieve_readiness)

  @cached_property
  def ingestion(self) -> IngestionWithRawResponse:
    return IngestionWithRawResponse(self._resource.ingestion)

  @cached_property
  def specs(self) -> SpecsWithRawResponse:
    return SpecsWithRawResponse(self._resource.specs)

  @cached_property
  def tasks(self) -> TasksWithRawResponse:
    return TasksWithRawResponse(self._resource.tasks)

  @cached_property
  def images(self) -> ImagesWithRawResponse:
    return ImagesWithRawResponse(self._resource.images)
