# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel


class TracebackDiagnostic(BaseModel):
  exception_chain: list[str] = []

  locations: list[str] = []


class HarnessDiagnostic(BaseModel):
  exception_chain: list[str] = []

  locations: list[str] = []

  category: Literal["timeout", "connection", "rate_limit", "authentication", "server", "other"]

  preceding_tracebacks: list[TracebackDiagnostic] = []

  exit_code: int | None = None

  exception_messages: list[str] = []


class TrajectoryRolloutStatus(BaseModel):
  rollout_id: str

  status: str
  """Recorded Rollout Service state, such as IN_PROGRESS or FAILED."""

  termination_reason: str | None = None
  """Recorded rollout termination enum."""

  harness_diagnostic: HarnessDiagnostic | None = None
