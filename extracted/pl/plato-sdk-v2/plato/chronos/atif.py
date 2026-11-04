"""Client-side ATIF trajectory reconstruction from OTel spans.

Chronos no longer serves ``GET /api/sessions/{id}/trajectory`` — the server-side
build capped sessions at 1000 spans (returning silently partial trajectories)
and pinned chronos workers on large sessions. ``Chronos.get_trajectory()`` now
drains the session's agent spans from the logs-stream endpoint — the same
uncapped, cursor-resumable source the chronos UI and ``plato chronos traces``
read — and rebuilds the identical ``SessionTrajectory`` shape here.

The models are the chronos-generated ones from ``plato.chronos.models``
(re-exported here for compatibility): chronos keeps the SessionTrajectory
family referenced in its OpenAPI via the ``/api/sessions/schemas/atif-trajectory``
schema-carrier endpoint, so SDK regeneration maintains them — nothing is
hand-written. Because the wire models carry no parsing logic, this converter
decodes the JSON-string span attributes (tool_calls, observation) itself.
``total_count``/``has_more`` are kept for payload compatibility but a
client-built trajectory is always complete: ``has_more`` is always ``False``.
"""

from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Sequence
from typing import Any

from plato.chronos.models import (
    AgentStep,
    AgentStepMetrics,
    AgentTrace,
    AgentTrajectory,
    Artifact,
    OTelSpanSchema,
    SessionTrajectory,
    Status,
    TrajectoryAgentInfo,
    TrajectoryMetrics,
    TrajectoryObservation,
    TrajectoryObservationResult,
    TrajectorySandboxInfo,
    TrajectoryToolCall,
    TrajectoryWorldInfo,
    WorldStep,
)

__all__ = [
    "AgentStep",
    "AgentStepMetrics",
    "AgentTrace",
    "AgentTrajectory",
    "Artifact",
    "SessionTrajectory",
    "TrajectoryAgentInfo",
    "TrajectoryMetrics",
    "TrajectoryObservation",
    "TrajectoryObservationResult",
    "TrajectorySandboxInfo",
    "TrajectoryToolCall",
    "TrajectoryWorldInfo",
    "WorldStep",
    "spans_to_trajectory",
    "total_metrics",
]


def total_metrics(trajectory: SessionTrajectory) -> TrajectoryMetrics:
    """Aggregated metrics across all agents in the session."""
    totals = TrajectoryMetrics()
    for trace in trajectory.agents or []:
        fm = trace.trajectory.final_metrics
        if fm is None:
            continue
        totals.total_steps = (totals.total_steps or 0) + (fm.total_steps or 0)
        totals.prompt_tokens = (totals.prompt_tokens or 0) + (fm.prompt_tokens or 0)
        totals.completion_tokens = (totals.completion_tokens or 0) + (fm.completion_tokens or 0)
        totals.cost_usd = (totals.cost_usd or 0.0) + (fm.cost_usd or 0.0)
    return totals


# ============= Span → trajectory conversion =============


def _safe_int(value: object) -> int:
    """Coerce a value to int, handling strings from ClickHouse JSON columns.

    Uses float() as intermediate to handle float-formatted strings like "150.0".
    """
    try:
        return int(float(value))  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0


def _safe_float(value: object) -> float:
    """Coerce a value to float, handling strings from ClickHouse JSON columns."""
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0.0


def _parse_json_attr(value: Any) -> Any:
    """ATIF tool_calls/observation span attributes arrive as JSON strings.

    The generated wire models carry no parsing validators (the removed server
    endpoint used to decode these), so the converter decodes them itself.
    Undecodable strings become None, matching the old server behavior.
    """
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return None
    return value


