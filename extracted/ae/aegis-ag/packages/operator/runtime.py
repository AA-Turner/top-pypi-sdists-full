"""Owner-aligned operator projections and shared surface wording for CSR-6."""

from __future__ import annotations

from dataclasses import dataclass
import re

from packages.context import ContextAssemblyResult
from packages.contracts import (
    CloneIdentityRecord,
    GoalNode,
    IntentDecision,
    MemoryRecord,
    ProcedureCandidate,
    ProcedureRecord,
    RelationshipMemoryRecord,
    UserCardRecord,
    VerificationBundle,
)

from .activity_rendering import render_activity_goal_tree_lines


@dataclass(frozen=True, slots=True)
class ProfileOperatorSurface:
    session_id: str
    profile_id: str
    profile_mode: str
    identity: CloneIdentityRecord
    user: UserCardRecord
    relationship: RelationshipMemoryRecord
    provenance: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ActivityOperatorSurface:
    session_id: str
    active_goal_id: str | None
    active_goal_reason: str
    wake_action: str
    wake_factors: tuple[str, ...]
    goal_graph_revision: str | None
    goals: tuple[GoalNode, ...]
    intent: "IntentOperatorDetail | None" = None


@dataclass(frozen=True, slots=True)
class IntentOperatorDetail:
    resolved_intent: str
    confidence: float
    focus_activity_ids: tuple[str, ...]
    opened_scopes: tuple[str, ...]
    scope_suggestion: str
    budget_class: str
    resume_signal: str
    embedding_status: str
    degradation_mode: str
    weak_assist_state: str
    fallback_path: str
    top_audit_reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class MemoryOperatorDetail:
    memory: MemoryRecord
    state: str | None
    lineage: str | None


@dataclass(frozen=True, slots=True)
class MemorySearchHit:
    memory: MemoryRecord
    score: float
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class MemoryOperatorSurface:
    session_id: str
    memories: tuple[MemoryOperatorDetail, ...]
    search_query: str | None = None
    search_hits: tuple[MemorySearchHit, ...] = ()
    scope_reason: str = ""
    index_policy: EmbeddingIndexPolicy | None = None


@dataclass(frozen=True, slots=True)
class ProcedureOperatorDetail:
    procedure: ProcedureRecord
    verification: VerificationBundle | None = None


@dataclass(frozen=True, slots=True)
class ProcedureOperatorSurface:
    session_id: str
    profile_id: str
    procedures: tuple[ProcedureOperatorDetail, ...]
    candidates: tuple[ProcedureCandidate, ...] = ()


@dataclass(frozen=True, slots=True)
class AuditSurface:
    session_id: str
    active_goal_id: str | None
    active_goal_reason: str
    intent: IntentOperatorDetail | None
    recalled_memory_ids: tuple[str, ...]
    retrieval_requests: tuple[str, ...]
    procedure_overlay_lines: tuple[str, ...]
    procedure_overlay_reason: str
    source_trace: tuple[str, ...]
    rendered_prompt: str


@dataclass(frozen=True, slots=True)
class DashboardMetric:
    label: str
    value: str
    note: str
    tone: str


@dataclass(frozen=True, slots=True)
class DashboardAlert:
    title: str
    detail: str
    tone: str


@dataclass(frozen=True, slots=True)
class DashboardTimelineEvent:
    label: str
    summary: str
    age: str
    tone: str


@dataclass(frozen=True, slots=True)
class DashboardProviderReadiness:
    status: str
    provider: str
    transport: str
    strong_model: str
    weak_model: str
    secret_status: str
    embedding_status: str
    summary: str
    tone: str


@dataclass(frozen=True, slots=True)
class DashboardHeartbeat:
    mode: str
    summary: str
    backlog: str
    scheduled_jobs: str
    last_success: str
    last_failure: str
    next_run: str
    tone: str


@dataclass(frozen=True, slots=True)
class DashboardProgressionRecord:
    title: str
    cycle: str
    level: str
    momentum: str
    challenge: str
    proof: str
    rollout: str
    fallback: str
    tone: str


@dataclass(frozen=True, slots=True)
class DashboardOverviewSurface:
    metrics: tuple[DashboardMetric, ...]
    alerts: tuple[DashboardAlert, ...]
    timeline: tuple[DashboardTimelineEvent, ...]
    provider: DashboardProviderReadiness | None = None
    heartbeat: DashboardHeartbeat | None = None
    progression: DashboardProgressionRecord | None = None


