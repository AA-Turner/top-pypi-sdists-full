"""Goal and memory mutation methods for the API runtime app."""


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
from packages.planning import (
    PlanningService,
    normalize_goal_owner,
    normalize_goal_priority,
    normalize_goal_status,
    normalize_time_sensitivity,
)
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

def inspect_goal(self, session_id: str, goal_id: str) -> dict[str, Any]:
    graph = self._load_activity_graph(session_id)
    goal = graph.goal(goal_id)
    if goal is None:
        raise KeyError(goal_id)
    return {
        "session_id": session_id,
        "goal": goal,
        "goal_graph_revision": graph.revision_id,
        "goal_graph_updated_at": graph.updated_at,
        "goal_status_counts": graph.status_counts(),
        "goal_graph": graph,
    }

def create_goal(
    self,
    session_id: str,
    *,
    title: str,
    status: str = "active",
    priority: str = "medium",
    owner: str = "shared",
    parent_goal_id: str | None = None,
    dependency_refs: Any = None,
    evidence_refs: Any = None,
    related_memory_ids: Any = None,
    review_checkpoint: str | None = None,
    deadline: Any = None,
    time_sensitivity: str | None = None,
    reason: str | None = None,
    activate: bool | None = None,
) -> dict[str, Any]:
    normalized_title = title.strip()
    if not normalized_title:
        raise ValueError("goal title is required")
    updated_at = _now()
    revision_id = f"goal:create:{uuid4().hex}"
    graph = self.repository.load_activity_graph(session_id) or ActivityGraph(session_id=session_id)
    root_goal_id = graph.root_goal_id or graph.active_goal_id or (graph.goals[0].goal_id if graph.goals else None)
    activate_goal = (status == "active") if activate is None else _optional_bool(activate)
    normalized_status = normalize_goal_status(status, default="active")
    if activate_goal is None:
        activate_goal = normalized_status == "active"
    dependency_values = _coerce_str_tuple(dependency_refs) if dependency_refs is not None else ()
    evidence_values = _coerce_str_tuple(evidence_refs) if evidence_refs is not None else ()
    related_values = _coerce_str_tuple(related_memory_ids) if related_memory_ids is not None else ()
    new_goal = GoalNode(
        goal_id=f"goal:{uuid4().hex[:12]}",
        session_id=session_id,
        title=normalized_title,
        status="active" if activate_goal else normalized_status,
        priority=normalize_goal_priority(priority),
        owner=normalize_goal_owner(owner, default="shared"),
        parent_goal_id=parent_goal_id if parent_goal_id is not None else (root_goal_id if graph.goals else None),
        dependencies=dependency_values,
        evidence_refs=evidence_values,
        related_memory_ids=related_values,
        deadline=_optional_datetime(deadline),
        time_sensitivity=normalize_time_sensitivity(time_sensitivity),
        review_checkpoint=review_checkpoint,
        revision_id=revision_id,
        updated_at=updated_at,
    )
    active_goal = graph.active_goal()
    if activate_goal and active_goal is not None and active_goal.goal_id != new_goal.goal_id and active_goal.status == "active":
        graph = graph.transition_goal(
            active_goal.goal_id,
            status="queued",
            revision_id=revision_id,
            updated_at=updated_at,
            active_goal_id=active_goal.goal_id,
        )
    graph = graph.with_goal(new_goal)
    graph = replace(
        graph,
        root_goal_id=root_goal_id if root_goal_id is not None else new_goal.goal_id,
        active_goal_id=new_goal.goal_id if activate_goal else graph.active_goal_id,
        revision_id=revision_id,
    )
    self.repository.upsert_activity_graph(graph)
    created = graph.goal(new_goal.goal_id)
    if created is None:
        raise KeyError(new_goal.goal_id)
    return {
        "session_id": session_id,
        "reason": reason or "goal created",
        "goal": created,
        "goal_graph": graph,
    }

def inspect_memory(self, session_id: str, memory_id: str) -> dict[str, Any]:
    memory = self.memory_runtime.store.get(memory_id)
    if memory is None or memory.session_id != session_id:
        raise KeyError(memory_id)
    return {
        "session_id": session_id,
        "memory": memory,
        "memory_state": self.memory_runtime.store.state(memory_id),
        "memory_lineage": self.memory_runtime.store.lineage(memory_id),
    }