def _build_trajectory(spans: list[OTelSpanSchema], session_id: str) -> AgentTrajectory:
    """Build a single ATIF trajectory from one agent's group of spans."""
    agent_info: dict[str, Any] = {}
    for span in spans:
        attrs = span.attributes or {}
        if "atif.agent.name" in attrs:
            agent_info = {
                "name": attrs.get("atif.agent.name"),
                "version": attrs.get("atif.agent.version"),
                "model_name": attrs.get("atif.agent.model_name"),
                "atif_version": attrs.get("atif.version"),
            }
            if "atif.session.success" in attrs:
                agent_info["success"] = attrs["atif.session.success"]
            if "atif.session.result" in attrs:
                agent_info["result"] = attrs["atif.session.result"]
            if "atif.session.error" in attrs:
                agent_info["error"] = attrs["atif.session.error"]
            if "atif.agent.config" in attrs:
                agent_info["config"] = attrs["atif.agent.config"]
            if "atif.agent.turn_count" in attrs:
                agent_info["turn_count"] = _safe_int(attrs["atif.agent.turn_count"])
            sandbox: dict[str, Any] = {}
            if "atif.sandbox.type" in attrs:
                sandbox["type"] = attrs["atif.sandbox.type"]
            if "atif.sandbox.cpus" in attrs:
                sandbox["cpus"] = attrs["atif.sandbox.cpus"]
            if "atif.sandbox.memory_mb" in attrs:
                sandbox["memory_mb"] = attrs["atif.sandbox.memory_mb"]
            if "atif.sandbox.disk_mb" in attrs:
                sandbox["disk_mb"] = attrs["atif.sandbox.disk_mb"]
            if sandbox:
                agent_info["sandbox"] = sandbox
            break

    step_spans = [s for s in spans if s.attributes and "atif.step.id" in s.attributes]
    step_spans.sort(key=lambda s: _safe_int((s.attributes or {}).get("atif.step.id", 0)))

    steps: list[dict[str, Any]] = []
    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_cost_usd = 0.0

    for s in step_spans:
        attrs = s.attributes or {}
        step: dict[str, Any] = {
            "step_id": _safe_int(attrs.get("atif.step.id")),
            "span_id": s.span_id,
            "source": attrs.get("atif.step.source") or "",
            "message": attrs.get("atif.step.message", ""),
        }

        if "atif.step.model_name" in attrs:
            step["model_name"] = attrs["atif.step.model_name"]
        if "atif.step.reasoning" in attrs:
            step["reasoning_content"] = attrs["atif.step.reasoning"]
        if "atif.step.tool_calls" in attrs:
            step["tool_calls"] = _parse_json_attr(attrs["atif.step.tool_calls"])
        if "atif.step.observation" in attrs:
            step["observation"] = _parse_json_attr(attrs["atif.step.observation"])
        if "atif.step.screenshot" in attrs:
            step["screenshot"] = attrs["atif.step.screenshot"]
        if "atif.step.screenshot_format" in attrs:
            step["screenshot_format"] = attrs["atif.step.screenshot_format"]

        metrics: dict[str, Any] = {}
        if "atif.step.prompt_tokens" in attrs:
            pt = _safe_int(attrs["atif.step.prompt_tokens"])
            metrics["prompt_tokens"] = pt
            total_prompt_tokens += pt
        if "atif.step.completion_tokens" in attrs:
            ct = _safe_int(attrs["atif.step.completion_tokens"])
            metrics["completion_tokens"] = ct
            total_completion_tokens += ct
        if "atif.step.cost_usd" in attrs:
            cu = _safe_float(attrs["atif.step.cost_usd"])
            metrics["cost_usd"] = cu
            total_cost_usd += cu

        if metrics:
            step["metrics"] = metrics

        step["start_time_unix_nano"] = s.start_time_unix_nano
        if s.end_time_unix_nano:
            step["end_time_unix_nano"] = s.end_time_unix_nano

        steps.append(step)

    # Use agent-level totals as fallback when step-level totals are missing.
    # Some agents (e.g. openhands) report atif.agent.cost_usd on the root span
    # but don't break costs down per step.
    for span in spans:
        attrs = span.attributes or {}
        if "atif.agent.name" in attrs:
            if total_cost_usd == 0.0 and "atif.agent.cost_usd" in attrs:
                total_cost_usd = _safe_float(attrs["atif.agent.cost_usd"])
            if total_prompt_tokens == 0 and "atif.agent.prompt_tokens" in attrs:
                total_prompt_tokens = _safe_int(attrs["atif.agent.prompt_tokens"])
            if total_completion_tokens == 0 and "atif.agent.completion_tokens" in attrs:
                total_completion_tokens = _safe_int(attrs["atif.agent.completion_tokens"])
            break

    return AgentTrajectory.model_validate(
        {
            "session_id": session_id,
            "agent": agent_info,
            "steps": steps,
            "final_metrics": {
                "total_steps": len(steps),
                "prompt_tokens": total_prompt_tokens,
                "completion_tokens": total_completion_tokens,
                "cost_usd": total_cost_usd,
            },
        }
    )


def _is_descendant(
    span_id: str,
    ancestor_id: str,
    span_by_id: dict[str, OTelSpanSchema],
) -> bool:
    """Check if span_id is a descendant of ancestor_id by walking parents."""
    current = span_id
    seen: set[str] = set()
    while current and current not in seen:
        if current == ancestor_id:
            return True
        seen.add(current)
        parent = span_by_id.get(current)
        if parent and parent.parent_span_id:
            current = parent.parent_span_id
        else:
            break
    return False


