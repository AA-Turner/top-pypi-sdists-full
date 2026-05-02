"""Support contracts and row helpers for the runtime storage repository."""


from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from typing import Iterator, Mapping

from packages.auth.runtime import AuthProfile, EncryptedSecretValue, ProviderAuthState, SecretReference
from packages.contracts.runtime import (
    AgentRunState,
    AgentRunStep,
    ArtifactRecord,
    CloneIdentityRecord,
    EvidenceGraph,
    ExperienceRecord,
    GoalNode,
    MemoryRecord,
    ProcedureLibrary,
    ProcedureRecord,
    ProcedureStep,
    ProfileGraph,
    ProfileGrowthState,
    ProfileState,
    RelationshipMemoryRecord,
    SessionState,
    UserCardRecord,
    VerificationBundle,
    ActivityGraph,
)
from packages.planning import GoalGraph, goal_graph_to_activity_graph

MIGRATION_VERSION = 20
MIGRATIONS = {
    1: Path(__file__).with_name("migrations") / "0001_initial.sql",
    2: Path(__file__).with_name("migrations") / "0002_auth_profiles.sql",
    3: Path(__file__).with_name("migrations") / "0003_goal_graph.sql",
    4: Path(__file__).with_name("migrations") / "0004_memory_substrate.sql",
    5: Path(__file__).with_name("migrations") / "0005_agent_runs.sql",
    6: Path(__file__).with_name("migrations") / "0006_experiences.sql",
    7: Path(__file__).with_name("migrations") / "0007_profile_growth.sql",
    8: Path(__file__).with_name("migrations") / "0008_profiles_clone_path.sql",
    9: Path(__file__).with_name("migrations") / "0009_auth_secret_values.sql",
    10: Path(__file__).with_name("migrations") / "0010_provider_auth_states.sql",
    11: Path(__file__).with_name("migrations") / "0011_canonical_personal_ai_state.sql",
    12: Path(__file__).with_name("migrations") / "0012_evidence_and_procedure_graphs.sql",
    13: Path(__file__).with_name("migrations") / "0013_learning_verification_bundles.sql",
    14: Path(__file__).with_name("migrations") / "0014_structured_turn_memory_metadata.sql",
    15: Path(__file__).with_name("migrations") / "0015_activity_graph_cutover.sql",
    16: Path(__file__).with_name("migrations") / "0016_user_profile_source_column_rename.sql",
    17: Path(__file__).with_name("migrations") / "0017_user_card_durable_notes.sql",
    18: Path(__file__).with_name("migrations") / "0018_token_usage_events.sql",
    19: Path(__file__).with_name("migrations") / "0019_activity_node_projection_identity.sql",
    20: Path(__file__).with_name("migrations") / "0020_agent_run_wall_time_budget.sql",
}

@dataclass(frozen=True, slots=True)
class StorageBootstrapState:
    database_path: str
    schema_version: int

@dataclass(frozen=True, slots=True)
class StoredMemoryLedgerEntry:
    entry_id: str
    session_id: str
    event_id: str
    event_type: str
    content: str
    kind: str
    source_event_id: str | None = None
    goal_refs: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    created_at: datetime | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)

@dataclass(frozen=True, slots=True)
class StoredMemoryRecord:
    memory_id: str
    session_id: str
    kind: str
    content: str
    source_event_id: str | None = None
    goal_refs: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    created_at: datetime | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)

@dataclass(frozen=True, slots=True)
class StoredIdentityLedgerEntry:
    entry_id: str
    clone_id: str
    profile_id: str
    action: str
    summary: str
    metadata: Mapping[str, str] = field(default_factory=dict)
    created_at: datetime | None = None

@dataclass(frozen=True, slots=True)
class StoredUserCardLedgerEntry:
    entry_id: str
    user_card_id: str
    profile_id: str
    action: str
    summary: str
    metadata: Mapping[str, str] = field(default_factory=dict)
    created_at: datetime | None = None

@dataclass(frozen=True, slots=True)
class StoredRelationshipLedgerEntry:
    entry_id: str
    relationship_id: str
    profile_id: str
    action: str
    summary: str
    metadata: Mapping[str, str] = field(default_factory=dict)
    created_at: datetime | None = None

