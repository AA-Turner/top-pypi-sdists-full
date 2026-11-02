"""
The shape of `seq policy doctor`'s report: the platform's walk of a deployment's request path, segment by segment.

In one sentence: the gateway runs the doctor server-side (GET /v1/deployments/{id}/diagnostics: initial-connect →
capacity → cold-start → worker-ping → act, without starting a worker) → seq/_observe_gateway.py reads its JSON into a
`DoctorReport` of `Segment`s → seq/observe.py prints it. The client-side chain that once ran here (connect → network →
cert-pin → auth-401 → worker-ping → act, and the mock backend that fed it) moved to the gateway on 2026-09-29; what
stays is the report's shape.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


OK = "ok"
FAIL = "fail"
WARMING = "warming"


@dataclass
class Segment:
    name: str
    status: str
    detail: Optional[str] = None
    extra: dict = field(default_factory=dict)


@dataclass
class DoctorReport:
    deployment: str
    segments: list[Segment]
    overall: str
    retry_after_s: Optional[float] = None
    eta_s: Optional[float] = None

    def segment(self, name: str) -> Optional[Segment]:
        return next((s for s in self.segments if s.name == name), None)
