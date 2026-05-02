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

def upsert_session(self, session: SessionState, *, resume_count_delta: int = 0) -> None:
    with self.connection() as connection:
        connection.execute(
            """
            INSERT INTO sessions (
                session_id,
                profile_id,
                workspace_id,
                status,
                started_at,
                updated_at,
                parent_session_id,
                interruption_state,
                resume_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(session_id) DO UPDATE SET
                profile_id = excluded.profile_id,
                workspace_id = excluded.workspace_id,
                status = excluded.status,
                started_at = excluded.started_at,
                updated_at = excluded.updated_at,
                parent_session_id = excluded.parent_session_id,
                interruption_state = excluded.interruption_state,
                resume_count = sessions.resume_count + ?
            """,
            (
                session.session_id,
                session.profile_id,
                session.workspace_id,
                session.status,
                _iso(session.started_at),
                _iso(session.updated_at),
                session.parent_session_id,
                session.interruption_state,
                resume_count_delta,
                resume_count_delta,
            ),
        )
        connection.commit()

def load_session(self, session_id: str) -> SessionState | None:
    with self.connection() as connection:
        row = connection.execute(
            """
            SELECT session_id, profile_id, workspace_id, status, started_at,
                   updated_at, parent_session_id, interruption_state
            FROM sessions
            WHERE session_id = ?
            """,
            (session_id,),
        ).fetchone()
    if row is None:
        return None
    return SessionState(
        session_id=str(row["session_id"]),
        profile_id=str(row["profile_id"]),
        workspace_id=str(row["workspace_id"]) if row["workspace_id"] is not None else None,
        status=str(row["status"]),
        started_at=_parse_datetime(str(row["started_at"])),
        updated_at=_parse_datetime(str(row["updated_at"])),
        parent_session_id=str(row["parent_session_id"]) if row["parent_session_id"] is not None else None,
        interruption_state=str(row["interruption_state"]) if row["interruption_state"] is not None else None,
    )