@dataclass(frozen=True, slots=True)
class CanonicalRowFamily:
    owner: str
    graph_contract: str
    record_contracts: tuple[str, ...]
    state_tables: tuple[str, ...]
    ledger_tables: tuple[str, ...] = ()
    index_names: tuple[str, ...] = ()
    status: str = "active"
    notes: str = ""

@dataclass(frozen=True, slots=True)
class LegacyOwnerCutover:
    legacy_surface: str
    canonical_owner: str
    disposition: str
    notes: str

@dataclass(frozen=True, slots=True)
class StorageCutoverManifest:
    schema_version: int
    migration_version: int
    migration_file: str
    index_version_policy: str
    row_families: tuple[CanonicalRowFamily, ...]
    legacy_mappings: tuple[LegacyOwnerCutover, ...]

def _utc_now() -> datetime:
    return datetime.now(timezone.utc)

def _iso(value: datetime | None) -> str:
    return (value or _utc_now()).isoformat()

def _parse_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed

def _json_text(values: tuple[str, ...]) -> str:
    return json.dumps(list(values), separators=(",", ":"))

def _tuple_text(payload: str) -> tuple[str, ...]:
    data = json.loads(payload)
    return tuple(str(item) for item in data)

def _json_mapping(values: dict[str, str]) -> str:
    return json.dumps(values, separators=(",", ":"), sort_keys=True)

def _mapping_text(payload: str) -> dict[str, str]:
    data = json.loads(payload)
    if not isinstance(data, dict):
        raise ValueError("expected a JSON object")
    return {str(key): str(value) for key, value in data.items()}

def _json_dict_text(values: dict[str, object]) -> str:
    return json.dumps(values, separators=(",", ":"), sort_keys=True, default=str)

def _mapping_object(payload: str) -> dict[str, object]:
    data = json.loads(payload)
    if not isinstance(data, dict):
        raise ValueError("expected a JSON object")
    return {str(key): value for key, value in data.items()}

def _record_from_row(row: sqlite3.Row) -> StoredMemoryRecord:
    return StoredMemoryRecord(
        memory_id=str(row["memory_id"]),
        session_id=str(row["session_id"]),
        kind=str(row["kind"]),
        content=str(row["content"]),
        source_event_id=str(row["source_event_id"]) if row["source_event_id"] is not None else None,
        goal_refs=_tuple_text(str(row["goal_refs_json"])),
        tags=_tuple_text(str(row["tags_json"])),
        created_at=_parse_datetime(str(row["created_at"])) if row["created_at"] is not None else None,
        metadata=_mapping_object(str(row["metadata_json"])) if row["metadata_json"] is not None else {},
    )

def _ledger_entry_from_row(row: sqlite3.Row) -> StoredMemoryLedgerEntry:
    return StoredMemoryLedgerEntry(
        entry_id=str(row["entry_id"]),
        session_id=str(row["session_id"]),
        event_id=str(row["event_id"]),
        event_type=str(row["event_type"]),
        content=str(row["content"]),
        kind=str(row["kind"]),
        source_event_id=str(row["source_event_id"]) if row["source_event_id"] is not None else None,
        goal_refs=_tuple_text(str(row["goal_refs_json"])),
        tags=_tuple_text(str(row["tags_json"])),
        created_at=_parse_datetime(str(row["created_at"])) if row["created_at"] is not None else _utc_now(),
        metadata=_mapping_text(str(row["metadata_json"])),
    )

def _agent_run_from_row(row: sqlite3.Row) -> AgentRunState:
    return AgentRunState(
        run_id=str(row["run_id"]),
        session_id=str(row["session_id"]),
        source_event_id=str(row["source_event_id"]),
        prompt=str(row["prompt"]),
        status=str(row["status"]),
        phase=str(row["phase"]),
        step_count=int(row["step_count"]),
        model_turn_count=int(row["model_turn_count"]),
        tool_call_count=int(row["tool_call_count"]),
        max_model_turns=int(row["max_model_turns"]),
        max_wall_time_seconds=int(row["max_wall_time_seconds"]),
        created_at=_parse_datetime(str(row["created_at"])),
        updated_at=_parse_datetime(str(row["updated_at"])),
        waiting_reason=str(row["waiting_reason"]) if row["waiting_reason"] is not None else None,
        continuation_prompt=(
            str(row["continuation_prompt"]) if row["continuation_prompt"] is not None else None
        ),
        last_summary=str(row["last_summary"]) if row["last_summary"] is not None else None,
    )

