# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, TypeAlias

from trajectory._models import BaseModel

EvalTaskSplit: TypeAlias = Literal["test", "train", "all"]


class EvalTaskSelection(BaseModel):
  split: EvalTaskSplit

  available_task_count: int
  """Tasks in the selected scope at launch."""

  selected_task_count: int
  """Distinct tasks selected for execution."""

  max_samples: int | None = None
  """Explicit options.val_num_tasks, or null to run every task in the selected scope."""
