"""Method group extracted from packages/storage/repository.py."""


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

MIGRATION_VERSION = 16
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
}



from .repository_support import (
    CanonicalRowFamily,
    LegacyOwnerCutover,
    MIGRATIONS,
    MIGRATION_VERSION,
    StorageBootstrapState,
    StorageCutoverManifest,
    StoredIdentityLedgerEntry,
    StoredMemoryLedgerEntry,
    StoredMemoryRecord,
    StoredRelationshipLedgerEntry,
    StoredUserCardLedgerEntry,
    _agent_run_from_row,
    _agent_run_step_from_row,
    _artifact_from_row,
    _clone_identity_from_row,
    _experience_from_row,
    _growth_from_row,
    _identity_ledger_from_row,
    _iso,
    _json_dict_text,
    _json_mapping,
    _json_text,
    _ledger_entry_from_row,
    _mapping_object,
    _mapping_text,
    _memory_contract_from_record,
    _parse_datetime,
    _record_from_row,
    _relationship_ledger_from_row,
    _relationship_memory_from_row,
    _tuple_text,
    _user_card_from_row,
    _user_card_ledger_from_row,
    _utc_now,
)

def upsert_profile(self, profile: ProfileState, *, updated_at: datetime | None = None) -> None:
    timestamp = _iso(updated_at)
    created_at = timestamp
    with self.connection() as connection:
        existing = connection.execute(
            "SELECT created_at FROM profiles WHERE profile_id = ?",
            (profile.profile_id,),
        ).fetchone()
        if existing is not None:
            created_at = str(existing["created_at"])
        connection.execute(
            """
            INSERT INTO profiles (
                profile_id,
                display_name,
                mode,
                clone_path,
                preferences_json,
                enabled_capabilities_json,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(profile_id) DO UPDATE SET
                display_name = excluded.display_name,
                mode = excluded.mode,
                clone_path = excluded.clone_path,
                preferences_json = excluded.preferences_json,
                enabled_capabilities_json = excluded.enabled_capabilities_json,
                updated_at = excluded.updated_at
            """,
            (
                profile.profile_id,
                profile.display_name,
                profile.mode,
                profile.clone_path,
                _json_text(profile.preferences),
                _json_text(profile.enabled_capabilities),
                created_at,
                timestamp,
            ),
        )
        connection.commit()

def load_profile(self, profile_id: str) -> ProfileState | None:
    with self.connection() as connection:
        row = connection.execute(
            """
            SELECT profile_id, display_name, mode, clone_path,
                   preferences_json, enabled_capabilities_json
            FROM profiles
            WHERE profile_id = ?
            """,
            (profile_id,),
        ).fetchone()
    if row is None:
        return None
    return ProfileState(
        profile_id=str(row["profile_id"]),
        display_name=str(row["display_name"]),
        mode=str(row["mode"]),
        clone_path=str(row["clone_path"]) if row["clone_path"] is not None else None,
        preferences=_tuple_text(str(row["preferences_json"])),
        enabled_capabilities=_tuple_text(str(row["enabled_capabilities_json"])),
    )