def _agent_run_step_from_row(row: sqlite3.Row) -> AgentRunStep:
    return AgentRunStep(
        step_id=str(row["step_id"]),
        run_id=str(row["run_id"]),
        session_id=str(row["session_id"]),
        step_index=int(row["step_index"]),
        kind=str(row["kind"]),
        title=str(row["title"]),
        content=str(row["content"]),
        created_at=_parse_datetime(str(row["created_at"])),
        outcome=str(row["outcome"]) if row["outcome"] is not None else None,
        tool_name=str(row["tool_name"]) if row["tool_name"] is not None else None,
    )

def _experience_from_row(row: sqlite3.Row) -> ExperienceRecord:
    return ExperienceRecord(
        experience_id=str(row["experience_id"]),
        session_id=str(row["session_id"]),
        profile_id=str(row["profile_id"]),
        workspace_id=str(row["workspace_id"]) if row["workspace_id"] is not None else None,
        kind=str(row["kind"]),
        title=str(row["title"]),
        summary=str(row["summary"]),
        status=str(row["status"]),
        run_id=str(row["run_id"]) if row["run_id"] is not None else None,
        source_event_id=str(row["source_event_id"]) if row["source_event_id"] is not None else None,
        goal_id=str(row["goal_id"]) if row["goal_id"] is not None else None,
        tool_call_count=int(row["tool_call_count"]),
        model_turn_count=int(row["model_turn_count"]),
        related_skill_ids=_tuple_text(str(row["related_skill_ids_json"])),
        produced_artifact_ids=_tuple_text(str(row["produced_artifact_ids_json"])),
        tags=_tuple_text(str(row["tags_json"])),
        created_at=_parse_datetime(str(row["created_at"])) if row["created_at"] is not None else None,
        updated_at=_parse_datetime(str(row["updated_at"])) if row["updated_at"] is not None else None,
    )

def _memory_contract_from_record(record: StoredMemoryRecord) -> MemoryRecord:
    return MemoryRecord(
        memory_id=record.memory_id,
        session_id=record.session_id,
        kind=record.kind,
        content=record.content,
        source_event_id=record.source_event_id,
        goal_refs=record.goal_refs,
        tags=record.tags,
        created_at=record.created_at,
        metadata=record.metadata,
    )

def _artifact_from_row(row: sqlite3.Row) -> ArtifactRecord:
    return ArtifactRecord(
        artifact_id=str(row["artifact_id"]),
        session_id=str(row["session_id"]),
        kind=str(row["kind"]),
        name=str(row["name"]),
        uri=str(row["uri"]),
        checksum=str(row["checksum"]) if row["checksum"] is not None else None,
        created_at=_parse_datetime(str(row["created_at"])) if row["created_at"] is not None else None,
    )

def _growth_from_row(row: sqlite3.Row) -> ProfileGrowthState:
    return ProfileGrowthState(
        profile_id=str(row["profile_id"]),
        growth_score=int(row["growth_score"]),
        total_dialogues=int(row["total_dialogues"]),
        total_tokens=int(row["total_tokens"]),
        total_experiences=int(row["total_experiences"]),
        promoted_experiences=int(row["promoted_experiences"]),
        active_days=int(row["active_days"]),
        streak_days=int(row["streak_days"]),
        first_dialogue_at=(
            _parse_datetime(str(row["first_dialogue_at"])) if row["first_dialogue_at"] is not None else None
        ),
        last_dialogue_at=(
            _parse_datetime(str(row["last_dialogue_at"])) if row["last_dialogue_at"] is not None else None
        ),
        last_active_day=str(row["last_active_day"]) if row["last_active_day"] is not None else None,
        created_at=_parse_datetime(str(row["created_at"])) if row["created_at"] is not None else None,
        updated_at=_parse_datetime(str(row["updated_at"])) if row["updated_at"] is not None else None,
    )