def upsert_activity_graph(self, graph: ActivityGraph) -> None:
    work_graph = graph
    timestamp = _iso(work_graph.updated_at or _utc_now())
    with self.connection() as connection:
        existing_graph = connection.execute(
            """
            SELECT created_at
            FROM activity_graphs
            WHERE session_id = ?
            """,
            (work_graph.session_id,),
        ).fetchone()
        created_at = str(existing_graph["created_at"]) if existing_graph is not None else timestamp

        connection.execute(
            """
            INSERT INTO activity_graphs (
                session_id,
                root_goal_id,
                active_goal_id,
                revision_id,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(session_id) DO UPDATE SET
                root_goal_id = excluded.root_goal_id,
                active_goal_id = excluded.active_goal_id,
                revision_id = excluded.revision_id,
                updated_at = excluded.updated_at
            """,
            (
                work_graph.session_id,
                work_graph.root_goal_id,
                work_graph.active_goal_id,
                work_graph.revision_id,
                created_at,
                timestamp,
            ),
        )

        existing_goal_rows = connection.execute(
            """
            SELECT goal_id, status, revision_id, created_at
            FROM activity_nodes
            WHERE session_id = ?
            """,
            (work_graph.session_id,),
        ).fetchall()
        existing_by_goal_id = {str(row["goal_id"]): row for row in existing_goal_rows}

        for goal_order, goal in enumerate(work_graph.goals):
            previous = existing_by_goal_id.get(goal.goal_id)
            goal_created_at = str(previous["created_at"]) if previous is not None else timestamp
            goal_updated_at = _iso(goal.updated_at or _utc_now())
            connection.execute(
                """
                INSERT INTO activity_nodes (
                    goal_id,
                    session_id,
                    goal_order,
                    title,
                    status,
                    priority,
                    owner,
                    parent_goal_id,
                    dependency_refs_json,
                    evidence_refs_json,
                    related_memory_ids_json,
                    deadline,
                    time_sensitivity,
                    review_checkpoint,
                    revision_id,
                    created_at,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(session_id, goal_id) DO UPDATE SET
                    goal_order = excluded.goal_order,
                    title = excluded.title,
                    status = excluded.status,
                    priority = excluded.priority,
                    owner = excluded.owner,
                    parent_goal_id = excluded.parent_goal_id,
                    dependency_refs_json = excluded.dependency_refs_json,
                    evidence_refs_json = excluded.evidence_refs_json,
                    related_memory_ids_json = excluded.related_memory_ids_json,
                    deadline = excluded.deadline,
                    time_sensitivity = excluded.time_sensitivity,
                    review_checkpoint = excluded.review_checkpoint,
                    revision_id = excluded.revision_id,
                    updated_at = excluded.updated_at
                """,
                (
                    goal.goal_id,
                    work_graph.session_id,
                    goal_order,
                    goal.title,
                    goal.status,
                    goal.priority,
                    goal.owner,
                    goal.parent_goal_id,
                    _json_text(goal.dependencies),
                    _json_text(goal.evidence_refs),
                    _json_text(goal.related_memory_ids),
                    goal.deadline.isoformat() if goal.deadline is not None else None,
                    goal.time_sensitivity,
                    goal.review_checkpoint,
                    goal.revision_id,
                    goal_created_at,
                    goal_updated_at,
                ),
            )
            if previous is not None and str(previous["status"]) != goal.status:
                connection.execute(
                    """
                    INSERT INTO activity_lifecycle_events (
                        event_id,
                        session_id,
                        goal_id,
                        from_status,
                        to_status,
                        reason,
                        revision_id,
                        metadata_json,
                        created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(event_id) DO UPDATE SET
                        from_status = excluded.from_status,
                        to_status = excluded.to_status,
                        reason = excluded.reason,
                        revision_id = excluded.revision_id,
                        metadata_json = excluded.metadata_json
                    """,
                    (
                        f"{work_graph.session_id}:{goal.goal_id}:{goal_updated_at}:{goal.status}",
                        work_graph.session_id,
                        goal.goal_id,
                        str(previous["status"]),
                        goal.status,
                        None,
                        goal.revision_id,
                        _json_dict_text(
                            {
                                "goal_order": goal_order,
                                "title": goal.title,
                                "priority": goal.priority,
                                "owner": goal.owner,
                            }
                        ),
                        goal_updated_at,
                    ),
                )
        connection.commit()

def load_activity_graph(self, session_id: str) -> ActivityGraph | None:
    with self.connection() as connection:
        graph_row = connection.execute(
            """
            SELECT session_id, root_goal_id, active_goal_id, revision_id, updated_at
            FROM activity_graphs
            WHERE session_id = ?
            """,
            (session_id,),
        ).fetchone()
        goal_rows = connection.execute(
            """
            SELECT goal_id, session_id, goal_order, title, status, priority, owner,
                   parent_goal_id, dependency_refs_json, evidence_refs_json,
                   related_memory_ids_json, deadline, time_sensitivity,
                   review_checkpoint, revision_id, updated_at
            FROM activity_nodes
            WHERE session_id = ?
            ORDER BY goal_order ASC, goal_id ASC
            """,
            (session_id,),
        ).fetchall()

    if graph_row is None and not goal_rows:
        return None

    return ActivityGraph(
        session_id=session_id,
        root_goal_id=graph_row["root_goal_id"] if graph_row is not None else None,
        active_goal_id=graph_row["active_goal_id"] if graph_row is not None else None,
        revision_id=graph_row["revision_id"] if graph_row is not None else None,
        goals=tuple(
            GoalNode(
                goal_id=str(row["goal_id"]),
                session_id=str(row["session_id"]),
                title=str(row["title"]),
                status=str(row["status"]),
                priority=str(row["priority"]),
                dependencies=_tuple_text(str(row["dependency_refs_json"])),
                evidence_refs=_tuple_text(str(row["evidence_refs_json"])),
                owner=str(row["owner"]) if row["owner"] is not None else None,
                parent_goal_id=str(row["parent_goal_id"]) if row["parent_goal_id"] is not None else None,
                related_memory_ids=_tuple_text(str(row["related_memory_ids_json"])),
                deadline=_parse_datetime(str(row["deadline"])) if row["deadline"] is not None else None,
                time_sensitivity=str(row["time_sensitivity"]) if row["time_sensitivity"] is not None else None,
                review_checkpoint=str(row["review_checkpoint"]) if row["review_checkpoint"] is not None else None,
                revision_id=str(row["revision_id"]) if row["revision_id"] is not None else None,
                updated_at=_parse_datetime(str(row["updated_at"])) if row["updated_at"] is not None else None,
            )
            for row in goal_rows
        ),
    )

