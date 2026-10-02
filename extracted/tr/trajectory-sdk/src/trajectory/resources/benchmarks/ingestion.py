# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Iterable, Literal, Mapping

import httpx

from trajectory._base_client import make_request_options, path_template, serialize_header
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.types.benchmark_ingestion_operation_page import BenchmarkIngestionOperationPage
from trajectory.types.benchmark_ingestion_session import BenchmarkIngestionSession
from trajectory.types.benchmark_ingestion_upload_urls import BenchmarkIngestionUploadUrls
from trajectory.types.benchmarks.ingestion.benchmark_ingestion_operation_status import (
  BenchmarkIngestionOperationStatus,
)
from trajectory.types.benchmarks.ingestion.ingestion_allocate_uploads_params import (
  BenchmarkIngestionUploadObjectParam,
  IngestionAllocateUploadsParams,
)
from trajectory.types.benchmarks.ingestion.ingestion_create_session_params import (
  IngestionCreateSessionParams,
)
from trajectory.types.benchmarks.ingestion.ingestion_finalize_params import IngestionFinalizeParams


class Ingestion(APIResource):
  @cached_property
  def with_raw_response(self) -> IngestionWithRawResponse:
    return IngestionWithRawResponse(self)

  def create_session(
    self,
    *,
    idempotency_key: str,
    bench_name: str,
    metadata: Mapping[str, Any],
    upload_digest: str,
    agent_id: str | None | Omit = omit,
    agent_name: str | None | Omit = omit,
    build_images: bool | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkIngestionSession:
    """Create Session

    Args:
      bench_name: Reusing a benchmark name pushes a new version of that benchmark.

      agent_id: The benchmark's agent ID. Provide agent_id or agent_name for every ingestion.

      agent_name: The benchmark's agent name. Provide agent_id or agent_name for every ingestion.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/benchmark-ingestion/sessions",
      cast_to=BenchmarkIngestionSession,
      body=maybe_transform(
        {
          "bench_name": bench_name,
          "metadata": metadata,
          "upload_digest": upload_digest,
          "agent_id": agent_id,
          "agent_name": agent_name,
          "build_images": build_images,
        },
        IngestionCreateSessionParams,
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

  def allocate_uploads(
    self,
    operation_id: str,
    *,
    files: Iterable[BenchmarkIngestionUploadObjectParam],
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkIngestionUploadUrls:
    """Allocate

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
    return self._post(
      path_template(
        "/api/v1/benchmark-ingestion/sessions/{operation_id}/uploads",
        operation_id=operation_id,
      ),
      cast_to=BenchmarkIngestionUploadUrls,
      body=maybe_transform(
        {
          "files": files,
        },
        IngestionAllocateUploadsParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def cancel(
    self,
    operation_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkIngestionOperationStatus:
    """Cancel an uploading, queued, or running submission; finished submissions return 409.

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
    return self._post(
      path_template(
        "/api/v1/benchmark-ingestion/sessions/{operation_id}/cancel",
        operation_id=operation_id,
      ),
      cast_to=BenchmarkIngestionOperationStatus,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def finalize(
    self,
    operation_id: str,
    *,
    object_count: int,
    part_count: int,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkIngestionOperationStatus:
    """Finalize

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
    return self._post(
      path_template(
        "/api/v1/benchmark-ingestion/sessions/{operation_id}/finalize",
        operation_id=operation_id,
      ),
      cast_to=BenchmarkIngestionOperationStatus,
      body=maybe_transform(
        {
          "object_count": object_count,
          "part_count": part_count,
        },
        IngestionFinalizeParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def retrieve(
    self,
    operation_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkIngestionOperationStatus:
    """Status

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
        "/api/v1/benchmark-ingestion/operations/{operation_id}",
        operation_id=operation_id,
      ),
      cast_to=BenchmarkIngestionOperationStatus,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def list_items(
    self,
    operation_id: str,
    kind: Literal["result", "failure", "runtime", "runtime_task"],
    *,
    after: str | Omit = omit,
    limit: int | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkIngestionOperationPage:
    """Items

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
    if isinstance(kind, str) and not kind:
      raise ValueError(f"Expected a non-empty value for `kind` but received {kind!r}")
    return self._get(
      path_template(
        "/api/v1/benchmark-ingestion/operations/{operation_id}/{kind}",
        operation_id=operation_id,
        kind=kind,
      ),
      cast_to=BenchmarkIngestionOperationPage,
      options=make_request_options(
        params=maybe_transform(
          {
            "after": after,
            "limit": limit,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class IngestionWithRawResponse:
  def __init__(self, resource: Ingestion) -> None:
    self._resource = resource
    self.create_session = to_raw_response_wrapper(resource.create_session)
    self.allocate_uploads = to_raw_response_wrapper(resource.allocate_uploads)
    self.cancel = to_raw_response_wrapper(resource.cancel)
    self.finalize = to_raw_response_wrapper(resource.finalize)
    self.retrieve = to_raw_response_wrapper(resource.retrieve)
    self.list_items = to_raw_response_wrapper(resource.list_items)
