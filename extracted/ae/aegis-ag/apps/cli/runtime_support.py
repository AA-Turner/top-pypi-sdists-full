"""Shared helpers and lightweight data models for the CLI runtime."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any
from urllib.parse import quote

from packages.contracts.runtime import (
    EvidenceRetrievalResult,
    MemoryRecord,
    PlanDraft,
    ProfileState,
    ResumePacket,
    SessionState,
    ActivityGraph,
)
from packages.kernel import KernelOutcome, WakeReconciliationReport
from packages.planning.runtime import PlanningDecision
from packages.session import RelationshipMemoryPolicy
from packages.state import CompanionSettings, LoadedProfile, render_clone_charter
from packages.voice import VoiceInputResolution, VoiceTurnResult

_PLACEHOLDER_MODELS_BY_PROVIDER = {
    "openai-compatible": {"model-id", "Any OpenAI-compatible chat model"},
}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(value: datetime) -> str:
    return value.isoformat()


def _restore_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def _tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[A-Za-z0-9_]+", text.lower()) if token}


def _path_is_within(path: Path, root: Path) -> bool:
    try:
        path.expanduser().resolve().relative_to(root.expanduser().resolve())
    except ValueError:
        return False
    return True


def _coerce_str_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        if not value.strip():
            return ()
        return tuple(part.strip() for part in value.split(",") if part.strip())
    if isinstance(value, (list, tuple)):
        return tuple(str(item) for item in value if str(item))
    return (str(value),)


def _optional_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return datetime.fromisoformat(text)


def _normalized_profile_text(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


def _current_clone_text(profile: LoadedProfile) -> str | None:
    return _normalized_profile_text(profile.clone_text)


def _default_clone_text(
    profile: LoadedProfile,
    *,
    display_name: str | None = None,
    mode: str | None = None,
    companion: CompanionSettings | None = None,
) -> str:
    effective_companion = companion or profile.companion or CompanionSettings()
    return render_clone_charter(
        display_name=display_name or profile.state.display_name,
        personality_preset=effective_companion.personality_preset,
        initiative=effective_companion.initiative,
        mode=mode or profile.state.mode,
    ).strip()


def _clone_text_uses_default(profile: LoadedProfile) -> bool:
    current = _current_clone_text(profile)
    if current is None:
        return True
    return current == _default_clone_text(profile)


def _seed_clone_text(
    profile: LoadedProfile,
    *,
    display_name: str | None = None,
    mode: str | None = None,
    companion: CompanionSettings | None = None,
) -> str:
    current = _current_clone_text(profile)
    if current is None or _clone_text_uses_default(profile):
        return _default_clone_text(
            profile,
            display_name=display_name,
            mode=mode,
            companion=companion,
        )
    return current


@dataclass(frozen=True, slots=True)
class CliPaths:
    home_dir: Path
    state_dir: Path
    profile_dir: Path
    skills_dir: Path
    builtin_skills_dir: Path
    installed_skills_dir: Path
    authored_skills_dir: Path
    skill_search_cache_dir: Path
    cron_dir: Path
    workspace_dir: Path
    pairing_dir: Path

    @property
    def database_path(self) -> Path:
        return self.state_dir / "aegis.sqlite3"

    @property
    def snapshot_path(self) -> Path:
        return self.state_dir / "preview-snapshot.json"

    @property
    def cron_jobs_path(self) -> Path:
        return self.cron_dir / "jobs.json"

    @property
    def cron_output_dir(self) -> Path:
        return self.cron_dir / "output"

    @property
    def cron_lock_path(self) -> Path:
        return self.cron_dir / "cron.lock"

    @property
    def secret_key_path(self) -> Path:
        return self.state_dir / "provider-secrets.key"

    def workspace_path_for_clone(self, clone_id: str) -> Path:
        key = quote(clone_id.strip(), safe="")
        if not key:
            raise ValueError("clone id is required")
        return self.workspace_dir / key


@dataclass(frozen=True, slots=True)
class WakeProgressionResult:
    profile: ProfileState
    session: SessionState
    decision: PlanningDecision
    planned_goal_graph: ActivityGraph
    applied: bool
    plan: PlanDraft | None
    reconciliation: WakeReconciliationReport
    retrieval: EvidenceRetrievalResult | None = None
    resume_packet: ResumePacket | None = None


@dataclass(frozen=True, slots=True)
class CliVoiceTurnResult:
    input_resolution: VoiceInputResolution
    kernel_outcome: KernelOutcome | None
    voice_turn: VoiceTurnResult


@dataclass(frozen=True, slots=True)
class ContinuityStatus:
    profile: LoadedProfile
    session: SessionState
    relationship_policy: RelationshipMemoryPolicy
    governance_summary: str
    proactive_summary: str
    initiative: str
    wake_action: str
    wake_summary: str
    wake_factors: tuple[str, ...]
    reengagement_style: str
    reengagement_prompt: str
    continuity_summary: str
    voice_status: str
    voice_identity_binding: str
    voice_identity_summary: str


@dataclass(frozen=True, slots=True)
class CloneSummary:
    clone_id: str
    latest_session_id: str
    latest_status: str
    updated_at: datetime
    session_count: int


@dataclass(frozen=True, slots=True)
class _PlanningMemoryRecovery:
    memories: tuple[MemoryRecord, ...]
    query: str
    goal_ids: tuple[str, ...]
    scope_session_ids: tuple[str, ...]
    scope_reason: str
    retrieval: EvidenceRetrievalResult | None = None
    resume_packet: ResumePacket | None = None
