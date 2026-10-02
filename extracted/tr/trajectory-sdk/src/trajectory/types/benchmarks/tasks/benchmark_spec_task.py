# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.benchmarks.secret_ref import SecretRef
from trajectory.types.task_split import TaskSplit


class BenchmarkTaskCategory(BaseModel):
  task_category_id: str

  label: str


class BenchmarkSpecTask(BaseModel):
  task_id: str

  label: str | None = None

  split: TaskSplit | None = None

  input_message: str | None = None

  task_categories: list[BenchmarkTaskCategory] | None = None

  runtime_id: str | None = None

  run_command: str | None = None
  """
    For SDK evaluation and training, the command to run your agent in the sandbox, e.g.
    `python /app/agent.py`. Your script must call the model, run any tools, log a reward,
    and finalize the trajectory before exiting.
    """

  build_status: str | None = None

  env_vars: dict[str, str | SecretRef] | None = None
