"""Profile, continuity, and canonical identity methods for the CLI runtime."""

from __future__ import annotations

from dataclasses import replace
from uuid import uuid4

from packages.context import ContextAssemblyResult
from packages.contracts.runtime import ActivityGraph, CloneIdentityRecord, RelationshipMemoryRecord, UserCardRecord
from packages.continuity import ContinuityProjectionService
from packages.kernel.memory_recovery import memory_retrieval_scopes
from packages.learning import LearningRuntime
from packages.operator import (
    MemoryOperatorDetail,
    MemorySearchHit,
    ProcedureOperatorDetail,
    build_activity_operator_surface,
    build_audit_surface,
    build_memory_operator_surface,
    build_procedure_operator_surface,
    build_profile_operator_surface,
)
from packages.planning.runtime import PlanningService
from packages.state import (
    CompanionSettings,
    LoadedProfile,
    apply_user_card_update,
    build_canonical_profile_state,
    user_profile_updates,
    is_companion_mode,
    load_persisted_canonical_state,
    normalize_profile_mode,
    render_user_card_profile_text,
    resolve_personality_preset,
)
from packages.security import ApprovalClass, SecurityRequest, evaluate_with_telemetry

from .runtime_cognition import _CliContextCapability
from .runtime_extensions import _PreviewTelemetrySink
from .runtime_snapshot import load_snapshot_intent
from .runtime_support import ContinuityStatus, _normalized_profile_text