@dataclass(frozen=True, slots=True)
class DashboardCloneRecord:
    clone: str
    focus: str
    provider: str
    continuity: str
    last_contact: str
    tone: str
    details: tuple["DashboardDetailItem", ...] = ()

@dataclass(frozen=True, slots=True)
class DashboardDetailItem:
    label: str
    value: str


@dataclass(frozen=True, slots=True)
class DashboardMemoryLayer:
    layer: str
    owner: str
    freshness: str
    last_mutation: str
    volume: str
    provenance: str
    index_status: str
    note: str
    tone: str
    stats: tuple[DashboardDetailItem, ...] = ()


@dataclass(frozen=True, slots=True)
class DashboardGraphRecord:
    lane: str
    graph: str
    anchor: str
    focus: str
    state: str
    blocker: str
    support_path: str
    projection_health: str
    note: str
    tone: str
    stats: tuple[DashboardDetailItem, ...] = ()
    sources: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DashboardSessionRecord:
    thread: str
    conversation: str
    log: str
    model: str
    tokens: str
    usage: str
    continuity: str
    last_touch: str
    tone: str
    details: tuple[DashboardDetailItem, ...] = ()

@dataclass(frozen=True, slots=True)
class DashboardOpsRecord:
    lane: str
    event: str
    source: str
    summary: str
    outcome: str
    age: str
    tone: str


@dataclass(frozen=True, slots=True)
class DashboardCapabilityRecord:
    capability: str
    source: str
    state: str
    provenance: str
    note: str
    tone: str
    details: tuple[DashboardDetailItem, ...] = ()


@dataclass(frozen=True, slots=True)
class DashboardProviderProfileRecord:
    provider: str
    profile: str
    state: str
    auth: str
    model: str
    note: str
    tone: str
    details: tuple[DashboardDetailItem, ...] = ()


@dataclass(frozen=True, slots=True)
class DashboardControlRecord:
    control: str
    surface: str
    state: str
    boundary: str
    note: str
    tone: str
    details: tuple[DashboardDetailItem, ...] = ()


@dataclass(frozen=True, slots=True)
class DashboardMeta:
    scenario: str
    source_label: str
    shell_status: str
    generated_at: str
    note: str
    query_contract: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DashboardSurface:
    meta: DashboardMeta
    overview: DashboardOverviewSurface
    clones: tuple[DashboardCloneRecord, ...] = ()
    memory_layers: tuple[DashboardMemoryLayer, ...] = ()
    graphs: tuple[DashboardGraphRecord, ...] = ()
    sessions: tuple[DashboardSessionRecord, ...] = ()
    ops: tuple[DashboardOpsRecord, ...] = ()
    capabilities: tuple[DashboardCapabilityRecord, ...] = ()
    provider_profiles: tuple[DashboardProviderProfileRecord, ...] = ()
    controls: tuple[DashboardControlRecord, ...] = ()


DEFAULT_DASHBOARD_QUERY_CONTRACT = (
    "Read-first shell over canonical runtime state; the dashboard is not a source of truth.",
    "Default 30-second polling with a manual refresh and visible projection time.",
    "The product dashboard only renders live local operator state; unavailable, empty, stale, and degraded states stay visible as real states.",
)


def build_profile_operator_surface(
    *,
    session_id: str,
    profile_id: str,
    profile_mode: str,
    identity: CloneIdentityRecord,
    user: UserCardRecord,
    relationship: RelationshipMemoryRecord,
    provenance: tuple[str, ...] = (),
) -> ProfileOperatorSurface:
    return ProfileOperatorSurface(
        session_id=session_id,
        profile_id=profile_id,
        profile_mode=profile_mode,
        identity=identity,
        user=user,
        relationship=relationship,
        provenance=provenance or ("ProfileGraph.identity", "ProfileGraph.user", "ProfileGraph.relationship"),
    )