def upsert_clone_identity(
    self,
    record: CloneIdentityRecord,
    *,
    updated_at: datetime | None = None,
) -> None:
    timestamp = _iso(updated_at or record.updated_at or record.created_at)
    created_at = timestamp
    with self.connection() as connection:
        existing = connection.execute(
            "SELECT created_at FROM clone_identities WHERE clone_id = ?",
            (record.clone_id,),
        ).fetchone()
        if existing is not None:
            created_at = str(existing["created_at"])
        connection.execute(
            """
            INSERT INTO clone_identities (
                clone_id,
                profile_id,
                display_name,
                identity_mode,
                personality_preset,
                initiative,
                relational_stance,
                voice_contract,
                working_style_contract,
                charter_extension,
                governance_flags_json,
                source_manifest_path,
                source_clone_path,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(clone_id) DO UPDATE SET
                profile_id = excluded.profile_id,
                display_name = excluded.display_name,
                identity_mode = excluded.identity_mode,
                personality_preset = excluded.personality_preset,
                initiative = excluded.initiative,
                relational_stance = excluded.relational_stance,
                voice_contract = excluded.voice_contract,
                working_style_contract = excluded.working_style_contract,
                charter_extension = excluded.charter_extension,
                governance_flags_json = excluded.governance_flags_json,
                source_manifest_path = excluded.source_manifest_path,
                source_clone_path = excluded.source_clone_path,
                updated_at = excluded.updated_at
            """,
            (
                record.clone_id,
                record.profile_id,
                record.display_name,
                record.identity_mode,
                record.personality_preset,
                record.initiative,
                record.relational_stance,
                record.voice_contract,
                record.working_style_contract,
                record.charter_extension,
                _json_text(record.governance_flags),
                record.source_manifest_path,
                record.source_clone_path,
                created_at,
                timestamp,
            ),
        )
        connection.commit()

def load_clone_identity(self, clone_id: str) -> CloneIdentityRecord | None:
    with self.connection() as connection:
        row = connection.execute(
            """
            SELECT clone_id, profile_id, display_name, identity_mode,
                   personality_preset, initiative, relational_stance,
                   voice_contract, working_style_contract, charter_extension,
                   governance_flags_json, source_manifest_path,
                   source_clone_path, created_at, updated_at
            FROM clone_identities
            WHERE clone_id = ?
            """,
            (clone_id,),
        ).fetchone()
    return _clone_identity_from_row(row) if row is not None else None

def load_clone_identity_for_profile(self, profile_id: str) -> CloneIdentityRecord | None:
    with self.connection() as connection:
        row = connection.execute(
            """
            SELECT clone_id, profile_id, display_name, identity_mode,
                   personality_preset, initiative, relational_stance,
                   voice_contract, working_style_contract, charter_extension,
                   governance_flags_json, source_manifest_path,
                   source_clone_path, created_at, updated_at
            FROM clone_identities
            WHERE profile_id = ?
            ORDER BY updated_at DESC, created_at DESC
            LIMIT 1
            """,
            (profile_id,),
        ).fetchone()
    return _clone_identity_from_row(row) if row is not None else None

def upsert_user_card(
    self,
    record: UserCardRecord,
    *,
    updated_at: datetime | None = None,
) -> None:
    timestamp = _iso(updated_at or record.updated_at or record.created_at)
    created_at = timestamp
    with self.connection() as connection:
        existing = connection.execute(
            "SELECT created_at FROM user_cards WHERE user_card_id = ?",
            (record.user_card_id,),
        ).fetchone()
        if existing is not None:
            created_at = str(existing["created_at"])
        connection.execute(
            """
            INSERT INTO user_cards (
                user_card_id,
                profile_id,
                preferred_name,
                locale,
                timezone,
                communication_preferences_json,
                boundaries_json,
                biography_fragments_json,
                durable_notes_json,
                shared_preferences_json,
                source_user_profile_path,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_card_id) DO UPDATE SET
                profile_id = excluded.profile_id,
                preferred_name = excluded.preferred_name,
                locale = excluded.locale,
                timezone = excluded.timezone,
                communication_preferences_json = excluded.communication_preferences_json,
                boundaries_json = excluded.boundaries_json,
                biography_fragments_json = excluded.biography_fragments_json,
                durable_notes_json = excluded.durable_notes_json,
                shared_preferences_json = excluded.shared_preferences_json,
                source_user_profile_path = excluded.source_user_profile_path,
                updated_at = excluded.updated_at
            """,
            (
                record.user_card_id,
                record.profile_id,
                record.preferred_name,
                record.locale,
                record.timezone,
                _json_text(record.communication_preferences),
                _json_text(record.boundaries),
                _json_text(record.biography_fragments),
                _json_text(record.durable_notes),
                _json_text(record.shared_preferences),
                record.source_user_profile_path,
                created_at,
                timestamp,
            ),
        )
        connection.commit()

