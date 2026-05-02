from __future__ import annotations

from .service_support import *  # noqa: F401,F403

class PlanningService:
    """Score goal graph candidates and emit next-step rationale."""

    def __init__(self, reasoner: TemporalReasoner | None = None) -> None:
        self._reasoner = TemporalReasoner() if reasoner is None else reasoner

    def maintain_goal_graph(
        self,
        *,
        session: SessionState,
        graph: GoalGraph | ActivityGraph,
        prompt: str,
        goal_query: str | None = None,
        event: EventEnvelope | None = None,
        now: datetime | None = None,
    ) -> GoalGraphLifecycleUpdate:
        graph_surface = graph
        graph = activity_graph_to_goal_graph(graph)
        current = _now() if now is None else now

        def lifecycle(
            graph_value: GoalGraph,
            *,
            changed: bool,
            summary: str,
            created_goal_ids: tuple[str, ...] = (),
            updated_goal_ids: tuple[str, ...] = (),
        ) -> GoalGraphLifecycleUpdate:
            return GoalGraphLifecycleUpdate(
                graph=_project_graph_surface(graph_surface, graph_value),
                changed=changed,
                summary=summary,
                created_goal_ids=created_goal_ids,
                updated_goal_ids=updated_goal_ids,
            )

        seed = _goal_seed_text(prompt=prompt, goal_query=goal_query, event=event)
        if not seed:
            return lifecycle(graph, changed=False, summary="No explicit durable goal signal was present.")

        signal = _analyze_goal_signal(seed)
        signal = replace(signal, task_like=True)

        if not signal.task_like and not any((signal.completion, signal.deferred, signal.blocked, signal.focus)):
            return lifecycle(graph, changed=False, summary="The turn did not imply a durable goal mutation.")

        event_refs = (f"event:{event.event_id}",) if event is not None else ()
        revision_id = f"goal:maintain:{uuid4().hex}"

        if not graph.nodes:
            initial_goal = replace(
                _new_goal_node(
                    graph=graph,
                    session_id=session.session_id,
                    signal=signal,
                    updated_at=current,
                    revision_id=revision_id,
                ),
                parent_goal_id=None,
                evidence_refs=event_refs,
            )
            next_graph = GoalGraph(
                session_id=session.session_id,
                nodes=(initial_goal,),
                root_goal_id=initial_goal.goal_id,
                active_goal_id=initial_goal.goal_id,
                revision_id=revision_id,
                updated_at=current,
            )
            return lifecycle(
                next_graph,
                changed=True,
                summary=f'Created the initial durable goal "{initial_goal.title}".',
                created_goal_ids=(initial_goal.goal_id,),
                updated_goal_ids=(initial_goal.goal_id,),
            )

        matched = _match_goal_for_signal(graph, signal)
        similarity = _goal_similarity(signal.source_text, matched.title) if matched is not None else 0.0
        desired_status = _status_for_signal(signal, matched)
        next_graph = graph
        updated_goal_ids: list[str] = []

        if matched is not None and desired_status is not None:
            next_status = desired_status
            next_active_goal_id = graph.active_goal_id
            if next_status in {"completed", "done", "failed", "dropped", "blocked", "deferred"} and graph.active_goal_id == matched.goal_id:
                next_active_goal_id = _fallback_active_goal_id(graph, exclude_goal_id=matched.goal_id)
            next_graph = next_graph.transition_goal(
                matched.goal_id,
                status=next_status,
                revision_id=revision_id,
                updated_at=current,
                active_goal_id=next_active_goal_id,
                evidence_refs=_dedupe_strings(matched.evidence_refs, event_refs),
                review_checkpoint=matched.review_checkpoint,
            )
            refreshed = next_graph.goal(matched.goal_id)
            if refreshed is not None:
                if signal.time_sensitivity != refreshed.time_sensitivity and _TIME_SENSITIVITY_POINTS[signal.time_sensitivity] > _TIME_SENSITIVITY_POINTS[refreshed.time_sensitivity]:
                    next_graph = next_graph.with_goal(
                        replace(
                            refreshed,
                            time_sensitivity=signal.time_sensitivity,
                            revision_id=revision_id,
                            updated_at=current,
                        )
                    )
                if next_status == "active":
                    next_graph = _ensure_single_active_goal(
                        next_graph,
                        goal_id=matched.goal_id,
                        revision_id=revision_id,
                        updated_at=current,
                    )
            updated_goal_ids.append(matched.goal_id)
            if next_graph != graph:
                action = {
                    "completed": "Completed",
                    "blocked": "Marked blocked",
                    "deferred": "Deferred",
                    "active": "Focused",
                }.get(next_status, "Updated")
                return lifecycle(
                    next_graph,
                    changed=True,
                    summary=f'{action} goal "{matched.title}".',
                    updated_goal_ids=tuple(updated_goal_ids),
                )

        if matched is not None and signal.task_like and (
            similarity >= 0.35 or (goal_query is not None and matched.goal_id == graph.active_goal_id)
        ):
            focused_graph = _ensure_single_active_goal(
                graph,
                goal_id=matched.goal_id,
                revision_id=revision_id,
                updated_at=current,
            )
            refreshed = focused_graph.goal(matched.goal_id)
            if refreshed is not None:
                refreshed = replace(
                    refreshed,
                    evidence_refs=_dedupe_strings(refreshed.evidence_refs, event_refs),
                    time_sensitivity=(
                        signal.time_sensitivity
                        if _TIME_SENSITIVITY_POINTS[signal.time_sensitivity] > _TIME_SENSITIVITY_POINTS[refreshed.time_sensitivity]
                        else refreshed.time_sensitivity
                    ),
                    revision_id=revision_id,
                    updated_at=current,
                )
                focused_graph = focused_graph.with_goal(refreshed)
            if focused_graph != graph:
                return lifecycle(
                    focused_graph,
                    changed=True,
                    summary=f'Kept "{matched.title}" as the active durable goal.',
                    updated_goal_ids=(matched.goal_id,),
                )
            return lifecycle(
                graph,
                changed=False,
                summary=f'"{matched.title}" already matches the current durable goal.',
            )

        if signal.task_like:
            new_goal = replace(
                _new_goal_node(
                    graph=graph,
                    session_id=session.session_id,
                    signal=signal,
                    updated_at=current,
                    revision_id=revision_id,
                ),
                evidence_refs=event_refs,
            )
            created_graph = graph.with_goal(new_goal)
            created_graph = _ensure_single_active_goal(
                created_graph,
                goal_id=new_goal.goal_id,
                revision_id=revision_id,
                updated_at=current,
            )
            if created_graph.root_goal_id is None:
                created_graph = replace(
                    created_graph,
                    root_goal_id=graph.active_goal_id or new_goal.goal_id,
                    revision_id=revision_id,
                    updated_at=current,
                )
            created_graph = _reassign_active_goal(
                created_graph,
                active_goal_id=new_goal.goal_id,
                revision_id=revision_id,
                updated_at=current,
            )
            return lifecycle(
                created_graph,
                changed=True,
                summary=f'Created a new durable goal "{new_goal.title}".',
                created_goal_ids=(new_goal.goal_id,),
                updated_goal_ids=(new_goal.goal_id,),
            )

        return lifecycle(graph, changed=False, summary="No durable goal mutation was required.")

    def reconcile_goal_graph(
        self,
        *,
        session: SessionState,
        graph: GoalGraph | ActivityGraph,
        prompt: str,
        execution: ExecutionResult,
        decision: PlanningDecision | None = None,
        event: EventEnvelope | None = None,
        now: datetime | None = None,
    ) -> GoalGraphLifecycleUpdate:
        graph_surface = graph
        graph = activity_graph_to_goal_graph(graph)
        current = _now() if now is None else now

        def lifecycle(
            graph_value: GoalGraph,
            *,
            changed: bool,
            summary: str,
            created_goal_ids: tuple[str, ...] = (),
            updated_goal_ids: tuple[str, ...] = (),
        ) -> GoalGraphLifecycleUpdate:
            return GoalGraphLifecycleUpdate(
                graph=_project_graph_surface(graph_surface, graph_value),
                changed=changed,
                summary=summary,
                created_goal_ids=created_goal_ids,
                updated_goal_ids=updated_goal_ids,
            )

        if not graph.nodes:
            return lifecycle(graph, changed=False, summary="No durable goals existed to reconcile.")

        goal_id = (
            decision.selected_move.goal_id
            if decision is not None and decision.selected_move.goal_id is not None
            else graph.active_goal_id
        )
        if goal_id is None:
            return lifecycle(graph, changed=False, summary="No active goal was available for reconciliation.")
        goal = graph.goal(goal_id)
        if goal is None:
            return lifecycle(graph, changed=False, summary="The selected goal no longer exists in durable state.")

        signal = _analyze_goal_signal(" ".join(part for part in (prompt, execution.summary) if part).strip())
        revision_id = f"goal:reconcile:{uuid4().hex}"
        evidence_refs = _dedupe_strings(
            goal.evidence_refs,
            (f"event:{event.event_id}",) if event is not None else (),
            (f"execution:{execution.execution_id}",),
        )

        next_status = goal.status
        if signal.completion:
            next_status = "completed"
        elif signal.deferred:
            next_status = "deferred"
        elif signal.blocked or execution.outcome in {"error", "failed"}:
            next_status = "blocked"
        elif decision is not None and decision.selected_move.kind in {"act_on_task", "answer_directly"} and goal.status in {"proposed", "queued"}:
            next_status = "active"

        review_checkpoint = goal.review_checkpoint
        if execution.outcome == "paused":
            review_checkpoint = execution.summary[:160]

        next_active_goal_id = graph.active_goal_id
        if next_status in {"completed", "done", "failed", "dropped", "blocked", "deferred"} and graph.active_goal_id == goal.goal_id:
            next_active_goal_id = _fallback_active_goal_id(graph, exclude_goal_id=goal.goal_id)
        elif next_status == "active":
            next_active_goal_id = goal.goal_id

        next_graph = graph.transition_goal(
            goal.goal_id,
            status=next_status,
            revision_id=revision_id,
            updated_at=current,
            active_goal_id=next_active_goal_id,
            evidence_refs=evidence_refs,
            review_checkpoint=review_checkpoint,
        )
        if next_status == "active":
            next_graph = _ensure_single_active_goal(
                next_graph,
                goal_id=goal.goal_id,
                revision_id=revision_id,
                updated_at=current,
            )
        else:
            next_graph = _reassign_active_goal(
                next_graph,
                active_goal_id=next_active_goal_id,
                revision_id=revision_id,
                updated_at=current,
            )

        if next_graph == graph:
            return lifecycle(
                graph,
                changed=False,
                summary=f'Execution left "{goal.title}" unchanged in the durable graph.',
            )

        summary = f'Attached execution evidence to "{goal.title}".'
        if next_status != goal.status:
            summary = f'Updated "{goal.title}" to {next_status} after execution.'
        return lifecycle(
            next_graph,
            changed=True,
            summary=summary,
            updated_goal_ids=(goal.goal_id,),
        )

    def score_candidates(
        self,
        *,
        session: SessionState,
        graph: GoalGraph | ActivityGraph,
        memories: tuple[MemoryRecord, ...] = (),
        execution_tracker: ExecutionTracker | None = None,
        initiative_hint: str | None = None,
        continuity_notes: tuple[str, ...] = (),
        mode: PlanningMode = "guided",
        now: datetime | None = None,
    ) -> tuple[CandidateMove, ...]:
        graph = activity_graph_to_goal_graph(graph)
        current = _now() if now is None else now
        temporal = self._reasoner.analyze(session, graph, now=current)
        indexed = graph.index()
        candidates: list[CandidateMove] = []
        initiative = _normalize_initiative(initiative_hint)
        continuity_bonus = _INITIATIVE_CONTINUITY_BONUS.get(initiative, 0.0)
        note_bonus = _continuity_note_bonus(continuity_notes)
        note_factors = _continuity_note_factors(continuity_notes)

        for goal in graph.nodes:
            if goal.status in {"completed", "done", "failed", "dropped", "deferred"}:
                continue

            dependencies_ready = _dependencies_satisfied(goal, indexed)
            priority_score = _PRIORITY_POINTS[goal.priority]
            status_score = _STATUS_POINTS[goal.status]
            deadline_score = _deadline_score(goal.deadline, current)
            time_sensitivity_score = _TIME_SENSITIVITY_POINTS[goal.time_sensitivity]
            dependency_score = 0.6 if dependencies_ready else -1.0
            resume_score = 1.0 if temporal.resumed and goal.goal_id == temporal.active_goal_id else 0.0
            continuity_score = _continuity_score(goal, graph, temporal)
            if mode == "proactive" and goal.goal_id == temporal.active_goal_id:
                continuity_score = round(continuity_score + continuity_bonus, 3)
                if note_bonus > 0:
                    continuity_score = round(continuity_score + note_bonus, 3)
            if execution_tracker and goal.goal_id in execution_tracker.in_flight_goal_ids:
                resume_score += 0.7
            tracker_score = 0.5 if execution_tracker and goal.goal_id in execution_tracker.retry_goal_ids else 0.0
            evidence_score = 0.2 * len(goal.evidence_refs) + 0.15 * len(goal.related_memory_ids)
            repair_score = _repair_score(goal, temporal)
            staleness_score = _staleness_score(goal, temporal, current)

            kind = _kind_for_goal(goal, temporal, execution_tracker)
            replay = _replay_feedback_for(goal, kind=kind, memories=memories, temporal=temporal)
            score = (
                priority_score
                + status_score
                + deadline_score
                + time_sensitivity_score
                + dependency_score
                + resume_score
                + continuity_score
                + tracker_score
                + evidence_score
                + repair_score
                + staleness_score
                + replay.score
            )

            rationale, factors = _rationale_for(goal, temporal, kind, execution_tracker, now=current)
            if replay.summary:
                rationale = f"{rationale} {replay.summary}"
                factors = tuple((*factors, *replay.factors))
            if mode == "proactive" and goal.goal_id == temporal.active_goal_id and note_factors:
                factors = tuple((*factors, *note_factors))
            confidence = min(0.99, max(0.1, 0.2 + (priority_score / 5.0) + max(0.0, deadline_score)))
            if memories:
                confidence = min(0.99, confidence + min(0.1, 0.02 * len(memories)))
            if replay.score > 0:
                confidence = min(0.99, confidence + min(0.08, replay.score / 12.0))

            candidates.append(
                CandidateMove(
                    move_id=f"move:{session.session_id}:{goal.goal_id}",
                    kind=kind,
                    goal_id=goal.goal_id,
                    title=goal.title,
                    score=round(score, 3),
                    priority_score=priority_score,
                    status_score=status_score,
                    deadline_score=deadline_score,
                    time_sensitivity_score=time_sensitivity_score,
                    dependency_score=dependency_score,
                    resume_score=resume_score,
                    continuity_score=continuity_score,
                    tracker_score=tracker_score,
                    evidence_score=evidence_score,
                    repair_score=repair_score,
                    rationale=rationale,
                    rationale_factors=factors,
                    dependency_refs=goal.dependency_refs,
                    evidence_refs=goal.evidence_refs,
                    replay_score=replay.score,
                    replay_summary=replay.summary,
                    replay_refs=replay.refs,
                    confidence=round(confidence, 3),
                )
            )

        if not candidates:
            candidates.append(
                CandidateMove(
                    move_id=f"move:{session.session_id}:defer",
                    kind="defer_or_schedule",
                    goal_id=None,
                    title="Defer and schedule follow-up",
                    score=0.0,
                    priority_score=0.0,
                    status_score=0.0,
                    deadline_score=0.0,
                    time_sensitivity_score=0.0,
                    dependency_score=0.0,
                    resume_score=0.0,
                    continuity_score=0.0,
                    tracker_score=0.0,
                    evidence_score=0.0,
                    repair_score=0.0,
                    rationale="No actionable goals were available, so the planner should defer and schedule a follow-up.",
                    rationale_factors=(),
                    confidence=0.2,
                )
            )

        return tuple(sorted(candidates, key=lambda candidate: candidate.score, reverse=True))

    def choose_next_step(
        self,
        *,
        session: SessionState,
        graph: GoalGraph | ActivityGraph,
        memories: tuple[MemoryRecord, ...] = (),
        execution_tracker: ExecutionTracker | None = None,
        mode: PlanningMode = "guided",
        initiative_hint: str | None = None,
        continuity_notes: tuple[str, ...] = (),
        now: datetime | None = None,
    ) -> PlanningDecision:
        graph = activity_graph_to_goal_graph(graph)
        current = _now() if now is None else now
        initiative = _normalize_initiative(initiative_hint)
        continuity_bonus = _INITIATIVE_CONTINUITY_BONUS.get(initiative, 0.0)
        candidates = self.score_candidates(
            session=session,
            graph=graph,
            memories=memories,
            execution_tracker=execution_tracker,
            initiative_hint=initiative,
            continuity_notes=continuity_notes,
            mode=mode,
            now=current,
        )
        selected = candidates[0]
        temporal = self._reasoner.analyze(session, graph, now=current)
        selected_goal = graph.goal(selected.goal_id) if selected.goal_id is not None else None
        progression_action = _progression_action_for(selected.kind)
        planned_status, planned_active_goal_id = _planned_progression(graph, selected_goal, selected.kind)
        factors: list[str] = [
            f"mode={mode}",
            f"selected={selected.kind}",
            f"priority={selected.priority_score:.1f}",
            f"status={selected.status_score:.1f}",
            f"candidate-count={len(candidates)}",
        ]
        factors.extend(selected.rationale_factors)
        if temporal.resumed:
            factors.append("resumed-session")
        if selected.resume_score > 0:
            factors.append("resume-weighted")
        if selected.continuity_score > 0:
            factors.append("continuity-weighted")
        if selected_goal is not None and _staleness_score(selected_goal, temporal, current) > 0:
            factors.append("stale-goal-pressure")
        if selected.repair_score > 0:
            factors.append("repair-weighted")
        if selected.replay_score > 0:
            factors.append("replay-weighted")
        elif selected.replay_score < 0:
            factors.append("replay-caution")
        if selected.replay_refs:
            factors.append(f"replay-evidence-count={len(selected.replay_refs)}")
        if mode == "proactive":
            factors.append("wake-loop")
            if temporal.resumed:
                factors.append("proactive-resume")
            factors.append(f"initiative={initiative}")
            factors.extend(_continuity_note_factors(continuity_notes))
            if continuity_bonus != 0:
                factors.append("initiative-weighted")
            if _continuity_note_bonus(continuity_notes) > 0:
                factors.append("continuity-notes-weighted")
        if selected.deadline_score > 0:
            factors.append("deadline-pressure")
        if selected.time_sensitivity_score > 0:
            factors.append("time-sensitive")
        if selected.dependency_score < 0:
            factors.append("dependency-blocked")
        if selected.evidence_refs:
            factors.append("durable-evidence")
        if selected_goal is not None:
            factors.append(f"selected-goal-status={selected_goal.status}")
            factors.append(f"selected-goal-priority={selected_goal.priority}")
        if temporal.blocked_active_goal_id is not None:
            factors.append(f"blocked-active-goal={temporal.blocked_active_goal_id}")
        factors.append(f"progression={progression_action}")
        factors.append(f"planned-active-goal={planned_active_goal_id or '<none>'}")

        rationale = PlanningRationale(
            summary=f"{selected.rationale} {_progression_sentence(selected_goal, action=progression_action, planned_status=planned_status, planned_active_goal_id=planned_active_goal_id)}",
            factors=tuple(dict.fromkeys(factors)),
            candidate_ids=tuple(candidate.move_id for candidate in candidates),
            selected_move_id=selected.move_id,
            selected_goal_id=selected.goal_id,
            selected_goal_status=selected_goal.status if selected_goal is not None else None,
            selected_goal_priority=selected_goal.priority if selected_goal is not None else None,
            progression_action=progression_action,
            active_goal_id_before=graph.active_goal_id,
            planned_active_goal_id=planned_active_goal_id,
            mode=mode,
            replay_summary=selected.replay_summary,
            replay_evidence_refs=selected.replay_refs,
        )
        return PlanningDecision(
            decision_id=f"decision:{session.session_id}:{selected.goal_id or 'defer'}",
            session_id=session.session_id,
            mode=mode,
            selected_move=selected,
            rationale=rationale,
            candidates=candidates,
            temporal_context=temporal,
            goal_graph_revision=graph.updated_at,
        )

    def wake_next_step(
        self,
        *,
        session: SessionState,
        graph: GoalGraph | ActivityGraph,
        memories: tuple[MemoryRecord, ...] = (),
        execution_tracker: ExecutionTracker | None = None,
        initiative_hint: str | None = None,
        continuity_notes: tuple[str, ...] = (),
        now: datetime | None = None,
    ) -> tuple[PlanningDecision, GoalGraph]:
        graph = activity_graph_to_goal_graph(graph)
        decision = self.choose_next_step(
            session=session,
            graph=graph,
            memories=memories,
            execution_tracker=execution_tracker,
            mode="proactive",
            initiative_hint=initiative_hint,
            continuity_notes=continuity_notes,
            now=now,
        )
        return decision, apply_decision_to_goal_graph(graph, decision, updated_at=decision.selected_at)

    def emit_rationale(self, decision: PlanningDecision) -> EventEnvelope:
        payload = {
            "decision_id": decision.decision_id,
            "mode": decision.mode,
            "selected_move_id": decision.selected_move.move_id,
            "selected_goal_id": decision.selected_move.goal_id or "",
            "selected_kind": decision.selected_move.kind,
            "progression_action": decision.rationale.progression_action,
            "planned_active_goal_id": decision.rationale.planned_active_goal_id or "",
            "summary": decision.rationale.summary,
            "factors": _stringify(decision.rationale.factors),
            "candidate_ids": _stringify(decision.rationale.candidate_ids),
            "score": f"{decision.selected_move.score:.3f}",
            "replay_score": f"{decision.selected_move.replay_score:.3f}",
            "replay_summary": decision.rationale.replay_summary,
            "replay_evidence_refs": _stringify(decision.rationale.replay_evidence_refs),
            "resumed": str(decision.temporal_context.resumed),
        }
        return EventEnvelope(
            event_id=f"event:{decision.decision_id}:rationale",
            event_type="planning.rationale.emitted",
            session_id=decision.session_id,
            source="packages.planning",
            payload=payload,
        )