def spans_to_trajectory(spans: Sequence[OTelSpanSchema], session_id: str, status: str = "queued") -> SessionTrajectory:
    """Convert a session's OTel spans into a SessionTrajectory.

    Extracts:
    - World info from spans with plato.phase attributes
    - World steps from plato.phase="step" spans (with observation, done, timing)
    - Agent traces from atif.agent.name spans, correlated to their parent world step
    - Artifacts from plato.type="artifact" spans

    Pass the spans returned by ``get_all_traces(session_id, atif_only=True)``
    (plus ``plato_type="artifact"`` spans if artifacts matter to the caller);
    ``Chronos.get_trajectory`` does exactly that. Duplicate span_ids (e.g. a
    span matching both filters) are deduplicated here.
    """
    span_by_id: dict[str, OTelSpanSchema] = {s.span_id: s for s in spans}
    spans = list(span_by_id.values())

    children_by_parent: dict[str, list[OTelSpanSchema]] = defaultdict(list)
    for s in spans:
        if s.parent_span_id:
            children_by_parent[s.parent_span_id].append(s)

    # Extract world info from the root world span (plato.phase="world_start")
    world_info: dict[str, Any] = {}
    for s in spans:
        attrs = s.attributes or {}
        if attrs.get("plato.phase") == "world_start":
            world_info = {
                "name": attrs.get("plato.world.name"),
                "version": attrs.get("plato.world.version"),
            }
            break

    # Extract world config and observation from reset span
    for s in spans:
        attrs = s.attributes or {}
        if attrs.get("plato.phase") == "reset":
            if "plato.world.config" in attrs:
                try:
                    world_info["config"] = json.loads(attrs["plato.world.config"])
                except (ValueError, TypeError):
                    world_info["config"] = attrs["plato.world.config"]
            if "plato.observation" in attrs:
                world_info["observation"] = attrs["plato.observation"]
            break

    # Extract world steps (plato.phase="step")
    world_step_spans: list[OTelSpanSchema] = []
    for s in spans:
        attrs = s.attributes or {}
        if attrs.get("plato.phase") == "step":
            world_step_spans.append(s)
    world_step_spans.sort(key=lambda s: _safe_int((s.attributes or {}).get("plato.step.number", 0)))

    # Find all ATIF agent session spans. Per-model cost rollup child spans
    # (``atif.cost.{model}``, emitted under the session root by the harness)
    # also carry ``atif.agent.name``, so only top-level candidates — not
    # descendants of another candidate — count as agent roots. Without this,
    # each rollup becomes a phantom zero-step trace and ``total_metrics``
    # double-counts its agent-level cost/token attributes on top of the real
    # agent's per-step sums.
    candidates: list[OTelSpanSchema] = []
    for s in spans:
        attrs = s.attributes or {}
        if "atif.agent.name" in attrs:
            candidates.append(s)
    candidate_ids = {s.span_id for s in candidates}

    def _descends_from_candidate(span: OTelSpanSchema) -> bool:
        current = span.parent_span_id
        seen: set[str] = set()
        while current and current not in seen:
            if current in candidate_ids:
                return True
            seen.add(current)
            parent = span_by_id.get(current)
            current = parent.parent_span_id if parent else None
        return False

    agent_session_spans = [s for s in candidates if not _descends_from_candidate(s)]

    # Build agent traces (BFS descendants from each agent session span)
    def _build_agent_trace(session_span: OTelSpanSchema) -> AgentTrace:
        group: list[OTelSpanSchema] = [session_span]
        queue = [session_span.span_id]
        while queue:
            parent_id = queue.pop(0)
            for child in children_by_parent.get(parent_id, []):
                group.append(child)
                queue.append(child.span_id)
        trajectory = _build_trajectory(group, session_id)
        return AgentTrace(
            agent=trajectory.agent,
            trajectory=trajectory,
            trace_id=session_span.trace_id,
            span_count=len(group),
        )

    traces_by_root_span: dict[str, AgentTrace] = {s.span_id: _build_agent_trace(s) for s in agent_session_spans}
    all_agents = list(traces_by_root_span.values())

    # Build world steps with correlated agents
    world_steps: list[WorldStep] = []
    for ws in world_step_spans:
        attrs = ws.attributes or {}

        # Find agents whose session span is a descendant of this world step
        step_agents = [
            traces_by_root_span[agent_span.span_id]
            for agent_span in agent_session_spans
            if _is_descendant(agent_span.span_id, ws.span_id, span_by_id)
        ]

        world_steps.append(
            WorldStep(
                number=_safe_int(attrs.get("plato.step.number")),
                span_id=ws.span_id,
                done=bool(attrs.get("plato.step.done", False)),
                observation=attrs.get("plato.step.observation"),
                agents=step_agents,
                start_time_unix_nano=ws.start_time_unix_nano,
                end_time_unix_nano=ws.end_time_unix_nano,
            )
        )

    world_info["steps"] = world_steps

    # Extract artifacts (plato.type="artifact")
    artifacts: list[Artifact] = []
    for s in spans:
        attrs = s.attributes or {}
        if attrs.get("plato.type") == "artifact":
            artifacts.append(
                Artifact(
                    kind=attrs.get("plato.artifact.kind", ""),
                    url=attrs.get("plato.artifact.url", ""),
                    session_id=attrs.get("plato.artifact.session_id"),
                    start_time_unix_nano=s.start_time_unix_nano,
                    end_time_unix_nano=s.end_time_unix_nano,
                )
            )

    return SessionTrajectory(
        session_id=session_id,
        status=Status(status) if isinstance(status, str) else status,
        world=TrajectoryWorldInfo.model_validate(world_info),
        agents=all_agents,
        artifacts=artifacts,
        total_count=len(spans),
        has_more=False,
    )
