"""Turn execution and HTTP dispatch methods for the API runtime app."""


from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
import json
from typing import Any, Mapping
from uuid import uuid4

from apps.provider_runtime import (
    SurfaceModelProviderCapability,
    provider_profile_from_payload,
)
from packages.auth import AuthProfile, PersistentAuthProfileStore
from packages.context import ContextRuntime
from packages.contracts import ContextBundle, EventEnvelope, ExecutionResult, GoalNode, MemoryRecord, ProfileState, SessionState, ActivityGraph
from packages.kernel import KernelDependencies, KernelOutcome, KernelService, KernelTurnRequest, ObservationPipeline, StateReconciler
from packages.learning import LearningRuntime
from packages.evidence import MemoryRuntime
from packages.operator import (
    MemoryOperatorDetail,
    MemorySearchHit,
    ProcedureOperatorDetail,
    build_audit_surface,
    build_memory_operator_surface,
    build_procedure_operator_surface,
    build_profile_operator_surface,
    build_activity_operator_surface,
    library_procedure_overlays,
)
from packages.planning import PlanningService
from packages.session import SessionLineageService, SessionResumeResult
from packages.storage import RuntimeStorageRepository
from packages.tools import BuiltinToolDependencies, build_tool_runtime
from packages.tools.adapters import DeliveryMessageSurfaceAdapter, StructuredClarifySurface
from packages.tools.browser_backend import create_playwright_browser_backend

from .capabilities import (
    APIContextCapability,
    APIDeliveryCapability,
    APIMemoryCapability,
    APIModelProvider,
    APIPlanningCapability,
    APITelemetrySink,
    APIToolExecution,
)
from .state_runtime import APIContinuityInspection, APIStateService
from .tool_surfaces import APIMemoryManagementSurface

