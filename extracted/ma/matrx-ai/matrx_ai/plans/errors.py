"""The agent-plan validation gate.

An invalid plan must fail BEFORE any money is spent or any row is created,
with every problem reported at once (not fail-first) so the planning agent
can self-correct in one round trip. Follows the internal-validation-gate
contract (see TOOL_OUTPUT_VALIDATION_GATE.md): loud self-identifying
banner, short clean exception, dedicated error_type for one-grep
separation from real failures.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

AGENT_PLAN_GATE_ERROR_TYPE = "agent_plan_validation_gate"


class PlanIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str
    message: str
    step: int | None = None


class AgentPlanValidationError(Exception):
    """Raised when a plan fails the validation gate. Carries ALL issues."""

    error_type = AGENT_PLAN_GATE_ERROR_TYPE

    def __init__(self, issues: list[PlanIssue]) -> None:
        self.issues = issues
        super().__init__(self.render())

    def render(self) -> str:
        lines = [
            f"AgentPlan rejected by the validation gate — "
            f"{len(self.issues)} issue(s). Fix ALL of them and resubmit:"
        ]
        for i, issue in enumerate(self.issues, 1):
            step = f" (step {issue.step})" if issue.step is not None else ""
            lines.append(f"  {i}. [{issue.path}]{step} {issue.message}")
        return "\n".join(lines)


def issues_from_validation_error(exc: Exception) -> list[PlanIssue]:
    """Convert a pydantic ValidationError on AgentPlan into gate-style
    issues — one clean line per problem, no pydantic.dev URLs, no
    union-branch noise (a bad value in a union otherwise reports once per
    branch, which buried the real problems in the 2026-07-07 test)."""
    raw = getattr(exc, "errors", None)
    if not callable(raw):
        return [PlanIssue(path="plan", message=str(exc))]
    seen: set[tuple[str, str]] = set()
    issues: list[PlanIssue] = []
    for err in raw(include_url=False):
        loc = [str(part) for part in err.get("loc", ())]
        # Collapse union-branch suffixes ("...kinds.str", "...kinds.int")
        # onto the field itself.
        while loc and loc[-1] in ("str", "int", "float", "bool", "none", "list", "dict"):
            loc.pop()
        path = ".".join(loc) or "plan"
        message = str(err.get("msg", "invalid value"))
        step: int | None = None
        if len(loc) >= 2 and loc[0] == "steps" and loc[1].isdigit():
            step = int(loc[1]) + 1  # positional index → 1-based only as a hint
            path = "steps[?]." + ".".join(loc[2:]) if len(loc) > 2 else "steps[?]"
            message += f" (step at position {step} in your list)"
        key = (path, message)
        if key in seen:
            continue
        seen.add(key)
        issues.append(PlanIssue(path=path, message=message))
    return issues or [PlanIssue(path="plan", message=str(exc))]


def raise_if_issues(issues: list[PlanIssue]) -> None:
    if not issues:
        return
    error = AgentPlanValidationError(issues)
    try:
        from matrx_utils import vcprint

        vcprint(
            "\n============ AGENT PLAN VALIDATION GATE ============\n"
            f"{error.render()}\n"
            "====================================================",
            color="red",
        )
    except Exception:  # noqa: BLE001 — the banner is best-effort; the raise is not
        pass
    raise error
