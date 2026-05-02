"""Canonical personal-state and continuity services for the API surface."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Mapping, cast

from packages.continuity import ContinuityProjection, ContinuityProjectionService
from packages.contracts import CloneIdentityRecord, ProfileState, RelationshipMemoryRecord, SessionState, UserCardRecord
from packages.kernel import merge_preference_updates
from packages.evidence import MemoryRuntime
from packages.state import build_loaded_profile_from_state, load_persisted_canonical_state, render_user_card_profile_text, sync_canonical_profile_state
from packages.planning import PlanningService
from packages.state import CompanionSettings, apply_user_card_update, build_canonical_profile_state, user_profile_updates, is_companion_mode, resolve_personality_preset
from packages.session import SessionLineageService
from packages.storage import RuntimeStorageRepository


@dataclass(frozen=True, slots=True)
class APIContinuityInspection:
    profile: ProfileState
    session: SessionState
    identity: CloneIdentityRecord
    user: UserCardRecord
    relationship: RelationshipMemoryRecord
    continuity: ContinuityProjection
    active_goal_id: str | None
    wake_action: str
    wake_summary: str
    wake_factors: tuple[str, ...]

    def to_record(self) -> dict[str, Any]:
        return {
            "profile": self.profile,
            "session": self.session,
            "identity": self.identity,
            "user": self.user,
            "relationship": self.relationship,
            "continuity": self.continuity,
            "active_goal_id": self.active_goal_id,
            "wake_action": self.wake_action,
            "wake_summary": self.wake_summary,
            "wake_factors": self.wake_factors,
        }


@dataclass(frozen=True, slots=True)
class _CanonicalStateRecords:
    identity: CloneIdentityRecord
    user: UserCardRecord
    relationship: RelationshipMemoryRecord


@dataclass(frozen=True, slots=True)
class APIStateService:
    repository: RuntimeStorageRepository
    session_lineage: SessionLineageService
    memory_runtime: MemoryRuntime
    planning_service: PlanningService

    def ensure_profile_state(self, profile: ProfileState, *, sync_source: str = "api.bootstrap") -> _CanonicalStateRecords:
        persisted = load_persisted_canonical_state(self.repository, profile.profile_id)
        if (
            persisted.clone_identity is not None
            and persisted.user_card is not None
            and persisted.relationship_memory is not None
        ):
            return _CanonicalStateRecords(
                identity=cast(CloneIdentityRecord, persisted.clone_identity),
                user=cast(UserCardRecord, persisted.user_card),
                relationship=cast(RelationshipMemoryRecord, persisted.relationship_memory),
            )
        bundle = build_canonical_profile_state(build_loaded_profile_from_state(profile))
        synced = sync_canonical_profile_state(
            self.repository,
            bundle,
            previous=persisted,
            sync_source=sync_source,
        )
        return _CanonicalStateRecords(
            identity=cast(CloneIdentityRecord, synced.clone_identity),
            user=cast(UserCardRecord, synced.user_card),
            relationship=cast(RelationshipMemoryRecord, synced.relationship_memory),
        )

    def inspect_identity(self, *, session_id: str | None = None, profile_id: str | None = None) -> CloneIdentityRecord:
        profile = self._resolve_profile(session_id=session_id, profile_id=profile_id)
        return self.ensure_profile_state(profile).identity

    def inspect_user(self, *, session_id: str | None = None, profile_id: str | None = None) -> UserCardRecord:
        profile = self._resolve_profile(session_id=session_id, profile_id=profile_id)
        return self.ensure_profile_state(profile).user

    def inspect_relationship(
        self,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
    ) -> RelationshipMemoryRecord:
        profile = self._resolve_profile(session_id=session_id, profile_id=profile_id)
        return self.ensure_profile_state(profile).relationship

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
        profile = self._resolve_profile(session_id=session_id, profile_id=profile_id)
        current = self.ensure_profile_state(profile)
        next_mode = profile.mode
        if (personality_preset is not None or initiative is not None) and not is_companion_mode(next_mode):
            next_mode = "companion"
        updated_profile = replace(
            profile,
            display_name=display_name if display_name is not None else profile.display_name,
            mode=next_mode,
        )
        if updated_profile != profile:
            self.repository.upsert_profile(updated_profile)
        identity_record = replace(
            current.identity,
            display_name=updated_profile.display_name,
            identity_mode=updated_profile.mode,
        )
        loaded = build_loaded_profile_from_state(
            updated_profile,
            identity_record=identity_record,
            user_card=current.user,
            relationship_record=current.relationship,
        )
        companion = loaded.companion or CompanionSettings()
        if personality_preset is not None or initiative is not None:
            resolved_preset = (
                companion.personality_preset
                if personality_preset is None
                else resolve_personality_preset(personality_preset, mode=updated_profile.mode).preset_id
            )
            loaded = replace(
                loaded,
                companion=replace(
                    companion,
                    personality_preset=resolved_preset,
                    personality=resolve_personality_preset(resolved_preset, mode=updated_profile.mode).traits,
                    initiative=initiative if initiative is not None else companion.initiative,
                ),
            )
        if clear_charter or charter_text is not None:
            loaded = replace(
                loaded,
                clone_text=None if clear_charter else _normalized_text(charter_text),
            )
        bundle = build_canonical_profile_state(loaded)
        synced = sync_canonical_profile_state(
            self.repository,
            bundle,
            previous=load_persisted_canonical_state(self.repository, updated_profile.profile_id),
            sync_source="api.identity.update",
        )
        return cast(CloneIdentityRecord, synced.clone_identity)

    def update_user_state(
        self,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
        text: str | None = None,
        fields: dict[str, object] | None = None,
        append: bool = False,
        clear: bool = False,
    ) -> UserCardRecord:
        profile = self._resolve_profile(session_id=session_id, profile_id=profile_id)
        current = self.ensure_profile_state(profile)
        loaded = build_loaded_profile_from_state(
            profile,
            identity_record=current.identity,
            user_card=current.user,
            relationship_record=current.relationship,
        )
        next_user = apply_user_card_update(
            current.user,
            text=_normalized_text(text),
            field_values=user_profile_updates(fields) if fields else None,
            append=append,
            clear=clear,
        )
        bundle = build_canonical_profile_state(
            replace(loaded, user_profile_text=render_user_card_profile_text(next_user))
        )
        synced = sync_canonical_profile_state(
            self.repository,
            bundle,
            previous=load_persisted_canonical_state(self.repository, profile.profile_id),
            sync_source="api.user.update",
        )
        return cast(UserCardRecord, synced.user_card)

    def update_relationship_state(
        self,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
        text: str | None = None,
        append: bool = False,
        clear: bool = False,
    ) -> RelationshipMemoryRecord:
        profile = self._resolve_profile(session_id=session_id, profile_id=profile_id)
        current = self.ensure_profile_state(profile)
        loaded = build_loaded_profile_from_state(
            profile,
            identity_record=current.identity,
            user_card=current.user,
            relationship_record=current.relationship,
        )
        companion = loaded.companion or CompanionSettings()
        current_notes = tuple(note.strip() for note in companion.notes if note.strip())
        normalized = tuple(line.strip() for line in (text or "").splitlines() if line.strip())
        if clear:
            next_notes: tuple[str, ...] = ()
        elif append:
            next_notes = current_notes + tuple(note for note in normalized if note not in current_notes)
        elif normalized:
            next_notes = normalized
        else:
            next_notes = current_notes
        bundle = build_canonical_profile_state(
            replace(loaded, companion=replace(companion, notes=next_notes))
        )
        synced = sync_canonical_profile_state(
            self.repository,
            bundle,
            previous=load_persisted_canonical_state(self.repository, profile.profile_id),
            sync_source="api.relationship.update",
        )
        return cast(RelationshipMemoryRecord, synced.relationship_memory)

    def apply_turn_profile_delta(
        self,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
        user_fields: Mapping[str, str] | None = None,
        preference_updates: tuple[str, ...] = (),
        relationship_notes: tuple[str, ...] = (),
        sync_source: str = "api.turn.reconciliation",
    ) -> None:
        if not user_fields and not preference_updates and not relationship_notes:
            return
        profile = self._resolve_profile(session_id=session_id, profile_id=profile_id)
        current = self.ensure_profile_state(profile)
        loaded = build_loaded_profile_from_state(
            profile,
            identity_record=current.identity,
            user_card=current.user,
            relationship_record=current.relationship,
        )
        next_loaded = loaded
        if user_fields:
            next_user = apply_user_card_update(
                current.user,
                field_values=dict(user_fields),
                append=True,
            )
            next_loaded = replace(
                next_loaded,
                user_profile_text=render_user_card_profile_text(next_user),
            )
        if preference_updates:
            next_loaded = replace(
                next_loaded,
                state=replace(
                    next_loaded.state,
                    preferences=merge_preference_updates(
                        next_loaded.state.preferences,
                        preference_updates,
                    ),
                ),
            )
        if relationship_notes:
            companion = next_loaded.companion or CompanionSettings()
            current_notes = tuple(note.strip() for note in companion.notes if note.strip())
            next_notes = current_notes + tuple(note for note in relationship_notes if note not in current_notes)
            next_loaded = replace(
                next_loaded,
                companion=replace(companion, notes=next_notes),
            )
        if next_loaded == loaded:
            return
        self.repository.upsert_profile(next_loaded.state)
        bundle = build_canonical_profile_state(next_loaded)
        sync_canonical_profile_state(
            self.repository,
            bundle,
            previous=load_persisted_canonical_state(self.repository, profile.profile_id),
            sync_source=sync_source,
        )

    def inspect_continuity(self, session_id: str) -> APIContinuityInspection:
        session = self._session(session_id)
        profile = self._profile(session.profile_id)
        records = self.ensure_profile_state(profile)
        loaded = build_loaded_profile_from_state(
            profile,
            identity_record=records.identity,
            user_card=records.user,
            relationship_record=records.relationship,
        )
        lineage = self.session_lineage.lineage(session_id)
        goal_graph = self.repository.load_activity_graph(session_id)
        active_goal_id = goal_graph.active_goal_id if goal_graph is not None else None
        continuity = ContinuityProjectionService(self.session_lineage).inspect(
            loaded,
            session,
            lineage=lineage,
            active_goal_id=active_goal_id,
            identity_record=records.identity,
            relationship_record=records.relationship,
        )
        memories = tuple(self.memory_runtime.store.list(session_id=session_id))
        if goal_graph is None:
            wake_action = "idle"
            wake_summary = "No durable wake action is available yet; start or resume a goal-bearing session first."
            wake_factors = ("no-goal-graph",)
        else:
            decision, _ = self.planning_service.wake_next_step(
                session=session,
                graph=goal_graph,
                memories=memories,
                initiative_hint=records.identity.initiative,
                continuity_notes=records.relationship.continuity_notes,
            )
            wake_action = decision.selected_move.kind
            wake_summary = decision.rationale.summary
            wake_factors = tuple(decision.rationale.factors)
        return APIContinuityInspection(
            profile=profile,
            session=session,
            identity=records.identity,
            user=records.user,
            relationship=records.relationship,
            continuity=continuity,
            active_goal_id=active_goal_id,
            wake_action=wake_action,
            wake_summary=wake_summary,
            wake_factors=wake_factors,
        )

    def _resolve_profile(self, *, session_id: str | None, profile_id: str | None) -> ProfileState:
        if profile_id is not None:
            return self._profile(profile_id)
        if session_id is None:
            raise ValueError("session_id or profile_id is required")
        session = self._session(session_id)
        return self._profile(session.profile_id)

    def _profile(self, profile_id: str) -> ProfileState:
        profile = self.repository.load_profile(profile_id)
        if profile is None:
            raise KeyError(profile_id)
        return profile

    def _session(self, session_id: str) -> SessionState:
        session = self.repository.load_session(session_id)
        if session is None:
            raise KeyError(session_id)
        return session


def _normalized_text(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


__all__ = ["APIContinuityInspection", "APIStateService"]
