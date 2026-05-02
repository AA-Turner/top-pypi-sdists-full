"""Session and inspection methods for the API runtime app."""
from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass, replace
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version as package_version
from pathlib import Path
import json
from typing import Any, Mapping
from uuid import uuid4

from apps.provider_runtime import SurfaceModelProviderCapability, provider_selection_from_payload
from packages.auth import AuthProfile, PersistentAuthProfileStore
from packages.context import ContextRuntime
from packages.contracts import ContextBundle, EventEnvelope, ExecutionResult, GoalNode, MemoryRecord, ProfileState, SessionState, ActivityGraph
from packages.kernel import KernelDependencies, KernelOutcome, KernelService, KernelTurnRequest, ObservationPipeline, StateReconciler
from packages.learning import LearningRuntime
from packages.evidence import MemoryRuntime
from packages.kernel.memory_recovery import memory_retrieval_scopes
from packages.operator import (
    DashboardAlert, DashboardCloneRecord, DashboardDetailItem, DashboardHeartbeat, DashboardMetric,
    DashboardProviderReadiness, DashboardTimelineEvent, MemoryOperatorDetail, MemorySearchHit,
    ProcedureOperatorDetail, build_activity_operator_surface, build_audit_surface, build_dashboard_surface,
    build_memory_operator_surface, build_procedure_operator_surface, build_profile_operator_surface,
    dashboard_surface_record, library_procedure_overlays,
)
from packages.planning import PlanningService
from packages.session import SessionLineageService, SessionResumeResult
from packages.storage import RuntimeStorageRepository
from packages.tools import BuiltinToolDependencies, build_tool_runtime
from packages.tools.adapters import DeliveryMessageSurfaceAdapter, StructuredClarifySurface
from packages.tools.browser_backend import create_playwright_browser_backend

from .capabilities import APIContextCapability, APIDeliveryCapability, APIMemoryCapability, APIModelProvider, APIPlanningCapability, APITelemetrySink, APIToolExecution
from .state_runtime import APIContinuityInspection, APIStateService
from .tool_surfaces import APIMemoryManagementSurface

from .api_runtime_support import (
    APIAppConfig,
    APIResponse,
    APISessionCreationResult,
    APISessionInspection,
    APISessionLifecycleResult,
    APIResumeResult,
    APITurnRecord,
    APITurnResult,
    _coerce_str_tuple,
    _json_bytes,
    _jsonable,
    _now,
    _optional_bool,
    _optional_datetime,
    _optional_str,
    _read_json_bytes,
    _split_path,
)
from .api_runtime_dashboard_capabilities import build_dashboard_capability_registry
from .api_runtime_dashboard_memory_layers import build_dashboard_memory_layers
from .api_runtime_dashboard_graphs import build_dashboard_graphs, load_dashboard_activity_graph
from .api_runtime_dashboard_progression import build_dashboard_progression, build_progression_projection, progression_metric_note
from .api_runtime_dashboard_observability import (
    _compact_provider_label, _dashboard_clone_rows, _display_timestamp, _provider_tone, _relative_age,
    _session_status_counts, _tone_for_status, build_dashboard_observability, dashboard_graph_session_ids,
)
def _latest_turn_record(self, session_id: str):
    turns = self._turns.get(session_id, ())
    return turns[-1] if turns else None


def _latest_turn_intent(self, session_id: str):
    latest_turn = _latest_turn_record(self, session_id)
    return latest_turn.outcome.intent if latest_turn is not None else None


def _embedding_status(self) -> str | None:
    status = str(self.model_provider.describe().get("embedding_bootstrap_status") or "").strip()
    return status or None


def _opened_scopes_for_session(self, session_id: str, *, session: SessionState, graph: ActivityGraph | None):
    intent = _latest_turn_intent(self, session_id)
    if intent is None:
        return ()
    continuity = self.session_lineage.continuity_state(
        session,
        lineage=self.repository.lineage(session_id),
        active_goal_id=graph.active_goal_id if graph is not None else None,
    )
    return memory_retrieval_scopes(session, continuity=continuity, intent=intent)


def _resolve_aegis_version() -> str:
    try:
        return package_version("aegis-ag")
    except PackageNotFoundError:
        pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
        if pyproject.exists():
            for raw in pyproject.read_text(encoding="utf-8").splitlines():
                stripped = raw.strip()
                if stripped.startswith("version = "):
                    return stripped.split("=", 1)[1].strip().strip('"')
        return "dev"


def _dashboard_status_label(status: object) -> str:
    normalized = str(status or "").strip()
    if not normalized:
        return "unknown"
    if normalized.casefold() == "preview":
        return "needs setup"
    return normalized