class CliRuntimeProfileMixin:
    def _load_activity_graph_or_none(self, session_id: str) -> ActivityGraph | None:
        try:
            return self.repository.load_activity_graph(session_id)
        except ValueError:
            return None

    def inspect_continuity(self, *, session_id: str | None = None) -> ContinuityStatus:
        session = self.inspect_session(session_id) if session_id is not None else self.latest_session()
        if session is None:
            raise KeyError("latest-session")
        profile = self._load_profile(session.profile_id)
        lineage = self.session_service.lineage(session.session_id)
        voice_report = self.voice_doctor(profile_id=session.profile_id)
        goal_graph = self._load_activity_graph_or_none(session.session_id)
        active_goal_id = goal_graph.active_goal_id if goal_graph is not None else None
        identity = self.inspect_identity(profile_id=session.profile_id)
        relationship = self.inspect_relationship(profile_id=session.profile_id)
        continuity_report = ContinuityProjectionService(self.session_service).inspect(
            profile,
            session,
            lineage=lineage,
            active_goal_id=active_goal_id,
            identity_record=identity,
            relationship_record=relationship,
        )
        if goal_graph is None:
            wake_action = "idle"
            wake_summary = "No durable wake action is available yet; start or resume a goal-bearing session first."
            wake_factors: tuple[str, ...] = ("no-goal-graph",)
        else:
            recovery = self._planning_memory_recovery(session, goal_graph)
            decision, _ = PlanningService().wake_next_step(
                session=session,
                graph=goal_graph,
                memories=recovery.memories,
                initiative_hint=identity.initiative,
                continuity_notes=relationship.continuity_notes,
            )
            wake_action = decision.selected_move.kind
            wake_summary = decision.rationale.summary
            wake_factors = tuple((*decision.rationale.factors, f"memory-scope={','.join(recovery.scope_session_ids)}"))
        return ContinuityStatus(
            profile=profile,
            session=session,
            relationship_policy=continuity_report.relationship_policy,
            governance_summary=continuity_report.governance.identity.governance_summary,
            proactive_summary=continuity_report.governance.identity.proactive_summary,
            initiative=continuity_report.initiative,
            wake_action=wake_action,
            wake_summary=wake_summary,
            wake_factors=wake_factors,
            reengagement_style=continuity_report.reengagement_style,
            reengagement_prompt=continuity_report.reengagement_prompt,
            continuity_summary=continuity_report.summary,
            voice_status=str(voice_report["status"]),
            voice_identity_binding=str(
                voice_report.get("identity_binding") or continuity_report.voice_identity_binding
            ),
            voice_identity_summary=str(
                voice_report.get("voice_identity_summary")
                or continuity_report.governance.identity.voice_identity_summary
            ),
        )

    def inspect_context_frame(self, session_id: str) -> ContextAssemblyResult:
        session = self.inspect_session(session_id)
        goals = self.inspect_goals(session_id)
        memories = self.inspect_memories(session_id)
        intent = load_snapshot_intent(self, session_id=session_id)
        capability = _CliContextCapability(
            profile_loader=self.profile_loader,
            repository=self.repository,
            prompt_mode="full",
            snapshot_path=self.snapshot_path,
            total_tokens=self.active_provider_context_window(),
            tool_runtime=self.tool_runtime,
            skill_runtime=self.skill_runtime,
            skill_hub=self.skill_hub,
            workspace_dir=self.paths.workspace_dir,
        )
        return capability.assemble_detailed(session, goals, memories, intent=intent)

    def inspect_profile_surface(self, session_id: str):
        session = self.inspect_session(session_id)
        profile = self._load_profile(session.profile_id)
        return build_profile_operator_surface(
            session_id=session_id,
            profile_id=profile.state.profile_id,
            profile_mode=profile.state.mode,
            identity=self.inspect_identity(session_id=session_id),
            user=self.inspect_user(session_id=session_id),
            relationship=self.inspect_relationship(session_id=session_id),
        )

    def patch_profile_surface(self, session_id: str, payload: dict[str, object]):
        if any(
            key in payload
            for key in {"display_name", "name", "personality_preset", "initiative", "charter_text", "text", "content", "clear_charter"}
        ):
            self.update_identity_state(
                session_id=session_id,
                display_name=str(payload.get("display_name") or payload.get("name") or "").strip() or None,
                personality_preset=str(payload.get("personality_preset") or "").strip() or None,
                initiative=str(payload.get("initiative") or "").strip() or None,
                charter_text=str(payload.get("charter_text") or payload.get("text") or payload.get("content") or "").strip() or None,
                clear_charter=bool(payload.get("clear_charter", False)),
            )
        if any(key in payload for key in {"user_text", "user_content", "user_fields", "user_append", "user_clear"}):
            self.update_user_state(
                session_id=session_id,
                text=str(payload.get("user_text") or payload.get("user_content") or "").strip() or None,
                fields=payload.get("user_fields") if isinstance(payload.get("user_fields"), dict) else None,
                append=bool(payload.get("user_append", False)),
                clear=bool(payload.get("user_clear", False)),
            )
        if any(key in payload for key in {"relationship_text", "relationship_content", "relationship_append", "relationship_clear"}):
            self.update_relationship_state(
                session_id=session_id,
                text=str(payload.get("relationship_text") or payload.get("relationship_content") or "").strip() or None,
                append=bool(payload.get("relationship_append", False)),
                clear=bool(payload.get("relationship_clear", False)),
            )
        return self.inspect_profile_surface(session_id)

    def inspect_activity_surface(self, session_id: str):
        session = self.inspect_session(session_id)
        continuity = self.inspect_continuity(session_id=session_id)
        graph = self._load_activity_graph_or_none(session_id)
        intent = load_snapshot_intent(self, session_id=session_id)
        opened_scopes = ()
        if intent is not None:
            continuity_state = self._session_continuity_state(session_id, session=session, active_goal_id=graph.active_goal_id if graph is not None else None)
            opened_scopes = memory_retrieval_scopes(session, continuity=continuity_state, intent=intent)
        embedding_status = str(self.provider_summary().get("embedding_bootstrap_status") or "").strip() or None
        return build_activity_operator_surface(
            session_id=session_id,
            active_goal_id=graph.active_goal_id if graph is not None else None,
            active_goal_reason=continuity.wake_summary,
            wake_action=continuity.wake_action,
            wake_factors=continuity.wake_factors,
            goal_graph_revision=graph.revision_id if graph is not None else None,
            goals=graph.goals if graph is not None else (),
            intent=intent,
            opened_scopes=opened_scopes,
            embedding_status=embedding_status,
        )

    def inspect_memory_surface(self, session_id: str):
        memories = tuple(
            MemoryOperatorDetail(
                memory=memory,
                state=self.memory_state(memory.memory_id),
                lineage=self.memory_lineage(memory.memory_id),
            )
            for memory in self.inspect_memories(session_id)
        )
        return build_memory_operator_surface(session_id=session_id, memories=memories)

    def search_memory_surface(self, session_id: str, *, query: str, limit: int = 5):
        retrieval = self.retrieve_evidence(session_id, query, limit=limit)
        memories = tuple(
            MemoryOperatorDetail(
                memory=memory,
                state=self.memory_state(memory.memory_id),
                lineage=self.memory_lineage(memory.memory_id),
            )
            for memory in self.inspect_memories(session_id)
        )
        return build_memory_operator_surface(
            session_id=session_id,
            memories=memories,
            search_query=query,
            search_hits=tuple(
                MemorySearchHit(
                    memory=candidate.memory,
                    score=candidate.score,
                    reasons=tuple(reason.detail for reason in candidate.reasons if reason.detail),
                )
                for candidate in retrieval.candidates
            ),
            scope_reason=retrieval.scope_reason,
            index_policy=retrieval.index_policy,
        )

    def inspect_procedure_surface(self, session_id: str, *, minimum_support: int = 2):
        session = self.inspect_session(session_id)
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

    def patch_procedure_surface(self, session_id: str, procedure_id: str, payload: dict[str, object]):
        session = self.inspect_session(session_id)
        learning = LearningRuntime(self.repository)
        updated = learning.patch_procedure(
            profile_id=session.profile_id,
            procedure_id=procedure_id,
            title=str(payload.get("title") or "").strip() or None,
            summary=str(payload.get("summary") or payload.get("content") or "").strip() or None,
            trigger_refs=self._coerce_str_tuple(payload.get("trigger_refs")) if payload.get("trigger_refs") is not None else None,
            status=str(payload.get("status") or "").strip() or None,
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
        session = self.inspect_session(session_id)
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
        activity = self.inspect_activity_surface(session_id)
        intent = load_snapshot_intent(self, session_id=session_id)
        return build_audit_surface(
            session_id=session_id,
            active_goal_id=activity.active_goal_id,
            active_goal_reason=activity.active_goal_reason,
            context_result=self.inspect_context_frame(session_id),
            intent=intent,
            opened_scopes=activity.intent.opened_scopes if activity.intent is not None else (),
            embedding_status=(
                activity.intent.embedding_status
                if activity.intent is not None
                else None
            ),
        )

    def _coerce_str_tuple(self, value: object) -> tuple[str, ...]:
        if value is None:
            return ()
        if isinstance(value, str):
            stripped = value.strip()
            return tuple(part.strip() for part in stripped.split(",") if part.strip()) if stripped else ()
        if isinstance(value, (list, tuple)):
            return tuple(str(item).strip() for item in value if str(item).strip())
        return (str(value).strip(),) if str(value).strip() else ()

    def _session_continuity_state(self, session_id: str, *, session, active_goal_id: str | None):
        return self.session_service.continuity_state(
            session,
            lineage=self.session_service.lineage(session_id),
            active_goal_id=active_goal_id,
        )

    def inspect_profile(self, profile_id: str) -> LoadedProfile:
        return self._load_profile(profile_id)

    def inspect_identity(
        self,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
    ) -> CloneIdentityRecord:
        resolved_profile_id = self._resolve_extension_profile_id(
            session_id=session_id,
            profile_id=profile_id,
        )
        persisted = load_persisted_canonical_state(self.repository, resolved_profile_id).clone_identity
        if persisted is not None:
            return persisted
        return build_canonical_profile_state(self._load_profile(resolved_profile_id)).clone_identity

    def inspect_user(
        self,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
    ) -> UserCardRecord:
        resolved_profile_id = self._resolve_extension_profile_id(
            session_id=session_id,
            profile_id=profile_id,
        )
        persisted = load_persisted_canonical_state(self.repository, resolved_profile_id).user_card
        if persisted is not None:
            return persisted
        return build_canonical_profile_state(self._load_profile(resolved_profile_id)).user_card

    def inspect_relationship(
        self,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
    ) -> RelationshipMemoryRecord:
        resolved_profile_id = self._resolve_extension_profile_id(
            session_id=session_id,
            profile_id=profile_id,
        )
        persisted = load_persisted_canonical_state(self.repository, resolved_profile_id).relationship_memory
        if persisted is not None:
            return persisted
        return build_canonical_profile_state(self._load_profile(resolved_profile_id)).relationship_memory

    def current_profile(self) -> LoadedProfile:
        return self._load_profile(self.profile_loader.load_state().profile_id)

    def _authorize_write(
        self,
        *,
        operation: str,
        session_id: str | None = None,
        description: str | None = None,
        is_destructive: bool = False,
        metadata: Mapping[str, str] | None = None,
    ) -> None:
        result = evaluate_with_telemetry(
            self.security_policy,
            SecurityRequest(
                request_id=f"req:cli:{uuid4().hex[:8]}",
                approval_class=ApprovalClass.WRITE,
                operation=operation,
                session_id=session_id,
                description=description,
                consent_given=True,
                is_destructive=is_destructive,
                metadata=dict(metadata or {}),
            ),
            _PreviewTelemetrySink(self.snapshot_path),
            source="cli.operator",
        )
        if not result.approved:
            raise PermissionError(result.rationale)

    def update_identity(
        self,
        *,
        profile_id: str | None = None,
        display_name: str | None = None,
        mode: str | None = None,
    ) -> LoadedProfile:
        loaded = self._load_profile_source(profile_id or self.current_profile().state.profile_id)
        self._authorize_write(
            operation="cli.identity.update",
            session_id=self.latest_session().session_id if self.latest_session() is not None else None,
            description=display_name or loaded.state.display_name,
            metadata={"profile_id": loaded.state.profile_id},
        )
        resolved_mode = loaded.state.mode if mode is None else normalize_profile_mode(mode)
        resolved_companion = loaded.companion
        if mode is not None and not is_companion_mode(resolved_mode):
            resolved_companion = None
        elif is_companion_mode(resolved_mode) and resolved_companion is None:
            resolved_companion = CompanionSettings()
        updated_state = replace(
            loaded.state,
            display_name=loaded.state.display_name if display_name is None else display_name,
            mode=resolved_mode,
        )
        return self._persist_profile(
            LoadedProfile(
                state=updated_state,
                companion=resolved_companion,
                profile_dir=loaded.profile_dir,
                manifest_path=loaded.manifest_path,
                clone_text=loaded.clone_text,
                user_profile_text=loaded.user_profile_text,
                aegis_path=loaded.aegis_path,
                user_profile_path=loaded.user_profile_path,
                manifest=dict(loaded.manifest),
            ),
            sync_source="identity.update",
        )

    def update_companion_settings(
        self,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
        text_first: bool | None = None,
        initiative: str | None = None,
        personality_preset: str | None = None,
        personality: tuple[str, ...] | None = None,
        allow_voice_extension: bool | None = None,
        notes: tuple[str, ...] | None = None,
    ) -> LoadedProfile:
        resolved_profile_id = self._resolve_extension_profile_id(
            session_id=session_id,
            profile_id=profile_id,
        )
        loaded = self._load_profile(resolved_profile_id)
        self._authorize_write(
            operation="cli.personality.update",
            session_id=session_id or (self.latest_session().session_id if self.latest_session() is not None else None),
            description=personality_preset or initiative or "update identity settings",
            metadata={"profile_id": loaded.state.profile_id},
        )
        current = loaded.companion or CompanionSettings()
        resolved_preset = (
            current.personality_preset
            if personality_preset is None
            else resolve_personality_preset(personality_preset, mode=loaded.state.mode).preset_id
        )
        resolved_personality = current.personality if personality is None else personality
        if personality_preset is not None and personality is None:
            resolved_personality = resolve_personality_preset(resolved_preset, mode=loaded.state.mode).traits
        updated_companion = CompanionSettings(
            text_first=current.text_first if text_first is None else text_first,
            personality_preset=resolved_preset,
            personality=resolved_personality,
            initiative=current.initiative if initiative is None else initiative,
            preserve_relationship_timeline=current.preserve_relationship_timeline,
            preserve_preferences=current.preserve_preferences,
            preserve_corrections=current.preserve_corrections,
            preserve_emotional_context=current.preserve_emotional_context,
            allow_voice_extension=(
                current.allow_voice_extension
                if allow_voice_extension is None
                else allow_voice_extension
            ),
            notes=current.notes if notes is None else notes,
        )
        return self._persist_profile(
            LoadedProfile(
                state=loaded.state,
                companion=updated_companion,
                profile_dir=loaded.profile_dir,
                manifest_path=loaded.manifest_path,
                clone_text=loaded.clone_text,
                user_profile_text=loaded.user_profile_text,
                aegis_path=loaded.aegis_path,
                user_profile_path=loaded.user_profile_path,
                manifest=dict(loaded.manifest),
            ),
            sync_source="identity.settings.update",
        )

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
    ) -> CloneIdentityRecord:
        resolved_profile_id = self._resolve_extension_profile_id(session_id=session_id, profile_id=profile_id)
        if display_name is not None:
            self.update_identity(profile_id=resolved_profile_id, display_name=display_name)
        loaded = self._load_profile(resolved_profile_id)
        if personality_preset is not None or initiative is not None:
            if loaded.state.mode != "companion":
                loaded = self.update_identity(profile_id=resolved_profile_id, mode="companion")
            loaded = self.update_companion_settings(
                profile_id=resolved_profile_id,
                personality_preset=personality_preset,
                initiative=initiative,
            )
        if clear_charter or charter_text is not None:
            self._authorize_write(
                operation="cli.identity.surface.update",
                session_id=session_id or (self.latest_session().session_id if self.latest_session() is not None else None),
                description="update identity charter",
                metadata={"profile_id": resolved_profile_id},
            )
            loaded = self._persist_profile(
                LoadedProfile(
                    state=loaded.state,
                    companion=loaded.companion,
                    profile_dir=loaded.profile_dir,
                    manifest_path=loaded.manifest_path,
                    clone_text=None if clear_charter else _normalized_profile_text(charter_text),
                    user_profile_text=loaded.user_profile_text,
                    aegis_path=loaded.aegis_path,
                    user_profile_path=loaded.user_profile_path,
                    manifest=dict(loaded.manifest),
                ),
                sync_source="identity.charter.update",
            )
        return self.inspect_identity(profile_id=resolved_profile_id)

    def update_user_state(
        self,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
        text: str | None = None,
        fields: Mapping[str, object] | None = None,
        append: bool = False,
        clear: bool = False,
    ) -> UserCardRecord:
        resolved_profile_id = self._resolve_extension_profile_id(session_id=session_id, profile_id=profile_id)
        loaded = self._load_profile(resolved_profile_id)
        current_user = self.inspect_user(profile_id=resolved_profile_id)
        self._authorize_write(
            operation="cli.user.update",
            session_id=session_id or (self.latest_session().session_id if self.latest_session() is not None else None),
            description="update user state",
            metadata={"profile_id": resolved_profile_id},
        )
        next_user = apply_user_card_update(
            current_user,
            text=_normalized_profile_text(text),
            field_values=user_profile_updates(fields) if fields else None,
            append=append,
            clear=clear,
        )
        self._persist_profile(
            LoadedProfile(
                state=loaded.state,
                companion=loaded.companion,
                profile_dir=loaded.profile_dir,
                manifest_path=loaded.manifest_path,
                clone_text=loaded.clone_text,
                user_profile_text=render_user_card_profile_text(next_user),
                aegis_path=loaded.aegis_path,
                user_profile_path=loaded.user_profile_path,
                manifest=dict(loaded.manifest),
            ),
            sync_source="user.update",
        )
        return self.inspect_user(profile_id=resolved_profile_id)

    def update_relationship_state(
        self,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
        text: str | None = None,
        append: bool = False,
        clear: bool = False,
    ) -> RelationshipMemoryRecord:
        resolved_profile_id = self._resolve_extension_profile_id(session_id=session_id, profile_id=profile_id)
        loaded = self._load_profile(resolved_profile_id)
        self._authorize_write(
            operation="cli.relationship.update",
            session_id=session_id or (self.latest_session().session_id if self.latest_session() is not None else None),
            description="update relationship continuity",
            metadata={"profile_id": resolved_profile_id},
        )
        current = loaded.companion or CompanionSettings()
        current_notes = tuple(note.strip() for note in current.notes if note.strip())
        normalized = tuple(line.strip() for line in (text or "").splitlines() if line.strip())
        if clear:
            next_notes: tuple[str, ...] = ()
        elif append:
            next_notes = current_notes + tuple(note for note in normalized if note not in current_notes)
        elif normalized:
            next_notes = normalized
        else:
            next_notes = current_notes
        updated_companion = CompanionSettings(
            text_first=current.text_first,
            personality_preset=current.personality_preset,
            personality=current.personality,
            initiative=current.initiative,
            preserve_relationship_timeline=current.preserve_relationship_timeline,
            preserve_preferences=current.preserve_preferences,
            preserve_corrections=current.preserve_corrections,
            preserve_emotional_context=current.preserve_emotional_context,
            allow_voice_extension=current.allow_voice_extension,
            notes=next_notes,
        )
        self._persist_profile(
            LoadedProfile(
                state=loaded.state,
                companion=updated_companion,
                profile_dir=loaded.profile_dir,
                manifest_path=loaded.manifest_path,
                clone_text=loaded.clone_text,
                user_profile_text=loaded.user_profile_text,
                aegis_path=loaded.aegis_path,
                user_profile_path=loaded.user_profile_path,
                manifest=dict(loaded.manifest),
            ),
            sync_source="relationship.update",
        )
        return self.inspect_relationship(profile_id=resolved_profile_id)
