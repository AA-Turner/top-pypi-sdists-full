from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from .snapshot_io import load_snapshot_payload, write_snapshot_payload
from packages.contracts.runtime import (
    ContextBundle,
    EventEnvelope,
    ExecutionResult,
    ExperienceRecord,
    GoalNode,
    IntentCandidateScore,
    IntentDecision,
    IntentReason,
    MemoryRecord,
    PlanDraft,
    ProfileGrowthState,
    ProfileState,
    ProcedureLibrary,
    SessionState,
)
from packages.experience import capture_turn_experience
from packages.growth import GrowthTurnSignals, apply_turn_growth
from packages.kernel import KernelOutcome
from packages.skills import builtin_prompt_skill_catalog_entries

if TYPE_CHECKING:
    from apps.cli.runtime import CliRuntime


@dataclass(frozen=True, slots=True)
class SessionContextEpoch:
    session_id: str
    frozen: bool = False
    frozen_prefix: str = ""
    session_snapshot: str = ""
    base_turn_injections: str = ""
    tool_schema: str = ""
    thread_focus: str = ""
    frozen_skill_count: int = 0
    frozen_tool_count: int = 0
    frozen_skill_index: tuple["FrozenSkillIndexEntry", ...] = ()
    frozen_skill_ids: tuple[str, ...] = ()
    frozen_tool_ids: tuple[str, ...] = ()
    frozen_skill_disclosures: tuple["SkillDisclosureRecord", ...] = ()
    latest_skill_disclosures: tuple["SkillDisclosureRecord", ...] = ()
    compacted_history_summary: str = ""
    compaction_count: int = 0
    compacted_history_count: int = 0
    context_projection_tokens: int = 0
    context_projection_limit: int = 0
    history_lines: tuple[str, ...] = ()
    frozen_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class SkillDisclosureRecord:
    skill_id: str
    display_name: str = ""
    reason: str = ""
    source: str = "intent-selection"


@dataclass(frozen=True, slots=True)
class FrozenSkillIndexEntry:
    skill_id: str
    display_name: str = ""
    category: str = ""
    source_id: str = ""
    storage_tier: str = ""
    slash_command: str = ""


def load_snapshot(runtime: CliRuntime) -> dict[str, Any] | None:
    return load_snapshot_payload(runtime.snapshot_path)


def load_snapshot_intent(runtime: CliRuntime, *, session_id: str | None = None) -> IntentDecision | None:
    snapshot = load_snapshot(runtime)
    return restore_snapshot_intent(snapshot, session_id=session_id)


def restore_snapshot_intent(
    snapshot: Mapping[str, Any] | None,
    *,
    session_id: str | None = None,
) -> IntentDecision | None:
    if not snapshot:
        return None
    if session_id is not None:
        session = snapshot.get("session")
        if not isinstance(session, Mapping) or str(session.get("session_id") or "") != session_id:
            return None
    payload = snapshot.get("intent")
    if not isinstance(payload, Mapping):
        return None
    reasons = tuple(_restore_intent_reason(reason) for reason in payload.get("reasons", ()) if isinstance(reason, Mapping))
    candidate_scores = tuple(
        _restore_intent_candidate_score(score)
        for score in payload.get("candidate_scores", ())
        if isinstance(score, Mapping)
    )
    return IntentDecision(
        intent=str(payload.get("intent") or "").strip(),
        confidence=float(payload.get("confidence") or 0.0),
        focus_activity_ids=_as_str_tuple(payload.get("focus_activity_ids")),
        provisional_activity_seed=_optional_str(payload.get("provisional_activity_seed")),
        resume_signal=str(payload.get("resume_signal") or "none"),
        scope_suggestion=str(payload.get("scope_suggestion") or "session"),
        budget_class=str(payload.get("budget_class") or "standard"),
        embedding_available=bool(payload.get("embedding_available", False)),
        degradation_mode=str(payload.get("degradation_mode") or "none"),
        needs_weak_model_assist=bool(payload.get("needs_weak_model_assist", False)),
        weak_assist_outcome=str(payload.get("weak_assist_outcome") or "not-requested"),
        fallback_path=str(payload.get("fallback_path") or "direct"),
        reasons=reasons,
        candidate_scores=candidate_scores,
        audit_trace=_as_str_tuple(payload.get("audit_trace")),
    )


def load_snapshot_session_context_epoch(
    runtime: CliRuntime,
    *,
    session_id: str | None = None,
) -> SessionContextEpoch | None:
    return restore_snapshot_session_context_epoch(load_snapshot(runtime), session_id=session_id)


