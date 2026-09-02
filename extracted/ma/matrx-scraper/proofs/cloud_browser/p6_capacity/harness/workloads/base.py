"""Workload contract. Phase-0 proof harness (NOT shipped code).

A workload is one row of PLAN.md's six-workload list. It must be able to say, BEFORE the
ramp starts, whether it can run here -- and if it cannot, say so in one sentence an
operator can act on. A workload that quietly measures less than it claims is the single
failure mode this harness exists to prevent, so `Preflight.status` is carried all the way
into the summary and a run is "complete" only when every workload reports "ok".
"""

from __future__ import annotations

import dataclasses
from typing import Protocol

STATUS_OK = "ok"  # every metric this workload owns can be measured here
STATUS_PARTIAL = "partial"  # it runs, but at least one required metric cannot be taken
STATUS_SKIP = "skip"  # it cannot run at all here


@dataclasses.dataclass
class Preflight:
    status: str
    reasons: list[str] = dataclasses.field(default_factory=list)
    unmeasurable: list[str] = dataclasses.field(default_factory=list)

    @property
    def runnable(self) -> bool:
        return self.status in (STATUS_OK, STATUS_PARTIAL)

    def to_json(self) -> dict:
        return {
            "status": self.status,
            "reasons": self.reasons,
            "unmeasurable_metrics": self.unmeasurable,
        }


@dataclasses.dataclass
class UnitSpec:
    """How to launch one unit of this workload."""

    argv: list[str]
    env: dict[str, str] = dataclasses.field(default_factory=dict)
    cwd: str | None = None


class Workload(Protocol):
    id: str
    plan_workload: int  # 1..6, PLAN.md's own numbering
    title: str
    capacity_class: str
    steady_state: bool  # False = a burst/rate workload (storms)

    def preflight(self, ctx) -> Preflight: ...

    def unit_spec(self, ctx, unit_id: str, level: int) -> UnitSpec: ...