from .api_runtime_support import (
    APIAppConfig,
    APIResponse,
    APISessionCreationResult,
    APISessionInspection,
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

def run_turn(
    self,
    session_id: str,
    *,
    prompt: str,
    goal_query: str | None = None,
    tool_name: str | None = None,
    tool_arguments: Mapping[str, Any] | None = None,
    delivery_payload: Mapping[str, Any] | None = None,
) -> APITurnResult:
    session = self.repository.load_session(session_id)
    if session is None:
        raise KeyError(session_id)
    profile = self.repository.load_profile(session.profile_id)
    if profile is None:
        raise KeyError(session.profile_id)
    previous_goal_graph = self.repository.load_activity_graph(session_id) or ActivityGraph(session_id=session_id)
    event = EventEnvelope(
        event_id=f"api:{session_id}:turn:{uuid4().hex}",
        event_type="turn.received",
        session_id=session_id,
        source="api",
        payload={
            "message": prompt,
            "content": prompt,
            "summary": prompt,
            "goal_query": goal_query or "",
            "tool_name": tool_name or "",
        },
    )
    outcome = self.kernel.run(
        KernelTurnRequest(
            event=event,
            prompt=prompt,
            goal_query=goal_query,
            tool_name=tool_name,
            tool_arguments=dict(tool_arguments or {}),
            delivery_payload=dict(delivery_payload or {}),
        )
    )
    observation = ObservationPipeline().observe_turn(
        inbound_event=event,
        execution=outcome.execution,
        previous_goal_graph=previous_goal_graph,
        reconciled_goal_graph=outcome.goal_graph,
        selected_goal_id=(
            outcome.decision.selected_move.goal_id
            if outcome.decision is not None and outcome.decision.selected_move.goal_id
            else outcome.goal_graph.active_goal_id
        ),
        decision_summary=(
            outcome.decision.rationale.summary
            if outcome.decision is not None and outcome.decision.rationale.summary.strip()
            else outcome.execution.summary
        ),
        source="api",
    )
    StateReconciler().reconcile_turn(
        repository=self.repository,
        memory_runtime=self.memory_runtime,
        observation=observation,
    )
    self.personal_state.apply_turn_profile_delta(
        session_id=session_id,
        user_fields=dict(observation.profile_delta.user_fields),
        preference_updates=observation.profile_delta.preference_updates,
        relationship_notes=observation.profile_delta.relationship_notes,
    )
    record = APITurnRecord(
        request={
            "prompt": prompt,
            "goal_query": goal_query,
            "tool_name": tool_name,
            "tool_arguments": dict(tool_arguments or {}),
            "delivery_payload": dict(delivery_payload or {}),
        },
        outcome=outcome,
        recorded_at=_now(),
    )
    active_provider = self.model_provider.describe()
    token_metadata = {
        "outcome": outcome.execution.outcome,
        "execution_id": outcome.execution.execution_id,
        "source": "api.turn",
    }
    if (
        outcome.execution.cache_usage_reported
        or outcome.execution.cached_prompt_tokens
        or outcome.execution.cache_creation_prompt_tokens
    ):
        token_metadata.update(
            {
                "cached_prompt_tokens": outcome.execution.cached_prompt_tokens,
                "cache_creation_prompt_tokens": outcome.execution.cache_creation_prompt_tokens,
                "cache_usage_reported": outcome.execution.cache_usage_reported,
            }
        )
    self.repository.record_token_usage(
        session_id=session_id,
        profile_id=session.profile_id,
        run_id=outcome.run.run_id if outcome.run is not None else None,
        source_event_id=event.event_id,
        provider_id=_optional_str(active_provider.get("provider_id") or active_provider.get("source")),
        model_id=_optional_str(active_provider.get("strong_model") or active_provider.get("model")),
        prompt_tokens=outcome.execution.prompt_tokens,
        completion_tokens=outcome.execution.completion_tokens,
        total_tokens=outcome.execution.total_tokens,
        metadata=token_metadata,
    )
    self._turns.setdefault(session_id, []).append(record)
    inspection = self.inspect_session(session_id)
    return APITurnResult(
        session=inspection.session,
        outcome=outcome,
        latest_turn=record,
        inspection=inspection,
    )

def dispatch(self, method: str, path: str, body: bytes | None = None) -> APIResponse:
    if method.upper() == "GET" and path == "/healthz":
        return APIResponse(200, {"status": "ok", "service": "aegis-api"})

    try:
        parts = _split_path(path)
        if not parts:
            return APIResponse(404, {"error": "not_found"})
        if parts[0] == "providers":
            return self._dispatch_providers(method, parts[1:], body)
        if parts[0] == "operator":
            return self._dispatch_operator(method, parts[1:], body)
        if parts[0] != "sessions":
            return APIResponse(404, {"error": "not_found"})
        if method.upper() == "POST" and len(parts) == 1:
            payload = _read_json_bytes(body)
            result = self.create_session(
                profile_id=str(payload["profile_id"]),
                display_name=str(payload["display_name"]),
                mode=str(payload["mode"]),
                workspace_id=payload.get("workspace_id"),
                clone_path=payload.get("clone_path"),
                preferences=tuple(payload.get("preferences", ())),
                enabled_capabilities=tuple(payload.get("enabled_capabilities", ())),
                provider_profile=payload.get("provider_profile"),
                session_id=payload.get("session_id"),
            )
            return APIResponse(201, _jsonable(result.to_record()))
        if len(parts) < 2:
            return APIResponse(404, {"error": "not_found"})
        session_id = parts[1]
        if method.upper() == "GET" and len(parts) == 2:
            return APIResponse(200, _jsonable(self.inspect_session(session_id).to_record()))
        if method.upper() == "POST" and len(parts) == 3 and parts[2] == "interrupt":
            payload = _read_json_bytes(body)
            result = self.interrupt_session(session_id, interruption_state=str(payload["interruption_state"]))
            return APIResponse(200, _jsonable(result.to_record()))
        if method.upper() == "POST" and len(parts) == 3 and parts[2] == "resume":
            payload = _read_json_bytes(body)
            result = self.resume_session(session_id, child_session_id=payload.get("child_session_id"))
            return APIResponse(200, _jsonable(result.to_record()))
        if method.upper() == "POST" and len(parts) == 3 and parts[2] == "turns":
            payload = _read_json_bytes(body)
            result = self.run_turn(
                session_id,
                prompt=str(payload["prompt"]),
                goal_query=payload.get("goal_query"),
                tool_name=payload.get("tool_name"),
                tool_arguments=payload.get("tool_arguments"),
                delivery_payload=payload.get("delivery_payload"),
            )
            return APIResponse(200, _jsonable(result.to_record()))
        if len(parts) == 3 and parts[2] in {"profile", "activity", "memory", "procedure", "audit"}:
            surface = parts[2]
            if surface == "profile":
                if method.upper() == "GET":
                    return APIResponse(200, _jsonable({"session_id": session_id, "profile": self.inspect_profile_surface(session_id)}))
                if method.upper() in {"PATCH", "POST"}:
                    payload = _read_json_bytes(body)
                    return APIResponse(200, _jsonable({"session_id": session_id, "profile": self.patch_profile_surface(session_id, payload)}))
            if surface == "activity":
                if method.upper() == "GET":
                    return APIResponse(200, _jsonable({"session_id": session_id, "activity": self.inspect_activity_surface(session_id)}))
                if method.upper() == "POST":
                    payload = _read_json_bytes(body)
                    result = self.create_goal(
                        session_id,
                        title=str(payload["title"]),
                        status=str(payload.get("status", "active")),
                        priority=str(payload.get("priority", "medium")),
                        owner=str(payload.get("owner", "shared")),
                        parent_goal_id=_optional_str(payload.get("parent_goal_id")),
                        dependency_refs=payload.get("dependency_refs"),
                        evidence_refs=payload.get("evidence_refs"),
                        related_memory_ids=payload.get("related_memory_ids"),
                        review_checkpoint=_optional_str(payload.get("review_checkpoint")),
                        deadline=payload.get("deadline"),
                        time_sensitivity=_optional_str(payload.get("time_sensitivity")),
                        reason=_optional_str(payload.get("reason")),
                        activate=_optional_bool(payload.get("activate")),
                    )
                    return APIResponse(201, _jsonable({"session_id": session_id, "activity": self.inspect_activity_surface(session_id), "activity_item": result["goal"]}))
            if surface == "memory":
                if method.upper() == "GET":
                    return APIResponse(200, _jsonable({"session_id": session_id, "memory": self.inspect_memory_surface(session_id)}))
            if surface == "procedure" and method.upper() == "GET":
                return APIResponse(200, _jsonable({"session_id": session_id, "procedure": self.inspect_procedure_surface(session_id)}))
            if surface == "audit" and method.upper() == "GET":
                return APIResponse(200, _jsonable({"session_id": session_id, "audit": self.inspect_audit_surface(session_id)}))
        if len(parts) == 3 and parts[2] in {"identity", "user", "relationship", "continuity"}:
            surface = parts[2]
            if surface == "identity":
                if method.upper() == "GET":
                    return APIResponse(200, _jsonable({"session_id": session_id, "identity": self.inspect_identity(session_id=session_id)}))
                if method.upper() in {"PATCH", "POST"}:
                    payload = _read_json_bytes(body)
                    result = self.update_identity_state(
                        session_id=session_id,
                        display_name=_optional_str(payload.get("display_name") or payload.get("name")),
                        personality_preset=_optional_str(payload.get("personality_preset")),
                        initiative=_optional_str(payload.get("initiative")),
                        charter_text=_optional_str(payload.get("charter_text") or payload.get("text") or payload.get("content")),
                        clear_charter=bool(payload.get("clear_charter", False)),
                    )
                    return APIResponse(200, _jsonable({"session_id": session_id, "identity": result}))
            if surface == "user":
                if method.upper() == "GET":
                    return APIResponse(200, _jsonable({"session_id": session_id, "user": self.inspect_user(session_id=session_id)}))
                if method.upper() in {"PATCH", "POST"}:
                    payload = _read_json_bytes(body)
                    result = self.update_user_state(
                        session_id=session_id,
                        text=_optional_str(payload.get("text") or payload.get("content")),
                        fields=payload.get("fields") if isinstance(payload.get("fields"), dict) else None,
                        append=bool(payload.get("append", False)),
                        clear=bool(payload.get("clear", False)),
                    )
                    return APIResponse(200, _jsonable({"session_id": session_id, "user": result}))
            if surface == "relationship":
                if method.upper() == "GET":
                    return APIResponse(200, _jsonable({"session_id": session_id, "relationship": self.inspect_relationship(session_id=session_id)}))
                if method.upper() in {"PATCH", "POST"}:
                    payload = _read_json_bytes(body)
                    result = self.update_relationship_state(
                        session_id=session_id,
                        text=_optional_str(payload.get("text") or payload.get("content")),
                        append=bool(payload.get("append", False)),
                        clear=bool(payload.get("clear", False)),
                    )
                    return APIResponse(200, _jsonable({"session_id": session_id, "relationship": result}))
            if surface == "continuity" and method.upper() == "GET":
                return APIResponse(200, _jsonable(self.inspect_continuity(session_id).to_record()))
        if len(parts) == 3 and parts[2] in {"goals", "memories"}:
            if parts[2] == "goals":
                if method.upper() == "GET":
                    return APIResponse(200, _jsonable({"session_id": session_id, "goals": self.list_goals(session_id)}))
                if method.upper() == "POST":
                    payload = _read_json_bytes(body)
                    result = self.create_goal(
                        session_id,
                        title=str(payload["title"]),
                        status=str(payload.get("status", "active")),
                        priority=str(payload.get("priority", "medium")),
                        owner=str(payload.get("owner", "shared")),
                        parent_goal_id=_optional_str(payload.get("parent_goal_id")),
                        dependency_refs=payload.get("dependency_refs"),
                        evidence_refs=payload.get("evidence_refs"),
                        related_memory_ids=payload.get("related_memory_ids"),
                        review_checkpoint=_optional_str(payload.get("review_checkpoint")),
                        deadline=payload.get("deadline"),
                        time_sensitivity=_optional_str(payload.get("time_sensitivity")),
                        reason=_optional_str(payload.get("reason")),
                        activate=_optional_bool(payload.get("activate")),
                    )
                    return APIResponse(201, _jsonable(result))
            if method.upper() == "GET":
                return APIResponse(200, _jsonable({"session_id": session_id, "memories": self.list_memories(session_id)}))
        if len(parts) == 4 and parts[2] == "memory" and parts[3] == "search":
            payload = _read_json_bytes(body)
            query = _optional_str(payload.get("query"))
            if query is None:
                raise ValueError("memory search query is required")
            limit = int(payload.get("limit", 5))
            return APIResponse(200, _jsonable({"session_id": session_id, "memory": self.search_memory_surface(session_id, query=query, limit=limit)}))
        if len(parts) == 4 and parts[2] == "activity":
            goal_id = parts[3]
            if method.upper() == "GET":
                return APIResponse(200, _jsonable({"session_id": session_id, "activity_item": self.inspect_goal(session_id, goal_id), "activity": self.inspect_activity_surface(session_id)}))
            payload = _read_json_bytes(body)
            if method.upper() in {"PATCH", "POST"}:
                result = self.update_goal(
                    session_id,
                    goal_id,
                    title=payload.get("title"),
                    status=payload.get("status"),
                    priority=payload.get("priority"),
                    owner=payload.get("owner"),
                    dependency_refs=payload.get("dependency_refs"),
                    evidence_refs=payload.get("evidence_refs"),
                    related_memory_ids=payload.get("related_memory_ids"),
                    review_checkpoint=payload.get("review_checkpoint"),
                    deadline=payload.get("deadline"),
                    time_sensitivity=payload.get("time_sensitivity"),
                    reason=payload.get("reason"),
                )
                return APIResponse(200, _jsonable({"session_id": session_id, "activity_item": result["goal"], "before": result["before"], "activity": self.inspect_activity_surface(session_id)}))
            if method.upper() == "DELETE":
                result = self.delete_goal(session_id, goal_id, reason=str(payload.get("reason", "")))
                return APIResponse(200, _jsonable({"session_id": session_id, "activity_item": result["goal"], "before": result["before"], "activity": self.inspect_activity_surface(session_id)}))
        if len(parts) == 4 and parts[2] == "memory":
            memory_id = parts[3]
            if method.upper() == "GET":
                return APIResponse(200, _jsonable({
                    "session_id": session_id,
                    "memory": MemoryOperatorDetail(
                        memory=self.inspect_memory(session_id, memory_id)["memory"],
                        state=self.memory_runtime.store.state(memory_id),
                        lineage=self.memory_runtime.store.lineage(memory_id),
                    ),
                }))
            payload = _read_json_bytes(body)
            if method.upper() in {"PATCH", "POST"}:
                if "corrected_content" in payload:
                    result = self.correct_memory(
                        session_id,
                        memory_id,
                        corrected_content=str(payload["corrected_content"]),
                        reason=str(payload.get("reason", "")),
                        actor=str(payload.get("actor", "user")),
                    )
                    return APIResponse(200, _jsonable(result))
                if "pinned" in payload:
                    result = self.pin_memory(
                        session_id,
                        memory_id,
                        pinned=bool(payload.get("pinned")),
                        reason=str(payload.get("reason", "")),
                        actor=str(payload.get("actor", "user")),
                    )
                    return APIResponse(200, _jsonable(result))
                raise ValueError("memory patch requires corrected_content or pinned")
            if method.upper() == "DELETE":
                result = self.delete_memory(
                    session_id,
                    memory_id,
                    reason=str(payload.get("reason", "")),
                    actor=str(payload.get("actor", "user")),
                )
                return APIResponse(200, _jsonable(result))
        if len(parts) == 4 and parts[2] == "procedure":
            procedure_id = parts[3]
            if method.upper() == "GET":
                return APIResponse(200, _jsonable({"session_id": session_id, "procedure": self.inspect_procedure_detail(session_id, procedure_id)}))
            payload = _read_json_bytes(body)
            if method.upper() in {"PATCH", "POST"}:
                return APIResponse(200, _jsonable({"session_id": session_id, "procedure": self.patch_procedure_surface(session_id, procedure_id, payload)}))
            if method.upper() == "DELETE":
                return APIResponse(200, _jsonable({"session_id": session_id, "procedure": self.retire_procedure_surface(session_id, procedure_id)}))
        if len(parts) == 4 and parts[2] == "goals":
            goal_id = parts[3]
            if method.upper() == "GET":
                return APIResponse(200, _jsonable(self.inspect_goal(session_id, goal_id)))
            payload = _read_json_bytes(body)
            if method.upper() in {"PATCH", "POST"}:
                result = self.update_goal(
                    session_id,
                    goal_id,
                    title=payload.get("title"),
                    status=payload.get("status"),
                    priority=payload.get("priority"),
                    owner=payload.get("owner"),
                    dependency_refs=payload.get("dependency_refs"),
                    evidence_refs=payload.get("evidence_refs"),
                    related_memory_ids=payload.get("related_memory_ids"),
                    review_checkpoint=payload.get("review_checkpoint"),
                    deadline=payload.get("deadline"),
                    time_sensitivity=payload.get("time_sensitivity"),
                    reason=payload.get("reason"),
                )
                return APIResponse(200, _jsonable(result))
            if method.upper() == "DELETE":
                result = self.delete_goal(session_id, goal_id, reason=str(payload.get("reason", "")))
                return APIResponse(200, _jsonable(result))
        if len(parts) == 4 and parts[2] == "memories":
            memory_id = parts[3]
            if method.upper() == "GET":
                return APIResponse(200, _jsonable(self.inspect_memory(session_id, memory_id)))
            payload = _read_json_bytes(body)
            if method.upper() in {"PATCH", "POST"}:
                result = self.correct_memory(
                    session_id,
                    memory_id,
                    corrected_content=str(payload["corrected_content"]),
                    reason=str(payload.get("reason", "")),
                    actor=str(payload.get("actor", "user")),
                )
                return APIResponse(200, _jsonable(result))
            if method.upper() == "DELETE":
                result = self.delete_memory(
                    session_id,
                    memory_id,
                    reason=str(payload.get("reason", "")),
                    actor=str(payload.get("actor", "user")),
                )
                return APIResponse(200, _jsonable(result))
        return APIResponse(404, {"error": "not_found"})
    except KeyError as error:
        return APIResponse(404, {"error": "not_found", "missing": str(error)})
    except (ValueError, TypeError) as error:
        return APIResponse(400, {"error": "bad_request", "detail": str(error)})

def _dispatch_providers(self, method: str, parts: tuple[str, ...], body: bytes | None) -> APIResponse:
    if method.upper() == "GET" and len(parts) == 0:
        return APIResponse(200, _jsonable(self.list_providers()))
    if method.upper() == "GET" and len(parts) == 1 and parts[0] == "doctor":
        return APIResponse(200, _jsonable(self.doctor_provider()))
    if method.upper() == "GET" and len(parts) == 2 and parts[0] == "setup":
        return APIResponse(200, _jsonable(self.setup_provider(parts[1])))
    if method.upper() == "POST" and len(parts) == 1 and parts[0] == "models":
        payload = _read_json_bytes(body)
        return APIResponse(200, _jsonable(self.discover_provider_models(payload)))
    if method.upper() == "POST" and len(parts) == 1 and parts[0] == "default":
        payload = _read_json_bytes(body)
        provider_profile = payload.get("provider_profile")
        if not isinstance(provider_profile, dict):
            raise ValueError("provider_profile must be an object containing strong_profile, weak_profile, and intent_mode")
        result = self.set_default_provider(provider_profile)
        return APIResponse(200, _jsonable(result))
    if method.upper() == "POST" and len(parts) == 1 and parts[0] == "test":
        payload = _read_json_bytes(body)
        result = self.test_provider(prompt=str(payload.get("prompt", "Summarize the current provider configuration.")))
        return APIResponse(200, _jsonable(result))
    if method.upper() == "GET" and len(parts) == 1 and parts[0] == "keys":
        return APIResponse(200, _jsonable(self.list_provider_keys()))
    if method.upper() == "POST" and len(parts) == 1 and parts[0] == "keys":
        payload = _read_json_bytes(body)
        return APIResponse(201, _jsonable(self.create_provider_key(payload)))
    if method.upper() == "PATCH" and len(parts) == 2 and parts[0] == "keys":
        payload = _read_json_bytes(body)
        return APIResponse(200, _jsonable(self.upsert_provider_key(parts[1], payload)))
    if method.upper() == "DELETE" and len(parts) == 2 and parts[0] == "keys":
        return APIResponse(200, _jsonable(self.delete_provider_key(parts[1])))
    return APIResponse(404, {"error": "not_found"})


def _dispatch_operator(self, method: str, parts: tuple[str, ...], body: bytes | None) -> APIResponse:
    if method.upper() == "GET" and len(parts) == 1 and parts[0] == "dashboard":
        return APIResponse(200, {"dashboard": _jsonable(self.inspect_dashboard_surface())})
    if method.upper() == "GET" and len(parts) == 1 and parts[0] == "console":
        return APIResponse(200, {"console": _jsonable(self.inspect_operator_console())})
    if parts and parts[0] == "cron":
        if method.upper() == "GET" and len(parts) == 1:
            return APIResponse(200, {"cron": {"jobs": [_cron_job_record(job) for job in self.cron_runtime.list_jobs()]}})
        if method.upper() == "POST" and len(parts) == 1:
            payload = _read_json_bytes(body)
            job_payload = _cron_payload(payload)
            job = self.cron_runtime.create_job(
                name=str(payload.get("name") or "Aegis job"),
                schedule_text=str(payload["schedule"]),
                action_kind=str(payload.get("job_kind") or payload.get("action_kind") or "prompt"),
                payload=job_payload,
                profile_id=_optional_str(payload.get("profile_id")),
                clone_id=_optional_str(payload.get("clone_id")),
                timezone_name=_optional_str(payload.get("timezone_name")),
            )
            return APIResponse(201, {"cron": {"job": _cron_job_record(job)}})
        if len(parts) == 2:
            job_id = parts[1]
            if method.upper() == "GET":
                return APIResponse(200, {"cron": {"job": _cron_job_record(self.cron_runtime.inspect_job(job_id))}})
            if method.upper() == "PATCH":
                payload = _read_json_bytes(body)
                action = str(payload.get("action") or "").strip().lower()
                if action == "pause":
                    job = self.cron_runtime.pause_job(job_id)
                elif action == "resume":
                    job = self.cron_runtime.resume_job(job_id)
                else:
                    raise ValueError("cron PATCH requires action=pause or action=resume")
                return APIResponse(200, {"cron": {"job": _cron_job_record(job)}})
            if method.upper() == "DELETE":
                job = self.cron_runtime.remove_job(job_id)
                return APIResponse(200, {"cron": {"job": _cron_job_record(job), "status": "removed"}})
    if method.upper() == "PATCH" and len(parts) == 1 and parts[0] == "settings":
        payload = _read_json_bytes(body)
        return APIResponse(200, _jsonable(self.patch_operator_settings(payload)))
    if method.upper() == "PATCH" and len(parts) == 1 and parts[0] == "config":
        payload = _read_json_bytes(body)
        return APIResponse(200, _jsonable(self.patch_operator_global_config(payload)))
    if method.upper() == "POST" and len(parts) == 1 and parts[0] == "gateway":
        payload = _read_json_bytes(body)
        return APIResponse(200, _jsonable(self.gateway_action(payload)))
    if method.upper() == "PATCH" and len(parts) == 2 and parts[0] in {"skills", "tools"}:
        payload = _read_json_bytes(body)
        result = self.set_console_item_enabled(
            kind="skill" if parts[0] == "skills" else "tool",
            item_id=parts[1],
            enabled=bool(payload.get("enabled")),
        )
        return APIResponse(200, _jsonable(result))
    return APIResponse(404, {"error": "not_found"})


def _cron_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    job_payload = {
        key: value
        for key, value in (
            ("message", _optional_str(payload.get("message"))),
            ("query", _optional_str(payload.get("query"))),
            ("prompt", _optional_str(payload.get("prompt"))),
        )
        if value is not None
    }
    skills = _cron_skill_ids(payload.get("skills"))
    if skills:
        job_payload["skills"] = list(skills)
    extra_payload = payload.get("payload")
    if isinstance(extra_payload, Mapping):
        for key, value in extra_payload.items():
            if key not in job_payload:
                job_payload[str(key)] = value
    return job_payload


def _cron_skill_ids(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        raw_items = value.replace("\n", ",").split(",")
    elif isinstance(value, (list, tuple)):
        raw_items = [str(item) for item in value]
    else:
        raw_items = [str(value)]
    return tuple(dict.fromkeys(item.strip() for item in raw_items if item.strip()))


def _cron_job_record(job) -> dict[str, Any]:
    return {
        "jobId": job.job_id,
        "name": job.name,
        "schedule": job.schedule_text,
        "scheduleKind": job.schedule_kind,
        "jobKind": job.action_kind,
        "status": job.status,
        "profileId": job.profile_id,
        "cloneId": job.clone_id,
        "payload": dict(job.payload),
        "skills": list(_cron_skill_ids(job.payload.get("skills"))),
        "createdAt": job.created_at.isoformat(),
        "updatedAt": job.updated_at.isoformat(),
        "nextRunAt": job.next_run_at.isoformat() if job.next_run_at is not None else None,
        "lastRunAt": job.last_run_at.isoformat() if job.last_run_at is not None else None,
        "runCount": job.run_count,
        "lastSummary": job.last_summary,
    }


def _read_wsgi_body(environ: Mapping[str, Any]) -> bytes:
    body = environ.get("wsgi.input")
    if body is None:
        return b""
    raw_length = environ.get("CONTENT_LENGTH")
    try:
        length = int(str(raw_length)) if raw_length not in {None, ""} else 0
    except (TypeError, ValueError):
        length = 0
    if length <= 0:
        return b""
    return body.read(length)


def __call__(self, environ: Mapping[str, Any], start_response: Any) -> list[bytes]:
    method = str(environ.get("REQUEST_METHOD", "GET"))
    path = str(environ.get("PATH_INFO", "/"))
    payload = _read_wsgi_body(environ)
    response = self.dispatch(method, path, payload)
    start_response(
        f"{response.status_code} {'OK' if response.status_code < 400 else 'ERROR'}",
        list(response.headers),
    )
    return [_json_bytes(response.payload)]