def restore_snapshot_session_context_epoch(
    snapshot: Mapping[str, Any] | None,
    *,
    session_id: str | None = None,
) -> SessionContextEpoch | None:
    if not snapshot:
        return None
    if session_id is not None:
        session = snapshot.get("session")
        if not isinstance(session, Mapping) or str(session.get("session_id") or "") != session_id:
            return None
    payload = snapshot.get("session_context_epoch")
    if not isinstance(payload, Mapping):
        return None
    resolved_session_id = str(payload.get("session_id") or "").strip()
    if not resolved_session_id:
        return None
    return SessionContextEpoch(
        session_id=resolved_session_id,
        frozen=bool(payload.get("frozen", False)),
        frozen_prefix=str(payload.get("frozen_prefix") or ""),
        session_snapshot=str(payload.get("session_snapshot") or ""),
        base_turn_injections=_base_turn_injection_refs(payload.get("base_turn_injections")),
        tool_schema=str(payload.get("tool_schema") or ""),
        thread_focus=str(payload.get("thread_focus") or ""),
        frozen_skill_count=int(payload.get("frozen_skill_count") or 0),
        frozen_tool_count=int(payload.get("frozen_tool_count") or 0),
        frozen_skill_index=_frozen_skill_index_tuple(payload.get("frozen_skill_index")),
        frozen_skill_ids=_as_str_tuple(payload.get("frozen_skill_ids")),
        frozen_tool_ids=_as_str_tuple(payload.get("frozen_tool_ids")),
        frozen_skill_disclosures=_skill_disclosure_tuple(payload.get("frozen_skill_disclosures")),
        latest_skill_disclosures=_skill_disclosure_tuple(payload.get("latest_skill_disclosures")),
        compacted_history_summary=str(payload.get("compacted_history_summary") or ""),
        compaction_count=int(payload.get("compaction_count") or 0),
        compacted_history_count=int(payload.get("compacted_history_count") or 0),
        context_projection_tokens=int(payload.get("context_projection_tokens") or 0),
        context_projection_limit=int(payload.get("context_projection_limit") or 0),
        history_lines=_as_str_tuple(payload.get("history_lines")),
        frozen_at=_optional_datetime(payload.get("frozen_at")),
    )


def write_snapshot_session_context_epoch(runtime: CliRuntime, epoch: SessionContextEpoch) -> None:
    payload = load_snapshot(runtime) or {}
    payload["session_context_epoch"] = _session_context_epoch_payload(epoch)
    write_snapshot_payload(runtime.snapshot_path, payload)


def append_outcome_memory(runtime: CliRuntime, outcome: KernelOutcome) -> None:
    goal_ids: tuple[str, ...] = ()
    tags: tuple[str, ...] = ("continuity", "assistant")
    content = outcome.execution.summary.strip()
    if outcome.decision is not None:
        selected_goal_id = outcome.decision.selected_move.goal_id
        if selected_goal_id:
            goal_ids = (selected_goal_id,)
        tags = tags + (outcome.decision.selected_move.kind,)
        rationale = outcome.decision.rationale.summary.strip()
        if rationale and rationale not in content:
            content = f"{rationale}\n{content}" if content else rationale
    elif outcome.plan is not None and outcome.plan.goal_id:
        goal_ids = (outcome.plan.goal_id,)
    if not content:
        return
    event = EventEnvelope(
        event_id=f"event:{uuid4().hex}",
        event_type="decision",
        session_id=outcome.session.session_id,
        source="cli",
        payload={
            "content": content,
            "summary": content.splitlines()[0],
            "memory_kind": "decision",
            "goal_ids": ",".join(goal_ids),
            "tags": ",".join(tags),
            "source_event_id": outcome.event.event_id,
        },
    )
    runtime.memory_runtime.append_event(event)


