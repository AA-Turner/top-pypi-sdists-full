from __future__ import annotations

import concurrent.futures
import sys
from uuid import uuid4

from packages.embeddings import build_default_embedding_service, embedding_runtime_is_loaded
from packages.intent import HybridIntentResolver
from packages.contracts import IntentCandidate

from .context_compaction import (
    compact_context_after_usage,
    flush_projection_memory,
    latest_compacted_projection,
    projection_compaction_detail,
    retry_context_after_provider_overflow,
    stage_context_projection, stage_context_usage,
)
from .generation_context import build_context_for_generation
from .memory_recovery import (
    memory_goal_ids,
    memory_query,
    memory_replay_mode,
    memory_retrieval_scopes,
    memory_scope_reason,
    memory_scope_session_ids,
)
from .runtime_support import *  # noqa: F401,F403
_SUPPORT_UTC_NOW = _utc_now


def _clock_now() -> datetime:
    runtime_module = sys.modules.get("packages.kernel.runtime")
    runtime_now = getattr(runtime_module, "_utc_now", None) if runtime_module is not None else None
    if callable(runtime_now):
        return runtime_now()
    return _SUPPORT_UTC_NOW()


def _provider_system_prompt_for_recording(context: ContextBundle) -> str:
    system_prompt = context.prompt_envelope.system_prompt()
    if system_prompt.strip():
        return system_prompt
    return context.rendered_prompt or ""


