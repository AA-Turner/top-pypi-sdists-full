"""Session lineage and resume helpers."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from uuid import uuid4

from packages.contracts.runtime import ProfileState, SessionContinuityState, SessionState
from packages.storage.repository import RuntimeStorageRepository


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class SessionResumeResult:
    parent: SessionState
    session: SessionState
    lineage: tuple[SessionState, ...]


@dataclass(frozen=True, slots=True)
class RelationshipMemoryPolicy:
    profile_mode: str
    text_first: bool = True
    preserve_relationship_timeline: bool = True
    preserve_preferences: bool = True
    preserve_corrections: bool = True
    preserve_emotional_context: bool = True
    allow_voice_extension: bool = False
    allowed_memory_kinds: tuple[str, ...] = ("relationship", "preference", "continuity")

    def allows(self, memory_kind: str) -> bool:
        return memory_kind in self.allowed_memory_kinds

    def summary(self) -> str:
        posture = "text-first" if self.text_first else "multi-modal"
        return (
            f"{self.profile_mode} {posture} continuity: "
            f"timeline={self.preserve_relationship_timeline}, "
            f"preferences={self.preserve_preferences}, "
            f"corrections={self.preserve_corrections}, "
            f"emotional={self.preserve_emotional_context}, "
            f"voice_extension={self.allow_voice_extension}"
        )


@dataclass(frozen=True, slots=True)
class SessionLineageService:
    """Encapsulate session lifecycle behavior on top of durable storage."""

    repository: RuntimeStorageRepository

    def start_session(
        self,
        profile: ProfileState,
        *,
        workspace_id: str | None = None,
        session_id: str | None = None,
        started_at: datetime | None = None,
    ) -> SessionState:
        timestamp = started_at or _utc_now()
        state = SessionState(
            session_id=session_id or uuid4().hex,
            profile_id=profile.profile_id,
            workspace_id=workspace_id,
            status="active",
            started_at=timestamp,
            updated_at=timestamp,
        )
        self.repository.upsert_profile(profile, updated_at=timestamp)
        self.repository.upsert_session(state)
        return state

    def interrupt_session(
        self,
        session_id: str,
        *,
        interruption_state: str,
        interrupted_at: datetime | None = None,
    ) -> SessionState:
        timestamp = interrupted_at or _utc_now()
        return self.repository.refresh_session(
            session_id,
            status="interrupted",
            interruption_state=interruption_state,
            updated_at=timestamp,
        )

    def resume_session(
        self,
        session_id: str,
        *,
        resumed_at: datetime | None = None,
        child_session_id: str | None = None,
    ) -> SessionResumeResult:
        timestamp = resumed_at or _utc_now()
        parent = self.repository.load_session(session_id)
        if parent is None:
            raise KeyError(session_id)
        resumed_session = SessionState(
            session_id=child_session_id or uuid4().hex,
            profile_id=parent.profile_id,
            workspace_id=parent.workspace_id,
            status="active",
            started_at=timestamp,
            updated_at=timestamp,
            parent_session_id=parent.session_id,
        )
        self.repository.upsert_session(resumed_session)
        self.repository.record_resume(parent.session_id, resumed_session.session_id, timestamp)
        updated_parent = self.repository.load_session(parent.session_id) or parent
        lineage = self.repository.lineage(resumed_session.session_id)
        return SessionResumeResult(parent=updated_parent, session=resumed_session, lineage=lineage)

    def lineage(self, session_id: str) -> tuple[SessionState, ...]:
        return self.repository.lineage(session_id)

    def continuity_state(
        self,
        session: SessionState,
        *,
        lineage: tuple[SessionState, ...] = (),
        active_goal_id: str | None = None,
    ) -> SessionContinuityState:
        chain = lineage or (session,)
        lineage_session_ids = tuple(node.session_id for node in chain)
        origin_session_id = lineage_session_ids[0] if lineage_session_ids else (session.parent_session_id or session.session_id)
        inherited_interruption_state = session.interruption_state
        if inherited_interruption_state is None:
            for ancestor in reversed(chain[:-1]):
                if ancestor.interruption_state is not None:
                    inherited_interruption_state = ancestor.interruption_state
                    break

        if session.parent_session_id and inherited_interruption_state is not None:
            mode = "background"
        elif session.parent_session_id:
            mode = "resumed"
        elif inherited_interruption_state is not None:
            mode = "interrupted"
        else:
            mode = "foreground"

        summary = self._continuity_summary(
            mode=mode,
            session=session,
            origin_session_id=origin_session_id,
            inherited_interruption_state=inherited_interruption_state,
            active_goal_id=active_goal_id,
        )
        return SessionContinuityState(
            session_id=session.session_id,
            mode=mode,
            origin_session_id=origin_session_id,
            lineage_session_ids=lineage_session_ids,
            inherited_interruption_state=inherited_interruption_state,
            active_goal_id=active_goal_id,
            summary=summary,
        )

    def apply_continuity_state(
        self,
        session: SessionState,
        continuity: SessionContinuityState,
    ) -> SessionState:
        if session.interruption_state is not None:
            return session
        if not continuity.requires_recovery:
            return session
        return replace(session, interruption_state=continuity.summary)

    def relationship_memory_policy(
        self,
        profile_mode: str,
        *,
        text_first: bool = True,
        preserve_relationship_timeline: bool = True,
        preserve_preferences: bool = True,
        preserve_corrections: bool = True,
        preserve_emotional_context: bool = True,
        allow_voice_extension: bool = False,
        allowed_memory_kinds: tuple[str, ...] = ("relationship", "preference", "continuity"),
    ) -> RelationshipMemoryPolicy:
        return RelationshipMemoryPolicy(
            profile_mode=profile_mode,
            text_first=text_first,
            preserve_relationship_timeline=preserve_relationship_timeline,
            preserve_preferences=preserve_preferences,
            preserve_corrections=preserve_corrections,
            preserve_emotional_context=preserve_emotional_context,
            allow_voice_extension=allow_voice_extension,
            allowed_memory_kinds=allowed_memory_kinds,
        )

    def _continuity_summary(
        self,
        *,
        mode: str,
        session: SessionState,
        origin_session_id: str,
        inherited_interruption_state: str | None,
        active_goal_id: str | None,
    ) -> str:
        if mode == "foreground":
            summary = "continue the active session directly from durable state"
        elif mode == "resumed":
            summary = f"resume durable work from session {origin_session_id}"
        elif mode == "interrupted":
            summary = f"recover after interruption: {inherited_interruption_state}"
        else:
            summary = (
                f"resume durable work from session {origin_session_id} "
                f"after interruption: {inherited_interruption_state}"
            )
        if active_goal_id is not None:
            summary += f"; keep goal {active_goal_id} in focus"
        if session.parent_session_id and session.parent_session_id != origin_session_id:
            summary += f"; immediate parent={session.parent_session_id}"
        return summary