def append_outcome_experience(runtime: CliRuntime, outcome: KernelOutcome) -> ExperienceRecord | None:
    execution = outcome.execution
    if execution is None:
        return None
    goal_id: str | None = None
    if outcome.decision is not None:
        goal_id = outcome.decision.selected_move.goal_id
    elif outcome.plan is not None and outcome.plan.goal_id:
        goal_id = outcome.plan.goal_id
    active_skills = runtime.skill_runtime.resolve_for_context(
        profile_id=outcome.session.profile_id,
        workspace_id=outcome.session.workspace_id,
        session_id=outcome.session.session_id,
        mode=outcome.profile.mode,
    )
    extra_tags: list[str] = [f"outcome:{execution.outcome}"]
    if outcome.decision is not None:
        extra_tags.append(f"decision:{outcome.decision.selected_move.kind}")
    record = capture_turn_experience(
        session_id=outcome.session.session_id,
        profile_id=outcome.session.profile_id,
        workspace_id=outcome.session.workspace_id,
        summary=execution.summary,
        source_event_id=outcome.event.event_id,
        run_id=outcome.run.run_id if outcome.run is not None else None,
        goal_id=goal_id,
        tool_call_count=outcome.run.tool_call_count if outcome.run is not None else 0,
        model_turn_count=outcome.run.model_turn_count if outcome.run is not None else 0,
        related_skill_ids=tuple(skill.skill_id for skill in active_skills),
        produced_artifact_ids=execution.produced_artifact_ids,
        tags=tuple(extra_tags),
    )
    if record is None:
        return None
    runtime.repository.upsert_experience(record)
    return record


def append_outcome_growth(
    runtime: CliRuntime,
    outcome: KernelOutcome,
    *,
    experience: ExperienceRecord | None,
) -> ProfileGrowthState:
    profile_id = outcome.session.profile_id
    current = runtime.repository.load_profile_growth(profile_id)
    if _growth_state_predates_profile_sessions(runtime, profile_id=profile_id, state=current):
        current = None
    procedure_library = runtime.repository.load_procedure_library(profile_id)
    update = apply_turn_growth(
        current,
        _build_growth_turn_signals(
            current=current,
            outcome=outcome,
            experience=experience,
            procedure_library=procedure_library,
        ),
    )
    runtime.repository.upsert_profile_growth(update.after.state)
    runtime.growth_updates[outcome.session.session_id] = update
    return update.after.state


def _growth_state_predates_profile_sessions(
    runtime: CliRuntime,
    *,
    profile_id: str,
    state: ProfileGrowthState | None,
) -> bool:
    if state is None:
        return False
    growth_timestamp = state.updated_at or state.created_at or state.last_dialogue_at or state.first_dialogue_at
    if growth_timestamp is None:
        return False
    with runtime.repository.connection() as connection:
        row = connection.execute(
            """
            SELECT MIN(started_at) AS first_started_at
            FROM sessions
            WHERE profile_id = ?
            """,
            (profile_id,),
        ).fetchone()
    if row is None or row["first_started_at"] is None:
        return False
    first_started_at = datetime.fromisoformat(str(row["first_started_at"]))
    if first_started_at.tzinfo is None:
        first_started_at = first_started_at.replace(tzinfo=timezone.utc)
    if growth_timestamp.tzinfo is None:
        growth_timestamp = growth_timestamp.replace(tzinfo=timezone.utc)
    return growth_timestamp < first_started_at


def _build_growth_turn_signals(
    *,
    current: ProfileGrowthState | None,
    outcome: KernelOutcome,
    experience: ExperienceRecord | None,
    procedure_library: ProcedureLibrary | None,
) -> GrowthTurnSignals:
    goal = _growth_goal_from_outcome(outcome)
    promoted_delta, promoted_ids = _promoted_procedure_delta(current, procedure_library)
    return GrowthTurnSignals(
        session_id=outcome.session.session_id,
        profile_id=outcome.session.profile_id,
        total_tokens=outcome.execution.total_tokens,
        captured_experiences=1 if experience is not None else 0,
        promoted_experiences=promoted_delta,
        continuity_bonus=outcome.continuity.requires_recovery,
        occurred_at=outcome.session.updated_at,
        goal_id=goal.goal_id if goal is not None else outcome.goal_graph.active_goal_id,
        goal_status=goal.status if goal is not None else _optional_str(outcome.decision.rationale.selected_goal_status) if outcome.decision is not None else None,
        goal_priority=goal.priority if goal is not None else _optional_str(outcome.decision.rationale.selected_goal_priority) if outcome.decision is not None else None,
        progression_action=outcome.decision.rationale.progression_action if outcome.decision is not None else "",
        resume_signal=outcome.intent.resume_signal,
        continuity_mode=outcome.continuity.mode,
        execution_outcome=outcome.execution.outcome,
        experience_status=experience.status if experience is not None else None,
        active_goal_present=outcome.goal_graph.active_goal_id is not None,
        plan_step_count=len(outcome.plan.steps) if outcome.plan is not None else 0,
        goal_dependency_count=len(goal.dependencies) if goal is not None else 0,
        memory_count=len(outcome.memories),
        context_goal_count=len(outcome.context.goal_ids),
        tool_call_count=(
            outcome.run.tool_call_count
            if outcome.run is not None
            else len(outcome.execution.tool_calls)
        ),
        model_turn_count=outcome.run.model_turn_count if outcome.run is not None else 0,
        blocked_goal_count=outcome.goal_graph.status_counts().get("blocked", 0),
        goal_evidence_refs=goal.evidence_refs if goal is not None else (),
        replay_evidence_refs=(
            outcome.decision.rationale.replay_evidence_refs if outcome.decision is not None else ()
        ),
        skill_ids=experience.related_skill_ids if experience is not None else (),
        artifact_ids=outcome.execution.produced_artifact_ids,
        promoted_procedure_ids=promoted_ids,
        elapsed_since_last_turn_seconds=_growth_elapsed_seconds(current, occurred_at=outcome.session.updated_at),
    )