def record_resume(self, parent_session_id: str, child_session_id: str, resumed_at: datetime) -> None:
    with self.connection() as connection:
        connection.execute(
            """
            INSERT INTO session_lineage(parent_session_id, child_session_id, resumed_at)
            VALUES (?, ?, ?)
            ON CONFLICT(child_session_id) DO UPDATE SET
                parent_session_id = excluded.parent_session_id,
                resumed_at = excluded.resumed_at
            """,
            (parent_session_id, child_session_id, _iso(resumed_at)),
        )
        parent = connection.execute(
            "SELECT resume_count FROM sessions WHERE session_id = ?",
            (parent_session_id,),
        ).fetchone()
        if parent is not None:
            connection.execute(
                """
                UPDATE sessions
                SET status = ?, updated_at = ?, resume_count = resume_count + 1
                WHERE session_id = ?
                """,
                ("resumed", _iso(resumed_at), parent_session_id),
            )
        connection.commit()

def lineage(self, session_id: str) -> tuple[SessionState, ...]:
    session = self.load_session(session_id)
    if session is None:
        return ()
    chain = [session]
    current = session
    while current.parent_session_id is not None:
        parent = self.load_session(current.parent_session_id)
        if parent is None:
            break
        chain.append(parent)
        current = parent
    return tuple(reversed(chain))

def refresh_session(
    self,
    session_id: str,
    *,
    status: str | None = None,
    interruption_state: str | None = None,
    updated_at: datetime | None = None,
) -> SessionState:
    current = self.load_session(session_id)
    if current is None:
        raise KeyError(session_id)
    updated = replace(
        current,
        status=status if status is not None else current.status,
        interruption_state=(
            interruption_state if interruption_state is not None else current.interruption_state
        ),
        updated_at=updated_at or _utc_now(),
    )
    self.upsert_session(updated)
    return updated

def _table_exists(connection: sqlite3.Connection, table: str) -> bool:
    row = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name = ?",
        (table,),
    ).fetchone()
    return row is not None

def _delete_from_existing_table(
    connection: sqlite3.Connection,
    table: str,
    where_sql: str,
    parameters: tuple[object, ...],
    *,
    required_tables: tuple[str, ...] = (),
) -> None:
    if not _table_exists(connection, table):
        return
    if any(not _table_exists(connection, required_table) for required_table in required_tables):
        return
    connection.execute(f"DELETE FROM {table} WHERE {where_sql}", parameters)

