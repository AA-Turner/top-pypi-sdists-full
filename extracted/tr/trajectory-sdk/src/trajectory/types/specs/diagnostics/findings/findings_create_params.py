# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Iterable
from typing import Literal, Required, TypedDict

from trajectory._types import SequenceNotStr


class SpecEvidenceParam(TypedDict, total=False):
  kind: Required[Literal["spec"]]
  bench_id: Required[str]
  explanation: Required[str]


class TaskEvidenceParam(TypedDict, total=False):
  kind: Required[Literal["task"]]
  bench_id: Required[str]
  task_id: Required[str]
  explanation: Required[str]


class TrajectoryEvidenceParam(TypedDict, total=False):
  kind: Required[Literal["trajectory"]]
  trajectory_id: Required[str]
  step_indices: Iterable[int]
  """
  Zero-based recorded step indices.
  """
  tool_call_ids: SequenceNotStr[str]
  """
  Tool calls visible in the referenced steps. Requires step_indices.
  """
  explanation: Required[str]


class FindingsCreateParams(TypedDict, total=False):
  bench_id: Required[str]
  task_id: str | None
  trajectory_id: str | None
  title: Required[str]
  explanation: Required[str]
  suggested_fix: str | None
  detector_name: Required[str]
  evidence: Iterable[SpecEvidenceParam | TaskEvidenceParam | TrajectoryEvidenceParam]