def _growth_goal_from_outcome(outcome: KernelOutcome) -> GoalNode | None:
    if outcome.decision is not None and outcome.decision.rationale.selected_goal_id is not None:
        goal = outcome.goal_graph.goal(outcome.decision.rationale.selected_goal_id)
        if goal is not None:
            return goal
    if outcome.plan is not None and outcome.plan.goal_id:
        goal = outcome.goal_graph.goal(outcome.plan.goal_id)
        if goal is not None:
            return goal
    return outcome.goal_graph.active_goal()


def _promoted_procedure_delta(
    current: ProfileGrowthState | None,
    procedure_library: ProcedureLibrary | None,
) -> tuple[int, tuple[str, ...]]:
    if procedure_library is None:
        return 0, ()
    promoted = tuple(
        procedure.procedure_id
        for procedure in procedure_library.procedures
        if procedure.status in {"active", "promoted", "verified"}
    )
    already_recorded = current.promoted_experiences if current is not None else 0
    delta = max(0, len(promoted) - already_recorded)
    if delta == 0:
        return 0, ()
    return delta, promoted[-delta:]


def _growth_elapsed_seconds(
    current: ProfileGrowthState | None,
    *,
    occurred_at: datetime,
) -> int | None:
    if current is None or current.last_dialogue_at is None:
        return None
    elapsed = occurred_at - current.last_dialogue_at
    return max(0, int(elapsed.total_seconds()))


def write_snapshot(
    runtime: CliRuntime,
    *,
    profile: ProfileState,
    session: SessionState,
    goals: tuple[GoalNode, ...],
    memories: tuple[MemoryRecord, ...],
    plan: PlanDraft | None,
    execution: ExecutionResult | None,
    delivery: ExecutionResult | None,
    stages: tuple[Any, ...],
    event: EventEnvelope | None,
    clone_text: str | None,
    intent: IntentDecision | None,
    context: ContextBundle | None = None,
) -> None:
    existing = load_snapshot(runtime) or {}
    session_context_epoch = _next_session_context_epoch(
        runtime,
        restore_snapshot_session_context_epoch(existing),
        profile=profile,
        session=session,
        goals=goals,
        event=event,
        execution=execution,
        delivery=delivery,
        intent=intent,
        context=context,
    )
    payload = {
        "profile": _profile_payload(profile, clone_text=clone_text),
        "session": _session_payload(session),
        "goals": [_goal_payload(goal) for goal in goals],
        "memories": [_memory_payload(memory) for memory in memories],
        "plan": _plan_payload(plan),
        "execution": _execution_payload(execution),
        "delivery": _execution_payload(delivery),
        "stages": [_stage_payload(stage) for stage in stages],
        "event": _event_payload(event),
        "intent": _intent_payload(intent),
        "session_context_epoch": _session_context_epoch_payload(session_context_epoch),
        "telemetry": existing.get("telemetry", ()),
    }
    write_snapshot_payload(runtime.snapshot_path, payload)


