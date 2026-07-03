"""Typed view of ``kytte.decision.v1.EvaluateSpanResponse``."""

from dataclasses import dataclass
from typing import Any  # noqa: TID251 — generated proto types are dynamically typed.


@dataclass(frozen=True)
class RemediationDecision:
    verdict: int  # kytte.decision.v1.Verdict enum value
    problem_type: str
    steps: tuple[Any, ...]  # RemediationStep protos — opaque in read-only
    apply: bool
    execution_id: str | None  # None ⇒ no autonomous action selected
    request_full_context: bool

    @property
    def action_selected(self) -> bool:
        return self.execution_id is not None

    @classmethod
    def from_response(cls, resp: Any) -> "RemediationDecision":
        return cls(
            verdict=resp.verdict,
            problem_type=resp.problem_type,
            steps=tuple(resp.steps),
            apply=resp.apply,
            execution_id=resp.execution_id if resp.HasField("execution_id") else None,
            request_full_context=resp.request_full_context,
        )