def _dashboard_config_label(value: object, *, fallback: str = "not configured") -> str:
    normalized = str(value or "").strip()
    if not normalized or normalized.casefold() == "preview":
        return fallback
    return normalized


def create_session(
    self,
    *,
    profile_id: str,
    display_name: str,
    mode: str,
    workspace_id: str | None = None,
    clone_path: str | None = None,
    preferences: tuple[str, ...] = (),
    enabled_capabilities: tuple[str, ...] = (),
    provider_profile: Mapping[str, Any] | None = None,
    session_id: str | None = None,
) -> APISessionCreationResult:
    profile = ProfileState(
        profile_id=profile_id,
        display_name=display_name,
        mode=mode,
        clone_path=clone_path,
        preferences=preferences,
        enabled_capabilities=enabled_capabilities,
    )
    if provider_profile is not None:
        selection = provider_selection_from_payload(provider_profile)
        active_profile = selection.strong_profile
        weak_profile = selection.weak_profile
        if active_profile is None or weak_profile is None:
            raise ValueError("provider_profile must include strong_profile and weak_profile objects")
        self.auth_store.register(active_profile)
        self.auth_store.register(weak_profile)
        self.model_provider.set_active_profiles(
            strong_provider_profile_id=active_profile.profile_id,
            weak_provider_profile_id=weak_profile.profile_id,
            provider_id=active_profile.provider_id,
            intent_mode=selection.intent_mode,
        )
    elif self.model_provider.active_profile() is None and self.auth_store.list():
        active_profile = self.auth_store.list()[0]
        self.model_provider.set_active_profiles(
            strong_provider_profile_id=active_profile.profile_id,
            weak_provider_profile_id=active_profile.profile_id,
            provider_id=active_profile.provider_id,
        )
    session = self.session_lineage.start_session(
        profile,
        workspace_id=workspace_id,
        session_id=session_id,
    )
    self.personal_state.ensure_profile_state(profile, sync_source="api.create-session")
    return APISessionCreationResult(profile=profile, session=session)

def interrupt_session(self, session_id: str, *, interruption_state: str) -> APISessionLifecycleResult:
    session = self.session_lineage.interrupt_session(session_id, interruption_state=interruption_state)
    return APISessionLifecycleResult(session=session)

def resume_session(self, session_id: str, *, child_session_id: str | None = None) -> APIResumeResult:
    result: SessionResumeResult = self.session_lineage.resume_session(
        session_id,
        child_session_id=child_session_id,
    )
    return APIResumeResult(parent=result.parent, session=result.session, lineage=result.lineage)

def _load_activity_graph(self, session_id: str) -> ActivityGraph:
    graph = self.repository.load_activity_graph(session_id)
    if graph is None:
        raise KeyError(session_id)
    return graph

def list_goals(self, session_id: str) -> tuple[GoalNode, ...]:
    graph = self.repository.load_activity_graph(session_id)
    if graph is None:
        return ()
    return graph.goals

def list_memories(self, session_id: str) -> tuple[MemoryRecord, ...]:
    return tuple(self.memory_runtime.store.list(session_id=session_id))

def inspect_identity(self, *, session_id: str | None = None, profile_id: str | None = None):
    return self.personal_state.inspect_identity(session_id=session_id, profile_id=profile_id)

def update_identity_state(
    self,
    *,
    session_id: str | None = None,
    profile_id: str | None = None,
    display_name: str | None = None,
    personality_preset: str | None = None,
    initiative: str | None = None,
    charter_text: str | None = None,
    clear_charter: bool = False,
):
    return self.personal_state.update_identity_state(
        session_id=session_id,
        profile_id=profile_id,
        display_name=display_name,
        personality_preset=personality_preset,
        initiative=initiative,
        charter_text=charter_text,
        clear_charter=clear_charter,
    )

def inspect_user(self, *, session_id: str | None = None, profile_id: str | None = None):
    return self.personal_state.inspect_user(session_id=session_id, profile_id=profile_id)

def update_user_state(
    self,
    *,
    session_id: str | None = None,
    profile_id: str | None = None,
    text: str | None = None,
    fields: dict[str, object] | None = None,
    append: bool = False,
    clear: bool = False,
):
    return self.personal_state.update_user_state(
        session_id=session_id,
        profile_id=profile_id,
        text=text,
        fields=fields,
        append=append,
        clear=clear,
    )

def inspect_relationship(self, *, session_id: str | None = None, profile_id: str | None = None):
    return self.personal_state.inspect_relationship(session_id=session_id, profile_id=profile_id)