def _next_session_context_epoch(
    runtime: CliRuntime,
    existing: SessionContextEpoch | None,
    *,
    profile: ProfileState,
    session: SessionState,
    goals: tuple[GoalNode, ...],
    event: EventEnvelope | None,
    execution: ExecutionResult | None,
    delivery: ExecutionResult | None,
    intent: IntentDecision | None,
    context: ContextBundle | None,
) -> SessionContextEpoch:
    epoch = existing if existing is not None and existing.session_id == session.session_id else SessionContextEpoch(
        session_id=session.session_id
    )
    disclosures = _skill_disclosure_records(runtime, intent=intent, context=context)
    frozen_skill_index = _frozen_session_skill_index(runtime, profile=profile, session=session)
    if (
        not epoch.frozen
        and context is not None
        and event is not None
        and _snapshot_event_is_user_turn(event.event_type, event.source)
        and execution is not None
    ):
        envelope = context.prompt_envelope
        epoch = replace(
            epoch,
            frozen=True,
            frozen_prefix=envelope.frozen_prefix,
            session_snapshot=envelope.session_snapshot,
            base_turn_injections=_base_turn_injection_refs(envelope.turn_injections),
            tool_schema="",
            thread_focus=_derive_session_epoch_focus(runtime, session=session, goals=goals),
            frozen_skill_count=len(frozen_skill_index),
            frozen_tool_count=_frozen_session_tool_count(runtime),
            frozen_skill_index=frozen_skill_index,
            frozen_skill_ids=tuple(entry.skill_id for entry in frozen_skill_index),
            frozen_tool_ids=_frozen_session_tool_ids(runtime),
            frozen_skill_disclosures=disclosures,
            latest_skill_disclosures=disclosures,
            frozen_at=_utc_now(),
        )
    elif event is not None and _snapshot_event_is_user_turn(event.event_type, event.source):
        epoch = replace(epoch, latest_skill_disclosures=disclosures)
    history_lines = _session_history_lines(event=event, execution=execution, delivery=delivery)
    if history_lines:
        epoch = replace(epoch, history_lines=epoch.history_lines + history_lines)
    return epoch


def _snapshot_event_is_user_turn(event_type: str | None, source: str | None) -> bool:
    if str(source or "").strip() == "cli.startup":
        return False
    normalized_event_type = str(event_type or "").strip().lower()
    if not normalized_event_type:
        return True
    return normalized_event_type == "turn.received"


def _base_turn_injection_refs(value: Any) -> str:
    lines = [line.strip() for line in str(value or "").splitlines() if line.strip()]
    ref_prefixes = (
        "ref:",
        "- ref:",
        "refs:",
        "- refs:",
        "source_ref:",
        "- source_ref:",
        "source_refs:",
        "- source_refs:",
    )
    return "\n".join(line for line in lines if line.lower().startswith(ref_prefixes))


def _session_history_lines(
    *,
    event: EventEnvelope | None,
    execution: ExecutionResult | None,
    delivery: ExecutionResult | None,
) -> tuple[str, ...]:
    if event is None or execution is None or not _snapshot_event_is_user_turn(event.event_type, event.source):
        return ()
    lines: list[str] = []
    message = (
        str(event.payload.get("message") or event.payload.get("content") or event.payload.get("summary") or "").strip()
        if isinstance(event.payload, Mapping)
        else ""
    )
    if message:
        lines.append(f"user: {message}")
    summary = execution.summary.strip()
    if summary:
        lines.append(f"aegis: {summary}")
    if delivery is not None and delivery.summary.strip():
        lines.append(f"delivery: {delivery.summary.strip()}")
    return tuple(lines)


def _derive_session_epoch_focus(
    runtime: CliRuntime,
    *,
    session: SessionState,
    goals: tuple[GoalNode, ...],
) -> str:
    active_goal = next((goal for goal in goals if goal.status == "active" and goal.title.strip()), None)
    if active_goal is None:
        active_goal = next((goal for goal in goals if goal.title.strip()), None)
    if active_goal is not None:
        return active_goal.title.strip()
    continuity = runtime.inspect_continuity(session_id=session.session_id)
    for candidate in (
        continuity.wake_action,
        continuity.wake_summary,
        continuity.continuity_summary,
    ):
        normalized = str(candidate or "").strip()
        if normalized and not _focus_summary_is_planner_fallback(normalized):
            return normalized
    return "No durable session focus was available when this session froze."


def _focus_summary_is_planner_fallback(text: str) -> bool:
    normalized = text.strip().lower()
    return "no actionable goals were available" in normalized or "planner should defer" in normalized


def _frozen_session_skill_count(
    runtime: CliRuntime,
    *,
    profile: ProfileState,
    session: SessionState,
) -> int:
    return len(_frozen_session_skill_index(runtime, profile=profile, session=session))


def _frozen_session_skill_index(
    runtime: CliRuntime,
    *,
    profile: ProfileState,
    session: SessionState,
) -> tuple[FrozenSkillIndexEntry, ...]:
    del session
    skill_overrides = _runtime_skill_prompt_index_overrides(runtime, profile=profile)
    return tuple(
        FrozenSkillIndexEntry(
            skill_id=entry.skill_id,
            display_name=entry.display_name,
            category=str(entry.metadata.get("category") or "").strip(),
            source_id=entry.source_id,
            storage_tier=entry.storage_tier,
            slash_command=str(entry.metadata.get("slash_command") or "").strip(),
        )
        for entry in builtin_prompt_skill_catalog_entries(skill_overrides, limit=10_000)
    )


