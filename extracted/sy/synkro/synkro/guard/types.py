"""Unified result types for PolicyGuard."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from synkro.remediation.types import Violation
    from synkro.verify.types import Report, Result, Verdict


@dataclass
class GuardResult:
    """Unified result from PolicyGuard.check().

    Combines Logic Map policy detection with SQL ground-truth verification
    into a single gateway-friendly response.

    Examples:
        >>> result = await guard.check_async(messages)
        >>> if not result.passed:
        ...     print(result.issues)
        ...     log_to_db(result.to_dict())
    """

    # Overall verdict
    passed: bool
    trace_id: str = ""

    # Policy detection results (Logic Map)
    violation: Violation | None = None

    # SQL verification results (ground truth)
    sql_report: Report | None = None

    # Unified issues list (merged from both sources)
    issues: list[str] = field(default_factory=list)

    # Severity (worst-case from both checks)
    severity: str = "none"

    # Rules violated (from policy detection)
    rules_violated: list[str] = field(default_factory=list)

    # Timing and cost
    latency_ms: float = 0.0
    cost: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def has_policy_violation(self) -> bool:
        """True if LogicMap policy check found a violation."""
        return self.violation is not None

    @property
    def has_sql_violation(self) -> bool:
        """True if SQL verification found a violation."""
        return self.sql_report is not None and not self.sql_report.passed

    @property
    def sql_results(self) -> list[Result]:
        """SQL verification results (empty if SQL not configured)."""
        return self.sql_report.results if self.sql_report else []

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return {
            "passed": self.passed,
            "trace_id": self.trace_id,
            "severity": self.severity,
            "issues": self.issues,
            "rules_violated": self.rules_violated,
            "violation": self.violation.to_dict() if self.violation else None,
            "sql_report": {
                "trace_id": self.sql_report.trace_id,
                "passed": self.sql_report.passed,
                "results": [
                    {
                        "name": r.name,
                        "score": r.score,
                        "value": r.value.value,
                        "comment": r.comment,
                        "metadata": r.metadata,
                    }
                    for r in self.sql_report.results
                ],
            }
            if self.sql_report
            else None,
            "latency_ms": self.latency_ms,
            "cost": self.cost,
            "timestamp": self.timestamp.isoformat(),
        }

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), default=str)

    def to_langsmith(self) -> dict[str, Any]:
        """Convert to LangSmith feedback format."""
        if self.violation:
            return self.violation.to_langsmith()
        return {
            "run_id": self.trace_id,
            "key": "policy_compliance",
            "score": 1.0 if self.passed else 0.0,
            "comment": "; ".join(self.issues) if self.issues else "Passed all checks",
        }

    def to_langfuse(self) -> dict[str, Any]:
        """Convert to Langfuse score format."""
        if self.violation:
            return self.violation.to_langfuse()
        return {
            "traceId": self.trace_id,
            "name": "policy_compliance",
            "value": "pass" if self.passed else "violation",
            "dataType": "CATEGORICAL",
            "comment": "; ".join(self.issues) if self.issues else "Passed all checks",
        }

    def to_datadog(self) -> dict[str, Any]:
        """Convert to Datadog evaluation format."""
        if self.violation:
            return self.violation.to_datadog()
        return {
            "span_context": self.trace_id,
            "label": "policy_compliance",
            "metric_type": "categorical",
            "value": "pass" if self.passed else "violation",
            "reasoning": "; ".join(self.issues) if self.issues else "Passed all checks",
        }