def update_relationship_state(
    self,
    *,
    session_id: str | None = None,
    profile_id: str | None = None,
    text: str | None = None,
    append: bool = False,
    clear: bool = False,
):
    return self.personal_state.update_relationship_state(
        session_id=session_id,
        profile_id=profile_id,
        text=text,
        append=append,
        clear=clear,
    )

def inspect_continuity(self, session_id: str) -> APIContinuityInspection:
    return self.personal_state.inspect_continuity(session_id)

def inspect_context_frame(self, session_id: str):
    session = self.repository.load_session(session_id)
    if session is None:
        raise KeyError(session_id)
    goals = self.list_goals(session_id)
    memories = self.list_memories(session_id)
    latest_turn = _latest_turn_record(self, session_id)
    hot_turns = tuple(
        part
        for part in (
            str(latest_turn.request.get("prompt") or "").strip() if latest_turn is not None else "",
            latest_turn.outcome.execution.summary.strip() if latest_turn is not None else "",
        )
        if part
    )
    library = self.repository.load_procedure_library(session.profile_id)
    procedure_overlays = library_procedure_overlays(
        goals=goals,
        procedures=library.procedures if library is not None else (),
    )
    return self.context_runtime.assemble_detailed(
        session,
        goals,
        memories,
        hot_turns=hot_turns,
        profile_snapshot_refs=(
            f"profile:{session.profile_id}:identity",
            f"profile:{session.profile_id}:user",
            f"profile:{session.profile_id}:relationship",
        ),
        procedure_overlays=procedure_overlays,
        intent=latest_turn.outcome.intent if latest_turn is not None else None,
    )

def inspect_profile_surface(self, session_id: str):
    session = self.repository.load_session(session_id)
    if session is None:
        raise KeyError(session_id)
    profile = self.repository.load_profile(session.profile_id)
    if profile is None:
        raise KeyError(session.profile_id)
    return build_profile_operator_surface(
        session_id=session_id,
        profile_id=profile.profile_id,
        profile_mode=profile.mode,
        identity=self.inspect_identity(session_id=session_id),
        user=self.inspect_user(session_id=session_id),
        relationship=self.inspect_relationship(session_id=session_id),
    )

def patch_profile_surface(self, session_id: str, payload: Mapping[str, Any]):
    if any(key in payload for key in {"display_name", "name", "personality_preset", "initiative", "charter_text", "text", "content", "clear_charter"}):
        self.update_identity_state(
            session_id=session_id,
            display_name=_optional_str(payload.get("display_name") or payload.get("name")),
            personality_preset=_optional_str(payload.get("personality_preset")),
            initiative=_optional_str(payload.get("initiative")),
            charter_text=_optional_str(payload.get("charter_text") or payload.get("text") or payload.get("content")),
            clear_charter=bool(payload.get("clear_charter", False)),
        )
    if any(key in payload for key in {"user_text", "user_content", "user_fields", "user_append", "user_clear"}):
        self.update_user_state(
            session_id=session_id,
            text=_optional_str(payload.get("user_text") or payload.get("user_content")),
            fields=payload.get("user_fields") if isinstance(payload.get("user_fields"), dict) else None,
            append=bool(payload.get("user_append", False)),
            clear=bool(payload.get("user_clear", False)),
        )
    if any(key in payload for key in {"relationship_text", "relationship_content", "relationship_append", "relationship_clear"}):
        self.update_relationship_state(
            session_id=session_id,
            text=_optional_str(payload.get("relationship_text") or payload.get("relationship_content")),
            append=bool(payload.get("relationship_append", False)),
            clear=bool(payload.get("relationship_clear", False)),
        )
    return self.inspect_profile_surface(session_id)

def inspect_activity_surface(self, session_id: str):
    session = self.repository.load_session(session_id)
    if session is None:
        raise KeyError(session_id)
    continuity = self.inspect_continuity(session_id)
    graph = self.repository.load_activity_graph(session_id)
    intent = _latest_turn_intent(self, session_id)
    return build_activity_operator_surface(
        session_id=session_id,
        active_goal_id=continuity.active_goal_id,
        active_goal_reason=continuity.wake_summary,
        wake_action=continuity.wake_action,
        wake_factors=continuity.wake_factors,
        goal_graph_revision=graph.revision_id if graph is not None else None,
        goals=graph.goals if graph is not None else (),
        intent=intent,
        opened_scopes=_opened_scopes_for_session(self, session_id, session=session, graph=graph),
        embedding_status=_embedding_status(self),
    )