def _runtime_skill_prompt_index_overrides(runtime: CliRuntime, *, profile: ProfileState) -> dict[str, bool]:
    try:
        loaded = runtime._load_profile(profile.profile_id)
    except Exception:
        return {}
    raw = loaded.manifest.get("skill_overrides", {})
    if not isinstance(raw, Mapping):
        return {}
    overrides: dict[str, bool] = {}
    for skill_id, record in raw.items():
        if isinstance(record, Mapping) and "enabled" in record:
            overrides[str(skill_id)] = bool(record["enabled"])
    return overrides


def _frozen_session_skill_ids(
    runtime: CliRuntime,
    *,
    profile: ProfileState,
    session: SessionState,
) -> tuple[str, ...]:
    return tuple(
        entry.skill_id
        for entry in _frozen_session_skill_index(runtime, profile=profile, session=session)
    )


def _frozen_session_tool_count(runtime: CliRuntime) -> int:
    return len(_frozen_session_tool_ids(runtime))


def _frozen_session_tool_ids(runtime: CliRuntime) -> tuple[str, ...]:
    if runtime.tool_runtime is None:
        return ()
    return tuple(
        tool.tool_id
        for tool in runtime.tool_runtime.list_tools(
            audience="model",
            enabled_only=True,
            available_only=True,
        )
    )


def _skill_disclosure_records(
    runtime: CliRuntime,
    *,
    intent: IntentDecision | None,
    context: ContextBundle | None,
) -> tuple[SkillDisclosureRecord, ...]:
    if intent is None or context is None or runtime.skill_runtime is None:
        return ()
    disclosed_skill_ids = tuple(
        artifact_id.split(":", 1)[1]
        for artifact_id in context.artifact_ids
        if artifact_id.startswith("skill:") and ":" in artifact_id
    )
    if not disclosed_skill_ids:
        return ()
    candidate_scores = {
        score.candidate_id: score
        for score in intent.candidate_scores
        if score.kind == "skill"
    }
    records: list[SkillDisclosureRecord] = []
    for skill_id in dict.fromkeys(disclosed_skill_ids):
        definition = runtime.skill_runtime.describe(skill_id)
        score = candidate_scores.get(skill_id)
        display_name = (
            definition.display_name.strip()
            if definition is not None and definition.display_name.strip()
            else str(score.label).strip()
            if score is not None
            else skill_id
        )
        records.append(
            SkillDisclosureRecord(
                skill_id=skill_id,
                display_name=display_name,
                reason=_skill_disclosure_reason(skill_id=skill_id, display_name=display_name, score=score),
            )
        )
    return tuple(records)


def _skill_disclosure_reason(*, skill_id: str, display_name: str, score: IntentCandidateScore | None) -> str:
    if score is None:
        return (
            f"{display_name} ({skill_id}) was disclosed because the runtime recorded an explicit skill overlay "
            "without a recoverable intent score."
        )
    reason_fragments = [reason.detail for reason in score.reasons[:2] if reason.detail.strip()]
    rationale = "; ".join(reason_fragments) or "the intent resolver ranked this as the best skill candidate for the turn"
    return (
        f"{display_name} ({skill_id}) was disclosed from the intent-selected skill lane "
        f"with total_score={score.total_score:.2f}; {rationale}"
    )


def _profile_payload(profile: ProfileState, *, clone_text: str | None) -> dict[str, Any]:
    return {
        "profile_id": profile.profile_id,
        "display_name": profile.display_name,
        "mode": profile.mode,
        "clone_path": profile.clone_path,
        "preferences": list(profile.preferences),
        "enabled_capabilities": list(profile.enabled_capabilities),
        "clone_text": clone_text,
    }


def _session_payload(session: SessionState) -> dict[str, Any]:
    return {
        "session_id": session.session_id,
        "profile_id": session.profile_id,
        "workspace_id": session.workspace_id,
        "status": session.status,
        "started_at": _iso(session.started_at),
        "updated_at": _iso(session.updated_at),
        "parent_session_id": session.parent_session_id,
        "interruption_state": session.interruption_state,
    }


