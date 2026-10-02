# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Iterable
from typing import Literal, Required, TypedDict

from trajectory.types.benchmarks.runtime_spec_param import RuntimeSpecParam
from trajectory.types.benchmarks.task_spec_param import TaskSpecParam


class BenchmarkSpecParams(TypedDict, total=False):
  name: Required[str]
  description: str
  visibility: Literal["public", "private"]
  family: str | None
  runtime: RuntimeSpecParam | None
  tasks: Required[Iterable[TaskSpecParam]]
