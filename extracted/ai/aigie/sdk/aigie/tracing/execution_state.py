"""Per-trace execution state aggregator.

Replaces the 13 ad-hoc dicts in AigieCallbackHandler.__init__ with a
single cohesive object. Tracks the workflow's execution path, per-span
timing/status/errors, agent iteration counts, run-level counters
(turns, tool calls), plus optional event lists (edge conditions, state
transitions, nested workflows, retries) that are populated conditionally
based on chain metadata.

Used by the framework callback while the run is in flight; produces the
``execution_data`` and ``execution_plan`` payloads at trace finalization.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ExecutionState:
    """Mutable per-trace state. One instance per trace."""

    execution_path: list[str] = field(default_factory=list)
    execution_timing: dict[str, dict[str, Any]] = field(default_factory=dict)
    execution_status: dict[str, str] = field(default_factory=dict)
    execution_errors: dict[str, str] = field(default_factory=dict)
    agent_iterations: dict[str, int] = field(default_factory=dict)
    span_start_times: dict[str, str] = field(default_factory=dict)
    turn_count: int = 0
    tool_call_count: int = 0

    # Optional event lists — populated only when the framework surfaces
    # the corresponding metadata. Kept empty by default so they don't
    # pollute execution_data when unused.
    edge_conditions: list[dict[str, Any]] = field(default_factory=list)
    state_transitions: list[dict[str, Any]] = field(default_factory=list)
    nested_workflows: list[dict[str, Any]] = field(default_factory=list)
    retry_info: list[dict[str, Any]] = field(default_factory=list)

    def start_span(self, *, name: str, span_type: str, at: datetime) -> None:
        self.execution_path.append(name)
        iso = at.isoformat()
        self.execution_timing[name] = {"start_time": iso, "end_time": None, "duration_ms": 0}
        self.execution_status[name] = "running"
        self.span_start_times[name] = iso

    def end_span(
        self,
        *,
        name: str,
        status: str,
        at: datetime,
        error_message: str | None = None,
    ) -> None:
        timing = self.execution_timing.get(name)
        if timing:
            timing["end_time"] = at.isoformat()
            start_iso = timing.get("start_time")
            if start_iso:
                start_dt = datetime.fromisoformat(start_iso)
                timing["duration_ms"] = int((at - start_dt).total_seconds() * 1000)
        self.execution_status[name] = status
        if error_message and status == "error":
            self.execution_errors[name] = error_message

    def track_agent_iteration(self, agent_name: str) -> None:
        self.agent_iterations[agent_name] = self.agent_iterations.get(agent_name, 0) + 1

    def track_edge_condition(self, *, step_name: str, condition: Any, result: Any = None) -> None:
        self.edge_conditions.append({"step": step_name, "condition": condition, "result": result})

    def track_state_transition(
        self, *, from_state: Any, to_state: Any, trigger: Any = None
    ) -> None:
        self.state_transitions.append(
            {"from_state": from_state, "to_state": to_state, "trigger": trigger}
        )

    def track_nested_workflow(self, *, workflow_name: str, trace_id: str) -> None:
        self.nested_workflows.append({"workflow_name": workflow_name, "trace_id": trace_id})

    def track_retry(self, *, span_name: str, attempt: int, reason: str | None = None) -> None:
        self.retry_info.append({"span_name": span_name, "attempt": attempt, "reason": reason})

    def to_execution_data(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "execution_path": list(self.execution_path),
            "execution_timing": dict(self.execution_timing),
            "execution_status": dict(self.execution_status),
            "execution_errors": dict(self.execution_errors),
            "agent_iterations": dict(self.agent_iterations),
        }
        if self.edge_conditions:
            out["edge_conditions"] = list(self.edge_conditions)
        if self.state_transitions:
            out["state_transitions"] = list(self.state_transitions)
        if self.nested_workflows:
            out["nested_workflows"] = list(self.nested_workflows)
        if self.retry_info:
            out["retry_info"] = list(self.retry_info)
        return out

    def to_execution_plan(self, *, agent_name: str, status: str) -> dict[str, Any]:
        return build_execution_plan(
            agent=agent_name,
            tool_calls=self.tool_call_count,
            turn_count=self.turn_count,
            status=status,
        )


def build_execution_plan(
    *, agent: str, tool_calls: int, turn_count: int, status: str
) -> dict[str, Any]:
    """The run summary every framework integration stamps on its run root.

    Goal Adherence & Drift binds ``{{execution_plan}}`` to this payload, so the
    four keys are a wire contract shared across the integrations rather than a
    detail of whichever one emits it. Kept as a free function because only the
    LangChain family accumulates an :class:`ExecutionState`; the other
    integrations already carry their own run-level counters and need the shape,
    not the aggregator.
    """
    return {
        "agent": agent,
        "tool_calls": tool_calls,
        "turn_count": turn_count,
        "status": status,
    }