@dataclass(frozen=True, slots=True)
class KernelService:
    dependencies: KernelDependencies

    def run(self, request: KernelTurnRequest) -> KernelOutcome:
        stages: list[KernelStageRecord] = []
        event = request.event
        current = _clock_now()

        def stage(name: str, detail: str) -> None:
            record = KernelStageRecord(stage=name, detail=detail, recorded_at=_clock_now())
            stages.append(record)
            self.dependencies.telemetry.emit(
                {
                    "event_id": f"telemetry:{event.session_id}:{record.stage}:{record.recorded_at.isoformat()}",
                    "event_type": "kernel.stage",
                    "session_id": event.session_id,
                    "source": "kernel",
                    "payload": {
                        "stage": record.stage,
                        "detail": record.detail,
                        "recorded_at": record.recorded_at.isoformat(),
                        "event_id": event.event_id,
                    },
                }
            )

        stage("ingest", f"event={event.event_id}")
        session = self.dependencies.storage.load_session(event.session_id)
        if session is None:
            raise KeyError(f"unknown session: {event.session_id}")

        profile = self.dependencies.storage.load_profile(session.profile_id)
        if profile is None:
            raise KeyError(f"unknown profile: {session.profile_id}")

        stage("resolve", f"profile={profile.profile_id} session={session.session_id}")

        recovered_state = self._recover_state_bundle(profile)
        stage(
            "identity-user",
            " ".join(
                (
                    f"identity={(recovered_state.identity.clone_id if recovered_state.identity is not None else '<missing>')}",
                    f"user={(recovered_state.user.user_card_id if recovered_state.user is not None else '<missing>')}",
                )
            ),
        )

        goal_graph = self._recover_work_graph(session)
        goal_graph = self._maintain_goal_graph(session, goal_graph, request, current)
        stage(
            "goals-maintain",
            f"goals={len(goal_graph.goals)} active_goal={goal_graph.active_goal_id or '<none>'}",
        )
        stage(
            "relationship",
            " ".join(
                (
                    f"relationship={(recovered_state.relationship.relationship_id if recovered_state.relationship is not None else '<missing>')}",
                    f"continuity_notes={len(recovered_state.continuity_notes)}",
                )
            ),
        )
        continuity_session, continuity = self._recover_continuity(session, goal_graph)
        clock = _build_clock_context(continuity_session, user=recovered_state.user, now=current)
        intent = self._resolve_intent(
            request,
            continuity_session,
            profile,
            goal_graph,
            continuity=continuity,
        )
        stage(
            "intent",
            " ".join(
                (
                    f"intent={intent.intent}",
                    f"confidence={intent.confidence:.2f}",
                    f"focus={','.join(intent.focus_activity_ids) or '<none>'}",
                    f"scope={intent.scope_suggestion}",
                    f"degradation={intent.degradation_mode}",
                    f"weak_assist={str(intent.needs_weak_model_assist).lower()}",
                    f"weak_outcome={intent.weak_assist_outcome}",
                    f"fallback={intent.fallback_path}",
                    f"candidates={len(intent.candidate_scores)}",
                )
            ),
        )
        memory_recovery = self._recover_memories(
            continuity_session,
            goal_graph,
            request,
            intent=intent,
            relationship=recovered_state.relationship,
            continuity=continuity,
        )
        memories = memory_recovery.memories
        goals = goal_graph.goals
        stage(
            "recover",
            " ".join(
                (
                    f"goals={len(goals)}",
                    f"memories={len(memories)}",
                    f"active_goal={goal_graph.active_goal_id or '<none>'}",
                    f"continuity={continuity.mode}",
                    f"origin={continuity.origin_session_id}",
                    f"scope={','.join(memory_recovery.scope_session_ids)}",
                )
            ),
        )

        context = self.dependencies.context.assemble(continuity_session, goals, memories, intent=intent)
        projection_compaction = latest_compacted_projection(self.dependencies.context)
        if projection_compaction is not None:
            stage("context-compact", projection_compaction_detail(projection_compaction))
            flush_projection_memory(self.dependencies.context)
        stage(
            "context",
            f"bundle={context.bundle_id} budget={context.token_budget} recovery_scope_reason={memory_recovery.scope_reason}",
        )

        decision, plan = self._choose_plan(
            goal_graph,
            memories,
            continuity_session,
            recovered_state=recovered_state,
        )
        stage(
            "select",
            " ".join(
                (
                    f"decision={decision.decision_id}",
                    f"goal={decision.selected_move.goal_id or 'none'}",
                    f"kind={decision.selected_move.kind}",
                    f"progression={decision.rationale.progression_action}",
                    f"planned_active_goal={decision.rationale.planned_active_goal_id or '<none>'}",
                )
            ),
        )
        execution_goals = goal_graph.goals
        context = self._context_for_generation(
            request=request,
            profile=profile,
            session=continuity_session,
            intent=intent,
            goals=execution_goals,
            memories=memories,
            context=context,
            decision=decision,
            plan=plan,
            continuity=continuity,
            clock=clock,
        )
        stage_context_projection(stage, context)
        prepared_run, prompt_for_execution = self._prepare_agent_run(request, continuity_session, clock=clock)
        try:
            execution, run = self._execute(
                request,
                profile,
                continuity_session,
                context,
                prompt_for_execution=prompt_for_execution,
                agent_run=prepared_run, stage=stage,
            )
        except RuntimeError as error:
            retry_context = retry_context_after_provider_overflow(
                error=error,
                dependencies=self.dependencies,
                request=request,
                profile=profile,
                session=continuity_session,
                intent=intent,
                goals=execution_goals,
                memories=memories,
                decision=decision,
                plan=plan,
                continuity=continuity,
                clock=clock,
                stage=stage,
                context_for_generation=self._context_for_generation,
                recovery_scope_reason=memory_recovery.scope_reason,
            )
            if retry_context is None:
                raise
            context = retry_context
            execution, run = self._execute(
                request,
                profile,
                continuity_session,
                context,
                prompt_for_execution=prompt_for_execution,
                agent_run=prepared_run, stage=stage,
            )
        compact_context_after_usage(dependencies=self.dependencies, execution=execution, context=context, stage=stage)
        stage("execute", f"execution={execution.execution_id} outcome={execution.outcome}")

        goal_graph = self._refresh_work_graph(event.session_id, fallback=goal_graph)
        goal_graph = self._reconcile_goal_graph(
            continuity_session,
            goal_graph,
            request,
            execution,
            decision=decision,
            current=_clock_now(),
        )
        execution_goals = goal_graph.goals
        stage(
            "goals-reconcile",
            f"goals={len(goal_graph.goals)} active_goal={goal_graph.active_goal_id or '<none>'}",
        )

        persisted_at = _clock_now()
        refreshed_session = self._persist(
            profile,
            continuity_session,
            persisted_at,
            goal_graph,
            continuity,
            run=run,
        )
        stage("persist", f"session={session.session_id}")

        delivery = self._deliver(request, profile, refreshed_session, execution, plan)
        stage("emit", "telemetry and delivery hooks dispatched")

        outcome = KernelOutcome(
            event=event,
            profile=profile,
            session=refreshed_session,
            continuity=continuity,
            intent=intent,
            goals=execution_goals,
            goal_graph=goal_graph,
            memories=memories,
            context=context,
            decision=decision,
            plan=plan,
            run=run,
            execution=execution,
            delivery=delivery,
            stages=tuple(stages),
        )
        self._emit_telemetry(outcome)
        return outcome

    def _recover_work_graph(self, session: SessionState) -> ActivityGraph:
        load_activity_graph = getattr(self.dependencies.storage, "load_activity_graph", None)
        if callable(load_activity_graph):
            graph = load_activity_graph(session.session_id)
            if graph is not None:
                return goal_graph_to_activity_graph(graph)
        return ActivityGraph(session_id=session.session_id)

    def _refresh_work_graph(self, session_id: str, *, fallback: ActivityGraph) -> ActivityGraph:
        load_activity_graph = getattr(self.dependencies.storage, "load_activity_graph", None)
        if callable(load_activity_graph):
            graph = load_activity_graph(session_id)
            if graph is not None:
                return goal_graph_to_activity_graph(graph)
        return fallback

    def _recover_state_bundle(self, profile: ProfileState) -> _RecoveredStateBundle:
        load_identity = getattr(self.dependencies.storage, "load_clone_identity_for_profile", None)
        load_user = getattr(self.dependencies.storage, "load_user_card_for_profile", None)
        load_relationship = getattr(self.dependencies.storage, "load_relationship_memory_for_profile", None)
        return _RecoveredStateBundle(
            identity=load_identity(profile.profile_id) if callable(load_identity) else None,
            user=load_user(profile.profile_id) if callable(load_user) else None,
            relationship=load_relationship(profile.profile_id) if callable(load_relationship) else None,
        )

    def _resolve_intent(
        self,
        request: KernelTurnRequest,
        session: SessionState,
        profile: ProfileState,
        goal_graph: ActivityGraph,
        *,
        continuity: SessionContinuityState,
    ) -> IntentDecision:
        surface_hints: list[str] = []
        stripped_prompt = request.prompt.strip()
        if stripped_prompt.startswith("/"):
            surface_hints.append(stripped_prompt.split()[0].lower())
        for key in ("surface", "command", "view"):
            candidate = str(request.event.payload.get(key, "")).strip().lower()
            if candidate:
                surface_hints.append(candidate)
        artifact_hints: tuple[str, ...] = ()
        artifact_intent = _artifact_intent_from_prompt(request.prompt)
        if artifact_intent is not None:
            artifact_hints = (artifact_intent.path,)
        selection_getter = getattr(self.dependencies.model_provider, "selection_state", None)
        selection_state = selection_getter() if callable(selection_getter) else None
        intent_mode_override = str(request.event.payload.get("intent_mode_override", "")).strip().lower()
        if selection_state is not None and intent_mode_override == "skip":
            selection_state = replace(selection_state, intent_mode="skip")
        embedding_service = self._intent_embedding_service()
        embedding_available = False
        if selection_state is not None and selection_state.intent_mode == "embedded":
            try:
                embedding_available = embedding_runtime_is_loaded(embedding_service.health())
            except Exception:
                embedding_available = False
        return HybridIntentResolver(embedding_service=embedding_service).resolve(
            IntentResolutionRequest(
                prompt=request.prompt or str(request.event.payload.get("message", "")),
                session_id=session.session_id,
                profile_id=session.profile_id,
                workspace_id=session.workspace_id,
                continuity=continuity,
                activity_graph=goal_graph,
                surface_hints=tuple(surface_hints),
                artifact_hints=artifact_hints,
                capability_hints=((f"tool:{request.tool_name}",) if request.tool_name is not None else ()),
                guardian_candidates=(),
                skill_candidates=(),
                mixture=selection_state,
                embedding_available=embedding_available,
            )
        )

    def _intent_embedding_service(self):
        service = self.dependencies.embedding_service
        if service is not None:
            return service
        return build_default_embedding_service()

    def _recover_memories(
        self,
        session: SessionState,
        goal_graph: ActivityGraph,
        request: KernelTurnRequest,
        *,
        intent: IntentDecision,
        relationship: RelationshipMemoryRecord | None,
        continuity: SessionContinuityState,
    ) -> _MemoryRecoverySelection:
        query = memory_query(request, goal_graph=goal_graph, relationship=relationship, intent=intent)
        if not query.strip():
            return _MemoryRecoverySelection(
                memories=(),
                query="",
                goal_ids=(),
                scope_session_ids=(session.session_id,),
                scope_reason="no durable recovery query was available",
            )
        goal_ids = memory_goal_ids(goal_graph, intent=intent)
        scope_session_ids = memory_scope_session_ids(session, continuity=continuity, intent=intent)
        scope_reason = memory_scope_reason(
            session=session,
            goal_graph=goal_graph,
            intent=intent,
            relationship=relationship,
            continuity=continuity,
            scope_session_ids=scope_session_ids,
        )
        retrieve_evidence = getattr(self.dependencies.memory, "retrieve_evidence", None)
        if callable(retrieve_evidence):
            retrieval = retrieve_evidence(
                EvidenceRetrievalRequest(
                    session_id=session.session_id,
                    profile_id=session.profile_id,
                    workspace_id=session.workspace_id,
                    lineage_session_ids=scope_session_ids,
                    work_item_ids=goal_ids,
                    query=query,
                    scopes=memory_retrieval_scopes(session, continuity=continuity, intent=intent),
                    latency_mode="fast",
                    limit=5,
                    scope_reason=scope_reason,
                    relationship_hints=relationship.continuity_notes if relationship is not None else (),
                    max_compression="episode_summary",
                    replay_mode=memory_replay_mode(intent),
                    intent_decision=intent,
                    allow_embeddings=str(request.event.payload.get("allow_embeddings", "true")).strip().lower() != "false",
                )
            )
            return _MemoryRecoverySelection(
                memories=tuple(candidate.memory for candidate in retrieval.candidates),
                query=query,
                goal_ids=goal_ids,
                scope_session_ids=retrieval.scope_session_ids,
                scope_reason=retrieval.scope_reason,
            )
        memories = self.dependencies.memory.search(
            session.session_id,
            query,
            goal_ids=goal_ids,
            scope_session_ids=scope_session_ids,
            scope_reason=scope_reason,
        )
        return _MemoryRecoverySelection(
            memories=memories,
            query=query,
            goal_ids=goal_ids,
            scope_session_ids=scope_session_ids,
            scope_reason=scope_reason,
        )

    def _recover_continuity(
        self,
        session: SessionState,
        goal_graph: ActivityGraph,
    ) -> tuple[SessionState, SessionContinuityState]:
        service = SessionLineageService(repository=self.dependencies.storage)
        load_lineage = getattr(self.dependencies.storage, "lineage", None)
        lineage = load_lineage(session.session_id) if callable(load_lineage) else (session,)
        continuity = service.continuity_state(
            session,
            lineage=lineage,
            active_goal_id=goal_graph.active_goal_id,
        )
        return service.apply_continuity_state(session, continuity), continuity

    def _choose_plan(
        self,
        goal_graph: ActivityGraph,
        memories: tuple[MemoryRecord, ...],
        session: SessionState,
        *,
        recovered_state: _RecoveredStateBundle,
    ) -> tuple[PlanningDecision, PlanDraft]:
        decision = self.dependencies.planning.choose_next_step(
            session=session,
            graph=goal_graph,
            memories=memories,
            initiative_hint=recovered_state.initiative_hint,
            continuity_notes=recovered_state.continuity_notes,
        )
        return decision, build_plan_draft_from_decision(decision)

    def _maintain_goal_graph(
        self,
        session: SessionState,
        goal_graph: ActivityGraph,
        request: KernelTurnRequest,
        current: datetime,
    ) -> ActivityGraph:
        maintain = getattr(self.dependencies.planning, "maintain_goal_graph", None)
        if not callable(maintain):
            return goal_graph
        result = maintain(
            session=session,
            graph=goal_graph,
            prompt=request.prompt,
            goal_query=request.goal_query,
            event=request.event,
            now=current,
        )
        if hasattr(result, "graph"):
            return goal_graph_to_activity_graph(result.graph)
        return goal_graph

    def _reconcile_goal_graph(
        self,
        session: SessionState,
        goal_graph: ActivityGraph,
        request: KernelTurnRequest,
        execution: ExecutionResult,
        *,
        decision: PlanningDecision | None,
        current: datetime,
    ) -> ActivityGraph:
        reconcile = getattr(self.dependencies.planning, "reconcile_goal_graph", None)
        if not callable(reconcile):
            return goal_graph
        result = reconcile(
            session=session,
            graph=goal_graph,
            prompt=request.prompt,
            execution=execution,
            decision=decision,
            event=request.event,
            now=current,
        )
        if hasattr(result, "graph"):
            return goal_graph_to_activity_graph(result.graph)
        return goal_graph

    def _context_for_generation(
        self,
        *,
        request: KernelTurnRequest,
        profile: ProfileState,
        session: SessionState,
        intent: IntentDecision,
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        context: ContextBundle,
        decision: PlanningDecision | None,
        plan: PlanDraft | None,
        continuity: SessionContinuityState,
        clock: _ClockContext | None = None,
    ) -> ContextBundle:
        return build_context_for_generation(
            dependencies=self.dependencies,
            request=request,
            profile=profile,
            session=session,
            intent=intent,
            goals=goals,
            memories=memories,
            context=context,
            decision=decision,
            plan=plan,
            continuity=continuity,
            clock=clock,
            augment_clock=_augment_context_with_clock,
        )

    def _prepare_agent_run(
        self,
        request: KernelTurnRequest,
        session: SessionState,
        *,
        clock: _ClockContext | None = None,
    ) -> tuple[AgentRunState | None, str]:
        prompt_for_execution = _apply_request_execution_guidance(request.prompt, clock=clock)
        if request.tool_name is not None or self.dependencies.tools is None:
            return None, prompt_for_execution
        load_active_run = getattr(self.dependencies.storage, "load_latest_open_agent_run", None)
        upsert_run = getattr(self.dependencies.storage, "upsert_agent_run", None)
        if not callable(load_active_run):
            return None, prompt_for_execution
        active_run = load_active_run(session.session_id)
        service = AgentRunService()
        if active_run is None or not service.should_resume(request.prompt):
            return None, prompt_for_execution
        resumed = service.resume_run(active_run)
        if callable(upsert_run):
            upsert_run(resumed)
        return resumed, _apply_request_execution_guidance(
            service.resume_prompt_for_request(resumed, request.prompt),
            clock=clock,
        )

    def _execute(
        self,
        request: KernelTurnRequest,
        profile: ProfileState,
        session: SessionState,
        context: ContextBundle,
        *,
        prompt_for_execution: str,
        agent_run: AgentRunState | None,
        stage: object | None = None,
    ) -> tuple[ExecutionResult, AgentRunState | None]:
        if request.tool_name is not None:
            if self.dependencies.tools is None:
                raise RuntimeError("tool execution requested but no tool capability was configured")
            return _execute_direct_tool_run(request=request, session=session, tool_capability=self.dependencies.tools, persist_agent_run=self._persist_agent_run)
        response = self.dependencies.model_provider.generate(
            profile=profile,
            session=session,
            context=context,
            prompt=prompt_for_execution,
        )
        if self.dependencies.tools is None:
            stage_context_usage(stage, response.prompt_tokens, response.completion_tokens, response.total_tokens)
            return _clean_execution_summary(response), None
        return self._execute_model_tool_loop(
            request=request,
            profile=profile,
            session=session,
            context=context,
            initial=response,
            prompt_for_execution=prompt_for_execution,
            agent_run=agent_run,
            stage=stage,
        )

    def _execute_model_tool_loop(
        self,
        *,
        request: KernelTurnRequest,
        profile: ProfileState,
        session: SessionState,
        context: ContextBundle,
        initial: ExecutionResult,
        prompt_for_execution: str,
        agent_run: AgentRunState | None,
        stage: object | None = None,
    ) -> tuple[ExecutionResult, AgentRunState | None]:
        response = initial
        prompt_tokens_total = response.prompt_tokens
        completion_tokens_total = response.completion_tokens
        total_tokens_total = response.total_tokens
        cached_prompt_tokens_total = response.cached_prompt_tokens
        cache_creation_prompt_tokens_total = response.cache_creation_prompt_tokens
        cache_usage_reported = response.cache_usage_reported
        stage_context_usage(stage, prompt_tokens_total, completion_tokens_total, total_tokens_total)
        loop_context = context
        loop_traces: list[str] = []
        run_service = AgentRunService()
        budget = run_service.budget
        current_run = agent_run
        starting_model_turn_count = current_run.model_turn_count if current_run is not None else 0
        context_recorded = False
        deadline = _clock_now() + timedelta(seconds=(current_run.max_wall_time_seconds if current_run is not None else budget.max_wall_time_seconds))
        while True:
            parsed = _parse_execution_tool_calls(response)
            deduped_calls = _deduplicate_tool_calls(parsed.calls)
            parsed_for_turn = replace(parsed, calls=deduped_calls)
            if current_run is None:
                current_run = run_service.start_run(session_id=session.session_id, source_event_id=request.event.event_id, prompt=request.prompt)
                self._persist_agent_run(current_run)
            provider_system_prompt = _provider_system_prompt_for_recording(context)
            if current_run is not None and not context_recorded and provider_system_prompt:
                current_run, context_step = run_service.record_context_prompt(current_run, system_prompt=provider_system_prompt)
                self._persist_agent_run(current_run, step=context_step)
                context_recorded = True
            if current_run is not None:
                cleaned_summary = _model_turn_summary(response, parsed=parsed_for_turn)
                current_run, model_step = run_service.record_model_turn(current_run, summary=cleaned_summary, response_text=_clean_execution_summary(response).summary)
                self._persist_agent_run(current_run, step=model_step)
            if not deduped_calls:
                cleaned = _with_execution_usage(
                    _clean_execution_summary(response),
                    prompt_tokens=prompt_tokens_total,
                    completion_tokens=completion_tokens_total,
                    total_tokens=total_tokens_total,
                    cached_prompt_tokens=cached_prompt_tokens_total,
                    cache_creation_prompt_tokens=cache_creation_prompt_tokens_total,
                    cache_usage_reported=cache_usage_reported,
                )
                if not loop_traces:
                    if current_run is not None:
                        current_run = run_service.complete(current_run, summary=cleaned.summary)
                        self._persist_agent_run(current_run)
                    return cleaned, current_run
                finalized = replace(
                    cleaned,
                    side_effects=tuple(dict.fromkeys((*cleaned.side_effects, *loop_traces))),
                )
                if current_run is not None:
                    current_run = run_service.complete(current_run, summary=finalized.summary)
                    self._persist_agent_run(current_run)
                return finalized, current_run

            observations: list[str] = []
            tool_budget_config = _tool_result_budget_config(
                preview_chars=budget.tool_result_preview_chars,
                turn_budget_chars=budget.tool_result_turn_budget_chars,
                persist_threshold_chars=budget.tool_result_persist_threshold_chars,
            )
            for call, result in self._invoke_tool_batch(deduped_calls, session=session):
                loop_traces.append(call.tool_name)
                if current_run is not None:
                    current_run, tool_step = run_service.record_tool_step(
                        current_run,
                        tool_name=call.tool_name,
                        arguments=call.arguments,
                        result=result,
                    )
                    self._persist_agent_run(current_run, step=tool_step)
                summary = _budget_tool_result_summary(
                    result.summary,
                    tool_name=call.tool_name,
                    tool_use_id=result.execution_id,
                    config=tool_budget_config,
                )
                observations.append(
                    "\n".join(
                        [
                            f"tool: {call.tool_name}",
                            f"arguments: {_format_tool_arguments(call.arguments)}",
                            f"outcome: {result.outcome}",
                            f"summary: {summary}",
                        ]
                    )
                )

            observations = _enforce_observation_budget(
                observations,
                config=tool_budget_config,
            )

            if current_run is not None and (
                (current_run.model_turn_count - starting_model_turn_count) >= current_run.max_model_turns
                or _clock_now() >= deadline
            ):
                reason = (
                    "model-turn-budget"
                    if (current_run.model_turn_count - starting_model_turn_count) >= current_run.max_model_turns
                    else "wall-time-budget"
                )
                recent_steps = self._list_recent_agent_run_steps(current_run.run_id, limit=6)
                continuation_prompt = run_service.build_continuation_prompt(
                    current_run,
                    recent_steps=recent_steps,
                    observations=tuple(observations),
                )
                parked = run_service.park(
                    current_run,
                    continuation_prompt=continuation_prompt,
                    waiting_reason=reason,
                    last_summary=parsed.cleaned_text or response.summary,
                )
                self._persist_agent_run(parked)
                message = (
                    "I kept working through this request and parked it at a durable checkpoint "
                    f"after {parked.model_turn_count} model rounds and {parked.tool_call_count} tool calls. "
                    "Ask me to continue and I will resume from the saved run."
                )
                return (
                    ExecutionResult(
                        execution_id=f"run:{parked.run_id}:pending",
                        session_id=session.session_id,
                        outcome="paused",
                        summary=message,
                        prompt_tokens=prompt_tokens_total,
                        completion_tokens=completion_tokens_total,
                        total_tokens=total_tokens_total,
                        cached_prompt_tokens=cached_prompt_tokens_total,
                        cache_creation_prompt_tokens=cache_creation_prompt_tokens_total,
                        cache_usage_reported=cache_usage_reported,
                        side_effects=tuple(dict.fromkeys(loop_traces)),
                    ),
                    parked,
                )

            loop_context = _augment_context_with_tool_results(loop_context, observations)
            response = self.dependencies.model_provider.generate(
                profile=profile,
                session=session,
                context=loop_context,
                prompt=_tool_followup_prompt(
                    current_run.prompt if current_run is not None else request.prompt,
                    observations=tuple(observations),
                ),
            )
            prompt_tokens_total += response.prompt_tokens
            completion_tokens_total += response.completion_tokens
            total_tokens_total += response.total_tokens
            cached_prompt_tokens_total += response.cached_prompt_tokens
            cache_creation_prompt_tokens_total += response.cache_creation_prompt_tokens
            cache_usage_reported = cache_usage_reported or response.cache_usage_reported
            stage_context_usage(stage, prompt_tokens_total, completion_tokens_total, total_tokens_total)

    def _invoke_tool_batch(
        self,
        calls: tuple[_TextToolCall, ...],
        *,
        session: SessionState,
    ) -> list[tuple[_TextToolCall, ExecutionResult]]:
        if not _should_parallelize_tool_batch(calls):
            return [(call, self._invoke_tool_call(call, session=session)) for call in calls]

        max_workers = min(len(calls), _MAX_PARALLEL_TOOL_WORKERS)
        ordered_results: list[tuple[_TextToolCall, ExecutionResult] | None] = [None] * len(calls)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self._invoke_tool_call, call, session=session): index
                for index, call in enumerate(calls)
            }
            for future in concurrent.futures.as_completed(futures):
                index = futures[future]
                ordered_results[index] = (calls[index], future.result())
        return [result for result in ordered_results if result is not None]

    def _invoke_tool_call(
        self,
        call: _TextToolCall,
        *,
        session: SessionState,
    ) -> ExecutionResult:
        try:
            assert self.dependencies.tools is not None
            return self.dependencies.tools.invoke(
                call.tool_name,
                dict(call.arguments),
                session_id=session.session_id,
            )
        except Exception as error:
            return ExecutionResult(
                execution_id=f"tool:{session.session_id}:{uuid4().hex[:8]}",
                session_id=session.session_id,
                outcome="failed",
                summary=str(error),
                side_effects=(call.tool_name,),
            )

    def _deliver(
        self,
        request: KernelTurnRequest,
        profile: ProfileState,
        session: SessionState,
        execution: ExecutionResult,
        plan: PlanDraft | None,
    ) -> ExecutionResult | None:
        if self.dependencies.delivery is None:
            return None
        payload = {
            "event_id": request.event.event_id,
            "profile_id": profile.profile_id,
            "session_id": session.session_id,
            "outcome": execution.outcome,
            "summary": execution.summary,
            "plan_id": plan.plan_id if plan is not None else None,
        }
        payload.update(dict(request.delivery_payload))
        return self.dependencies.delivery.deliver(session.session_id, payload)

    def _persist(
        self,
        profile: ProfileState,
        session: SessionState,
        updated_at: datetime,
        goal_graph: ActivityGraph,
        continuity: SessionContinuityState,
        *,
        run: AgentRunState | None,
    ) -> SessionState:
        interruption_state = session.interruption_state
        if run is not None:
            run_interruption = AgentRunService().interruption_state(run)
            if run_interruption is not None:
                interruption_state = run_interruption
            elif interruption_state is not None and interruption_state.startswith("agent-run:"):
                interruption_state = None
        refreshed_session = replace(session, updated_at=updated_at, interruption_state=interruption_state)
        self.dependencies.storage.upsert_profile(profile, updated_at=updated_at)
        self.dependencies.storage.upsert_session(
            refreshed_session,
            resume_count_delta=1 if continuity.requires_recovery else 0,
        )
        return refreshed_session

    def _persist_agent_run(
        self,
        run: AgentRunState,
        *,
        step: AgentRunStep | None = None,
    ) -> None:
        upsert_run = getattr(self.dependencies.storage, "upsert_agent_run", None)
        if callable(upsert_run):
            upsert_run(run)
        append_step = getattr(self.dependencies.storage, "append_agent_run_step", None)
        if step is not None and callable(append_step):
            append_step(step)

    def _list_recent_agent_run_steps(self, run_id: str, *, limit: int) -> tuple[AgentRunStep, ...]:
        list_steps = getattr(self.dependencies.storage, "list_agent_run_steps", None)
        if not callable(list_steps):
            return ()
        return tuple(list_steps(run_id, limit=limit))

    def _emit_telemetry(self, outcome: KernelOutcome) -> None:
        self.dependencies.telemetry.emit(
            {
                "event_id": f"telemetry:{outcome.session.session_id}:outcome:{uuid4().hex}",
                "event_type": "kernel.outcome",
                "session_id": outcome.session.session_id,
                "source": "kernel",
                "payload": {
                    "event_id": outcome.event.event_id,
                    "profile_id": outcome.profile.profile_id,
                    "context_bundle_id": outcome.context.bundle_id,
                    "execution_id": outcome.execution.execution_id,
                    "execution_outcome": outcome.execution.outcome,
                    "delivery_execution_id": outcome.delivery.execution_id if outcome.delivery is not None else "",
                    "continuity_mode": outcome.continuity.mode,
                    "continuity_origin_session_id": outcome.continuity.origin_session_id,
                    "continuity_requires_recovery": str(outcome.continuity.requires_recovery).lower(),
                    "intent_family": outcome.intent.intent,
                    "intent_confidence": f"{outcome.intent.confidence:.2f}",
                    "intent_degradation_mode": outcome.intent.degradation_mode,
                    "intent_needs_weak_model_assist": str(outcome.intent.needs_weak_model_assist).lower(),
                    "intent_weak_assist_outcome": outcome.intent.weak_assist_outcome,
                    "intent_fallback_path": outcome.intent.fallback_path,
                    "selected_goal_id": outcome.decision.selected_move.goal_id if outcome.decision is not None else "",
                    "selected_kind": outcome.decision.selected_move.kind if outcome.decision is not None else "",
                    "progression_action": outcome.decision.rationale.progression_action if outcome.decision is not None else "",
                    "planned_active_goal_id": outcome.decision.rationale.planned_active_goal_id if outcome.decision is not None else "",
                    "goal_graph_revision": outcome.goal_graph.revision_id or "",
                    "agent_run_id": outcome.run.run_id if outcome.run is not None else "",
                    "agent_run_status": outcome.run.status if outcome.run is not None else "",
                    "agent_run_step_count": outcome.run.step_count if outcome.run is not None else 0,
                },
            }
        )