def inspect_memory_surface(self, session_id: str):
    memories = tuple(
        MemoryOperatorDetail(
            memory=memory,
            state=self.memory_runtime.store.state(memory.memory_id),
            lineage=self.memory_runtime.store.lineage(memory.memory_id),
        )
        for memory in self.list_memories(session_id)
    )
    return build_memory_operator_surface(session_id=session_id, memories=memories)

def search_memory_surface(self, session_id: str, *, query: str, limit: int = 5):
    retrieval = self.memory_runtime.retrieve(
        session_id,
        query,
        goal_ids=tuple(goal.goal_id for goal in self.list_goals(session_id)),
        limit=limit,
    )
    memories = tuple(
        MemoryOperatorDetail(
            memory=memory,
            state=self.memory_runtime.store.state(memory.memory_id),
            lineage=self.memory_runtime.store.lineage(memory.memory_id),
        )
        for memory in self.list_memories(session_id)
    )
    hits = tuple(
        MemorySearchHit(memory=candidate.record, score=candidate.score, reasons=candidate.reasons)
        for candidate in retrieval.candidates
    )
    return build_memory_operator_surface(
        session_id=session_id,
        memories=memories,
        search_query=query,
        search_hits=hits,
        scope_reason=retrieval.scope_reason,
        index_policy=self.memory_runtime.index_policy(),
    )

def inspect_procedure_surface(self, session_id: str, *, minimum_support: int = 2):
    session = self.repository.load_session(session_id)
    if session is None:
        raise KeyError(session_id)
    library = self.repository.load_procedure_library(session.profile_id)
    learning = LearningRuntime(self.repository)
    candidates = learning.list_procedure_candidates(
        profile_id=session.profile_id,
        session_id=session_id,
        minimum_support=minimum_support,
    )
    procedures = tuple(
        ProcedureOperatorDetail(
            procedure=procedure,
            verification=(
                self.repository.load_verification_bundle(procedure.verification_bundle_id)
                if procedure.verification_bundle_id is not None
                else None
            ),
        )
        for procedure in (library.procedures if library is not None else ())
    )
    return build_procedure_operator_surface(
        session_id=session_id,
        profile_id=session.profile_id,
        procedures=procedures,
        candidates=candidates,
    )

def inspect_procedure_detail(self, session_id: str, procedure_id: str):
    surface = self.inspect_procedure_surface(session_id)
    for detail in surface.procedures:
        if detail.procedure.procedure_id == procedure_id:
            return detail
    raise KeyError(procedure_id)

def patch_procedure_surface(self, session_id: str, procedure_id: str, payload: Mapping[str, Any]):
    session = self.repository.load_session(session_id)
    if session is None:
        raise KeyError(session_id)
    learning = LearningRuntime(self.repository)
    updated = learning.patch_procedure(
        profile_id=session.profile_id,
        procedure_id=procedure_id,
        title=_optional_str(payload.get("title")),
        summary=_optional_str(payload.get("summary") or payload.get("content")),
        trigger_refs=_coerce_str_tuple(payload.get("trigger_refs")) if payload.get("trigger_refs") is not None else None,
        status=_optional_str(payload.get("status")),
    )
    return ProcedureOperatorDetail(
        procedure=updated,
        verification=(
            self.repository.load_verification_bundle(updated.verification_bundle_id)
            if updated.verification_bundle_id is not None
            else None
        ),
    )

def retire_procedure_surface(self, session_id: str, procedure_id: str):
    session = self.repository.load_session(session_id)
    if session is None:
        raise KeyError(session_id)
    learning = LearningRuntime(self.repository)
    retired = learning.retire_procedure(profile_id=session.profile_id, procedure_id=procedure_id)
    return ProcedureOperatorDetail(
        procedure=retired,
        verification=(
            self.repository.load_verification_bundle(retired.verification_bundle_id)
            if retired.verification_bundle_id is not None
            else None
        ),
    )

def inspect_audit_surface(self, session_id: str):
    session = self.repository.load_session(session_id)
    if session is None:
        raise KeyError(session_id)
    graph = self.repository.load_activity_graph(session_id)
    intent = _latest_turn_intent(self, session_id)
    opened_scopes = _opened_scopes_for_session(self, session_id, session=session, graph=graph)
    work = self.inspect_activity_surface(session_id)
    context_result = self.inspect_context_frame(session_id)
    return build_audit_surface(
        session_id=session_id,
        active_goal_id=work.active_goal_id,
        active_goal_reason=work.active_goal_reason,
        context_result=context_result,
        intent=intent,
        opened_scopes=opened_scopes,
        embedding_status=_embedding_status(self),
    )