def update_goal(
    self,
    session_id: str,
    goal_id: str,
    *,
    title: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    owner: str | None = None,
    dependency_refs: Any = None,
    evidence_refs: Any = None,
    related_memory_ids: Any = None,
    review_checkpoint: str | None = None,
    deadline: Any = None,
    time_sensitivity: str | None = None,
    reason: str | None = None,
) -> dict[str, Any]:
    graph = self._load_activity_graph(session_id)
    goal = graph.goal(goal_id)
    if goal is None:
        raise KeyError(goal_id)
    original_goal = goal

    transition_dependencies = _coerce_str_tuple(dependency_refs) if dependency_refs is not None else None
    transition_evidence = _coerce_str_tuple(evidence_refs) if evidence_refs is not None else None
    transition_related = _coerce_str_tuple(related_memory_ids) if related_memory_ids is not None else None
    if status is not None or transition_dependencies is not None or transition_evidence is not None or transition_related is not None or review_checkpoint is not None:
        graph = graph.transition_goal(
            goal_id,
            status=normalize_goal_status(
                goal.status if status is None else status,
                default=normalize_goal_status(goal.status),
            ),
            revision_id=f"goal:update:{uuid4().hex}",
            updated_at=_now(),
            dependencies=transition_dependencies,
            evidence_refs=transition_evidence,
            related_memory_ids=transition_related,
            review_checkpoint=review_checkpoint,
        )
        goal = graph.goal(goal_id)
        if goal is None:
            raise KeyError(goal_id)

    updated_goal = replace(
        goal,
        title=goal.title if title is None else title,
        priority=normalize_goal_priority(
            goal.priority if priority is None else priority,
            default=normalize_goal_priority(goal.priority),
        ),
        owner=normalize_goal_owner(goal.owner if owner is None else owner, default="shared"),
        parent_goal_id=goal.parent_goal_id,
        dependencies=goal.dependencies if transition_dependencies is None else transition_dependencies,
        evidence_refs=goal.evidence_refs if transition_evidence is None else transition_evidence,
        related_memory_ids=goal.related_memory_ids if transition_related is None else transition_related,
        deadline=goal.deadline if deadline is None else _optional_datetime(deadline),
        time_sensitivity=goal.time_sensitivity if time_sensitivity is None else normalize_time_sensitivity(time_sensitivity),
        review_checkpoint=goal.review_checkpoint if review_checkpoint is None else review_checkpoint,
        revision_id=f"goal:update:{uuid4().hex}",
        updated_at=_now(),
    )
    graph = graph.with_goal(updated_goal)
    self.repository.upsert_activity_graph(graph)
    return {
        "session_id": session_id,
        "reason": reason or "goal updated",
        "before": original_goal,
        "goal": updated_goal,
        "goal_graph": graph,
    }

def delete_goal(self, session_id: str, goal_id: str, *, reason: str = "") -> dict[str, Any]:
    graph = self._load_activity_graph(session_id)
    goal = graph.goal(goal_id)
    if goal is None:
        raise KeyError(goal_id)
    updated_graph = graph.transition_goal(
        goal_id,
        status="dropped",
        revision_id=f"goal:delete:{uuid4().hex}",
        updated_at=_now(),
    )
    self.repository.upsert_activity_graph(updated_graph)
    updated_goal = updated_graph.goal(goal_id)
    if updated_goal is None:
        raise KeyError(goal_id)
    return {
        "session_id": session_id,
        "reason": reason or "goal deleted",
        "before": goal,
        "goal": updated_goal,
        "goal_graph": updated_graph,
    }

def correct_memory(
    self,
    session_id: str,
    memory_id: str,
    *,
    corrected_content: str,
    reason: str = "",
    actor: str = "user",
) -> dict[str, Any]:
    result = self.memory_runtime.correct_memory(memory_id, corrected_content, actor=actor, reason=reason)
    if result.decision.target_memory_id is None:
        raise KeyError(memory_id)
    original = self.memory_runtime.store.get(memory_id)
    if original is None or original.session_id != session_id:
        raise KeyError(memory_id)
    return {
        "session_id": session_id,
        "decision": result.decision,
        "memory": result.record,
        "memory_state": self.memory_runtime.store.state(memory_id),
        "memory_lineage": self.memory_runtime.store.lineage(memory_id),
    }

def delete_memory(
    self,
    session_id: str,
    memory_id: str,
    *,
    reason: str,
    actor: str = "user",
) -> dict[str, Any]:
    original = self.memory_runtime.store.get(memory_id)
    if original is None or original.session_id != session_id:
        raise KeyError(memory_id)
    result = self.memory_runtime.delete_memory(memory_id, actor=actor, reason=reason)
    return {
        "session_id": session_id,
        "decision": result.decision,
        "memory": original,
        "memory_state": self.memory_runtime.store.state(memory_id),
        "memory_lineage": self.memory_runtime.store.lineage(memory_id),
    }

def pin_memory(
    self,
    session_id: str,
    memory_id: str,
    *,
    pinned: bool,
    reason: str = "",
    actor: str = "user",
) -> dict[str, Any]:
    original = self.memory_runtime.store.get(memory_id)
    if original is None or original.session_id != session_id:
        raise KeyError(memory_id)
    result = (
        self.memory_runtime.pin_memory(memory_id, actor=actor, reason=reason)
        if pinned
        else self.memory_runtime.unpin_memory(memory_id, actor=actor, reason=reason)
    )
    record = result.record
    if record is None:
        raise RuntimeError(result.decision.reason)
    return {
        "session_id": session_id,
        "decision": result.decision,
        "memory": record,
        "memory_state": self.memory_runtime.store.state(memory_id),
        "memory_lineage": self.memory_runtime.store.lineage(memory_id),
    }
