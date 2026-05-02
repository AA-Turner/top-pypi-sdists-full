"""Runtime-owned observation and reconciliation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import re
from typing import Protocol
from uuid import uuid4

from packages.contracts.runtime import (
    ArtifactRecord,
    EventEnvelope,
    EvidenceGraph,
    ExecutionResult,
    MemoryRecord,
    StructuredTurnRecord,
    StructuredTurnSlot,
    ActivityGraph,
)
from packages.evidence import build_structured_turn_memory


class _ActivityGraphRepository(Protocol):
    def upsert_activity_graph(self, graph: ActivityGraph) -> None:
        """Persist the canonical activity graph."""


class _EventAppender(Protocol):
    def append_event(self, event: EventEnvelope):
        """Append a durable event or memory envelope."""


def merge_preference_updates(existing: tuple[str, ...], updates: tuple[str, ...]) -> tuple[str, ...]:
    """Merge extracted preference updates into the durable profile preference tuple."""

    merged = [value.strip() for value in existing if value.strip()]
    for update in updates:
        normalized = update.strip()
        if not normalized:
            continue
        prefix = _preference_prefix(normalized)
        if prefix is not None:
            merged = [value for value in merged if not value.startswith(prefix)]
        if normalized not in merged:
            merged.append(normalized)
    return tuple(merged)


@dataclass(frozen=True, slots=True)
class WakeObservation:
    session_id: str
    source: str
    previous_goal_graph: ActivityGraph
    planned_goal_graph: ActivityGraph
    durable_events: tuple[EventEnvelope, ...]
    selected_goal_id: str | None
    decision_summary: str
    observed_delta: bool
    summary: str


@dataclass(frozen=True, slots=True)
class WakeReconciliationReport:
    source: str
    observed_delta: bool
    persisted_activity_graph: bool
    appended_event_types: tuple[str, ...]
    summary: str
    ignored_reason: str | None = None


@dataclass(frozen=True, slots=True)
class TurnProfileDelta:
    user_fields: tuple[tuple[str, str], ...] = ()
    preference_updates: tuple[str, ...] = ()
    relationship_notes: tuple[str, ...] = ()
    summary: str = ""

    @property
    def observed(self) -> bool:
        return bool(self.user_fields or self.preference_updates or self.relationship_notes)


@dataclass(frozen=True, slots=True)
class TurnObservation:
    session_id: str
    source: str
    inbound_event: EventEnvelope
    previous_goal_graph: ActivityGraph
    reconciled_goal_graph: ActivityGraph
    durable_events: tuple[EventEnvelope, ...]
    evidence_memories: tuple[MemoryRecord, ...]
    evidence_artifacts: tuple[ArtifactRecord, ...]
    profile_delta: TurnProfileDelta
    selected_goal_id: str | None
    decision_summary: str
    observed_activity_delta: bool
    summary: str


@dataclass(frozen=True, slots=True)
class TurnReconciliationReport:
    source: str
    observed_activity_delta: bool
    observed_profile_delta: bool
    persisted_activity_graph: bool
    appended_event_types: tuple[str, ...]
    persisted_memory_ids: tuple[str, ...] = ()
    persisted_artifact_ids: tuple[str, ...] = ()
    summary: str = ""
    ignored_reason: str | None = None


class ObservationPipeline:
    """Build durable observations from runtime execution."""

    def observe_wake(
        self,
        *,
        session_id: str,
        previous_goal_graph: ActivityGraph,
        planned_goal_graph: ActivityGraph,
        durable_events: tuple[EventEnvelope, ...],
        selected_goal_id: str | None,
        decision_summary: str,
        source: str = "cli.wake",
    ) -> WakeObservation:
        observed_delta = previous_goal_graph != planned_goal_graph
        target = selected_goal_id or planned_goal_graph.active_goal_id or "no-goal"
        if observed_delta:
            summary = f"Observed a wake-owned durable activity delta for {target}."
        else:
            summary = f"Observed wake rationale for {target} without a durable activity-graph delta."
        return WakeObservation(
            session_id=session_id,
            source=source,
            previous_goal_graph=previous_goal_graph,
            planned_goal_graph=planned_goal_graph,
            durable_events=durable_events,
            selected_goal_id=selected_goal_id,
            decision_summary=decision_summary,
            observed_delta=observed_delta,
            summary=summary,
        )

    def observe_turn(
        self,
        *,
        inbound_event: EventEnvelope,
        execution: ExecutionResult,
        previous_goal_graph: ActivityGraph,
        reconciled_goal_graph: ActivityGraph,
        selected_goal_id: str | None,
        decision_summary: str | None = None,
        include_input_event: bool = True,
        include_outcome_event: bool = True,
        source: str | None = None,
        profile_id: str | None = None,
        workspace_id: str | None = None,
    ) -> TurnObservation:
        resolved_source = source or inbound_event.source
        prompt_text = _event_text(inbound_event)
        profile_delta = _extract_turn_profile_delta(prompt_text)
        durable_events: list[EventEnvelope] = []
        if include_input_event:
            durable_events.append(inbound_event)
        if include_outcome_event:
            outcome_event = _turn_outcome_event(
                session_id=inbound_event.session_id,
                source=resolved_source,
                inbound_event=inbound_event,
                execution=execution,
                selected_goal_id=selected_goal_id,
                decision_summary=decision_summary,
            )
            if outcome_event is not None:
                durable_events.append(outcome_event)
        evidence_memories = (
            _structured_turn_memory_from_turn(
                inbound_event=inbound_event,
                execution=execution,
                reconciled_goal_graph=reconciled_goal_graph,
                selected_goal_id=selected_goal_id,
                decision_summary=decision_summary,
                source=resolved_source,
                profile_id=profile_id,
                workspace_id=workspace_id,
            ),
        )
        evidence_artifacts = _artifact_records_from_execution(
            session_id=inbound_event.session_id,
            execution=execution,
        )
        observed_activity_delta = previous_goal_graph != reconciled_goal_graph
        target = selected_goal_id or reconciled_goal_graph.active_goal_id or "no-goal"
        observed_parts: list[str] = []
        if observed_activity_delta:
            observed_parts.append(f"a durable activity delta for {target}")
        if profile_delta.observed:
            observed_parts.append(profile_delta.summary or "profile and relationship deltas")
        if evidence_memories:
            observed_parts.append(f"{len(evidence_memories)} structured turn evidence record")
        if evidence_artifacts:
            observed_parts.append(f"{len(evidence_artifacts)} execution artifacts")
        if not observed_parts:
            observed_parts.append("no durable owner delta beyond the runtime memory envelopes")
        summary = "Observed a turn-owned reconciliation candidate with " + ", ".join(observed_parts) + "."
        return TurnObservation(
            session_id=inbound_event.session_id,
            source=resolved_source,
            inbound_event=inbound_event,
            previous_goal_graph=previous_goal_graph,
            reconciled_goal_graph=reconciled_goal_graph,
            durable_events=tuple(durable_events),
            evidence_memories=evidence_memories,
            evidence_artifacts=evidence_artifacts,
            profile_delta=profile_delta,
            selected_goal_id=selected_goal_id,
            decision_summary=(decision_summary or execution.summary).strip(),
            observed_activity_delta=observed_activity_delta,
            summary=summary,
        )


class StateReconciler:
    """Apply runtime observations to durable owners."""

    def reconcile_wake(
        self,
        *,
        repository: _ActivityGraphRepository,
        memory_runtime: _EventAppender,
        observation: WakeObservation,
        inspect_only: bool = False,
    ) -> WakeReconciliationReport:
        if inspect_only:
            return WakeReconciliationReport(
                source=observation.source,
                observed_delta=observation.observed_delta,
                persisted_activity_graph=False,
                appended_event_types=(),
                summary="Ignored the wake-owned durable delta because inspect-only mode requested no writes.",
                ignored_reason="inspect_only",
            )

        persisted_activity_graph = False
        if observation.observed_delta:
            repository.upsert_activity_graph(observation.planned_goal_graph)
            persisted_activity_graph = True

        appended_event_types: list[str] = []
        for event in observation.durable_events:
            memory_runtime.append_event(event)
            appended_event_types.append(event.event_type)

        if persisted_activity_graph:
            summary = "Applied the wake-owned durable activity delta through runtime reconciliation and recorded the rationale events."
        else:
            summary = "Recorded wake rationale events through runtime reconciliation and skipped activity-graph persistence because no durable activity delta was observed."

        return WakeReconciliationReport(
            source=observation.source,
            observed_delta=observation.observed_delta,
            persisted_activity_graph=persisted_activity_graph,
            appended_event_types=tuple(appended_event_types),
            summary=summary,
        )

    def reconcile_turn(
        self,
        *,
        repository,
        memory_runtime: _EventAppender,
        observation: TurnObservation,
        inspect_only: bool = False,
    ) -> TurnReconciliationReport:
        if inspect_only:
            return TurnReconciliationReport(
                source=observation.source,
                observed_activity_delta=observation.observed_activity_delta,
                observed_profile_delta=observation.profile_delta.observed,
                persisted_activity_graph=False,
                appended_event_types=(),
                persisted_memory_ids=(),
                persisted_artifact_ids=(),
                summary="Ignored the turn-owned durable delta because inspect-only mode requested no writes.",
                ignored_reason="inspect_only",
            )

        persisted_activity_graph = False
        if observation.observed_activity_delta:
            repository.upsert_activity_graph(observation.reconciled_goal_graph)
            persisted_activity_graph = True

        appended_event_types: list[str] = []
        for event in observation.durable_events:
            memory_runtime.append_event(event)
            appended_event_types.append(event.event_type)

        persisted_memory_ids: list[str] = []
        record_memory = getattr(memory_runtime, "record_memory", None)
        if callable(record_memory):
            for record in observation.evidence_memories:
                decision = record_memory(record)
                if getattr(decision, "allowed", False):
                    persisted_memory_ids.append(record.memory_id)

        persisted_artifact_ids: tuple[str, ...] = ()
        upsert_evidence_graph = getattr(repository, "upsert_evidence_graph", None)
        if callable(upsert_evidence_graph):
            fallback_memories = () if persisted_memory_ids else observation.evidence_memories
            if fallback_memories or observation.evidence_artifacts:
                upsert_evidence_graph(
                    EvidenceGraph(
                        session_id=observation.session_id,
                        memories=fallback_memories,
                        artifacts=observation.evidence_artifacts,
                    )
                )
                if fallback_memories:
                    persisted_memory_ids.extend(record.memory_id for record in fallback_memories)
                persisted_artifact_ids = tuple(artifact.artifact_id for artifact in observation.evidence_artifacts)

        summary_parts: list[str] = []
        if persisted_activity_graph:
            summary_parts.append("applied the activity-graph delta")
        elif observation.observed_activity_delta:
            summary_parts.append("observed a activity-graph delta")
        else:
            summary_parts.append("kept the activity graph unchanged")
        if appended_event_types:
            summary_parts.append(f"recorded {len(appended_event_types)} durable events")
        if persisted_memory_ids:
            summary_parts.append(f"persisted {len(persisted_memory_ids)} structured turn evidence record(s)")
        if persisted_artifact_ids:
            summary_parts.append(f"persisted {len(persisted_artifact_ids)} evidence artifacts")
        if observation.profile_delta.observed:
            summary_parts.append("extracted profile and relationship deltas for the calling surface")
        summary = "Turn reconciliation " + ", ".join(summary_parts) + "."

        return TurnReconciliationReport(
            source=observation.source,
            observed_activity_delta=observation.observed_activity_delta,
            observed_profile_delta=observation.profile_delta.observed,
            persisted_activity_graph=persisted_activity_graph,
            appended_event_types=tuple(appended_event_types),
            persisted_memory_ids=tuple(dict.fromkeys(persisted_memory_ids)),
            persisted_artifact_ids=persisted_artifact_ids,
            summary=summary,
        )


def _extract_turn_profile_delta(text: str) -> TurnProfileDelta:
    normalized = text.strip()
    if not normalized:
        return TurnProfileDelta(summary="")
    user_fields = tuple(_extract_user_fields(normalized).items())
    preference_updates = _extract_preference_updates(normalized)
    relationship_notes = _extract_relationship_notes(normalized)
    summary_parts: list[str] = []
    if user_fields:
        summary_parts.append("user-card fields")
    if preference_updates:
        summary_parts.append("communication preferences")
    if relationship_notes:
        summary_parts.append("relationship continuity notes")
    return TurnProfileDelta(
        user_fields=user_fields,
        preference_updates=preference_updates,
        relationship_notes=relationship_notes,
        summary=", ".join(summary_parts),
    )


def _extract_user_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    preferred = _first_match(
        text,
        (
            r"(?im)^\s*(?:preferred name|name|nickname)\s*[:：]\s*(.+)$",
            r"(?im)^\s*(?:称呼|叫我)\s*[:：]\s*(.+)$",
            r"(?i)\b(?:call me|i go by|my name is|i'm called|i am called)\s+([^\n,.;:]+)",
            r"(?i)(?:可以叫我|叫我|我叫)\s*([^\n，。；：,.;:]+)",
        ),
    )
    if preferred is not None:
        fields["preferred_name"] = preferred
    current_work = _first_match(
        text,
        (
            r"(?im)^\s*(?:current work|work|work focus)\s*[:：]\s*(.+)$",
            r"(?im)^\s*(?:当前工作|工作方向|目前在做)\s*[:：]\s*(.+)$",
            r"(?i)\b(?:i work on|i'm working on|i am working on|i build|i'm building|i am building|current work is|my work is)\s+([^\n.!?]+)",
            r"(?i)(?:我在做|我目前在做|我正在做|我在研究|我正在研究)\s*([^\n。！？]+)",
        ),
    )
    if current_work is not None:
        fields["current_work"] = current_work
    return fields


def _extract_preference_updates(text: str) -> tuple[str, ...]:
    updates: list[str] = []
    lower = text.lower()
    if re.search(r"(?i)(?:reply|respond|responses|replies|answers|be|keep).{0,24}(?:concise|brief|short)", text) or any(
        token in text for token in ("简洁", "简短", "精炼")
    ):
        updates.append("verbosity:concise")
    if re.search(r"(?i)(?:reply|respond|responses|replies|answers|be|keep).{0,24}(?:detailed|thorough|long-form)", text) or any(
        token in text for token in ("详细", "展开一些")
    ):
        updates.append("verbosity:detailed")
    if re.search(r"(?i)(?:reply|respond).{0,16}(?:in chinese)", text) or any(token in text for token in ("用中文", "中文回答", "请中文回答")):
        updates.append("language:zh-CN")
    if re.search(r"(?i)(?:reply|respond).{0,16}(?:in english)", text) or any(token in text for token in ("用英文", "英文回答", "请英文回答")):
        updates.append("language:en")
    if "bullet" in lower or "bullets" in lower or "bullet points" in lower or "要点" in text or "列表" in text:
        updates.append("response-style:bullets")
    return tuple(dict.fromkeys(updates))


def _extract_relationship_notes(text: str) -> tuple[str, ...]:
    notes: list[str] = []
    lines = [line.strip() for line in re.split(r"[\n\r]+", text) if line.strip()]
    if not lines and text.strip():
        lines = [text.strip()]
    for line in lines:
        lowered = line.lower()
        if _first_match(
            line,
            (
                r"(?im)^\s*(?:preferred name|name|nickname|current work|work|work focus)\s*[:：]",
                r"(?im)^\s*(?:称呼|叫我|当前工作|工作方向|目前在做)\s*[:：]",
            ),
        ) is not None:
            continue
        if any(
            marker in lowered
            for marker in (
                "keep replies",
                "keep response",
                "keep responses",
                "reply to me",
                "talk to me",
                "remember that",
                "for future reference",
                "don't call me",
                "do not call me",
                "keep it",
            )
        ) or any(marker in line for marker in ("以后", "记住", "下次", "别叫我", "不要叫我", "回复时", "回答时", "说话时")):
            cleaned = _clean_capture(line)
            if cleaned:
                notes.append(cleaned)
    return tuple(dict.fromkeys(notes))


def _turn_outcome_event(
    *,
    session_id: str,
    source: str,
    inbound_event: EventEnvelope,
    execution: ExecutionResult,
    selected_goal_id: str | None,
    decision_summary: str | None,
) -> EventEnvelope | None:
    content_parts: list[str] = []
    rationale = (decision_summary or "").strip()
    if rationale:
        content_parts.append(rationale)
    summary = execution.summary.strip()
    if summary and summary not in content_parts:
        content_parts.append(summary)
    content = "\n".join(part for part in content_parts if part)
    if not content:
        return None
    return EventEnvelope(
        event_id=f"event:{uuid4().hex}",
        event_type="decision",
        session_id=session_id,
        source=source,
        payload={
            "content": content,
            "summary": content.splitlines()[0],
            "memory_kind": "decision",
            "goal_ids": selected_goal_id or "",
            "tags": "continuity,assistant,turn-outcome",
            "source_event_id": inbound_event.event_id,
            "execution_id": execution.execution_id,
            "execution_outcome": execution.outcome,
        },
    )


def _artifact_records_from_execution(
    *,
    session_id: str,
    execution: ExecutionResult,
) -> tuple[ArtifactRecord, ...]:
    created_at = datetime.now(timezone.utc)
    artifacts = []
    for artifact_id in execution.produced_artifact_ids:
        resolved = artifact_id.strip()
        if not resolved:
            continue
        artifacts.append(
            ArtifactRecord(
                artifact_id=resolved,
                session_id=session_id,
                kind="execution-artifact",
                name=resolved,
                uri=f"artifact://{resolved}",
                created_at=created_at,
            )
        )
    return tuple(artifacts)


def _structured_turn_memory_from_turn(
    *,
    inbound_event: EventEnvelope,
    execution: ExecutionResult,
    reconciled_goal_graph: ActivityGraph,
    selected_goal_id: str | None,
    decision_summary: str | None,
    source: str,
    profile_id: str | None,
    workspace_id: str | None,
) -> MemoryRecord:
    reasoning_trace = _payload_text(inbound_event, "reasoning_trace", "raw_reasoning_trace")
    reasoning_summary = _payload_text(inbound_event, "reasoning_summary") or (decision_summary or execution.summary).strip()
    reasoning_availability = "raw_trace" if reasoning_trace else ("structured_summary" if reasoning_summary else "unavailable")
    reasoning_provenance = _payload_text(inbound_event, "reasoning_provenance") or (
        "provider.raw_trace" if reasoning_trace else "runtime.decision_summary"
    )
    work_item_ids = _turn_work_item_ids(reconciled_goal_graph, selected_goal_id=selected_goal_id)
    action_detail = _tool_call_details(execution)
    artifact_ids = tuple(artifact_id for artifact_id in execution.produced_artifact_ids if artifact_id.strip())
    turn_id = f"{inbound_event.event_id}:structured-turn"
    record = StructuredTurnRecord(
        turn_id=turn_id,
        session_id=inbound_event.session_id,
        source=source,
        observation=StructuredTurnSlot(
            summary=_compact_text(_event_text(inbound_event), limit=180),
            detail=(_event_text(inbound_event),) if _event_text(inbound_event) else (),
            compression="raw_turn",
            provenance="user.input",
            source_refs=(inbound_event.event_id,),
            linkage_refs=work_item_ids,
        ),
        reasoning=StructuredTurnSlot(
            summary=reasoning_summary,
            detail=((reasoning_trace,) if reasoning_trace else ((reasoning_summary,) if reasoning_summary else ())),
            compression="raw_trace" if reasoning_trace else ("structured_summary" if reasoning_summary else "none"),
            provenance=reasoning_provenance,
            source_refs=(inbound_event.event_id, execution.execution_id),
            linkage_refs=work_item_ids,
        ),
        action=StructuredTurnSlot(
            summary=(
                f"executed {len(action_detail)} recorded action(s)"
                if action_detail
                else ("completed without tool calls" if execution.outcome == "ok" else "no tool action detail was recorded")
            ),
            detail=action_detail,
            compression="structured",
            provenance="runtime.execution",
            source_refs=(execution.execution_id,),
            linkage_refs=work_item_ids + artifact_ids,
        ),
        outcome=StructuredTurnSlot(
            summary=execution.summary.strip() or f"turn outcome: {execution.outcome}",
            detail=tuple(
                item
                for item in (
                    f"outcome:{execution.outcome}",
                    *(f"artifact:{artifact_id}" for artifact_id in artifact_ids),
                    *execution.side_effects,
                )
                if item
            ),
            compression="structured",
            provenance="runtime.execution",
            source_refs=(execution.execution_id,),
            linkage_refs=artifact_ids or work_item_ids,
        ),
        profile_id=profile_id,
        workspace_id=workspace_id,
        source_event_id=inbound_event.event_id,
        reasoning_availability=reasoning_availability,
        reasoning_provenance=reasoning_provenance,
        compression_tier="raw_turn",
        work_item_ids=work_item_ids,
        source_turn_ids=(turn_id,),
        artifact_ids=artifact_ids,
        created_at=datetime.now(timezone.utc),
    )
    return build_structured_turn_memory(record)


def _turn_work_item_ids(
    reconciled_goal_graph: ActivityGraph,
    *,
    selected_goal_id: str | None,
) -> tuple[str, ...]:
    work_item_ids: list[str] = []
    if selected_goal_id is not None:
        work_item_ids.append(selected_goal_id)
    if reconciled_goal_graph.active_goal_id is not None:
        work_item_ids.append(reconciled_goal_graph.active_goal_id)
    active_goal = reconciled_goal_graph.active_goal()
    if active_goal is not None and active_goal.parent_goal_id is not None:
        work_item_ids.append(active_goal.parent_goal_id)
    for goal in reconciled_goal_graph.goals:
        if goal.status in {"active", "blocked", "queued", "proposed"}:
            work_item_ids.append(goal.goal_id)
        if len(work_item_ids) >= 5:
            break
    return tuple(dict.fromkeys(goal_id for goal_id in work_item_ids if goal_id))


def _tool_call_details(execution: ExecutionResult) -> tuple[str, ...]:
    details: list[str] = []
    for call in execution.tool_calls:
        argument_keys = tuple(sorted(str(key) for key in call.arguments.keys()))
        if argument_keys:
            details.append(f"{call.tool_name}({', '.join(argument_keys)})")
        else:
            details.append(call.tool_name)
    for artifact_id in execution.produced_artifact_ids:
        resolved = artifact_id.strip()
        if resolved:
            details.append(f"artifact:{resolved}")
    return tuple(dict.fromkeys(details))


def _payload_text(event: EventEnvelope, *keys: str) -> str:
    for key in keys:
        value = event.payload.get(key)
        if value is None:
            continue
        cleaned = str(value).strip()
        if cleaned:
            return cleaned
    return ""


def _compact_text(value: str, *, limit: int) -> str:
    compact = re.sub(r"\s+", " ", value).strip()
    if len(compact) <= limit:
        return compact
    return compact[: max(0, limit - 1)].rstrip() + "…"


def _event_text(event: EventEnvelope) -> str:
    payload = event.payload
    text = payload.get("content") or payload.get("message") or payload.get("summary") or ""
    return str(text).strip()


def _first_match(text: str, patterns: tuple[str, ...]) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text)
        if match is None:
            continue
        cleaned = _clean_capture(match.group(1) if match.lastindex else match.group(0))
        if cleaned:
            return cleaned
    return None


def _clean_capture(value: str) -> str:
    cleaned = re.sub(r"\s+", " ", value).strip()
    return cleaned.strip(" ,.;:，。；：")


def _preference_prefix(value: str) -> str | None:
    for prefix in ("tone:", "verbosity:", "language:", "response-style:"):
        if value.startswith(prefix):
            return prefix
    return None