def build_activity_operator_surface(
    *,
    session_id: str,
    active_goal_id: str | None,
    active_goal_reason: str,
    wake_action: str,
    wake_factors: tuple[str, ...],
    goal_graph_revision: str | None,
    goals: tuple[GoalNode, ...],
    intent: IntentDecision | None = None,
    opened_scopes: tuple[str, ...] = (),
    embedding_status: str | None = None,
) -> ActivityOperatorSurface:
    return ActivityOperatorSurface(
        session_id=session_id,
        active_goal_id=active_goal_id,
        active_goal_reason=active_goal_reason,
        wake_action=wake_action,
        wake_factors=wake_factors,
        goal_graph_revision=goal_graph_revision,
        goals=goals,
        intent=_build_intent_operator_detail(
            intent,
            opened_scopes=opened_scopes,
            embedding_status=embedding_status,
        ),
    )


def build_memory_operator_surface(
    *,
    session_id: str,
    memories: tuple[MemoryOperatorDetail, ...],
    search_query: str | None = None,
    search_hits: tuple[MemorySearchHit, ...] = (),
    scope_reason: str = "",
    index_policy: EmbeddingIndexPolicy | None = None,
) -> MemoryOperatorSurface:
    return MemoryOperatorSurface(
        session_id=session_id,
        memories=memories,
        search_query=search_query,
        search_hits=search_hits,
        scope_reason=scope_reason,
        index_policy=index_policy,
    )


def build_procedure_operator_surface(
    *,
    session_id: str,
    profile_id: str,
    procedures: tuple[ProcedureOperatorDetail, ...],
    candidates: tuple[ProcedureCandidate, ...] = (),
) -> ProcedureOperatorSurface:
    return ProcedureOperatorSurface(
        session_id=session_id,
        profile_id=profile_id,
        procedures=procedures,
        candidates=candidates,
    )


def build_audit_surface(
    *,
    session_id: str,
    active_goal_id: str | None,
    active_goal_reason: str,
    context_result: ContextAssemblyResult,
    intent: IntentDecision | None = None,
    opened_scopes: tuple[str, ...] = (),
    embedding_status: str | None = None,
) -> AuditSurface:
    procedure_overlay_reason = next(
        (
            trace.reason
            for trace in context_result.source_trace
            if trace.layer_name == "procedure_overlay"
        ),
        "no procedure overlay was needed",
    )
    retrieval_requests = tuple(
        f"{request.request_id}: {', '.join(request.memory_ids) or 'none'} | {request.reason}"
        for request in context_result.plan.retrieval_requests
    )
    procedure_overlay_lines = (
        context_result.frame.procedure_overlay.content
        if context_result.frame is not None
        else ("no active procedure overlay",)
    )
    return AuditSurface(
        session_id=session_id,
        active_goal_id=active_goal_id,
        active_goal_reason=active_goal_reason,
        intent=_build_intent_operator_detail(
            intent,
            opened_scopes=opened_scopes,
            embedding_status=embedding_status,
        ),
        recalled_memory_ids=context_result.retrieved_memory_ids,
        retrieval_requests=retrieval_requests,
        procedure_overlay_lines=procedure_overlay_lines,
        procedure_overlay_reason=procedure_overlay_reason,
        source_trace=tuple(trace.describe() for trace in context_result.source_trace),
        rendered_prompt=context_result.rendered_prompt,
    )


def build_dashboard_surface(
    *,
    scenario: str,
    source_label: str,
    shell_status: str,
    generated_at: str,
    note: str,
    metrics: tuple[DashboardMetric, ...],
    alerts: tuple[DashboardAlert, ...],
    timeline: tuple[DashboardTimelineEvent, ...],
    clones: tuple[DashboardCloneRecord, ...],
    memory_layers: tuple[DashboardMemoryLayer, ...] = (),
    graphs: tuple[DashboardGraphRecord, ...] = (),
    sessions: tuple[DashboardSessionRecord, ...] = (),
    ops: tuple[DashboardOpsRecord, ...] = (),
    capabilities: tuple[DashboardCapabilityRecord, ...] = (),
    provider_profiles: tuple[DashboardProviderProfileRecord, ...] = (),
    controls: tuple[DashboardControlRecord, ...] = (),
    provider: DashboardProviderReadiness | None = None,
    heartbeat: DashboardHeartbeat | None = None,
    progression: DashboardProgressionRecord | None = None,
    query_contract: tuple[str, ...] = (),
) -> DashboardSurface:
    return DashboardSurface(
        meta=DashboardMeta(
            scenario=scenario,
            source_label=source_label,
            shell_status=shell_status,
            generated_at=generated_at,
            note=note,
            query_contract=query_contract or DEFAULT_DASHBOARD_QUERY_CONTRACT,
        ),
        overview=DashboardOverviewSurface(
            metrics=metrics,
            alerts=alerts,
            timeline=timeline,
            provider=provider,
            heartbeat=heartbeat,
            progression=progression,
        ),
        clones=clones,
        memory_layers=memory_layers,
        graphs=graphs,
        sessions=sessions,
        ops=ops,
        capabilities=capabilities,
        provider_profiles=provider_profiles,
        controls=controls,
    )


