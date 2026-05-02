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

def append_memory_ledger(self, entry: StoredMemoryLedgerEntry, *, created_at: datetime | None = None) -> None:
    timestamp = _iso(created_at or entry.created_at)
    created_value = timestamp
    with self.connection() as connection:
        existing = connection.execute(
            "SELECT created_at FROM memory_ledger_entries WHERE entry_id = ?",
            (entry.entry_id,),
        ).fetchone()
        if existing is not None:
            created_value = str(existing["created_at"])
        connection.execute(
            """
            INSERT INTO memory_ledger_entries (
                entry_id,
                session_id,
                event_id,
                event_type,
                content,
                kind,
                source_event_id,
                goal_refs_json,
                tags_json,
                metadata_json,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(entry_id) DO UPDATE SET
                session_id = excluded.session_id,
                event_id = excluded.event_id,
                event_type = excluded.event_type,
                content = excluded.content,
                kind = excluded.kind,
                source_event_id = excluded.source_event_id,
                goal_refs_json = excluded.goal_refs_json,
                tags_json = excluded.tags_json,
                metadata_json = excluded.metadata_json
            """,
            (
                entry.entry_id,
                entry.session_id,
                entry.event_id,
                entry.event_type,
                entry.content,
                entry.kind,
                entry.source_event_id,
                _json_text(entry.goal_refs),
                _json_text(entry.tags),
                _json_mapping(dict(entry.metadata)),
                created_value,
            ),
        )
        connection.commit()

def list_memory_ledger(self, session_id: str | None = None) -> tuple[StoredMemoryLedgerEntry, ...]:
    with self.connection() as connection:
        if session_id is None:
            rows = connection.execute(
                """
                SELECT entry_id, session_id, event_id, event_type, content, kind,
                       source_event_id, goal_refs_json, tags_json, metadata_json, created_at
                FROM memory_ledger_entries
                ORDER BY created_at ASC, entry_id ASC
                """
            ).fetchall()
        else:
            rows = connection.execute(
                """
                SELECT entry_id, session_id, event_id, event_type, content, kind,
                       source_event_id, goal_refs_json, tags_json, metadata_json, created_at
                FROM memory_ledger_entries
                WHERE session_id = ?
                ORDER BY created_at ASC, entry_id ASC
                """,
                (session_id,),
            ).fetchall()
    return tuple(_ledger_entry_from_row(row) for row in rows)

def upsert_memory_record(
    self,
    record: StoredMemoryRecord,
    *,
    state: str = "active",
    updated_at: datetime | None = None,
) -> None:
    timestamp = _iso(updated_at or record.created_at)
    created_value = timestamp
    state_value = state
    replacement_memory_id: str | None = None
    with self.connection() as connection:
        existing = connection.execute(
            """
            SELECT created_at, lifecycle_state, replacement_memory_id
            FROM memories
            WHERE memory_id = ?
            """,
            (record.memory_id,),
        ).fetchone()
        if existing is not None:
            created_value = str(existing["created_at"])
            state_value = str(existing["lifecycle_state"])
            replacement_memory_id = (
                str(existing["replacement_memory_id"]) if existing["replacement_memory_id"] is not None else None
            )
        connection.execute(
            """
            INSERT INTO memories (
                memory_id,
                session_id,
                kind,
                content,
                source_event_id,
                goal_refs_json,
                tags_json,
                created_at,
                lifecycle_state,
                replacement_memory_id,
                updated_at,
                metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(memory_id) DO UPDATE SET
                session_id = excluded.session_id,
                kind = excluded.kind,
                content = excluded.content,
                source_event_id = excluded.source_event_id,
                goal_refs_json = excluded.goal_refs_json,
                tags_json = excluded.tags_json,
                lifecycle_state = excluded.lifecycle_state,
                replacement_memory_id = excluded.replacement_memory_id,
                updated_at = excluded.updated_at,
                metadata_json = excluded.metadata_json
            """,
            (
                record.memory_id,
                record.session_id,
                record.kind,
                record.content,
                record.source_event_id,
                _json_text(record.goal_refs),
                _json_text(record.tags),
                created_value,
                state_value,
                replacement_memory_id,
                timestamp,
                _json_dict_text(dict(record.metadata)),
            ),
        )
        connection.commit()

def load_memory_record(self, memory_id: str) -> StoredMemoryRecord | None:
    with self.connection() as connection:
        row = connection.execute(
            """
            SELECT memory_id, session_id, kind, content, source_event_id,
                   goal_refs_json, tags_json, created_at, metadata_json
            FROM memories
            WHERE memory_id = ?
            """,
            (memory_id,),
        ).fetchone()
    if row is None:
        return None
    return _record_from_row(row)

def list_memory_records(
    self,
    session_id: str | None = None,
    *,
    include_inactive: bool = False,
) -> tuple[StoredMemoryRecord, ...]:
    clauses = []
    params: list[str] = []
    if session_id is not None:
        clauses.append("session_id = ?")
        params.append(session_id)
    if not include_inactive:
        clauses.append("lifecycle_state = 'active'")
    where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with self.connection() as connection:
        rows = connection.execute(
            f"""
            SELECT memory_id, session_id, kind, content, source_event_id,
                   goal_refs_json, tags_json, created_at, metadata_json
            FROM memories
            {where_sql}
            ORDER BY created_at ASC, memory_id ASC
            """,
            tuple(params),
        ).fetchall()
    return tuple(_record_from_row(row) for row in rows)

