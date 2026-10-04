# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Literal

import httpx

from trajectory._base_client import make_request_options, path_template
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.types.benchmark_diagnostic_status_response import BenchmarkDiagnosticStatusResponse
from trajectory.types.benchmark_diagnostics_response import BenchmarkDiagnosticsResponse
from trajectory.types.benchmark_images_response import BenchmarkImagesResponse
from trajectory.types.benchmarks.task_spec import TaskSpec
from trajectory.types.benchmarks.task_spec_param import TaskSpecParam
from trajectory.types.diagnostics.diagnostics_start_benchmark_params import (
  DiagnosticsStartBenchmarkParams,
)
from trajectory.types.start_benchmark_diagnostics_response import StartBenchmarkDiagnosticsResponse


class Diagnostics(APIResource):
  @cached_property
  def with_raw_response(self) -> DiagnosticsWithRawResponse:
    return DiagnosticsWithRawResponse(self)

  def ingest_task(
    self,
    *,
    agent_id: str,
    task: TaskSpec,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkImagesResponse:
    """Register one task as a private benchmark and submit its image build. Poll
    listBenchmarkImages until the image is ready, then call startBenchmarkDiagnostics with
    the returned bench_id.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/diagnostics/task",
      cast_to=BenchmarkImagesResponse,
      body=maybe_transform(task, TaskSpecParam),
      options=make_request_options(
        params=maybe_transform(
          {
            "agent_id": agent_id,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def start_benchmark(
    self,
    *,
    bench_id: str,
    base_model_slug: Literal[
      "thinkingmachines/Inkling-Small",
      "Qwen/Qwen3.5-4B",
      "Qwen/Qwen3.5-397B-A17B",
      "Qwen/Qwen3.6-27B",
      "Qwen/Qwen3.6-35B-A3B",
      "Qwen/Qwen3.8-27B",
      "qwen/qwen3-235b-a22b",
      "nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16",
      "nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16",
      "nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16",
      "nvidia/NVIDIA-Nemotron-3.5-Super-120B-A12B-BF16",
      "openai/gpt-5.6-sol",
      "openai/gpt-5.6-luna",
      "anthropic/claude-opus-5.5",
      "anthropic/claude-sonnet-5.5",
      "openai/gpt-5-mini",
      "openai/gpt-5.4-mini",
      "openai/gpt-5.5",
      "anthropic/claude-sonnet-4.6",
      "google/gemini-3.1-pro-preview",
      "z-ai/glm-5.3",
      "moonshotai/kimi-k3",
    ]
    | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> StartBenchmarkDiagnosticsResponse:
    """Start diagnostics for a benchmark, including one returned by ingestTaskForDiagnostics
    after its image is ready. Defaults to Nemotron 3.5 Lightning.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/diagnostics/benchmark",
      cast_to=StartBenchmarkDiagnosticsResponse,
      body=maybe_transform(
        {
          "bench_id": bench_id,
          "base_model_slug": base_model_slug,
        },
        DiagnosticsStartBenchmarkParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def get_status(
    self,
    benchmark_diagnostic_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkDiagnosticStatusResponse:
    """Poll the status of a benchmark diagnostic.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(benchmark_diagnostic_id, str) and not benchmark_diagnostic_id:
      raise ValueError(
        f"Expected a non-empty value for `benchmark_diagnostic_id` but received {benchmark_diagnostic_id!r}"
      )
    return self._get(
      path_template(
        "/api/v1/diagnostics/{benchmark_diagnostic_id}/status",
        benchmark_diagnostic_id=benchmark_diagnostic_id,
      ),
      cast_to=BenchmarkDiagnosticStatusResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def get_diagnostics(
    self,
    benchmark_diagnostic_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> BenchmarkDiagnosticsResponse:
    """Get task outcomes and failure reasons after a benchmark diagnostic finishes.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(benchmark_diagnostic_id, str) and not benchmark_diagnostic_id:
      raise ValueError(
        f"Expected a non-empty value for `benchmark_diagnostic_id` but received {benchmark_diagnostic_id!r}"
      )
    return self._get(
      path_template(
        "/api/v1/diagnostics/{benchmark_diagnostic_id}",
        benchmark_diagnostic_id=benchmark_diagnostic_id,
      ),
      cast_to=BenchmarkDiagnosticsResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class DiagnosticsWithRawResponse:
  def __init__(self, resource: Diagnostics) -> None:
    self._resource = resource
    self.ingest_task = to_raw_response_wrapper(resource.ingest_task)
    self.start_benchmark = to_raw_response_wrapper(resource.start_benchmark)
    self.get_status = to_raw_response_wrapper(resource.get_status)
    self.get_diagnostics = to_raw_response_wrapper(resource.get_diagnostics)
