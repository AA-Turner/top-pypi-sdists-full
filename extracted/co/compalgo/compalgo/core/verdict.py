from __future__ import annotations

import json
import hashlib
from datetime import datetime, timezone
from typing import List, Dict, Any

from pydantic import BaseModel, Field


SEVERITY_ORDER = ["info", "low", "medium", "high", "critical"]
SEVERITY_WEIGHT = {"critical": 20, "high": 10, "medium": 5, "low": 2, "info": 0}


class ComplianceVerdict(BaseModel):
    framework: str = Field(default="SOC2")
    control_id: str = Field(default="CC6.1")
    status: str  # "pass" | "fail"
    contract: str
    rules_triggered: List[str]
    severity: str  # highest severity across violations
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def canonical_json(self) -> str:
        # Deterministic JSON for hashing
        data = self.model_dump(exclude_none=True)
        return json.dumps(data, separators=(",", ":"), sort_keys=True)

    def hash_hex(self) -> str:
        return hashlib.sha256(self.canonical_json().encode()).hexdigest()


def _highest_severity(violations: List[Dict[str, Any]]) -> str:
    if not violations:
        return "info"
    max_idx = 0
    for v in violations:
        sev = (v.get("severity") or "info").lower()
        idx = SEVERITY_ORDER.index(sev) if sev in SEVERITY_ORDER else 0
        if idx > max_idx:
            max_idx = idx
    return SEVERITY_ORDER[max_idx]


def build_verdict(
    *,
    contract: str,
    violations: List[Dict[str, Any]],
    framework: str = "SOC2",
    control_id: str = "CC6.1",
    fail_on: str = "high",  # fail if any violation >= this
) -> ComplianceVerdict:
    highest = _highest_severity(violations)
    # Determine fail/pass based on threshold
    threshold_idx = SEVERITY_ORDER.index(fail_on)
    status = "pass"
    for v in violations:
        sev = (v.get("severity") or "info").lower()
        if sev in SEVERITY_ORDER and SEVERITY_ORDER.index(sev) >= threshold_idx:
            status = "fail"
            break
    rules = [v.get("rule_id") for v in violations if v.get("rule_id")]
    return ComplianceVerdict(
        framework=framework,
        control_id=control_id,
        status=status,
        contract=contract,
        rules_triggered=sorted(set(rules)),
        severity=highest,
    )


def verdict_hash(verdict: ComplianceVerdict) -> str:
    return verdict.hash_hex()
