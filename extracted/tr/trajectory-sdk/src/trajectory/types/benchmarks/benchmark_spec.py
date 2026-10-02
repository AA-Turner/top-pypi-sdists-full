# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel
from trajectory.types.benchmarks.runtime_spec import RuntimeSpec
from trajectory.types.benchmarks.task_spec import TaskSpec


class BenchmarkSpec(BaseModel):
  name: str

  description: str = ""

  visibility: Literal["public", "private"] = "private"

  family: str | None = None

  runtime: RuntimeSpec | None = None

  tasks: list[TaskSpec]