def _goal_payload(goal: GoalNode) -> dict[str, Any]:
    return {
        "goal_id": goal.goal_id,
        "session_id": goal.session_id,
        "title": goal.title,
        "status": goal.status,
        "priority": goal.priority,
        "dependencies": list(goal.dependencies),
        "evidence_refs": list(goal.evidence_refs),
        "owner": goal.owner,
        "parent_goal_id": goal.parent_goal_id,
        "related_memory_ids": list(goal.related_memory_ids),
        "deadline": _iso(goal.deadline) if goal.deadline is not None else None,
        "time_sensitivity": goal.time_sensitivity,
        "review_checkpoint": goal.review_checkpoint,
        "revision_id": goal.revision_id,
        "updated_at": _iso(goal.updated_at) if goal.updated_at is not None else None,
    }


def _memory_payload(memory: MemoryRecord) -> dict[str, Any]:
    return {
        "memory_id": memory.memory_id,
        "session_id": memory.session_id,
        "kind": memory.kind,
        "content": memory.content,
        "source_event_id": memory.source_event_id,
        "goal_refs": list(memory.goal_refs),
        "tags": list(memory.tags),
        "created_at": _iso(memory.created_at) if memory.created_at is not None else None,
    }


def _plan_payload(plan: PlanDraft | None) -> dict[str, Any] | None:
    if plan is None:
        return None
    return {
        "plan_id": plan.plan_id,
        "goal_id": plan.goal_id,
        "session_id": plan.session_id,
        "steps": [
            {
                "step_id": step.step_id,
                "title": step.title,
                "rationale": step.rationale,
                "dependency_refs": list(step.dependency_refs),
            }
            for step in plan.steps
        ],
        "rationale": plan.rationale,
    }


def _execution_payload(execution: ExecutionResult | None) -> dict[str, Any] | None:
    if execution is None:
        return None
    return {
        "execution_id": execution.execution_id,
        "session_id": execution.session_id,
        "outcome": execution.outcome,
        "summary": execution.summary,
        "prompt_tokens": execution.prompt_tokens,
        "completion_tokens": execution.completion_tokens,
        "total_tokens": execution.total_tokens,
        "produced_artifact_ids": list(execution.produced_artifact_ids),
        "telemetry_event_ids": list(execution.telemetry_event_ids),
        "side_effects": list(execution.side_effects),
    }


def _intent_payload(intent: IntentDecision | None) -> dict[str, Any] | None:
    if intent is None:
        return None
    return {
        "intent": intent.intent,
        "confidence": intent.confidence,
        "focus_activity_ids": list(intent.focus_activity_ids),
        "provisional_activity_seed": intent.provisional_activity_seed,
        "resume_signal": intent.resume_signal,
        "scope_suggestion": intent.scope_suggestion,
        "budget_class": intent.budget_class,
        "embedding_available": intent.embedding_available,
        "degradation_mode": intent.degradation_mode,
        "needs_weak_model_assist": intent.needs_weak_model_assist,
        "weak_assist_outcome": intent.weak_assist_outcome,
        "fallback_path": intent.fallback_path,
        "reasons": [_intent_reason_payload(reason) for reason in intent.reasons],
        "candidate_scores": [_intent_candidate_score_payload(score) for score in intent.candidate_scores],
        "audit_trace": list(intent.audit_trace),
    }


def _session_context_epoch_payload(epoch: SessionContextEpoch) -> dict[str, Any]:
    return {
        "session_id": epoch.session_id,
        "frozen": epoch.frozen,
        "frozen_prefix": epoch.frozen_prefix,
        "session_snapshot": epoch.session_snapshot,
        "base_turn_injections": epoch.base_turn_injections,
        "tool_schema": epoch.tool_schema,
        "thread_focus": epoch.thread_focus,
        "frozen_skill_count": epoch.frozen_skill_count,
        "frozen_tool_count": epoch.frozen_tool_count,
        "frozen_skill_index": [_frozen_skill_index_payload(entry) for entry in epoch.frozen_skill_index],
        "frozen_skill_ids": list(epoch.frozen_skill_ids),
        "frozen_tool_ids": list(epoch.frozen_tool_ids),
        "frozen_skill_disclosures": [_skill_disclosure_payload(record) for record in epoch.frozen_skill_disclosures],
        "latest_skill_disclosures": [_skill_disclosure_payload(record) for record in epoch.latest_skill_disclosures],
        "compacted_history_summary": epoch.compacted_history_summary,
        "compaction_count": epoch.compaction_count,
        "compacted_history_count": epoch.compacted_history_count,
        "context_projection_tokens": epoch.context_projection_tokens,
        "context_projection_limit": epoch.context_projection_limit,
        "history_lines": list(epoch.history_lines),
        "frozen_at": _iso(epoch.frozen_at) if epoch.frozen_at is not None else None,
    }