def _clone_identity_from_row(row: sqlite3.Row) -> CloneIdentityRecord:
    return CloneIdentityRecord(
        clone_id=str(row["clone_id"]),
        profile_id=str(row["profile_id"]),
        display_name=str(row["display_name"]),
        identity_mode=str(row["identity_mode"]),
        personality_preset=str(row["personality_preset"]),
        initiative=str(row["initiative"]),
        relational_stance=str(row["relational_stance"]),
        voice_contract=str(row["voice_contract"]),
        working_style_contract=str(row["working_style_contract"]),
        charter_extension=str(row["charter_extension"]) if row["charter_extension"] is not None else None,
        governance_flags=_tuple_text(str(row["governance_flags_json"])),
        source_manifest_path=(
            str(row["source_manifest_path"]) if row["source_manifest_path"] is not None else None
        ),
        source_clone_path=str(row["source_clone_path"]) if row["source_clone_path"] is not None else None,
        created_at=_parse_datetime(str(row["created_at"])) if row["created_at"] is not None else None,
        updated_at=_parse_datetime(str(row["updated_at"])) if row["updated_at"] is not None else None,
    )

def _user_card_from_row(row: sqlite3.Row) -> UserCardRecord:
    return UserCardRecord(
        user_card_id=str(row["user_card_id"]),
        profile_id=str(row["profile_id"]),
        preferred_name=str(row["preferred_name"]) if row["preferred_name"] is not None else None,
        locale=str(row["locale"]) if row["locale"] is not None else None,
        timezone=str(row["timezone"]) if row["timezone"] is not None else None,
        communication_preferences=_tuple_text(str(row["communication_preferences_json"])),
        boundaries=_tuple_text(str(row["boundaries_json"])),
        biography_fragments=_tuple_text(str(row["biography_fragments_json"])),
        durable_notes=_tuple_text(str(row["durable_notes_json"])),
        shared_preferences=_tuple_text(str(row["shared_preferences_json"])),
        source_user_profile_path=(
            str(row["source_user_profile_path"]) if row["source_user_profile_path"] is not None else None
        ),
        created_at=_parse_datetime(str(row["created_at"])) if row["created_at"] is not None else None,
        updated_at=_parse_datetime(str(row["updated_at"])) if row["updated_at"] is not None else None,
    )

def _relationship_memory_from_row(row: sqlite3.Row) -> RelationshipMemoryRecord:
    return RelationshipMemoryRecord(
        relationship_id=str(row["relationship_id"]),
        profile_id=str(row["profile_id"]),
        clone_id=str(row["clone_id"]),
        user_card_id=str(row["user_card_id"]) if row["user_card_id"] is not None else None,
        interaction_preferences=_tuple_text(str(row["interaction_preferences_json"])),
        repair_history=_tuple_text(str(row["repair_history_json"])),
        trust_markers=_tuple_text(str(row["trust_markers_json"])),
        expectations=_tuple_text(str(row["expectations_json"])),
        local_corrections=_tuple_text(str(row["local_corrections_json"])),
        continuity_notes=_tuple_text(str(row["continuity_notes_json"])),
        created_at=_parse_datetime(str(row["created_at"])) if row["created_at"] is not None else None,
        updated_at=_parse_datetime(str(row["updated_at"])) if row["updated_at"] is not None else None,
    )

def _identity_ledger_from_row(row: sqlite3.Row) -> StoredIdentityLedgerEntry:
    return StoredIdentityLedgerEntry(
        entry_id=str(row["entry_id"]),
        clone_id=str(row["clone_id"]),
        profile_id=str(row["profile_id"]),
        action=str(row["action"]),
        summary=str(row["summary"]),
        metadata=_mapping_text(str(row["metadata_json"])),
        created_at=_parse_datetime(str(row["created_at"])) if row["created_at"] is not None else None,
    )

def _user_card_ledger_from_row(row: sqlite3.Row) -> StoredUserCardLedgerEntry:
    return StoredUserCardLedgerEntry(
        entry_id=str(row["entry_id"]),
        user_card_id=str(row["user_card_id"]),
        profile_id=str(row["profile_id"]),
        action=str(row["action"]),
        summary=str(row["summary"]),
        metadata=_mapping_text(str(row["metadata_json"])),
        created_at=_parse_datetime(str(row["created_at"])) if row["created_at"] is not None else None,
    )

def _relationship_ledger_from_row(row: sqlite3.Row) -> StoredRelationshipLedgerEntry:
    return StoredRelationshipLedgerEntry(
        entry_id=str(row["entry_id"]),
        relationship_id=str(row["relationship_id"]),
        profile_id=str(row["profile_id"]),
        action=str(row["action"]),
        summary=str(row["summary"]),
        metadata=_mapping_text(str(row["metadata_json"])),
        created_at=_parse_datetime(str(row["created_at"])) if row["created_at"] is not None else None,
    )
