from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from packages.contracts.runtime import EventEnvelope, ProfileState, SessionState, ActivityGraph
from packages.kernel import (
    KernelDependencies,
    KernelOutcome,
    KernelService,
    KernelTurnRequest,
    ObservationPipeline,
    StateReconciler,
    TurnProfileDelta,
    merge_preference_updates,
)
from packages.planning.runtime import PlanningService, build_plan_draft_from_decision, goal_graph_to_activity_graph, activity_graph_to_goal_graph
from packages.state import (
    CompanionSettings,
    LoadedProfile,
    apply_user_card_update,
    is_companion_mode,
    profile_bundle_dir,
    render_user_card_profile_text,
)

if TYPE_CHECKING:
    from apps.cli.runtime import CliRuntime


@dataclass(frozen=True, slots=True)
class _RequesterScopedToolCapability:
    tool_runtime: Any
    requester: str
    descriptor: Any

    def invoke(
        self,
        tool_name: str,
        arguments: Mapping[str, Any],
        *,
        session_id: str,
    ) -> ExecutionResult:
        return self.tool_runtime.invoke(
            tool_name,
            arguments,
            session_id=session_id,
            requester=self.requester,
        )


def start_session(
    runtime: CliRuntime,
    *,
    profile_id: str | None = None,
    display_name: str | None = None,
    mode: str | None = None,
    session_id: str | None = None,
    initial_goal: str | None = None,
) -> SessionState:
    loaded = runtime.profile_loader.load(
        profile_id=profile_id,
        display_name=display_name,
        mode=mode,
    )
    profile_state = replace(loaded.state, preferences=loaded.state.preferences)
    session = runtime.session_service.start_session(
        profile_state,
        session_id=session_id,
    )
    current_profile = runtime._load_profile(profile_state.profile_id)
    if initial_goal:
        runtime.seed_initial_goal(session.session_id, initial_goal)
    runtime._write_snapshot(
        profile=profile_state,
        session=session,
        goals=runtime.inspect_goals(session.session_id),
        memories=(),
        plan=None,
        execution=None,
        delivery=None,
        stages=(),
        event=None,
        clone_text=current_profile.clone_text,
        intent=None,
    )
    return session


def create_clone_session(
    runtime: CliRuntime,
    *,
    clone_id: str,
    profile_id: str | None = None,
    display_name: str | None = None,
    mode: str | None = None,
    session_id: str | None = None,
    initial_goal: str | None = None,
    seed_clone_text,
) -> SessionState:
    resolved_clone_id = clone_id.strip()
    if not resolved_clone_id:
        raise ValueError("clone name is required")
    if runtime.latest_session_for_clone(resolved_clone_id) is not None:
        raise ValueError(f"clone already exists: {resolved_clone_id}")
    runtime.paths.workspace_path_for_clone(resolved_clone_id).mkdir(parents=True, exist_ok=True)
    source_profile = runtime._load_profile(profile_id or runtime.current_profile().state.profile_id)
    clone_profile_id = f"clone:{resolved_clone_id}"
    runtime.repository.delete_orphaned_profiles((clone_profile_id,))
    if display_name is None:
        clone_display_name = resolved_clone_id.replace("-", " ").title()
    else:
        clone_display_name = display_name.strip()
    clone_mode = mode or source_profile.state.mode
    clone_companion = source_profile.companion if is_companion_mode(clone_mode) else None
    clone_text = seed_clone_text(
        source_profile,
        display_name=clone_display_name,
        mode=clone_mode,
        companion=clone_companion,
    )
    cloned_profile = runtime._persist_profile(
        LoadedProfile(
            state=replace(
                source_profile.state,
                profile_id=clone_profile_id,
                display_name=clone_display_name,
                mode=clone_mode,
                clone_path=None,
            ),
            companion=clone_companion,
            profile_dir=str(profile_bundle_dir(runtime.paths.profile_dir, clone_profile_id)),
            manifest_path=None,
            clone_text=clone_text,
            user_profile_text=None,
            manifest=dict(source_profile.manifest),
        ),
        sync_source="clone.create",
    )
    profile_state = replace(cloned_profile.state, preferences=cloned_profile.state.preferences)
    session = runtime.session_service.start_session(
        profile_state,
        workspace_id=resolved_clone_id,
        session_id=session_id,
    )
    if initial_goal:
        runtime.seed_initial_goal(session.session_id, initial_goal)
    runtime._write_snapshot(
        profile=profile_state,
        session=session,
        goals=runtime.inspect_goals(session.session_id),
        memories=(),
        plan=None,
        execution=None,
        delivery=None,
        stages=(),
        event=None,
        clone_text=cloned_profile.clone_text,
        intent=None,
    )
    return session