def _intent_reason_payload(reason: IntentReason) -> dict[str, Any]:
    return {
        "code": reason.code,
        "detail": reason.detail,
        "weight": reason.weight,
    }


def _intent_candidate_score_payload(score: IntentCandidateScore) -> dict[str, Any]:
    return {
        "candidate_id": score.candidate_id,
        "kind": score.kind,
        "label": score.label,
        "total_score": score.total_score,
        "heuristics_score": score.heuristics_score,
        "embedding_score": score.embedding_score,
        "reasons": [_intent_reason_payload(reason) for reason in score.reasons],
        "metadata": dict(score.metadata),
    }


def _stage_payload(stage: Any) -> Any:
    return {
        "stage": stage.stage,
        "detail": stage.detail,
        "recorded_at": _iso(stage.recorded_at),
    }


def _restore_intent_reason(payload: Mapping[str, Any]) -> IntentReason:
    return IntentReason(
        code=str(payload.get("code") or "").strip(),
        detail=str(payload.get("detail") or "").strip(),
        weight=float(payload.get("weight") or 0.0),
    )


def _restore_intent_candidate_score(payload: Mapping[str, Any]) -> IntentCandidateScore:
    return IntentCandidateScore(
        candidate_id=str(payload.get("candidate_id") or "").strip(),
        kind=str(payload.get("kind") or "").strip(),
        label=str(payload.get("label") or "").strip(),
        total_score=float(payload.get("total_score") or 0.0),
        heuristics_score=float(payload.get("heuristics_score") or 0.0),
        embedding_score=float(payload.get("embedding_score") or 0.0),
        reasons=tuple(
            _restore_intent_reason(reason)
            for reason in payload.get("reasons", ())
            if isinstance(reason, Mapping)
        ),
        metadata={
            str(key): str(value)
            for key, value in dict(payload.get("metadata") or {}).items()
        },
    )


def _skill_disclosure_payload(record: SkillDisclosureRecord) -> dict[str, Any]:
    return {
        "skill_id": record.skill_id,
        "display_name": record.display_name,
        "reason": record.reason,
        "source": record.source,
    }


def _frozen_skill_index_payload(entry: FrozenSkillIndexEntry) -> dict[str, Any]:
    return {
        "skill_id": entry.skill_id,
        "display_name": entry.display_name,
        "category": entry.category,
        "source_id": entry.source_id,
        "storage_tier": entry.storage_tier,
        "slash_command": entry.slash_command,
    }


def _frozen_skill_index_tuple(payload: object) -> tuple[FrozenSkillIndexEntry, ...]:
    if not isinstance(payload, (list, tuple)):
        return ()
    return tuple(
        FrozenSkillIndexEntry(
            skill_id=str(item.get("skill_id") or "").strip(),
            display_name=str(item.get("display_name") or "").strip(),
            category=str(item.get("category") or "").strip(),
            source_id=str(item.get("source_id") or "").strip(),
            storage_tier=str(item.get("storage_tier") or "").strip(),
            slash_command=str(item.get("slash_command") or "").strip(),
        )
        for item in payload
        if isinstance(item, Mapping) and str(item.get("skill_id") or "").strip()
    )


def _skill_disclosure_tuple(payload: object) -> tuple[SkillDisclosureRecord, ...]:
    if not isinstance(payload, (list, tuple)):
        return ()
    return tuple(
        SkillDisclosureRecord(
            skill_id=str(item.get("skill_id") or "").strip(),
            display_name=str(item.get("display_name") or "").strip(),
            reason=str(item.get("reason") or "").strip(),
            source=str(item.get("source") or "intent-selection").strip() or "intent-selection",
        )
        for item in payload
        if isinstance(item, Mapping) and str(item.get("skill_id") or "").strip()
    )


def _as_str_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,) if value else ()
    return tuple(str(item) for item in value if str(item))


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _optional_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return datetime.fromisoformat(text)


def _event_payload(event: EventEnvelope | None) -> dict[str, Any] | None:
    if event is None:
        return None
    return {
        "event_id": event.event_id,
        "event_type": event.event_type,
        "session_id": event.session_id,
        "source": event.source,
        "payload": dict(event.payload),
    }


def _iso(value: datetime) -> str:
    return value.isoformat()


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)