def dashboard_surface_record(surface: DashboardSurface) -> dict[str, object]:
    provider = surface.overview.provider
    heartbeat = surface.overview.heartbeat
    progression = surface.overview.progression
    return {
        "meta": {
            "scenario": surface.meta.scenario,
            "sourceLabel": surface.meta.source_label,
            "shellStatus": surface.meta.shell_status,
            "generatedAt": surface.meta.generated_at,
            "note": surface.meta.note,
            "queryContract": list(surface.meta.query_contract),
        },
        "overview": {
            "metrics": [
                {
                    "label": metric.label,
                    "value": metric.value,
                    "note": metric.note,
                    "tone": metric.tone,
                }
                for metric in surface.overview.metrics
            ],
            "alerts": [
                {
                    "title": alert.title,
                    "detail": alert.detail,
                    "tone": alert.tone,
                }
                for alert in surface.overview.alerts
            ],
            "timeline": [
                {
                    "label": event.label,
                    "summary": event.summary,
                    "age": event.age,
                    "tone": event.tone,
                }
                for event in surface.overview.timeline
            ],
            "provider": (
                {
                    "status": provider.status,
                    "provider": provider.provider,
                    "transport": provider.transport,
                    "strongModel": provider.strong_model,
                    "weakModel": provider.weak_model,
                    "secretStatus": provider.secret_status,
                    "embeddingStatus": provider.embedding_status,
                    "summary": provider.summary,
                    "tone": provider.tone,
                }
                if provider is not None
                else None
            ),
            "heartbeat": (
                {
                    "mode": heartbeat.mode,
                    "summary": heartbeat.summary,
                    "backlog": heartbeat.backlog,
                    "scheduledJobs": heartbeat.scheduled_jobs,
                    "lastSuccess": heartbeat.last_success,
                    "lastFailure": heartbeat.last_failure,
                    "nextRun": heartbeat.next_run,
                    "tone": heartbeat.tone,
                }
                if heartbeat is not None
                else None
            ),
            "progression": (
                {
                    "title": progression.title,
                    "cycle": progression.cycle,
                    "level": progression.level,
                    "momentum": progression.momentum,
                    "challenge": progression.challenge,
                    "proof": progression.proof,
                    "rollout": progression.rollout,
                    "fallback": progression.fallback,
                    "tone": progression.tone,
                }
                if progression is not None
                else None
            ),
        },
        "clones": [
            {
                "clone": clone.clone,
                "focus": clone.focus,
                "provider": clone.provider,
                "continuity": clone.continuity,
                "lastContact": clone.last_contact,
                "tone": clone.tone,
                "details": [
                    {
                        "label": item.label,
                        "value": item.value,
                    }
                    for item in clone.details
                ],
            }
            for clone in surface.clones
        ],
        "memoryLayers": [
            {
                "layer": layer.layer,
                "owner": layer.owner,
                "freshness": layer.freshness,
                "lastMutation": layer.last_mutation,
                "volume": layer.volume,
                "provenance": layer.provenance,
                "indexStatus": layer.index_status,
                "note": layer.note,
                "tone": layer.tone,
                "stats": [
                    {
                        "label": item.label,
                        "value": item.value,
                    }
                    for item in layer.stats
                ],
            }
            for layer in surface.memory_layers
        ],
        "graphs": [
            {
                "lane": graph.lane,
                "graph": graph.graph,
                "anchor": graph.anchor,
                "focus": graph.focus,
                "state": graph.state,
                "blocker": graph.blocker,
                "supportPath": graph.support_path,
                "projectionHealth": graph.projection_health,
                "note": graph.note,
                "tone": graph.tone,
                "stats": [
                    {
                        "label": item.label,
                        "value": item.value,
                    }
                    for item in graph.stats
                ],
                "sources": list(graph.sources),
            }
            for graph in surface.graphs
        ],
        "sessions": [
            {
                "thread": session.thread,
                "conversation": session.conversation,
                "log": session.log,
                "model": session.model,
                "tokens": session.tokens,
                "usage": session.usage,
                "continuity": session.continuity,
                "lastTouch": session.last_touch,
                "tone": session.tone,
                "details": [
                    {
                        "label": item.label,
                        "value": item.value,
                    }
                    for item in session.details
                ],
            }
            for session in surface.sessions
        ],
        "ops": [
            {
                "lane": event.lane,
                "event": event.event,
                "source": event.source,
                "summary": event.summary,
                "outcome": event.outcome,
                "age": event.age,
                "tone": event.tone,
            }
            for event in surface.ops
        ],
        "capabilities": [
            {
                "capability": capability.capability,
                "source": capability.source,
                "state": capability.state,
                "provenance": capability.provenance,
                "note": capability.note,
                "tone": capability.tone,
                "details": [
                    {
                        "label": item.label,
                        "value": item.value,
                    }
                    for item in capability.details
                ],
            }
            for capability in surface.capabilities
        ],
        "providerProfiles": [
            {
                "provider": provider_profile.provider,
                "profile": provider_profile.profile,
                "state": provider_profile.state,
                "auth": provider_profile.auth,
                "model": provider_profile.model,
                "note": provider_profile.note,
                "tone": provider_profile.tone,
                "details": [
                    {
                        "label": item.label,
                        "value": item.value,
                    }
                    for item in provider_profile.details
                ],
            }
            for provider_profile in surface.provider_profiles
        ],
        "controls": [
            {
                "control": control.control,
                "surface": control.surface,
                "state": control.state,
                "boundary": control.boundary,
                "note": control.note,
                "tone": control.tone,
                "details": [
                    {
                        "label": item.label,
                        "value": item.value,
                    }
                    for item in control.details
                ],
            }
            for control in surface.controls
        ],
    }


