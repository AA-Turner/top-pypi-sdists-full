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
from trajectory.types.benchmarks.specs.benchmark_details import BenchmarkDetails


class Specs(APIResource):
  @cached_property
  def with_raw_response(self) -> SpecsWithRawResponse:
    return SpecsWithRawResponse(self)

  def retrieve(
    self,
    bench_id: str,
    *,
    include_tasks: bool | None | Omit = omit,
    include_tools: bool | None | Omit = omit,
    include_runtimes: bool | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkDetails:
    """Benchmark Spec

    Args:
      include_tasks: Include every task; listBenchmarkSpecTasks pages them. Defaults to false with
        Trajectory-API-Version: tmp-contract and to true otherwise.

      include_tools: Include every bound tool; listBenchmarkSpecTools pages them. Defaults to false
        with Trajectory-API-Version: tmp-contract and to true otherwise.

      include_runtimes: Include every task runtime; listBenchmarkSpecRuntimes pages them. Defaults to
        false with Trajectory-API-Version: tmp-contract and to true otherwise.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(bench_id, str) and not bench_id:
      raise ValueError(f"Expected a non-empty value for `bench_id` but received {bench_id!r}")
    return self._get(
      path_template(
        "/api/v1/benchmarks/{bench_id}/spec",
        bench_id=bench_id,
      ),
      cast_to=BenchmarkDetails,
      options=make_request_options(
        params=maybe_transform(
          {
            "include_tasks": include_tasks,
            "include_tools": include_tools,
            "include_runtimes": include_runtimes,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class SpecsWithRawResponse:
  def __init__(self, resource: Specs) -> None:
    self._resource = resource
    self.retrieve = to_raw_response_wrapper(resource.retrieve)