def load_user_card(self, user_card_id: str) -> UserCardRecord | None:
    with self.connection() as connection:
        row = connection.execute(
            """
            SELECT user_card_id, profile_id, preferred_name, locale, timezone,
                   communication_preferences_json, boundaries_json,
                   biography_fragments_json, durable_notes_json, shared_preferences_json,
                   source_user_profile_path, created_at, updated_at
            FROM user_cards
            WHERE user_card_id = ?
            """,
            (user_card_id,),
        ).fetchone()
    return _user_card_from_row(row) if row is not None else None

def load_user_card_for_profile(self, profile_id: str) -> UserCardRecord | None:
    with self.connection() as connection:
        row = connection.execute(
            """
            SELECT user_card_id, profile_id, preferred_name, locale, timezone,
                   communication_preferences_json, boundaries_json,
                   biography_fragments_json, durable_notes_json, shared_preferences_json,
                   source_user_profile_path, created_at, updated_at
            FROM user_cards
            WHERE profile_id = ?
            ORDER BY updated_at DESC, created_at DESC
            LIMIT 1
            """,
            (profile_id,),
        ).fetchone()
    return _user_card_from_row(row) if row is not None else None

def upsert_relationship_memory(
    self,
    record: RelationshipMemoryRecord,
    *,
    updated_at: datetime | None = None,
) -> None:
    timestamp = _iso(updated_at or record.updated_at or record.created_at)
    created_at = timestamp
    with self.connection() as connection:
        existing = connection.execute(
            "SELECT created_at FROM relationship_memories WHERE relationship_id = ?",
            (record.relationship_id,),
        ).fetchone()
        if existing is not None:
            created_at = str(existing["created_at"])
        connection.execute(
            """
            INSERT INTO relationship_memories (
                relationship_id,
                profile_id,
                clone_id,
                user_card_id,
                interaction_preferences_json,
                repair_history_json,
                trust_markers_json,
                expectations_json,
                local_corrections_json,
                continuity_notes_json,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(relationship_id) DO UPDATE SET
                profile_id = excluded.profile_id,
                clone_id = excluded.clone_id,
                user_card_id = excluded.user_card_id,
                interaction_preferences_json = excluded.interaction_preferences_json,
                repair_history_json = excluded.repair_history_json,
                trust_markers_json = excluded.trust_markers_json,
                expectations_json = excluded.expectations_json,
                local_corrections_json = excluded.local_corrections_json,
                continuity_notes_json = excluded.continuity_notes_json,
                updated_at = excluded.updated_at
            """,
            (
                record.relationship_id,
                record.profile_id,
                record.clone_id,
                record.user_card_id,
                _json_text(record.interaction_preferences),
                _json_text(record.repair_history),
                _json_text(record.trust_markers),
                _json_text(record.expectations),
                _json_text(record.local_corrections),
                _json_text(record.continuity_notes),
                created_at,
                timestamp,
            ),
        )
        connection.commit()

def load_relationship_memory(self, relationship_id: str) -> RelationshipMemoryRecord | None:
    with self.connection() as connection:
        row = connection.execute(
            """
            SELECT relationship_id, profile_id, clone_id, user_card_id,
                   interaction_preferences_json, repair_history_json,
                   trust_markers_json, expectations_json,
                   local_corrections_json, continuity_notes_json,
                   created_at, updated_at
            FROM relationship_memories
            WHERE relationship_id = ?
            """,
            (relationship_id,),
        ).fetchone()
    return _relationship_memory_from_row(row) if row is not None else None

def load_relationship_memory_for_profile(self, profile_id: str) -> RelationshipMemoryRecord | None:
    with self.connection() as connection:
        row = connection.execute(
            """
            SELECT relationship_id, profile_id, clone_id, user_card_id,
                   interaction_preferences_json, repair_history_json,
                   trust_markers_json, expectations_json,
                   local_corrections_json, continuity_notes_json,
                   created_at, updated_at
            FROM relationship_memories
            WHERE profile_id = ?
            ORDER BY updated_at DESC, created_at DESC
            LIMIT 1
            """,
            (profile_id,),
        ).fetchone()
    return _relationship_memory_from_row(row) if row is not None else None