def _delete_orphaned_profiles(connection: sqlite3.Connection, profile_ids: tuple[str, ...]) -> int:
    if not profile_ids:
        return 0
    placeholders = ", ".join("?" for _ in profile_ids)
    rows = connection.execute(
        f"""
        SELECT profile_id
        FROM profiles
        WHERE profile_id IN ({placeholders})
          AND profile_id NOT IN (SELECT DISTINCT profile_id FROM sessions)
        """,
        profile_ids,
    ).fetchall()
    orphaned_profile_ids = tuple(str(row["profile_id"]) for row in rows)
    if not orphaned_profile_ids:
        return 0
    profile_placeholders = ", ".join("?" for _ in orphaned_profile_ids)
    profile_filter = f"profile_id IN ({profile_placeholders})"

    _delete_from_existing_table(connection, "token_usage_events", profile_filter, orphaned_profile_ids)
    _delete_from_existing_table(connection, "experiences", profile_filter, orphaned_profile_ids)
    _delete_from_existing_table(connection, "verification_bundles", profile_filter, orphaned_profile_ids)
    _delete_from_existing_table(connection, "profile_growth", profile_filter, orphaned_profile_ids)
    _delete_from_existing_table(
        connection,
        "procedure_steps",
        f"procedure_id IN (SELECT procedure_id FROM procedures WHERE {profile_filter})",
        orphaned_profile_ids,
        required_tables=("procedures",),
    )
    _delete_from_existing_table(connection, "procedures", profile_filter, orphaned_profile_ids)
    _delete_from_existing_table(connection, "procedure_libraries", profile_filter, orphaned_profile_ids)
    _delete_from_existing_table(
        connection,
        "auth_secret_values",
        f"reference_id IN (SELECT reference_id FROM auth_secret_references WHERE {profile_filter})",
        orphaned_profile_ids,
        required_tables=("auth_secret_references",),
    )
    _delete_from_existing_table(connection, "auth_secret_references", profile_filter, orphaned_profile_ids)
    _delete_from_existing_table(connection, "auth_profiles", profile_filter, orphaned_profile_ids)
    _delete_from_existing_table(connection, "provider_auth_states", profile_filter, orphaned_profile_ids)
    _delete_from_existing_table(connection, "identity_ledger_entries", profile_filter, orphaned_profile_ids)
    _delete_from_existing_table(connection, "user_card_ledger_entries", profile_filter, orphaned_profile_ids)
    _delete_from_existing_table(connection, "relationship_ledger_entries", profile_filter, orphaned_profile_ids)
    _delete_from_existing_table(connection, "relationship_memories", profile_filter, orphaned_profile_ids)
    _delete_from_existing_table(connection, "user_cards", profile_filter, orphaned_profile_ids)
    _delete_from_existing_table(connection, "clone_identities", profile_filter, orphaned_profile_ids)
    deleted = connection.execute(
        f"DELETE FROM profiles WHERE {profile_filter}",
        orphaned_profile_ids,
    ).rowcount
    return max(0, deleted)

def delete_orphaned_profiles(self, profile_ids: tuple[str, ...]) -> int:
    with self.connection() as connection:
        deleted = _delete_orphaned_profiles(connection, profile_ids)
        connection.commit()
    return deleted

def delete_sessions(
    self,
    session_ids: tuple[str, ...],
    *,
    delete_orphaned_profiles: bool = False,
) -> int:
    if not session_ids:
        return 0
    placeholders = ", ".join("?" for _ in session_ids)
    with self.connection() as connection:
        profile_rows = connection.execute(
            f"SELECT DISTINCT profile_id FROM sessions WHERE session_id IN ({placeholders})",
            session_ids,
        ).fetchall()
        profile_ids = tuple(str(row["profile_id"]) for row in profile_rows if row["profile_id"] is not None)
        connection.execute(
            f"""
            DELETE FROM session_lineage
            WHERE parent_session_id IN ({placeholders})
               OR child_session_id IN ({placeholders})
            """,
            session_ids + session_ids,
        )
        session_filter = f"session_id IN ({placeholders})"
        _delete_from_existing_table(connection, "token_usage_events", session_filter, session_ids)
        _delete_from_existing_table(connection, "agent_run_steps", session_filter, session_ids)
        _delete_from_existing_table(connection, "agent_runs", session_filter, session_ids)
        _delete_from_existing_table(connection, "experiences", session_filter, session_ids)
        _delete_from_existing_table(connection, "artifacts", session_filter, session_ids)
        _delete_from_existing_table(connection, "memory_ledger_entries", session_filter, session_ids)
        _delete_from_existing_table(connection, "memories", session_filter, session_ids)
        _delete_from_existing_table(connection, "activity_lifecycle_events", session_filter, session_ids)
        _delete_from_existing_table(connection, "activity_nodes", session_filter, session_ids)
        _delete_from_existing_table(connection, "activity_graphs", session_filter, session_ids)
        _delete_from_existing_table(connection, "goal_lifecycle_events", session_filter, session_ids)
        _delete_from_existing_table(connection, "goal_nodes", session_filter, session_ids)
        _delete_from_existing_table(connection, "goal_graphs", session_filter, session_ids)
        deleted = connection.execute(
            f"DELETE FROM sessions WHERE session_id IN ({placeholders})",
            session_ids,
        ).rowcount
        if delete_orphaned_profiles:
            _delete_orphaned_profiles(connection, profile_ids)
        connection.commit()
    return deleted