def resume_session(
    runtime: CliRuntime,
    session_id: str,
    *,
    resumed_session_id: str | None = None,
):
    result = runtime.session_service.resume_session(
        session_id,
        child_session_id=resumed_session_id,
    )
    session = result.session
    profile = runtime._load_profile(session.profile_id)
    parent_graph = runtime.repository.load_activity_graph(session_id)
    if parent_graph is not None:
        runtime.repository.upsert_activity_graph(
            replace(
                parent_graph,
                session_id=session.session_id,
                goals=tuple(replace(goal, session_id=session.session_id) for goal in parent_graph.goals),
            )
        )
    runtime._write_snapshot(
        profile=profile.state,
        session=session,
        goals=runtime.inspect_goals(session.session_id),
        memories=(),
        plan=None,
        execution=None,
        delivery=None,
        stages=(),
        event=None,
        clone_text=profile.clone_text,
        intent=None,
    )
    if session is result.session:
        return result
    return result.__class__(session=session, lineage=result.lineage)


def explain_next_step(
    runtime: CliRuntime,
    *,
    session_id: str,
    prompt: str,
    goal_query: str | None = None,
    tool_name: str | None = None,
    tool_arguments: Mapping[str, Any] | None = None,
    delivery_payload: Mapping[str, Any] | None = None,
    event_payload: Mapping[str, str] | None = None,
) -> KernelOutcome:
    return runtime._run_turn(
        session_id=session_id,
        prompt=prompt,
        goal_query=goal_query,
        tool_name=tool_name,
        tool_arguments=tool_arguments,
        delivery_payload=delivery_payload,
        event_payload=event_payload,
    )


def generate_opening_reply(
    runtime: CliRuntime,
    *,
    session_id: str,
    prompt: str,
    opening_label: str,
) -> KernelOutcome | None:
    if runtime.model_provider.active_profile() is None:
        return None
    return runtime._run_turn(
        session_id=session_id,
        prompt=prompt,
        event_type="turn.internal",
        source="cli.startup",
        event_payload={
            "message": f"startup opening ({opening_label})",
            "summary": f"startup opening ({opening_label})",
            "content": "",
            "allow_embeddings": "false",
            "intent_mode_override": "skip",
        },
        record_input_event=False,
        record_outcome_memory=False,
        capture_experience=False,
        apply_growth=False,
    )


def run_turn(
    runtime: CliRuntime,
    *,
    session_id: str,
    prompt: str,
    goal_query: str | None = None,
    tool_name: str | None = None,
    tool_arguments: Mapping[str, Any] | None = None,
    delivery_payload: Mapping[str, Any] | None = None,
    event_type: str = "turn.received",
    source: str = "cli",
    event_payload: Mapping[str, str] | None = None,
    record_input_event: bool = True,
    record_outcome_memory: bool = True,
    capture_experience: bool = True,
    apply_growth: bool = True,
) -> KernelOutcome:
    session = runtime._load_session(session_id)
    loaded_profile = runtime._load_profile(session.profile_id)
    profile = loaded_profile.state
    previous_goal_graph = runtime.repository.load_activity_graph(session.session_id) or ActivityGraph(session_id=session.session_id)
    dependencies = runtime._build_kernel_dependencies(session, profile)
    service = KernelService(dependencies=dependencies)
    payload = {
        "message": prompt,
        "content": prompt,
        "summary": prompt,
        "goal_query": goal_query or "",
        "tool_name": tool_name or "",
    }
    if event_payload is not None:
        payload.update(dict(event_payload))
    event = EventEnvelope(
        event_id=f"event:{uuid4().hex}",
        event_type=event_type,
        session_id=session.session_id,
        source=source,
        payload=payload,
    )
    outcome = service.run(
        KernelTurnRequest(
            event=event,
            prompt=prompt,
            goal_query=goal_query,
            tool_name=tool_name,
            tool_arguments=dict(tool_arguments or {}),
            delivery_payload=dict(delivery_payload or {}),
        )
    )
    performed_turn_reconciliation = record_input_event or record_outcome_memory
    persisted_profile = runtime._load_profile(outcome.profile.profile_id)
    if performed_turn_reconciliation:
        turn_observation = ObservationPipeline().observe_turn(
            inbound_event=event,
            execution=outcome.execution,
            previous_goal_graph=previous_goal_graph,
            reconciled_goal_graph=outcome.goal_graph,
            selected_goal_id=_selected_goal_id_from_outcome(outcome),
            decision_summary=_decision_summary_from_outcome(outcome),
            include_input_event=record_input_event,
            include_outcome_event=record_outcome_memory,
            source=source,
            profile_id=outcome.profile.profile_id,
            workspace_id=outcome.session.workspace_id,
        )
        StateReconciler().reconcile_turn(
            repository=runtime.repository,
            memory_runtime=runtime.memory_runtime,
            observation=turn_observation,
        )
        persisted_profile = _apply_turn_profile_delta(
            runtime,
            session_id=outcome.session.session_id,
            profile_delta=turn_observation.profile_delta,
        )
    experience = runtime._append_outcome_experience(outcome) if capture_experience else None
    if apply_growth:
        runtime._append_outcome_growth(outcome, experience=experience)
    snapshot_goals = runtime.inspect_goals(outcome.session.session_id) if performed_turn_reconciliation else outcome.goals
    snapshot_memories = (
        runtime.inspect_memories(outcome.session.session_id)
        if performed_turn_reconciliation
        else outcome.memories
    )
    runtime._write_snapshot(
        profile=persisted_profile.state,
        session=outcome.session,
        goals=snapshot_goals,
        memories=snapshot_memories,
        plan=outcome.plan,
        execution=outcome.execution,
        delivery=outcome.delivery,
        stages=outcome.stages,
        event=outcome.event,
        clone_text=persisted_profile.clone_text,
        intent=outcome.intent,
        context=outcome.context,
    )
    return outcome