def load_profile_graph(self, profile_id: str) -> ProfileGraph | None:
    profile = self.load_profile(profile_id)
    clone_identity = self.load_clone_identity_for_profile(profile_id)
    user_card = self.load_user_card_for_profile(profile_id)
    relationship_memory = self.load_relationship_memory_for_profile(profile_id)
    if (
        profile is None
        or clone_identity is None
        or user_card is None
        or relationship_memory is None
    ):
        return None
    return ProfileGraph(
        profile=profile,
        clone_identity=clone_identity,
        user_card=user_card,
        relationship_memory=relationship_memory,
    )

def canonical_cutover_manifest(self) -> StorageCutoverManifest:
    return StorageCutoverManifest(
        schema_version=MIGRATION_VERSION,
        migration_version=MIGRATION_VERSION,
        migration_file=MIGRATIONS[MIGRATION_VERSION].name,
        index_version_policy=(
            "bump MIGRATION_VERSION and add a numbered SQL migration whenever a canonical row family or its indexes change"
        ),
        row_families=(
            CanonicalRowFamily(
                owner="profile",
                graph_contract="ProfileGraph",
                record_contracts=(
                    "ProfileState",
                    "CloneIdentityRecord",
                    "UserCardRecord",
                    "RelationshipMemoryRecord",
                ),
                state_tables=(
                    "profiles",
                    "clone_identities",
                    "user_cards",
                    "relationship_memories",
                ),
                ledger_tables=(
                    "identity_ledger_entries",
                    "user_card_ledger_entries",
                    "relationship_ledger_entries",
                ),
                index_names=(
                    "idx_clone_identities_profile_id",
                    "idx_user_cards_profile_id",
                    "idx_relationship_memories_profile_id",
                    "idx_relationship_memories_clone_id",
                    "idx_identity_ledger_entries_clone_created",
                    "idx_user_card_ledger_entries_card_created",
                    "idx_relationship_ledger_entries_rel_created",
                ),
                status="active-bridge",
                notes="Retired profile-file ownership has been replaced by structured profile rows and ledgers.",
            ),
            CanonicalRowFamily(
                owner="activity",
                graph_contract="ActivityGraph",
                record_contracts=("SessionState", "GoalNode"),
                state_tables=("sessions", "activity_graphs", "activity_nodes"),
                ledger_tables=("activity_lifecycle_events",),
                index_names=(
                    "idx_sessions_profile_id",
                    "idx_sessions_parent_session_id",
                    "idx_activity_graphs_revision",
                    "idx_activity_nodes_session_order",
                    "idx_activity_nodes_status",
                    "idx_activity_lifecycle_events_goal",
                ),
                notes="goal-state rows are the current canonical durable activity owner projection; downstream runtime reconciliation should write through these rows only.",
            ),
            CanonicalRowFamily(
                owner="evidence",
                graph_contract="EvidenceGraph",
                record_contracts=("MemoryRecord", "ArtifactRecord"),
                state_tables=("memories", "artifacts"),
                ledger_tables=("memory_ledger_entries",),
                index_names=(
                    "idx_memory_ledger_entries_session_created",
                    "idx_memories_session_state_created",
                    "idx_memories_state_created",
                    "idx_artifacts_session_created",
                ),
                status="active",
                notes="memory and artifact rows are the canonical durable evidence owner and should be read back through the graph contract.",
            ),
            CanonicalRowFamily(
                owner="procedure",
                graph_contract="ProcedureLibrary",
                record_contracts=("ProcedureLibrary", "ProcedureRecord", "ProcedureStep"),
                state_tables=("procedure_libraries", "procedures", "procedure_steps"),
                ledger_tables=(),
                index_names=(
                    "idx_procedures_profile_status",
                    "idx_procedure_steps_procedure_order",
                ),
                status="active",
                notes="procedure promotion now persists through dedicated library, procedure, and step rows; experiences remain historical input only.",
            ),
        ),
        legacy_mappings=(
            LegacyOwnerCutover(
                legacy_surface="legacy.clone-charter-file",
                canonical_owner="ProfileGraph.clone_identity",
                disposition="retired",
                notes="clone charter ownership now belongs to canonical identity rows only.",
            ),
            LegacyOwnerCutover(
                legacy_surface="legacy.user-profile-file",
                canonical_owner="ProfileGraph.user_card + ProfileGraph.relationship_memory",
                disposition="retired",
                notes="shared user and relationship truth now belongs to canonical rows only.",
            ),
            LegacyOwnerCutover(
                legacy_surface="packages/profile",
                canonical_owner="ProfileGraph",
                disposition="bridge-and-projection",
                notes="profile package may keep bridge helpers, but durable truth must round-trip through structured rows and ledgers.",
            ),
            LegacyOwnerCutover(
                legacy_surface="packages/planning.GoalGraph",
                canonical_owner="ActivityGraph",
                disposition="rename-toward-canonical",
                notes="existing goal graph behavior maps to the clean-slate work owner and should converge on the canonical graph contract.",
            ),
            LegacyOwnerCutover(
                legacy_surface="packages/memory",
                canonical_owner="EvidenceGraph via packages/evidence",
                disposition="removed-after-cutover",
                notes="the transitional memory package is deleted; durable memory runtime, ledgers, and retrieval helpers now live under packages/evidence.",
            ),
            LegacyOwnerCutover(
                legacy_surface="packages/experience",
                canonical_owner="ProcedureLibrary",
                disposition="deprecate-as-owner",
                notes="experience rows are historical outcome evidence today and should not remain the durable owner once procedure storage lands.",
            ),
        ),
    )

