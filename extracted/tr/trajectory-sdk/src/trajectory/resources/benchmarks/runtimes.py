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
from trajectory.types.benchmark_runtimes_page import BenchmarkRuntimesPage


class Runtimes(APIResource):
  @cached_property
  def with_raw_response(self) -> RuntimesWithRawResponse:
    return RuntimesWithRawResponse(self)

  def list(
    self,
    bench_id: str,
    *,
    cursor: str | None | Omit = omit,
    limit: int | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkRuntimesPage:
    """Runtimes used by the benchmark's tasks, in ascending runtime-ID order. Build status is
    the stored value; listBenchmarkImages refreshes in-flight provider builds.

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
        "/api/v1/benchmarks/{bench_id}/runtimes",
        bench_id=bench_id,
      ),
      cast_to=BenchmarkRuntimesPage,
      options=make_request_options(
        params=maybe_transform(
          {
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


class RuntimesWithRawResponse:
  def __init__(self, resource: Runtimes) -> None:
    self._resource = resource
    self.list = to_raw_response_wrapper(resource.list)