def library_procedure_overlays(
    *,
    goals: tuple[GoalNode, ...],
    procedures: tuple[ProcedureRecord, ...],
    limit: int = 2,
) -> tuple[str, ...]:
    goal_ids = {goal.goal_id for goal in goals}
    goal_tokens = {
        token
        for goal in goals
        for token in _tokenize(f"{goal.title} {' '.join(goal.evidence_refs)}")
    }
    ranked: list[tuple[float, ProcedureRecord]] = []
    for procedure in procedures:
        if procedure.status not in {"active", "verified", "promoted"}:
            continue
        score = 0.0
        procedure_tokens = _tokenize(f"{procedure.title} {procedure.summary} {' '.join(procedure.trigger_refs)}")
        trigger_goal_ids = {
            trigger.split(":", 1)[1]
            for trigger in procedure.trigger_refs
            if trigger.startswith("goal:") and ":" in trigger
        }
        if goal_ids and goal_ids.intersection(trigger_goal_ids):
            score += 2.5
        if goal_tokens and goal_tokens.intersection(procedure_tokens):
            score += 1.0
        if score > 0.0:
            ranked.append((score, procedure))
    ranked.sort(key=lambda item: (-item[0], item[1].procedure_id))
    overlays: list[str] = []
    for _, procedure in ranked[:limit]:
        step_preview = "; ".join(step.instruction for step in procedure.steps[:2]) or procedure.summary
        overlays.append(
            f"procedure.{procedure.procedure_id}: {procedure.title} | "
            f"verified={procedure.verification_bundle_id or 'missing'} | "
            f"{_compact_text(step_preview, limit=360)}"
        )
    return tuple(overlays)


def render_profile_lines(surface: ProfileOperatorSurface) -> tuple[str, ...]:
    return (
        f"profile_id: {surface.profile_id}",
        f"profile_mode: {surface.profile_mode}",
        f"identity_display_name: {surface.identity.display_name}",
        f"identity_preset: {surface.identity.personality_preset}",
        f"identity_initiative: {surface.identity.initiative}",
        f"user_preferred_name: {surface.user.preferred_name or '<empty>'}",
        f"user_biography_fragments: {', '.join(surface.user.biography_fragments) or '<empty>'}",
        f"user_durable_notes: {', '.join(surface.user.durable_notes) or '<empty>'}",
        f"user_shared_preferences: {', '.join(surface.user.shared_preferences) or '<empty>'}",
        f"relationship_notes: {', '.join(surface.relationship.continuity_notes) or '<empty>'}",
        f"provenance: {', '.join(surface.provenance)}",
    )


