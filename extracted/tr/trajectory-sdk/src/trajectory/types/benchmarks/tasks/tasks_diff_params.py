# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Mapping
from typing import Required, TypedDict

from trajectory.types.benchmarks.benchmark_spec_params import BenchmarkSpecParams


class TasksDiffParams(TypedDict, total=False):
  manifest: Required[BenchmarkSpecParams]
  artifacts: Mapping[str, str]
