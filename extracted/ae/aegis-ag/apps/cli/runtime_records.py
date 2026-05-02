"""Session, goal, memory, and profile persistence methods for the CLI runtime."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
import json
from pathlib import Path
from typing import Any
from uuid import uuid4

from packages.contracts.runtime import EvidenceRetrievalRequest, EvidenceRetrievalResult, GoalNode, MemoryRecord, SessionState, ActivityGraph
from packages.planning import (
    normalize_goal_owner,
    normalize_goal_priority,
    normalize_goal_status,
    normalize_time_sensitivity,
)
from packages.state import (
    LoadedProfile,
    build_canonical_profile_state,
    load_persisted_canonical_state,
    overlay_canonical_profile_state,
    profile_manifest_payload,
    sync_canonical_profile_state,
    write_profile_manifest,
)

from .runtime_cognition import (
    _goal_ids_for_memory_search,
    _list_scope_memories,
    _memory_query_seed,
    _memory_query_with_relationship,
    _memory_scope_reason,
    _memory_scope_session_ids,
)
from .runtime_snapshot import load_snapshot_intent
from .runtime_support import CloneSummary, _PlanningMemoryRecovery, _coerce_str_tuple, _optional_datetime, _utc_now

class CliRuntimeRecordsMixin:
    def inspect_session(self, session_id: str) -> SessionState:
        return self._load_session(session_id)

    def recent_sessions(self, *, limit: int = 5) -> tuple[SessionState, ...]:
        return self._list_sessions(limit=limit)

    def list_clones(self, *, limit: int = 12) -> tuple[CloneSummary, ...]:
        grouped: dict[str, list[SessionState]] = {}
        for session in self._list_sessions():
            grouped.setdefault(self.clone_id_for_session(session), []).append(session)
        clones = tuple(
            CloneSummary(
                clone_id=clone_id,
                latest_session_id=sessions[0].session_id,
                latest_status=sessions[0].status,
                updated_at=sessions[0].updated_at,
                session_count=len(sessions),
            )
            for clone_id, sessions in grouped.items()
        )
        ordered = tuple(sorted(clones, key=lambda item: (item.updated_at, item.clone_id), reverse=True))
        return ordered[:limit]

    def latest_session_for_clone(self, clone_id: str) -> SessionState | None:
        target = clone_id.strip()
        if not target:
            return None
        for session in self._list_sessions():
            if self.clone_id_for_session(session) == target:
                return session
        return None

    def session_ids_for_clone(self, clone_id: str) -> tuple[str, ...]:
        target = clone_id.strip()
        if not target:
            return ()
        return tuple(
            session.session_id
            for session in self._list_sessions()
            if self.clone_id_for_session(session) == target
        )

    def delete_clone(self, clone_id: str) -> int:
        session_ids = self.session_ids_for_clone(clone_id)
        if not session_ids:
            return 0
        return self.repository.delete_sessions(session_ids, delete_orphaned_profiles=True)

    def delete_all_clones(self) -> tuple[int, int]:
        clones = self.list_clones(limit=4096)
        session_ids = tuple(session.session_id for session in self._list_sessions())
        if not session_ids:
            return (0, 0)
        deleted_sessions = self.repository.delete_sessions(session_ids, delete_orphaned_profiles=True)
        return (len(clones), deleted_sessions)

    def clone_id_for_session(self, session: SessionState) -> str:
        if session.workspace_id:
            return session.workspace_id
        lineage = self.session_service.lineage(session.session_id)
        origin = lineage[0].session_id if lineage else session.session_id
        return f"clone-{origin[:8]}"

    def _list_sessions(self, *, limit: int | None = None) -> tuple[SessionState, ...]:
        with self.repository.connection() as connection:
            query = """
                SELECT session_id
                FROM sessions
                ORDER BY updated_at DESC, started_at DESC, session_id DESC
            """
            params: tuple[object, ...] = ()
            if limit is not None:
                query += "\nLIMIT ?"
                params = (limit,)
            rows = connection.execute(query, params).fetchall()
        sessions: list[SessionState] = []
        for row in rows:
            session = self.repository.load_session(str(row["session_id"]))
            if session is not None:
                sessions.append(session)
        return tuple(sessions)

    def latest_session(self) -> SessionState | None:
        sessions = self.recent_sessions(limit=1)
        if not sessions:
            return None
        return sessions[0]

    def _planning_memory_recovery(
        self,
        session: SessionState,
        goal_graph: ActivityGraph,
        *,
        limit: int = 8,
    ) -> _PlanningMemoryRecovery:
        relationship = self.inspect_relationship(profile_id=session.profile_id)
        query = _memory_query_with_relationship(goal_graph, relationship=relationship)
        goal_ids = _goal_ids_for_memory_search(goal_graph)
        scope_session_ids = _memory_scope_session_ids(self.repository, session)
        scope_reason = _memory_scope_reason(
            session=session,
            goal_graph=goal_graph,
            relationship=relationship,
            scope_session_ids=scope_session_ids,
        )
        request = EvidenceRetrievalRequest(
            session_id=session.session_id,
            profile_id=session.profile_id,
            workspace_id=session.workspace_id,
            lineage_session_ids=scope_session_ids,
            work_item_ids=goal_ids,
            query=query,
            scopes=("session", "lineage", "workspace") if session.workspace_id else ("session", "lineage"),
            latency_mode="fast",
            limit=limit,
            scope_reason=scope_reason,
            relationship_hints=relationship.continuity_notes,
        )
        retrieval = self.memory_runtime.retrieve_evidence(request)
        focused_goals = tuple(
            goal
            for goal_id in goal_ids
            if (goal := goal_graph.goal(goal_id)) is not None
        )
        artifact_ids = tuple(
            dict.fromkeys(
                evidence_ref
                for goal in focused_goals
                for evidence_ref in goal.evidence_refs
                if evidence_ref
            )
        )
        constraint_ids = tuple(
            dict.fromkeys(
                dependency_ref
                for goal in focused_goals
                for dependency_ref in ((*goal.dependency_refs, *((goal.review_checkpoint,) if goal.review_checkpoint else ())))
                if dependency_ref
            )
        )
        resume_packet = self.memory_runtime.build_resume_packet(
            request,
            retrieval,
            next_move="wake-next-step",
            artifact_ids=artifact_ids,
            constraint_ids=constraint_ids,
        )
        memories = tuple(candidate.memory for candidate in retrieval.candidates)
        if memories:
            return _PlanningMemoryRecovery(
                memories=memories,
                query=query,
                goal_ids=goal_ids,
                scope_session_ids=retrieval.scope_session_ids,
                scope_reason=retrieval.scope_reason,
                retrieval=retrieval,
                resume_packet=resume_packet,
            )
        listed = _list_scope_memories(self.repository, scope_session_ids=scope_session_ids)
        fallback = listed[-limit:] if listed else ()
        return _PlanningMemoryRecovery(
            memories=fallback,
            query=query,
            goal_ids=goal_ids,
            scope_session_ids=scope_session_ids,
            scope_reason=scope_reason,
            retrieval=retrieval,
            resume_packet=resume_packet,
        )

    def _planning_memories(
        self,
        session: SessionState,
        goal_graph: ActivityGraph,
        *,
        limit: int = 8,
    ) -> tuple[MemoryRecord, ...]:
        return self._planning_memory_recovery(session, goal_graph, limit=limit).memories

    def inspect_goals(self, session_id: str) -> tuple[GoalNode, ...]:
        graph = self.repository.load_activity_graph(session_id)
        if graph is None:
            return ()
        return graph.goals

    def inspect_memories(self, session_id: str) -> tuple[MemoryRecord, ...]:
        return tuple(self.memory_runtime.store.list(session_id=session_id))

    def search_memories(self, session_id: str, query: str, *, limit: int = 5) -> tuple[MemoryRecord, ...]:
        retrieval = self.retrieve_evidence(session_id, query, limit=limit)
        return tuple(candidate.memory for candidate in retrieval.candidates)

    def recall(self, session_id: str, query: str, *, limit: int = 5) -> EvidenceRetrievalResult:
        return self.retrieve_evidence(session_id, query, limit=limit)

    def retrieve_evidence(
        self,
        session_id: str,
        query: str,
        *,
        goal_ids: tuple[str, ...] = (),
        limit: int = 5,
        scope_session_ids: tuple[str, ...] = (),
        scope_reason: str = "",
        scopes: tuple[str, ...] = (),
    ) -> EvidenceRetrievalResult:
        session = self._load_session(session_id)
        goal_graph = self.repository.load_activity_graph(session_id)
        resolved_goal_ids = goal_ids or _goal_ids_for_memory_search(goal_graph)
        resolved_scope_session_ids = _memory_scope_session_ids(self.repository, session)
        requested_scopes = scopes or (("session", "lineage") if len(resolved_scope_session_ids) > 1 else ("session",))
        request = EvidenceRetrievalRequest(
            session_id=session.session_id,
            profile_id=session.profile_id,
            workspace_id=session.workspace_id,
            lineage_session_ids=scope_session_ids or resolved_scope_session_ids,
            work_item_ids=resolved_goal_ids,
            query=query.strip() or _memory_query_seed(goal_graph),
            scopes=requested_scopes,
            latency_mode="fast",
            limit=limit,
            scope_reason=scope_reason,
            relationship_hints=(
                self.inspect_relationship(profile_id=session.profile_id).continuity_notes
                if session.profile_id
                else ()
            ),
        )
        return self.memory_runtime.retrieve_evidence(request)

    def inspect_goal(self, session_id: str, goal_id: str) -> GoalNode:
        graph = self.repository.load_activity_graph(session_id)
        if graph is None:
            raise KeyError(session_id)
        goal = graph.goal(goal_id)
        if goal is None:
            raise KeyError(goal_id)
        return goal

    def inspect_memory(self, session_id: str, memory_id: str) -> MemoryRecord:
        memory = self.memory_runtime.store.get(memory_id)
        if memory is None or memory.session_id != session_id:
            raise KeyError(memory_id)
        return memory

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
    ) -> GoalNode:
        normalized_title = title.strip()
        if not normalized_title:
            raise ValueError("goal title is required")
        self._authorize_write(
            operation="cli.goal.create",
            session_id=session_id,
            description=reason or normalized_title,
            metadata={"title": normalized_title},
        )
        updated_at = _utc_now()
        revision_id = f"goal:create:{uuid4().hex}"
        graph = self.repository.load_activity_graph(session_id) or ActivityGraph(session_id=session_id)
        root_goal_id = graph.root_goal_id or graph.active_goal_id or (graph.goals[0].goal_id if graph.goals else None)
        normalized_status = normalize_goal_status(status, default="active")
        activate_goal = (normalized_status == "active") if activate is None else activate
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
        return created

    def update_goal(
        self,
        session_id: str,
        goal_id: str,
        *,
        title: str | None = None,
        status: str | None = None,
        priority: str | None = None,
        reason: str | None = None,
    ) -> tuple[GoalNode, GoalNode, str]:
        self._authorize_write(
            operation="cli.goal.update",
            session_id=session_id,
            description=reason or title or status or priority or goal_id,
            metadata={"goal_id": goal_id},
        )
        graph = self.repository.load_activity_graph(session_id)
        if graph is None:
            raise KeyError(session_id)
        goal = graph.goal(goal_id)
        if goal is None:
            raise KeyError(goal_id)
        before = goal
        if status is not None:
            graph = graph.transition_goal(
                goal_id,
                status=normalize_goal_status(status, default=normalize_goal_status(goal.status)),
                revision_id=f"goal:update:{uuid4().hex}",
                updated_at=_utc_now(),
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
            revision_id=f"goal:update:{uuid4().hex}",
            updated_at=_utc_now(),
        )
        graph = graph.with_goal(updated_goal)
        self.repository.upsert_activity_graph(graph)
        return before, updated_goal, reason or "goal updated"

    def delete_goal(self, session_id: str, goal_id: str, *, reason: str) -> tuple[GoalNode, GoalNode]:
        self._authorize_write(
            operation="cli.goal.delete",
            session_id=session_id,
            description=reason,
            is_destructive=True,
            metadata={"goal_id": goal_id},
        )
        graph = self.repository.load_activity_graph(session_id)
        if graph is None:
            raise KeyError(session_id)
        goal = graph.goal(goal_id)
        if goal is None:
            raise KeyError(goal_id)
        before = goal
        graph = graph.transition_goal(
            goal_id,
            status="dropped",
            revision_id=f"goal:delete:{uuid4().hex}",
            updated_at=_utc_now(),
        )
        self.repository.upsert_activity_graph(graph)
        updated = graph.goal(goal_id)
        if updated is None:
            raise KeyError(goal_id)
        return before, updated

    def correct_memory(
        self,
        session_id: str,
        memory_id: str,
        *,
        corrected_content: str,
        reason: str = "",
    ) -> tuple[MemoryRecord | None, MemoryRecord | None, str, str | None]:
        self._authorize_write(
            operation="cli.memory.correct",
            session_id=session_id,
            description=reason or corrected_content,
            metadata={"memory_id": memory_id},
        )
        original = self.memory_runtime.store.get(memory_id)
        if original is None or original.session_id != session_id:
            raise KeyError(memory_id)
        result = self.memory_runtime.correct_memory(memory_id, corrected_content, reason=reason)
        corrected = result.record
        return original, corrected, result.decision.reason, self.memory_runtime.store.lineage(memory_id)

    def delete_memory(self, session_id: str, memory_id: str, *, reason: str) -> tuple[MemoryRecord, str | None]:
        self._authorize_write(
            operation="cli.memory.delete",
            session_id=session_id,
            description=reason,
            is_destructive=True,
            metadata={"memory_id": memory_id},
        )
        original = self.memory_runtime.store.get(memory_id)
        if original is None or original.session_id != session_id:
            raise KeyError(memory_id)
        result = self.memory_runtime.delete_memory(memory_id, reason=reason)
        return original, result.decision.reason

    def pin_memory(self, session_id: str, memory_id: str, *, reason: str = "") -> tuple[MemoryRecord, str]:
        self._authorize_write(
            operation="cli.memory.pin",
            session_id=session_id,
            description=reason or memory_id,
            metadata={"memory_id": memory_id},
        )
        record = self.memory_runtime.store.get(memory_id)
        if record is None or record.session_id != session_id:
            raise KeyError(memory_id)
        result = self.memory_runtime.pin_memory(memory_id, reason=reason)
        if result.record is None:
            raise RuntimeError(result.decision.reason)
        return result.record, result.decision.reason

    def unpin_memory(self, session_id: str, memory_id: str, *, reason: str = "") -> tuple[MemoryRecord, str]:
        self._authorize_write(
            operation="cli.memory.unpin",
            session_id=session_id,
            description=reason or memory_id,
            metadata={"memory_id": memory_id},
        )
        record = self.memory_runtime.store.get(memory_id)
        if record is None or record.session_id != session_id:
            raise KeyError(memory_id)
        result = self.memory_runtime.unpin_memory(memory_id, reason=reason)
        if result.record is None:
            raise RuntimeError(result.decision.reason)
        return result.record, result.decision.reason

    def memory_lineage(self, memory_id: str) -> str | None:
        return self.memory_runtime.store.lineage(memory_id)

    def memory_state(self, memory_id: str) -> str | None:
        return self.memory_runtime.store.state(memory_id)

    def _load_profile_source(self, profile_id: str) -> LoadedProfile:
        return self.profile_loader.load(profile_id=profile_id)

    def _load_profile(self, profile_id: str) -> LoadedProfile:
        loaded = self._load_profile_source(profile_id)
        persisted = load_persisted_canonical_state(self.repository, profile_id)
        return overlay_canonical_profile_state(
            loaded,
            identity_record=persisted.clone_identity,
            user_card=persisted.user_card,
            relationship_record=persisted.relationship_memory,
        )

    def _load_session(self, session_id: str) -> SessionState:
        session = self.repository.load_session(session_id)
        if session is None:
            raise KeyError(session_id)
        return session

    def _load_profile_manifest(self) -> dict[str, Any]:
        manifest_path = self.paths.profile_dir / "profile.json"
        if not manifest_path.exists():
            return {}
        return json.loads(manifest_path.read_text(encoding="utf-8"))

    def _write_profile_manifest(self, manifest: Mapping[str, Any]) -> None:
        write_profile_manifest(self.paths.profile_dir, manifest)

    def _persist_profile(
        self,
        loaded_profile: LoadedProfile,
        *,
        sync_source: str = "profile.persist",
    ) -> LoadedProfile:
        previous_canonical = load_persisted_canonical_state(self.repository, loaded_profile.state.profile_id)
        manifest = profile_manifest_payload(
            loaded_profile,
            existing_manifest=loaded_profile.manifest,
        )
        profile_dir = Path(loaded_profile.profile_dir)
        write_profile_manifest(profile_dir, manifest)
        self.repository.upsert_profile(loaded_profile.state)
        canonical_bundle = build_canonical_profile_state(loaded_profile)
        sync_canonical_profile_state(
            self.repository,
            canonical_bundle,
            previous=previous_canonical,
            sync_source=sync_source,
        )
        reloaded = self._load_profile(loaded_profile.state.profile_id)
        self.repository.upsert_profile(reloaded.state)
        latest_session = self.latest_session()
        if latest_session is not None and latest_session.profile_id == reloaded.state.profile_id:
            self._write_snapshot(
                profile=reloaded.state,
                session=latest_session,
                goals=self.inspect_goals(latest_session.session_id),
                memories=self.inspect_memories(latest_session.session_id),
                plan=None,
                execution=None,
                delivery=None,
                stages=(),
                event=None,
                clone_text=reloaded.clone_text,
                intent=load_snapshot_intent(self, session_id=latest_session.session_id),
            )
        return reloaded