def append_identity_ledger(
    self,
    entry: StoredIdentityLedgerEntry,
    *,
    created_at: datetime | None = None,
) -> None:
    timestamp = _iso(created_at or entry.created_at)
    created_value = timestamp
    with self.connection() as connection:
        existing = connection.execute(
            "SELECT created_at FROM identity_ledger_entries WHERE entry_id = ?",
            (entry.entry_id,),
        ).fetchone()
        if existing is not None:
            created_value = str(existing["created_at"])
        connection.execute(
            """
            INSERT INTO identity_ledger_entries (
                entry_id,
                clone_id,
                profile_id,
                action,
                summary,
                metadata_json,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(entry_id) DO UPDATE SET
                clone_id = excluded.clone_id,
                profile_id = excluded.profile_id,
                action = excluded.action,
                summary = excluded.summary,
                metadata_json = excluded.metadata_json
            """,
            (
                entry.entry_id,
                entry.clone_id,
                entry.profile_id,
                entry.action,
                entry.summary,
                _json_mapping(dict(entry.metadata)),
                created_value,
            ),
        )
        connection.commit()

def list_identity_ledger(self, clone_id: str | None = None) -> tuple[StoredIdentityLedgerEntry, ...]:
    with self.connection() as connection:
        if clone_id is None:
            rows = connection.execute(
                """
                SELECT entry_id, clone_id, profile_id, action, summary,
                       metadata_json, created_at
                FROM identity_ledger_entries
                ORDER BY created_at ASC, entry_id ASC
                """
            ).fetchall()
        else:
            rows = connection.execute(
                """
                SELECT entry_id, clone_id, profile_id, action, summary,
                       metadata_json, created_at
                FROM identity_ledger_entries
                WHERE clone_id = ?
                ORDER BY created_at ASC, entry_id ASC
                """,
                (clone_id,),
            ).fetchall()
    return tuple(_identity_ledger_from_row(row) for row in rows)