def upsert_artifact_record(self, artifact: ArtifactRecord, *, updated_at: datetime | None = None) -> None:
    timestamp = _iso(updated_at or artifact.created_at)
    created_value = timestamp
    with self.connection() as connection:
        existing = connection.execute(
            "SELECT created_at FROM artifacts WHERE artifact_id = ?",
            (artifact.artifact_id,),
        ).fetchone()
        if existing is not None:
            created_value = str(existing["created_at"])
        connection.execute(
            """
            INSERT INTO artifacts (
                artifact_id,
                session_id,
                kind,
                name,
                uri,
                checksum,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(artifact_id) DO UPDATE SET
                session_id = excluded.session_id,
                kind = excluded.kind,
                name = excluded.name,
                uri = excluded.uri,
                checksum = excluded.checksum,
                updated_at = excluded.updated_at
            """,
            (
                artifact.artifact_id,
                artifact.session_id,
                artifact.kind,
                artifact.name,
                artifact.uri,
                artifact.checksum,
                created_value,
                timestamp,
            ),
        )
        connection.commit()

def load_artifact_record(self, artifact_id: str) -> ArtifactRecord | None:
    with self.connection() as connection:
        row = connection.execute(
            """
            SELECT artifact_id, session_id, kind, name, uri, checksum, created_at
            FROM artifacts
            WHERE artifact_id = ?
            """,
            (artifact_id,),
        ).fetchone()
    return _artifact_from_row(row) if row is not None else None

def list_artifact_records(self, session_id: str | None = None) -> tuple[ArtifactRecord, ...]:
    with self.connection() as connection:
        if session_id is None:
            rows = connection.execute(
                """
                SELECT artifact_id, session_id, kind, name, uri, checksum, created_at
                FROM artifacts
                ORDER BY created_at ASC, artifact_id ASC
                """
            ).fetchall()
        else:
            rows = connection.execute(
                """
                SELECT artifact_id, session_id, kind, name, uri, checksum, created_at
                FROM artifacts
                WHERE session_id = ?
                ORDER BY created_at ASC, artifact_id ASC
                """,
                (session_id,),
            ).fetchall()
    return tuple(_artifact_from_row(row) for row in rows)

def upsert_evidence_graph(self, graph: EvidenceGraph) -> None:
    for memory in graph.memories:
        self.upsert_memory_record(
            StoredMemoryRecord(
                memory_id=memory.memory_id,
                session_id=memory.session_id,
                kind=memory.kind,
                content=memory.content,
                source_event_id=memory.source_event_id,
                goal_refs=memory.goal_refs,
                tags=memory.tags,
                created_at=memory.created_at,
                metadata=dict(memory.metadata),
            )
        )
    for artifact in graph.artifacts:
        self.upsert_artifact_record(artifact)

def load_evidence_graph(self, session_id: str, *, include_inactive: bool = False) -> EvidenceGraph | None:
    memories = tuple(
        _memory_contract_from_record(record)
        for record in self.list_memory_records(session_id=session_id, include_inactive=include_inactive)
    )
    artifacts = self.list_artifact_records(session_id=session_id)
    if not memories and not artifacts:
        return None
    return EvidenceGraph(session_id=session_id, memories=memories, artifacts=artifacts)

def mark_memory_consolidated(self, source_ids: tuple[str, ...], summary_id: str) -> None:
    if not source_ids:
        return
    with self.connection() as connection:
        for source_id in source_ids:
            connection.execute(
                """
                UPDATE memories
                SET lifecycle_state = ?, replacement_memory_id = ?, updated_at = ?
                WHERE memory_id = ?
                """,
                ("consolidated", summary_id, _iso(None), source_id),
            )
        connection.commit()

def mark_memory_superseded(self, source_id: str, replacement_id: str) -> None:
    with self.connection() as connection:
        connection.execute(
            """
            UPDATE memories
            SET lifecycle_state = ?, replacement_memory_id = ?, updated_at = ?
            WHERE memory_id = ?
            """,
            ("superseded", replacement_id, _iso(None), source_id),
        )
        connection.commit()

def mark_memory_deleted(self, memory_id: str) -> None:
    with self.connection() as connection:
        connection.execute(
            """
            UPDATE memories
            SET lifecycle_state = ?, updated_at = ?
            WHERE memory_id = ?
            """,
            ("deleted", _iso(None), memory_id),
        )
        connection.commit()

def memory_state(self, memory_id: str) -> str | None:
    with self.connection() as connection:
        row = connection.execute(
            "SELECT lifecycle_state FROM memories WHERE memory_id = ?",
            (memory_id,),
        ).fetchone()
    if row is None:
        return None
    return str(row["lifecycle_state"])

def memory_lineage(self, memory_id: str) -> str | None:
    with self.connection() as connection:
        row = connection.execute(
            "SELECT replacement_memory_id FROM memories WHERE memory_id = ?",
            (memory_id,),
        ).fetchone()
    if row is None or row["replacement_memory_id"] is None:
        return None
    return str(row["replacement_memory_id"])