def inspect_session(self, session_id: str) -> APISessionInspection:
    session = self.repository.load_session(session_id)
    if session is None:
        raise KeyError(session_id)
    profile = self.repository.load_profile(session.profile_id)
    if profile is None:
        raise KeyError(session.profile_id)
    lineage = self.repository.lineage(session_id)
    latest_turn = self._turns.get(session_id, [])[-1] if self._turns.get(session_id) else None
    graph = self.repository.load_activity_graph(session_id)
    goals = graph.goals if graph is not None else ()
    memories = tuple(self.memory_runtime.store.list(session_id=session_id))
    memory_count = len(memories)
    telemetry_count = len(self.telemetry.events)
    provider_profile = self.model_provider.active_profile()
    progression = build_progression_projection(
        self,
        profile_id=session.profile_id,
        session_id=session_id,
        state=self.repository.load_profile_growth(session.profile_id),
    )
    return APISessionInspection(
        profile=profile,
        session=session,
        lineage=lineage,
        goals=goals,
        memories=memories,
        latest_turn=latest_turn,
        memory_count=memory_count,
        telemetry_count=telemetry_count,
        goal_graph_revision=graph.revision_id if graph is not None else None,
        goal_status_counts=graph.status_counts() if graph is not None else {},
        provider_profile=provider_profile,
        progression=progression,
    )