def append_user_card_ledger(
    self,
    entry: StoredUserCardLedgerEntry,
    *,
    created_at: datetime | None = None,
) -> None:
    timestamp = _iso(created_at or entry.created_at)
    created_value = timestamp
    with self.connection() as connection:
        existing = connection.execute(
            "SELECT created_at FROM user_card_ledger_entries WHERE entry_id = ?",
            (entry.entry_id,),
        ).fetchone()
        if existing is not None:
            created_value = str(existing["created_at"])
        connection.execute(
            """
            INSERT INTO user_card_ledger_entries (
                entry_id,
                user_card_id,
                profile_id,
                action,
                summary,
                metadata_json,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(entry_id) DO UPDATE SET
                user_card_id = excluded.user_card_id,
                profile_id = excluded.profile_id,
                action = excluded.action,
                summary = excluded.summary,
                metadata_json = excluded.metadata_json
            """,
            (
                entry.entry_id,
                entry.user_card_id,
                entry.profile_id,
                entry.action,
                entry.summary,
                _json_mapping(dict(entry.metadata)),
                created_value,
            ),
        )
        connection.commit()

def list_user_card_ledger(self, user_card_id: str | None = None) -> tuple[StoredUserCardLedgerEntry, ...]:
    with self.connection() as connection:
        if user_card_id is None:
            rows = connection.execute(
                """
                SELECT entry_id, user_card_id, profile_id, action, summary,
                       metadata_json, created_at
                FROM user_card_ledger_entries
                ORDER BY created_at ASC, entry_id ASC
                """
            ).fetchall()
        else:
            rows = connection.execute(
                """
                SELECT entry_id, user_card_id, profile_id, action, summary,
                       metadata_json, created_at
                FROM user_card_ledger_entries
                WHERE user_card_id = ?
                ORDER BY created_at ASC, entry_id ASC
                """,
                (user_card_id,),
            ).fetchall()
    return tuple(_user_card_ledger_from_row(row) for row in rows)

def append_relationship_ledger(
    self,
    entry: StoredRelationshipLedgerEntry,
    *,
    created_at: datetime | None = None,
) -> None:
    timestamp = _iso(created_at or entry.created_at)
    created_value = timestamp
    with self.connection() as connection:
        existing = connection.execute(
            "SELECT created_at FROM relationship_ledger_entries WHERE entry_id = ?",
            (entry.entry_id,),
        ).fetchone()
        if existing is not None:
            created_value = str(existing["created_at"])
        connection.execute(
            """
            INSERT INTO relationship_ledger_entries (
                entry_id,
                relationship_id,
                profile_id,
                action,
                summary,
                metadata_json,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(entry_id) DO UPDATE SET
                relationship_id = excluded.relationship_id,
                profile_id = excluded.profile_id,
                action = excluded.action,
                summary = excluded.summary,
                metadata_json = excluded.metadata_json
            """,
            (
                entry.entry_id,
                entry.relationship_id,
                entry.profile_id,
                entry.action,
                entry.summary,
                _json_mapping(dict(entry.metadata)),
                created_value,
            ),
        )
        connection.commit()

def list_relationship_ledger(
    self,
    relationship_id: str | None = None,
) -> tuple[StoredRelationshipLedgerEntry, ...]:
    with self.connection() as connection:
        if relationship_id is None:
            rows = connection.execute(
                """
                SELECT entry_id, relationship_id, profile_id, action, summary,
                       metadata_json, created_at
                FROM relationship_ledger_entries
                ORDER BY created_at ASC, entry_id ASC
                """
            ).fetchall()
        else:
            rows = connection.execute(
                """
                SELECT entry_id, relationship_id, profile_id, action, summary,
                       metadata_json, created_at
                FROM relationship_ledger_entries
                WHERE relationship_id = ?
                ORDER BY created_at ASC, entry_id ASC
                """,
                (relationship_id,),
            ).fetchall()
    return tuple(_relationship_ledger_from_row(row) for row in rows)