def wake(runtime: CliRuntime, session_id: str, *, inspect_only: bool = False, result_cls):
    session = runtime._load_session(session_id)
    goal_graph = runtime.repository.load_activity_graph(session_id)
    if goal_graph is None:
        raise KeyError(session_id)
    profile = runtime._load_profile(session.profile_id)
    identity = runtime.inspect_identity(profile_id=session.profile_id)
    relationship = runtime.inspect_relationship(profile_id=session.profile_id)
    recovery = runtime._planning_memory_recovery(session, goal_graph)
    service = PlanningService()
    decision, planned_goal_graph = service.wake_next_step(
        session=session,
        graph=activity_graph_to_goal_graph(goal_graph),
        memories=recovery.memories,
        initiative_hint=identity.initiative,
        continuity_notes=relationship.continuity_notes,
    )
    planned_goal_graph = goal_graph_to_activity_graph(planned_goal_graph)
    plan = build_plan_draft_from_decision(decision)
    rationale_event = _wake_rationale_event(
        session_id=session.session_id,
        decision=decision,
        recovery=recovery,
    )
    planning_rationale_event = service.emit_rationale(decision)
    wake_observation = ObservationPipeline().observe_wake(
        session_id=session.session_id,
        previous_goal_graph=goal_graph,
        planned_goal_graph=planned_goal_graph,
        durable_events=(rationale_event, planning_rationale_event),
        selected_goal_id=decision.selected_move.goal_id,
        decision_summary=decision.rationale.summary,
    )
    reconciliation = StateReconciler().reconcile_wake(
        repository=runtime.repository,
        memory_runtime=runtime.memory_runtime,
        observation=wake_observation,
        inspect_only=inspect_only,
    )
    if not inspect_only:
        runtime._write_snapshot(
            profile=profile.state,
            session=session,
            goals=planned_goal_graph.goals,
            memories=recovery.memories,
            plan=plan,
            execution=None,
            delivery=None,
            stages=(),
            event=rationale_event,
            clone_text=profile.clone_text,
            intent=None,
        )
    return result_cls(
        profile=profile.state,
        session=session,
        decision=decision,
        planned_goal_graph=planned_goal_graph,
        applied=not inspect_only,
        plan=plan,
        reconciliation=reconciliation,
        retrieval=recovery.retrieval,
        resume_packet=recovery.resume_packet,
    )