def render_activity_lines(surface: ActivityOperatorSurface) -> tuple[str, ...]:
    goal_lines = render_activity_goal_tree_lines(surface.goals)
    lines = [
        f"active_goal_id: {surface.active_goal_id or '<none>'}",
        f"active_goal_reason: {surface.active_goal_reason}",
        f"wake_action: {surface.wake_action}",
        f"wake_factors: {', '.join(surface.wake_factors) or '<none>'}",
        f"goal_graph_revision: {surface.goal_graph_revision or '<none>'}",
    ]
    lines.extend(_render_intent_lines(surface.intent))
    lines.extend(("goals:", *goal_lines))
    return tuple(lines)


def render_memory_lines(surface: MemoryOperatorSurface) -> tuple[str, ...]:
    lines: list[str] = []
    for item in surface.memories:
        lines.append(
            f"{item.memory.memory_id} | state={item.state or 'active'} | lineage={item.lineage or 'none'} | "
            f"tags={', '.join(item.memory.tags) or 'none'} | {item.memory.kind} | {item.memory.content}"
        )
    if not lines:
        lines.append("<empty>")
    if surface.search_query is not None:
        lines.extend(("", f"search_query: {surface.search_query}", f"scope_reason: {surface.scope_reason or '<none>'}"))
        for hit in surface.search_hits:
            lines.append(
                f"- {hit.memory.memory_id} | score={hit.score:.2f} | reasons={'; '.join(hit.reasons) or '<none>'} | {hit.memory.content}"
            )
    return tuple(lines)


def render_procedure_lines(surface: ProcedureOperatorSurface) -> tuple[str, ...]:
    lines = [f"profile_id: {surface.profile_id}", f"candidate_count: {len(surface.candidates)}", f"procedure_count: {len(surface.procedures)}"]
    if surface.candidates:
        lines.append("candidates:")
        lines.extend(
            f"- {candidate.candidate_id} | support={len(candidate.source_evidence_ids)} | confidence={candidate.confidence:.2f} | {candidate.title}"
            for candidate in surface.candidates
        )
    if surface.procedures:
        lines.append("procedures:")
        lines.extend(
            f"- {detail.procedure.procedure_id} | {detail.procedure.status} | verification={detail.procedure.verification_bundle_id or 'missing'} | skill={detail.procedure.skill_id or 'none'} | {detail.procedure.title}"
            for detail in surface.procedures
        )
    if len(lines) == 3:
        lines.append("<empty>")
    return tuple(lines)


def render_audit_lines(surface: AuditSurface) -> tuple[str, ...]:
    lines = [
        f"active_goal_id: {surface.active_goal_id or '<none>'}",
        f"active_goal_reason: {surface.active_goal_reason}",
        *_render_intent_lines(surface.intent),
        f"recalled_memory_ids: {', '.join(surface.recalled_memory_ids) or '<none>'}",
        f"procedure_overlay_reason: {surface.procedure_overlay_reason}",
        "procedure_overlay:",
        *tuple(f"- {line}" for line in (surface.procedure_overlay_lines or ("no active procedure overlay",))),
        "retrieval_requests:",
        *tuple(f"- {line}" for line in (surface.retrieval_requests or ("none",))),
        "source_trace:",
        *tuple(f"- {line}" for line in surface.source_trace),
    ]
    return tuple(lines)


def _tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[A-Za-z0-9_]+", text.lower()) if token}


def _compact_text(text: str, *, limit: int) -> str:
    normalized = " ".join(text.split()).strip()
    if len(normalized) <= limit:
        return normalized
    return normalized[: max(0, limit - 1)].rstrip() + "…"


