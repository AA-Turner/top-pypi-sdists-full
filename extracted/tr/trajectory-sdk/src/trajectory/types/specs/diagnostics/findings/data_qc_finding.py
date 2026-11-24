# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime
from typing import Literal

from trajectory._models import BaseModel


class SpecEvidence(BaseModel):
  kind: Literal["spec"]

  bench_id: str

  explanation: str


class TaskEvidence(BaseModel):
  kind: Literal["task"]

  bench_id: str

  task_id: str

  explanation: str


class TrajectoryEvidence(BaseModel):
  kind: Literal["trajectory"]

  trajectory_id: str

  step_indices: list[int] | None = None
  """Zero-based recorded step indices."""

  tool_call_ids: list[str] | None = None
  """Tool calls visible in the referenced steps. Requires step_indices."""

  explanation: str


class DataQcFinding(BaseModel):
  bench_id: str

  task_id: str | None = None

  trajectory_id: str | None = None

  title: str

  explanation: str

  suggested_fix: str | None = None

  detector_name: str

  evidence: list[SpecEvidence | TaskEvidence | TrajectoryEvidence] | None = None

  finding_id: str

  state: Literal["open", "resolved"]

  created_by: str

  created_at: datetime

  resolved_by: str | None = None

  resolved_at: datetime | None = None

  resolution_note: str | None = None