def _wake_rationale_event(
    *,
    session_id: str,
    decision,
    recovery,
) -> EventEnvelope:
    selected_goal_id = decision.selected_move.goal_id or ""
    scope_summary = ", ".join(recovery.scope_session_ids) or session_id
    content = (
        f"Wake recovery searched scope {scope_summary}. "
        f"Reason: {recovery.scope_reason}. "
        f"Next step: {decision.rationale.summary}"
    )
    return EventEnvelope(
        event_id=f"event:{uuid4().hex}",
        event_type="wake.recovery.rationale",
        session_id=session_id,
        source="cli.wake",
        payload={
            "content": content,
            "summary": f"wake recovery scope selected for {selected_goal_id or 'no-goal'}",
            "memory_kind": "semantic",
            "goal_ids": ",".join(recovery.goal_ids or ((selected_goal_id,) if selected_goal_id else ())),
            "tags": "continuity,recovery,wake,scope-aware,resume-packet",
            "scope_session_ids": ",".join(recovery.scope_session_ids),
            "scope_reason": recovery.scope_reason,
            "query": recovery.query,
            "selected_goal_id": selected_goal_id,
            "planned_active_goal_id": decision.rationale.planned_active_goal_id or "",
            "progression_action": decision.rationale.progression_action,
            "resume_packet_summary": recovery.resume_packet.summary if getattr(recovery, "resume_packet", None) is not None else "",
            "resume_packet_evidence_ids": ",".join(
                recovery.resume_packet.evidence_ids if getattr(recovery, "resume_packet", None) is not None else ()
            ),
        },
    )


def _selected_goal_id_from_outcome(outcome: KernelOutcome) -> str | None:
    if outcome.decision is not None and outcome.decision.selected_move.goal_id:
        return outcome.decision.selected_move.goal_id
    if outcome.plan is not None and outcome.plan.goal_id:
        return outcome.plan.goal_id
    return outcome.goal_graph.active_goal_id


def _decision_summary_from_outcome(outcome: KernelOutcome) -> str:
    if outcome.decision is not None and outcome.decision.rationale.summary.strip():
        return outcome.decision.rationale.summary.strip()
    if outcome.plan is not None and outcome.plan.rationale.strip():
        return outcome.plan.rationale.strip()
    return outcome.execution.summary.strip()


def _apply_turn_profile_delta(
    runtime: CliRuntime,
    *,
    session_id: str,
    profile_delta: TurnProfileDelta,
) -> LoadedProfile:
    session = runtime._load_session(session_id)
    loaded = runtime._load_profile(session.profile_id)
    if not profile_delta.observed:
        return loaded
    next_loaded = loaded
    user_fields = {key: value for key, value in profile_delta.user_fields}
    if user_fields:
        current_user = runtime.inspect_user(profile_id=session.profile_id)
        next_user = apply_user_card_update(
            current_user,
            field_values=user_fields,
            append=True,
        )
        next_loaded = replace(
            next_loaded,
            user_profile_text=render_user_card_profile_text(next_user),
        )
    if profile_delta.preference_updates:
        next_loaded = replace(
            next_loaded,
            state=replace(
                next_loaded.state,
                preferences=merge_preference_updates(
                    next_loaded.state.preferences,
                    profile_delta.preference_updates,
                ),
            ),
        )
    if profile_delta.relationship_notes:
        companion = next_loaded.companion or CompanionSettings()
        current_notes = tuple(note.strip() for note in companion.notes if note.strip())
        next_notes = current_notes + tuple(note for note in profile_delta.relationship_notes if note not in current_notes)
        next_loaded = replace(
            next_loaded,
            companion=replace(companion, notes=next_notes),
        )
    if next_loaded == loaded:
        return loaded
    return runtime._persist_profile(next_loaded, sync_source="turn.reconciliation")


def build_kernel_dependencies(
    runtime: CliRuntime,
    session: SessionState,
    profile: ProfileState,
    *,
    memory_capability_cls,
    context_capability_cls,
    telemetry_cls,
    delivery_capability_cls,
) -> KernelDependencies:
    memory = memory_capability_cls(memory_runtime=runtime.memory_runtime, repository=runtime.repository)
    model_tools = _RequesterScopedToolCapability(
        tool_runtime=runtime.tool_runtime,
        requester="model",
        descriptor=runtime.tool_runtime.descriptor,
    )
    return KernelDependencies(
        storage=runtime.repository,
        context=context_capability_cls(
            profile_loader=runtime.profile_loader,
            repository=runtime.repository,
            prompt_mode="full",
            snapshot_path=runtime.snapshot_path,
            total_tokens=runtime.active_provider_context_window(),
            tool_runtime=runtime.tool_runtime,
            skill_runtime=runtime.skill_runtime,
            workspace_dir=runtime.paths.workspace_dir,
            summary_model_provider=runtime.model_provider,
        ),
        planning=PlanningService(),
        memory=memory,
        model_provider=runtime.model_provider,
        telemetry=telemetry_cls(runtime.snapshot_path, observer=runtime.kernel_event_observer),
        tools=model_tools,
        delivery=delivery_capability_cls(),
        embedding_service=runtime.memory_runtime.retriever.evidence_retriever.embedding_service,
        security_policy=runtime.security_policy,
        skill_runtime=runtime.skill_runtime,
    )