def inspect_dashboard_surface(self, *, clone_limit: int = 12) -> dict[str, object]:
    now = _now()
    version = _resolve_aegis_version()
    doctor = self.doctor_provider()
    active_provider = doctor["active_provider"]
    doctor_status = str(doctor.get("status") or "preview")
    provider_status_label = _dashboard_status_label(doctor_status)
    embedding_status = str(active_provider.get("embedding_bootstrap_status") or "unknown")
    embedding_status_label = _dashboard_status_label(embedding_status)
    provider_tone = _provider_tone(doctor_status, embedding_status)

    runs = self.repository.list_agent_runs(statuses=("active", "pending", "failed", "completed"))
    backlog_count = sum(1 for run in runs if run.status in {"active", "pending"})
    last_success = next((run for run in runs if run.status == "completed"), None)
    last_failure = next((run for run in runs if run.status == "failed"), None)
    open_runs_by_session: dict[str, Any] = {}
    for run in runs:
        if run.status not in {"active", "pending"}:
            continue
        open_runs_by_session.setdefault(run.session_id, run)

    jobs = self.cron_runtime.list_jobs()
    scheduled_jobs = tuple(job for job in jobs if job.status == "scheduled")
    due_jobs = self.cron_runtime.due_jobs(now=now)
    latest_job = next(
        (
            job
            for job in sorted(
                jobs,
                key=lambda item: (item.last_run_at or item.updated_at, item.updated_at, item.name),
                reverse=True,
            )
        ),
        None,
    )
    next_job = next(
        (
            job
            for job in sorted(
                scheduled_jobs,
                key=lambda item: ((item.next_run_at or item.updated_at), item.name),
            )
        ),
        None,
    )

    clone_records: list[DashboardCloneRecord] = []
    active_goal_titles = 0
    for row in _dashboard_clone_rows(self, limit=clone_limit):
        session_id = str(row["session_id"]) if row["session_id"] is not None else None
        session_updated_at = _optional_datetime(row["session_updated_at"])
        identity_updated_at = _optional_datetime(row["identity_updated_at"])
        focus = "No active session yet."
        continuity = "idle"
        tone = "neutral"
        details = [
            DashboardDetailItem("Profile", str(row["profile_id"])),
        ]
        if session_id is not None:
            session = self.repository.load_session(session_id)
            if session is not None:
                graph, graph_issue = load_dashboard_activity_graph(self, session_id=session_id)
                active_goal = (
                    graph.goal(graph.active_goal_id)
                    if graph is not None and graph.active_goal_id is not None
                    else None
                )
                if graph_issue is not None:
                    focus = "Persisted activity graph needs repair before live focus can be restored."
                    continuity = "activity graph invalid"
                    tone = "critical"
                else:
                    continuity_state = self.inspect_continuity(session_id)
                    if active_goal is not None:
                        focus = active_goal.title
                        active_goal_titles += 1
                    else:
                        focus = continuity_state.wake_summary or "No active goal yet."
                    continuity = continuity_state.wake_action or continuity_state.continuity.summary or session.status
                    tone = (
                        "attention"
                        if continuity_state.continuity.continuity.requires_recovery
                        else "healthy"
                    )
                    open_run = open_runs_by_session.get(session_id)
                    if open_run is not None:
                        if open_run.status == "pending":
                            continuity = open_run.waiting_reason or "wake waiting"
                            tone = "attention"
                        elif open_run.status == "active":
                            continuity = "wake running"
                            tone = "healthy"
                    if session.status == "interrupted":
                        continuity = session.interruption_state or "interrupted"
                        tone = "attention"
                details.extend(
                    (
                        DashboardDetailItem("Session", session.session_id),
                        DashboardDetailItem("Status", session.status),
                    )
                )
                if graph_issue is not None:
                    details.append(DashboardDetailItem("Graph", graph_issue.detail))
                elif graph is not None and graph.active_goal_id:
                    details.append(DashboardDetailItem("Goal", graph.active_goal_id))
        else:
            details.append(DashboardDetailItem("Session", "not materialized"))
        clone_records.append(
            DashboardCloneRecord(
                clone=str(row["display_name"]),
                focus=focus,
                provider=_compact_provider_label(active_provider),
                continuity=continuity,
                last_contact=_relative_age(session_updated_at or identity_updated_at, now=now),
                tone=tone,
                details=tuple(details),
            )
        )

    graph_projection_session_ids = dashboard_graph_session_ids(self, limit=clone_limit)
    primary_graph_session_id = graph_projection_session_ids[0] if graph_projection_session_ids else None

    session_counts = _session_status_counts(self)
    total_sessions = sum(session_counts.values())
    active_sessions = session_counts.get("active", 0)
    interrupted_sessions = session_counts.get("interrupted", 0)
    memory_layers = build_dashboard_memory_layers(self, now=now)
    memory_layer_attention = any(layer.tone in {"attention", "critical"} for layer in memory_layers)
    graph_records = build_dashboard_graphs(
        self,
        session_ids=graph_projection_session_ids,
        open_runs_by_session=open_runs_by_session,
    )
    primary_graph_attention = (
        any(
            record.tone in {"attention", "critical"}
            and record.lane.endswith(f"/ {primary_graph_session_id}")
            for record in graph_records
        )
        if primary_graph_session_id is not None
        else False
    )
    graph_attention = any(record.tone == "critical" for record in graph_records) or primary_graph_attention
    session_records, ops_records = build_dashboard_observability(
        self,
        now=now,
        active_provider=active_provider,
        runs=runs,
        jobs=jobs,
        limit=clone_limit,
    )
    capability_records, provider_profiles, control_records = build_dashboard_capability_registry(
        self,
        active_provider=active_provider,
    )
    capability_attention = any(
        row.tone in {"attention", "critical"}
        for row in (*capability_records, *provider_profiles, *control_records)
    )
    dashboard_progression = None
    progression_projection = None
    progression_issue: str | None = None
    if primary_graph_session_id is not None:
        session = self.repository.load_session(primary_graph_session_id)
        if session is not None:
            try:
                progression_projection = build_progression_projection(
                    self,
                    profile_id=session.profile_id,
                    session_id=primary_graph_session_id,
                    state=self.repository.load_profile_growth(session.profile_id),
                )
                dashboard_progression = build_dashboard_progression(progression_projection)
            except ValueError as error:
                progression_issue = str(error)

    heartbeat_tone = "critical" if last_failure is not None and backlog_count else (
        "attention"
        if backlog_count or due_jobs or any(job.status == "paused" for job in jobs)
        else "healthy"
    )
    if not jobs and not runs:
        heartbeat_tone = "neutral"

    provider_summary = str(doctor.get("probe_summary") or "").strip() or str(
        active_provider.get("embedding_bootstrap_summary") or "No provider doctor summary yet."
    )
    heartbeat_summary = (
        f"{backlog_count} wake run(s) open, {len(scheduled_jobs)} scheduled cron job(s), {len(due_jobs)} due now."
        if jobs or runs
        else "No wake or cron activity has been recorded yet."
    )
    has_live_state = bool(clone_records or total_sessions or runs or jobs or self.repository.list_auth_profiles())

    metrics = (
        DashboardMetric(
            label="Aegis version",
            value=version,
            note="Resolved from the packaged project metadata so dashboard claims match the shipped runtime.",
            tone="neutral",
        ),
        DashboardMetric(
            label="Runtime health",
            value=provider_status_label,
            note="Provider doctor, embedding bootstrap, and backlog posture are synthesized into the landing signal.",
            tone=provider_tone if heartbeat_tone == "healthy" else heartbeat_tone,
        ),
        DashboardMetric(
            label="Clone fleet",
            value=f"{len(clone_records)} tracked",
            note=f"{active_goal_titles} clone lane(s) have an explicit active goal projection.",
            tone="healthy" if clone_records else "neutral",
        ),
        DashboardMetric(
            label="Active sessions",
            value=f"{active_sessions} active",
            note=f"{total_sessions} total session(s); {interrupted_sessions} interrupted.",
            tone="healthy" if active_sessions else ("attention" if interrupted_sessions else "neutral"),
        ),
        DashboardMetric(
            label="Memory layers",
            value=f"{len(memory_layers)} owners",
            note="Profile, activity, evidence, procedure, and capability owners now publish live drill-down summaries.",
            tone="neutral" if not has_live_state else ("attention" if memory_layer_attention else "healthy"),
        ),
        DashboardMetric(
            label="Provider readiness",
            value=provider_status_label,
            note=provider_summary,
            tone=provider_tone,
        ),
        DashboardMetric(
            label="Embedding preload",
            value=embedding_status_label,
            note=str(active_provider.get("embedding_bootstrap_summary") or "No embedding bootstrap summary."),
            tone=provider_tone,
        ),
        DashboardMetric(
            label="Wake / cron",
            value=f"{backlog_count} queued",
            note=heartbeat_summary,
            tone=heartbeat_tone,
        ),
        DashboardMetric(
            label="Capability registry",
            value=f"{len(capability_records)} skills / {len(provider_profiles)} profiles",
            note=(
                "Installed skills, provider profiles, and governed operator controls now share one "
                "CapabilityRegistry-backed dashboard route."
            ),
            tone=(
                "attention"
                if capability_attention
                else ("healthy" if provider_profiles else "neutral")
            ),
        ),
        DashboardMetric(
            label="Progression",
            value=(
                progression_projection.identity_line
                if progression_projection is not None
                else ("Progression blocked" if progression_issue else "No projected progression yet")
            ),
            note=(
                f"Progression projection degraded because the primary lane activity graph is invalid: {progression_issue}"
                if progression_issue
                else progression_metric_note(progression_projection, dashboard_progression)
            ),
            tone=(
                "critical"
                if progression_issue
                else (
                    "attention"
                    if progression_projection is not None and progression_projection.title_window_open
                    else ("healthy" if progression_projection is not None else "neutral")
                )
            ),
        ),
    )

    alerts: list[DashboardAlert] = []
    invalid_graph_records = tuple(record for record in graph_records if record.state == "invalid")
    if doctor_status != "ready":
        alerts.append(
            DashboardAlert(
                title="Provider readiness needs operator attention",
                detail=provider_summary,
                tone=provider_tone,
            )
        )
    if backlog_count or due_jobs:
        alerts.append(
            DashboardAlert(
                title="Wake or cron backlog is non-zero",
                detail=heartbeat_summary,
                tone=heartbeat_tone,
            )
        )
    if memory_layer_attention:
        attention_layers = ", ".join(layer.layer for layer in memory_layers if layer.tone in {"attention", "critical"})
        alerts.append(
            DashboardAlert(
                title="One or more durable owner layers need inspection",
                detail=f"Review the Memory route for {attention_layers}.",
                tone="attention",
            )
        )
    if interrupted_sessions:
        alerts.append(
            DashboardAlert(
                title="Interrupted sessions remain in the continuity set",
                detail=f"{interrupted_sessions} session(s) are currently interrupted and will require an explicit resume or operator review.",
                tone="attention",
            )
        )
    if invalid_graph_records:
        affected_lanes = ", ".join(record.lane for record in invalid_graph_records[:3])
        if len(invalid_graph_records) > 3:
            affected_lanes = f"{affected_lanes}, +{len(invalid_graph_records) - 3} more"
        alerts.append(
            DashboardAlert(
                title="Persisted activity graph failed validation",
                detail=(
                    f"Dashboard degraded the affected lane instead of failing live projection. "
                    f"Review {affected_lanes}. {invalid_graph_records[0].blocker}"
                ),
                tone="critical",
            )
        )
    if graph_attention and not invalid_graph_records:
        attention_graphs = ", ".join(
            f"{record.lane} -> {record.graph}"
            for record in graph_records
            if record.tone in {"attention", "critical"}
        )
        alerts.append(
            DashboardAlert(
                title="Graph focus or recall support needs inspection",
                detail=f"Review the Graphs route for {attention_graphs}.",
                tone="attention",
            )
        )
    if capability_attention:
        attention_rows = ", ".join(
            row.capability
            for row in capability_records
            if row.tone in {"attention", "critical"}
        ) or ", ".join(
            row.profile
            for row in provider_profiles
            if row.tone in {"attention", "critical"}
        ) or "CapabilityRegistry"
        alerts.append(
            DashboardAlert(
                title="Capability registry needs operator review",
                detail=f"Review the Capabilities route for {attention_rows}.",
                tone="attention",
            )
        )
    if not alerts:
        alerts.append(
            DashboardAlert(
                title="Landing projection is live",
                detail="Overview, Clones, Memory, Graphs, Sessions, Ops, and Capabilities now read from durable API/runtime state.",
                tone="healthy" if clone_records else "neutral",
            )
        )

    timeline = [
        DashboardTimelineEvent(
            label="Provider doctor",
            summary=provider_summary,
            age=_relative_age(_optional_datetime(active_provider.get("embedding_bootstrap_updated_at")), now=now),
            tone=provider_tone,
        )
    ]
    if last_success is not None:
        timeline.append(
            DashboardTimelineEvent(
                label="Wake success",
                summary=last_success.last_summary or "Latest resumable run completed successfully.",
                age=_relative_age(last_success.updated_at, now=now),
                tone="healthy",
            )
        )
    if last_failure is not None:
        timeline.append(
            DashboardTimelineEvent(
                label="Wake failure",
                summary=last_failure.last_summary or last_failure.waiting_reason or "Latest resumable run failed.",
                age=_relative_age(last_failure.updated_at, now=now),
                tone="critical",
            )
        )
    if latest_job is not None:
        timeline.append(
            DashboardTimelineEvent(
                label="Cron heartbeat",
                summary=latest_job.last_summary or f"{latest_job.name} remains {latest_job.status}.",
                age=_relative_age(latest_job.last_run_at or latest_job.updated_at, now=now),
                tone=_tone_for_status(latest_job.status),
            )
        )
    if clone_records:
        timeline.append(
            DashboardTimelineEvent(
                label="Clone roster",
                summary=f"{len(clone_records)} tracked clone(s); latest lane contact is {clone_records[0].clone}.",
                age=clone_records[0].last_contact,
                tone=clone_records[0].tone,
            )
        )

    scenario = "healthy"
    if not has_live_state:
        scenario = "empty"
    elif (
        provider_tone == "critical"
        or heartbeat_tone in {"attention", "critical"}
        or memory_layer_attention
        or graph_attention
        or capability_attention
    ):
        scenario = "degraded"

    provider = DashboardProviderReadiness(
        status=provider_status_label,
        provider=_dashboard_config_label(active_provider.get("display_name") or active_provider.get("provider_id")),
        transport=_dashboard_config_label(active_provider.get("transport_display_name") or active_provider.get("transport_id")),
        strong_model=_dashboard_config_label(active_provider.get("strong_model"), fallback="n/a"),
        weak_model=_dashboard_config_label(active_provider.get("weak_model"), fallback="n/a"),
        secret_status=_dashboard_config_label(active_provider.get("secret_status"), fallback="n/a"),
        embedding_status=embedding_status_label,
        summary=provider_summary,
        tone=provider_tone,
    )
    heartbeat = DashboardHeartbeat(
        mode="wake+cron" if jobs and runs else ("cron" if jobs else ("wake" if runs else "idle")),
        summary=heartbeat_summary,
        backlog=f"{backlog_count} open wake run(s)",
        scheduled_jobs=f"{len(scheduled_jobs)} scheduled / {len(due_jobs)} due",
        last_success=_display_timestamp(last_success.updated_at if last_success is not None else None, now=now),
        last_failure=_display_timestamp(last_failure.updated_at if last_failure is not None else None, now=now),
        next_run=_display_timestamp(next_job.next_run_at if next_job is not None else None, now=now),
        tone=heartbeat_tone,
    )

    shell_status = (
        "DASH-6 now projects live runtime, clone, heartbeat, durable owner memory, graph focus, session observability, capability inventory, provider profiles, and governed control boundaries through the dashboard routes."
        if has_live_state
        else "Dashboard projection is live, and CapabilityRegistry-backed inventory is readable even before clone, wake, and provider runtime state are materialized."
    )
    note = (
        "Overview, Clones, Memory, Graphs, Sessions, Ops, Capabilities, and progression now read from the API/operator snapshot without reopening model-owned install or search behavior."
    )

    return dashboard_surface_record(
        build_dashboard_surface(
            scenario=scenario,
            source_label="Live operator projection",
            shell_status=shell_status,
            generated_at=now.isoformat(),
            note=note,
            metrics=metrics,
            alerts=tuple(alerts),
            timeline=tuple(timeline[:4]),
            clones=tuple(clone_records),
            memory_layers=memory_layers,
            graphs=graph_records,
            sessions=tuple(session_records),
            ops=ops_records,
            capabilities=capability_records,
            provider_profiles=provider_profiles,
            controls=control_records,
            provider=provider,
            heartbeat=heartbeat,
            progression=dashboard_progression,
        )
    )
