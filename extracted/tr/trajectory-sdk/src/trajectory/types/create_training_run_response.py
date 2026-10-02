# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class ResolvedTrajectoryTrainingOptions(BaseModel):
  max_output_tokens_per_step: int

  max_total_tokens_per_trajectory: int

  max_turns_per_trajectory: int

  max_tool_calls_per_step: int

  max_response_chars_per_tool_call: int

  timeout_seconds: int


class CreateTrainingRunResponse(BaseModel):
  bench_id: str

  training_run_id: str

  display_name: str
  """User-facing name for the training run."""

  resolved_trajectory_options: ResolvedTrajectoryTrainingOptions | None