def _build_intent_operator_detail(
    intent: IntentDecision | None,
    *,
    opened_scopes: tuple[str, ...],
    embedding_status: str | None,
) -> IntentOperatorDetail | None:
    if intent is None:
        return None
    return IntentOperatorDetail(
        resolved_intent=intent.intent,
        confidence=intent.confidence,
        focus_activity_ids=intent.focus_activity_ids,
        opened_scopes=tuple(dict.fromkeys(scope for scope in opened_scopes if scope)) or ("session",),
        scope_suggestion=intent.scope_suggestion,
        budget_class=intent.budget_class,
        resume_signal=intent.resume_signal,
        embedding_status=_resolve_embedding_status(intent, explicit_status=embedding_status),
        degradation_mode=intent.degradation_mode,
        weak_assist_state=_weak_assist_state(intent),
        fallback_path=intent.fallback_path,
        top_audit_reasons=_top_audit_reasons(intent),
    )


def _resolve_embedding_status(intent: IntentDecision, *, explicit_status: str | None) -> str:
    status = str(explicit_status or "").strip().lower()
    if intent.embedding_available:
        return "ready"
    if intent.degradation_mode == "skip":
        return "skipped"
    if status in {"ready", "skipped", "pending", "downloading", "failed"}:
        return status
    if intent.degradation_mode == "embedding-unavailable":
        return "unavailable"
    return status or "not-used"


def _weak_assist_state(intent: IntentDecision) -> str:
    if not intent.needs_weak_model_assist:
        return "not-requested"
    if intent.weak_assist_outcome != "not-requested":
        return intent.weak_assist_outcome
    return "requested"


def _top_audit_reasons(intent: IntentDecision, *, limit: int = 3) -> tuple[str, ...]:
    if intent.reasons:
        ranked = sorted(intent.reasons, key=lambda item: item.weight, reverse=True)
        return tuple(
            f"{reason.code} | {_compact_text(reason.detail, limit=120)}"
            for reason in ranked[:limit]
        )
    return tuple(_compact_text(line, limit=120) for line in intent.audit_trace[:limit])


def _render_intent_lines(intent: IntentOperatorDetail | None) -> tuple[str, ...]:
    if intent is None:
        return (
            "resolved_intent: <none>",
            "focus_activity_ids: <none>",
            "opened_scopes: <none>",
            "fallback_path: <none>",
        )
    lines = [
        f"resolved_intent: {intent.resolved_intent}",
        f"intent_confidence: {intent.confidence:.2f}",
        f"focus_activity_ids: {', '.join(intent.focus_activity_ids) or '<none>'}",
        f"opened_scopes: {', '.join(intent.opened_scopes) or '<none>'}",
        f"scope_suggestion: {intent.scope_suggestion}",
        f"budget_class: {intent.budget_class}",
        f"resume_signal: {intent.resume_signal}",
        f"embedding_status: {intent.embedding_status}",
        f"degradation_mode: {intent.degradation_mode}",
        f"weak_assist_state: {intent.weak_assist_state}",
        f"fallback_path: {intent.fallback_path}",
    ]
    if intent.top_audit_reasons:
        lines.append("top_audit_reasons:")
        lines.extend(f"- {reason}" for reason in intent.top_audit_reasons)
    return tuple(lines)


__all__ = [
    "AuditSurface",
    "DashboardAlert",
    "DashboardCloneRecord",
    "DashboardDetailItem",
    "DashboardHeartbeat",
    "DashboardGraphRecord",
    "DashboardMemoryLayer",
    "DashboardMeta",
    "DashboardMetric",
    "DashboardOpsRecord",
    "DashboardOverviewSurface",
    "DashboardProgressionRecord",
    "DashboardProviderReadiness",
    "DashboardSessionRecord",
    "DashboardSurface",
    "DashboardTimelineEvent",
    "IntentOperatorDetail",
    "MemoryOperatorDetail",
    "MemoryOperatorSurface",
    "MemorySearchHit",
    "ProcedureOperatorDetail",
    "ProcedureOperatorSurface",
    "ProfileOperatorSurface",
    "ActivityOperatorSurface",
    "build_audit_surface",
    "build_dashboard_surface",
    "build_memory_operator_surface",
    "build_procedure_operator_surface",
    "build_profile_operator_surface",
    "build_activity_operator_surface",
    "dashboard_surface_record",
    "library_procedure_overlays",
    "render_audit_lines",
    "render_memory_lines",
    "render_procedure_lines",
    "render_profile_lines",
    "render_activity_lines",
]
