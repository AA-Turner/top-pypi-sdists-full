# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any

import httpx

from trajectory._base_client import make_request_options, path_template
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, not_given
from trajectory.types.benchmark_images_response import BenchmarkImagesResponse


class Images(APIResource):
  @cached_property
  def with_raw_response(self) -> ImagesWithRawResponse:
    return ImagesWithRawResponse(self)

  def list(
    self,
    bench_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkImagesResponse:
    """List the bench's task images with build status, refreshing in-flight provider builds
    (building -> ready/failed) as a side effect.

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
        "/api/v1/benchmarks/{bench_id}/images",
        bench_id=bench_id,
      ),
      cast_to=BenchmarkImagesResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def build(
    self,
    bench_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkImagesResponse:
    """Trigger provider image builds for every unbuilt task image of the bench. Build
    completion is asynchronous; poll listBenchmarkImages until every row reports
    build_status=ready.

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
        "/api/v1/benchmarks/{bench_id}/images/build",
        bench_id=bench_id,
      ),
      cast_to=BenchmarkImagesResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class ImagesWithRawResponse:
  def __init__(self, resource: Images) -> None:
    self._resource = resource
    self.list = to_raw_response_wrapper(resource.list)
    self.build = to_raw_response_wrapper(resource.build)
